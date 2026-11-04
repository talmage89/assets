"""Low-detail FWD unibody: subframes, transverse engine, tank and suspension."""
import bpy
from kit import model as G
from mathutils import Vector
from hatch_check import mesh_tree
from detail_helpers import box,tube
import hatch_spec as S


def build(b):
    # A 1.2 mm returned floor rises over the under-seat fuel tank, then
    # into the trunk well. Front seat rails and sill boxes meet its actual top.
    rings=[[(x,y,z) for x,z in [(-half,top-.0012),(half,top-.0012),(half,top),(-half,top)]]
           for y,half,top in [(-.77,.56,.270),(-.50,.71,.270),(.28,.71,.270),(.48,.71,.384),(1.20,.57,.384),(1.63,.55,.480)]]
    floor=b.add(G.loft('H120 stamped floor',rings,b.m['frame']),category='underbody')
    for sign in [-1,1]:
        rings=[[(sign*.43+x,y,z+dz) for x,dz in [(-.04,-.035),(.04,-.035),(.04,.035),(-.04,.035)]]
               for y,z in [(-1.98,.48),(-1.90,.30),(-.990,.270)]]
        b.add(G.loft('H120 front longitudinal rail '+str(sign),rings,b.m['frame']),category='underbody')
    for axle,label in [(S.FRONT_AXLE,'front'),(S.REAR_AXLE,'rear')]:
        box(b,'H120 '+label+' subframe crossmember',(0,axle,.232),(1.18,.13,.075),b.m['frame'],'underbody',radius=.010)
        for sign in [-1,1]:
            x=sign*(.46 if label=='front' else .48)
            tube(b,'H120 '+label+' subframe arm '+str(sign),[(x,axle-.22,.24),(sign*(.53 if label=='front' else .56),axle,.24),(x,axle+.22,.24)],.032,b.m['frame'],'underbody',sides=6)
            joint=Vector((sign*.69,axle,.28));lower=Vector((sign*.69,axle,.30))
            if label=='front':
                steer=bpy.data.objects['Steer_F'+('L' if sign<0 else 'R')]
                direction=Vector(steer['kingpin_axis_vehicle']);center=steer.matrix_world.translation
                joint=center+direction*((.28-center.z)/direction.z)
                lower=center+direction*((.30-center.z)/direction.z)
                upper=mesh_tree([bpy.data.objects['Wheelwell_F'+('L' if sign<0 else 'R')]]).ray_cast(center+direction, -direction,2)[0]
            else:
                upper=mesh_tree([bpy.data.objects['Wheelwell_R'+('L' if sign<0 else 'R')]]).ray_cast(Vector((sign*.61,axle,.4)),Vector((0,0,1)),1)[0]
            if upper is None:raise ValueError('Damper misses its actual structural wheelhouse')
            upper.z+=.0003
            tube(b,'H120 '+label+' lower arm '+str(sign),[(sign*.46,axle-.18,.24),joint,(sign*.46,axle+.18,.24)],.019,b.m['caliper'],'underbody',sides=6)
            if label=='front':upper.x-=sign*.022;lower.x-=sign*.022
            tube(b,'H120 '+label+' damper '+str(sign),[upper,lower],.026,b.m['frame'],'underbody',sides=8)
            parent=bpy.data.objects['Steer_F'+('L' if sign<0 else 'R')] if label=='front' else b.root
            track=S.FRONT_TRACK if label=='front' else S.REAR_TRACK
            tube(b,'H120 bearing '+label+str(sign),[(sign*(track/2-.11),axle,S.HUB_HEIGHT),(sign*(track/2+.060),axle,S.HUB_HEIGHT)],.035,b.m['caliper'],'underbody',parent,sides=8)
            tube(b,'H120 brake carrier '+label+str(sign),[(sign*(track/2-.025),axle,S.HUB_HEIGHT),(sign*(track/2-.023),axle+.12,S.HUB_HEIGHT+.032)],.012,b.m['caliper'],'underbody',parent,sides=6)
            if label=='front':
                tube(b,'H120 halfshaft '+str(sign),[(sign*.22,axle,S.HUB_HEIGHT),(sign*(track/2-.06),axle,S.HUB_HEIGHT)],.018,b.m['frame'],'underbody',sides=8)
                tube(b,'H120 tie rod '+str(sign),[(sign*.33,axle+.10,.30),(sign*.68,axle+.10,.30)],.010,b.m['brake'],'underbody',sides=6)
    box(b,'H120 steel firewall',(0,-1.035,.68),(1.00,.012,.42),b.m['frame'],'underbody',radius=0)
    box(b,'H120 transverse engine',(0,-1.56,.50),(.65,.49,.45),b.m['caliper'],'underbody',radius=.035)
    box(b,'H120 engine sump',(0,-1.52,.213),(.39,.35,.133),b.m['frame'],'underbody',radius=.017)
    box(b,'H120 engine top cover',(0,-1.56,.732),(.56,.43,.035),b.m['plastic'],'underbody',radius=.016)
    box(b,'H120 radiator',(0,-2.02,.54),(.96,.055,.31),b.m['frame'],'underbody',radius=.006)
    for sign in [-1,1]:
        box(b,'H120 engine mount '+str(sign),(sign*.35,-1.55,.36),(.10,.13,.07),b.m['rubber'],'underbody',radius=.005)
        b.add(G.profile('H120 engine mount pedestal '+str(sign),[(sign*.42,.25),(sign*.47,.25),(sign*.35,.34)],-1.57,-1.53,b.m['frame'],axis='Y'),category='underbody')
        box(b,'H120 sill reinforcement '+str(sign),(sign*.69,.15,.2295),(.12,1.64,.079),b.m['frame'],'underbody',radius=.006)
    box(b,'H120 transmission',(.37,-1.48,.42),(.25,.36,.28),b.m['caliper'],'underbody',radius=.028)
    box(b,'H120 fuel tank',(0,.72,.29),(.84,.48,.14),b.m['plastic'],'underbody',radius=.032)
    for y in [.56,.88]:
        outline=[(-.4212,.383),(-.4212,.2188),(.4212,.2188),(.4212,.383),(.420,.383),(.420,.220),(-.420,.220),(-.420,.383)]
        b.add(G.profile('H120 tank strap '+str(y),outline,y-.0125,y+.0125,b.m['frame'],axis='Y'),category='underbody')
    tube(b,'H120 exhaust',[(.15,-1.5,.29),(.20,-.97,.185),(.26,.30,.185),(.27,.98,.20),(.36,1.45,.24),(.50,1.92,.29),(.50,2.02,.28)],.022,b.m['brake'],'underbody',sides=8)
    box(b,'H120 catalyst',(.20,-.75,.20),(.16,.32,.095),b.m['brake'],'underbody',radius=.025)
    box(b,'H120 rear muffler',(.40,1.71,.273),(.28,.42,.13),b.m['brake'],'underbody',radius=.028)
    # Trunk well closes the car above the departure tangent.
    tub=box(b,'H120 trunk tub',(0,1.75,.45),(1.10,.48,.060),b.m['frame'],'underbody',radius=.02)
    support=mesh_tree([floor,tub])
    for y in [1.62,1.85]:
        hit=support.ray_cast(Vector((.52,y,.35)),Vector((0,0,1)),1)[0]
        if hit is None:raise ValueError('Exhaust hanger misses its actual floor support')
        tube(b,'H120 exhaust hanger '+str(y),[(.42,y,.31),(.46,y,.35),(.52,y,hit.z+.0003)],.006,b.m['frame'],'underbody',sides=6)
        box(b,'H120 exhaust isolator '+str(y),(.52,y,hit.z-.012),(.032,.025,.024),b.m['rubber'],'underbody',radius=0)
    for front in [True,False]:
        skin=mesh_tree([bpy.data.objects['Front molded fascia' if front else 'Rear molded fascia']]);rings=[]
        for x in [-.58,-.40,0,.40,.58]:
            p=skin.ray_cast(Vector((x,-3 if front else 3,.42 if front else .60)),Vector((0,1 if front else -1,0)),5)[0]
            if p is None:raise ValueError('Crash beam misses its fascia envelope')
            y=p.y+(.090 if front else -.090)
            rings.append([(x,y+dy,p.z+dz) for dy,dz in [(-.025,-.035),(.025,-.035),(.025,.035),(-.025,.035)]])
        b.add(G.loft('H120 '+('front' if front else 'rear')+' crash beam',rings,b.m['frame']),category='underbody')
