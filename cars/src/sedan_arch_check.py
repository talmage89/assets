"""Open stamped arch returns must clear the actual tires through both sweeps.

Open game sheets are intentionally omitted by the kit's solid-parity sweep.
Check their triangle crossings and vertices inside closed rubber explicitly.
"""
import argparse,json,sys,hashlib,math
from pathlib import Path
import bpy
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.motion import surface,inside
from sedan_surface_check import intersects


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);path=Path(a.source).resolve();bpy.ops.wm.open_mainfile(filepath=str(path));rows=[]
    for code in ['FL','FR','RL','RR']:
        flange=surface(bpy.data.objects['Arch flange_'+code]);tire=bpy.data.objects['Tire_'+code]
        axes=[('Wheel_'+code,'X',range(0,361,10))]
        if code.startswith('F'):axes.append(('Steer_'+code,'Z',range(-35,36)))
        for name,axis,angles in axes:
            node=bpy.data.objects[name];rest=node.matrix_basis.copy();violations=[];minimum=1.;samples=0
            for angle in angles:
                node.matrix_basis=rest@Matrix.Rotation(math.radians(angle),4,axis);bpy.context.view_layer.update();rubber=surface(tire);samples+=1
                crossings=[]
                for fi,ti in flange['tree'].overlap(rubber['tree']):
                    if intersects([flange['points'][i] for i in flange['faces'][fi]],[rubber['points'][i] for i in rubber['faces'][ti]]):crossings.append((fi,ti))
                enclosed=[list(q) for q in flange['points'] if all(rubber['lo'][k]<=q[k]<=rubber['hi'][k] for k in range(3)) and inside(rubber['tree'],q)]
                for current,other in [(flange,rubber),(rubber,flange)]:
                    for q in current['points']:minimum=min(minimum,other['tree'].find_nearest(q)[3])
                if crossings or enclosed:violations.append(dict(angle_degrees=angle,triangle_crossings=len(crossings),flange_vertices_inside_rubber=enclosed[:6]))
            node.matrix_basis=rest;bpy.context.view_layer.update()
            rows.append(dict(node=name,arch='Arch flange_'+code,samples=samples,minimum_sampled_vertex_to_surface_distance_m=minimum,violations=violations))
    report=dict(passed=all(not r['violations'] for r in rows),sweeps=rows,source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        scope='Actual open game arch triangles versus closed tire surfaces; exact edge/triangle intersections plus solid-parity containment; sampled distance is explicitly a vertex-to-surface measurement, not a claimed global minimum')
    Path(a.out).write_text(json.dumps(report,indent=2));print('S240_OPEN_ARCH_CLEARANCE',report['passed'],sum(r['samples'] for r in rows),'poses')
    if not report['passed']:raise SystemExit(1)
if __name__=='__main__':main()
