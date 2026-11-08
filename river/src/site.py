"""Approaches, connected paths, outfalls, floodwall and bank-card planting."""
import math
import random
import geometry as G
from channel import surface_z


def road(p,parent):
    b=G.Batch('ApproachRoadAndWalks',parent,'site')
    for side in (-1,1):
        a=side*p.length/2;c=side*145
        for y0,y1 in ((-3.3528,0),(0,3.3528)):
            b.geom([(x,y,p.deck_z-.02*abs(y)) for x,y in ((a,y0),(c,y0),(c,y1),(a,y1))],[(0,1,2,3)],'asphalt',up=True)
        for s in (-1,1):
            b.box(((a+c)/2,s*4.2672,p.deck_z+.009144),(abs(c-a),1.524,.1524))
    # Road-paint module is Ground's existing worn paint chart (bound below).
    for y in (-.0762,.0762):
        b.geom([(-145,y-.05,p.deck_z+.002),(145,y-.05,p.deck_z+.002),(145,y+.05,p.deck_z+.002),(-145,y+.05,p.deck_z+.002)],[(0,1,2,3)],'paint_yellow')
    for y in (-3.18,3.18):
        b.geom([(-145,y-.05,p.deck_z-.02*abs(y)+.003),(145,y-.05,p.deck_z-.02*abs(y)+.003),(145,y+.05,p.deck_z-.02*abs(y)+.003),(-145,y+.05,p.deck_z-.02*abs(y)+.003)],[(0,1,2,3)],'paint_white')
    b.finish()


def fixtures(p,parent):
    rt=G.root('BankPublicWorks',parent=parent)
    b=G.Batch('FloodwallTrailAndAccess',rt,'site');trail=[]
    for i in range(150):
        y=-150+i*2;yy=y+2
        edge=lambda v:p.center(v)-p.halfwidth(v)
        x=edge(y);xx=edge(yy)
        if p.kind=='downtown':
            # Riverwalk below Main Street with 6m poured bays and a real cap.
            b.geom([(x-1,y,-.3),(xx-1,yy,-.3),(xx-1,yy,.65),(x-1,y,.65)],[(0,1,2,3)],'concrete',(.63,.64,.60,1))
            b.geom([(x-1.12,y,.65),(xx-1.12,yy,.65),(xx-4.2,yy,.65),(x-4.2,y,.65)],[(0,1,2,3)],'concrete',(.80,.80,.75,1))
            wall_top=.65 if abs((y+yy)/2)<8 or -82<(y+yy)/2<-80 else 3.70
            opening=next((oy for oy in (-33,59) if y<oy<yy),None)
            if opening is None:
                b.geom([(x-4.2,y,.50),(xx-4.2,yy,.50),(xx-4.2,yy,wall_top),(x-4.2,y,wall_top)],[(0,1,2,3)],'concrete',(.65,.65,.60,1))
            else:
                # Radial frame quads leave a real circular aperture in the
                # retaining face; the culvert's hollow barrel meets its rim.
                inner=[];outer=[];oz=1.22;r=.4318
                angles=sorted(set([k*math.tau/20 for k in range(20)]+[
                    math.atan2(zz-oz,v-opening)%math.tau for v in (y,yy) for zz in (.50,wall_top)]))
                for a in angles:
                    dy,dz=math.cos(a),math.sin(a)
                    limits=[]
                    if abs(dy)>1e-8:limits.append(((yy if dy>0 else y)-opening)/dy)
                    if abs(dz)>1e-8:limits.append(((wall_top if dz>0 else .50)-oz)/dz)
                    t=min(limits)
                    for ring,rr in ((inner,r),(outer,t)):
                        v=opening+dy*rr;ring.append((edge(v)-4.2,v,oz+dz*rr))
                for k in range(len(angles)):
                    c=(k+1)%len(angles);b.geom([inner[c],inner[k],outer[k],outer[c]],[(0,1,2,3)],'concrete',(.65,.65,.60,1))
            b.geom([(x-4.03,y,wall_top+.025),(xx-4.03,yy,wall_top+.025),(xx-4.55,yy,wall_top+.025),(x-4.55,y,wall_top+.025)],[(0,1,2,3)],'concrete',(.72,.72,.67,1))
            trail.append((x-2.6,y,.65))
            if abs(y)>9:
                b.cylinder((x-1.2,y,1.15),.024,1,'steel',8,caps=False)
                for z in (.80,1.65):b.tube([(x-1.2,y,z),(xx-1.2,yy,z)],.022,'steel',6,caps=i in (0,149))
                for j in range(1,18):
                    t=j/18;bx=(1-t)*x+t*xx-1.2
                    b.beam((bx,y+2*t,.80),(bx,y+2*t,1.65),.019,role='steel',caps=False)
        else:
            x-=7;xx-=7;z=p.bed(x,y)+.035;zz=p.bed(xx,yy)+.035
            if abs(y)>12:
                b.geom([(x-1,y,z),(xx-1,yy,zz),(xx+1,yy,zz),(x+1,y,z)],[(0,1,2,3)],'bank',(.93,.90,.82,1))
            trail.append((x,y,z))
    # 30in storm drain through a concrete endwall. The opening has no disk.
    for y in (-33,59):
        x=p.center(y)+p.halfwidth(y)*1.13;z=p.bed(x,y)
        if p.kind=='downtown':x=p.center(y)+p.halfwidth(y)+4.20;z=.64
        b.box((x+.1,y,z+.1),(.35,2.1,.25))
        for side in (-1,1):b.box((x+.1,y+side*.65,z+.68),(.35,.40,1.15))
        b.box((x+.1,y,z+1.20),(.35,1.7,.22))
        rings=[[(xx,y+r*math.cos(k*math.tau/20),z+.58+r*math.sin(k*math.tau/20)) for k in range(20)] for xx,r in ((x+.65,.4318),(x-.12,.4318),(x-.12,.381),(x+.65,.381))]
        b.loft(rings,'concrete',caps=False)
    if p.kind=='edge':
        # Small worn fishing landing and 12%-slope boat launch into shallow edge.
        y=-36;x=p.center(y)-p.halfwidth(y)
        b.geom([(x-18,y-2,2.10),(x-18,y+2,2.10),(x+.8,y+2,-.12),(x+.8,y-2,-.12)],[(0,1,2,3)],'concrete',(.66,.65,.58,1))
        G.root('BoatLaunch',(x-5,y,2.10-2.22*13/18.8),rt,socket_kind='launch')
        fy=33;fx=p.center(fy)-p.halfwidth(fy)
        G.root('FishingSpot',(fx-2,fy+5,surface_z(p,fx-2,fy+5)+.02),rt,socket_kind='fishing')
    ob=b.finish()
    if p.kind=='downtown':
        # Matching opposite riverwalk/floodwall follows the bent channel,
        # rather than leaving one suburban lawn across the town river.
        right=ob.copy();right.data=ob.data.copy();right.name='OppositeFloodwallTrail'
        import bpy
        bpy.context.collection.objects.link(right);right.parent=rt
        for v in right.data.vertices:v.co.x=2*p.center(v.co.y)-v.co.x
        import bmesh
        bm=bmesh.new();bm.from_mesh(right.data);bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(right.data);bm.free()
    G.path('RiverbankTrail',trail,rt,'walk')
    from wall_details import add
    add(p,rt)
    return rt


