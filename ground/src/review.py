"""Three final docs JPGs and a complete contact sheet, with GLB provenance."""
import argparse,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.contact import contact,review_sheet
from kit.delivery_docs import jpg
from views import TITLE

p=argparse.ArgumentParser();p.add_argument('--final',action='store_true');a=p.parse_args()
folder=Path('renders/final');meta=json.loads((folder/'shots.json').read_text())
digest=hashlib.sha256(Path('export/GroundStreet.glb').read_bytes()).hexdigest()
names=['hero','dressed','streetside','block','repetition','curb','joint','ramp','drivecut','driveway','inlet','manhole','lawn','scale','front','side','back']
for n in names:
    row=meta[n];assert row['stage']=='final' and row['source_sha256']==digest and row['engine']=='CYCLES'
eevee=Path('renders/final-eevee/hero.png');assert json.loads((eevee.parent/'shots.json').read_text())['hero']['source_sha256']==digest
allshots=[folder/(n+'.png') for n in names]+[eevee]+[Path('renders/tiles')/('tile_'+n+'.png') for n in ('asphalt','concrete','lawn')]
contact(allshots,folder/'contact.jpg',width=2400,title=TITLE+' / exported GLBs / Eevee then 3x3 tiles')
review_sheet([[folder/'block.png',folder/'repetition.png'],[folder/'scale.png',folder/'dressed.png']],folder/'overview.jpg',width=2000,title='Assembly / honest lawn tiling / 1.8 m scale / library context')
review_sheet([[folder/'driveway.png',folder/'inlet.png'],[folder/'manhole.png',folder/'lawn.png']],folder/'details.jpg',width=2000,title='Exported apron and slab / cast inlet / 24 in cover / sod edge')
if a.final:
    for src,dst in [(folder/'dressed.png','hero.jpg'),(folder/'overview.jpg','overview.jpg'),(folder/'details.jpg','details.jpg')]:jpg(src,Path('docs')/dst)
print('Reviewed provenance; contact at renders/final/contact.jpg; three docs JPGs')
