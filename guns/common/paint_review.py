"""Receiver-only photographic audit for the accepted stamped gun family.

Observations select complete visible receivers independently of image color.
Nothing in this module supplies a texture or modeling input. Camera/light
recipes remain member-owned. Unfitted shots use the Harrow's neutral world.
"""
import hashlib
import json
import math
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

from kit.fonts import find_font
from kit.photo_match import project

LUMA = np.array((.2126, .7152, .0722))


def metrics(rgb):
    a = np.asarray(rgb, float).reshape(-1, 3)
    y = a @ LUMA
    hi = a[y >= np.percentile(y, 90)].mean(0)
    return dict(pixels=len(a), value_p10_p50_p90=np.percentile(a.max(1), (10, 50, 90)).tolist(),
                highlight_rgb=hi.tolist(), highlight_value=float(hi.max()),
                highlight_color=(hi / max(hi.max(), 1)).tolist(),
                value_histogram=np.histogram(a.max(1), bins=32, range=(0, 256))[0].tolist())


def erode(mask):
    return np.asarray(Image.fromarray(np.uint8(mask) * 255).filter(ImageFilter.MinFilter(3))) > 0


def comparison(render, photo):
    errors={}
    for key in ('value_p10_p50_p90','highlight_rgb','highlight_value','highlight_color'):
        observed,target=np.asarray(render[key]),np.asarray(photo[key])
        errors[key]=np.where(target != 0,(observed-target)/np.maximum(target,1e-9),
                            np.where(observed == 0,0,np.inf)).tolist()
    passed=(np.all(np.abs(errors['value_p10_p50_p90']) <= (.15,.10,.15)) and
            all(np.all(np.abs(errors[k]) <= .10) for k in ('highlight_rgb','highlight_value','highlight_color')))
    return errors,bool(passed)


def geometry(base):
    if base.name == 'ak':
        return dict(np.load(base / 'build/value-geometry.npz'))
    d = np.load(base / 'build/value-surfaces.npz')
    return dict(xyz=d['triangles'], uv=d['uvs'], ids=d['parts'] + 1, names=d['names'])


