"""Outward-arching low stem clusters with opposite leaves and terminal mopheads."""
import math,random
from mathutils import Vector,Quaternion
from kit import botany
from hydrangea_atlas import LEAF_RECTS,FLOWER_RECTS


def bezier(ctrl,t):
    a,b,c,d=map(Vector,ctrl);return a*(1-t)**3+b*(3*t*(1-t)**2)+c*(3*t*t*(1-t))+d*t**3


def generate(images,bark,seed=815):
    from kit.foliage import material
    rng=random.Random(seed);mat=material(images['BaseColor'],images['Normal'],images['ORM'],name='Hydrangea thin leaves and sepals',specular=.12,transmission=.15,normal_strength=.90,back_multiplier=(1.12,1.10,1.16,1),back_saturation=.84)
    cards=botany.Cards();stems=[];heads=[];leaves=[];wood=[];paths=[];terminals=[]
    def add_stem(pts,radius,parent=-1,sides=4):
        i=len(stems);radii=[radius*(1-.79*t/(len(pts)-1)) for t in range(len(pts))]
        ob=botany.sweep(f'Hydrangea stem {i:02}',pts,radii,bark,sides=sides,phase=i*.37)
        owner=ob.data.attributes.new(name='GrowthPart',type='INT',domain='FACE')
        for value in owner.data:value.value=i
        wood.append(ob);stems.append(dict(points=[list(p) for p in pts],radii=radii,parent=parent,sides=sides,level=1 if parent<0 else 2,phase=rng.random()));paths.append(pts);return i
    def pair(stem,t,node):
        pts=paths[stem];x=t*(len(pts)-1);j=min(int(x),len(pts)-2);anchor=pts[j].lerp(pts[j+1],x-j)-Vector((0,0,.002))
        az=math.atan2(anchor.y,anchor.x)
        for side in (-1,1):
            a=az+side*(.62 if node%2==0 else 1.35)+rng.uniform(-.34,.34)
            axis=Vector((math.cos(a),math.sin(a),rng.uniform(-.32,.26))).normalized()
            norm=Vector((-.1*math.cos(a),-.1*math.sin(a),1)).normalized();u=axis.cross(norm).normalized();u=Quaternion(axis,rng.uniform(-.56,.56))@u;norm=u.cross(axis).normalized()
            length=rng.uniform(.126,.170);width=length*rng.uniform(.74,.88);start=anchor
            # Physical cross-blade cup and drooping tip. Only four triangles per
            # blade; analytic pinnate ribs/teeth supply the smaller-scale form.
            grid=[[start+u*(gx*width/2)+axis*(gy*length)+norm*(width*.12*abs(gx)-length*.22*gy) for gx in (-1,0,1)] for gy in (0,1)]
            tile=0
            cards.add_grid(grid,LEAF_RECTS[tile],(min(1,anchor.z/1.2),.75,stems[stem]['phase'],rng.uniform(.5,.85)))
            leaves.append(dict(stem=stem,node=node,opposite_side=side,anchor_m=list(anchor),tile_length_m=length,expected_blade_length_m=length*.865))
    # Seven loose stem families; outer stems sweep low and carry low flowers.
    for i in range(22):
        az=i*2.3999632297+.16
        reach=(rng.uniform(.20,.40) if i<7 else rng.uniform(.48,.63))*1.05
        height=rng.uniform(.98,1.08) if i<7 else rng.uniform(.57,.87)
        tip=Vector((math.cos(az)*reach,math.sin(az)*reach,height));base=Vector((math.cos(az)*rng.uniform(.025,.09),math.sin(az)*rng.uniform(.025,.09),0))
        ctrl=[base,Vector((tip.x*.94,tip.y*.94,.24)),Vector((tip.x*1.03,tip.y*1.03,tip.z+.04)),tip]
        pts=[bezier(ctrl,t/4) for t in range(5)];idx=add_stem(pts,rng.uniform(.0042,.0063))
        terminals.append(dict(stem=idx,tip=tip,az=az,nodding=i%4==0,bloom=i%4!=3))
        for node in range(6):pair(idx,.16+node*.141,node)
    # Low daughters fill leaf masses between the taller flowering stems.
    for i in range(18):
        parent=i%22;pp=paths[parent];t=rng.uniform(.22,.34) if i%2==0 else rng.uniform(.48,.63);xx=t*4;jj=min(int(xx),3);base=pp[jj].lerp(pp[jj+1],xx-jj);az=math.atan2(pp[-1].y,pp[-1].x)+rng.choice((-1,1))*.42
        tip=Vector((math.cos(az)*rng.uniform(.48,.60),math.sin(az)*rng.uniform(.48,.60),rng.uniform(.27,.51) if i%2==0 else rng.uniform(.67,.94)))
        pts=[base,base.lerp(tip,.55)+Vector((0,0,.045)),tip];idx=add_stem(pts,.0031,parent=parent,sides=3)
        for node,t in enumerate((.28,.56,.85)):pair(idx,t,node)
    core_clusters=[]
    for stem,pts in enumerate(paths):
        stations=(.35,.56,.74) if stem<22 else (.40,.68)
        for t in stations:
            x=t*(len(pts)-1);j=min(int(x),len(pts)-2);anchor=pts[j].lerp(pts[j+1],x-j)-Vector((0,0,.002))
            tangent=(pts[j+1]-pts[j]).normalized();az=math.atan2(anchor.y,anchor.x)
            side=Vector((-math.sin(az),math.cos(az),0));axis=(tangent+Vector((math.cos(az)*.2,math.sin(az)*.2,0))).normalized()
            n=side.cross(axis).normalized();normals=(n,axis.cross(n).normalized())
            for nn in normals:
                seed=Vector((0,0,1)) if abs(nn.z)<.95 else Vector((1,0,0));bu=nn.cross(seed).normalized();bv=nn.cross(bu).normalized()
                roll=math.atan2(-axis.dot(bu),axis.dot(bv));c=anchor+axis*.05
                reach=math.hypot(c.x,c.y)
                if reach>.32:c.x*=.32/reach;c.y*=.32/reach
                c.z=max(.25,min(.74,c.z))
                cards.add(c,nn,roll,.36,LEAF_RECTS[1],(0,0,.56),(min(1,anchor.z/1.2),.75,stems[stem]['phase'],.65),normal_bend=.25,clump_center=anchor,clump_blend=.8)
            core_clusters.append(dict(stem=stem,anchor_m=list(anchor),opposite_blades_per_card=6,cards=2))
    for term in terminals:
        if not term['bloom']:continue
        i=term['stem'];az=term['az'];nod=term['nodding'];tip=term['tip']
        normal=Vector((math.cos(az)*(.72 if nod else .18),math.sin(az)*(.72 if nod else .18),.82 if nod else 1)).normalized()
        radius=rng.uniform(.080,.094);hc=tip+normal*.012-Vector((0,0,.002));tile=0 if i%5 else 1
        if i in (5,16):tile=2
        q=Vector((0,0,1)).rotation_difference(normal);first=len(cards.faces)
        for f in range(65):
            z=-.98+1.96*(f+.5)/65;a=f*2.3999632297+rng.uniform(-.1,.1)
            n=q@Vector((math.sqrt(1-z*z)*math.cos(a),math.sqrt(1-z*z)*math.sin(a),z))
            pos=hc+n*(radius-.010+rng.uniform(-.005,.005));tilt=Vector((rng.uniform(-.25,.25),rng.uniform(-.25,.25),rng.uniform(-.15,.15)));nn=(n+tilt).normalized()
            cards.add(pos,nn,rng.random()*math.tau,rng.uniform(.062,.068),FLOWER_RECTS[tile],hc,(min(1,hc.z/1.2),1,stems[i]['phase'],.55),normal_bend=.05)
        heads.append(dict(center_m=list(hc),radius_m=radius,stem=i,nodding=nod,normal=list(normal),first_face=first,faces=65))
    return wood,cards.mesh('Hydrangea leaf and flower cards',mat),dict(stems=stems,heads=heads,leaves=leaves,core_clusters=core_clusters)
