"""Closure hinges and articulated telescopic supports, in the H120 rest frame."""
import math
import bpy
from mathutils import Vector,Matrix
from kit import model as G
from detail_helpers import box,tube,pivot
from hatch_check import mesh_tree
from hatch_exterior import repivot,world_parent
import hatch_spec as S


def gas_strut(b,label,lower,upper,closure,length,frame_anchor=None):
    lower,upper=Vector(lower),Vector(upper)
    for code,position,target,parent,material in [
        ('sleeve',lower,upper,b.root,b.m['frame']),
        ('rod',upper,lower,closure,b.m['chrome'])]:
        root=pivot(b,'H120 '+label+' '+code,position,parent,axis='Z',limits=(0,0))
        xf=Matrix.Translation(position)@(target-position).to_track_quat('Z','Y').to_matrix().to_4x4()
        root.matrix_world=xf
        endpoint=pivot(b,'H120 '+label+' target '+code,target,closure if code=='sleeve' else b.root)
        con=root.constraints.new('DAMPED_TRACK');con.target=endpoint;con.track_axis='TRACK_Z'
        if code=='sleeve':
            ob=G.lathe('H120 '+label+' telescoping sleeve',[(0,0),(0,.010),(length,.010),(length,.0058),(.020,.0058),(.020,0)],material,12 if b.high else 8)
            ob.matrix_world=xf
        else:ob=G.cylinder('H120 '+label+' telescoping rod',position,position+(target-position).normalized()*length,.0045,material,10 if b.high else 8)
        b.add(ob,root,'hinges');root['support_target']=endpoint.name;root['member_length_m']=length
        root['closed_length_m']=(target-position).length
    box(b,'H120 '+label+' fixed ball bracket',lower,(.024,.025,.025),b.m['frame'],'hinges',radius=0)
    hood=label.startswith('hood')
    if frame_anchor is None:
        box(b,'H120 '+label+' moving ball bracket',upper+Vector((0,0,.006 if hood else 0)),(.024,.025,.0272 if hood else .025),b.m['frame'],'hinges',closure,radius=0)
    else:
        b.add(G.cylinder('H120 '+label+' moving ball bracket',upper,frame_anchor,.0035,b.m['frame'],12 if b.high else 6),closure,'hinges')


