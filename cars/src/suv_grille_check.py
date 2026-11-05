"""Measure the grille's actual blade, carrier and badge attachment surfaces.

Triangle crossings prove physical engagement at these joints; they do not
prove load capacity or manufacturing tolerances. No input dimensions stand in
for a query of the built mesh.
"""
import argparse, hashlib, json, sys
from pathlib import Path
import bpy

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from suv_exterior import tree_for


def inspect():
    badge=bpy.data.objects['Front badge land']
    stem=bpy.data.objects['Grille badge stem']
    rails=[o for o in bpy.context.scene.objects if o.name.startswith('Grille structural rail')]
    blades=[o for o in bpy.context.scene.objects if o.name.startswith('Alder chevron grille blade')]
    rail_tree=tree_for(rails);stem_tree=tree_for([stem])
    result=dict(badge_stem_triangle_crossings=len(tree_for([badge]).overlap(stem_tree)),
                stem_rail_triangle_crossings=len(stem_tree.overlap(rail_tree)),
                blade_rail_crossings={o.name:len(tree_for([o]).overlap(rail_tree)) for o in blades})
    result['passed']=(len(rails)==2 and len(blades)==16 and
                      result['badge_stem_triangle_crossings']>0 and
                      result['stem_rail_triangle_crossings']>0 and
                      all(result['blade_rail_crossings'].values()))
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source)
    bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));bpy.context.view_layer.update()
    result=inspect();result['source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    result['scope']='Actual triangle intersections at blade/carrier and badge/stem/carrier joints'
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2))
    print('SUV_GRILLE_SUPPORT',result['passed'],result)
    if not result['passed']:raise AssertionError(result)


if __name__=='__main__':main()
