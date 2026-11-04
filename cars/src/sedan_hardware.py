"""Five-stud passenger wheels and real concealed door hinge leaves/knuckles."""
import math
import bpy
from mathutils import Vector
from kit import model as G
from sedan_check import mesh_tree
import sedan_spec as S


def passenger_wheels(b):
    """Keep the six-fork casting; use a 5 x 114.3 mm stud circle.

    Bolt chamfers and the rotor hat's small return are source-only detail.
    These hidden subdivisions fund the structural door hinges.
    """
    for code in ['FL','FR','RL','RR']:
        sign=-1 if code.endswith('L') else 1;track=S.FRONT_TRACK if code.startswith('F') else S.REAR_TRACK
        y=S.FRONT_AXLE if code.startswith('F') else S.REAR_AXLE;cx=sign*track/2;axial=1.0;parent=bpy.data.objects['Wheel_'+code]
        bpy.context.view_layer.update()
        # Retain the actual 18 x 7.5 casting width. Its center and spoke roots
        # sit inboard of the lip, with sufficient room for the caliper behind.
        for ob in list(bpy.context.scene.objects):
            if ob.name.startswith('Wheel lug_'+code):
                bpy.data.objects.remove(ob,do_unlink=True);continue
            if ob.name not in ['Wheel center_'+code,'Alder center cap_'+code] and not ob.name.startswith('Cast spoke_'+code):continue
            inverse=ob.matrix_world.inverted()
            for v in ob.data.vertices:
                p=ob.matrix_world@v.co
                if ob.name.startswith('Cast spoke_'):
                    radial=math.hypot(p.y-y,p.z-S.HUB_HEIGHT)
                    shift=.039*max(0,min(1,(.211-radial)/(.211-.058)))
                else:shift=.039
                p.x-=sign*shift;v.co=inverse@p
        tire=bpy.data.objects['Tire_'+code]
        # 190.5 mm nominal bead seating width for the 7.5 inch rim;
        # preserve the accepted 235 mm sidewall envelope and rolling radius.
        for v in tire.data.vertices:
            radius=math.hypot(v.co.y,v.co.z)
            delta=.01065*max(0,min(1,(.2286+.075-radius)/.075))
            v.co.x+=math.copysign(delta,v.co.x)

        for k in range(5):
            angle=math.tau*k/5;cy=y+.05715*math.cos(angle);cz=S.HUB_HEIGHT+.05715*math.sin(angle)
            profile=[(.090,0),(.090,.011),(.102,.011),(.105,.0087),(.105,0)] if b.high else [(.090,0),(.090,.011),(.105,.011),(.105,0)]
            lug=G.lathe('S240 wheel stud '+code+str(k),[(cx+sign*x*axial,r) for x,r in profile],b.m['chrome'],6,axis='X',center=(cy,cz))
            b.add(lug,parent,'wheels')
        if not b.high:
            old=bpy.data.objects['Brake rotor_'+code];bpy.data.objects.remove(old,do_unlink=True)
            profile=[(.008,.061),(.008,.161),(.028,.161),(.028,.104),(.045,.061)]
            rotor=G.lathe('Brake rotor_'+code,[(cx+sign*x*axial,r) for x,r in profile],b.m['brake'],18,axis='X',center=(y,S.HUB_HEIGHT),closed=True)
            rotor.data.materials.append(b.m['caliper'])
            for face in rotor.data.polygons:
                radius=sum(math.hypot(rotor.data.vertices[i].co.y-y,rotor.data.vertices[i].co.z-S.HUB_HEIGHT) for i in face.vertices)/len(face.vertices)
                if radius<.102:face.material_index=1
            b.add(rotor,parent,'brakes')


def prism(b,name,points,z,material,parent):
    return b.add(G.profile(name,[(p.x,p.y) for p in points],z-.0015,z+.0015,material,axis='Z'),parent,'hinges')


