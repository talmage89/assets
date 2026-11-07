"""Actual triangle-plane sections through dense and game castings."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
import bpy
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
def segments(o,axis,station):
    o.data.calc_loop_triangles();points=[o.matrix_world@v.co for v in o.data.vertices];other=[k for k in range(3) if k!=axis];lines=[]
    for t in o.data.loop_triangles:
        vs=[points[q] for q in t.vertices];hits=[]
        for u,v in zip(vs,vs[1:]+vs[:1]):
            d,e=u[axis]-station,v[axis]-station
            if d*e<0:
                q=u.lerp(v,d/(d-e));hits.append([float(q[k]) for k in other])
        if len(hits)==2:lines.append(hits)
    return lines
rows=[]
for name,axis,stations in [('Front sculpted hanger',0,[-.045,0,.045]),('Front cast baseplate',0,[-.018,0,.018])]:
    game=bpy.data.objects[name];dense=bpy.data.objects[game['dense_source']]
    for station in stations:rows.append(dict(part=name,plane_axis='XYZ'[axis],station_m=station,dense=segments(dense,axis,station),game=segments(game,axis,station)))
Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(rows));print('Measured',len(rows),'dense/game casting cross-sections')
