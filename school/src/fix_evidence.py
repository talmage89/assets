"""Native-size crops, paired only when the exported camera is identical."""
import hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
FONT=ImageFont.truetype(find_font('DejaVu Sans','Book'),18)


def pair(left,right,out,label,check_camera=True,left_name=None,right_name=None,crop=None):
    left,right=Path(left),Path(right);a,b=[Image.open(p).convert('RGB') for p in (left,right)]
    assert min(a.width,b.width)>=800,(left,right,'native panels too small')
    assert a.size==b.size,(left,right,'native framing differs')
    camera=None
    if check_camera:
        ca=json.loads((left.parent/'provenance.json').read_text())[left_name or left.stem]['camera']
        cb=json.loads((right.parent/'provenance.json').read_text())[right_name or right.stem]['camera']
        assert all(ca[k]==cb[k] for k in ('location','target','lens','aspect')),(out,'camera mismatch',ca,cb)
        camera=ca
    if crop:
        assert 0<=crop[0]<crop[2]<=a.width and 0<=crop[1]<crop[3]<=a.height,'Crop must remain inside native pixels'
        a,b=a.crop(crop),b.crop(crop)
        assert a.width>=800,'Never enlarge a small crop to claim native-size evidence'
    im=Image.new('RGB',(a.width*2,a.height+48),(25,29,26));im.paste(a,(0,48));im.paste(b,(a.width,48));d=ImageDraw.Draw(im)
    d.text((14,12),'Before / '+label,font=FONT,fill='white');d.text((a.width+14,12),'After / '+('identical camera' if camera else 'reframed hero'),font=FONT,fill='white')
    out.parent.mkdir(parents=True,exist_ok=True);im.save(out,quality=95,optimize=True)
    return dict(before=str(left),after=str(right),panel_pixels=a.size,crop=crop,camera=camera,sha256=[hashlib.sha256(p.read_bytes()).hexdigest() for p in (left,right)])


def main():
    final=Path('renders/final');before=Path('renders/fix-before');dest=Path('renders/fixes');rows={}
    for seed in (101,102,103):
        s=str(seed)
        for shot in ('hero','above','entry','windows','door'):
            out=dest/(s+'-'+shot+'.jpg');rows[out.name]=pair(before/s/(shot+'.png'),final/s/(shot+'.png'),out,'school '+s+' / '+shot)
        out=dest/(s+'-wear-crop.jpg');rows[out.name]=pair(before/s/'hero.png',final/s/'hero.png',out,'school '+s+' / maintained facade and drain',crop=(500,180,1400,650))
        # The 103 slit and the vehicle-body changes retain the old hero camera.
        out=dest/(s+'-accepted-camera.jpg');rows[out.name]=pair(Path('renders/accepted-lookdev')/s/'hero.png',final/s/'accepted_hero.png',out,'school '+s+' / curb, planting, cars',right_name='accepted_hero')
        old=Image.open(Path('renders/accepted-lookdev')/s/'hero.png').convert('RGB');new=Image.open(final/s/'hero.png').convert('RGB')
        # Composition changes necessarily use different cameras. Keep this
        # comparison separately labeled, without calling it same-camera proof.
        old=old.resize((1400,round(old.height*1400/old.width)));new=new.resize((1400,round(new.height*1400/new.width)))
        im=Image.new('RGB',(2800,max(old.height,new.height)+48),(25,29,26));im.paste(old,(0,48));im.paste(new,(1400,48));d=ImageDraw.Draw(im);d.text((14,12),s+' / accepted wide hero',font=FONT,fill='white');d.text((1414,12),'New drop-off composition / 42mm',font=FONT,fill='white');im.save(dest/(s+'-framing.jpg'),quality=95,optimize=True)
    out=dest/'ribbon-glass.jpg';rows[out.name]=pair('renders/fix-before-matches/ribbon.png','renders/final-matches/ribbon.png',out,'glass and classroom / refitted north camera')
    out=dest/'103-curb-crop.jpg';rows[out.name]=pair('renders/accepted-lookdev/103/hero.png','renders/final/103/accepted_hero.png',out,'curb outer face',right_name='accepted_hero',crop=(200,450,1400,778))
    out=dest/'102-cars-crop.jpg';rows[out.name]=pair('renders/accepted-lookdev/102/hero.png','renders/final/102/accepted_hero.png',out,'native body and paint variation',right_name='accepted_hero',crop=(600,300,1400,778))
    Path('build/fix-evidence.json').write_text(json.dumps(rows,indent=2))
    print('FIX EVIDENCE',len(rows),'native same-camera pairs')

if __name__=='__main__':main()
