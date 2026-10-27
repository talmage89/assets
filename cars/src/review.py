"""Checkpoint measurement overlays/contact; never writes committed docs."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
FONT='/usr/share/fonts/noto/NotoSans-Regular.ttf'
def main():
    p=argparse.ArgumentParser();p.add_argument('--renders',required=True);a=p.parse_args();root=Path(a.renders)
    shots=json.loads((root/'shots.json').read_text());font=ImageFont.truetype(FONT,21);small=ImageFont.truetype(FONT,17)
    tonal={}
    for name in shots:
        rgba=Image.open(root/(name+'.png')).convert('RGBA')
        arr=np.asarray(rgba);rgb=arr[:,:,:3];mask=arr[:,:,3]>250
        # Orthographic foreground masks exclude the transparent background.
        if name in ['side','front','top']:
            lum=rgb[mask]@np.array([.2126,.7152,.0722])
            tonal[name]=dict(foreground_value_p5_p50_p95=np.percentile(lum,[5,50,95]).tolist(),
                             bright_clipped_fraction=float(np.mean(np.max(rgb[mask],axis=1)>=250)),
                             dark_fraction=float(np.mean(lum<12)))
        bg=Image.new('RGBA',rgba.size,(226,229,232,255));bg.alpha_composite(rgba)
        bg.convert('RGB').save(root/(name+'.jpg'),quality=94)
    (root/'tonal-check.json').write_text(json.dumps(tonal,indent=2))
    for name in ['side','front','top']:
        data=shots[name];im=Image.open(root/(name+'.png')).convert('RGBA');bg=Image.new('RGBA',im.size,(226,229,232,255));bg.alpha_composite(im)
        im=bg.convert('RGB');d=ImageDraw.Draw(im);pts=data['points']
        def horizontal(k1,k2,y,label):
            x1=pts[k1][0];x2=pts[k2][0];x1,x2=sorted((x1,x2));col=(40,83,110)
            d.line((x1,y,x2,y),fill=col,width=2)
            for x in (x1,x2):d.line((x,y-9,x,y+9),fill=col,width=2)
            box=d.textbbox((0,0),label,font=small);w=box[2]-box[0]
            d.rectangle(((x1+x2-w)/2-5,y-28,(x1+x2+w)/2+5,y-4),fill=(226,229,232))
            d.text(((x1+x2-w)/2,y-29),label,font=small,fill=col)
        if name=='side':
            horizontal('front_ground','rear_ground',im.height-30,'5890 mm overall / manufacturer 231.9 in')
            horizontal('front_axle','rear_axle',im.height-82,'3683 mm wheelbase / manufacturer 145.0 in')
            horizontal('bed_front','bed_rear',110,'1704 mm bed floor / 67.1 in')
            x=im.width-60;z0=pts['origin'][1];zt=pts['roof'][1]
            d.line((x,zt,x,z0),fill=(40,83,110),width=2);d.text((x-190,(zt+z0)/2),'1961 mm roof',font=small,fill=(40,83,110))
        elif name=='front':
            horizontal('left','right',im.height-42,'2029 mm body / 79.9 in')
            horizontal('track_left','track_right',im.height-94,'1716 mm track')
        else:
            # Top camera is rolled 90 degrees; length lies horizontally.
            horizontal('front_ground','rear_ground',im.height-35,'5890 mm overall')
            horizontal('bed_front','bed_rear',90,'1704 mm clear bed length')
        d.text((22,18),'ALDER C150 / '+name.upper()+' / BODY FORM CHECKPOINT',font=font,fill=(25,38,48))
        d.text((22,48),'Dimension lines are cited targets; actual surface measurements: build/form-check.json',font=small,fill=(54,66,75))
        im.save(root/(name+'-dimensions.jpg'),quality=93)
    files=['front_three_quarter.jpg','rear_three_quarter.jpg','side-dimensions.jpg','front-dimensions.jpg','top-dimensions.jpg',
           'stripes_front.jpg','stripes_side.jpg','match_front-pair.jpg','match_rear-pair.jpg']
    tilew,tileh=900,600;contact=Image.new('RGB',(tilew*3,tileh*3),(220,224,228));d=ImageDraw.Draw(contact)
    for i,name in enumerate(files):
        im=Image.open(root/name).convert('RGBA');im.thumbnail((tilew-20,tileh-56),Image.Resampling.LANCZOS)
        x=(i%3)*tilew+(tilew-im.width)//2;y=(i//3)*tileh+46+(tileh-56-im.height)//2
        contact.paste(im,(x,y),im);d.text(((i%3)*tilew+16,(i//3)*tileh+10),name,font=font,fill=(25,38,48))
    contact.save(root/'contact.jpg',quality=93)
    print('CHECKPOINT CONTACT',root/'contact.jpg')
if __name__=='__main__':main()
