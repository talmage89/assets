"""Original molded name, rasterized only from the installed open Noto font."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from PIL import Image,ImageDraw,ImageFont,ImageFilter
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
im=Image.new('L',(1024,256),0);d=ImageDraw.Draw(im)
f=find_font('Noto Sans', 'Bold')
d.text((512,82),'RILL',font=ImageFont.truetype(f,146),anchor='mm',fill=255)
d.text((512,207),'C 4 8  /  O U T D O O R',font=ImageFont.truetype(f,32),anchor='mm',fill=255)
im.filter(ImageFilter.GaussianBlur(1.3)).save(out/'mold.png')
