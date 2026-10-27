"""Photo display populations and bark crops; never inputs to asset generation."""
import argparse,json,sys,hashlib,colorsys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from color_values import measure as fifths

def measure(path,crop=None):
    row=fifths(path,crop)
    im=Image.open(path).convert('RGBA')
    if crop:im=im.crop(crop)
    a=np.asarray(im)/255
    # Include near-neutral green highlights, rather than dropping them as the
    # original strict green fifths selector did. Identical rule for photos.
    mask=(a[:,:,1]>a[:,:,0]*1.015)&(a[:,:,1]>a[:,:,2]*1.03)&(a[:,:,3]>.5)
    rgb=a[:,:,:3][mask];v=rgb@np.array([.2126,.7152,.0722])
    row['including_neutral_highlights']=dict(selected_pixels=len(rgb),median_display_luminance=float(np.median(v)),fraction_above_05=float((v>.5).mean()),mean_display_rgb=rgb.mean(0).tolist(),mean_hsv=list(colorsys.rgb_to_hsv(*rgb.mean(0))),mask='G > 1.015 R; G > 1.03 B; alpha > .5',scope='Loose-mask diagnostic includes neutral highlights but can also include tinted sky or grade; not a segmented foliage population')
    mask=(a[:,:,1]>a[:,:,0]*1.10)&(a[:,:,1]>a[:,:,2]*1.08)&(a[:,:,3]>.5)
    rgb=a[:,:,:3][mask];v=rgb@np.array([.2126,.7152,.0722])
    row['whole_foliage']=dict(selected_pixels=len(rgb),median_display_luminance=float(np.median(v)),fraction_above_05=float((v>.5).mean()),mean_display_rgb=rgb.mean(0).tolist(),mean_hsv=list(colorsys.rgb_to_hsv(*rgb.mean(0))),mask='G > 1.10 R; G > 1.08 B; alpha > .5; same selector as fifths')
    yy=np.nonzero(mask)[0];split=round(yy.min()+(yy.max()-yy.min())*.5)
    upper=mask.copy();upper[split:]=False
    values=a[:,:,:3][upper]@np.array([.2126,.7152,.0722])
    row['upper_projected_crown']=dict(split_row_px=split,median_display_luminance=float(np.median(values)),fraction_above_05=float((values>.5).mean()),scope='Top half of the strict green pixel image span; approximate projected upper crown, not a surveyed height section')
    return row
def patch(path,box):
    im=Image.open(path).convert('RGB');v=np.asarray(im.crop(box))/255
    return dict(rectangle_px=list(box),median_display_rgb=np.median(v.reshape(-1,3),axis=0).tolist(),display_luminance_p10_p50_p90=np.percentile(v@np.array([.2126,.7152,.0722]),[10,50,90]).tolist())
from kit.fonts import find_font

