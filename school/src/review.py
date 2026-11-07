"""Export receipts, review sheets and explicitly gated final documentation."""
import json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font


def sheet(paths,out,columns=3,thumb=480,height=350):
    if not paths:return
    h=height;rows=math.ceil(len(paths)/columns);im=Image.new('RGB',(columns*thumb,rows*h),(25,29,26));d=ImageDraw.Draw(im);font=ImageFont.truetype(find_font('DejaVu Sans','Book'),15)
    for i,p in enumerate(paths):
        src=Image.open(p).convert('RGB');src.thumbnail((thumb,h-28));x=(i%columns)*thumb;y=(i//columns)*h
        label=('Eevee / ' if p.parent.parent.name=='eevee' else '')+p.parent.name+' / '+p.stem
        im.paste(src,(x+(thumb-src.width)//2,y+26));d.text((x+8,y+5),label,font=font,fill=(224,224,213))
    out.parent.mkdir(parents=True,exist_ok=True);im.save(out,quality=91,optimize=True)


def main():
    folder=Path('renders/final');paths=sorted(folder.glob('*/*.png'))+sorted(Path('renders/eevee').glob('*/*.png'));sheet(paths,folder/'contact.jpg')
    stats={}
    for p in folder.glob('*/hero.png'):
        a=np.array(Image.open(p).convert('RGB'))/255;y=a@np.array([.2126,.7152,.0722]);stats[p.parent.name]=dict(display_luma_p1_p50_p99=np.percentile(y,[1,50,99]).tolist(),all_channel_clipped_fraction=float((a.min(2)>.99).mean()),camera=json.loads((p.parent/'provenance.json').read_text())['hero']['camera'])
    Path('build/tonal-check.json').write_text(json.dumps(stats,indent=2))
    sheet(sorted(Path('renders/final-matches').glob('*-pair.jpg')),Path('renders/final-matches/contact.jpg'),columns=1,thumb=1600)
    sheet(sorted(Path('renders/source-matches').glob('*-pair.jpg')),Path('renders/source-matches/contact.jpg'),columns=1,thumb=1600)
    from fix_evidence import main as evidence
    evidence()
    sheet(sorted(p for p in Path('renders/fixes').glob('*.jpg') if p.name!='contact.jpg'),Path('renders/fixes/contact.jpg'),columns=1,thumb=1600)
    sheet([folder/str(seed)/'plan.png' for seed in (101,102,103)],folder/'plans.jpg',columns=3,thumb=1400,height=1220)
    from site_evidence import main as site_plans
    site_plans()
    from render_audit import main as audit
    audit()
    if '--final' in sys.argv:docs(folder)
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

def docs(folder):
    """Manual full-size critique must name the current exported packages."""
    import hashlib
    approval=json.loads(Path('build/final-review.json').read_text())
    audit=json.loads(Path('build/delivery-audit.json').read_text())
    for seed in (101,102,103):
        assert approval['packages'][str(seed)]==audit['Campus-'+str(seed)]['package_sha256'],'Final export changed after visual review'
    assert approval['all_six_fixes_visible'] and approval['every_final_opened']
    current=json.loads(Path('build/render-audit.json').read_text())['views']
    assert approval['inspected_final_images']=={p:r['image_sha256'] for p,r in current.items()},'Final images changed after full-size review'
    dest=Path('docs');dest.mkdir(exist_ok=True)
    for seed in (101,102,103):save_jpg(Image.open(folder/str(seed)/'hero.png').convert('RGB'),dest/f'hero-{seed}.jpg')
    sheet([*[folder/str(seed)/'above.png' for seed in (101,102,103)],folder/'plans.jpg'],Path('build/family-doc.jpg'),columns=2,thumb=800,height=560)
    save_jpg(Image.open('build/family-doc.jpg'),dest/'family.jpg')
    sheet([folder/'102/windows.png',folder/'101/entry.png',folder/'103/gym.png',folder/'101/door.png',folder/'102/scale.png',Path('renders/eevee/101/hero.png')],Path('build/details-doc.jpg'),columns=2,thumb=800,height=560)
    save_jpg(Image.open('build/details-doc.jpg'),dest/'details.jpg')
    print('FINAL DOCS',[(p.name,p.stat().st_size) for p in dest.glob('*.jpg')])


def save_jpg(im,path):
    im.thumbnail((1600,10000),Image.Resampling.LANCZOS)
    for quality in range(92,29,-2):
        im.save(path,quality=quality,optimize=True,progressive=True)
        if path.stat().st_size<=200000:return
    raise ValueError('Could not meet documentation byte limit: '+str(path))


if __name__=='__main__':main()