def plants(p,parent):
    import bpy
    rng=random.Random(p.seed+18);templates=[]
    for k in range(16):
        b=G.Batch('BankColonyTemplate_'+str(k),parent,'vegetation')
        a=(k%4)/4;c=(1-k//4%2)/4
        uv=[(a+.002,c+.002),(a+.248,c+.002),(a+.248,c+.248),(a+.002,c+.248)]
        for j in range(3):
            angle=j*math.pi/3+k*.19;dx=math.cos(angle)*.40;dy=math.sin(angle)*.40
            b.geom([(-dx,-dy,-.02),(dx,dy,-.02),(dx+.09,dy,1),(-dx+.09,-dy,1)],[(0,1,2,3)],'plants',uv=uv)
        ob=b.finish();templates.append(ob)
    # Dense low colonies, wide enough to read as cover; no lone wire tufts.
    for i in range(22000):
        y=rng.uniform(-149,149);side=(-1,1)[i%2]
        if abs(y)<8:continue
        u=side*rng.uniform(1.0,1.47)
        if p.kind=='downtown' and side<0:continue
        x=p.center(y)+u*p.halfwidth(y);z=surface_z(p,x,y)
        if p.kind=='edge':
            if side<0 and abs(x-(p.center(y)-p.halfwidth(y)-7))<1.15:continue
            ramp_edge=p.center(-36)-p.halfwidth(-36)
            if abs(y+36)<2.15 and ramp_edge-18.1<x<ramp_edge+.9:continue
        if z<.03 or z>2.8:continue
        if math.sin(y*.13+u*19)+math.sin(y*.33-u*8)<-.9:continue
        # Colonies thin into water rather than stopping in a solid dark row.
        if z<.22 and rng.random()<.55:continue
        reed=z<.65 and i%3==0;h=rng.uniform(.55,1.15) if reed else rng.uniform(.15,.45)
        w=rng.uniform(.35,.65) if reed else rng.uniform(.55,.95)
        k=rng.randrange(6,8) if reed else rng.randrange(6)
        ob=templates[k+(8 if i%2 else 0)].copy();ob.name='Bank colony '+str(i)
        bpy.context.collection.objects.link(ob);ob.location=(x,y,z);ob.scale=(w/.8,w/.8,h);ob.rotation_euler.z=rng.uniform(0,6.28)
        ob['river_instance']='bank_colony'
    for ob in templates:bpy.data.objects.remove(ob,do_unlink=True)
