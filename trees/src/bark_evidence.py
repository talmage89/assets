"""Measure shipped bole density/texture relief and inspected photo display patches.

This is an appearance diagnostic, not an equal-illumination or albedo calibration.
Photo pixels are read only here, never by a geometry or texture generator.
"""
import argparse,json,sys,io,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.gltf import GLB


def density(glb):
    raw=GLB(glb);rows=[];samples=[];texture_uv=[];areas=[]
    for mesh in raw.json['meshes']:
        if mesh['name']!='Trunk and branches':continue
        for prim in mesh['primitives']:
            attr=prim['attributes'];p=raw.accessor(attr['POSITION']);u=raw.accessor(attr['TEXCOORD_0'])
            indices=raw.accessor(prim['indices']).reshape(-1,3)
            for tri in indices:
                v=p[tri];q=u[tri];center=v.mean(axis=0)
                if not 1.0<center[1]<1.8 or np.linalg.norm(center[[0,2]])>.3:continue
                a=np.linalg.norm(np.cross(v[1]-v[0],v[2]-v[0]))*.5
                ua=abs(np.linalg.det(np.stack([q[1]-q[0],q[2]-q[0]])))*.5
                if a<1e-10:continue
                rows.append((2048*np.sqrt(ua/a),a))
                texture_uv.append(q);areas.append(a)
                # 2D UV Jacobian in an orthonormal tangent frame, reporting
                # directional density too; area density alone hides stretching.
                e=v[1]-v[0];f=v[2]-v[0];ex=e/np.linalg.norm(e);ey=f-ex*np.dot(f,ex);ey/=np.linalg.norm(ey)
                j=(q[1:]-q[0]).T@np.linalg.inv(np.array([[e@ex,f@ex],[e@ey,f@ey]]))
                samples.append(np.linalg.svd(j*2048,compute_uv=False))
    values=np.array(rows);s=np.array(samples)
    if len(values)==0:raise RuntimeError('No eye-height bole surface')
    # Uniform area samples read the actual embedded 2048 maps, after filtering.
    rng=np.random.default_rng(2718);chosen=rng.choice(len(areas),24000,p=np.array(areas)/sum(areas))
    bary=rng.random((24000,2));flip=bary.sum(axis=1)>1;bary[flip]=1-bary[flip]
    q=np.array(texture_uv)[chosen];coords=q[:,0]+bary[:,:1]*(q[:,1]-q[:,0])+bary[:,1:]*(q[:,2]-q[:,0])
    textures={r['name']:np.asarray(Image.open(io.BytesIO(raw.image(i))))/255 for i,r in enumerate(raw.json['images'])}
    normal=next(v for k,v in textures.items() if 'Normal' in k);orm=next(v for k,v in textures.items() if 'ORM' in k)
    ix=np.clip((coords[:,0]*2048).astype(int),0,2047);iy=np.clip((coords[:,1]*2048).astype(int),0,2047)
    ns=normal[iy,ix,:3]*2-1;ns/=np.linalg.norm(ns,axis=1)[:,None]
    relief=dict(tangent_normal_angle_degrees_p10_p50_p90=np.percentile(np.degrees(np.arccos(np.clip(ns[:,2],-1,1))),[10,50,90]).tolist(),
                orm_occlusion_p10_p50_p90=np.percentile(orm[iy,ix,0],[10,50,90]).tolist(),sample_count=24000)
    return dict(eye_height_m=[1.,1.8],triangles=len(rows),surface_m2=float(values[:,1].sum()),embedded_texture_relief=relief,
                area_density_px_m_p0_p5_p50_p95_p100=np.percentile(values[:,0],[0,5,50,95,100]).tolist(),
                directional_density_px_m_min_median_max=[float(s.min()),float(np.median(s)),float(s.max())])


def patch(path,box):
    im=Image.open(path).convert('RGB');a=np.asarray(im.crop(box))/255
    return dict(rectangle_px=list(box),pixels=a.shape[0]*a.shape[1],
                median_display_rgb=np.median(a.reshape(-1,3),axis=0).tolist(),
                display_luminance_p10_p50_p90=np.percentile(a@np.array([.2126,.7152,.0722]),[10,50,90]).tolist())


