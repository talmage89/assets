"""Kit photo pairs with explicit native-pixel error and EXIF lens provenance."""
import argparse,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit import photo_match
from kit.fonts import find_font

def main():
 p=argparse.ArgumentParser();p.add_argument('--calibration',default='build/cameras.json');p.add_argument('--renders',required=True);p.add_argument('--out',required=True)
 args=p.parse_args();photo_match.compose(args.calibration,args.renders,args.out)
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),18)
 for name,row in json.loads(Path(args.calibration).read_text()).items():
  path=Path(args.out)/(name+'-pair.jpg');im=Image.open(path).convert('RGB');draw=ImageDraw.Draw(im)
  draw.rectangle((0,im.height-56,im.width,im.height),fill=(238,239,236))
  lens=(f"EXIF equivalent {row['exif_35mm_focal_length']} mm; original padding uncertain" if 'exif_35mm_focal_length' in row
        else f"Estimated lens {row['shot']['lens']:.1f} mm")
  draw.text((18,im.height-42),f"{lens} | landmark RMS {row['residual_rms_pixels']:.1f} native px | comparison only",font=font,fill=(49,64,52))
  im.save(path,quality=94,optimize=True)

if __name__=='__main__':main()
