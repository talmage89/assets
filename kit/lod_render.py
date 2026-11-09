"""Same-camera exported LOD evidence, at actual 1080p switch sizes.

All measurements use full 1920x1080 renders. Review strips crop around the
asset at native scale (never enlarge the switch comparison); close views use
a separate camera. Metrics use union alpha support, not the empty background.
Three azimuths expose front/side/rear silhouette and shading changes. Cycles
uses the same fixed seed and sample count, with denoising disabled. Small
sampling differences remain part of the measured error when geometry changes.
"""
import argparse
import json
import math
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Vector
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit.lod import configuration,image_limits
from kit.lod_io import Document,digest


def setup(source, bounds, azimuth, dist, size=(1920,1080), include=None,foliage=False,elevation=0,samples=None,factory_paint=False):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(source),import_pack_images=False)
    mesh_names={n.get('name') for n in Document(source).data['nodes'] if 'mesh' in n}
    for ob in list(bpy.context.scene.objects):
        if ob.type=='MESH' and ob.name not in mesh_names:bpy.data.objects.remove(ob,do_unlink=True)
    from kit.lod_impostor import pose
    pose(azimuth)
    if include:
        roots=[bpy.data.objects[n] for n in include]
        keep={x for r in roots for x in [r]+list(r.children_recursive)}
        document=Document(source);selected=document.selected_nodes(include)
        for n in document.data['nodes']:
            if selected.intersection(n.get('extras',{}).get('lod_sources',[])):
                if bpy.data.objects.get(n.get('name','')):keep.add(bpy.data.objects[n['name']])
        for o in bpy.context.scene.objects:
            if o.type=='MESH' and o not in keep:o.hide_render=True
    if not foliage:
        from kit.lod_shading import restore
        shading_receipt=restore(Document(source))
    if factory_paint:
        from kit.lod_factory import apply
        apply(lights=True)
    sc=bpy.context.scene;sc.render.engine='CYCLES'
    if not foliage:sc['lod_delivered_frame']=json.dumps(shading_receipt)
    from kit import gpu
    gpu.enable();sc.cycles.samples=samples if samples is not None else (128 if foliage else 24);sc.cycles.seed=23
    sc.cycles.use_denoising=False;sc.cycles.use_adaptive_sampling=False
    sc.cycles.max_bounces=6;sc.cycles.transparent_max_bounces=32
    # Powered canopy lenses produce rare indirect fireflies at checkpoint
    # sample counts. Clamp only indirect radiance, identically for all levels;
    # direct light and the visible emissive lenses keep their delivered values.
    sc.cycles.sample_clamp_indirect=3
    # Restore the maple's published thin-leaf shader from imported maps only.
    for mat in list(bpy.data.materials) if foliage else []:
        if not mat.use_nodes:continue
        if 'leaf' in mat.name.lower() or 'foliage' in mat.name.lower():
            images=[n.image for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]
            named={k:next((i for i in images if k in i.name),None) for k in ('BaseColor','Normal','ORM')}
            if named['BaseColor']:
                from kit.foliage import material
                replacement=material(named['BaseColor'],named['Normal'],named['ORM'])
                for o in sc.objects:
                    if o.type=='MESH':
                        for s in o.material_slots:
                            if s.material==mat:s.material=replacement
    lo,hi=bounds;center=(lo+hi)*.5
    # glTF Y up -> Blender Z up; +Z forward -> Blender -Y.
    target=Vector((center[0],-center[2],center[1]))
    theta=math.radians(azimuth)
    cam=bpy.data.objects.new('LOD review camera',bpy.data.cameras.new('LOD review camera'))
    sc.collection.objects.link(cam);sc.camera=cam
    cam.data.type='PERSP';cam.data.sensor_fit='VERTICAL';cam.data.sensor_height=32
    cam.data.lens=32/(2*math.tan(math.radians(60)/2))
    # Horizontal view gives a well-defined height fraction / distance equation.
    tilt=math.radians(elevation)
    cam.location=target+Vector((math.sin(theta)*dist*math.cos(tilt),-math.cos(theta)*dist*math.cos(tilt),math.sin(tilt)*dist))
    cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
    cam.data.clip_start=.001;cam.data.clip_end=max(10000,dist*3)
    world=bpy.data.worlds.new('LOD procedural world');world.use_nodes=True;sc.world=world
    world.node_tree.nodes['Background'].inputs[0].default_value=(.35,.40,.48,1)
    world.node_tree.nodes['Background'].inputs[1].default_value=.35
    sun=bpy.data.lights.new('LOD procedural sun','SUN');sun.energy=2.2;sun.angle=.1
    ob=bpy.data.objects.new('LOD procedural sun',sun);sc.collection.objects.link(ob)
    ob.rotation_euler=(math.radians(28),math.radians(-24),math.radians(-30))
    sc.render.resolution_x,sc.render.resolution_y=size;sc.render.resolution_percentage=100
    sc.render.film_transparent=True;sc.render.image_settings.file_format='PNG'
    sc.render.image_settings.color_mode='RGBA';sc.view_settings.view_transform='AgX'
    sc.render.threads_mode='FIXED';sc.render.threads=4
    return sc


