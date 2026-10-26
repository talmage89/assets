"""Physical construction gates, separate from GLB serialization verification.

Measures actual evaluated source/game surfaces and imported socket transforms.
Motion uses the kit's solid-surface solver with the latch released first.
"""
import argparse,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from dimensions import *
from kit import motion


def vertices(ob):
    ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
    ps=[ob.matrix_world@v.co for v in me.vertices];ev.to_mesh_clear();return ps


def box(ob,frame=None):
    inv=frame.matrix_world.inverted() if frame else Matrix.Identity(4)
    ps=[inv@p for p in vertices(ob)]
    return [[min(p[k] for p in ps) for k in range(3)],[max(p[k] for p in ps) for k in range(3)]]


def owned(ob,root):
    while ob:
        if ob==root:return True
        ob=ob.parent
    return False


def source_check(path):
    bpy.ops.wm.open_mainfile(filepath=str(Path(path).resolve()));bpy.context.view_layer.update()
    obs=bpy.context.scene.objects;errors=[]
    def require(test,message):
        if not test:errors.append(message)
    pieces={}
    for name in STAGING:
        root=obs[name];meshes=[o for o in obs if o.type=='MESH' and owned(o,root)]
        tris=0
        for ob in meshes:
            ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles();tris+=len(me.loop_triangles);ev.to_mesh_clear()
        pieces[name]=dict(triangles=tris,meshes=len(meshes),origin_world_m=list(root.matrix_world.translation))
        if bpy.context.scene.get('quality')=='game':require(tris<=2000,f'{name} exceeds 2k triangles')
    sections={}
    for name in ('Section_A','Section_B'):
        root=obs[name];pickets=[obs[f'{name} picket {i+1:02}'] for i in range(17)]
        boxes=[box(ob,root) for ob in pickets]
        gaps=[b[0][0]-a[1][0] for a,b in zip(boxes,boxes[1:])]
        rails=[box(obs[f'{name} rail {i+1}'],root) for i in range(3)]
        seat=[];postweb=[];screw_gaps=[]
        for sign in (-1,1):
            face=sign*(PITCH-POST)/2
            for j,rail in enumerate(rails):
                prefix=f'{name} saddle {(-sign):+} {j+1}'
                web=box(obs[prefix+' web'],root);bottom=box(obs[prefix+' seat'],root)
                seat.append(rail[0][2]-bottom[1][2])
                postweb.append(abs((web[0 if sign<0 else 1][0])-face))
                screw_gaps.append((rail[0][0]-web[1][0]) if sign<0 else (web[0][0]-rail[1][0]))
        width=boxes[-1][1][0]-boxes[0][0][0]
        socket_span=(obs[name+'__R'].matrix_world.translation-obs[name+'__L'].matrix_world.translation).length
        sections[name]=dict(socket_span_m=socket_span,picket_envelope_width_m=width,
            board_count=len(boxes),min_dry_gap_m=min(gaps),max_dry_gap_m=max(gaps),
            minimum_bottom_m=min(b[0][2] for b in boxes),maximum_top_m=max(b[1][2] for b in boxes),
            rail_centers_m=[(b[0][2]+b[1][2])/2 for b in rails],
            rail_to_seat_gaps_m=seat,web_to_post_plane_gaps_m=postweb,rail_to_web_gaps_m=screw_gaps)
        require(abs(socket_span-PITCH)<2e-6,name+' wrong socket pitch')
        require(abs(width-(PITCH-POST))<2e-5,name+' picket/post seam')
        require(min(gaps)>.0004 and max(gaps)<.003,name+' boards intersect or have large gaps')
        require(min(b[0][2] for b in boxes)>.049,name+' insufficient ground clearance')
        require(max(abs(v) for v in seat)<.0002,name+' rails do not bear on saddles')
        require(max(postweb)<.0002,name+' saddle does not meet post plane')
        require(min(screw_gaps)>.004,name+' missing rail-to-web screw clearance')
    gate_root=obs['Gate_Bay'];gb=[box(obs['Gate picket '+str(i+1)],gate_root) for i in range(7)]
    leftpost=box(obs['Gate hinge post'],gate_root);rightpost=box(obs['Gate latch post'],gate_root)
    open_width=rightpost[0][0]-leftpost[1][0]
    sidegaps=[gb[0][0][0]-leftpost[1][0],rightpost[0][0]-gb[-1][1][0]]
    gate_width=gb[-1][1][0]-gb[0][0][0]
    require(abs(open_width-OPENING)<2e-5,'gate clear opening')
    require(min(sidegaps)>.012 and max(sidegaps)<.0134,'gate side gaps')
    brace_contacts=[]
    for i in (1,2):
        brace=box(obs['Gate compression brace '+str(i)],gate_root)
        low=box(obs['Gate rail '+str(i)],gate_root);high=box(obs['Gate rail '+str(i+1)],gate_root)
        brace_contacts += [brace[0][2]-low[1][2],high[0][2]-brace[1][2]]
    require(max(abs(x) for x in brace_contacts)<.0002,'brace does not bear on rails')
    # Gate pivot must be coaxial with BOTH stationary pins, from actual vertices.
    axis=gate_root.matrix_world.inverted()@obs['Gate'].matrix_world.translation
    pin_centers=[]
    for i in (1,2):
        b=box(obs[f'Gate hinge {i} fixed pin'],gate_root)
        pin_centers.append([(b[0][k]+b[1][k])/2 for k in (0,1)])
    axis_error=max(math.hypot(v[0]-axis.x,v[1]-axis.y) for v in pin_centers)
    require(axis_error<2e-5,'gate pivot not coaxial with physical pins')
    # Raise the gravity latch before swinging the leaf; restoring both states
    # lets the ordinary kit check separately exercise the latch at closed gate.
    latch=obs['Latch'];rest=latch.matrix_basis.copy()
    latch.rotation_euler.y=math.radians(-65);bpy.context.view_layer.update()
    sweep=motion.sweep({'MOTIONS':[dict(node='Gate',axis='Z',range=[-110,0],step=1,tolerance_m=.0003)]})
    latch.matrix_basis=rest;bpy.context.view_layer.update()
    require(sweep['passed'],'released gate hits fixed geometry')
    return dict(passed=not errors,errors=errors,pieces=pieces,sections=sections,
        gate=dict(clear_opening_m=open_width,leaf_width_m=gate_width,side_gaps_m=sidegaps,
                  brace_to_rail_gaps_m=brace_contacts,hinge_axis_xy_error_m=axis_error,
                  released_gate_sweep=sweep),source=str(path))