def build(b):
    for side,sign in [('L',-1),('R',1)]:
        for end,y in [('F',S.DOOR_FRONT-.012),('R',S.DOOR_SPLIT+.005)]:
            door=bpy.data.objects['Door_'+end+side];limit=62 if end=='F' else 66
            repivot(door,(sign*(.838 if end=='F' else .820),y,.74),(-limit,0) if sign>0 else (0,limit))
            door['pivot_axis']='CUSTOM';door['hinge_axis_vehicle']=list(Vector((sign*.10,0,1)).normalized())
        # Jamb and B-post anchor the hinge leaves; not a floating sleeve.
        for end,yy in [('F',-.75),('R',S.DOOR_SPLIT-.020)]:
            box(b,'H120 hinge jamb '+end+side,(sign*.705,yy,.635),(.050,.065,.69),b.m['frame'],'hinges',radius=.003)
            parent=bpy.data.objects['Door_'+end+side];axis=Vector(parent['hinge_axis_vehicle']);center=parent.matrix_world.translation
            skin=mesh_tree([bpy.data.objects['Door '+end+'_'+side]])
            for z in [.60,.85]:
                c=center+axis*((z-center.z)/axis.z);label=end+side+str(z)
                pin=G.cylinder('H120 hinge pin '+label,c-axis*.020,c+axis*.020,.0035,b.m['chrome'],8 if b.high else 6)
                b.add(pin,category='hinges')
                count=12 if b.high else 6;inside=.0038/math.cos(math.pi/count)
                sleeve=G.lathe('H120 hinge sleeve '+label,[(-.011,.0065),(.011,.0065),(.011,inside),(-.011,inside)],b.m['frame'],count,closed=True)
                sleeve.location=c;sleeve.rotation_euler=axis.to_track_quat('Z','Y').to_euler();b.add(sleeve,parent,'hinges')
                p=skin.ray_cast(Vector((sign*2,yy+.20,z)),Vector((-sign,0,0)),4)[0]
                if p is not None:
                    path=[c+Vector((-sign*.006,.004,0))]
                    for t in ([.40,.55,.70,.85,1] if b.high else [.40,.70,1]):
                        yy2=c.y+(p.y-c.y)*t
                        hit=skin.ray_cast(Vector((sign*2,yy2,z)),Vector((-sign,0,0)),4)[0]
                        if hit is not None:path.append(hit+Vector((-sign*.014,0,0)))
                    outline=[(v.x-sign*.003,v.y) for v in path]+[(v.x+sign*.003,v.y) for v in reversed(path)]
                    b.add(G.profile('H120 moving hinge leaf '+label,outline,z-.0015,z+.0015,b.m['frame'],axis='Z'),parent,'hinges')
                    rings=[]
                    for depth in [.0007,.016]:
                        ring=[]
                        for dy,dz in [(-.020,-.012),(.020,-.012),(.020,.012),(-.020,.012)]:
                            hit=skin.ray_cast(Vector((sign*2,p.y+dy,z+dz)),Vector((-sign,0,0)),4)[0]
                            if hit is None:raise ValueError('Door hinge reinforcement misses its skin')
                            ring.append(hit+Vector((-sign*depth,0,0)))
                        rings.append(ring)
                    b.add(G.loft('H120 welded hinge reinforcement '+label,rings,b.m['frame']),parent,'hinges')
                plate=[(c.x,c.y),(sign*.705,yy),(c.x-sign*.012,c.y)]
                b.add(G.profile('H120 fixed hinge leaf '+label,plate,z-.019,z-.017,b.m['frame'],axis='Z'),category='hinges')
    hood=bpy.data.objects['Hood'];repivot(hood,(0,-1.080,.977),(-62,0))
    gate=bpy.data.objects['Liftgate'];repivot(gate,(0,1.455,1.385),(0,82))
    for side,sign in [('L',-1),('R',1)]:
        hood_tree=mesh_tree([bpy.data.objects['Hood outer']])
        q=hood_tree.ray_cast(Vector((sign*.57,-1.64,2)),Vector((0,0,-1)),3)[0]
        upper=q-Vector((0,0,.020));lower=Vector((sign*.57,-1.10,.69))
        gas_strut(b,'hood support '+side,lower,upper,hood,.42)
        support=mesh_tree([bpy.data.objects['Wheelwell_F'+side]]).ray_cast(lower+Vector((0,0,.10)),Vector((0,0,-1)),1)[0]
        if support is None:raise ValueError('Hood support pedestal misses the wheelhouse')
        middle=(lower+support)/2
        box(b,'H120 hood pedestal '+side,middle,(.020,.020,abs(lower.z-support.z)+.001),b.m['frame'],'hinges',radius=0)
        # Transverse roof bearings carry the liftgate hinge leaf and spoiler.
        c=Vector((sign*.46,1.455,1.385))
        tube(b,'H120 roof hinge pin '+side,[c-Vector((.030,0,0)),c+Vector((.030,0,0))],.004,b.m['chrome'],'hinges',sides=6)
        tube(b,'H120 gate hinge leaf '+side,[c+Vector((0,.012,0)),(sign*.46,1.565,1.356)],.006,b.m['frame'],'hinges',gate,sides=4)
        sleeve=G.lathe('H120 roof hinge sleeve '+side,[(-.018,.007),(.018,.007),(.018,.0044/math.cos(math.pi/6)),(-.018,.0044/math.cos(math.pi/6))],b.m['frame'],12 if b.high else 6,closed=True)
        sleeve.location=c;sleeve.rotation_euler=(0,math.pi/2,0);b.add(sleeve,gate,'hinges')
        for dx in [-.027,.027]:box(b,'H120 roof hinge bearing ear '+side+str(dx),c+Vector((dx,-.010,-.014)),(.010,.050,.025),b.m['frame'],'hinges',radius=0)
        # Ball ends remain attached to the body jamb and hatch frame.
        lower=Vector((sign*.60,1.79,.84))
        from hatch_exterior import perimeter,optical_normal
        glass=bpy.data.objects['Backlight'];points=perimeter(glass);normal=optical_normal(glass)
        guess=Vector((sign*.65,1.68,1.28));choices=[]
        for i,(a,c2) in enumerate(zip(points,points[1:]+points[:1])):
            delta=c2-a;t=max(0,min(1,(guess-a).dot(delta)/delta.length_squared))
            q=a.lerp(c2,t);choices.append(((q-guess).length,i,t,q))
        _,i,t,q=min(choices,key=lambda row:row[0])
        center=sum(points,Vector())/len(points)
        frame=[p-normal(p)*.009+(center-p).normalized()*.003 for p in points]
        anchor=frame[i].lerp(frame[(i+1)%len(frame)],t)
        upper=anchor-normal(q)*.015-Vector((sign*.015,.040,0))
        gas_strut(b,'gate support '+side,lower,upper,gate,.40,anchor)
        tube(b,'H120 gate strut jamb '+side,[(sign*.60,1.79,.84),(sign*.535,1.79,.477)],.010,b.m['frame'],'hinges',sides=6)
    # Liftgate inner trim closes the lower stamping while preserving cargo space.
    gate_skin=mesh_tree([bpy.data.objects['Liftgate outer']])
    rings=[]
    for z in [.67,.78,.88]:
        row=[]
        for x in [-.58,-.30,0,.30,.58]:
            hit=gate_skin.ray_cast(Vector((x,3,z)),Vector((0,-1,0)),3)[0]
            if hit is None:raise ValueError('Liftgate inner trim misses its stamping')
            row.append(hit-Vector((0,.018,0)))
        rings.append(row)
    trim=G.mesh('H120 liftgate inner trim',[p for r in rings for p in r],[(j*5+i,j*5+i+1,(j+1)*5+i+1,(j+1)*5+i) for j in range(2) for i in range(4)],b.m['interior'])
    sol=trim.modifiers.new('Molded inner card gauge','SOLIDIFY');sol.thickness=.004;sol.use_even_offset=False;G.apply(trim)
    b.add(trim,gate,'cargo')
    # Rear blade and arm follow the actual backlight, carried by the gate.
    glass=bpy.data.objects['Backlight'];tree=mesh_tree([glass]);path=[]
    for i in range(7):
        p=tree.ray_cast(Vector((-.04+.46*i/6,3,1.064)),Vector((0,-1,0)),3)[0]
        if p is not None:path.append(p+Vector((0,.007,0)))
    if len(path)>2:
        tube(b,'H120 rear wiper blade',path,.0035,b.m['rubber'],'trim',gate,sides=6)
        tube(b,'H120 rear wiper arm',[(0,path[0].y+.013,1.047),path[3]+Vector((0,.007,.005))],.006,b.m['frame'],'trim',gate,sides=6)
