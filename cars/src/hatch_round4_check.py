"""Round-four measurements of actual game surfaces, with round-three controls.

Curvature measures positions, not custom normals. The crease angle measures the
interpolated shading field used in the gloss render. Neither accepts the look;
the maps, reflection stripes and photographic pairs supply that judgment.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from hatch_curvature_map import calibrate,measure as curvature,outer_faces
from hatch_fairness import field
from hatch_round3_check import measure as construction
from hatch_body import section_field


def section_normal(p):
    """Independent intended normal; never inherit a triangle's flipped shade."""
    gradient=[]
    for axis in range(3):
        a,b=p.copy(),p.copy();a[axis]+=.0002;b[axis]-=.0002
        gradient.append((section_field(a)-section_field(b))/.0004)
    return Vector(gradient).normalized()


def parent_orientation():
    """Build the uncut parent independently and test the diagnosed fold zones."""
    from hatch_body import master
    bpy.ops.wm.read_factory_settings(use_empty=True);parent,_=master(2)
    regions={'lamp_corner':dict(tested=0,suspect_faces=0,suspect_area_m2=0.,worst_degrees=0.),
             'cowl_corner':dict(tested=0,suspect_faces=0,suspect_area_m2=0.,worst_degrees=0.)}
    for f in parent.data.polygons:
        p=f.center
        region=('lamp_corner' if .50<abs(p.x)<.84 and -2.02<p.y<-1.70 and .68<p.z<.85 else
                'cowl_corner' if .70<abs(p.x)<.93 and -1.30<p.y<-1.08 and .8<p.z<1.0 else None)
        if region is None:continue
        r=regions[region];angle=math.degrees(f.normal.angle(section_normal(p)))
        r['tested']+=1;r['worst_degrees']=max(r['worst_degrees'],angle)
        if angle>75:r['suspect_faces']+=1;r['suspect_area_m2']+=f.area
    return dict(cage=json.loads(parent['cage_report']),regions=regions)


def measure(source,baseline=None,parent=False):
    reference=construction(baseline) if baseline else None
    current=construction(source)
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and outer_faces(o)]
    ray=field(obs);creases=[]
    for x in [0,.25,.45]:
        candidates=[]
        for i in range(61):
            z=.870+i*.001
            a,b=[ray((x,3,z+d),(0,-1,0)) for d in [-.015,.015]]
            if a and b and a[0].y>1.8 and b[0].y>1.8:candidates.append((math.degrees(a[1].angle(b[1])),z,a,b))
        angle,z,a,b=max(candidates,key=lambda q:q[0])
        creases.append(dict(x_m=x,center_z_m=z,vertical_width_m=.030,
            surface_chord_m=(a[0]-b[0]).length,normal_turn_degrees=angle,
            endpoints_m=[list(a[0]),list(b[0])]))
    maps={};folds=[];sampling={}
    for ob in obs:
        values,boundary,record=curvature(ob);maps[ob.name]=record
        sampling[ob.name]={k:ob[k] for k in ['retired_cut_boundary_points','retired_interior_samples','retile_probe_error_m','reflection_samples_added'] if k in ob}
        if ob.name!='Hood outer' and not ob.name.startswith('Front fender'):continue
        outer=outer_faces(ob);ob.data.calc_loop_triangles()
        for tri in ob.data.loop_triangles:
            if tri.polygon_index not in outer:continue
            ps=[ob.matrix_world@ob.data.vertices[i].co for i in tri.vertices]
            center=sum(ps,Vector())/3
            if not (-2.05<center.y<-1.08 and center.z>.70):continue
            n=(ps[1]-ps[0]).cross(ps[2]-ps[0]);area=n.length/2
            if area>1e-10 and n.dot(section_normal(center))<0:
                folds.append(dict(object=ob.name,area_m2=area,point_m=list(center)))
    errors=[]
    if folds:errors.append('Inverted hood/fender game triangles')
    if current['triangles']>46843:errors.append('Round-three form allocation exceeded')
    differences={}
    if reference:
        differences=dict(
            center_vertical_depth_mm=1000*(current['gate'][0]['concave_vertical_chord_depth_m']-reference['gate'][0]['concave_vertical_chord_depth_m']),
            quarter_vertical_depth_mm=1000*(current['gate'][1]['concave_vertical_chord_depth_m']-reference['gate'][1]['concave_vertical_chord_depth_m']),
            center_plan_depth_mm=1000*(current['gate_plan'][1]['center_recess_below_chord_m']-reference['gate_plan'][1]['center_recess_below_chord_m']))
        if any(abs(d)>3 for d in differences.values()):errors.append('Gate depth moved more than 3 mm from round three')
    validation=calibrate()
    parent_report=parent_orientation() if parent else None
    if parent_report and any(r['suspect_faces'] for r in parent_report['regions'].values()):errors.append('Parent hood/cowl fold')
    return dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        reference_sha256=reference['source_sha256'] if reference else None,
        analytic_curvature_calibration=validation,parent_orientation=parent_report,gate_crease=creases,
        gate=current['gate'],gate_plan=current['gate_plan'],gate_depth_change_mm=differences,
        inverted_hood_fender_triangles=folds,curvature=maps,sampling=sampling,
        triangles_per_category=current['triangles_per_category'],triangles=current['triangles'],
        reserved_detail_triangles=12500,finished_plan=current['triangles']+12500,
        accepted_plan=59343,passed=not errors,errors=errors)


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    p.add_argument('--baseline');p.add_argument('--diagnostic',action='store_true')
    p.add_argument('--parent',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    report=measure(Path(a.source),Path(a.baseline) if a.baseline else None,a.parent)
    Path(a.out).write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k not in ['curvature','gate','gate_plan']},indent=2))
    if report['errors'] and not a.diagnostic:raise AssertionError(report['errors'])


if __name__=='__main__':main()
