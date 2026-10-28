"""Class photo calibration with the left image's own EXIF constraint."""
import json,sys
from pathlib import Path
from PIL import Image
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit import photo_match
from white_balance import build
corrections=build()
path=BASE/'build/cameras.json'
photo_match.solve(BASE/'src/photo_matches.py',path)
data=json.loads(path.read_text());row=data['left_photo']
for item in data.values():
 name=Path(item['photo']).name
 item['original_photo']=item['photo'];item['photo']=corrections[name]['output'];item['white_balance']=corrections[name]
exif=Image.open(BASE/'refs/PEO_M24_SWS-01.jpg').getexif()
assert exif.get(41989,exif.get_ifd(34665).get(41989))==105
row['lens_status']='105 mm equivalent from source EXIF; original padding is uncertain; pose fitted from action landmarks'
row['exif_35mm_focal_length']=105
path.write_text(json.dumps(data,indent=2))
