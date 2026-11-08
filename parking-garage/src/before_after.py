"""Native-size comparison panels; never enlarge a source to meet the brief."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
from kit.contact import review_sheet


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pass-name',default='lookdev-checkpoint');a=ap.parse_args()
    dest=Path('renders/fixes');dest.mkdir(parents=True,exist_ok=True);records=[]
    aliases={'retained_hero':'hero','retained_aisle':'aisle'}
    oldrows={(r['seed'],aliases.get(r['name'],r['name'])):r for r in json.loads(Path('renders/before/checkpoint/views.json').read_text()) if 'seed' in r}
    oldrows.update({(r['seed'],r['name']):r for r in json.loads(Path('renders/before/open-lift/views.json').read_text())})
    newrows={(r['seed'],r['name']):r for r in json.loads(Path(f'renders/{a.pass_name}/views.json').read_text())}
    font=ImageFont.truetype(find_font('DejaVu Sans','Book'),20)
    for seed in (101,202):
        for shot in ('retained_hero','retained_aisle','tower','above','entry','ramp_turn','top_deck','tower_open'):
            original={'retained_hero':'hero','retained_aisle':'aisle'}.get(shot,shot)
            old=Path(f'renders/before/{"open-lift" if shot=="tower_open" else "checkpoint"}/{seed}/{original}.png');new=Path(f'renders/{a.pass_name}/{seed}/{shot}.png')
            before=Image.open(old).convert('RGB');after=Image.open(new).convert('RGB');width=min(before.width,after.width);assert width>=800
            bcam=oldrows[seed,original];acam=newrows[seed,shot]
            camera_error=sum((x-y)**2 for x,y in zip(bcam['camera'],acam['camera']))**.5
            assert camera_error<.00002 and bcam['lens_mm']==acam['lens_mm']
            # Identical sensor aspect for retained cameras and detail views.
            # Above baseline alone carries the old path overlay; final above
            # is clean and the separate plan_path view retains the route.
            height=round(width*before.height/before.width);assert abs(after.height/after.width-before.height/before.width)<.002
            pair=Image.new('RGB',(2*width,height+52),(29,32,30));d=ImageDraw.Draw(pair)
            for x,im,label in ((0,before,'Before / previous form checkpoint'),(width,after,'After / baked look-dev checkpoint')):
                pair.paste(im.resize((width,height),Image.Resampling.LANCZOS),(x,52));d.text((x+14,14),label,font=font,fill=(235,230,218))
            path=dest/f'{seed}-{shot}.jpg';pair.save(path,quality=95,optimize=True)
            records.append(dict(seed=seed,shot=shot,before=str(old),after=str(new),output=str(path),panel_width=width,camera_error_m=camera_error,lens_mm=acam['lens_mm']))
    review_sheet([[Path(r['output'])] for r in records],dest/'contact.jpg',width=2400,title='Fixed cameras / before and after / native-size panels')
    (dest/'views.json').write_text(json.dumps(records,indent=2)+'\n')


if __name__=='__main__':main()
