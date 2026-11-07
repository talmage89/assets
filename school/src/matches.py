"""Neutral-balanced, measured-feature camera fits through the kit solver.

Original school designs are type comparisons, not photographic replicas.
All reference processing stays in build/; no photo becomes a material input.
"""
import json,math,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(HERE),str(ROOT)]
from plans import school,world
from kit.photo_match import calibrate


def linear(a):return np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
def srgb(a):return np.where(a<=.0031308,a*12.92,1.055*np.maximum(a,0)**(1/2.4)-.055)


def neutral(source,name,roi,description):
    im=ImageOps.exif_transpose(Image.open(source)).convert('RGB');arr=np.array(im)/255.;patch=linear(np.array(im.crop(roi))/255.);rgb=np.median(patch.reshape(-1,3),axis=0);gain=rgb.mean()/np.maximum(rgb,.001)
    dest=Path('build/references')/(name+'-balanced.png');dest.parent.mkdir(parents=True,exist_ok=True)
    Image.fromarray(np.uint8(np.clip(srgb(linear(arr)*gain),0,1)*255+.5)).save(dest)
    return dest.as_posix(),dict(source=str(source),neutral_roi_pixels=roi,neutral_assumption=description,median_linear_rgb=rgb.tolist(),linear_gains=gain.tolist(),exposure_preserved='Equal-channel neutral mean; no global exposure raise or albedo inference')


def main():
    # Render the printed archival photograph at a reproducible native size;
    # this extracts a reference photograph, never model geometry or textures.
    dest=Path('build/references');dest.mkdir(parents=True,exist_ok=True)
    subprocess.run(['pdftoppm','-f','77','-l','77','-scale-to','3200','-png','refs/colorado-schools.pdf',str(dest/'emerald')],check=True)
    Image.open(dest/'emerald-077.png').crop((217,640,2256,2660)).save(dest/'emerald-photo.png')
    balances={};photos={}
    f=2255/1200
    photos['gym'],balances['gym']=neutral('refs/walls.jpg','gym',tuple(round(v*f) for v in (400,605,455,615)),'Sunlit concrete curb, assumed neutral gray; not the brick or foliage')
    f=2.5
    photos['ribbon'],balances['ribbon']=neutral('refs/mcdowell.jpg','ribbon',tuple(round(v*f) for v in (700,565,760,580)),'Pale white-painted spandrel panel; aged transparency, approximate neutral assumption')
    f=2039/1200
    photos['walk'],balances['walk']=neutral(dest/'emerald-photo.png','walk',tuple(round(v*f) for v in (110,650,160,660)),'Pale painted fascia in an archival monochrome scan; gain removes scan color cast only')
    Path('build/reference-balance.json').write_text(json.dumps(balances,indent=2))
    specs={}
    # Tall gym / lower office and a visible right-side depth baseline.
    p=school(103);b=next(b for b in p['blocks'] if b['kind']=='gym');l,r,ff,k=b['rect'];z=b['roof']+.19;base=p['floor'];factor=2255/1200
    points=[((l,ff,z),(577,403)),((r,ff,z),(1138,386)),((l,ff,base),(579,598)),((r,ff,base),(1138,606)),((r,k,z),(1185,439)),((r,k,base),(1185,603))]
    specs['gym']=dict(seed=103,photo=photos['gym'],title='1970s gym / lower office massing',crop=(400,650,2255,1450),location=(40,-85,1.68),target=((l+r)/2,ff,3.2),lens=40,lens_bounds_mm=(25,65),camera_height_m=(1.68,.45),landmarks=[dict(world=w,pixel=(px[0]*factor,px[1]*factor),weight=.3 if i==2 else 1) for i,(w,px) in enumerate(points)],light=dict(sky=.16,energy=3.0,direction=(-.3,.8,-.85),exposure=-.45))
    # One full classroom ribbon, not the entire two-room pod facade.
    p=school(102);b=next(b for b in p['blocks'] if b['id']=='Cluster_B');o=next(o for o in b['openings'] if o['face']=='north' and o['type']=='window');u,w,z,h=o['u'],o['w'],o['z']+.1524,o['h']
    points=[((u-w/2,0,z+h),(350,408)),((u+w/2,0,z+h),(984,396)),((u-w/2,0,z),(350,586)),((u+w/2,0,z),(984,589)),((u,0,z+.39),(669,560))]
    target=world((u,0,z+h/2),o['origin'],o['yaw']);location=world((u,-24,1.68),o['origin'],o['yaw'])
    specs['ribbon']=dict(seed=102,photo=photos['ribbon'],title='1960s classroom ribbon / spandrel / eave',crop=(700,750,2650,1700),location=location,target=target,lens=45,lens_bounds_mm=(25,65),camera_height_m=(1.68,.6),landmarks=[dict(world=world(w,o['origin'],o['yaw']),pixel=(px[0]*2.5,px[1]*2.5),weight=.4 if i==4 else 1) for i,(w,px) in enumerate(points)],light=dict(sky=.22,energy=.85,direction=(.3,-.8,-.8),softness=6,exposure=-.45))
    # Three actual canopy-column top/bottom pairs provide a perspective-depth
    # baseline rather than fitting an unrelated telephoto view of a whole site.
    p=school(101);c=p['covered'][0];l,r,ff,k=c['rect'];steps=math.ceil((r-l)/4.5);factor=2039/1200;anchors=[]
    for j,px,top,bottom in ((0,181,675,865),(2,531,700,840),(4,784,710,829)):
        x=l+j*(r-l)/steps
        for z,py in ((.1524,bottom),(c['height'],top)):anchors.append(dict(world=(x,ff+.18,z),pixel=(px*factor,py*factor)))
    specs['walk']=dict(seed=101,photo=photos['walk'],title='1958 covered walk / columns / fascia',crop=(0,945,1850,1630),location=(l-18,ff-15,1.68),target=((l+r)/2,ff,1.65),lens=40,lens_bounds_mm=(25,65),camera_height_m=(1.68,.5),landmarks=anchors,light=dict(sky=.22,energy=1.8,direction=(.8,.3,-.9),softness=4,exposure=-.45))
    result={}
    for name,s in specs.items():
        row=calibrate(s);row.update(seed=s['seed'],light=s['light']);row['lens_status']='Estimated feature/type fit on an original design; not EXIF camera recovery or a building survey.';result[name]=row
        print(name,'estimated lens',round(row['shot']['lens'],2),'RMS native pixels',round(row['residual_rms_pixels'],2))
    Path('build/matched-cameras.json').write_text(json.dumps(result,indent=2))
    Path('build/photo-definitions.json').write_text(json.dumps(specs,indent=2))

if __name__=='__main__':main()
