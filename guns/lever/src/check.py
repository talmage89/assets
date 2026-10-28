"""Independent actual-surface construction and sampled-motion checkpoint."""
import argparse
import json
import math
import sys
from pathlib import Path
import bpy
import bmesh
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import motion, assembly, weapon as W, model as M
from guns.common.interface_checks import scene_frame
from guns.common.interface_v1_5 import manifest
import interface
import form_audit


def parts():return [o for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o and not o.get('check_proxy')]
def part(name):return bpy.data.objects[name]
def surface(name):return motion.surface(part(name))


def contacts(arm):
    rows=[]
    def contact(a,b,limit,label):
        gap,method=assembly.distance(part(a),part(b))
        rows.append(dict(kind=label,parts=[a,b],distance_m=gap,limit_m=limit,method=method,passed=gap<=limit))
    W.pose(arm,'Idle',0)
    for a,b,limit,label in [
        ('Bolt_Body','Barrel',.00015,'bolt face closed on barrel breech'),
        ('Locking_Block','Lock_Seat',.00015,'locking block raised against receiver seat'),
        ('Locking_Block','Bolt_LockAbutment',.00015,'locking block opposed bolt abutment'),
        ('Stock_TangScrew','Upper_Tang',.00015,'stock retention screw seated on upper tang'),
        ('Lever_LatchLand','Tang_LatchSeat',.00015,'lever latched against lower tang'),
        ('Hammer_SearLand','Sear_Nose',.00015,'full cock hammer supported at sear land'),
    ]:contact(a,b,limit,label)
    contact('Locking_Block','Lock_Seat.001',.00015,'opposite locking-block seat')
    contact('Locking_Block','Bolt_LockAbutment.001',.00015,'opposite bolt abutment')
    for a,b,label in [('Rear_Dovetail','Barrel','rear dovetail in barrel seat'),
                      ('Rear_SpringLeaf','Rear_Dovetail','spring leaf supported at dovetail'),
                      ('Rear_SpringLeaf','Rear_Elevator','elevation wedge supports leaf'),
                      ('Front_Ramp','Barrel','front sight saddle on barrel'),
                      ('Forend_Band','Forend','forend band bears on wood'),
                      ('Forend_Band','Barrel','forend band bears on barrel'),
                      ('Muzzle_Band','Barrel','muzzle band bears on barrel'),
                      ('Muzzle_Band','Magazine_Tube','muzzle band bears on tube'),
                      ('Butt_Plate','Stock','curved butt plate seated against wood'),
                      ('Stock','Receiver','stock head meets receiver'),
                      ('Gate_Hinge','Gate_HingePin','loading gate supported on real hinge axis')]:
        contact(a,b,.0002,label)
    # Check the bearing lands themselves, including their outer edges; a
    # single minimum-distance contact cannot prove a broad tongue is seated.
    tang=surface('Upper_Tang');wood=surface('Stock')
    for y,x,start_z in [(-.035,.0046,-.08),(-.005,.0046,-.08),(.025,.0046,-.08),(.060,.0118,.039)]:
        for side in (-1,1):
            p=tang['tree'].ray_cast(Vector((side*x,y,start_z)),Vector((0,0,1)),.16)[0]
            assert p is not None,('Missing actual tang support land',y,side)
            gap=wood['tree'].find_nearest(p)[3]
            rows.append(dict(kind='tang underside supported by stock at Y %.1f mm / side %d'%(y*1000,side),
                metal_surface_m=list(p),distance_m=gap,limit_m=.00015,passed=gap<=.00015))
    tang=surface('Upper_Tang');bm=bmesh.new()
    mesh=bpy.data.meshes.new('CHECK tang solids');mesh.from_pydata(tang['points'],[],tang['faces']);bm.from_mesh(mesh)
    bpy.data.meshes.remove(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8)
    unseen=set(bm.verts);components=[]
    while unseen:
        seed=unseen.pop();group={seed};todo=[seed]
        while todo:
            for edge in todo.pop().link_edges:
                for vertex in edge.verts:
                    if vertex in unseen:unseen.remove(vertex);group.add(vertex);todo.append(vertex)
        components.append(group)
    for index,group in enumerate(components):
        vertices=list(group);lookup={v:i for i,v in enumerate(vertices)}
        faces=[f for f in bm.faces if f.verts[0] in group]
        mesh=bpy.data.meshes.new('CHECK tang component')
        mesh.from_pydata([tuple(v.co) for v in vertices],[],[[lookup[v] for v in f.verts] for f in faces])
        temporary=bpy.data.objects.new('CHECK tang component',mesh);bpy.context.collection.objects.link(temporary)
        gap,method=assembly.distance(temporary,part('Receiver'))
        rows.append(dict(kind='upper tang component %d physically reaches receiver'%index,
            distance_m=gap,limit_m=.00015,method=method,passed=gap<=.00015))
        bpy.data.objects.remove(temporary,do_unlink=True);bpy.data.meshes.remove(mesh)
    bm.free()
    W.pose(arm,'HammerSafe',48)
    contact('Hammer_HalfCockLand','Sear_Nose',.00015,'half-cock hammer supported at sear land')
    W.pose(arm,'Fire',3)
    contact('Hammer_StrikeLand','FiringPin_Tail',.00015,'fired hammer rests on firing-pin tail')
    W.pose(arm,'Cycle',36)
    contact('Carrier_Cradle','Carrier_Live_Case',.0002,'raised carrier holds round')
    round_s=surface('Carrier_Live_Case')
    # Actual head and mouth ring centers independently recover the cartridge
    # axis; named-bone coordinates alone cannot establish presentation.
    points=round_s['points'];low=min(p.y for p in points);high=max(p.y for p in points)
    rings=[]
    for y in (low,high):
        ring=[p for p in points if abs(p.y-y)<1e-6]
        rings.append(sum(ring,Vector())/len(ring))
    rows.append(dict(kind='carrier round aligned to chamber',head_m=list(rings[0]),mouth_m=list(rings[1]),
        passed=all(abs(p.x)<.0001 and abs(p.z-.048)<.0001 for p in rings)))
    for f in (0,22,36,58):
        W.pose(arm,'Cycle',f)
        contact('Lever_Hub','Lever_PivotPin',.00016,'lever bearing supported on dropping link at f'+str(f))
    for f in (0,36):
        W.pose(arm,'Cycle',f)
        contact('Carrier_Hub','Carrier_Pin',.00016,'carrier bearing support at f'+str(f))
    for n in range(1,7):
        W.pose(arm,'Idle' if n==6 else 'IdleTube'+str(n),0)
        contact('Magazine_Follower','Tube_Round'+str(n)+'_FlatNose',.00015,'follower bears on count '+str(n))
        for i in range(1,n):contact('Tube_Round'+str(i)+'_FlatNose','Tube_Round'+str(i+1)+'_Case',.0002,'adjacent tube rounds '+str(i)+'/'+str(i+1))
    W.pose(arm,'Idle',0)
    # Separate containment proof: every tube cartridge vertex lies inside the
    # actual inner-tube radius and between its rear/front planes.
    tube=surface('Magazine_Tube');inner=tube['tree'].ray_cast(Vector((0,.30,.020)),Vector((1,0,0)),.02)[0]
    assert inner is not None;inner_radius=inner.x
    for i in range(1,7):
        points=[p for ob in parts() if ob['bone']=='Tube'+str(i) for p in motion.surface(ob)['points']]
        radial=max(math.hypot(p.x,p.z-.020) for p in points)
        rows.append(dict(kind='tube contains round '+str(i),maximum_radius_m=radial,
            y_range_m=[min(p.y for p in points),max(p.y for p in points)],
            measured_inner_tube_radius_m=inner_radius,
            passed=radial<inner_radius and min(p.y for p in points)>tube['lo'].y and max(p.y for p in points)<tube['hi'].y))
    return rows