def evidence(renders,glb):
    renders=Path(renders);sha=hashlib.sha256(Path(glb).read_bytes()).hexdigest()
    metadata=json.loads((renders/'shots.json').read_text())
    for name in ('match_psu','match_osu'):
        if metadata[name]['source_sha256']!=sha:raise RuntimeError('Stale bark comparison: '+name)
    result=dict(glb_sha256=sha,density=density(glb),comparisons={},scope='Display pixels across different illumination and specimens, not calibrated reflectance. OSU scanned slide is form-only.')
    for name,x,ys,boxes in [('psu',.505,[(.82,.855),(.91,.95)],[(464,585,473,608),(464,622,473,648)]),
                          ('osu',.525,[(.83,.86),(.91,.95)],[(1074,737,1084,770),(1078,797,1090,825)])]:
        model=renders/('match_'+name+'.png');im=Image.open(model);w,h=im.size
        pairs={}
        for label,(lo,hi),box in zip(['upper_shade','lower_bole'],ys,boxes):
            mb=(round((x-.004)*w),round(lo*h),round((x+.004)*w),round(hi*h))
            pairs[label]=dict(model=patch(model,mb),photo=patch(ROOT/'trees/refs'/f'{name}-form.jpg',box))
        result['comparisons'][name]=pairs
    return result


def pair(renders,row):
    """Context crops make the measured display rectangles reviewable."""
    from PIL import ImageOps,ImageFont
    from kit.fonts import find_font
    font=ImageFont.truetype(find_font('Noto Sans','Regular'),20)
    canvas=Image.new('RGB',(1000,740),(238,239,236));draw=ImageDraw.Draw(canvas)
    for i,(label,path,box,kind) in enumerate([
        ('EXPORTED GLB',Path(renders)/'match_psu.png',None,'model'),
        ('PENN STATE photograph',ROOT/'trees/refs/psu-form.jpg',(445,550,491,661),'photo')]):
        im=Image.open(path).convert('RGB');w,h=im.size
        if box is None:box=(round(.480*w),round(.78*h),round(.535*w),round(.982*h))
        d=ImageDraw.Draw(im)
        for color,key in [((210,90,30),'upper_shade'),((30,130,190),'lower_bole')]:
            d.rectangle(row['comparisons']['psu'][key][kind]['rectangle_px'],outline=color,width=1)
        crop=ImageOps.contain(im.crop(box),(420,520));canvas.paste(crop,(i*500+250-crop.width//2,70))
        draw.text((i*500+28,22),label,font=font,fill=(20,35,25))
        for j,key in enumerate(('upper_shade','lower_bole')):
            value=row['comparisons']['psu'][key][kind]['display_luminance_p10_p50_p90'][1]
            draw.text((i*500+28,610+j*30),f'{key}: median display Y {value:.3f}',font=font,fill=(20,35,25))
    draw.text((28,691),'Different specimens and illumination; PSU lower bole is also beneath the crown.',font=font,fill=(20,35,25))
    canvas.save(Path(renders)/'bark-value-pair.jpg',quality=94,optimize=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--renders',type=Path,required=True);p.add_argument('--glb',type=Path,default=ROOT/'trees/export/RedMaple.glb');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    row=evidence(a.renders,a.glb)
    (a.renders/'bark-evidence.json').write_text(json.dumps(row,indent=2));print(json.dumps(row,indent=2))
    pair(a.renders,row)
    assert row['density']['area_density_px_m_p0_p5_p50_p95_p100'][0]>=400
    assert row['density']['directional_density_px_m_min_median_max'][0]>=400
    assert row['density']['embedded_texture_relief']['tangent_normal_angle_degrees_p10_p50_p90'][2]>5
    assert row['density']['embedded_texture_relief']['orm_occlusion_p10_p50_p90'][0]<.9
