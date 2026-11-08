"""Rebuild only the mold in a saved source while retaining the accepted body."""
import argparse,sys
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from build import Bus,finish_scene
from front import sculpt

class Front:
    add=Bus.add;box=Bus.box;tube=Bus.tube
    def __init__(self):
        self.root=bpy.data.objects['SchoolBus'];self.seed=101;self.high=False;self.detail=True
        self.m={k:bpy.data.materials['Bus '+v] for k,v in {
            'yellow':'yellow','black':'black','frame':'frame','aluminum':'aluminum',
            'headlight':'headlight','windshield':'windshield','amber':'amber'}.items()}

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
    prefixes=('Compound hood','Dense front mold','Seated grille','Grille radiator','Recessed grille',
              'Grille vertical','Headlamp closed','Headlamp silver','Lamp front lowbeam',
              'Glass sealed headlamp','Bonded headlamp','Front amber','Hood cowl','Hood rubber')
    for ob in list(bpy.context.scene.objects):
        if ob.type=='MESH' and ob.name.startswith(prefixes):bpy.data.objects.remove(ob,do_unlink=True)
    b=Front();sculpt(b);finish_scene(b,a.out)

if __name__=='__main__':main()
