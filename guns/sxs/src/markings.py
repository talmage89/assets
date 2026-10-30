"""Original ammunition headstamp, rasterized from an installed open font."""
import json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.fonts import find_font

def main():
    out=BASE/'build/markings';out.mkdir(parents=True,exist_ok=True)
    font_path=find_font('Noto Sans','Regular');im=Image.new('L',(1024,1024));d=ImageDraw.Draw(im)
    font=ImageFont.truetype(font_path,130)
    d.text((512,250),'P D',font=font,anchor='mm',fill=255)
    d.text((512,774),'FIELD',font=ImageFont.truetype(font_path,100),anchor='mm',fill=255)
    for x in (245,779):d.text((x,518),'12',font=ImageFont.truetype(font_path,112),anchor='mm',fill=255)
    im.save(out/'headstamp.png')
    (out/'provenance.json').write_text(json.dumps(dict(text=['P D','FIELD','12'],font=Path(font_path).name,
        origin='Original fictional headstamp. Installed open font. No source photograph.'),indent=2))
if __name__=='__main__':main()
