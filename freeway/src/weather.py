"""Placement-owned age. Coarse causes persist in glTF COLOR_0 and decal UVs."""
import math,random
from mathutils import Vector
import geom as Q
from plan import *
from textures import rect


def road_tint(p,s,u):
    side=1 if u>0 else -1;lane=min(range(2),key=lambda k:abs(u-p.lane(side,k)));d=u-p.lane(side,lane)
    # Water and rubbing change the wheel tracks; engine drips occupy the center.
    # Bounded station modulation breaks the marks at maintenance/traffic history.
    traveled=.68+.18*math.sin(s/21+lane*3+side*1.7)+.09*math.sin(s/7.7+p.seed*.37+side*.8)
    wheel=max(math.exp(-((d-.82)/.31)**4),math.exp(-((d+.82)/.31)**4))
    oil=math.exp(-(d/.16)**2)*(.60+.35*math.sin(s/8.1+side*.9+lane*1.2)**2)
    use=.25*wheel*traveled+.16*oil
    if abs(d)>LANE_HALF:return (1,1,1,1)
    return (1-use,1-use*1.04,1-use*1.12,1)
LANE_HALF=1.80


def decal(b,points,kind,tint=(1,1,1,1),reverse=False):
    u0,v0,u1,v1=rect(kind);uv=[(u0,v0),(u1,v0),(u1,v1),(u0,v1)]
    if reverse:uv=[(u1,v1),(u0,v1),(u0,v0),(u1,v0)]
    b.surface(points,'Maintenance',uv=uv,tint=tint)


