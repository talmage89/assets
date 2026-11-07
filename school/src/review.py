"""Contact sheets and objective exposure facts; no final docs at this gate."""
import json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font


def sheet(paths,out,columns=3,thumb=480):
    if not paths:return
    h=350;rows=math.ceil(len(paths)/columns);im=Image.new('RGB',(columns*thumb,rows*h),(25,29,26));d=ImageDraw.Draw(im);font=ImageFont.truetype(find_font('DejaVu Sans','Book'),15)
    for i,p in enumerate(paths):
        src=Image.open(p).convert('RGB');src.thumbnail((thumb,h-28));x=(i%columns)*thumb;y=(i//columns)*h
        label=('Eevee / ' if p.parent.parent.name=='eevee' else '')+p.parent.name+' / '+p.stem
        im.paste(src,(x+(thumb-src.width)//2,y+26));d.text((x+8,y+5),label,font=font,fill=(224,224,213))
    out.parent.mkdir(parents=True,exist_ok=True);im.save(out,quality=91,optimize=True)


def main():
    folder=Path('renders/lookdev');paths=sorted(folder.glob('*/*.png'))+sorted(Path('renders/eevee').glob('*/*.png'));sheet(paths,folder/'contact.jpg')
    stats={}
    for p in folder.glob('*/hero.png'):
        a=np.array(Image.open(p).convert('RGB'))/255;y=a@np.array([.2126,.7152,.0722]);stats[p.parent.name]=dict(display_luma_p1_p50_p99=np.percentile(y,[1,50,99]).tolist(),all_channel_clipped_fraction=float((a.min(2)>.99).mean()),camera=json.loads((p.parent/'provenance.json').read_text())['hero']['camera'])
    Path('build/tonal-check.json').write_text(json.dumps(stats,indent=2))
    sheet(sorted(Path('renders/look-matches').glob('*-pair.jpg')),Path('renders/look-matches/contact.jpg'),columns=1,thumb=1600)
    sheet(sorted(Path('renders/source-matches').glob('*-pair.jpg')),Path('renders/source-matches/contact.jpg'),columns=1,thumb=1600)
    comparisons(folder)
    from site_evidence import main as site_plans
    site_plans()
    print('REVIEW SHEETS',folder/'contact.jpg')


def comparisons(folder):
    """Full-size, identical-world-camera baseline pairs; no docs are written."""
    import hashlib,sys
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    from plans import school
    report={};dest=Path('renders/before-after');dest.mkdir(parents=True,exist_ok=True)
    for seed in (101,102,103):
        p=school(seed);old=Path('renders/before')/str(seed);new=folder/str(seed)
        if not (old/'provenance.json').exists() or not (new/'provenance.json').exists():continue
        before=json.loads((old/'provenance.json').read_text());after=json.loads((new/'provenance.json').read_text())
        for name in ('hero','above','rear','windows'):
            first=old/(name+'.png');last=new/('legacy_'+name+'.png')
            if not first.exists() or not last.exists():continue
            bc=before[name]['camera'];ac=after['legacy_'+name]['camera']
            error=max(float(np.max(abs(np.array(ac[k])-np.array(bc[k])))) for k in ('location','target'))
            assert error<1e-5 and abs(ac['lens']-bc['lens'])<1e-6,(seed,name,'baseline camera changed',error)
            left,right=[Image.open(f).convert('RGB') for f in (first,last)];width=max(800,min(left.width,right.width));h=round(width/bc['aspect'])
            pair=Image.new('RGB',(width*2,h+62),(24,28,25));draw=ImageDraw.Draw(pair);font=ImageFont.truetype(find_font('DejaVu Sans','Book'),18)
            pair.paste(left.resize((width,h),Image.Resampling.LANCZOS),(0,62));pair.paste(right.resize((width,h),Image.Resampling.LANCZOS),(width,62))
            draw.text((14,10),f'{seed} / {name} / accepted checkpoint',font=font,fill=(230,231,221))
            draw.text((width+14,10),'Revised form and PBR / identical world camera',font=font,fill=(230,231,221))
            draw.text((14,35),'Camera, lens and direct-light settings are fixed; the new campus frontage and site arrangement may turn.',font=ImageFont.truetype(find_font('DejaVu Sans','Book'),14),fill=(198,201,190))
            out=dest/f'{seed}-{name}.jpg';pair.save(out,quality=93,optimize=True)
            report[out.as_posix()]=dict(baseline_camera=bc,revised_camera=ac,campus_yaw_degrees=p['site_yaw'],max_camera_residual_m=error,panel_width=width,before_image_sha256=hashlib.sha256(first.read_bytes()).hexdigest(),after_image_sha256=hashlib.sha256(last.read_bytes()).hexdigest(),after_package_sha256=after['legacy_'+name]['package_sha256'])
    Path('build/before-after.json').write_text(json.dumps(report,indent=2))
    sheet(sorted(p for p in dest.glob('*.jpg') if p.name!='contact.jpg'),dest/'contact.jpg',columns=1,thumb=1600)

if __name__=='__main__':main()
