"""Supplement kit sweeps with the gas springs' actual constraint-driven poses.

The kit caches nominally fixed geometry. A body-mounted spring cylinder also
aims at the opening closure, so its surface must be rebuilt at every sample.
Rod/cylinder and ball/bracket joints are covered by travel/contact checks;
this supplementary sweep tests every non-hardware solid against the cylinders.
"""
import math
import bpy
from mathutils import Vector,Matrix
from kit.motion import surface,penetration


def sweep():
    others=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o
            and o.get('part_category')!='hinges' and not o.get('allow_boundary',False)]
    cache={};result=dict(passed=True,tolerance_m=.0005,step_degrees=1,motions=[],
        method='Evaluated coupled spring cylinders versus actual posed non-hardware solids; kit BVH/solid-parity penetration')
    for node,label in [('Hood','hood'),('Liftgate','gate')]:
        pivot=bpy.data.objects[node];rest=pivot.matrix_basis.copy();lo,hi=pivot['range_degrees'];violations={};maximum=0
        cases=[bpy.data.objects['H120 '+label+' support '+side+' telescoping sleeve'] for side in ['L','R']]
        for angle in range(round(lo),round(hi)+1):
            pivot.matrix_basis=rest@Matrix.Rotation(math.radians(angle),4,'X');bpy.context.view_layer.update()
            for casing in cases:
                current=surface(casing)
                for other in others:
                    ps=[other.matrix_world@Vector(q) for q in other.bound_box]
                    low=[min(p[k] for p in ps) for k in range(3)];high=[max(p[k] for p in ps) for k in range(3)]
                    if any(min(current['hi'][k],high[k])-max(current['lo'][k],low[k])<=.0005 for k in range(3)):continue
                    key=(other.name,tuple(round(q,8) for row in other.matrix_world for q in row))
                    if key not in cache:cache[key]=surface(other)
                    depth,crossings=penetration(current,cache[key],.0005);maximum=max(maximum,depth)
                    if depth>.0005:
                        pair=(casing.name,other.name)
                        if pair not in violations or depth>violations[pair]['depth_m']:
                            violations[pair]=dict(cylinder=casing.name,other=other.name,angle=angle,depth_m=depth,triangle_crossings=crossings)
        pivot.matrix_basis=rest;bpy.context.view_layer.update()
        row=dict(node=node,samples=round(hi-lo)+1,max_penetration_m=maximum,violations=list(violations.values()))
        result['motions'].append(row);result['passed'] &= not violations
        print('COUPLED_STRUT',node,maximum,'m',len(violations),'violations',flush=True)
    result['passed']=bool(result['passed']);return result