def paving(p):
    from roads import seq
    rt=Q.root('CausalPavementAge',module_kind='decals');b=Q.Batch('Repairs sealants ghosts tire contacts',rt);rng=random.Random(p.seed+991);events=[]
    def patch(s0,s1,u0,u1,kind,tint=(1,1,1,1)):
        decal(b,[p.xyz(s0,u0,.012),p.xyz(s0,u1,.012),p.xyz(s1,u1,.012),p.xyz(s1,u0,.012)],kind,tint,reverse=rng.random()<.5)
    for side in (-1,1):
        for lane in range(2):
            u=p.lane(side,lane)
            for j in range(-round(p.length/2/JOINT),round(p.length/2/JOINT)):
                s=j*JOINT
                if p.pavement=='Concrete' and rng.random()<.32:
                    lo=u+rng.uniform(-1.55,.8);width=rng.uniform(.35,1.4);patch(s-.16,s+.16,lo,lo+width,'spall');events.append(('joint_spall',s,u))
                if rng.random()<.025:
                    # Full-depth repair respects the slab boundaries, with a
                    # perimeter seal; scene-owned phase prevents repeated age.
                    if p.pavement=='Concrete':
                        patch(s+.02,s+JOINT-.02,u-1.79,u+1.79,'repair',(.93,.93,.91,1))
                    else:
                        # A maintained asphalt lane gets darker asphalt, not
                        # the pale concrete-repair chart used by the JPCP.
                        b.surface([p.xyz(s+.02,u-1.79,.003),p.xyz(s+.02,u+1.79,.003),p.xyz(s+JOINT-.02,u+1.79,.003),p.xyz(s+JOINT-.02,u-1.79,.003)],'Asphalt',tint=(.68,.68,.67,1))
                    events.append(('full_depth_repair',s,u))
                if rng.random()<.055:patch(s-1,s+2,u-.05,u+.05,'oil')
            # The prior dashed stripe is offset a few inches after re-striping.
            boundary=side*(p.median/2+LEFT+LANE)
            for s in seq(-p.length/2,p.length/2-4,CYCLE):
                if rng.random()<.55:patch(s,s+DASH,boundary+.12,boundary+.28,'ghost')
            for j in range(8):
                s=rng.uniform(-p.length*.45,p.length*.45);offset=rng.uniform(-.9,.9);width=rng.uniform(.25,.50);patch(s,s+rng.uniform(1,3.2),u+offset-width/2,u+offset+width/2,'crack')
        # Shoulder crack seals and silt belong outside the driving edge.
        for j in range(40):
            s=rng.uniform(-p.length*.48,p.length*.48);u=side*(p.edge-rng.uniform(.3,2.5))
            patch(s,s+rng.uniform(1,6),u-.3,u+.3,rng.choice(['seal','crack','silt']))
        if p.kind=='diamond':
            for j in range(5):
                # Gore approach braking/rubber migration, away from through-lane oil.
                s=-side*(270-j*8);u=side*(10.4+j*.48)
                patch(s,s+7,u-.12,u+.12,'rubber')
    if p.pavement=='Concrete':
        # A later asphalt overlay replaces the wearing surface in one stretch;
        # painted lane geometry remains above it. The source joints stay below.
        for a,c in zip(seq(310,390,4.572),seq(310,390,4.572)[1:]):
            for side in (-1,1):
                m=side*(p.median/2+LEFT);e=side*(p.edge-RIGHT)
                b.surface([p.xyz(a,m,.002),p.xyz(a,e,.002),p.xyz(c,e,.002),p.xyz(c,m,.002)],'Asphalt',tint=(.77,.77,.74,1))
        events.append(('asphalt_overlay',310,390))
    # Ground-lodged litter, discarded carcasses and rooted weeds accumulate at
    # barrier/fence traps, never uniformly across travel lanes.
    for side in (-1,1):
        for j in range(75):
            s=rng.uniform(-p.length*.49,p.length*.49);u=side*(.55 if p.kind=='diamond' else p.edge+.40)
            pt=Vector(p.xyz(s,u,.025));w=rng.uniform(.05,.14);h=rng.uniform(.12,.25)
            decal(b,[(pt.x-w,pt.y-h,pt.z),(pt.x+w,pt.y-h,pt.z+.018),(pt.x+w,pt.y+h,pt.z),(pt.x-w,pt.y+h,pt.z+.035)],'litter')
        for j in range(35):
            s=round(rng.uniform(-p.length*.48,p.length*.48)/6.096)*6.096
            u=side*(.44 if p.kind=='diamond' else p.median/2-.7)
            q=Vector(p.xyz(s,u,.01 if p.kind=='diamond' else -.22));h=rng.uniform(.09,.24)
            for k in range(3):
                dx=rng.uniform(-.05,.05);dy=rng.uniform(-.06,.06)
                b.face([(q.x+dx-.05,q.y+dy,q.z+h*.3),(q.x+dx+.04,q.y+dy+.02,q.z+h*.45),(q.x+dx,q.y+dy+.04,q.z+h)],'Lawn',tint=(.43,.54,.27,1))
        for s in (-117+side*21,278+side*37):
            pt=Vector(p.xyz(s,side*(p.edge+.42),-.07));b.tube([pt,pt+Vector((0,0,.20))],.30,'Rubber',12,caps=False)
    b.finish();rt['weather_events_json']=__import__('json').dumps(events);return rt


