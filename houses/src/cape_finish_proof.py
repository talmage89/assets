"""Measure delivered lap relief, independent of stored construction claims."""
import json,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from check_mesh import surface

rows=[]
for seed in (31,33,34,36):
    path=Path(f'build/cape/delivery/game-{seed}.blend');bpy.ops.wm.open_mainfile(filepath=str(path.resolve()))
    meta=json.loads(path.with_suffix('.json').read_text());m=meta['blocks'][0];skin=meta['spec']['siding']
    ob=next(o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('component')=='wall' and o.get('block')=='Main' and o.get('face')=='front')
    tree=surface([ob]);levels=sorted(set(round((ob.matrix_world@ob.data.vertices[p.vertices[0]].co).z,6) for p in ob.data.polygons if p.normal.z<-.999))
    differences=np.diff(levels);expected=.2794 if skin=='cement' else .1016;valid=differences[(differences>expected*.99)&(differences<expected*1.01)]
    assert len(valid)>2,(seed,levels)
    measured=[]
    for z in levels:
        if not m['floor']+.15<z<m['floor']+1.6:continue
        for fraction in (.08,.12,.2,.3,.5,.7,.9):
            x=m['x0']+(m['x1']-m['x0'])*fraction;eps=.0002
            hits=[tree.ray_cast(Vector((x,m['y0']-1,zz)),Vector((0,1,0)),2)[0] for zz in (z+eps,z+expected-eps)]
            if all(h is not None for h in hits):measured.append(dict(x_m=x,butt_z_m=z,raw_outward_difference_m=hits[1].y-hits[0].y,linear_extrapolated_projection_m=(hits[1].y-hits[0].y)/(1-2*eps/expected)))
    assert measured
    projection=float(np.median([r['linear_extrapolated_projection_m'] for r in measured]));target=.00437 if skin=='cement' else .014 if skin=='wood' else .0105
    assert abs(projection-target)<2e-5,(seed,projection,target)
    rows.append(dict(seed=seed,siding=skin,course_exposure_m=float(np.median(valid)),measured_projection_m=projection,samples=measured,scope='Ray intersections with actual delivered chart surfaces; course datums read from horizontal butt faces, not metadata'))
paint=[]
for seed in (35,36):
    path=Path(f'build/cape/delivery/game-{seed}.blend');bpy.ops.wm.open_mainfile(filepath=str(path.resolve()))
    support=surface([ob for ob in bpy.context.scene.objects if ob.type=='MESH' and ob.get('component')=='window'])
    values={}
    for name in ('Aged_GrayWoodAtSillNoses','Aged_LiftedPaint'):
        ob=bpy.data.objects[name];distances=[float(support.find_nearest(ob.matrix_world@v.co)[3]) for v in ob.data.vertices]
        values[name]=dict(vertices=len(distances),minimum_surface_gap_m=min(distances),maximum_surface_gap_m=max(distances))
    assert values['Aged_GrayWoodAtSillNoses']['maximum_surface_gap_m']<.0004,(seed,values)
    assert values['Aged_LiftedPaint']['maximum_surface_gap_m']<.0022,(seed,values)
    paint.append(dict(seed=seed,measured=values,scope='Actual nearest window/sill surfaces; bare patches stay on the weather surface, raised film clearance is intentional'))
Path('build/cape/delivery/construction.json').write_text(json.dumps(dict(passed=True,rows=rows,paint_support=paint),indent=2));print('CAPE_LAP_MEASUREMENTS',[(r['siding'],r['measured_projection_m']) for r in rows]);print('CAPE_PAINT_SUPPORT',paint)
