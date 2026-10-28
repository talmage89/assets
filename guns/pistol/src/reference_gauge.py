"""C9 review: manual photographic wall-gauge picks, never a modeling input."""
from pathlib import Path
import sys
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.fonts import find_font
im=Image.open(BASE/'refs/round2-right.jpg').convert('RGB');d=ImageDraw.Draw(im)
f=ImageFont.truetype(find_font('Noto Sans','Regular'),13)
scale=(690-164)/174
for a,b,label in [((448,299),(448,318),'bottom 19 px'),((500,270),(521,270),'front 21 px')]:
 d.line([a,b],fill=(180,20,10),width=2)
 for x,y in (a,b):d.ellipse((x-2,y-2,x+2,y+2),fill=(180,20,10))
 d.text((b[0]+5,b[1]+5),label,font=f,fill=(180,20,10))
d.text((20,555),f'Slide: 526 px / 174 mm = {scale:.3f} px/mm. Bottom ~6.3 mm; front ~6.9 mm.',font=f,fill=(100,10,10))
d.text((20,575),'Pixel picks ±2 px (~0.7 mm); perspective / fillets prevent a wall-gauge claim.',font=f,fill=(100,10,10))
out=BASE/'renders/round3/reference-guard-gauge.jpg';out.parent.mkdir(parents=True,exist_ok=True)
im.save(out,quality=94,optimize=True)
