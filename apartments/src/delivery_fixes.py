"""Native before/after fix crops and disclosed pavement-value measurements.

The accepted-session witnesses live in the worktree's ignored build archive;
they are never substituted for new exports or committed documentation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]))
from kit.fonts import find_font


def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def patch(path,box):
    a=np.asarray(Image.open(path).convert('RGB'),dtype='float32')/255
    x0,y0,x1,y1=box;q=a[y0:y1,x0:x1];assert q.size
    y=q@np.array([.2126,.7152,.0722])
    return dict(box_native_px=box,median_Yprime=float(np.median(y)),p10_p90_Yprime=np.quantile(y,[.1,.9]).tolist(),median_RGB=np.median(q,axis=(0,1)).tolist())


def run(before,after,out):
    out.mkdir(parents=True,exist_ok=True);font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),22);rows={}
    cases={
      'asphalt':('renders/checkpoint/Complex-301/hero.png','Complex-301/hero.png',(0,570,1400,786)),
      'dormer':('renders/matches/used-garden.png','matches/used-garden.png',(500,185,1400,420)),
      'planting':('renders/checkpoint/Complex-301/hero.png','Complex-301/hero.png',(200,420,1250,610)),
      'dusk':('renders/checkpoint/Complex-301/dusk.png','Complex-301/dusk.png',(0,390,1400,786))}
    for key,(old,new,box) in cases.items():
        a,b=before/old,after/new;ims=[Image.open(p).convert('RGB') for p in (a,b)]
        assert ims[0].size==ims[1].size,(key,[im.size for im in ims]);assert box[2]-box[0]>=800
        crops=[im.crop(box) for im in ims];w,h=crops[0].size
        plate=Image.new('RGB',(w,2*h+90),'#e8e8e1');draw=ImageDraw.Draw(plate)
        for y,label,im in ((0,'Before / accepted e382440 / native pixels',crops[0]),(h+45,'After / actual external PBR export / native pixels',crops[1])):
            draw.text((12,y+10),label,font=font,fill='#202720');plate.paste(im,(0,y+45))
        path=out/(key+'-before-after.jpg');plate.save(path,quality=96,optimize=True)
        rows[key]=dict(before=str(a),after=str(b),before_sha256=digest(a),after_sha256=digest(b),crop_native_px=box,width_each_px=w,resampled=False)
    photo=Path('refs/townhouses-balanced.jpg');photo_boxes=((500,1030,720,1090),(100,1090,600,1180),(750,1000,1000,1090))
    render_boxes=((350,710,550,760),(1050,705,1250,750))
    values=dict(scope='Encoded display RGB Yprime (.2126,.7152,.0722), not linear luminance, albedo or calibrated photometry.',
                photo=str(photo),photo_sha256=digest(photo),neutral='White garage panel (679,774)-(704,799); linear neutral-preserving balance from neutral_refs.py.',
                photo_patches=[patch(photo,b) for b in photo_boxes],
                hero_before=[patch(before/cases['asphalt'][0],b) for b in render_boxes],
                hero_after=[patch(after/cases['asphalt'][1],b) for b in render_boxes])
    street=after/'matches/garage-row.png';street_boxes=((1000,720,1350,820),)
    values['public_street_match']=dict(image=str(street),sha256=digest(street),patches=[patch(street,b) for b in street_boxes])
    for path,boxes,name in ((photo,photo_boxes,'photo-pavement-patches.jpg'),(after/cases['asphalt'][1],render_boxes,'hero-pavement-patches.jpg'),(street,street_boxes,'public-street-patch.jpg')):
        im=Image.open(path).convert('RGB');draw=ImageDraw.Draw(im)
        for i,box in enumerate(boxes):draw.rectangle(box,outline='#ed8b37',width=3);draw.text((box[0]+4,box[1]+4),str(i+1),fill='#ffe490')
        im.save(out/name,quality=96,optimize=True)
    # Camera equality is independent of the crop compositor.
    oldcam=json.loads((before/'renders/checkpoint/Complex-301/provenance.json').read_text())
    newcam=json.loads((after/'Complex-301/provenance.json').read_text())
    for key in ('hero','dusk'):
        for prop in ('location','target','lens','aspect'):
            assert np.allclose(oldcam[key]['camera'][prop],newcam[key]['camera'][prop],atol=1e-6),(key,prop)
    oldmatch=json.loads((before/'renders/matches/provenance.json').read_text())['used-garden']['camera']
    newmatch=json.loads((after/'matches/provenance.json').read_text())['used-garden']['camera']
    for prop in ('location','target','lens','aspect'):
        assert np.allclose(oldmatch[prop],newmatch[prop],atol=1e-6),('dormer',prop)
    values['surface_probes']=newcam['hero']['camera'].get('paving_surface_probes',[])
    rows['same_hero_dusk_cameras_verified']=True
    rows['same_dormer_camera_verified']=True
    (out/'crops.json').write_text(json.dumps(rows,indent=2)+'\n');(out/'asphalt-values.json').write_text(json.dumps(values,indent=2)+'\n')
    print('FIX CROPS',[(k,v['width_each_px']) for k,v in rows.items() if isinstance(v,dict)])
    print('PHOTO',[round(q['median_Yprime'],3) for q in values['photo_patches']],'HERO',[round(q['median_Yprime'],3) for q in values['hero_before']],'->',[round(q['median_Yprime'],3) for q in values['hero_after']])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--before',type=Path,default=HERE.parents[1]/'build/apartments-delivery-baseline');p.add_argument('--after',type=Path,default=Path('renders/delivery-pass2'));p.add_argument('--out',type=Path,default=Path('renders/delivery-fixes'));a=p.parse_args();run(a.before,a.after,a.out)