def geometry(arm):
    W.pose(arm,'Idle',0);obs=parts();counts={o.name:len(o.data.polygons) for o in obs}
    bad={}
    for ob in obs:
        if ob.get('allow_boundary'):continue
        bm=bmesh.new();bm.from_mesh(ob.data);n=sum(not e.is_manifold for e in bm.edges);bm.free()
        if n:bad[ob.name]=n
    points=[p for ob in obs if min(abs(v) for v in arm.pose.bones[ob['bone']].matrix.to_scale())>.01
            for p in motion.surface(ob)['points']]
    lo=[min(p[k] for p in points) for k in range(3)];hi=[max(p[k] for p in points) for k in range(3)]
    barrel=surface('Barrel')
    eye=part('Socket_Eye').matrix_world.translation
    comb=surface('Stock')['tree'].ray_cast(eye,Vector((0,0,-1)),.2)[0]
    assert comb is not None,'Eye must sit over an actual comb surface'
    # Actual front bead center from opposing surface intersections.
    bead=surface('Front_Bead');beadcenter=(bead['lo']+bead['hi'])/2
    # The central sight ray must pass through the notch and meet only the bead.
    obstructions=[]
    for ob in obs:
        if ob.get('allow_boundary') or min(abs(v) for v in arm.pose.bones[ob['bone']].matrix.to_scale())<.001:continue
        hit=motion.surface(ob)['tree'].ray_cast(eye,Vector((0,1,0)),.85)
        if hit[0] is not None:obstructions.append((hit[3],ob.name))
    obstructions.sort()
    trigger=surface('Trigger_Blade');pad=surface('Butt_Plate')
    face=trigger['tree'].ray_cast(Vector((0,.12,-.017)),Vector((0,-1,0)),.1)[0]
    shoulder=pad['tree'].ray_cast(Vector((0,-.30,-.017)),Vector((0,1,0)),.1)[0]
    lop=face.y-shoulder.y if face is not None and shoulder is not None else None
    backcurve=[]
    for z in (-.100,-.050,0):
        hit=pad['tree'].ray_cast(Vector((0,-.30,z)),Vector((0,1,0)),.1)[0]
        assert hit is not None
        backcurve.append(list(hit))
    shoulder=part('Socket_Butt').matrix_world.translation
    shoulder_gap=pad['tree'].find_nearest(shoulder)[3]
    rear=surface('Rear_Buckhorn')['tree']
    ledge=rear.ray_cast(Vector((.0025,.283,.085)),Vector((0,0,-1)),.04)[0]
    assert ledge is not None
    bead_angle=math.atan2(bead['hi'].z-eye.z,beadcenter.y-eye.y)
    ledge_angle=math.atan2(ledge.z-eye.z,ledge.y-eye.y)
    assert abs(bead_angle-ledge_angle)<math.radians(.03),'Bead top must appear level with notch shoulders'
    origin=Vector((0,.283,.0655))
    edges=[rear.ray_cast(origin,Vector((s,0,0)),.015)[0] for s in (-1,1)]
    assert all(v is not None for v in edges)
    blade_rows=[]
    for z in (-.011,-.020,-.026):
        p=trigger['tree'].ray_cast(Vector((0,.12,z)),Vector((0,-1,0)),.10)[0]
        assert p is not None;blade_rows.append(list(p))
    assert blade_rows[0][1]>blade_rows[1][1] and blade_rows[2][1]>blade_rows[1][1], 'Muzzle-facing concavity and forward toe'
    forms=form_audit.measure(arm)
    return dict(form_round2=forms,triangles=sum(counts.values()),parts=counts,nonmanifold=bad,
        bounds_m=dict(low=lo,high=hi,size=[b-a for a,b in zip(lo,hi)]),
        barrel_length_m=barrel['hi'].y-barrel['lo'].y,length_of_pull_m=lop,
        eye_position_m=list(eye),eye_above_comb_m=eye.z-comb.z,comb_surface_m=list(comb),
        front_bead_center_m=list(beadcenter),sight_first_hits=obstructions,
        materials=len({m.name for o in obs for m in o.data.materials}),butt_plate_back_samples_m=backcurve,
        shoulder_socket_surface_gap_m=shoulder_gap,rear_notch_shoulder_m=list(ledge),
        eye_behind_rear_sight_m=ledge.y-eye.y,notch_width_m=edges[1].x-edges[0].x,
        projected_bead_shoulder_difference_degrees=math.degrees(bead_angle-ledge_angle),
        trigger_front_surface_samples_m=blade_rows)


