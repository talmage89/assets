"""Whole-mesh curvature/stripe comparisons and measured round-three sections."""
from pathlib import Path
import math
import numpy as np
from PIL import Image,ImageDraw
from suv_review import font,rgb,save,ASSET
SHOTS={'side_raking':dict(location=(10,-.25,1.20),target=(0,0,.85),ortho=5.4)}


def tile(page,source,box,label):
    x,y,w,h=box;im=rgb(source);im.thumbnail((w-30,h-65),Image.Resampling.LANCZOS)
    page.paste(im,(x+(w-im.width)//2,y+55+(h-65-im.height)//2))
    ImageDraw.Draw(page).text((x+20,y+10),label,font=font(25),fill=(25,50,65))


def legend(page,y):
    d=ImageDraw.Draw(page);stops=[(-20,(.10,.05,.45)),(-5,(.05,.28,.9)),(-1,(.12,.75,.85)),(0,(.48,.72,.45)),(1,(.90,.82,.16)),(5,(.98,.25,.035)),(20,(.5,.025,.02))]
    for i,(value,col) in enumerate(stops):
        srgb=tuple(round(255*(12.92*c if c<=.0031308 else 1.055*c**(1/2.4)-.055)) for c in col)
        x=50+i*220;d.rectangle((x,y,x+180,y+24),fill=srgb);d.text((x,y+30),f'{value:+g} /m',font=font(24),fill=(25,50,65))
    d.text((50,y+76),'Signed mean H=(k1+k2)/2. Convex positive; fixed nonlinear color scale. Gray: open boundaries; dark: unmeasured parts.',font=font(24),fill=(25,50,65))
    d.text((50,y+116),'Cotangent weights / mixed Voronoi area on actual game triangles. No smoothing, normal-map data or parent substitution.',font=font(24),fill=(25,50,65))


def project(p,shot,w,h):
    eye=np.asarray(shot['location']);target=np.asarray(shot['target']);forward=target-eye;forward/=np.linalg.norm(forward)
    right=np.cross(forward,[0.,0.,1.]);right/=np.linalg.norm(right);up=np.cross(right,forward);q=np.asarray(p)-target
    return w/2+np.dot(q,right)*w/shot['ortho'],h/2-np.dot(q,up)*w/shot['ortho']


def make(out,report):
    names=[];old=ASSET/'renders/suv-round2';r=report['round3']
    for view in ['front_three_quarter','rear_three_quarter','side','front','rear']:
        page=Image.new('RGB',(2400,1300),(228,231,232))
        tile(page,out/('curvature_stripes_'+view+'.png'),(0,0,1200,1050),'ROUND 3 / SAME CAMERA / REFLECTION STRIPES')
        tile(page,out/('mean_curvature_'+view+'.png'),(1200,0,1200,1050),'ROUND 3 / ACTUAL GAME MESH CURVATURE')
        legend(page,1080);name='round3-curvature-'+view+'.jpg';save(page,out/name);names.append(name)
    page=Image.new('RGB',(2400,2300),(228,231,232))
    for j,view in enumerate(['front','rear','side_raking']):
        for i,folder in enumerate([old,out]):tile(page,folder/(view+'.png'),(i*1200,j*760,1200,760),f'ROUND {2+i} / '+view.replace('_',' ').upper())
    name='round2-round3-ends-raking.jpg';save(page,out/name);names.append(name)
    for make in ['crv','rav4']:
        page=Image.new('RGB',(2400,900),(228,231,232))
        tile(page,ASSET/('refs/suv-'+make+'-rear.jpg'),(0,0,800,850),make.upper()+' / REFERENCE')
        tile(page,old/(make+'_rear_clay.png'),(800,0,800,850),'ROUND 2 / CALIBRATED CAMERA')
        tile(page,out/(make+'_rear_clay.png'),(1600,0,800,850),'ROUND 3 / SAME CAMERA')
        name='round2-round3-'+make+'-rear.jpg';save(page,out/name);names.append(name)
    page=rgb(out/'side_raking.png');d=ImageDraw.Draw(page);w,h=page.size
    d.text((25,20),'ACTUAL RAY-HIT SECTIONS / shoulder cyan / lower crease orange',font=font(25),fill=(25,50,65))
    for i,rec in enumerate(r['lines']):
        for name,col in [('shoulder',(10,145,190)),('lower',(210,85,20))]:
            line=rec[name];p=np.asarray(line['endpoints_m']).mean(axis=0);x,y=project(p,SHOTS['side_raking'],w,h)
            d.line((x,y-23,x,y+23),fill=col,width=3);d.line((x-8,y,x+8,y),fill=col,width=3)
        line=rec['shoulder'];low=rec['lower']
        d.text((30+i*w//3,h-72),f"y={rec['station_y_m']:+.3f}: shoulder {line['normal_turn_degrees']:.1f} deg / {line['width_z_m']*1000:.0f} mm",font=font(18),fill=(25,65,85))
        d.text((30+i*w//3,h-44),f"lower {low['normal_turn_degrees']:.1f} deg / {low['width_z_m']*1000:.0f} mm",font=font(18),fill=(125,65,30))
    name='round3-raking-measured.jpg';save(page,out/name);names.append(name)
    return names
