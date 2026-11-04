"""Actual S240 construction measurements, distinct from serialization/sweeps."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from sedan_check import points,bounds
import sedan_spec as S


def mechanical_measurements():
    """Dimensions read from actual hinge/wheel surfaces, not spec constants."""
    from sedan_check import mesh_tree
    from kit.motion import inside
    hinges={};wheels={}
    def radial(p,c,a):return ((p-c)-a*(p-c).dot(a)).length
    for code in ['FL','FR','RL','RR']:
        parent=bpy.data.objects['Door_'+code];axis=Vector(parent['hinge_axis_vehicle']).normalized();origin=parent.matrix_world.translation
        for label in ['lower','upper']:
            name=code+' '+label;pin=bpy.data.objects['S240 hinge pin '+name];sleeve=bpy.data.objects['S240 hinge sleeve '+name]
            c=sleeve.matrix_world.translation;pin_points=points(pin);sleeve_points=points(sleeve)
            arr=np.array([list(p) for p in pin_points]);_,eigen=np.linalg.eigh(np.cov(arr.T));pin_axis=Vector(eigen[:,-1]).normalized()
            pr=max(radial(p,c,axis) for p in pin_points);rs=[radial(p,c,axis) for p in sleeve_points];minimum=min(rs)
            bore=[]
            for edge in sleeve.data.edges:
                a,d=[sleeve_points[i] for i in edge.vertices]
                if max(radial(a,c,axis),radial(d,c,axis))>minimum+1e-5:continue
                av=(a-c)-axis*(a-c).dot(axis);dv=(d-a)-axis*(d-a).dot(axis)
                t=max(0,min(1,-av.dot(dv)/max(dv.length_squared,1e-15)))
                bore.append((av+t*dv).length)
            leaf=bpy.data.objects['S240 hinge moving leaf '+name];ps=points(leaf);anchor=(ps[0]+ps[len(ps)//2])*.5
            tree=mesh_tree([sleeve]);tip=max(ps,key=lambda p:abs(p.x) if p.y>max(q.y for q in ps)-1e-5 else -10)
            door=mesh_tree([bpy.data.objects['Door '+code[0]+'_'+code[1]]]);distance=door.find_nearest(tip)[3]
            fixed=bpy.data.objects['S240 hinge fixed leaf '+name];pin_tree=mesh_tree([pin])
            hinges[name]=dict(pin_diameter_m=2*pr,minimum_bore_diameter_m=2*min(bore),radial_running_clearance_m=min(bore)-pr,
                barrel_axis_offset_m=radial(c,origin,axis),pin_axis_dot=abs(pin_axis.dot(axis)),
                moving_leaf_anchor_inside_barrel=inside(tree,anchor),moving_leaf_skin_tip_distance_m=distance,
                fixed_leaf_contacts_pin=any(inside(pin_tree,p) for p in points(fixed)))
        spin=bpy.data.objects['Wheel_'+code];hub=spin.matrix_world.translation;sign=-1 if code.endswith('L') else 1
        barrel=points(bpy.data.objects['Wheel barrel_'+code]);tire=points(bpy.data.objects['Tire_'+code]);cap=points(bpy.data.objects['Alder center cap_'+code])
        bead_radius=min(math.hypot(p.y-hub.y,p.z-hub.z) for p in tire)
        beads=[p for p in tire if abs(math.hypot(p.y-hub.y,p.z-hub.z)-bead_radius)<1e-5]
        studs=[o for o in bpy.context.scene.objects if o.name.startswith('S240 wheel stud '+code)]
        circles=[]
        for ob in studs:
            ps=points(ob);cy=sum(p.y for p in ps)/len(ps);cz=sum(p.z for p in ps)/len(ps);circles.append(2*math.hypot(cy-hub.y,cz-hub.z))
        wheels[code]=dict(rim_mesh_width_m=max(p.x for p in barrel)-min(p.x for p in barrel),tire_bead_width_m=max(p.x for p in beads)-min(p.x for p in beads),
            cap_recess_from_outer_lip_m=max(sign*(p.x-hub.x) for p in barrel)-max(sign*(p.x-hub.x) for p in cap),stud_count=len(studs),measured_pitch_circle_diameters_m=circles)
    return dict(hinges=hinges,wheels=wheels)


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve();bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.view_layer.update()
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')=='Sedan']
    counts={};parents={};categories={};rest_errors=[]
    for o in obs:
        o.data.calc_loop_triangles();num=len(o.data.loop_triangles);counts[o.name]=num
        parents[o.parent.name]=parents.get(o.parent.name,0)+num;cat=o['part_category'];categories[cat]=categories.get(cat,0)+num
        attr=o.data.attributes.get('VehicleRest')
        if attr is None:rest_errors.append((o.name,'missing'));continue
        error=max((d.vector-o.matrix_world@v.co).length for d,v in zip(attr.data,o.data.vertices))
        if error>1e-5:rest_errors.append((o.name,error))
    under=[o for o in obs if o.get('part_category')=='underbody']
    underbody_lowest=min(((p.z,o.name,list(p)) for o in under for p in points(o)),key=lambda r:r[0])
    wheel_center=bpy.data.objects['Wheel_RL'].matrix_world.translation
    measured_radius=max(math.hypot(p.y-wheel_center.y,p.z-wheel_center.z) for p in points(bpy.data.objects['Tire_RL']))
    departure=[]
    for o in obs:
        if o.get('part_category') in ['tires','wheels','brakes']:continue
        for point in points(o):
            dy=point.y-wheel_center.y;dz=point.z-wheel_center.z;r=math.hypot(dy,dz)
            if dy<=.03 or r<measured_radius:continue
            angle=math.degrees(math.atan2(dz,dy)+math.asin(measured_radius/r))
            if 0<angle<85:departure.append((angle,o.name,list(point)))
    tangent=min(departure)
    optics={}
    for o in obs:
        if not o.name.startswith(('Headlamp opening','Taillamp opening')):continue
        count=o.get('lens_outer_faces',0);dots=[];edges=[]
        for face in o.data.polygons:
            if face.index>=count:continue
            for li in face.loop_indices:dots.append(float(face.normal.dot(o.data.corner_normals[li].vector)))
            vs=[o.matrix_world@o.data.vertices[i].co for i in face.vertices]
            edges.extend((p-q).length for p,q in zip(vs,vs[1:]+vs[:1]))
        optics[o.name]=dict(outer_faces=count,normal_dot_min_p01_p50=np.percentile(dots,[0,1,50]).tolist(),maximum_outer_edge_m=max(edges))
    pivots={}
    for name in ['Door_FL','Door_FR','Door_RL','Door_RR','Hood','Trunk','Wheel_FL','Wheel_FR','Wheel_RL','Wheel_RR','Steer_FL','Steer_FR']:
        o=bpy.data.objects[name];pivots[name]=dict(position_m=list(o.matrix_world.translation),local_axis=o.get('pivot_axis'),range_degrees=list(o.get('range_degrees',[])),world_axis=list(Vector(o['hinge_axis_vehicle']).normalized() if 'hinge_axis_vehicle' in o else (o.matrix_world.to_3x3()@Vector(tuple(1 if c==o['pivot_axis'] else 0 for c in 'XYZ'))).normalized()))
    # Measure telescoping overlap and actual axes throughout the hood range.
    from kit.motion import surface,penetration,owned
    hood=bpy.data.objects['Hood'];rest=hood.matrix_basis.copy();struts=[]
    members=[o for o in obs if o.name.startswith('S240 telescoping ')]
    others=[o for o in obs if o not in members and not o.get('allow_boundary')]
    stationary={o.name:surface(o) for o in others if not owned(o,hood)}
    support_contacts=[];support_maximum=0.0

    for angle in range(-62,1,2):
        hood.matrix_basis=rest@Matrix.Rotation(math.radians(angle),4,'X');bpy.context.view_layer.update()
        dynamic={o.name:surface(o) for o in others if owned(o,hood)}
        evaluated_members={o.name:surface(o) for o in members}
        for member in members:
            current=evaluated_members[member.name];side=member.name[-1]
            for other in others:
                # The actual end bearing is attached to its supporting sheet.
                if other.name in ['S240 hood strut upper bracket '+side,'S240 hood strut lower bracket '+side,'S240 steel firewall']:continue
                depth,crossings=penetration(current,dynamic.get(other.name) or stationary.get(other.name),.0005)
                support_maximum=max(support_maximum,depth)
                if depth>.0005:support_contacts.append(dict(angle=angle,member=member.name,other=other.name,depth_m=depth,crossings=crossings))
        for side in ['L','R']:
            pair=[evaluated_members['S240 telescoping '+label+' '+side] for label in ['sleeve','rod']]
            depth,crossings=penetration(*pair,.0005);support_maximum=max(support_maximum,depth)
            if depth>.0005:support_contacts.append(dict(angle=angle,member='rod '+side,other='hollow sleeve '+side,depth_m=depth,crossings=crossings))
            sleeve=bpy.data.objects['S240 hood strut sleeve '+side];rod=bpy.data.objects['S240 hood strut rod '+side]
            lower=sleeve.matrix_world.translation;upper=rod.matrix_world.translation;direction=(upper-lower).normalized();distance=(upper-lower).length
            lengths=[]
            for frame,label in [(sleeve,'sleeve'),(rod,'rod')]:
                ob=bpy.data.objects['S240 telescoping '+label+' '+side];axis=frame.matrix_world.to_3x3()@Vector((0,0,1));projections=[(p-frame.matrix_world.translation).dot(axis) for p in points(ob)]
                lengths.append(max(projections)-min(projections))
            struts.append(dict(angle=angle,side=side,pin_distance_m=distance,measured_member_lengths_m=lengths,overlap_m=sum(lengths)-distance,
                sleeve_alignment=float((sleeve.matrix_world.to_3x3()@Vector((0,0,1))).normalized().dot(direction)),rod_alignment=float((rod.matrix_world.to_3x3()@Vector((0,0,1))).normalized().dot(-direction))))
    hood.matrix_basis=rest;bpy.context.view_layer.update()
    mechanical=mechanical_measurements()
    errors=[]
    if any(r["radial_running_clearance_m"]<.00018 or r["barrel_axis_offset_m"]>1e-5 or r["pin_axis_dot"]<.9999 or not r["moving_leaf_anchor_inside_barrel"] or r["moving_leaf_skin_tip_distance_m"]>.0015 or not r["fixed_leaf_contacts_pin"] for r in mechanical["hinges"].values()):errors.append("Door hinge running clearance or attachment")
    if support_contacts:errors.append('Evaluated telescoping support collision')
    if rest_errors:errors.append('Rest coordinates disagree with actual closed geometry')
    if sum(counts.values())>60000:errors.append('Triangle budget')
    if not .140<=underbody_lowest[0]<=.155:errors.append('Underbody clearance')
    if tangent[0]<17.5:errors.append('Departure ground tangent below the manufacturer class cross-check')
    if any(v['normal_dot_min_p01_p50'][0]<0 for v in optics.values()):errors.append('Reversed cover shading normals')
    if any(v['maximum_outer_edge_m']>.056 for v in optics.values()):errors.append('Long optical cover chord')
    if any(not .025<r['overlap_m']<min(r['measured_member_lengths_m']) or min(r['sleeve_alignment'],r['rod_alignment'])<.999 for r in struts):errors.append('Hood strut stroke or alignment')
    report=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scope='Measured source construction; motion collision and GLB serialization are separate checks',triangles=sum(counts.values()),triangles_per_mesh=counts,triangles_per_parent=parents,triangles_per_category=categories,
        full_bounds_m=bounds(obs),underbody_lowest=underbody_lowest,measured_rear_tire_radius_m=measured_radius,
        departure_tangent_degrees=tangent[0],departure_limiting_mesh=tangent[1],departure_contact_m=tangent[2],departure_method='Ground plane tangent to the actual mean tire radius and each rear overhang vertex; minimum positive angle. Later-generation Accord reference: 17.5 degrees.',
        mechanical_construction=mechanical,rest_attribute_errors=rest_errors,optical_covers=optics,pivots=pivots,hood_strut_samples=struts,evaluated_support_sweep=dict(samples=32,step_degrees=2,maximum_penetration_m=support_maximum,violations=support_contacts,intended_contacts='Upper/lower anchor brackets and steel firewall at the support bearing; all members evaluated in every hood pose, including the hollow rod/sleeve pair'),passed=not errors,errors=errors)
    Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ['triangles','underbody_lowest','departure_tangent_degrees','departure_limiting_mesh','optical_covers','errors']},indent=2))
    if errors:raise AssertionError(errors)
if __name__=='__main__':main()