def evidence(renders,source):
    renders=Path(renders);source=Path(source);sha=hashlib.sha256(source.read_bytes()).hexdigest()
    meta=json.loads((renders/'shots.json').read_text());rows={}
    for name,file,crop in [('osu','oak-osu-summer.jpg',(15,10,575,730)),('stony','oak-stony-summer.png',(300,160,2115,2290))]:
        key='oak_match_'+name;assert meta[key]['source_sha256']==sha,'Stale photo evidence'
        model=measure(renders/(key+'.png'));photo=measure(ROOT/'trees/refs'/file,crop)
        delta={kind:model[kind]['median_display_luminance']-photo[kind]['median_display_luminance'] for kind in ['brightest_20_percent','darkest_20_percent']}
        delta['whole_foliage_median']=model['whole_foliage']['median_display_luminance']-photo['whole_foliage']['median_display_luminance']
        rows[name]=dict(model=model,photo=photo,photo_crop_px=crop,display_luminance_delta=delta,within_03=all(abs(d)<=.03 for d in delta.values()),lighting=meta[key]['lighting'])
    result=dict(source_sha256=sha,stage='exported GLB' if source.suffix=='.glb' else 'source',foliage=rows,
                scope='Green display-image populations across different specimens, photographic processing and illumination. Bright/dark fifths are proxies for sun/shade, not segmented equal-light surfaces or calibrated reflectance. Per-view daylight is explicit; authored albedo is shared.')
    if (renders/'hero.png').exists():
        cycles=measure(renders/'hero.png')['whole_foliage']
        ep=renders.parent/('oak-final-eevee' if renders.name=='oak-final' else renders.name+'-eevee')/'hero.png'
        if ep.exists():
            eevee=measure(ep)['whole_foliage'];h=abs(eevee['mean_hsv'][0]-cycles['mean_hsv'][0]);h=min(h,1-h)
            result['engine_comparison']=dict(cycles=cycles,eevee=eevee,hue_delta_turns=float(h),median_luminance_delta=eevee['median_display_luminance']-cycles['median_display_luminance'],hsv_value_delta=eevee['mean_hsv'][2]-cycles['mean_hsv'][2],within_05=bool(h<=.05 and abs(eevee['median_display_luminance']-cycles['median_display_luminance'])<=.05 and abs(eevee['mean_hsv'][2]-cycles['mean_hsv'][2])<=.05))

        hero=np.asarray(Image.open(renders/'hero.png').convert('RGBA'))/255
        mask=(hero[:,:,1]>hero[:,:,0]*1.10)&(hero[:,:,1]>hero[:,:,2]*1.08)&(hero[:,:,3]>.5)
        rgb=hero[:,:,:3][mask];values=rgb@np.array([.2126,.7152,.0722])
        result['hero_tonal_check']=dict(display_luminance_p5_p50_p95_p99=np.percentile(values,[5,50,95,99]).tolist(),fraction_below_02=float((values<.02).mean()),fraction_channel_clipped=float((rgb>=1).any(axis=1).mean()),scope='Selected green hero display pixels only; excludes sky, grade, wood and neutral highlights')
    if source.suffix=='.glb':
        from bark_evidence import density
        result['bark_delivery']=density(source)
        # Read albedo independently of the blue procedural skylight. Uniform
        # area samples on actual delivered chest-height triangles, embedded PNG.
        from kit.gltf import GLB
        import io
        raw=GLB(source);tri_uv=[];areas=[]
        if 'bark_raking' in meta:
            from mathutils import Vector
            from mathutils.bvhtree import BVHTree
            prim=next(m for m in raw.json['meshes'] if m['name']=='Trunk and branches')['primitives'][0]
            pos=raw.accessor(prim['attributes']['POSITION']);tri=raw.accessor(prim['indices']).reshape(-1,3)
            tree=BVHTree.FromPolygons([Vector(p) for p in pos],tri.tolist(),all_triangles=True)
            row=meta['bark_raking'];a=row['camera']['location'];b=row['shot']['target']
            camera=Vector((a[0],a[2],-a[1]));target=Vector((b[0],b[2],-b[1]))
            hit=tree.ray_cast(camera,(target-camera).normalized())
            assert hit[0] is not None,'Raking camera misses delivered wood'
            result['raking_camera_surface_distance_m']=float(hit[3])
        for mesh in raw.json['meshes']:
            if mesh['name']!='Trunk and branches':continue
            for prim in mesh['primitives']:
                pos=raw.accessor(prim['attributes']['POSITION']);uvs=raw.accessor(prim['attributes']['TEXCOORD_0'])
                for tri in raw.accessor(prim['indices']).reshape(-1,3):
                    points=pos[tri];center=points.mean(axis=0)
                    if 1.<center[1]<1.8 and np.linalg.norm(center[[0,2]])<.3:
                        tri_uv.append(uvs[tri]);areas.append(np.linalg.norm(np.cross(points[1]-points[0],points[2]-points[0]))/2)
        rng=np.random.default_rng(614);ids=rng.choice(len(areas),4000,p=np.array(areas)/sum(areas));b=rng.random((4000,2));flip=b.sum(axis=1)>1;b[flip]=1-b[flip]
        q=np.array(tri_uv)[ids];coords=q[:,0]+b[:,:1]*(q[:,1]-q[:,0])+b[:,1:]*(q[:,2]-q[:,0])
        index=next(i for i,row in enumerate(raw.json['images']) if 'BaseColor' in row['name']);tex=np.asarray(Image.open(io.BytesIO(raw.image(index))))/255
        H,W=tex.shape[:2];rgb=tex[np.clip((coords[:,1]*H).astype(int),0,H-1),np.clip((coords[:,0]*W).astype(int),0,W-1),:3]
        linear=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
        result['bark_albedo']=dict(median_srgb_rgb=np.median(rgb,axis=0).tolist(),median_linear_rgb=np.median(linear,axis=0).tolist(),samples=4000,scope='Embedded albedo on delivered chest-height wood, without illumination; not inferred from a photograph')
    if (renders/'bark.png').exists():
        im=Image.open(renders/'bark.png');w,h=im.size
        # Avoid sky and silhouette boundaries, include the chest-height surface.
        mb=(round(.43*w),round(.34*h),round(.57*w),round(.78*h));pb=(25,40,220,370)
        result['bark_display']=dict(model=patch(renders/'bark.png',mb),photo=patch(ROOT/'trees/refs/oak-osu-bark.jpg',pb),scope='OSU left bole panel vs rendered chest-height bole. Different illumination, not albedo calibration.')
        bd=result['bark_display'];bd['median_luminance_delta']=bd['model']['display_luminance_p10_p50_p90'][1]-bd['photo']['display_luminance_p10_p50_p90'][1]
        bd['red_minus_blue']={k:bd[k]['median_display_rgb'][0]-bd[k]['median_display_rgb'][2] for k in ('model','photo')}
        bd['within_03_warm']=abs(bd['median_luminance_delta'])<=.03 and bd['red_minus_blue']['model']>=0
        font=ImageFont.truetype(find_font('Noto Sans','Regular'),18)
        canvas=Image.new('RGB',(1000,780),(238,239,236));draw=ImageDraw.Draw(canvas)
        for i,(path,box,title) in enumerate([(renders/'bark.png',(round(.37*w),round(.13*h),round(.63*w),round(.94*h)),'Original tree / '+result['stage']),(ROOT/'trees/refs/oak-osu-bark.jpg',(5,0,250,400),'Pin oak photograph / OSU')]):
            image=Image.open(path).convert('RGB');d=ImageDraw.Draw(image);d.rectangle(mb if i==0 else pb,outline=(220,110,40),width=2)
            image=ImageOps.contain(image.crop(box),(450,620));canvas.paste(image,(i*500+250-image.width//2,55))
            row=result['bark_display']['model' if i==0 else 'photo'];v=row['display_luminance_p10_p50_p90'][1]
            draw.text((i*500+20,15),title,font=font,fill=(22,38,29));draw.text((i*500+20,695),f'Marked patch median display Y {v:.3f}',font=font,fill=(22,38,29))
            rgb=row['median_display_rgb']
            draw.text((i*500+20,720),f'Median channels R {rgb[0]:.3f} / B {rgb[2]:.3f}',font=font,fill=(22,38,29))
        draw.text((20,740),'Different lighting and specimens; photograph stays local. No reference pixels in the asset.',font=font,fill=(22,38,29))
        canvas.save(renders/'bark-pair.jpg',quality=93,optimize=True)
    (renders/'color-value-evidence.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--source',default=ROOT/'trees/export/PinOak.glb');a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None);evidence(a.renders,a.source)
