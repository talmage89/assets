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
        old=bpy.data.objects['Wheel center_'+code];bpy.data.objects.remove(old,do_unlink=True)
        count=32 if b.high else 16
        bore=.0352/math.cos(math.pi/count)
        profile=[(.029,bore),(.029,.065),(.079,.065),(.090,.052),(.090,0),(.086,0),(.086,bore)]
        hub=G.lathe('Wheel center_'+code,[(cx+sign*x,r) for x,r in profile],b.m['wheel'],count,axis='X',center=(y,S.HUB_HEIGHT),closed=True)
        b.add(hub,parent,'wheels')
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
            if b.high:
                lug=G.lathe('S240 wheel stud '+code+str(k),[(cx+sign*x*axial,r) for x,r in profile],b.m['chrome'],6,axis='X',center=(cy,cz))
            else:
                outline=[(cy+.011*math.cos(math.tau*j/6),cz+.011*math.sin(math.tau*j/6)) for j in range(6)]
                lug=G.profile('S240 wheel stud '+code+str(k),outline,min(cx+sign*.090,cx+sign*.105),max(cx+sign*.090,cx+sign*.105),b.m['chrome'],axis='X')
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
    # The cap seats on the continuous roof stamping and its structural rail;
    # the modeling/material partition is not a physical support boundary.
    roof=mesh_tree([bpy.data.objects[n] for n in ['Roof','Greenhouse_L','Greenhouse_R']]);posts={}
    for side,sign in [('L',-1),('R',1)]:
        rings=[]
        for z,x,width in [(.18,.72,.054),(.94,.77,.054),(1.38,.64,.054)]:
            ring=[]
            for dx,dy in [(-width/2,-.05),(width/2,-.05),(width/2,.05),(-width/2,.05)]:
                p=Vector((sign*(x+dx),S.DOOR_SPLIT-.005+dy,z))
                if z>1.3:
                    hit=roof.ray_cast(Vector((p.x,p.y,2)),Vector((0,0,-1)),3)[0]
                    if hit is None:
                        # The outer corner meets the sloping roof rail beyond
                        # the door's drain gap. Seat the cap radially on that
                        # actual steel, rather than aiming vertically through
                        # the gap or extending an unsupported flat cap.
                        origin=Vector((0,p.y,.60));direction=(p-origin).normalized()
                        hit=roof.ray_cast(origin,direction,1.5)[0]
                        if hit is None or (hit-p).length>.025:
                            raise ValueError('Inner B-post missed its roof support')
                        p=hit-direction*.0005
                    else:p.z=hit.z-.0005
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
            # Seat the upper barrel lower on the SAME accepted hinge axis.
            # Its true circular high-source sleeve and 24 mm axial span
            # must clear the newly fair fender's return at every door angle.
            for z,label in [(.59,'lower'),(.85 if end=='F' else .87,'upper')]:
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


def grade_tire(ob,code):
    """Round the visible rubber with 96 chords, grading only concealed rings.

    Both tire sides retain their measured maximum width, beads and crown.
    Extra outer-side profile stations round the shoulder in the oblique macro.
    The transition mesh shares all ring edges, without poles or T junctions.
    """
    segments=S.TIRE_DELIVERY_SEGMENTS
    profile=[Vector((ob.data.vertices[j*segments].co.x,
                     math.hypot(ob.data.vertices[j*segments].co.y,ob.data.vertices[j*segments].co.z)))
             for j in range(9)]
    counts=[16,16,48,96,96,96,96,32,16]
    if code.endswith('L'):counts=list(reversed(counts))
    starts=[];vertices=[];faces=[]
    for (x,r),num in zip(profile,counts):
        starts.append(len(vertices))
        vertices.extend((x,r*math.cos(math.tau*k/num),r*math.sin(math.tau*k/num)) for k in range(num))
    for ring in range(len(counts)):
        other=(ring+1)%len(counts);a,c=counts[ring],counts[other];i=j=0
        while i<a or j<c:
            va=starts[ring]+i%a;vc=starts[other]+j%c
            if (i+1)*c==(j+1)*a:
                faces.append((va,starts[ring]+(i+1)%a,starts[other]+(j+1)%c,vc));i+=1;j+=1
            elif (i+1)*c<(j+1)*a:
                faces.append((va,starts[ring]+(i+1)%a,vc));i+=1
            else:
                faces.append((va,starts[other]+(j+1)%c,vc));j+=1
    old=ob.data;me=bpy.data.meshes.new('S240 graded radial carcass');me.from_pydata(vertices,[],faces);me.update()
    for mat in old.materials:me.materials.append(mat)
    ob.data=me
    # Axis-X sweep winding follows the ordered bead -> crown -> bead profile.
    me.update();ob['s240_tire_ring_counts']=counts
    ob['tread_chord_sag_m']=S.HUB_HEIGHT*(1-math.cos(math.pi/96))
    if old.users==0:bpy.data.meshes.remove(old)


def tire_normals(b):
    """Continuous carcass normals; profile rings are rubber curvature, not creases."""
    for code in ['FL','FR','RL','RR']:
        ob=bpy.data.objects['Tire_'+code];me=ob.data;segments=96 if b.high else S.TIRE_DELIVERY_SEGMENTS
        counts=list(ob.get('s240_tire_ring_counts',[segments]*(len(me.vertices)//segments)))
        starts=[];ring_for=[]
        for ring,num in enumerate(counts):starts.append(len(ring_for));ring_for.extend([ring]*num)
        rings=len(counts)
        profile=[Vector((me.vertices[i].co.x,math.hypot(me.vertices[i].co.y,me.vertices[i].co.z))) for i in starts]
        tangents=[]
        for j in range(rings):
            a=profile[max(0,j-1)];c=profile[min(rings-1,j+1)]
            tangents.append((c-a).normalized())
        for edge in me.edges:edge.use_edge_sharp=False
        normals=[]
        for face in me.polygons:
            face.use_smooth=True;closing=any(ring_for[i]==0 for i in face.vertices) and any(ring_for[i]==rings-1 for i in face.vertices)
            for li in face.loop_indices:
                vi=me.loops[li].vertex_index;p=me.vertices[vi].co;r=math.hypot(p.y,p.z);dx,dr=tangents[ring_for[vi]]
                normal=Vector((0,-p.y/r,-p.z/r)) if closing else Vector((-dr,dx*p.y/r,dx*p.z/r)).normalized()
                normals.append(normal)
        me.normals_split_custom_set(normals)
