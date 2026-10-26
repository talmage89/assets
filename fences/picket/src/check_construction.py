"""Measured supports, snapped joints and released gate swing on real surfaces."""
import argparse,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[2])]
from dimensions import *
from kit import assembly,motion

def owned(ob,root):
    while ob:
        if ob==root:return True
        ob=ob.parent
    return False

def bounds(ob,root):
    ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();inv=root.matrix_world.inverted()
    ps=[inv@ob.matrix_world@v.co for v in me.vertices];ev.to_mesh_clear()
    return [[min(p[k] for p in ps) for k in range(3)],[max(p[k] for p in ps) for k in range(3)]]

def source(path):
    bpy.ops.wm.open_mainfile(filepath=str(Path(path).resolve()));bpy.context.view_layer.update();obs=bpy.context.scene.objects;errors=[];contacts=[]
    def require(t,m):
        if not t:errors.append(m)
    def support(a,b):
        d,method=assembly.distance(obs[a],obs[b]);contacts.append(dict(parts=[a,b],distance_m=d,method=method));require(d<.0002,'unsupported '+a+' / '+b)
    pieces={}
    for n in STAGING:
        r=obs[n];tri=0
        for o in obs:
            if o.type=='MESH' and owned(o,r):
                ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles();tri+=len(me.loop_triangles);ev.to_mesh_clear()
        pieces[n]=tri
        if bpy.context.scene['quality']=='game':require(tri<=2000,'module over 2k: '+n)
    section_report={}
    for n in ('Picket_A','Picket_B'):
        r=obs[n];boards=[bounds(obs[f'{n} picket {i+1:02}'],r) for i in range(13)];gaps=[b[0][0]-a[1][0] for a,b in zip(boards,boards[1:])]
        span=(obs[n+'__R'].matrix_world.translation-obs[n+'__L'].matrix_world.translation).length
        require(abs(span-PITCH)<2e-6,'section socket pitch')
        require(min(gaps)>.08 and max(gaps)<.09,'picket spacing')
        for i in range(13):
            for j in (1,2):support(f'{n} picket {i+1:02}',f'{n} rail {j}')
        for s in (-1,1):
            post=('Picket_End' if n=='Picket_A' and s<0 else 'Picket_Corner' if n=='Picket_B' and s>0 else 'Picket_Line')+' timber'
            for j in (0,1):
                support(f'{n} rail {j+1}',f'{n} saddle {s} {j} seat')
                support(f'{n} saddle {s} {j} web',post)
        section_report[n]=dict(socket_span_m=span,board_width_m=boards[0][1][0]-boards[0][0][0],height_m=boards[0][1][2]-boards[0][0][2],gaps_m=gaps,bottom_m=boards[0][0][2])
    r=obs['Picket_GateBay'];left=bounds(obs['Picket gate hinge post'],r);right=bounds(obs['Picket gate latch post'],r)
    leafboxes=[bounds(obs[f'Picket gate board {i+1}'],r) for i in range(5)]
    opening=right[0][0]-left[1][0];sidegaps=[leafboxes[0][0][0]-left[1][0],right[0][0]-leafboxes[-1][1][0]]
    require(abs(opening-OPENING)<2e-5,'clear gate opening');require(min(sidegaps)>.012 and max(sidegaps)<.0133,'gate side gaps')
    for j in (1,2):support('Picket compression brace','Picket gate rail '+str(j))
    for i in range(5):
        if i in (0,4):support(f'Picket gate board {i+1}','Picket gate stile '+str(-1 if i==0 else 1))
        else:
            for j in (1,2):support(f'Picket gate board {i+1}',f'Picket gate rail {j}')
    for ob in obs:
        if ob.type=='MESH' and ob.name.endswith(' pyramid cap'):support(ob.name,ob.name[:-12])
    axis=r.matrix_world.inverted()@obs['Picket_Gate'].matrix_world.translation;axis_errors=[]
    for i in (1,2):
        box=bounds(obs[f'Picket_Gate hinge {i} pin'],r);axis_errors.append(math.hypot((box[0][0]+box[1][0])/2-axis.x,(box[0][1]+box[1][1])/2-axis.y))
    require(max(axis_errors)<2e-5,'hinge pin not coaxial')
    latch=obs['Picket_Gate_Latch'];rest=latch.matrix_basis.copy();latch.rotation_euler.y=math.radians(-65);bpy.context.view_layer.update()
    sweep=motion.sweep({'MOTIONS':[dict(node='Picket_Gate',axis='Z',range=[-110,0],step=1,tolerance_m=.0003)]});latch.matrix_basis=rest
    require(sweep['passed'],'released gate collision')
    return dict(passed=not errors,errors=errors,pieces=pieces,sections=section_report,supports=contacts,gate=dict(opening_m=opening,sidegaps_m=sidegaps,axis_error_m=max(axis_errors),sweep=sweep))

def imported(path):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path(path).resolve()));bpy.context.view_layer.update();obs=bpy.context.scene.objects
    joins={}
    for n,s,p in [('Picket_A','L','Picket_End'),('Picket_A','R','Picket_Line'),('Picket_B','L','Picket_Line'),('Picket_B','R','Picket_Corner')]:joins[n+s]=(obs[n+'__'+s].matrix_world.translation-obs[p].matrix_world.translation).length
    # Check actual solids when Section A turns around the shared corner post.
    r=obs['Picket_A'];r.location=(PITCH,PITCH/2,0);r.rotation_mode='XYZ';r.rotation_euler.z=math.pi/2;bpy.context.view_layer.update()
    moving=[o for o in obs if o.type=='MESH' and owned(o,r)];fixed=[o for o in obs if o.type=='MESH' and (owned(o,obs['Picket_B']) or owned(o,obs['Picket_Corner']))]
    depth=max((motion.penetration(motion.surface(a),motion.surface(b),.0003)[0] for a in moving for b in fixed),default=0)
    return dict(passed=max(joins.values())<2e-5 and depth<=.0003,snap_errors_m=joins,corner_max_penetration_m=depth)

p=argparse.ArgumentParser();p.add_argument('--game',required=True);p.add_argument('--high',required=True);p.add_argument('--glb');p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
report={q:source(path) for q,path in [('game',a.game),('high',a.high)]}
if a.glb:report['imported']=imported(a.glb)
report['passed']=all(v['passed'] for v in report.values());Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if not report['passed']:raise RuntimeError('Picket construction failed')
