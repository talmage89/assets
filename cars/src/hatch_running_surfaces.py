"""Passenger carcass and supported wheel-arch returns, hatch only."""
import math
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from kit import model as G
import hatch_spec as S


def tires(b):
    # Monotone bead-to-crown profile: bulge at the middle of the sidewall,
    # followed by the rounded shoulder and continuous tread crown.
    half=[(.09525,.2286),(.109,.250),(.1125,.273),(.104,.298),(.078,.3125),(0,S.HUB_HEIGHT)]
    profile=[(-x,r) for x,r in half]+[(x,r) for x,r in reversed(half[:-1])]
    for code in ['FL','FR','RL','RR']:
        ob=bpy.data.objects['Tire_'+code];old=ob.data
        full_profile=list(profile)
        selected=list(range(len(profile))) if b.high else ([0,2,5,6,7,8,9,10] if code.endswith('R') else [0,1,2,3,4,5,8,10])
        sampled=[profile[i] for i in selected]
        new=G.lathe('H120 carcass construction',sampled,b.m['tire_'+code[-1]],96 if b.high else 56,axis='X',closed=True)
        ob.data=new.data;bpy.data.objects.remove(new,do_unlink=True)
        if old.users==0:bpy.data.meshes.remove(old)
        # Analytic rotational normals from the section tangent. Blend adjacent
        # section secants; do not hard-split an otherwise smooth rubber torus.
        count=96 if b.high else 56;ns=[]
        for j in selected:
            x,r=full_profile[j]
            a=Vector(full_profile[j-1]);c=Vector(full_profile[(j+1)%len(full_profile)])
            tangent=(c-a).normalized();nx,nr=-tangent.y,tangent.x
            for k in range(count):
                angle=math.tau*k/count;ns.append(Vector((nx,nr*math.cos(angle),nr*math.sin(angle))))
        for e in ob.data.edges:e.use_edge_sharp=False
        ob.data.shade_smooth();ob.data.normals_split_custom_set([ns[l.vertex_index] for l in ob.data.loops])
        ob['passenger_profile']=True;ob['tire_size']='225/40R18'
        ob['rolling_radius_m']=S.HUB_HEIGHT;ob['nominal_radius_m']=S.TIRE_RADIUS


def arches(b):
    for side,sign in [('L',-1),('R',1)]:
        for end,axle in [('F',S.FRONT_AXLE),('R',S.REAR_AXLE)]:
            ob=bpy.data.objects['Arch flange_'+end+side];old=ob.data
            targets=[bpy.data.objects[('Front fender_' if end=='F' else 'Rear quarter_')+side],bpy.data.objects['Front molded fascia' if end=='F' else 'Rear molded fascia']]
            ps=[];fs=[]
            for target in targets:
                start=len(ps);ps.extend(target.matrix_world@v.co for v in target.data.vertices)
                role=target.data.attributes.get('hatch_outer_skin');count=target.get('outer_skin_faces',0)
                fs.extend(tuple(start+i for i in f.vertices) for f in target.data.polygons if (role.data[f.index].value if role else f.index<count))
            from hatch_reference_surface import field
            parent=field()
            tree=BVHTree.FromPolygons(ps,fs);segments=48 if b.high else 24;rings=[[],[]]
            for i in range(segments+1):
                a=-.31+(math.pi+.62)*i/segments;r=S.ARCH_RADIUS+.0006
                y=axle+r*math.cos(a);z=S.HUB_HEIGHT+r*math.sin(a)
                sample=parent((sign*2,y,z),(-sign,0,0))
                if sample is None:continue  # The open arc stops at the actual body hem.
                hit=sample[0]
                # A hem lies behind the painted cut; no unsupported exterior lip.
                p=hit-Vector((sign*.0015,0,0))
                if rings[0] and (p-rings[0][-1]).length<.001:continue
                rings[0].append(p)
                inner=p-Vector((sign*.018,0,0))
                if end=='F':
                    rr=math.hypot(inner.y-axle,inner.z-S.HUB_HEIGHT)
                    inner.y=axle+(inner.y-axle)*(rr+.006)/rr;inner.z=S.HUB_HEIGHT+(inner.z-S.HUB_HEIGHT)*(rr+.006)/rr
                rings[1].append(inner)
            if len(rings[0])<8:raise ValueError('Insufficient supported arch samples')
            ob['arch_supported_samples']=len(rings[0]);ob['arch_trimmed_unsupported_samples']=segments+1-len(rings[0])
            count=len(rings[0])
            temp=G.mesh('H120 supported arch hem',rings[0]+rings[1],[(i,i+1,count+i+1,count+i) for i in range(count-1)],b.m['body'])
            mod=temp.modifiers.new('Hem gauge','SOLIDIFY');mod.thickness=.001;mod.offset=-1;mod.use_even_offset=False;G.apply(temp)
            temp.data.transform(ob.matrix_world.inverted());ob.data=temp.data;bpy.data.objects.remove(temp,do_unlink=True)
            if old.users==0:bpy.data.meshes.remove(old)
            G.smooth(ob,55);ob['supported_arch_return']=True



def liners(b):
    """Keep the molded lining inside the fascia's measured lower tuck.

    An outboard constant was wider than the lower fascia, exposing a sharp
    sheet edge through paint. Below an open hem, the liner apron continues
    inward using the width at the first actual body surface above it.
    """
    from hatch_reference_surface import field
    parent=field()
    for code in ['FL','FR','RL','RR']:
        ob=bpy.data.objects['Wheelwell_'+code];matrix=ob.matrix_world;inverse=matrix.inverted();sign=-1 if code.endswith('L') else 1
        changed=0;maximum=0
        for v in ob.data.vertices:
            p=matrix@v.co
            if abs(p.x)<.70:continue
            sample=parent((sign*2,p.y,p.z),(-sign,0,0))
            if sample is None:
                for j in range(1,41):
                    sample=parent((sign*2,p.y,p.z+j*.005),(-sign,0,0))
                    if sample is not None:break
            if sample is None:raise ValueError('No parent support width for liner apron '+code)
            target=min(abs(p.x),abs(sample[0].x)-.020)
            if target<abs(p.x)-1e-7:
                maximum=max(maximum,abs(p.x)-target);p.x=sign*target;v.co=inverse@p;changed+=1
        ob.data.update();G.smooth(ob,55)
        ob['liner_tuck_samples']=changed;ob['liner_tuck_max_m']=maximum
        print('H120_LINER_TUCK',code,changed,maximum,flush=True)
