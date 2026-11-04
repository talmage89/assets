"""Compare actual source positions/shading with an independently saved uncut parent.

Finite regional rays distinguish an already-dented parent from cut/reduction
loss. This measures correspondence only; the curvature maps judge the parent.
"""
import argparse,json,hashlib,sys,math
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from suv_fairness import field
from suv_measure import mesh_tree


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--parent',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.parent).resolve()));parent=field([o for o in bpy.data.objects if o.type=='MESH'])
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));obs=[o for o in bpy.data.objects if o.type=='MESH' and o.get('part_category') in ['body','doors','fascia','pillars'] and not any(k in o.name for k in ['applique','divider'])]
    skin=field(obs);geometric=mesh_tree(obs);regions={}
    definitions=[('hood_front_corner','Z',(.46,.78),(-2.18,-1.80)),('gate_surround','Y',(-.65,.65),(.73,1.08)),
                 ('rear_bumper_corner','X',(1.85,2.20),(.56,.96)),('d_pillar_base','X',(1.74,2.10),(1.10,1.35))]
    for name,axis,aa,bb in definitions:
        rows=[];excluded=0
        for u in np.linspace(*aa,25):
            for v in np.linspace(*bb,25):
                origin,direction=((u,v,3),(0,0,-1)) if axis=='Z' else ((u,3,v),(0,-1,0)) if axis=='Y' else ((2,u,v),(-1,0,0))
                src=skin(origin,direction);ref=parent(origin,direction)
                if src is None or ref is None:continue
                x,n,part=src;y,m,_=ref;hit,gn,_,_=geometric.ray_cast(Vector(origin),Vector(direction),5)
                if (x-y).length>.02 or n.dot(-Vector(direction))<.10:
                    excluded+=1;continue  # through an aperture or grazing a cut rim
                rows.append(dict(point_m=list(x),part=part,parent_chord_error_m=(x-y).length,shading_parent_degrees=math.degrees(n.angle(m)),facet_shading_degrees=math.degrees(n.angle(gn))))
        regions[name]=dict(samples=len(rows),aperture_or_grazing_exclusions=excluded,percentiles={key:np.percentile([r[key] for r in rows],[50,95,100]).tolist() for key in ['parent_chord_error_m','shading_parent_degrees','facet_shading_degrees']},rays=rows)
    Path(a.out).write_text(json.dumps(dict(source_sha256=hashlib.sha256(Path(a.source).read_bytes()).hexdigest(),parent_sha256=hashlib.sha256(Path(a.parent).read_bytes()).hexdigest(),regions=regions),indent=2))
    print('REGIONAL_PARENT_COMPARISON',json.dumps({k:{q:v for q,v in r.items() if q!='rays'} for k,r in regions.items()},indent=2))
if __name__=='__main__':main()
