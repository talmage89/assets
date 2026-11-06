"""Measure balanced photographic appearances, never infer calibrated albedo."""
import colorsys,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.image_io import srgb_to_linear,linear_to_srgb
PHOTOS={
 'residential-b':dict(neutral=(2150,330,2220,380),assumption='Achromatic bright cloud; approximate daylight white point',patches=dict(wood=(1058,410,1065,485),tank=(1076,468,1091,496),sky_upper=(700,50,850,95),sky_lower=(870,670,940,720))),
 'street-b':dict(neutral=(650,25,750,65),assumption='Achromatic fog/cloud away from tree silhouettes; diffuse wood comparator',patches=dict(wood=(309,450,325,650))),
 'residential-a':dict(neutral=(20,95,55,120),assumption='Achromatic thin cloud; approximate daylight white point',patches=dict(sky_upper=(600,20,700,60),sky_lower=(530,145,570,175))),
 'street-a':dict(neutral=(1450,1000,1490,1030),assumption='White painted facade in sun; approximate daylight white point',patches=dict(wood=(1017,600,1034,880),sky_upper=(1500,20,1600,90),sky_lower=(2250,590,2320,625))),
}
RENDERS={
 'md_top':dict(path='renders/matches/md_top.png',patches=dict(wood=(.4575,.1797,.4683,.2268),tank=(.5083,.3261,.525,.3442),sky_upper=(.025,.0217,.125,.0942))),
 'crossarm':dict(path='renders/final/101/crossarm.png',patches=dict(sun_wood=(.493,.237,.50,.289))),
 'hero':dict(path='renders/final/101/hero.png',patches=dict(sky_upper=(.6875,.01594,.8125,.05314),sky_middle=(.5625,.6642,.59375,.6854),sky_lower=(.5625,.703,.59375,.713))),
 'base':dict(path='renders/final/101/base.png',patches=dict(upper_base_wood=(.53,.19,.56,.30),wet_wood=(.53,.70,.56,.77))),
}

def stats(rgb):
    c=np.median(rgb.reshape(-1,3),axis=0);h,s,v=colorsys.rgb_to_hsv(*c)
    return dict(srgb_255=np.round(c*255,2).tolist(),hue_degrees=round(h*360,2),saturation=round(s,4),value=round(v,4),Yprime=round(float(c@np.array([.2126,.7152,.0722])),4))

def main():
    out=Path('build/color-review');out.mkdir(parents=True,exist_ok=True);rows={}
    for name,spec in PHOTOS.items():
        im=Image.open('refs/'+name+'.jpg').convert('RGB');lin=srgb_to_linear(np.asarray(im,float)/255)
        x,y,u,v=spec['neutral'];n=np.median(lin[y:v,x:u].reshape(-1,3),0);g=n.mean()/n
        balanced=np.clip(linear_to_srgb(lin*g),0,1);patches={}
        annotation=Image.fromarray(np.uint8(balanced*255+.5));draw=ImageDraw.Draw(annotation)
        for key,(x,y,u,v) in spec['patches'].items():
            patches[key]=dict(roi=[x,y,u,v],**stats(balanced[y:v,x:u]));draw.rectangle((x,y,u,v),outline='red',width=2);draw.text((u+3,y),key,fill='red')
        draw.rectangle(spec['neutral'],outline='lime',width=2);annotation.save(out/(name+'-patches.jpg'),quality=97)
        rows[name]=dict(neutral_roi=spec['neutral'],neutral_assumption=spec['assumption'],linear_gains=g.tolist(),patches=patches)
    rendered={}
    for name,spec in RENDERS.items():
        path=Path(spec['path'])
        if not path.exists():continue
        im=Image.open(path).convert('RGB');a=np.asarray(im,float)/255;draw=ImageDraw.Draw(im);patches={}
        for key,region in spec['patches'].items():
            x,y,u,v=[round(c*im.size[i%2]) for i,c in enumerate(region)];patches[key]=dict(roi=[x,y,u,v],**stats(a[y:v,x:u]));draw.rectangle((x,y,u,v),outline='red',width=2);draw.text((u+3,y),key,fill='red')
        im.save(out/(name+'-render-patches.jpg'),quality=97);rendered[name]=dict(source=str(path),patches=patches)
    comparison={}
    for key,ref,render,photo_patch,render_patch in [
        ('wood_md','residential-b','md_top','wood','wood'),
        ('wood_sun','street-a','crossarm','wood','sun_wood'),
        ('tank_md','residential-b','md_top','tank','tank'),
        ('sky_upper_md','residential-b','md_top','sky_upper','sky_upper'),
        ('sky_upper_nc','residential-a','hero','sky_upper','sky_upper'),
        ('sky_lower_nc','residential-a','hero','sky_lower','sky_lower'),
    ]:
        if render not in rendered:continue
        a=rows[ref]['patches'][photo_patch];b=rendered[render]['patches'][render_patch]
        comparison[key]=dict(photo_srgb=a['srgb_255'],render_srgb=b['srgb_255'],photo_Yprime=a['Yprime'],render_Yprime=b['Yprime'],Yprime_difference=round(b['Yprime']-a['Yprime'],4))
    result=dict(photographs=rows,renders=rendered,comparisons=comparison,scope='Balanced display RGB/HSV/Y prime. No calibrated reflectance or photographic exposure. Upper/lower sky are image zones, not surveyed elevation angles. Render patches are selected on the delivered material under the stated estimated light; equipment mounting differences preclude copying photo pixel rectangles onto the render.')
    (out/'measurements.json').write_text(json.dumps(result,indent=2));print('COLOR REVIEW',json.dumps(comparison))

if __name__=='__main__':main()
