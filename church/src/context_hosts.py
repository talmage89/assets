"""Six distinct nearby storefronts from Downtown's native Building factory.

Fresh-process adapter writes only church/build. The original brick, trim,
roofing and sign maps stay read-only, and no complete block repeats in view.
"""
import json,os,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path[:0]=[str(ROOT/'downtown/src'),str(ROOT)]
import bpy
from plan import generate
from graphics import generate as signs
from geometry import palette
from building import Building
from kit.tiling import export


def main():
    out=ROOT/'church/build/hosts';out.mkdir(parents=True,exist_ok=True)
    os.chdir(ROOT/'downtown')
    for i in range(6):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        p=generate(419+i,'midwest')['lots'][i]
        stories=(2,2,1,2,3,2)[i];depth=(21.336,24.384,18.288,27.432,24.384,21.336)[i]
        p.update(id=f'ChurchNeighbor_{i}',index=i,width=(8.5344,9.144,10.668,8.2296,8.5344,9.144)[i],depth=depth,stories=stories,
                 floor_first=4.2672,upper=3.3528,roof=4.2672+(stories-1)*3.3528,
                 height=5.0292+(stories-1)*3.3528,parapet=.762,corner=None,chamfer=0,
                 tenant=('barber','pharmacy','hardware','antiques','diner','barber')[i],
                 awning=i in (1,3),storefront='iron' if i%2 else 'wood',transom='clear',
                 gallery=False,bay_window=False,fire_escape=i==4,neighbor_left=8.5,neighbor_right=8.9)
        sheet,layout=signs(out/f'signs-{i}');root,obs,doors=Building(p,palette(sheet),layout).build()
        root.location.y=depth/2
        bpy.context.view_layer.update();export(out/f'town-{i}.glb',[root,*root.children_recursive])
        (out/f'town-{i}.json').write_text(json.dumps(p,indent=2))


if __name__=='__main__':main()
