"""Standalone checkpoint views, all loaded from their inspection GLBs."""
import sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path[:0]=[str(ROOT),str(BASE/'src')]
from guns.common.render import main
import shots,interface
for name in ('box_loaded','box_empty','cartridge','case','link'):
 sys.argv=['render_extra.py','--','--source',str(BASE/'build'/f'{name}.glb'),
  '--out',str(BASE/'renders/checkpoint/detachables'/name),'--shots',name,'--width','900','--samples','32']
 main(shots,interface)

sys.argv=['render_extra.py','--','--source',str(BASE/'build/lmg.glb'),'--out',str(BASE/'renders/checkpoint/belt-advance'),
 '--shots',','.join(f'belt_advance_{i:02d}' for i in range(7)),'--width','700','--samples','32']
main(shots,interface)
from PIL import Image,ImageDraw
frames=[Image.open(BASE/'renders/checkpoint/belt-advance'/f'belt_advance_{i:02d}.png').convert('RGB') for i in range(7)]
sheet=Image.new('RGB',(700*4,550*2),(230,233,229));draw=ImageDraw.Draw(sheet)
for i,(im,f) in enumerate(zip(frames,(0,3,5,6,7,8,12))):
 x=i%4*700;y=i//4*550;sheet.paste(im,(x,y+32));draw.text((x+10,y+8),f'Fire / frame {f} / {f/60:.3f} s',fill=(20,35,25))
sheet.save(BASE/'renders/checkpoint/belt-advance.jpg',quality=94)
