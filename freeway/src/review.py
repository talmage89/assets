"""Contact sheets and a measured checkpoint summary; no committed docs."""
import json,sys,math,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from external import bundle

def sheet(files,out,cols=3,width=480):
    rows=math.ceil(len(files)/cols);heights=[round(width*.68)+30]*rows
    if cols==1:
        heights=[round((width-12)*Image.open(p).height/Image.open(p).width)+40 for p in files]
    im=Image.new('RGB',(width*cols,sum(heights)),(31,36,33));d=ImageDraw.Draw(im);font=ImageFont.truetype(find_font('DejaVu Sans','Book'),15)
    for i,path in enumerate(files):
        row=i//cols;h=heights[row]
        image=Image.open(path).convert('RGB');image.thumbnail((width-12,h-40));x=(i%cols)*width+6;y=sum(heights[:row])+6
        im.paste(image,(x+(width-12-image.width)//2,y));d.text((x,y+h-32),str(path.relative_to(Path('renders'))).replace('.png',''),font=font,fill=(228,235,222))
    Path(out).parent.mkdir(parents=True,exist_ok=True);im.save(out,quality=91,optimize=True)

def main():
    files=[*sorted(Path('renders/lookdev/101').glob('*.png')),*sorted(Path('renders/lookdev/202').glob('*.png'))]
    files += [p for p in (Path('renders/lookdev/modules.png'),Path('renders/lookdev/scale.png')) if p.exists()]
    assert len(files)>=16,('Incomplete checkpoint views',len(files))
    for path in files:
        record=json.loads(path.with_suffix('.json').read_text());assert record['engine']=='CYCLES',path
        assert record['bundle_sha256']==bundle(record['source']),('Stale render',path)
        if record.get('recipe_sha256'):assert record['recipe_sha256']==hashlib.sha256(Path('src/render.py').read_bytes()).hexdigest(),('Stale render recipe',path)
        if record.get('frame_sha256'):assert record['frame_sha256']==hashlib.sha256(path.read_bytes()).hexdigest(),('Changed render pixels',path)
        for ctx in record.get('context',[]):assert ctx['bundle_sha256']==bundle(ctx['source']),('Stale context',path)
    sheet(files,'renders/lookdev/contact.jpg')
    pairs=sorted(Path('renders/look-matches').glob('*-pair.jpg'));assert len(pairs)>=3
    sheet(pairs,'renders/look-matches/contact.jpg',cols=1,width=1400)
    measurements=json.loads(Path('build/check.json').read_text())
    tone={}
    import numpy as np
    for seed in (101,202):
        a=np.asarray(Image.open(f'renders/lookdev/{seed}/hero.png').convert('RGB'),float)/255;y=a@np.array([.2126,.7152,.0722])
        tone[str(seed)]=dict(display_luma_p01_p50_p99=np.quantile(y,[.01,.5,.99]).tolist(),rgb_clipped_fraction=float((a>=.99).mean()),scope='Whole image includes sky; display-value range, not albedo measurement')
    Path('build/tones-overall.json').write_text(json.dumps(tone,indent=2))
    print('REVIEW',len(files),'Cycles views,',len(pairs),'period pairs; contact sheets written')
if __name__=='__main__':main()
