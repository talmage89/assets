"""Contact sheets and provenance of the delivered look round; no docs JPGs."""
import hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),20)

def sheet(items,path,columns=3,width=1800,cell_height=300):
    cw=width//columns;rows=(len(items)+columns-1)//columns
    out=Image.new('RGB',(width,rows*cell_height),(160,160,158));d=ImageDraw.Draw(out)
    for i,(label,p) in enumerate(items):
        im=Image.open(p).convert('RGBA');im.thumbnail((cw-16,cell_height-42),Image.Resampling.LANCZOS)
        x=(i%columns)*cw;y=(i//columns)*cell_height
        bg=Image.new('RGBA',im.size,(160,160,158,255));bg.alpha_composite(im)
        out.paste(bg.convert('RGB'),(x+(cw-im.width)//2,y+32+(cell_height-42-im.height)//2))
        d.text((x+10,y+6),label,font=FONT,fill=(20,20,20))
    out.save(path,quality=94,optimize=True)

def main():
    root=BASE/'renders/final';digest=hashlib.sha256((BASE/'export/sxs.glb').read_bytes()).hexdigest()
    beauty=json.loads((root/'beauty/shots.json').read_text())
    for name,r in beauty.items():assert r['sha256']==digest and r['source'].endswith('.glb'),name
    items=[(name,root/'beauty'/(name+'.png')) for name in beauty]
    items += [('Eevee hero',root/'eevee/hero.png'),('Shell 512 subset',root/'shell/shell.png'),('Fired hull 512 subset',root/'hull/hull.png')]
    sheet(items,root/'contact-sheet.jpg')
    sheet([(n,root/'beauty'/(n+'.png')) for n in ('side','front','left','back','top')],root/'turnaround.jpg',columns=2,cell_height=380)
    pairs=sorted((root/'look-review').glob('*-pair.jpg'));sheet([(p.stem,p) for p in pairs],root/'finish-contact.jpg',columns=2,cell_height=500)
    wear=sorted((root/'wear').glob('*-on-off-pair.jpg'));sheet([(p.stem,p) for p in wear],root/'wear-contact.jpg',columns=2,cell_height=650)
    records={}
    for p in (BASE/'export').glob('*.glb'):records[str(p.relative_to(BASE))]=dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    for p in (BASE/'textures').glob('*.png'):records[str(p.relative_to(BASE))]=dict(bytes=p.stat().st_size,size=Image.open(p).size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    (root/'delivery.json').write_text(json.dumps(dict(files=records,model_sha256=digest,views=list(beauty),
        finish_acceptance=json.loads((root/'look-review/values.json').read_text()),wear=json.loads((root/'wear/measurements.json').read_text())),indent=2))
    print('FINAL',len(items),'views;',len(pairs),'finish pairs;',len(wear),'wear pairs;',root/'contact-sheet.jpg')
if __name__=='__main__':main()