def add_hand_proxies(arm):
    """Conservative hand envelopes, no claimed anatomical hand animation."""
    W.pose(arm,None,0)
    mat=bpy.data.materials.new('Check hand envelope');mat.diffuse_color=(.2,.12,.08,1)
    # Palm alongside a straight wrist; four fingers inside the lever loop.
    ob=M.box('CHECK_HandPalm',(.029,-.006,-.004),(.023,.066,.044),mat,.006,3)
    proxies=[(ob,'Root')]
    for i,y in enumerate((-.026,-.010,.006,.022)):
        z=-.027+.1763*(y-.010)
        ob=M.cylinder('CHECK_LeverFinger'+str(i),(-.007,y,z),(.023,y,z),.0058,mat,16)
        proxies.append((ob,'LeverHand'))
    for ob,bone in proxies:
        M.apply(ob);ob.data.transform(ob.matrix_world);ob.matrix_world.identity()
        ob['check_proxy']=True;ob['bone']=bone;W.rigid_bind(ob,arm,bone)
    return [ob for ob,_ in proxies]


ALLOW=[
 dict(a='Chamber_Live',b='Barrel',reason='visual case rim/chamber seat',max_penetration_m=.00035),
 dict(a='Extracted_Case',b='Barrel',reason='visual fired rim/chamber seat before extraction',max_penetration_m=.00035),
 dict(a='Carrier_Live',b='Barrel',reason='visual case rim reaches chamber seat immediately before ownership handoff',max_penetration_m=.00035),
 dict(a='Lever_Hub',b='Lever_PivotPin',reason='solid inspection pin in lever bearing',max_penetration_m=.00015),
 dict(a='CHECK_HandPalm',b='CHECK_LeverFinger',reason='connected palm/finger envelopes overlap at knuckles',max_penetration_m=.006),
]


