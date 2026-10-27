"""Measured crown envelopes and independently annotated OSU photo profile.

Photo marks are comparison measurements ONLY, never inputs to tree growth.
The source profile clips alpha-support hull edges at actual world Z planes.
"""
import argparse,json,math,sys,io,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from crown_measure import hull
from kit.fonts import find_font

# Looking at the original 584 x 900 summer photo: crown top is partly clipped,
# left lower margins are partly obscured by a neighboring tree. +/-20 px on
# lateral tips and +/-20 px on the base. The widest band is inspected at 30%.
PHOTO_TOP=12
PHOTO_BASE=740
PHOTO_PROFILE=[(0.,164,421),(.1,88,480),(.2,40,528),(.3,24,550),(.4,36,526),
               (.5,63,514),(.6,85,500),(.7,126,468),(.8,158,447),(.9,199,425),(1.,279,327)]

def source_profile(source,out):
    import bpy
    from species import get
    bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));s=get('oak');ob=bpy.data.objects['Summer leaf cards']
    im=bpy.data.images.get('T_PinOak_BaseColor.png')
    alpha=np.asarray(Image.open(io.BytesIO(bytes(im.packed_file.data))).convert('RGBA'))[:,:,3];H,W=alpha.shape;supports=[]
    for u0,v0,u1,v1 in s.LEAF_RECTS:
        xa,xb=math.floor(u0*W),math.ceil(u1*W);ya,yb=math.floor((1-v1)*H),math.ceil((1-v0)*H);points=[]
        for j,row in enumerate(alpha[ya:yb,xa:xb]):
            xs=np.flatnonzero(row>127)
            if len(xs):
                for x in (xs[0],xs[-1]):points.append((((xa+x+.5)/W-u0)/(u1-u0),(1-(ya+j+.5)/H-v0)/(v1-v0)))
        supports.append(np.array(hull(points)))
    edges=[];uv=ob.data.uv_layers.active
    for face in ob.data.polygons:
        pts=np.array([ob.matrix_world@ob.data.vertices[i].co for i in face.vertices]);uv0=np.array(uv.data[face.loop_start].uv)
        k=min(range(len(s.LEAF_RECTS)),key=lambda j:np.linalg.norm(uv0-np.array(s.LEAF_RECTS[j][:2])))
        q=supports[k];poly=pts[0]+q[:,0,None]*(pts[1]-pts[0])+q[:,1,None]*(pts[3]-pts[0]);edges.extend(zip(poly,np.roll(poly,-1,axis=0)))
    edges=np.array(edges);A=edges[:,0];D=edges[:,1]-A;lo=edges[:,:,2].min();hi=edges[:,:,2].max();rows=[]
    for z in np.linspace(lo+.02,hi-.02,141):
        crosses=(edges[:,0,2]-z)*(edges[:,1,2]-z)<=0
        valid=crosses & (np.abs(D[:,2])>1e-10);p=A[valid]+D[valid]*((z-A[valid,2])/D[valid,2])[:,None]
        if len(p):rows.append(dict(z_m=float(z),fraction=float((z-lo)/(hi-lo)),width_x_m=float(np.ptp(p[:,0])),width_y_m=float(np.ptp(p[:,1]))))
    mean=np.array([(r['width_x_m']+r['width_y_m'])/2 for r in rows]);smooth=np.convolve(mean,np.ones(5)/5,mode='same');peak=rows[int(smooth.argmax())]
    report=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),base_m=float(lo),top_m=float(hi),height_m=float(hi-lo),profile=rows,
                max_mean_width_m=float(mean.max()),widest_smoothed_band=peak,width_height_ratio=float(mean.max()/(hi-lo)),
                scope='Actual alpha-pixel-center support hulls on authored cards, clipped by horizontal planes. Convex hulls bound each card; holes inside the alpha are not treated as foliage density. Five-plane (~0.5 m) averaging locates broadest band, not a single projecting leaf.')
    report['passed']=.25<=peak['fraction']<=.35 and .70<=report['width_height_ratio']<=.80
    out.write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='profile'},indent=2))
    if not report['passed']:raise RuntimeError('Measured source crown profile outside round-2 brief')

