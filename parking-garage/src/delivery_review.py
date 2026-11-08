"""Current-export contact sheets and fixed-camera correction evidence.

Historical PNGs are optional local review evidence, never a fresh-build input.
Docs are a separate, explicitly gated final action after full-size inspection.
"""
import argparse,hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import review_sheet
from kit.fonts import find_font
from lookdev_review import verify_receipt


def fixes(folder):
    out=Path('renders/delivery-fixes');out.mkdir(parents=True,exist_ok=True);rows=[]
    history=Path('build/delivery-before/views.json')
    old=json.loads(history.read_text()) if history.exists() else []
    new=json.loads((folder/'views.json').read_text())
    for seed in (101,202):
        for name in ('hero','aisle','top_deck','tower','entry','ramp_turn','above'):
            before=Path('build/delivery-before')/str(seed)/(name+'.png');after=folder/str(seed)/(name+'.png')
            if not before.exists() or not after.exists():continue
            original=next(r for r in old if r['seed']==seed and r['name']==name)
            revised=next(r for r in new if r['seed']==seed and r['name']==name)
            for key in ('camera','target'):
                assert max(abs(x-y) for x,y in zip(original[key],revised[key]))<1e-5,(seed,name,key)
            assert original['lens_mm']==revised['lens_mm'],(seed,name,'lens')
            left,right=Image.open(before).convert('RGB'),Image.open(after).convert('RGB')
            # Preserve native baseline and revised images. Per-panel width
            # is bounded by the smaller source; never upscale a proof image.
            w=min(left.width,right.width);assert w>=800
            left=left.resize((w,round(left.height*w/left.width)),Image.Resampling.LANCZOS)
            right=right.resize((w,round(right.height*w/right.width)),Image.Resampling.LANCZOS)
            canvas=Image.new('RGB',(2*w,max(left.height,right.height)+44),(25,28,28));d=ImageDraw.Draw(canvas)
            font=ImageFont.truetype(find_font('DejaVu Sans','Book'),18)
            d.text((12,12),'Before / 950b6d2 checkpoint',font=font,fill=(230,227,215));d.text((w+12,12),'After / current baked export',font=font,fill=(230,227,215))
            canvas.paste(left,(0,44));canvas.paste(right,(w,44));path=out/f'{seed}-{name}.jpg';canvas.save(path,quality=94,optimize=True);rows.append([path])
    if rows:review_sheet(rows,out/'contact.jpg',title='Parking garage corrections / unchanged cameras')


def main():
    p=argparse.ArgumentParser();p.add_argument('--pass-name',default='final');a=p.parse_args();folder=Path('renders')/a.pass_name
    receipts=json.loads((folder/'views.json').read_text());rows=[]
    if a.pass_name=='final':
        names='hero above aisle tee_detail ramp_turn tower tower_landing tower_open entry top_deck scale eevee front side back top'.split()
        expected={(seed,name) for seed in (101,202) for name in names}|{(101,'plan_path')}
        assert {(r['seed'],r['name']) for r in receipts}==expected,'Incomplete final scene gallery'
        assert len(json.loads((folder/'module-views.json').read_text()))==25,'Incomplete module gallery'
    for r in receipts:verify_receipt(r)
    modules=folder/'module-views.json'
    if modules.exists():
        for r in json.loads(modules.read_text()):verify_receipt(r)
    for seed in (101,202):
        paths=[Path(r['output']) for r in receipts if r['seed']==seed]
        rows.extend([paths[i:i+3] for i in range(0,len(paths),3)])
    if (folder/'modules.png').exists():rows.append([folder/'modules.png'])
    for suffix in ('-matches','-source-matches'):
        pair=Path('renders')/(a.pass_name+suffix)
        if not pair.exists():continue
        for r in json.loads((pair/'views.json').read_text()):verify_receipt(r)
        rows.extend([[q] for q in sorted(pair.glob('*-pair.jpg'))])
    review_sheet(rows,folder/'contact.jpg',width=2400,title='Parking garages / current exported game surfaces')
    fixes(folder)
    print('CURRENT EXPORT REVIEW RECEIPTS PASS',len(receipts),folder,flush=True)


if __name__=='__main__':main()