def construction(root):
    """Wet joints, low splash, bearing seats and drain lines tint native material.

    Each batch has per-face vertices. Local sample grids retain the causal
    field at actual surface locations instead of smearing it over whole boxes.
    """
    if root.get('bridge_weather_complete'):return
    if root.get('module_kind')=='bridge':
        import bpy
        bpy.context.view_layer.update()
    for ob in root.children_recursive:
        if ob.type!='MESH':continue
        roles=[m for m in ob.data.materials]
        if not any(m in (Q.M['Bridge'],Q.M['Barrier'],Q.M['Steel']) for m in roles):continue
        ob.data=ob.data.copy();ca=ob.data.color_attributes.get('Tint')
        if not ca:continue
        for face in ob.data.polygons:
            ma=ob.data.materials[face.material_index]
            if ma not in (Q.M['Bridge'],Q.M['Barrier'],Q.M['Steel']):continue
            for i in face.vertices:
                v=ob.data.vertices[i].co
                low=math.exp(-max(0,v.z)/.22)*(.08+.16*(.5+.5*math.sin(v.y*2.3+root.location.y*.7))) if root.get('module_kind') in ('barrier','soundwall') else 0
                value=1-low
                if ma==Q.M['Steel'] and root.get('module_kind')=='guardrail':
                    value=1.0 if ob.get('maintenance') else .86
                if root.get('module_kind')=='bridge' and ob.parent and ob.parent.get('module_kind')=='bridge_girder':
                    p=root.matrix_world.inverted()@ob.matrix_world@v
                    if abs(p.y)>8.7:
                        drain=math.exp(-((abs(p.x)-16)/.55)**2)
                        joint=math.exp(-((abs(p.x)-.2)/.7)**2)+math.exp(-((abs(p.x)-23.8)/.7)**2)
                        fall=math.exp(-max(0,7.15-p.z)/1.7)
                        value-=.26*drain*fall+.20*min(1,joint)*fall
                ca.data[i].color=(value,value*.995,value*.98,1)
    if root.get('module_kind')!='bridge':return
    b=Q.Batch('Joint bearing and scupper deposits',root)
    # Outer girder faces face the freeway shoulder. Runoff is top-connected,
    # with calcite discharge below each actual scupper, and staining at joints.
    for side in (-1,1):
        profile=[(.3302,5.7284),(.3302,5.9316),(.1016,6.1602),(.1016,6.7444),(.254,6.8968),(.254,7.10)]
        for x in (-23.0,-16,-.6,.6,16,23.):
            kind='salts' if abs(x)==16 else 'runoff';width=.48 if kind=='salts' else .75
            u0,v0,u1,v1=rect(kind)
            for (ua,za),(uc,zc) in zip(profile,profile[1:]):
                ya=side*(9.144+ua+.0018);yc=side*(9.144+uc+.0018)
                h=.018*math.sin(math.pi*max(0,min(1,(abs(x)-.16)/23.82)))
                pts=[(x-width,ya,za+h),(x+width,ya,za+h),(x+width,yc,zc+h),(x-width,yc,zc+h)]
                va=v0+(za-5.7284)/1.3716*(v1-v0);vc=v0+(zc-5.7284)/1.3716*(v1-v0)
                uv=[(u0,va),(u1,va),(u1,vc),(u0,vc)]
                if side>0:pts.reverse();uv.reverse()
                b.face(pts,'Maintenance',uv=uv)
    for side in (-1,1):
        for y in (-9.144,-6.096,-3.048,0,3.048,6.096,9.144):
            u0,v0,u1,v1=rect('runoff');x=side*1.152
            pts=[(x,y-.35,4.40),(x,y+.35,4.40),(x,y+.35,5.435),(x,y-.35,5.435)];uv=[(u0,v0),(u1,v0),(u1,v1),(u0,v1)]
            if side<0:pts.reverse();uv.reverse()
            b.face(pts,'Maintenance',uv=uv)
    # Fresh formed repairs use the same concrete manufacture, without a tar
    # perimeter intended for paving. Their irregular boundary follows the column.
    for row,(y,z) in enumerate([(-7,3.2),(0,2.1),(7,3.65)]):
        rng=random.Random(517+row)
        lower=[z-.28+rng.uniform(-.045,.045) for j in range(9)]
        upper=[z+.28+rng.uniform(-.035,.035) for j in range(9)]
        for j in range(8):
            a=-.52+1.04*j/8;c=-.52+1.04*(j+1)/8
            xa,ya=.6008*math.sin(a),y-.6008*math.cos(a);xc,yc=.6008*math.sin(c),y-.6008*math.cos(c)
            b.face([(xa,ya,lower[j]),(xc,yc,lower[j+1]),(xc,yc,upper[j+1]),(xa,ya,upper[j])],'Bridge',tint=(.88,.885,.89,1))
    b.finish()
    root['bridge_weather_complete']=True
