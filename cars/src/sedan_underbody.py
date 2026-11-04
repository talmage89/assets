"""Low-detail FWD unibody: subframes, transverse engine, tank and suspension."""
import bpy
from kit import model as G
from detail_helpers import box,tube
import sedan_spec as S


def build(b):
    box(b,'S240 stamped floor',(0,-.01,.224),(1.42,1.97,.050),b.m['frame'],'underbody',radius=.008)
    for axle,label in [(S.FRONT_AXLE,'front'),(S.REAR_AXLE,'rear')]:
        box(b,'S240 '+label+' subframe crossmember',(0,axle,.225),(1.18,.13,.075),b.m['frame'],'underbody',radius=.010)
        for sign in [-1,1]:
            x=sign*(.46 if label=='front' else .48)
            tube(b,'S240 '+label+' subframe arm '+str(sign),[(x,axle-.22,.24),(sign*(.55 if label=='front' else .56),axle,.24),(x,axle+.22,.24)],.032,b.m['frame'],'underbody',sides=6)
            tube(b,'S240 '+label+' lower arm '+str(sign),[(sign*.46,axle-.18,.24),(sign*.69,axle,.28),(sign*.46,axle+.18,.24)],.019,b.m['caliper'],'underbody',sides=6)
            tube(b,'S240 '+label+' damper '+str(sign),[(sign*.61,axle,.64),(sign*.69,axle,.30)],.026,b.m['frame'],'underbody',sides=8)
            parent=bpy.data.objects['Steer_F'+('L' if sign<0 else 'R')] if label=='front' else b.root
            track=S.FRONT_TRACK if label=='front' else S.REAR_TRACK
            tube(b,'S240 bearing '+label+str(sign),[(sign*(track/2-.07),axle,S.HUB_HEIGHT),(sign*(track/2+.01),axle,S.HUB_HEIGHT)],.035,b.m['caliper'],'underbody',parent,sides=8)
            tube(b,'S240 brake carrier '+label+str(sign),[(sign*(track/2-.025),axle,S.HUB_HEIGHT),(sign*(track/2-.023),axle+.12,S.HUB_HEIGHT+.032)],.012,b.m['caliper'],'underbody',parent,sides=6)
            if label=='front':
                tube(b,'S240 halfshaft '+str(sign),[(sign*.22,axle,S.HUB_HEIGHT),(sign*(track/2-.06),axle,S.HUB_HEIGHT)],.018,b.m['frame'],'underbody',sides=8)
                tube(b,'S240 tie rod '+str(sign),[(sign*.33,axle+.10,.30),(sign*.68,axle+.10,.30)],.010,b.m['brake'],'underbody',sides=6)
    box(b,'S240 steel firewall',(0,-1.035,.68),(1.50,.012,.42),b.m['frame'],'underbody',radius=0)
    box(b,'S240 transverse engine',(0,-1.56,.52),(.65,.49,.40),b.m['caliper'],'underbody',radius=.035)
    box(b,'S240 engine sump',(0,-1.52,.213),(.39,.35,.133),b.m['frame'],'underbody',radius=.017)
    box(b,'S240 engine top cover',(0,-1.56,.732),(.56,.43,.035),b.m['plastic'],'underbody',radius=.016)
    box(b,'S240 radiator',(0,-2.02,.54),(.96,.055,.31),b.m['frame'],'underbody',radius=.006)
    for sign in [-1,1]:
        box(b,'S240 engine mount '+str(sign),(sign*.38,-1.55,.52),(.10,.13,.09),b.m['rubber'],'underbody',radius=.005)
        box(b,'S240 sill reinforcement '+str(sign),(sign*.69,-.03,.18),(.12,2.00,.040),b.m['frame'],'underbody',radius=.006)
    box(b,'S240 transmission',(.37,-1.48,.42),(.25,.36,.28),b.m['caliper'],'underbody',radius=.028)
    box(b,'S240 fuel tank',(0,.72,.29),(.84,.48,.14),b.m['plastic'],'underbody',radius=.032)
    for y in [.56,.88]:box(b,'S240 tank strap '+str(y),(0,y,.218),(.85,.025,.006),b.m['frame'],'underbody',radius=0)
    tube(b,'S240 exhaust',[(.15,-1.5,.29),(.20,-.97,.185),(.26,.30,.185),(.27,.98,.20),(.36,1.45,.24),(.50,1.92,.29),(.50,2.19,.31)],.022,b.m['brake'],'underbody',sides=8)
    box(b,'S240 catalyst',(.20,-.75,.20),(.16,.32,.095),b.m['brake'],'underbody',radius=.025)
    box(b,'S240 rear muffler',(.40,1.79,.273),(.28,.42,.13),b.m['brake'],'underbody',radius=.028)
    for y in [1.62,1.96]:tube(b,'S240 exhaust hanger '+str(y),[(.42,y,.31),(.46,y,.35),(.56,y,.35)],.006,b.m['rubber'],'underbody',sides=6)
    # Trunk well closes the car above the departure tangent.
    box(b,'S240 trunk tub',(0,1.94,.57),(1.10,.62,.10),b.m['frame'],'underbody',radius=.02)
    box(b,'S240 front crash beam',(0,-2.13,.48),(1.25,.07,.10),b.m['frame'],'underbody',radius=.006)
    box(b,'S240 rear crash beam',(0,2.21,.61),(1.30,.07,.10),b.m['frame'],'underbody',radius=.006)