def door_hinges(b):
    roof=mesh_tree([bpy.data.objects['Roof']]);posts={}
    for side,sign in [('L',-1),('R',1)]:
        rings=[]
        for z,x,width in [(.18,.72,.054),(.94,.77,.054),(1.38,.64,.054)]:
            ring=[]
            for dx,dy in [(-width/2,-.04),(width/2,-.04),(width/2,.04),(-width/2,.04)]:
                p=Vector((sign*(x+dx),S.DOOR_SPLIT-.005+dy,z))
                if z>1.3:
                    hit=roof.ray_cast(Vector((p.x,p.y,2)),Vector((0,0,-1)),3)[0]
                    if hit is None:raise ValueError('Inner B-post missed its roof support')
                    p.z=hit.z-.0005
                ring.append(p)
            rings.append(ring)
        posts[side]=b.add(G.loft('S240 inner B post '+side,rings,b.m['frame']),category='interior')
    jambs={}
    for side,sign in [('L',-1),('R',1)]:
        section=[(-.030,-.040),(.030,-.040),(.030,.040),(.028,.040),(.028,-.038),(-.028,-.038),(-.028,.040),(-.030,.040)]
        rings=[[(sign*(center+x),cy+y,z) for x,y in section] for center,cy,z in [(.72,S.DOOR_FRONT+.15,.18),(.768,S.DOOR_FRONT-.010,.60),(.768,S.DOOR_FRONT-.010,.92)]]
        jambs[side]=b.add(G.loft('S240 front jamb reinforcement '+side,rings,b.m['frame']),category='interior')
    for side,sign in [('L',-1),('R',1)]:
        for end,front in [('F',S.DOOR_FRONT),('R',S.DOOR_SPLIT)]:
            code=end+side;parent=bpy.data.objects['Door_'+code];axis=parent.matrix_world.translation.copy();door=mesh_tree([bpy.data.objects['Door '+end+'_'+side]])
            for z,label in [(.59,'lower'),(.87,'upper')]:
                direction=Vector(parent['hinge_axis_vehicle']).normalized()
                center=axis+direction*((z-axis.z)/direction.z);name=code+' '+label
                pin=G.cylinder('S240 hinge pin '+name,center-direction*.016,center+direction*.016,.004,b.m['chrome'],12 if b.high else 6)
                b.add(pin,category='hinges')
                count=12 if b.high else 6
                # Circumscribe the bore so its measured minimum ID is 8.4 mm
                # even at game tessellation; the 8 mm pin clears at every pose.
                bore=.0042/math.cos(math.pi/count)
                outer=.006 if end=='F' else .0075
                sleeve=G.lathe('S240 hinge sleeve '+name,[(-.012,outer),(.012,outer),(.012,bore),(-.012,bore)],b.m['frame'],count,closed=True)
                sleeve.location=center;sleeve.rotation_euler=direction.to_track_quat('Z','Y').to_euler();b.add(sleeve,parent,'hinges')
                hit=door.ray_cast(Vector((sign*2,front+.170,z)),Vector((-sign,0,0)),4)[0]
                if hit is None:raise ValueError(('Hinge leaf missed its door',code,z))
                hit.x-=sign*.0008
                prism(b,'S240 hinge moving leaf '+name,[center+Vector((-sign*.0045,.0025,0)),hit,hit+Vector((-sign*.040,0,0))],z,b.m['frame'],parent)
                if end=='F':
                    y=S.DOOR_FRONT-.005;hit=mesh_tree([jambs[side]]).ray_cast(Vector((sign*2,y,z)),Vector((-sign,0,0)),4)[0]
                    if hit is None:raise ValueError(('Front hinge missed its body support',code,z))
                    hit.x-=sign*.0004
                else:
                    hit=mesh_tree([posts[side]]).ray_cast(Vector((sign*2,S.DOOR_SPLIT-.005,z)),Vector((-sign,0,0)),4)[0]
                    if hit is None:raise ValueError(('Rear hinge missed its B post',code,z))
                    hit.x-=sign*.0004
                prism(b,'S240 hinge fixed leaf '+name,[center+Vector((-sign*.002,-.002,0)),hit,hit+Vector((-sign*.040,0,0))],z-.017,b.m['frame'],b.root)
