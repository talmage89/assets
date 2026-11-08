"""Eight unique Main Street rows from the unchanged downtown generator.

Run separately in a fresh Blender. All generated files live under river/build;
the native baked surfaces are read-only inputs. No other delivery is rebuilt.
"""
import os
import sys
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
sys.path[:0]=[str(REPO/'downtown/src'),str(REPO)]
import bpy
from build import build_block
from plan import generate,validate


def long_row(seed,region):
    # The native JSON-plan interface accepts longer validated frontages.
    # Combine two native parameter draws; its unchanged Building factory and
    # per-building budget checks still generate every part and door.
    p=generate(seed,region,12);p['lots']+=generate(seed+1000,region,8)['lots']
    cursor=0
    for i,lot in enumerate(p['lots']):
        # Wide three-storey corners can exceed the native 30k cap. Retain
        # their construction with a narrower, validated native frontage.
        lot['width']=min(lot['width'],9.144 if lot['stories']==3 else 10.9728)
        if lot['stories']==3:lot['depth']=min(lot['depth'],36.576);lot['y']=lot['depth']/2
        lot['bays']=max(2,round((lot['width']-.7)/1.95))
        lot.update(id=f'{region.title()}_{seed}_{i+1:02}',index=i,x=cursor+lot['width']/2,
                   corner='left' if i==0 else 'right' if i==19 else None)
        if lot['corner'] and lot['stories']==3:
            lot['stories']=2;lot['roof']=lot['floor_first']+lot['upper']
            lot['height']=lot['roof']+lot['parapet']
        lot['chamfer']=1.8 if lot['corner'] else 0;cursor+=lot['width']
    for i,lot in enumerate(p['lots']):
        lot['x']-=cursor/2
        lot['neighbor_left']=p['lots'][i-1]['height'] if i else None
        lot['neighbor_right']=p['lots'][i+1]['height'] if i<19 else None
    p.update(count=20,width=cursor);validate(p)
    path=Path('build')/f'river-row-{seed}.json';path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(p,indent=2)+'\n');return path


def main():
    out=(REPO/'river/build/town').resolve();out.mkdir(parents=True,exist_ok=True)
    (out/'textures').mkdir(exist_ok=True)
    link=out/'textures/ship'
    if not link.exists():link.symlink_to(os.path.relpath(REPO/'downtown/textures/ship',link.parent),target_is_directory=True)
    os.chdir(out)
    rows=[]
    regions=('midwest','northeast','western','midwest','western','midwest','northeast','western')
    for seed,region in zip(range(811,819),regions):
        row=build_block(seed,region,20,path=long_row(seed,region),context=True)
        block=Path('build/context/blocks')/(region+'-'+str(seed))/'block.json'
        rows.append(dict(seed=seed,block=str(block),buildings=row['buildings']))
    Path('manifest.json').write_text(json.dumps(rows,indent=2)+'\n')


if __name__=='__main__':main()
