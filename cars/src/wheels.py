"""Original 18 x 7.5 six-fork alloy wheel, ISO tire and fixed caliper assembly."""
import math
from kit import model as G
from kit.vehicle import loaded_tire
from detail_helpers import box,print_quad


def build(b,S):
    for side,sign in [('L',-1),('R',1)]:
        for end,y in [('F',S.FRONT_AXLE),('R',S.REAR_AXLE)]:
            pos=(sign*S.TRACK/2,y,S.HUB_HEIGHT);parent=b.root
            if end=='F':
                steer=G.pivot('Steer_'+end+side,pos,'Z',(-35,35));steer.parent=b.root
                steer['checkpoint_only']=True;steer['kingpin_status']='vertical source proxy; caster/SAI delivery verification pending'
                parent=steer
            spin=G.pivot('Wheel_'+end+side,pos,'X',(-360,360))
            if end=='F':spin.location=(0,0,0)
            spin.parent=parent
            tire=loaded_tire('Tire_'+end+side,pos,S.TIRE_WIDTH,S.TIRE_ASPECT,S.RIM_INCHES,
                b.m['tire_'+side] if b.detail else b.m['rubber'],96 if b.high else 64,S.HUB_HEIGHT,
                profile_indices=None if b.high else [0,1,3,4,5,7,9,10,11,13,14])
            b.add(tire,spin,'tires');cx=pos[0];r=S.RIM_INCHES*.0254/2
            profile=[(-.093,r-.020),(-.093,r+.005),(-.081,r+.005),(.084,r-.008),(.099,r+.006),(.103,r-.015)]
            ob=G.lathe('Wheel barrel_'+end+side,[(cx+sign*x,rr) for x,rr in profile],b.m['wheel'],64 if b.high else 40,axis='X',center=(y,S.HUB_HEIGHT),closed=True)
            b.add(ob,spin,'wheels')
            hub=G.lathe('Wheel center_'+end+side,[(cx+sign*.068,0),(cx+sign*.068,.065),(cx+sign*.118,.065),(cx+sign*.129,.052),(cx+sign*.129,0)],b.m['wheel'],32 if b.high else 24,axis='X',center=(y,S.HUB_HEIGHT))
            b.add(hub,spin,'wheels')
            for k in range(6):
                angle=math.tau*k/6+.15
                for label,stations in [('root',[(.064,.123,.021,0),(.115,.109,.024,0),(.137,.103,.018,0)]),
                    ('a',[(.112,.110,.011,-.011),(.164,.095,.010,-.018),(.215,.090,.008,-.026)]),
                    ('b',[(.112,.110,.011,.011),(.164,.095,.010,.018),(.215,.090,.008,.026)])]:
                    loops=[]
                    for radial,axial,w,offset in stations:
                        loops.append([(cx+sign*(axial+dx),y+radial*math.cos(angle)-(offset+tw)*math.sin(angle),S.HUB_HEIGHT+radial*math.sin(angle)+(offset+tw)*math.cos(angle))
                                      for dx,tw in [(0,-w),(0,w),(-.018,w),(-.018,-w)]])
                    spoke=G.loft('Forged spoke_'+end+side+f'_{k}_{label}',loops,b.m['wheel'])
                    if b.high:G.bevel(spoke,.0012,2)
                    b.add(spoke,spin,'wheels')
                if b.detail:
                    a=math.tau*k/6;cy=y+.041*math.cos(a);cz=S.HUB_HEIGHT+.041*math.sin(a)
                    lug=G.lathe('Wheel lug_'+end+side+str(k),[(cx+sign*.125,0),(cx+sign*.125,.0088),(cx+sign*.137,.0088),(cx+sign*.140,.0068),(cx+sign*.140,0)],b.m['chrome'],6,axis='X',center=(cy,cz))
                    b.add(lug,spin,'wheels')
            if b.detail:
                x=cx+sign*.130
                print_quad(b,'Alder center cap_'+end+side,[(x,y-sign*.029,S.HUB_HEIGHT-.010),(x,y+sign*.029,S.HUB_HEIGHT-.010),(x,y+sign*.029,S.HUB_HEIGHT+.010),(x,y-sign*.029,S.HUB_HEIGHT+.010)],b.m['badge'],'wheels',spin)
                # Disc rotates; caliper follows the knuckle but never the wheel.
                rotor=G.lathe('Brake rotor_'+end+side,[(cx+sign*.008,.061),(cx+sign*.008,.161),(cx+sign*.028,.161),(cx+sign*.028,.061)],b.m['brake'],48 if b.high else 32,axis='X',center=(y,S.HUB_HEIGHT),closed=True)
                b.add(rotor,spin,'brakes')
                caliper=box(b,'Brake caliper_'+end+side,(cx+sign*.030,y+.132,S.HUB_HEIGHT+.035),(.046,.083,.135),b.m['caliper'],'brakes',parent,.012)
                caliper['wheel_clearance_basis']='Outboard x extent .053 versus spoke inner extent >=.072; radial barrel gap separately measured'
