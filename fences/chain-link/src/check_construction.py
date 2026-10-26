"""Chain-link surface supports, tube/gate dimensions and sampled clearance."""
import argparse,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
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
    def support(a,b,limit=.0003):
        d,method=assembly.distance(obs[a],obs[b]);contacts.append(dict(parts=[a,b],distance_m=d,method=method,limit_m=limit));require(d<=limit,'unsupported '+a+' / '+b)
    pieces={}
    for name in list(STAGING)+['Chain_GatePost_Hinge','Chain_GatePost_Latch','Chain_Gate']:
        tri=0
        for o in obs:
            if o.type=='MESH' and owned(o,obs[name]):
                ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles();tri+=len(me.loop_triangles);ev.to_mesh_clear()
        pieces[name]=tri
        if bpy.context.scene['quality']=='game' and name!='Chain_GateBay':require(tri<=2000,'module over 2k: '+name)
    panels={}
    for name in ('Chain_Start','Chain_EndSection','Chain_Section','Chain_BetweenTerminals'):
        r=obs[name];b=bounds(obs[name+'_Fabric'],r);span=(obs[name+'__R'].matrix_world.translation-obs[name+'__L'].matrix_world.translation).length
        require(abs(span-PITCH)<2e-6,'wrong post pitch');require(abs(b[1][2]-b[0][2]-HEIGHT)<2e-6,'wrong fabric height')
        require(abs(b[0][2]-GROUND)<2e-6,'wrong fabric ground clearance')
        for i in range(6):
            support(name+' top tie '+str(i),name+' top rail',.0017)
            support(name+' top tie '+str(i),name+'_Fabric',.0017)
        panels[name]=dict(socket_pitch_m=span,fabric_bounds_m=b)
    support('Chain_Start bottom tension wire','Chain_Terminal 0 tension bar')
    support('Chain_EndSection bottom tension wire','Chain_Corner 180 tension bar')
    support('Chain line post cap','Chain line post')
    support('Chain line post eye neck','Chain line post cap')
    support('Chain line post rail eye','Chain line post eye neck')
    for n in ('Chain_Terminal','Chain_Terminal_End','Chain_Corner'):
        support(n+' post cap',n+' post')
    # Bar/ear surfaces must meet around their real fastener, not just at nominal origins.
    for name in ['Chain_Terminal 0','Chain_Terminal_End 180','Chain_Corner 180','Chain_Corner 90','Chain gate outside -1','Chain gate outside 1']:
        for i in (1,2,3):
            for suffix in ('ear 0.0305','ear 0.0375'):
                support(name+' tension bar',name+' tension '+str(i)+' '+suffix,.0015)
    # A real corner stacks two band sets at different heights; duplicate rings
    # at the same height would z-fight and could not be assembled physically.
    corner_depths=[]
    for suffix in ['brace band']+['tension '+str(i)+' wrap' for i in (1,2,3)]:
        a=obs['Chain_Corner 180 '+suffix];b=obs['Chain_Corner 90 '+suffix]
        corner_depths.append(motion.penetration(motion.surface(a),motion.surface(b),.0003)[0])
    require(max(corner_depths)<.0003,'corner bands overlap')
    for n in ['Chain_Terminal 0','Chain_Terminal_End 180','Chain_Corner 180','Chain_Corner 90','Chain gate outside -1','Chain gate outside 1']:
        support(n+' rail end',n+' rail lug');support(n+' rail lug',n+' brace band')
    root=obs['Chain_GateBay'];a=bounds(obs['Chain gate hinge post'],root);b=bounds(obs['Chain gate latch post'],root);frame=bounds(obs['Chain gate welded frame'],root)
    clear=b[0][0]-a[1][0];gaps=[frame[0][0]-a[1][0],b[0][0]-frame[1][0]]
    require(abs(clear-OPENING)<.0001,'wrong walk-gate opening');require(min(gaps)>.045 and max(gaps)<.05,'wrong gate hardware allowance')
    axis=root.matrix_world.inverted()@obs['Chain_Gate'].matrix_world.translation;axes=[]
    for i in (0,1):
        pin=bounds(obs[f'Chain hinge {i} pin'],root);axes.append(math.hypot((pin[0][0]+pin[1][0])/2-axis.x,(pin[0][1]+pin[1][1])/2-axis.y))
        support(f'Chain hinge {i} fixed arm',f'Chain hinge {i} pin')
        support(f'Chain hinge {i} moving arm',f'Chain hinge {i} frame clamp')
        support(f'Chain hinge {i} moving arm',f'Chain hinge {i} sleeve')
    require(max(axes)<2e-5,'gate pivot is not on hinge pins')
    latch=obs['Chain_ForkLatch'];rest=latch.matrix_basis.copy();latch.rotation_euler.y=math.radians(-95);bpy.context.view_layer.update()
    swing=motion.sweep({'MOTIONS':[dict(node='Chain_Gate',axis='Z',range=[-110,0],step=1,tolerance_m=.0003)]});latch.matrix_basis=rest;bpy.context.view_layer.update()
    fork=motion.sweep({'MOTIONS':[dict(node='Chain_ForkLatch',axis='Y',range=[-95,0],step=1,tolerance_m=.0003)]})
    require(swing['passed'],'released gate hits fixed assembly');require(fork['passed'],'fork cannot release')
    return dict(passed=not errors,errors=errors,pieces=pieces,panels=panels,supports=contacts,corner_band_penetrations_m=corner_depths,gate=dict(clear_opening_m=clear,side_gaps_m=gaps,hinge_axis_error_m=max(axes),swing=swing,fork=fork))

def imported(path):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path(path).resolve()));bpy.context.view_layer.update();obs=bpy.context.scene.objects
    pairs=[('Chain_Start__L','Chain_Terminal'),('Chain_Start__R','Chain_Line'),('Chain_EndSection__L','Chain_Line'),('Chain_EndSection__R','Chain_Corner')]
    errors={a+' -> '+b:(obs[a].matrix_world.translation-obs[b].matrix_world.translation).length for a,b in pairs}
    for label,socket in [('Hinge','L'),('Latch','R')]:
        for node in ['Chain_GatePost_'+label,'Chain_GatePost_'+label+'__outside']:
            errors[node]=(obs[node].matrix_world.translation-obs['Chain_GateBay__'+socket].matrix_world.translation).length
    # Test the actual imported perpendicular bay against the shared corner.
    turn=obs['Chain_BetweenTerminals'];turn.location=(PITCH,PITCH/2,0);turn.rotation_mode='XYZ';turn.rotation_euler.z=math.pi/2
    bpy.context.view_layer.update()
    moving=[o for o in obs if o.type=='MESH' and owned(o,turn) and not o.get('allow_boundary',False)]
    fixed=[o for o in obs if o.type=='MESH' and (owned(o,obs['Chain_EndSection']) or owned(o,obs['Chain_Corner'])) and not o.get('allow_boundary',False)]
    depth=max((motion.penetration(motion.surface(a),motion.surface(b),.0003)[0] for a in moving for b in fixed),default=0)
    return dict(passed=max(errors.values())<2e-5 and depth<=.0003,snap_errors_m=errors,corner_penetration_m=depth)

p=argparse.ArgumentParser();p.add_argument('--game',required=True);p.add_argument('--high',required=True);p.add_argument('--glb');p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
report={q:source(path) for q,path in [('game',a.game),('high',a.high)]}
if a.glb:report['imported']=imported(a.glb)
report['passed']=all(v['passed'] for v in report.values());Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if not report['passed']:raise RuntimeError('Chain-link construction failed')
