"""One combined source-only contact sheet and measured-value summary."""
import argparse,json,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import review_sheet
from PIL import Image

p=argparse.ArgumentParser();p.add_argument('--boxwood',type=Path,required=True);p.add_argument('--hydrangea',type=Path,required=True);p.add_argument('--out',type=Path,default=Path('renders/family-checkpoint'));a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
rows=[[a.boxwood/(name+'.png'),a.hydrangea/(name+'.png')] for name in ('three_quarter','side','close_1m','scale','base','shaded_side','structure')]
rows += [[a.boxwood/'match_green_velvet-pair.jpg',a.boxwood/'match_clipped-pair.jpg'],[a.hydrangea/'hyd_match_house-pair.jpg',a.hydrangea/'hyd_match_bed-pair.jpg']]
review_sheet(rows,a.out/'contact.jpg',width=1800,title='Boxwood (left) / Hydrangea (right) — SOURCE look-dev, before bake')
report={}
for species,folder,source in [('Boxwood',a.boxwood,Path('build/lookdev.blend')),('Hydrangea',a.hydrangea,Path('build/hydrangea/lookdev.blend'))]:
    meta=json.loads((folder/'shots.json').read_text());digest=hashlib.sha256(source.read_bytes()).hexdigest();assert len(meta)==9 and all(x['source_sha256']==digest for x in meta.values())
    for name in meta:
        if 'match_' in name:
            im=Image.open(folder/(name+'.png'));bb=im.getchannel('A').getbbox()
            assert bb and bb[0]>1 and bb[1]>1 and bb[2]<im.width-1 and bb[3]<im.height-1,(species,name,bb,im.size)
    report[species]=dict(source_sha256=digest,renders=len(meta),geometry=json.loads((source.parent/'botanical-check.json').read_text()),values=json.loads((folder/'measured-values.json').read_text()))
(a.out/'family-check.json').write_text(json.dumps(report,indent=2));print('Combined source evidence:',a.out/'contact.jpg')
