"""Measure actual checkpoint vertices and distances; no shipping claims."""
import argparse,json,sys,hashlib,math
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
import pickup_spec as S
from forms import side_x
from form_evidence import collect

def points(ob):return [ob.matrix_world@v.co for v in ob.data.vertices]
def box(obs):
    ps=[p for ob in obs for p in points(ob)]
    lo=[min(p[k] for p in ps) for k in range(3)];hi=[max(p[k] for p in ps) for k in range(3)]
    return dict(min=lo,max=hi,size=[b-a for a,b in zip(lo,hi)])
def edge_gap(a,b):
    ps=points(a);end=max(p.y for p in ps)
    selected=[p for p in ps if abs(p.y-end)<1e-6 and .62<p.z<1.30]
    bv=BVHTree.FromPolygons(points(b),[list(p.vertices) for p in b.data.polygons])
    ds=[bv.find_nearest(p)[3] for p in selected]
    return dict(samples=len(ds),min_m=min(ds),max_m=max(ds))

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve()
    bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.view_layer.update()
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o]
    total=0;categories={};parts={};roots={}
    for ob in obs:
        ob.data.calc_loop_triangles();n=len(ob.data.loop_triangles);total+=n;parts[ob.name]=n
        cat=ob['part_category'];categories[cat]=categories.get(cat,0)+n
        parent=ob.parent.name;roots[parent]=roots.get(parent,0)+n
    b=box([o for o in obs if not o.get('bounds_exclude')]);pivots={n:list(bpy.data.objects[n].matrix_world.translation) for n in ['Wheel_FL','Wheel_FR','Wheel_RL','Wheel_RR']}
    wb=abs(pivots['Wheel_FL'][1]-pivots['Wheel_RL'][1]);track=abs(pivots['Wheel_FL'][0]-pivots['Wheel_FR'][0])
    tires={n:box([bpy.data.objects[n]]) for n in ['Tire_FL','Tire_FR','Tire_RL','Tire_RR']}
    gaps={side:edge_gap(bpy.data.objects['Door skin_F'+side],bpy.data.objects['Door skin_R'+side]) for side in ['L','R']}
    arch=[]
    for side in ['L','R']:
        for end,axle in [('F',S.FRONT_AXLE),('R',S.REAR_AXLE)]:
            lip=bpy.data.objects['Arch return_'+end+side];tire=bpy.data.objects['Tire_'+end+side]
            z=max(p.z for p in points(lip));tz=max(p.z for p in points(tire))
            arch.append(dict(wheel=end+side,opening_top_m=z,tire_top_m=tz,vertical_gap_m=z-tz))
    floor=box([bpy.data.objects['Pickup bed floor']])
    cab=box([bpy.data.objects['Cab rear lower']]);bed=box([bpy.data.objects['Bed outer_L']])
    cab_gap=bed['min'][1]-cab['max'][1]
    # Independent slope check on broad ruled panels, after gauge/attachment.
    normal_errors=[]
    for name in ['Front fender_L','Front fender_R','Bed outer_L','Bed outer_R','Door skin_FL','Door skin_FR']:
        ob=bpy.data.objects[name];sign=1 if name.endswith('R') else -1
        for face in ob.data.polygons[:ob['outer_skin_faces']]:
            for li in face.loop_indices:
                p=ob.matrix_world@ob.data.vertices[ob.data.loops[li].vertex_index].co
                if not .85<p.z<1.20:continue
                dz=(side_x(p.y,p.z+1e-5)-side_x(p.y,p.z-1e-5))/2e-5
                dy=(side_x(p.y+1e-5,p.z)-side_x(p.y-1e-5,p.z))/2e-5
                expected=Vector((sign,-dy,-dz)).normalized()
                actual=ob.matrix_world.to_3x3()@ob.data.corner_normals[li].vector
                normal_errors.append(math.degrees(expected.angle(actual)))
    normal_check=dict(samples=len(normal_errors),max_angle_degrees=max(normal_errors))
    report=dict(surfacing=collect(),stage=bpy.context.scene['stage'],source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                broad_panel_normal_check=normal_check,bounds_m=b,triangles=total,triangles_per_category=categories,triangles_per_mesh=parts,triangles_per_parent=roots,
                materials=sorted({m.name for ob in obs for m in ob.data.materials if m}),
                wheel_centers_m=pivots,wheelbase_m=wb,track_m=track,tire_bounds_m=tires,door_seam_distances=gaps,
                arch_vertical_clearances=arch,bed_floor_bounds_m=floor,cab_bed_y_gap_m=cab_gap,
                pending=['continuous rolling tire deformation','all swept-motion clearance',
                         'UV, bake, GLB and delivery budgets','paint/glass/light material delivery'])
    errors=[]
    if total>60000:errors.append('Triangle budget')
    if normal_check['max_angle_degrees']>.1:errors.append('Broad panel shading normal disagrees with slope')
    if abs(wb-S.WHEELBASE)>1e-5 or abs(track-S.TRACK)>1e-5:errors.append('Wheelbase/track')
    if abs(b['size'][1]-S.LENGTH)>.002:errors.append('Length')
    if abs(b['size'][0]-S.WIDTH)>.002:errors.append('Body width')
    if abs(b['size'][2]-S.HEIGHT)>.002:errors.append('Height')
    if abs(floor['size'][1]-S.BED_LENGTH)>.0005:errors.append('Bed floor length')
    if abs(cab_gap-.016)>.0005:errors.append('Cab/bed gap')
    form=report['surfacing']
    for value in form['arches']:
        if not .030<=value['measured_flare_depth_above_crown_m']<=.040:errors.append('Broad flare depth')
        if value['measured_draw_height_above_opening_m']<.150:errors.append('Flare confined to lip')
        if value['squared_crown_ratio']<.72:errors.append('Arch crown insufficiently squared')
    if form['door_crown_above_820_1200_chord_m']<.004:errors.append('Side crown absent')
    if form['windshield_top_to_roof_surface_m']>.003:errors.append('Raised or detached windshield header')
    if not 6<=form['grille_face_rake_degrees']<=10:errors.append('Grille face rake')
    if any(value['sash_outboard_of_rail_m']<.0003 for value in form['roof_rail_to_sash_clearances']):
        errors.append('Roof rail coincides with or covers door sash at sampled sections')
    for value in gaps.values():
        if value['min_m']<.004 or value['max_m']>.0051:errors.append('Door seam gap')
    for value in tires.values():
        if abs(value['min'][2])>1e-5:errors.append('Tire ground contact')
    report.update(errors=errors,passed=not errors)
    Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ['triangles','bounds_m','wheelbase_m','track_m','door_seam_distances','cab_bed_y_gap_m','errors','passed']},indent=2))
    if errors:raise RuntimeError('Checkpoint form checks failed')
if __name__=='__main__':main()