def review(renders,profile):
    r=json.loads(profile.read_text())
    assert r['source_sha256']==json.loads((renders/'shots.json').read_text())['oak_match_osu']['source_sha256']
    pixels=np.asarray(Image.open(renders/'oak_match_osu.png').convert('RGBA'));rgb=pixels[:,:,:3].astype(float)
    green=(pixels[:,:,3]>127)&(rgb[:,:,1]>rgb[:,:,0]*1.07)&(rgb[:,:,1]>rgb[:,:,2]*1.04)
    rows=np.flatnonzero(green.sum(axis=1)>12);top,base=int(rows.min()),int(rows.max())
    projected=[]
    for f in np.linspace(.025,.975,39):
        y=base-f*(base-top);half=max(2,round((base-top)*.015));band=green[max(0,round(y)-half):min(green.shape[0],round(y)+half+1)]
        xs=np.nonzero(band)[1]
        width=float(np.percentile(xs,99.7)-np.percentile(xs,.3)) if len(xs) else 0
        projected.append(dict(fraction=float(f),width_px=width))
    projected_max=max(x['width_px'] for x in projected)
    projected_peak=max(projected,key=lambda x:x['width_px'])['fraction']
    im=Image.open(ROOT/'trees/refs/oak-osu-summer.jpg').convert('RGB');d=ImageDraw.Draw(im)
    for f,left,right in PHOTO_PROFILE:
        y=PHOTO_BASE-f*(PHOTO_BASE-PHOTO_TOP);d.line((left,y,right,y),fill=(255,90,40),width=2)
        d.text((left+3,y-14),f'{f:.0%}',fill=(255,100,40))
    im.save(renders/'osu-profile-measurements.jpg',quality=94)
    # Compare normalized widths independently of different unknown tree sizes.
    canvas=Image.new('RGB',(1250,900),(238,239,236));d=ImageDraw.Draw(canvas);font=ImageFont.truetype(find_font('Noto Sans','Regular'),20)
    d.text((25,18),'Crown profile / width normalized to each crown maximum',font=font,fill='black')
    def point(width,f):return (120+width*920,780-f*680)
    for f in np.linspace(0,1,11):
        d.line((120,780-f*680,1040,780-f*680),fill=(195,198,190));d.text((30,770-f*680),f'{f:.0%}',font=font,fill='black')
    photo_max=max(b-a for _,a,b in PHOTO_PROFILE);photo=[point((b-a)/photo_max,f) for f,a,b in PHOTO_PROFILE]
    model=[point((row['width_x_m']+row['width_y_m'])/2/r['max_mean_width_m'],row['fraction']) for row in r['profile']]
    d.line(photo,fill=(197,78,34),width=4);d.line(model,fill=(20,102,70),width=4)
    d.line([point(x['width_px']/projected_max,x['fraction']) for x in projected],fill=(45,90,190),width=3)
    d.text((120,815),'Green: physical X/Y mean; blue: matched render; orange: OSU photo (+/-20 px)',font=font,fill='black')
    d.text((120,848),'Different specimens/projections. OSU apex clipped, lower left partly occluded.',font=font,fill='black')
    canvas.save(renders/'crown-profile.jpg',quality=94)
    rows=[]
    for f,a,b in PHOTO_PROFILE:
        if 0<f<1:
            sample=min(r['profile'],key=lambda x:abs(x['fraction']-f));rows.append(dict(fraction=f,source_x_m=sample['width_x_m'],source_y_m=sample['width_y_m'],source_mean_normalized=((sample['width_x_m']+sample['width_y_m'])/2/r['max_mean_width_m']),photo_width_px=b-a,photo_normalized=(b-a)/photo_max))
    (renders/'crown-profile-comparison.json').write_text(json.dumps(dict(source=r,projected_render=dict(profile=projected,widest_band_fraction=projected_peak,top_px=top,base_px=base,scope='Selected green alpha-supported rendered foliage; 3% height bands and 0.3/99.7 percentiles suppress single leaf outliers.'),photo=dict(top_px=PHOTO_TOP,base_px=PHOTO_BASE,profile=PHOTO_PROFILE,uncertainty_px=20,widest_band_fraction=.3,width_height_ratio=photo_max/(PHOTO_BASE-PHOTO_TOP)),comparison=rows),indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path);p.add_argument('--out',type=Path);p.add_argument('--renders',type=Path);p.add_argument('--profile',type=Path)
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:];a=p.parse_args(argv)
    if a.source:source_profile(a.source,a.out)
    else:review(a.renders,a.profile)
