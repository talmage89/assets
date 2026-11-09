"""Full-resolution same-camera comparisons against the retained checkpoint."""
import hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
from kit.contact import contact


def main():
    before=Path('../build/civic-round3-before');after=Path('renders/final');out=Path('renders/last-fixes');out.mkdir(parents=True,exist_ok=True)
    rows=[];font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),23)
    for seed,names in [('101',('hero','above','entry','cornice','police')),('202',('hero','above','bays','interior','tower'))]:
        for name in names:
            old=before/'checkpoint'/seed/(name+'.png');new=after/seed/(('hero-fixed' if name=='hero' else name)+'.png')
            a,b=Image.open(old).convert('RGB'),Image.open(new).convert('RGB')
            oa=json.loads(old.with_suffix('.json').read_text());nb=json.loads(new.with_suffix('.json').read_text())
            assert a.size==b.size and a.width>=800,(old,new,'Native-size comparison required')
            assert oa['camera']==nb['camera'],(old,new,'Camera changed')
            archived=before/'review'/Path(oa['source']).name
            assert hashlib.sha256(archived.read_bytes()).hexdigest()==oa['source_sha256'],(old,'Historical export differs')
            im=Image.new('RGB',(a.width*2,a.height+56),(232,233,229));im.paste(a,(0,56));im.paste(b,(a.width,56))
            draw=ImageDraw.Draw(im);draw.text((18,16),seed+' / '+name+' / before b9c5290',font=font,fill=(30,35,31));draw.text((a.width+18,16),'final / same camera / light, age and lawns',font=font,fill=(30,35,31))
            path=out/(seed+'-'+name+'.jpg');im.save(path,quality=91,subsampling=0)
            rows.append(dict(pair=str(path),before=str(old),after=str(new),native_panel_width=a.width,camera=oa['camera'],historical_export_sha256=oa['source_sha256'],current_export_sha256=nb['source_sha256'],before_image_sha256=hashlib.sha256(old.read_bytes()).hexdigest(),after_image_sha256=hashlib.sha256(new.read_bytes()).hexdigest()))
    contact([r['pair'] for r in rows],out/'contact.jpg',width=2200,title='Civic / same-camera changes / each underlying panel is 1400px wide')
    (out/'receipts.json').write_text(json.dumps(dict(passed=True,pairs=rows,scope='Historical frames and exports retained locally; current script cannot regenerate the historical checkpoint'),indent=2)+'\n')
    print('CIVIC COMPARISONS',len(rows),'native same-camera pairs')


if __name__=='__main__':main()
