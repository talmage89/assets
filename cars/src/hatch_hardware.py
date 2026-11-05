"""Five-stud passenger wheels and real concealed door hinge leaves/knuckles."""
import math
import bpy
from mathutils import Vector
from kit import model as G
from hatch_check import mesh_tree
import hatch_spec as S


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
        # preserve the accepted 225 mm sidewall envelope and rolling radius.
        for v in tire.data.vertices:
            radius=math.hypot(v.co.y,v.co.z)
            if b.high and abs(radius-(S.RIM_INCHES*.0254/2+.075*(S.HUB_HEIGHT-S.RIM_INCHES*.0254/2)/(S.TIRE_RADIUS-S.RIM_INCHES*.0254/2)))<.001:
                target=S.RIM_INCHES*.0254/2+.027
                target=S.RIM_INCHES*.0254/2+(target-S.RIM_INCHES*.0254/2)*(S.HUB_HEIGHT-S.RIM_INCHES*.0254/2)/(S.TIRE_RADIUS-S.RIM_INCHES*.0254/2)
                v.co.y*=target/radius;v.co.z*=target/radius;radius=target
            delta=.01425*max(0,min(1,(.2286+.020-radius)/.020))
            v.co.x+=math.copysign(delta,v.co.x)

        for k in range(5):
            angle=math.tau*k/5;cy=y+.05715*math.cos(angle);cz=S.HUB_HEIGHT+.05715*math.sin(angle)
            profile=[(.090,0),(.090,.011),(.102,.011),(.105,.0087),(.105,0)] if b.high else [(.090,0),(.090,.011),(.105,.011),(.105,0)]
            if b.high:
                lug=G.lathe('H120 wheel stud '+code+str(k),[(cx+sign*x*axial,r) for x,r in profile],b.m['chrome'],6,axis='X',center=(cy,cz))
            else:
                outline=[(cy+.011*math.cos(math.tau*j/6),cz+.011*math.sin(math.tau*j/6)) for j in range(6)]
                lug=G.profile('H120 wheel stud '+code+str(k),outline,min(cx+sign*.090,cx+sign*.105),max(cx+sign*.090,cx+sign*.105),b.m['chrome'],axis='X')
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



def game_wheel_allocation(b):
    """Retain visible cast chamfers; spend fewer chords on the inboard barrel."""
    if b.high:return
    for ob in list(bpy.context.scene.objects):
        if ob.name.startswith('Wheel barrel_'):
            code=ob.name[-2:];sign=-1 if code.endswith('L') else 1
            cx=sign*(S.FRONT_TRACK if code.startswith('F') else S.REAR_TRACK)/2
            y=S.FRONT_AXLE if code.startswith('F') else S.REAR_AXLE;r=S.RIM_INCHES*.0254/2
            # The high source retains the buried 12 mm bead-seat return.
            # Game keeps the inboard bearing lip and all outboard contours.
            profile=[(-.093,r-.020),(-.093,r+.005),(.084,r-.008),(.099,r+.006),(.103,r-.015)]
            counts=[16,16,32,32,32];points=[];rings=[];faces=[]
            for (x,rr),count in zip(profile,counts):
                rings.append(list(range(len(points),len(points)+count)))
                points.extend((cx+sign*x,y+rr*math.cos(math.tau*k/count),S.HUB_HEIGHT+rr*math.sin(math.tau*k/count)) for k in range(count))
            for a,c in zip(rings,rings[1:]+rings[:1]):
                if len(a)==len(c):
                    faces.extend((a[i],c[i],c[(i+1)%len(c)],a[(i+1)%len(a)]) for i in range(len(a)))
                elif len(a)*2==len(c):
                    for i in range(len(a)):
                        j=(i+1)%len(a);k=2*i
                        faces.extend([(a[i],c[k],c[k+1]),(a[i],c[k+1],a[j]),(a[j],c[k+1],c[(k+2)%len(c)])])
                else:
                    for i in range(len(c)):
                        j=(i+1)%len(c);k=2*i
                        faces.extend([(a[k],c[i],a[k+1]),(a[k+1],c[i],c[j]),(a[k+1],c[j],a[(k+2)%len(a)])])
            new=G.mesh('H120 allocation',points,faces,b.m['wheel'])
            new.data.transform(ob.matrix_world.inverted());old=ob.data;ob.data=new.data
            bpy.data.objects.remove(new,do_unlink=True)
            if old.users==0:bpy.data.meshes.remove(old)
            G.smooth(ob,35)