def raster(geo, shot, width, height):
    """Perspective-correct raster of the independently checked delivery surfaces."""
    loc = np.asarray(shot['location']); d = np.asarray(shot['target']) - loc
    camera = [math.atan2(d[1], d[0]), math.atan2(d[2], np.linalg.norm(d[:2])),
              *loc, math.log(shot['lens']), shot.get('roll', 0)]
    xy, depth, _ = project(camera, geo['xyz'].reshape(-1, 3), width, height)
    xy = xy.reshape(-1, 3, 2); depth = depth.reshape(-1, 3)
    zbuffer = np.full((height, width), np.inf)
    owner = np.zeros((height, width), np.int32)
    uv = np.zeros((height, width, 2), np.float32)
    for points, dist, ident, coords in zip(xy, depth, geo['ids'], geo['uv']):
        if min(dist) <= .001:
            continue
        lo = np.maximum(np.floor(points.min(0)).astype(int), 0)
        hi = np.minimum(np.ceil(points.max(0)).astype(int), (width - 1, height - 1))
        if np.any(hi < lo):
            continue
        a, b, c = points
        den = (b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
        if abs(den) < 1e-8:
            continue
        yy, xx = np.mgrid[lo[1]:hi[1]+1, lo[0]:hi[0]+1]
        xx = xx + .5; yy = yy + .5
        wa = ((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den
        wb = ((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den
        wc = 1-wa-wb
        z = 1 / np.maximum(wa/dist[0]+wb/dist[1]+wc/dist[2], 1e-12)
        sl = np.s_[lo[1]:hi[1]+1, lo[0]:hi[0]+1]
        active = (wa >= 0) & (wb >= 0) & (wc >= 0) & (z < zbuffer[sl])
        zbuffer[sl][active] = z[active]; owner[sl][active] = ident
        value = z[..., None] * (wa[..., None]*coords[0]/dist[0] +
                                wb[..., None]*coords[1]/dist[1] + wc[..., None]*coords[2]/dist[2])
        uv[sl][active] = value[active]
    return owner, uv


@lru_cache(maxsize=12)
def cached_raster(base, recipe, width, height, positions=False, outer=False):
    geo=geometry(Path(base))
    if positions:geo['uv']=geo['xyz'][:,:,[1,2]]
    if outer:
        # Compare the photographed outside of a U-shaped molding. Its visible
        # inner channel is a different surface and can otherwise occupy the
        # same object-ID/height band as the exterior photo region.
        tri=geo['xyz'];normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0])
        eligible=normal[:,0]*tri.mean(1)[:,0]>1e-12
        geo['ids']=np.where(eligible,geo['ids'],0)
    return raster(geo,json.loads(recipe),width,height)


def masks(base, spec, shot, width, height):
    if 'render_polygons' in spec:
        mask=Image.new('L',(width,height));draw=ImageDraw.Draw(mask)
        for p in spec['render_polygons']:
            draw.polygon([(x*width,y*height) for x,y in p],fill=255)
        return erode(np.asarray(mask)>0),None
    geo = geometry(base)
    # Camera-only key: light recipes can contain diagnostic metadata.
    recipe=json.dumps({k:shot[k] for k in ('location','target','lens','roll') if k in shot},sort_keys=True)
    ids, uv = cached_raster(str(base),recipe,width,height)
    selected = [i+1 for i, n in enumerate(geo['names']) if str(n).startswith(tuple(spec['prefixes']))]
    mask=np.isin(ids,selected)
    if spec.get('outer_surface'):
        mask &= cached_raster(str(base),recipe,width,height,False,True)[0]>0
    if spec.get('bounds'):
        positions=cached_raster(str(base),recipe,width,height,True)[1]
        for axis,index in (('y',0),('z',1)):
            mask &= positions[:,:,index]>=spec['bounds'].get(axis+'_min',-math.inf)
            mask &= positions[:,:,index]<spec['bounds'].get(axis+'_max',math.inf)
    return erode(mask), uv


def photographic_backdrop(scene,shot,description=None):
    """Comparison-only neutral card behind the asset, illuminated by the fit.

    Its assumed reflectance and distance are explicit, never a painted image
    or a camera-ray emission. No backdrop is included in game delivery.
    """
    import bpy
    from mathutils import Vector
    key='Photographic neutral backing'
    ob=scene.objects.get(key)
    if not description:
        if ob:ob.hide_render=True
        return
    if ob is None:
        mesh=bpy.data.meshes.new(key)
        mesh.from_pydata([(-2,-2,0),(2,-2,0),(2,2,0),(-2,2,0)],[],[(0,1,2,3)])
        ob=bpy.data.objects.new(key,mesh);scene.collection.objects.link(ob);ob['studio']=True
        mat=bpy.data.materials.new(key);mat.use_nodes=True
        ob.data.materials.append(mat)
    ob.hide_render=False
    target=Vector((0,.10,.06));direction=(Vector(shot['location'])-Vector(shot['target'])).normalized()
    ob.location=target-direction*description['distance']
    ob.rotation_euler=direction.to_track_quat('Z','Y').to_euler()
    if description.get('horizontal'):
        ob.location=(0,.10,description['height']);ob.rotation_euler=(0,0,0)
    if description.get('normal'):
        ob.location=description['point']
        ob.rotation_euler=Vector(description['normal']).to_track_quat('Z','Y').to_euler()
    bs=ob.data.materials[0].node_tree.nodes.get('Principled BSDF')
    value=description['albedo'];bs.inputs['Base Color'].default_value=(*(value if isinstance(value,list) else [value]*3),1)
    bs.inputs['Roughness'].default_value=.95;bs.inputs['Specular IOR Level'].default_value=.2


def reference(base, spec):
    photo = np.asarray(Image.open(base / 'build/white-balanced' / spec['photo']).convert('RGB'))
    mask = Image.new('L', (photo.shape[1], photo.shape[0]))
    draw = ImageDraw.Draw(mask)
    for polygon in spec['polygons']:
        draw.polygon([tuple(p) for p in polygon], fill=255)
    # A separate lever, fastener or ink can occlude a photographed material.
    # Object-ID masks exclude those components in the render; explicitly
    # outlined holes make the reference describe the same material.
    for polygon in spec.get('excluded_polygons', []):
        draw.polygon([tuple(p) for p in polygon], fill=0)
    return photo, erode(np.asarray(mask) > 0)


def crop(rgb, mask):
    im = Image.fromarray(np.uint8(rgb)).convert('RGBA')
    im.putalpha(Image.fromarray(np.uint8(mask)*255))
    im = im.crop(im.getbbox())
    bg = Image.new('RGBA', im.size, (108,111,114,255)); bg.alpha_composite(im)
    return ImageOps.contain(bg.convert('RGB'), (840,390), Image.Resampling.LANCZOS)


def audit(base, folder, out, preview=False):
    base, folder, out = map(Path, (base, folder, out)); out.mkdir(parents=True, exist_ok=True)
    specs = json.loads((base / 'src/paint_review.json').read_text())
    meta = json.loads((folder / 'shots.json').read_text()); rows = {}
    neutral = json.loads((base / 'build/white-balanced/corrections.json').read_text())
    font = ImageFont.truetype(find_font('Noto Sans', 'Regular'), 19)
    for name, spec in specs.items():
        if spec['shot'] not in meta:
            continue
        shot = meta[spec['shot']]
        assert hashlib.sha256(Path(shot['source']).read_bytes()).hexdigest() == shot['sha256'], 'Stale paint render'
        if not preview:
            assert Path(shot['source']).suffix == '.glb', 'Judge the exported GLB'
            assert 'REVIEW ONLY' not in shot.get('stage',''), 'A shader diagnostic cannot accept the shipped paint'
        rgb = np.asarray(Image.open(folder / (spec['shot']+'.png')).convert('RGB'))
        mask, _ = masks(base, spec, shot, rgb.shape[1], rgb.shape[0])
        photo, pm = reference(base, spec)
        r, p = metrics(rgb[mask]), metrics(photo[pm])
        errors,passed=comparison(r,p)
        row = dict(render=r, photo=p, relative_errors=errors, within_requested_bounds=bool(passed),
                   observation=spec, neutral=neutral[spec['neutral']], sha256=shot['sha256'], preview=preview)
        if spec.get('height_guards'):
            geo=geometry(base);geo['uv']=geo['xyz'][:,:,[2,1]]
            height=raster(geo,shot,rgb.shape[1],rgb.shape[0])[1][:,:,0]
            row['height_guards']=[]
            for guard in spec['height_guards']:
                selected=mask&(height>=guard.get('z_min',-1))&(height<guard.get('z_max',1))
                ref,rm=reference(base,dict(spec,polygons=guard['polygons']))
                row['height_guards'].append(dict(render=metrics(rgb[selected]),photo=metrics(ref[rm])))
        if spec.get('anchors'):
            row['unchanged_finish_anchors']=[]
            for anchor in spec['anchors']:
                selected,_=masks(base,anchor,shot,rgb.shape[1],rgb.shape[0])
                ref,rm=reference(base,anchor)
                ar,ap=metrics(rgb[selected]),metrics(ref[rm]);ae,passed_anchor=comparison(ar,ap)
                row['unchanged_finish_anchors'].append(dict(render=ar,photo=ap,relative_errors=ae,within_requested_bounds=passed_anchor,observation=anchor))
            row['light_fit_within_requested_bounds']=all(a['within_requested_bounds'] for a in row['unchanged_finish_anchors'])
        rows[name] = row
        canvas = Image.new('RGB',(1800,850),'#e7e9e6'); draw = ImageDraw.Draw(canvas)
        draw.text((25,15), base.name.upper()+' / '+name+' / '+('SOURCE PREVIEW' if preview else 'EXPORTED GLB'),font=font,fill='black')
        canvas.paste(crop(rgb,mask),(25,65)); canvas.paste(crop(photo,pm),(925,65))
        for i,(label,m) in enumerate((('Ours',r),('Balanced photo',p))):
            x=25+i*900
            draw.text((x,480),label+' V10/50/90 '+str(np.round(m['value_p10_p50_p90'],1).tolist()),font=font,fill='black')
            draw.text((x,520),'Highlight RGB '+str(np.round(m['highlight_rgb'],1).tolist()),font=font,fill='black')
            h=np.asarray(m['value_histogram'],float);h/=max(h.max(),1)
            draw.line([(x+10+j*25,740-v*150) for j,v in enumerate(h)],fill=(140,60,30) if i==0 else (30,90,140),width=3)
        draw.text((25,785),'Complete visible part, including accepted wear; one-pixel boundary erosion; no image grading.',font=font,fill='black')
        canvas.save(out/(name+'-histograms.jpg'),quality=94)
        print(base.name,name,'V',r['value_p10_p50_p90'],'/',p['value_p10_p50_p90'],'H',r['highlight_rgb'],'/',p['highlight_rgb'],'PASS',passed,flush=True)
    (out/'finish-values.json').write_text(json.dumps(rows,indent=2)+'\n')
    return rows


def apply_lights(scene, shot, base):
    """One physical, whole-scene rig per photograph; never applies to heroes."""
    import bpy
    from mathutils import Vector
    # Harrow's ordinary studio is neutral, including after a colored photo
    # rig. Reset every shot so its appearance never depends on render order.
    bg = scene.world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (.25,.25,.25,1)
    for ob in scene.objects:
        if ob.type == 'LIGHT' and ob.name.startswith('Paint photographic card'):
            ob.data.energy = 0
    path = Path(base) / 'src/paint_lights.json'
    fits = json.loads(path.read_text()) if path.exists() else {}
    fit = fits.get(shot.get('paint_photo'))
    photographic_backdrop(scene,shot,fit.get('backdrop') if fit else None)
    if not fit:
        return
    for ob in scene.objects:
        if ob.type == 'LIGHT':
            ob.data.energy = 0
    bg.inputs['Strength'].default_value = fit['world']
    bg.inputs['Color'].default_value = (*[.25*c for c in fit['color']],1)
    for i, card in enumerate(fit['lights']):
        key = 'Paint photographic card %02d' % i
        ob = scene.objects.get(key)
        if ob is None:
            data=bpy.data.lights.new(key,'AREA');data.shape='RECTANGLE'
            ob=bpy.data.objects.new(key,data);scene.collection.objects.link(ob)
        ob.hide_render=False;ob.location=card['position'];ob.data.energy=card['power']
        ob.data.size,ob.data.size_y=card['size'];ob.data.color=card.get('color',fit['color'])
        ob.rotation_euler=(Vector(card.get('target',(0,.10,.09)))-ob.location).to_track_quat('-Z','Y').to_euler()
    shot['physical_paint_photo_lights'] = fit
