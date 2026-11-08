"""Native-pixel before/after evidence; never enlarges a panel."""
import argparse,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font


def compare(before,after,out):
    out.mkdir(parents=True,exist_ok=True);font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),21)
    cameras=json.loads((before/'provenance.json').read_text());current=json.loads((after/'provenance.json').read_text());receipt=[]
    cases=[('01-traffic-old','Park-101','hero',(0,.18,1,1)),('01-traffic-new','Park-202','hero',(0,.18,1,1)),
           ('02-home-age','Park-101','row',(.15,.18,1,1)),('03-lanes-old','Park-101','hero',(.15,.43,.95,1)),
           ('02-apron-age','Park-101','single-2009',(0,.33,1,1)),
           ('03-lanes-new','Park-202','hero',(.15,.43,.95,1)),('04-lawn-old','Park-101','row',(0,.44,1,1)),
           ('04-turf-trees','Park-101','above',(0,0,1,1)),('05-street-same-camera','Park-101','street-2007',(0,0,1,1))]
    def frame(folder,stem,shot):
        path=folder/stem/(shot+'.png')
        return path if path.is_file() else folder/'matches'/stem/(shot+'.png')
    for name,stem,shot,box in cases:
        a=next(q for q in cameras if q['stem']==stem and q['shot']==shot);b=next(q for q in current if q['stem']==stem and q['shot']==shot)
        delta=max(abs(x-y) for aa,bb in zip(a['camera_matrix_world'],b['camera_matrix_world']) for x,y in zip(aa,bb));changed=shot=='street-2007' and delta>=1e-6
        assert changed or delta<1e-6
        if not changed:assert a['camera_parameters']==b['camera_parameters']
        for k in ('direction','sun_energy','sky_strength','exposure','angle_degrees'):assert a['light'][k]==b['light'][k],(name,k)
        aa=Image.open(frame(before,stem,shot)).convert('RGB');bb=Image.open(frame(after,stem,shot)).convert('RGB');assert aa.size==bb.size
        region=tuple(round(v*(aa.width if i%2==0 else aa.height)) for i,v in enumerate(box));aa=aa.crop(region);bb=bb.crop(region);assert aa.width>=800
        aa.save(out/(name+'-before.jpg'),quality=96);bb.save(out/(name+'-after.jpg'),quality=96)
        pair=Image.new('RGB',(aa.width*2,aa.height+45),(230,231,224));pair.paste(aa,(0,45));pair.paste(bb,(aa.width,45));d=ImageDraw.Draw(pair)
        d.text((14,10),'b0dbccc / original room camera' if changed else 'b0dbccc / accepted camera and light',font=font,fill=(25,30,25));d.text((aa.width+14,10),'Lane camera / framing changed as requested' if changed else 'Aged export / same camera and light',font=font,fill=(25,30,25))
        path=out/(name+'.jpg');pair.save(path,quality=95,optimize=True)
        receipt.append(dict(path=str(path),before=str(frame(before,stem,shot)),after=str(frame(after,stem,shot)),crop_pixels=region,panel_size=aa.size,max_camera_delta=delta,same_camera=not changed,same_light=True))
    historic=frame(before,'Park-101','street-historical')
    if historic.is_file():
        aa=Image.open(historic).convert('RGB');bb=Image.open(frame(after,'Park-101','street-2007')).convert('RGB');assert aa.size==bb.size and aa.width>=800
        pair=Image.new('RGB',(aa.width*2,aa.height+45),(230,231,224));pair.paste(aa,(0,45));pair.paste(bb,(aa.width,45));d=ImageDraw.Draw(pair)
        d.text((14,10),'b0dbccc / original room camera',font=font,fill=(25,30,25));d.text((aa.width+14,10),'Lane camera / framing changed as requested',font=font,fill=(25,30,25))
        path=out/'05-street-framing.jpg';pair.save(path,quality=95,optimize=True)
        receipt.append(dict(path=str(path),before=str(historic),after=str(frame(after,'Park-101','street-2007')),panel_size=aa.size,same_camera=False,scope='Explicit camera correction; same-camera package comparison supplied separately'))
    (out/'cameras.json').write_text(json.dumps(receipt,indent=2))
    print('NATIVE CROP PAIRS',len(receipt))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--before',type=Path,default=Path('renders/checkpoint/look5'));p.add_argument('--after',type=Path,required=True);p.add_argument('--out',type=Path,default=Path('renders/age-fixes'));a=p.parse_args();compare(a.before,a.after,a.out)
