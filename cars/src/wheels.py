"""Family wheel assembly. Checkpoint rims establish volume, without final detail."""
import math
from kit import model as G
from kit.vehicle import loaded_tire


def build(b, dimensions):
    S=dimensions
    for side,sign in [('L',-1),('R',1)]:
        for end,y in [('F',S.FRONT_AXLE),('R',S.REAR_AXLE)]:
            pos=(sign*S.TRACK/2,y,S.HUB_HEIGHT)
            parent=b.root
            if end=='F':
                steer=G.pivot('Steer_'+end+side,pos,'Z',(-35,35));steer.parent=b.root
                steer['checkpoint_only']=True;steer['kingpin_status']='provisional vertical axis, caster/SAI deferred'
                parent=steer
            spin=G.pivot('Wheel_'+end+side,pos,'X',(-360,360))
            if end=='F':spin.location=(0,0,0)
            spin.parent=parent
            tire=loaded_tire('Tire_'+end+side,pos,S.TIRE_WIDTH,S.TIRE_ASPECT,S.RIM_INCHES,
                             b.m['rubber'],80 if not b.high else 144,S.HUB_HEIGHT)
            b.add(tire,spin,'tires')
            rim=S.RIM_INCHES*.0254/2;cx=pos[0]
            # 18x7.5 wheel. Positive offset: mounting face 44 mm outboard of rim center.
            profile=[(-.095,rim-.013),(-.095,rim+.006),(-.086,rim+.008),(-.080,rim-.005),
                     (.079,rim-.005),(.087,rim+.008),(.098,rim+.006),(.098,rim-.014),
                     (.086,rim-.022),(-.083,rim-.022)]
            wheel=G.lathe('Wheel barrel_'+end+side,[(cx+sign*a,r) for a,r in profile],b.m['wheel'],
                          48 if not b.high else 96,axis='X',center=(y,S.HUB_HEIGHT),closed=True)
            b.add(wheel,spin,'wheels')
            hub=G.lathe('Wheel hub_'+end+side,[(cx+sign*.045,0),(cx+sign*.045,.064),
                         (cx+sign*.092,.064),(cx+sign*.106,.049),(cx+sign*.106,0)],b.m['wheel'],32,axis='X',center=(y,S.HUB_HEIGHT))
            b.add(hub,spin,'wheels')
            for k in range(6):
                a=math.tau*k/6+.15
                # Broad simple spokes at checkpoint. Final bevels, lugs and brakes deferred.
                coords=[]
                for x,r,w in [(.076,.052,.023),(.076,rim-.0206,.020)]:
                    for t in [-1,1]:
                        coords.append((cx+sign*x,y+r*math.cos(a)-t*w*math.sin(a),S.HUB_HEIGHT+r*math.sin(a)+t*w*math.cos(a)))
                ob=G.mesh('Wheel spoke_'+end+side+f'_{k}',coords,[(0,2,3,1)],b.m['wheel'])
                sol=ob.modifiers.new('Cast spoke thickness','SOLIDIFY');sol.thickness=.025
                G.bevel(ob,.005,2);G.smooth(ob)
                b.add(ob,spin,'wheels')
