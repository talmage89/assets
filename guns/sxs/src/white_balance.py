"""Linear neutral adaptation of review photos only; no asset-generation use."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageOps
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from look_matches import PHOTOS
from kit.image_io import srgb_to_linear,linear_to_srgb

def main():
 out=BASE/'build/look-photos';out.mkdir(parents=True,exist_ok=True);report={}
 for name,row in PHOTOS.items():
  im=ImageOps.exif_transpose(Image.open(BASE/'refs'/row['file'])).convert('RGB');box=row['neutral']
  if row.get('neutral_in_preview'):box=tuple(round(v*im.width/row['width']) for v in box)
  data=np.asarray(im,dtype=float)/255;x0,y0,x1,y1=box
  pixels=data[y0:y1,x0:x1].reshape(-1,3)
  valid=pixels[(pixels.max(axis=1)<.98)&(pixels.min(axis=1)>.04)]
  assert len(valid)>10,(name,'no valid neutral')
  patch=np.median(srgb_to_linear(valid),axis=0);gains=float(patch@np.array((.2126,.7152,.0722)))/patch
  balanced=np.clip(linear_to_srgb(srgb_to_linear(data)*gains),0,1)
  corrected=Image.fromarray(np.uint8(balanced*255+.5));corrected.save(out/(name+'-native.png'))
  annotated=im.copy();ImageDraw.Draw(annotated).rectangle(box,outline='red',width=6);annotated.thumbnail((1400,1400));annotated.save(out/(name+'-neutral.jpg'),quality=93)
  # The normalized view is for paired display and manually recorded masks.
  # Numeric statistics below inverse-map those masks to this balanced native.
  corrected.thumbnail((1707,10000)) if row['angle'] else None
  if row['angle']:corrected=corrected.rotate(row['angle'],resample=Image.Resampling.BICUBIC,expand=True,fillcolor=(170,170,170))
  transform_size=corrected.size
  corrected=corrected.resize((row['width'],round(corrected.height*row['width']/corrected.width)),Image.Resampling.LANCZOS)
  corrected.save(out/(name+'.png'))
  report[name]=dict(source=row['file'],native_size=im.size,neutral=row['neutral_name'],native_rectangle=box,
   native_linear_median=patch.tolist(),linear_rgb_gains=gains.tolist(),valid_neutral_pixels=len(valid),
   balanced_neutral_rgb=(linear_to_srgb(patch*gains)*255).tolist(),normalized_size=corrected.size,
   rotated_size=transform_size,rotation_degrees=row['angle'],
   limitation='Estimated photographic neutral and illumination; display values, not recovered albedo. Muzzle steel can reflect light color.' if name=='muzzle' else 'Uncalibrated studio light; gray paper is an estimated neutral, not a gray card.')
 (out/'white-balance.json').write_text(json.dumps(report,indent=2));print('WHITE BALANCE',report)
if __name__=='__main__':main()
