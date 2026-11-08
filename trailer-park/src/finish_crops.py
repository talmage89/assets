"""Same-camera native crops for the final four requested corrections."""
import argparse,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font


def compare(before,after,out):
    out.mkdir(parents=True,exist_ok=True);font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),21)
    a=json.loads((before/'provenance.json').read_text());b=json.loads((after/'provenance.json').read_text());receipt=[]
    def frame(folder,stem,shot):
        path=folder/stem/(shot+'.png')
        return path if path.is_file() else folder/'matches'/stem/(shot+'.png')
    def pair(name,aa,bb,left,right):
        assert min(aa.width,bb.width)>=800
        aa.save(out/(name+'-before.jpg'),quality=96);bb.save(out/(name+'-after.jpg'),quality=96)
        im=Image.new('RGB',(aa.width+bb.width,max(aa.height,bb.height)+45),(230,231,224));im.paste(aa,(0,45));im.paste(bb,(aa.width,45))
        draw=ImageDraw.Draw(im);draw.text((14,10),left,font=font,fill=(25,30,25));draw.text((aa.width+14,10),right,font=font,fill=(25,30,25))
        im.save(out/(name+'.jpg'),quality=95,optimize=True)
    cases=[('01-home-age','Park-101','row',(.15,.18,1,1)),('02-july-lawn','Park-101','row',(0,.44,1,1)),
           ('03-lane-old','Park-101','hero',(.15,.43,.95,1)),('03-lane-new','Park-202','hero',(.15,.43,.95,1)),
           ('04-level-street','Park-101','street-2007',(0,0,1,1)),('05-old-hero','Park-101','hero',(0,0,1,1))]
    for name,stem,shot,box in cases:
        aa=next(r for r in a if r['stem']==stem and r['shot']==shot);bb=next(r for r in b if r['stem']==stem and r['shot']==shot)
        delta=max(abs(x-y) for p,q in zip(aa['camera_matrix_world'],bb['camera_matrix_world']) for x,y in zip(p,q));assert delta<1e-6
        assert aa['camera_parameters']==bb['camera_parameters']
        for key in ('direction','sun_energy','sky_strength','exposure','angle_degrees','sky_saturation','camera_sky_strength','camera_sky_saturation'):assert aa['light'][key]==bb['light'][key]
        im=Image.open(frame(before,stem,shot)).convert('RGB');other=Image.open(frame(after,stem,shot)).convert('RGB');assert im.size==other.size
        crop=tuple(round(v*(im.width if k%2==0 else im.height)) for k,v in enumerate(box))
        im=im.crop(crop);other=other.crop(crop);pair(name,im,other,'aa071cd / same camera and light','Current export / same camera and light')
        receipt.append(dict(path=str(out/(name+'.jpg')),panel_size=im.size,crop_pixels=crop,max_camera_delta=delta,same_light=True))
    # Camera corrections also retain the actual rolled historical view.
    history=Path('renders/age-pass3/matches/Park-101/street-2007.png')
    if history.exists():
        pair('04-street-roll-correction',Image.open(history).convert('RGB'),Image.open(frame(after,'Park-101','street-2007')).convert('RGB'),
             'Previous rolled camera / 2007 curved apron','Level camera with lens rise / replacement photo')
    (out/'cameras.json').write_text(json.dumps(receipt,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--before',type=Path,default=Path('renders/finish-before'));p.add_argument('--after',type=Path,required=True);p.add_argument('--out',type=Path,default=Path('renders/finish-fixes'));a=p.parse_args();compare(a.before,a.after,a.out)