def imported_check(path):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path(path).resolve()))
    bpy.context.view_layer.update();obs=bpy.context.scene.objects
    errors=[];joins=[]
    for section,end,post in [('Section_A','L','Post_End'),('Section_A','R','Post_Line'),('Section_B','L','Post_Line'),('Section_B','R','Post_Corner')]:
        a=obs[section+'__'+end].matrix_world.translation;b=obs[post].matrix_world.translation
        gap=(a-b).length;joins.append(dict(section=section,socket=end,post=post,error_m=gap))
        if gap>2e-5:errors.append('imported snap seam '+section+end)
    # Independent local module dimensions and socket lengths after import.
    spans={n:(obs[n+'__R'].matrix_world.translation-obs[n+'__L'].matrix_world.translation).length for n in ('Section_A','Section_B','Gate_Bay')}
    for n,value in spans.items():
        if abs(value-(GATE_PITCH if n=='Gate_Bay' else PITCH))>2e-5:errors.append('imported span '+n)
    # A 90 degree turn uses the same endpoint/socket rule. Transform actual
    # imported picket/frame geometry into the corner pose, then check solids.
    root=obs['Section_A'];root.location=(PITCH,PITCH/2,0);root.rotation_mode='XYZ';root.rotation_euler.z=math.pi/2
    bpy.context.view_layer.update()
    moving=[o for o in obs if o.type=='MESH' and owned(o,root)]
    fixed=[o for o in obs if o.type=='MESH' and (owned(o,obs['Section_B']) or owned(o,obs['Post_Corner']))]
    depths=[]
    for ob in moving:
        for other in fixed:depths.append(motion.penetration(motion.surface(ob),motion.surface(other),.0003)[0])
    maximum=max(depths,default=0)
    if maximum>.0003:errors.append('corner overlap')
    return dict(passed=not errors,errors=errors,serialization_only=False,joins=joins,spans_m=spans,corner_max_penetration_m=maximum,
                method='Actual imported sockets; measured transformed imported solids at 90 degree corner')


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--glb',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);game=source_check(a.source)
    high=source_check(str(Path(a.source).with_name('lookdev.blend')))
    imp=imported_check(a.glb);result=dict(passed=game['passed'] and high['passed'] and imp['passed'],game=game,high=high,imported=imp)
    Path(a.out).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
    if not result['passed']:raise RuntimeError('Construction check failed: '+a.out)

if __name__=='__main__':main()
