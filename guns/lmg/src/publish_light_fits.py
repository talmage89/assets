"""Publish fitted physical fixtures, preserving their linear radiance exactly.

Run from the asset folder with one or more fit JSON paths. This changes only
static procedural light recipes; it cannot read or alter asset textures.
"""
import argparse,json,pprint
from pathlib import Path
from light_fits import FITS
p=argparse.ArgumentParser();p.add_argument('fits',nargs='+');a=p.parse_args()
for path in a.fits:
 for name,row in json.loads(Path(path).read_text()).items():
  raw=row['color'];scale=max(raw);fit=dict(color=[v/scale for v in raw],world=0,lights=[])
  for i,(energy,basis) in enumerate(zip(row['energies'],row['bases'])):
   color=row.get('light_colors',[raw]*len(row['bases']))[i];gain=max(color);color=[v/gain for v in color]
   if basis.get('world'):
    fit['world']=energy*gain
    if row.get('light_colors'):fit['world_color']=color
   elif energy>1e-5:
    light=dict(basis,power=round(energy*gain,9))
    if row.get('light_colors'):light['color']=color
    fit['lights'].append(light)
  FITS[name]=fit
Path(__file__).with_name('light_fits.py').write_text('"""Physical studio-light fits, rerendered and audited on exported GLBs."""\nFITS='+pprint.pformat(FITS,sort_dicts=True,width=112)+'\n')