def render(path, source, bounds, azimuth, dist, size=(1920,1080), include=None,foliage=False,elevation=0,samples=None,factory_paint=False):
    sc=setup(source,bounds,azimuth,dist,size,include,foliage,elevation,samples,factory_paint)
    sc.render.filepath=str(path);bpy.ops.render.render(write_still=True)
    return np.asarray(Image.open(path).convert('RGBA'),dtype=np.float32)/255


def compare(a,b):
    # Composite over neutral .18 display RGB so cutout coverage is measured too.
    rgb=lambda x:x[:,:,:3]*x[:,:,3:4]+.18*(1-x[:,:,3:4])
    support=np.maximum(a[:,:,3],b[:,:,3])>.02
    delta=np.abs(rgb(a)-rgb(b));d=delta.max(axis=2)
    if not support.any():raise ValueError('Empty render cannot verify LOD')
    y,x=np.where(support)
    scalar=delta.mean(axis=2);integral=np.pad(scalar,((1,0),(1,0))).cumsum(0).cumsum(1)
    patch=integral[8:,8:]-integral[:-8,8:]-integral[8:,:-8]+integral[:-8,:-8]
    return dict(mean=float(delta[support].mean()),p95=float(np.percentile(d[support],95)),
                patch_mean_max=float(patch.max()/64),
                changed_over_8pct=float((d[support]>.08).mean()),
                alpha_mae=float(np.abs(a[:,:,3]-b[:,:,3])[support].mean()),
                silhouette_loss=float(1-np.minimum(a[:,:,3],b[:,:,3]).sum()/np.maximum(a[:,:,3],b[:,:,3]).sum()),
                asset_pixels=int(support.sum()),bbox=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]),delta


