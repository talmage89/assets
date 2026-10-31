"""Measured R3 corner radii and die swells on the actual game sheet.

The three-point local radius is a finite-span circle estimate, not a constant
radius claim for the entire corner. The door comparison is at the same height.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
import sedan_spec as S
from sedan_check import mesh_tree


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve()
    bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.view_layer.update()
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('part_category') in ['body','doors','glass','pillars','fascia']]
    tree=mesh_tree(obs)
    def side(y,z):return tree.ray_cast(Vector((2,y,z)),Vector((-1,0,0)),4)[0]
    def end(x,z,front):return tree.ray_cast(Vector((x,-4 if front else 4,z)),Vector((0,1 if front else -1,0)),5)[0]
    report=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scope='Actual mesh rays; three-point local circle radius at x=800/850/880 mm')
    for front,z in [(True,.502),(False,.600)]:
        ps=[end(x,z,front) for x in [.80,.85,.88]]
        if any(p is None for p in ps):raise ValueError('Missing corner surface')
        aa,b,c=ps;area=(b-aa).cross(c-aa).length/2
        radius=(b-aa).length*(c-b).length*(aa-c).length/(4*area)
        report['front' if front else 'rear']=dict(plan_radius_m=radius,three_points_m=[list(p) for p in ps])
    report['fender_swell_m']={}
    for y,name in [(S.FRONT_AXLE,'front'),(S.REAR_AXLE,'rear')]:
        ps=[side(p,.760) for p in [0,y]]
        if any(p is None for p in ps):raise ValueError('Missing fender section')
        report['fender_swell_m'][name]=dict(outward_m=ps[1].x-ps[0].x,door_reference_m=list(ps[0]),fender_m=list(ps[1]))
    # A locator laid over paint would fail every center ray. Measure the
    # constructed opening directly, independently of the stored cut flags.
    openings={}
    for ob in bpy.context.scene.objects:
        if not ob.name.startswith(('Headlamp opening','Taillamp opening')):continue
        raw=list(ob['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
        nu,nv=ob['form_columns'],ob['form_rows'];lamp_tree=mesh_tree([ob]);samples=[]
        for i in [nu//3,nu//2,2*nu//3]:
            point=ps[(nv//2)*nu+i];_,normal,_,_=lamp_tree.find_nearest(point)
            hint=Vector((point.x,-.8 if ob.name.startswith('Headlamp') else .8,0))
            if normal.dot(hint)<0:normal.negate()
            hit,_,_,distance=tree.ray_cast(point+normal*.020,-normal,.035)
            samples.append(dict(point_m=list(point),outward_normal=list(normal),paint_hit_m=list(hit) if hit else None,paint_hit_distance_m=distance))
        openings[ob.name]=samples
    report['lamp_opening_rays']=dict(method='From 20 mm outside the actual backing, 35 mm inward; painted skin must be absent',samples=openings)
    errors=[]
    if len(openings)!=6:errors.append('Expected two front and four split rear lamp pieces')
    if not .250<=report['rear']['plan_radius_m']<=.400:errors.append('Rear corner radius')
    for name,row in report['fender_swell_m'].items():
        if not .020<=row['outward_m']<=.035:errors.append(name+' die swell')
    if any(s['paint_hit_m'] is not None for samples in openings.values() for s in samples):errors.append('Paint remains over a lamp opening')
    report.update(passed=not errors,errors=errors)
    Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
    if errors:raise AssertionError(errors)
if __name__=='__main__':main()
