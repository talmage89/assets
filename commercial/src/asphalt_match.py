"""Supplemental used-asphalt/concrete pair, with its own camera calibration.

Four picked column stations constrain framing; the original plan is not copied.
The sun is estimated from the tree and column shadows, never a surveyed value.
"""
import sys,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from plan import generate
p=generate(101);c=p['canopy'];coly=c['center'][1]+.92-c['column']/2
scale=3888/1920 # Picks were made on a 1920px inspection view; native pixels below.
landmarks=[]
for x,top,base in [(-c['pitch'],(470,636),(443,968)),(0,(675,595),(657,982))]:
 for z,pixel,label in ((c['clear'],top,'soffit'),(.20,base,'island')):
  landmarks.append(dict(world=(x,coly,z),pixel=tuple(v*scale for v in pixel),label='column / '+label))
MATCHES={'used_asphalt':dict(title='Virginia 2009 / used asphalt, concrete boundary and deposits',photo='build/va-store-neutral.png',crop=tuple(round(v*scale) for v in (200,935,1900,1280)),
 location=(18,-20,1.7),target=(0,coly,2.5),lens=35,lens_bounds_mm=(24,60),camera_height_m=(1.65,.20),background='transparent',exposure=-.15,landmarks=landmarks)}
# Long winter column/tree shadows: approximately 37 degrees, not the high PA sun.
LIGHT=dict(sky_strength=.16,sky_saturation=.28,neutral_ambient=0,sun_direction=(-1.15,.7,-1),sun_energy=3.8,exposure=-.15)

if __name__=='__main__':
 import argparse
 from kit.photo_match import verify
 from render import render
 a=argparse.ArgumentParser();a.add_argument('--width',type=int,default=1600);a.add_argument('--samples',type=int,default=48);a=a.parse_args(sys.argv[sys.argv.index('--')+1:])
 calibration=Path('build/asphalt-cameras.json');verify(calibration)
 row=json.loads(calibration.read_text())['used_asphalt'];row['shot'].update(LIGHT)
 camera=Path('build/camera-used_asphalt.json');camera.write_text(json.dumps({'used_asphalt':row}))
 folder=Path('renders/look-matches')
 render(Path('export/CommercialGas-101.gltf'),folder,['used_asphalt'],a.width,a.samples,camera)
 provenance=folder/'provenance.json';rows=json.loads(provenance.read_text())
 rows['used_asphalt']['comparison_recipe_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
 provenance.write_text(json.dumps(rows,indent=2))
