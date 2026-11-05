"""Calibrated photo illumination/exposure on the current exported strip GLBs.

Camera exposure belongs to the photograph, separately from the presentation
hero. Maps, material albedos and geometry are never changed for a comparison.
"""
import hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import argparse
from kit.photo_match import verify
from strip_photo_matches import PAIR_SEEDS,LIGHTING
from strip_render import render
EXPOSURE=dict(period_lot=1.75,period_walk=.30)


def run(width=1600,samples=40):
    path=Path('build/strip/cameras.json');verify(path);cameras=json.loads(path.read_text());out=Path('renders/strip/matches')
    digest=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    for name in PAIR_SEEDS:
        cameras[name]['shot'].update(LIGHTING[name])
        if name in EXPOSURE:cameras[name]['shot']['exposure']=EXPOSURE[name]
    for seed in dict.fromkeys(PAIR_SEEDS.values()):
        chosen={name:cameras[name] for name,v in PAIR_SEEDS.items() if v==seed};render(seed,Path('build/strip-look'),out,list(chosen),width,samples,chosen)
        p=out/'provenance.json';rows=json.loads(p.read_text())
        for name in chosen:rows[name]['comparison']['lighting_recipe_sha256']=digest
        p.write_text(json.dumps(rows,indent=2)+'\n')

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--width',type=int,default=1600);a.add_argument('--samples',type=int,default=40);a=a.parse_args(sys.argv[sys.argv.index('--')+1:]);run(a.width,a.samples)
