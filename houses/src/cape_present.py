"""Ignored review contact sheets; source checkpoints never publish docs JPGs."""
from pathlib import Path
import json
from PIL import Image,ImageOps,ImageDraw,ImageFont
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
FONT=ImageFont.truetype(str(find_font('Noto Sans','Regular')),19)


def sheet(items,out,cols=2,cell=(700,450)):
    canvas=Image.new('RGB',(cols*cell[0],((len(items)+cols-1)//cols)*cell[1]),(234,235,232));d=ImageDraw.Draw(canvas)
    for i,(label,path) in enumerate(items):
        im=Image.open(path).convert('RGB');im.thumbnail((cell[0]-18,cell[1]-42),Image.Resampling.LANCZOS);x=i%cols*cell[0];y=i//cols*cell[1]
        canvas.paste(im,(x+(cell[0]-im.width)//2,y+35+(cell[1]-42-im.height)//2));d.text((x+12,y+7),label,font=FONT,fill=(24,36,31))
    out.parent.mkdir(parents=True,exist_ok=True);canvas.save(out,quality=93,optimize=True)


def main(root):
    sheet([(f'Seed {seed} / {view}',root/'seeds'/str(seed)/(view+'.png')) for seed in range(31,37) for view in ('front','rear')],root/'family.jpg',cell=(700,420))
    sheet([(name,root/(name+'.png')) for name in ('hero','back','roof','dormer','eave','entry','scale')]+[('Three types / same meter scale',root/'comparison/types.png')],root/'contact.jpg')
    pairs=Path('renders/cape/matches')
    if (pairs/'cape_plain-pair.jpg').exists():sheet([(name,pairs/(name+'-pair.jpg')) for name in ('cape_dormers','cape_plain')],pairs/'pairs.jpg',cols=1,cell=(1400,660))
    if root==Path('renders/cape/checkpoint'):
        from cape_view_check import check
        check()
    print('CAPE_CONTACT',root/'contact.jpg',root/'family.jpg')


def lookdev(root):
    sheet([(f'Seed {seed} / {view}',root/'seeds'/str(seed)/(view+'.png')) for seed in range(31,37) for view in ('front','rear')],root/'family.jpg',cell=(800,430))
    sheet([(name,root/(name+'.png')) for name in ('hero','back','roof','dormer','eave','entry','scale','foundation','peeling')]+[(f'{seed} / {view}',root/'seeds'/str(seed)/(view+'.png')) for seed in (32,35) for view in ('hero','connector')]+[('Three types / same scale',root/'comparison/types.png')],root/'contact.jpg',cell=(800,520))
    sheet([(f"{seed} / {kind}",root/'seeds'/str(seed)/'siding.png') for seed,kind in ((31,'vinyl'),(32,'stained cedar'),(33,'cement shingles'),(34,'aluminum'),(35,'painted clapboard, red'),(36,'painted clapboard, white'))]+[('Painted cedar / authored control',root/'painted_cedar/siding.png'),('Tired roof / north plane',root/'seeds/32/tired.png'),('Lifted paint / sill',root/'peeling.png')],root/'materials.jpg',cell=(800,620))
    pairs=Path('renders/cape/lookdev/values')
    names=('cedar','wood','roof','vinyl','aluminum','cement','concrete','trim','brick','glass')
    sheet([(name,pairs/(name+'-pair.jpg')) for name in names],pairs/'pairs.jpg',cols=2,cell=(800,460))

if __name__=='__main__':
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path('renders/cape/checkpoint')
    lookdev(root) if 'lookdev' in root.parts else main(root)
