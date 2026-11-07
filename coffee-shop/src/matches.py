"""Photo-framing evidence using kit/photo_match.py; photos never enter Blender.

Anchors are named construction features measured by eye on a 1000px study.
These are different original shops, not surveyed reconstructions. Residuals
and assumed-neutral white balance remain explicit beside the pairs.
"""
import argparse
import json
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from kit.photo_match import calibrate
from kit.fonts import find_font


def balance(name,rect):
    im=Image.open(Path('build/photo-study')/(name+'.jpg')).convert('RGB');a=np.asarray(im)/255
    linear=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4);x,y,xx,yy=rect;neutral=np.median(linear[y:yy,x:xx],axis=(0,1));g=np.mean(neutral)/neutral
    lin=np.clip(linear*g,0,1);s=np.where(lin<=.0031308,lin*12.92,1.055*lin**(1/2.4)-.055);out=Path('build/photo-balanced');out.mkdir(exist_ok=True);p=out/(name+'.jpg');Image.fromarray(np.uint8(np.clip(s*255+.5,0,255))).save(p,quality=96)
    return str(p),dict(neutral_rectangle_1000px=rect,linear_channel_gains=g.tolist(),assumption='neutral painted trim or unpainted pavement, not a gray card; unknown photographic processing')


def prepare():
    study=Path('build/photo-study');study.mkdir(parents=True,exist_ok=True)
    for name in ('downtown-2008','coffea-2008','brew-2008','counter-2008','fair-2008'):
        im=Image.open(Path('refs')/(name+'.jpg'));im.resize((1000,round(im.height*1000/im.width)),Image.Resampling.LANCZOS).save(study/(name+'.jpg'),quality=98)
    p=json.loads(Path('build/shops/117.json').read_text());w=p['width'];left=-w/2+1.65;right=w/2-.4
    configs={
      'downtown':dict(seed=117,title='2008 independent sidewalk cafe / awning and storefront',photo='downtown-2008',neutral=[143,433,159,465],location=[-9,-7,1.65],target=[0,0,1.8],lens=35,
        landmarks=[('left window head', [left,0,3.15],[432,211]),('right window head',[right,0,3.15],[782,340]),('left window sill',[left,0,.51],[432,582]),('right window sill',[right,0,.51],[782,500])],sun_elevation=45,sun_azimuth=-112),
      'umbrella':dict(seed=117,title='Coffea, 2008 / umbrella span and furniture scale',photo='coffea-2008',neutral=[265,1124,326,1140],location=[2.8,-8.5,1.7],target=[0,-3.66,1.6],lens=42,
        landmarks=[('canopy left',[-1.3822,-3.66,1.94],[150,704]),('canopy right',[1.3822,-3.66,1.94],[900,748]),('canopy crown',[0,-3.66,2.565],[544,584]),('front rim',[0,-5.0422,1.94],[539,721]),('pole at ground',[0,-3.66,0],[505,1210])],sun_elevation=46,sun_azimuth=-135),
      'pad':dict(seed=339,title='Lakeview Brew, 2008 / converted pad and patio',photo='brew-2008',neutral=[373,551,400,562],location=[-18,-24,1.65],target=[0,1,1.7],lens=40,
        landmarks=[('front glazing left head',[-4.93,0,2.75],[427,468]),('front glazing right head',[4.93,0,2.75],[624,494]),('front glazing left sill',[-4.93,0,.27],[426,577]),('front glazing right sill',[4.93,0,.27],[629,587]),('left roof front',[-5.4864,0,3.66],[411,434]),('right roof front',[5.4864,0,3.66],[675,465])],sun_elevation=54,sun_azimuth=-126),
      'daily-use':dict(seed=117,title='Fair Grinds, June 2008 / occupied sidewalk and canopy shade',photo='fair-2008',neutral=[274,1030,298,1050],location=[-7,-5,1.65],target=[1,-.5,2],lens=35,
        landmarks=[('near canopy rib at wall',[left,0,3.52],[341,480]),('near canopy rib at eave',[left,-1.42,3.14],[764,480]),('middle canopy rib at wall',[(left+right)/2,0,3.52],[455,647]),('middle canopy rib at eave',[(left+right)/2,-1.42,3.14],[704,648])],sun_elevation=52,sun_azimuth=-125),
    }
    results={}
    for name,c in configs.items():
        photo,wb=balance(c['photo'],c['neutral']);im=Image.open(photo)
        crop=[300,125,930,675] if name=='downtown' else [95,505,965,1333] if name=='umbrella' else [280,460,840,1180] if name=='daily-use' else [115,345,855,650]
        m=dict(title=c['title'],photo=photo,crop=crop,location=c['location'],target=c['target'],lens=c['lens'],exposure=-1,
            lens_bounds_mm=[22,70],camera_height_m=[1.65,.75],landmarks=[dict(name=n,world=xyz,pixel=uv) for n,xyz,uv in c['landmarks']])
        result=calibrate(m);result.update(seed=c['seed'],white_balance=wb,sun_elevation=c['sun_elevation'],sun_azimuth=c['sun_azimuth'],feature_names=[r[0] for r in c['landmarks']],limits='Authored original design differs from photograph; positions and dimensions of photographed objects are estimated. Framing is not proof of matching albedo or construction.')
        results[name]=result;print(name,'RMS',result['residual_rms_pixels'],'lens',result['shot']['lens'])
    Path('build/photo-calibration.json').write_text(json.dumps(results,indent=2)+'\n')


def compose(folder=Path('renders/lookdev-matches')):
    folder=Path(folder);font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),20);source='source' in folder.name
    for name,r in json.loads(Path('build/photo-calibration.json').read_text()).items():
        photo=Image.open(r['photo']).convert('RGB').crop(r['crop']);render=Image.open(folder/(name+'.png')).convert('RGB');width=1000;height=round(width*photo.height/photo.width)
        out=Image.new('RGB',(width*2,height+118),'#e8e7df');d=ImageDraw.Draw(out)
        out.paste(render.resize((width,height),Image.Resampling.LANCZOS),(0,50));out.paste(photo.resize((width,height),Image.Resampling.LANCZOS),(width,50))
        d.text((14,14),r['title']+' / original export',font=font,fill='#21332c');d.text((width+14,14),'Neutral-balanced period photograph',font=font,fill='#21332c')
        finish='original manufacture fields + height' if source else 'exported baked PBR'
        d.text((14,height+66),'Estimated %.1f mm; RMS %.1f px; %s.'%(r['shot']['lens'],r['residual_rms_pixels'],finish),font=font,fill='#21332c')
        out.save(folder/(name+'-pair.jpg'),quality=94)
        overlay=photo.copy();dd=ImageDraw.Draw(overlay)
        for target,pred in zip(r['measured_pixels'],r['projected_pixels']):
            x,y=target;dd.ellipse((x-5,y-5,x+5,y+5),outline='lime',width=2);dd.line((*target,*pred),fill='red',width=2)
        overlay.save(folder/(name+'-residuals.jpg'),quality=94)
    from kit.contact import contact
    contact(sorted(folder.glob('*-pair.jpg')),folder/'matched-contact.jpg',width=1800,title='Period coffee shop comparisons — '+('source finish' if source else 'exported PBR sites'))


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--prepare',action='store_true');a.add_argument('--compose',action='store_true');a.add_argument('--renders',type=Path,default=Path('renders/lookdev-matches'));a=a.parse_args()
    prepare() if a.prepare else compose(a.renders)
