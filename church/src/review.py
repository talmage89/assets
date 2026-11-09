"""Ignored contact sheets only; no final docs at the form checkpoint."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps


def sheet(paths,out,columns=3,width=480):
    if not paths:return
    height=round(width*2/3)+28;rows=(len(paths)+columns-1)//columns
    im=Image.new('RGB',(columns*width,rows*height),(231,232,226));draw=ImageDraw.Draw(im)
    for i,p in enumerate(paths):
        photo=Image.open(p).convert('RGB');photo.thumbnail((width-12,height-30))
        x=(i%columns)*width;y=(i//columns)*height
        im.paste(photo,(x+(width-photo.width)//2,y+24));draw.text((x+8,y+5),str(p.parent.name)+' / '+p.stem,fill=(22,28,23))
    out.parent.mkdir(parents=True,exist_ok=True);im.save(out,quality=91,optimize=True)


def main():
    for folder in ('checkpoint','modules','matches','source-matches','eevee','pass1','pass2','pass3'):
        root=Path('renders')/folder
        paths=sorted(root.rglob('*.png')) if 'matches' not in folder else sorted(root.glob('*-pair.jpg'))
        sheet(paths,root/'contact.jpg',4 if folder=='modules' else 3)
    print('Contact sheets rebuilt; checkpoint docs remain uncommitted')


if __name__=='__main__':main()
