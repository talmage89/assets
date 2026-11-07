"""Full-resolution before/after pairs; no image alters an asset texture."""
from pathlib import Path
from PIL import Image,ImageDraw

def main():
    root=Path('renders/before-after');out=root/'pairs';out.mkdir(parents=True,exist_ok=True)
    for before in sorted((root/'before').glob('*/*.png')):
        rel=before.relative_to(root/'before');after=root/'after'/rel
        if not after.exists():continue
        a=Image.open(before).convert('RGB');b=Image.open(after).convert('RGB');assert a.size==b.size and a.width>=800
        im=Image.new('RGB',(a.width*2,a.height+30),(28,30,28));im.paste(a,(0,30));im.paste(b,(a.width,30));d=ImageDraw.Draw(im)
        d.text((12,8),f'{rel.parent}: archived checkpoint / BEFORE',fill='white');d.text((a.width+12,8),f'{rel.parent}: exported baked GLB / AFTER',fill='white')
        im.save(out/(rel.parent.name+'-'+rel.stem+'.jpg'),quality=94,optimize=True)

if __name__=='__main__':main()
