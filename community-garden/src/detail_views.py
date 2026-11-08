"""Readable plant close-ups and floor-safe orthographic inspections.

The canopy remains dense; wider framing exposes its cage below it. Only
plant details use fill. Orthographic sensor rays start above the floor.
Heroes and comparison cameras stay fixed.
"""
import argparse,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from render import render,views,bundle
from detail_camera import recipe
RECIPE=recipe()


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='renders/final');p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=96);p.add_argument('--seeds',nargs='+',type=int,default=[117,229,341]);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    for seed in a.seeds:
        plan=json.loads(Path(f'build/garden-{seed}.json').read_text())['plan'];fit=json.loads(Path('build/detail-cameras.json').read_text())[str(seed)]
        assert fit['recipe_sha256']==RECIPE and fit['bundle_sha256']==bundle(fit['source']),'Stale aisle-camera fit'
        v=dict(fit['camera'])
        folder=Path(a.out)/str(seed)
        render(seed,folder,a.width,a.samples,custom={'tomato':v},final=True)
        inspection={}
        for name in ('front','side','back'):
            shot=dict(views(plan)[name]);px,py,pz=shot['location']
            shot['location']=(px,py,max(pz,shot['ortho']/(2*shot['aspect'])+3))
            inspection[name]=shot
        render(seed,folder,a.width,a.samples,custom=inspection,with_context=False,final=True)
        for name in ('tomato','front','side','back'):
            receipt=folder/(name+'.json');r=json.loads(receipt.read_text());r['detail_recipe_sha256']=RECIPE;receipt.write_text(json.dumps(r,indent=2))

if __name__=='__main__':main()
