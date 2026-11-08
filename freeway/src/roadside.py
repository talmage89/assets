"""Grounded paving interfaces, maintained cut slopes and terminal controls."""
import math,random
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import geom as Q
from plan import *


def soil_tree():
    ob=next(o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('Cut slopes and drainage'))
    bpy.context.view_layer.update();return BVHTree.FromObject(ob,bpy.context.evaluated_depsgraph_get())


def seat(rt,soil):
    """Close exposed paving boundaries with real granular shoulder or curb return.

    Locate the external boundary from actual source faces; ray-sample adjacent
    earth instead of copying a nominal support height. The receipt records it.
    """
    edges={};samples=[]
    for ob in rt.children_recursive:
        if ob.type!='MESH':continue
        for face in ob.data.polygons:
            role=ob.data.materials[face.material_index]
            if role not in (Q.M['Asphalt'],Q.M['Concrete'],Q.M.get('WheelPolish',Q.M['Concrete'])):continue
            pts=[ob.matrix_world@ob.data.vertices[i].co for i in face.vertices]
            if len(pts)<3 or (pts[1]-pts[0]).cross(pts[2]-pts[0]).z<=0:continue
            for a,c in zip(pts,pts[1:]+pts[:1]):
                key=tuple(sorted((tuple(round(v,5) for v in a),tuple(round(v,5) for v in c))))
                edges.setdefault(key,[]).append((a,c,role))
    b=Q.Batch(rt.name+'__SeatedEdges',rt);corners={}
    for entries in edges.values():
        if len(entries)!=1:continue
        a,c,role=entries[0];d=c-a
        if d.xy.length<.03:continue
        outward=Vector((d.y,-d.x,0)).normalized();foot=[]
        width=.55 if role==Q.M['Asphalt'] else .18
        valid=True
        for pt in (a,c):
            q=pt+outward*width;hit=soil.ray_cast(Vector((q.x,q.y,30)),Vector((0,0,-1)),60)[0]
            if hit is None:valid=False;break
            # Embankment meets the pavement thickness, never rises onto its skin.
            hit.z=min(hit.z,pt.z-.025);foot.append(hit)
        if not valid:continue
        b.surface([a,c,foot[1],foot[0]],'Earth' if role==Q.M['Asphalt'] else 'Concrete')
        for top,footpoint in ((a,foot[0]),(c,foot[1])):
            key=tuple(round(v,5) for v in top);corners.setdefault(key,[]).append(footpoint)
        samples.extend([dict(top=list(a),foot=list(foot[0])),dict(top=list(c),foot=list(foot[1]))])
    for key,feet in corners.items():
        if len(feet)==2 and (feet[0]-feet[1]).length>.002:
            top=Vector(key)
            if (feet[0]-top).cross(feet[1]-top).length>1e-8:b.surface([top,feet[0],feet[1]],'Earth')
    b.finish();rt['edge_support_samples']=len(samples)
    return samples


def terminal(p):
    import pieces
    rt=Q.root('TerminalControls',module_kind='terminal_controls');b=Q.Batch('Turn arrows and entrance controls',rt)
    def arrow(x,y,yaw,turn=False):
        # 2009 MUTCD-inspired original straight/left pavement arrow.
        outline=[(-.10,-2),(.10,-2),(.10,.9),(.55,.30),(.72,.47),(0,1.5),(-.72,.47),(-.55,.30),(-.10,.9)]
        if turn:outline=[(-.12,-2),(.12,-2),(.12,.9),(-.75,.9),(-.75,1.3),(-1.4,.65),(-.75,0),(-.75,.4),(-.12,.4)]
        ang=math.radians(yaw)
        points=[(x+u*math.cos(ang)-v*math.sin(ang),y+u*math.sin(ang)+v*math.cos(ang)) for u,v in outline]
        b.surface([(a,c,BRIDGE_Z-.02*abs(c)+.009) for a,c in points],'White')
    for side in (-1,1):
        for y in (-6.7056,6.7056):arrow(side*78-25*(1 if y<0 else -1),y,-90 if y<0 else 90)
        for dx in (-28,28):arrow(side*78+dx,0,-90 if dx<0 else 90,True)
        # Entry path is on the same travel side of the arterial. Back-facing
        # WRONG WAY / DO NOT ENTER pairs discourage the opposite movement.
        for j,(dx,dy,legend,w,h,yaw) in enumerate([
            (6,-side*31,'wrong_way',1.2192,.762,0 if side>0 else 180),
            (-6,-side*22,'wrong',.9144,.9144,0 if side>0 else 180),
            (7,side*23,'entrance',1.524,.9144,180 if side>0 else 0),
            (10,side*26,'route',.6096,.762,180 if side>0 else 0)]):
            r=Q.root(f'Terminal_{side}_Control{j}',(side*78+dx,dy,7.0),rt);r.rotation_euler.z=math.radians(yaw)
            bb=Q.Batch(r.name+'__Post',r);bb.beam((0,0,-.1),(0,0,3.1),.055,'Steel',.055);bb.finish()
            pieces.sign_face(r.name+'__Face',w,h,legend,r,(0,-.04,2.6))
    b.finish();return rt


def landscape(p):
    from roads import seq
    rt=Q.root('RightOfWayMaintenance',module_kind='roadside');b=Q.Batch('Mowing drainage and volunteer growth',rt)
    soil=soil_tree();rng=random.Random(p.seed+987)
    def hit(s,u,lift=.006):
        x,y,_=p.xyz(s,u);a=soil.ray_cast(Vector((x,y,30)),Vector((0,0,-1)),60)[0]
        if a is not None:a.z+=lift
        return a
    for side in (-1,1):
        # Mowing belongs to the graded earth's color field. Separate opaque
        # grass skins intersected its nonplanar slopes and made green triangles.
        for s in seq(-p.length/2+54,p.length/2-54,114):
            # Cast 600mm flumes run down the cut into the actual low ditch.
            begin=p.edge+3 if p.kind=='diamond' else p.edge+2.8;end=begin+max(7,4*(7-p.xyz(s,begin)[2])) if p.kind=='diamond' else 29
            stations=[begin+(end-begin)*j/12 for j in range(13)]
            for lo,hi in zip(stations,stations[1:]):
                pts=[hit(s-.30,side*lo,.028),hit(s+.30,side*lo,.028),hit(s+.30,side*hi,.028),hit(s-.30,side*hi,.028)]
                if all(v is not None for v in pts):b.surface(pts,'Bridge')
            q=hit(s,side*(p.edge+2.2))
            if q is not None:
                b.box((q.x,q.y,q.z-.03),(.78,1.10,.14),'Bridge')
                for k in range(8):b.box((q.x-.29+k*.082,q.y,q.z+.047),(.025,.92,.014),'DarkSteel')
        # Small rooted volunteer stems outside the mowing line. Leaf crowns are
        # native trees in the separate context package; no geometric wire grass.
        for j in range(95):
            s=rng.uniform(-p.length*.49,p.length*.49);u=side*rng.uniform(101,109) if p.kind=='diamond' else side*rng.uniform(37,41)
            q=hit(s,u)
            if q is None:continue
            for k in range(3):
                h=rng.uniform(.18,.65);lean=rng.uniform(-.15,.15)
                b.beam(q,(q.x+lean,q.y+.12,q.z+h),.012,'Wood',.016)
                for z in (.4,.7):
                    b.face([(q.x-.09,q.y,q.z+h*z),(q.x+.08,q.y+.015,q.z+h*z+.07),(q.x+lean,q.y+.03,q.z+h*z+.18)],'Lawn',tint=(.42,.55,.26,1))
    b.finish();return rt