def main():
    p=argparse.ArgumentParser();p.add_argument('--config',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg,root,source,out=configuration(a.config)
    m=json.loads((out/'manifest.json').read_text());dest=root/cfg.get('renders','renders/lod')
    foliage=cfg.get('foliage_shader')=='maple'
    dest.mkdir(parents=True,exist_ok=True);bounds=Document(source).bounds(cfg.get('include_nodes'))
    rows=[];strips=[]
    from kit.lod_io import distance
    # Close construction views are independent of switch camera and clearly labeled.
    span=bounds[1]-bounds[0]
    def construction_extent(span):
        angle=math.radians(35);tilt=math.radians(25)
        horizontal=span[0]*math.cos(angle)+span[2]*math.sin(angle)
        depth=span[0]*math.sin(angle)+span[2]*math.cos(angle)
        return float(max(horizontal,span[1]*math.cos(tilt)+depth*math.sin(tilt)))
    close_extent=construction_extent(span)
    from functools import partial
    samples=cfg.get('render_samples',128 if foliage else 24)
    draw=partial(render,samples=samples,factory_paint=bool(cfg.get('factory_paint')))
    items=m['levels']+[a for r in m['levels'] for a in r.get('alternatives',[])]
    for row in items:
        path=out/row['path'];li=row['level']
        label=f'LOD{li}'+('-camera-facing' if row.get('alternative') else '')
        draw(dest/f'close-{label}.png',path,bounds,35,distance(close_extent,.75),
               size=(960,960),include=cfg.get('include_nodes'),foliage=foliage,elevation=25)
        for name in cfg.get('detail_nodes',[]):
            db=Document(source).bounds([name]);ds=db[1]-db[0]
            extent=construction_extent(ds)
            draw(dest/f'close-LOD{li}-{name}.png',path,db,35,distance(extent,.75),
                   size=(960,960),include=[name],foliage=foliage,elevation=25)
    for row in [r for r in items if r['level']]:
        li=row['level']
        label=f'LOD{li}'+('-camera-facing' if row.get('alternative') else '')
        for az in cfg.get('azimuths',[0,55,145]):
            prefix=f'{label}-{az}'
            ref=draw(dest/f'{prefix}-reference.png',source,bounds,az,row['distance_m'],include=cfg.get('include_nodes'),foliage=foliage)
            lod=draw(dest/f'{prefix}-level.png',out/row['path'],bounds,az,row['distance_m'],include=cfg.get('include_nodes'),foliage=foliage)
            previous=m['levels'][li-1]
            if li==1:prev=ref
            else:prev=draw(dest/f'{prefix}-previous.png',out/previous['path'],bounds,az,row['distance_m'],include=cfg.get('include_nodes'),foliage=foliage)
            metric,delta=compare(ref,lod);adjacent,_=compare(prev,lod)
            # Limits are asset-relative: empty background cannot dilute error.
            # 2% mean RGB, 8% p95 and 5% coverage change allow subpixel AA but
            # reject broad color shifts, obvious faceting and lost leaf masses.
            limits=image_limits(cfg,li)
            passed=all(metric[k]<=v and adjacent[k]<=v for k,v in limits.items())
            rows.append(dict(level=li,azimuth=az,distance_m=row['distance_m'],reference=metric,
                             adjacent=adjacent,limits=limits,passed=passed,alternative=row.get('alternative')))
            diff=np.uint8(np.clip(delta*6,0,1)*255)
            Image.fromarray(diff).save(dest/f'{prefix}-difference.png')
            box=metric['bbox'];pad=12;box=[max(0,box[0]-pad),max(0,box[1]-pad),min(1920,box[2]+pad),min(1080,box[3]+pad)]
            w,h=box[2]-box[0],box[3]-box[1]
            strip=Image.new('RGB',(max(700,4*w),h+65),(35,35,35));d=ImageDraw.Draw(strip)
            d.text((8,8),f'{cfg["kind"]} LOD{li} / {row["screen_height"]:.1%} / {row["distance_m"]:.2f}m / azimuth {az}',fill='white')
            d.text((8,25),f'LOD0 | preceding level | LOD{li} | difference x6; native 1080p crop; mean {metric["mean"]:.4f} / p95 {metric["p95"]:.4f}',fill='white')
            for j,arr in enumerate([ref,prev,lod,None]):
                if arr is None:im=Image.fromarray(diff)
                else:
                    rgb=arr[:,:,:3]*arr[:,:,3:4]+.18*(1-arr[:,:,3:4]);im=Image.fromarray(np.uint8(rgb*255))
                strip.paste(im.crop(box),(j*w,60))
            strip.save(dest/f'{prefix}-strip.jpg',quality=92);strips.append(strip)
    # Native strips remain separate; contact sheet is an index, not review proof.
    thumbs=[]
    for s in strips:
        thumb=s.copy();thumb.thumbnail((900,360));thumbs.append(thumb)
    contact=Image.new('RGB',(900,sum(i.height+5 for i in thumbs)),(28,28,28));y=0
    for t in thumbs:contact.paste(t,(0,y));y+=t.height+5
    contact.save(dest/'contact.jpg',quality=90)
    files={p.name:digest(p) for p in dest.iterdir() if p.suffix in ('.png','.jpg')}
    frame='published foliage shader unchanged' if foliage else 'supplied glTF normals/tangents and one-sided visibility'
    report=dict(manifest_sha256=digest(out/'manifest.json'),renderer_sha256=digest(Path(__file__)),
                shading_adapter_sha256=None if foliage else digest(Path(__file__).with_name('lod_shading.py')),
                renderer=f'Cycles GPU, procedural world/sun, {samples} samples, fixed seed, no denoiser, indirect clamp 3; {frame}',
                passed=all(r['passed'] for r in rows),comparisons=rows,files=files)
    (dest/'metrics.json').write_text(json.dumps(report,indent=2)+'\n')
    print('LOD RENDER',report['passed'],[(r['level'],r['azimuth'],r['reference']['mean']) for r in rows])


if __name__=='__main__':main()