def sweep(arm,clips=None):
    proxies=add_hand_proxies(arm)
    errors=[];plane_errors=[]
    def check_plane(scene,*_):
        try:plane_errors.append(form_audit.plane(arm))
        except AssertionError as exc:errors.append(str(exc))
    bpy.app.handlers.frame_change_post.append(check_plane)
    try:
        result=motion.sweep_clips(arm,clips or list(interface.CLIPS),step_frames=.5,tolerance_m=.0002,allow=ALLOW)
    finally:
        bpy.app.handlers.frame_change_post.remove(check_plane)
        for ob in proxies:bpy.data.objects.remove(ob,do_unlink=True)
    result['lever_midplane']=dict(passed=not errors,samples=len(plane_errors),errors=errors,
        maximum_normal_vector_error=max(plane_errors,default=0))
    result['passed']=result['passed'] and not errors
    return result


def semantics(arm):
    """Intended-state assertions independent of source/import agreement."""
    def delta(name):return arm.pose.bones[name].matrix@arm.data.bones[name].matrix_local.inverted()
    def visible(name):return min(abs(v) for v in arm.pose.bones[name].matrix.to_scale())>.5
    def count():return sum(visible('Tube'+str(i)) for i in range(1,7))
    checks=0
    for name,s in interface.CLIPS.items():
        for f in [0,s['frames'],*s['events'].values()]:
            W.pose(arm,name,f);scene_frame(arm,name,f)
            form_audit.plane(arm)
            assert abs(part('Socket_Shell').matrix_world.determinant()-1)<1e-5
            checks+=1
        W.pose(arm,name,s['frames']);end=interface.STATES[s['end']]
        assert count()==end['tube'],(name,'tube end count',count(),end)
        assert visible('ChamberRound')==bool(end['chamber']),(name,'chamber occupancy')
        assert visible('FiredCase')==bool(end['case']),(name,'case occupancy')
        if name.startswith('Cycle') or name=='Chamber':
            W.pose(arm,name,36)
            assert abs(math.degrees(delta('Carrier').to_quaternion().angle)-20)<.01, 'Carrier stroke independent of ammunition'
            W.pose(arm,name,6);assert delta('Bolt').translation.length<1e-6
            assert abs(delta('LockingBlock').translation.z+.030)<1e-6
            W.pose(arm,name,22);assert abs(delta('Bolt').translation.y+.090)<1e-6
            assert abs(math.degrees(delta('Lever').to_quaternion().angle)-80)<.01
        if name.startswith('Fire'):
            W.pose(arm,name,3);assert visible('FiredCase') and not visible('ChamberRound')
            assert delta('Hammer').to_quaternion().angle<1e-5
        for phase in s.get('interruptible',[]):
            for f in (phase['begin'],phase['end']):
                W.pose(arm,name,f);token=interface.interrupt(name,f)
                assert token['exit_state']==phase['state']
                assert count()==interface.STATES[phase['state']]['tube']
                checks+=1
    # Complete chain consumes one round at each manual cycle; Fire alone never
    # ejects or magically recocks the hammer.
    state='ready'
    for n in range(6,-1,-1):
        fire='Fire' if n==6 else ('FireLast' if n==0 else 'Fire'+str(n))
        cycle='Cycle' if n==6 else ('CycleLast' if n==0 else 'Cycle'+str(n))
        state=interface.transition(interface.transition(state,fire),cycle)
    assert state=='empty_closed'
    for f,tube_count,chamber in [(0,0,False),(58,1,False),(72,1,False),(122,0,True),
                                 *[(190+72*i,i+1,True) for i in range(6)]]:
        W.pose(arm,'ReloadEmpty',f)
        assert count()==tube_count and visible('ChamberRound')==chamber,('ReloadEmpty',f)
        checks+=1
    for clip,frame in [('Reload',31.5),('ReloadSeveral',97.5),('ReloadEmpty',231.5)]:
        W.pose(arm,clip,frame);before={b.name:b.matrix.copy() for b in arm.pose.bones}
        W.pose(arm,'IdleEmpty',0);W.pose(arm,clip,frame)
        assert max(abs(b.matrix[i][j]-before[b.name][i][j]) for b in arm.pose.bones for i in range(4) for j in range(4))<1e-6
        checks+=1
    W.pose(arm,'Idle',0)
    return dict(passed=True,intended_event_checks=checks,complete_count_chain=state)


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',default='build/lever.blend');p.add_argument('--out',default='build/check.json');p.add_argument('--motion',action='store_true');p.add_argument('--clips')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
    arm=part('LeverArmature');result=geometry(arm);result['schema']=manifest(interface)
    result['contacts']=contacts(arm);result['semantics']=semantics(arm)
    errors=[]
    if not 30000<=result['triangles']<=40000:errors.append('triangle budget')
    if result['nonmanifold']:errors.append('nonmanifold solids')
    if abs(result['barrel_length_m']-.508)>.0001:errors.append('barrel length')
    if abs(result['bounds_m']['size'][1]-.9652)>.002:errors.append('overall length')
    if result['length_of_pull_m'] is None or not .335<result['length_of_pull_m']<.350:errors.append('length of pull')
    if not .035<result['eye_above_comb_m']<.050:errors.append('cheek weld')
    if not result['sight_first_hits'] or result['sight_first_hits'][0][1]!='Front_Bead':errors.append('aim obstruction')
    if not all(r['passed'] for r in result['contacts']):errors.append('required contacts')
    if a.motion:
        result['motion']=sweep(arm,a.clips.split(',') if a.clips else None)
        if not result['motion']['passed']:errors.append('motion clearance')
    result.update(passed=not errors,errors=errors)
    Path(a.out).write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ('parts','contacts','motion')},indent=2))
    if errors:raise RuntimeError(errors)


if __name__=='__main__':main()
