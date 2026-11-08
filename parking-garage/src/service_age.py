"""Seed-owned age from parked engines, turning wheels, leaks and contact.

Eight generic coverage/normal charts are shared. Positions and widths belong
to this assembly, not the reusable tees. No photo or per-seed image enters.
"""
import json,math,random
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import geometry as G
from plan import FLOOR,TEE,SPAN,deck_z
import atlas_binding as A


def floor_surface(root):
    vs=[];fs=[];bpy.context.view_layer.update()
    for ob in root.children_recursive:
        if ob.type!='MESH' or not ob.name.startswith(('Flat_','Ramp_','Grade slab','SpeedRamp','North end grade','Inner closure')):continue
        offset=len(vs);vs.extend(ob.matrix_world@v.co for v in ob.data.vertices);ob.data.calc_loop_triangles()
        for tri in ob.data.loop_triangles:
            if (ob.matrix_world.to_3x3()@tri.normal).z>.7:fs.append(tuple(offset+i for i in tri.vertices))
    return BVHTree.FromPolygons(vs,fs,all_triangles=True)


def placed(root,p,mats):
    rng=random.Random(p['seed']+3717);old=p['system']=='precast';age=1 if old else .65
    G.M['Age']=mats[1];batch=G.Mesh('Cause-driven service history',root);strengths=[];counts={};projection=[]
    surface=floor_surface(root)
    def stamp(pts,key,strength=1,uv=None):
        if uv is None:batch.quad(pts,A.LAYOUT[key]['rect'],'Age')
        else:batch.geom(pts,[(0,1,2,3)],'Age',uv)
        strengths.append(strength);counts[key]=counts.get(key,0)+1
    def floor_mark(x,y,z,w,d,key,strength=1,angle=0):
        ca,sa=math.cos(angle),math.sin(angle);pts=[]
        for u,v in ((-w/2,-d/2),(w/2,-d/2),(w/2,d/2),(-w/2,d/2)):
            xx,yy=x+u*ca-v*sa,y+u*sa+v*ca
            hit=surface.ray_cast(Vector((xx,yy,z+.20)),Vector((0,0,-1)),.4)
            if hit[0] is None:return
            pts.append((xx,yy,hit[0].z+.0012));projection.append(abs(hit[0].z-z))
        stamp(pts,key,strength)
    # Engines leak at different fore/aft positions, never a full row of equal
    # dots. Each vacant stall retains the former car's accumulated history.
    for s in p['stalls']:
        if rng.random()>.84:continue
        sign=-1 if s['yaw']==180 else 1
        for j in range(rng.randint(2,5)):
            x=s['x']+rng.uniform(-.22,.22);y=s['y']+sign*rng.uniform(.3,1.35)
            z=deck_z(p,s['level'],x,y,s['ramp'])
            floor_mark(x,y,z,rng.uniform(.16,.42),rng.uniform(.34,.9),'oil',age*rng.uniform(.5,.9),rng.uniform(-.14,.14))
        if rng.random()<.42:
            xx=s['x']-s['width']/2+.08;yy=s['y']
            floor_mark(xx,yy,s['z'],.12,s['depth']-.3,'scuff',.30*age)
    # Wheel transfer follows actual turning path samples and paired tire
    # positions. It tapers along each arc rather than ringing every deck.
    for path in p['paths']:
        if not path['name'].startswith('Drive_Up_'):continue
        pts=[Vector(v) for v in path['points']]
        totals={-1:0,1:0};distances={-1:0,1:0}
        for a,b in zip(pts,pts[1:]):
            x=(a.x+b.x)/2
            if x<=p['ramp_limits'][0]+.1:totals[-1]+=(b-a).xy.length
            elif x>=p['ramp_limits'][1]-.1:totals[1]+=(b-a).xy.length
        for i,(a,b) in enumerate(zip(pts,pts[1:])):
            mid=(a+b)/2
            if p['ramp_limits'][0]+.1<mid.x<p['ramp_limits'][1]-.1:continue
            tangent=(b-a).xy
            if tangent.length<.06:continue
            group=-1 if mid.x<p['ramp_limits'][0]+.1 else 1
            progress=distances[group]/max(totals[group],.001);end=(distances[group]+tangent.length)/max(totals[group],.001)
            distances[group]+=tangent.length
            u0,v0,u1,v1=A.LAYOUT['rubber']['rect'];vstart=v0+progress*(v1-v0);vend=v0+end*(v1-v0)
            tangent.normalize();side=Vector((-tangent.y,tangent.x,0))
            for offset in (-.78,.78):
                q=[]
                for v in (a+side*(offset-.11),b+side*(offset-.11),b+side*(offset+.11),a+side*(offset+.11)):
                    hit=surface.ray_cast(v+Vector((0,0,.2)),Vector((0,0,-1)),.4)
                    if hit[0] is None:break
                    q.append(tuple(hit[0]+Vector((0,0,.0015))))
                if len(q)==4:
                    strength=age*(.36+.20*math.sin(math.pi*(progress+end)/2))
                    stamp(q,'rubber',strength,[(u0,vstart),(u0,vend),(u1,vend),(u1,vstart)])
    L,W=p['length'],p['width']
    # The exposed drive lane loses sealer where vehicles travel. This is a
    # projected soft ribbon with roughness, rather than vertex gradients
    # stretching a 20cm wear mask across a whole 18m deck triangle.
    upper=next(row for row in reversed(p['paths']) if row['name'].startswith('Drive_Up_'))
    pts=[Vector(v) for v in upper['points']];length=sum((b-a).xy.length for a,b in zip(pts,pts[1:]));distance=0
    for a,b in zip(pts,pts[1:]):
        delta=b-a;segment=delta.xy.length;start=distance;distance+=segment
        if segment<.06 or min(a.z,b.z)<(p['levels']-1)*FLOOR-.05:continue
        tangent=delta.xy.normalized();normal=Vector((-tangent.y,tangent.x,0));corners=[]
        for v in (a-normal*2.6,b-normal*2.6,b+normal*2.6,a+normal*2.6):
            hit=surface.ray_cast(v+Vector((0,0,.2)),Vector((0,0,-1)),.4)
            if hit[0] is None:break
            corners.append(tuple(hit[0]+Vector((0,0,.0018))))
        if len(corners)==4:
            u0,v0,u1,v1=A.LAYOUT['scuff']['rect'];va=v0+start/max(length,.001)*(v1-v0);vb=v0+distance/max(length,.001)*(v1-v0)
            stamp(corners,'scuff',.4*age,[(u0,va),(u0,vb),(u1,vb),(u1,va)])
    for lev in range(p['levels']):
        z=lev*FLOOR
        for x in (-L/3,0,L/3):
            for yy in (-W/2+.5,p['joint_y']-.5):
                floor_mark(x+.15,yy+.15,deck_z(p,lev,x,yy),rng.uniform(1,1.7),rng.uniform(.45,.85),'runoff',.48*age)
        # Runoff descends from panel tops and leaking flange joints. Individual
        # narrow streams, dry gaps and pale salts avoid a uniform dirty band.
        for side in (-1,1):
            y=side*(W/2+(.1308 if old else .0908))
            for a,c in zip(p['structural_stations'],p['structural_stations'][1:]):
                mid=(a+c)/2
                if lev==0 and side==-1 and mid>L/2-p['end_length']-3:continue
                if side==1 and p['ramp_limits'][0]<mid<p['ramp_limits'][1]:continue
                for j in range(rng.randint(5,9) if old else rng.randint(3,6)):
                    x=rng.uniform(a+.15,c-.15);width=rng.uniform(.18,.72);length=rng.uniform(.45,1.28)
                    top=z+((1.02 if side==-1 else .98) if old else .54);bottom=max(z-.30,top-length)
                    stamp([(x-width/2,y,bottom),(x+width/2,y,bottom),(x+width/2,y,top),(x-width/2,y,top)],'runoff',age*rng.uniform(.45,.85))
                x=rng.choice((a+.08,c-.08));w=rng.uniform(.20,.48);top=z+(.94 if old else .5)
                stamp([(x-w/2,y,z-.22),(x+w/2,y,z-.22),(x+w/2,y,top),(x-w/2,y,top)],'mineral',age*.62)
                if rng.random()<.65:
                    x=rng.uniform(a+.5,c-.5);zz=z+rng.uniform(-.08,.40);w=rng.uniform(.28,.68);h=rng.uniform(.16,.34)
                    stamp([(x-w/2,y,zz),(x+w/2,y,zz),(x+w/2,y,zz+h),(x-w/2,y,zz+h)],'spall',.8)
    construction(root,p,rng,age,stamp,floor_mark)
    ob=batch.finish();ob['allow_boundary']=True # open pigment films, never a collision solid
    attr=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER');ob.data.color_attributes.active_color=attr
    # G.Mesh triangulates each quad into two consecutive faces.
    for f in ob.data.polygons:
        strength=strengths[f.index//2]
        for li in f.loop_indices:attr.data[li].color=(1,1,1,strength)
    report=dict(seed=p['seed'],maintenance='1988 municipal: aged joints / 1996 commercial: more frequent patching',marks=counts,
        triangles=G.triangles([ob]),floor_corner_surface_samples=len(projection),max_corner_height_difference_m=max(projection,default=0))
    return report


def construction(root,p,rng,age,stamp,floor_mark):
    for rr in root.children:
        if not rr.name.startswith('Tower_') or not rr.get('module_kind'):continue
        for lev in range(p['levels']):
            for yy in (-1.78,1.78):
                top=lev*FLOOR+min(FLOOR,3.0 if lev==p['levels']-1 else FLOOR)-.035
                length=rng.uniform(.65,1.25);width=rng.uniform(.22,.42)
                pts=[tuple(rr.matrix_world@Vector(v)) for v in ((2.829,yy-width/2,top-length),(2.829,yy+width/2,top-length),(2.829,yy+width/2,top),(2.829,yy-width/2,top))]
                stamp(pts,'runoff',age*.5)
    # Iron oxide starts at real connector locations along the tee flange.
    # The thin deposit lies on the flange underside, not across the air gap.
    for rr in list(root.children):
        if rr.get('module_kind')!='DoubleTee':continue
        if rng.random()<.30*age:
            # Torn sealant traps dark fines in short irregular stretches,
            # extending beyond the still-intact 22mm manufactured joint.
            for j in range(rng.randint(1,3)):
                x=rr.location.x+TEE/2;y=rr.location.y+rng.uniform(-7.5,7.5)
                lev=round(rr.location.z/FLOOR)
                ramp=rr.name.startswith('Ramp_') and p['ramp_limits'][0]<rr.location.x<p['ramp_limits'][1]
                floor_mark(x,y,deck_z(p,lev,x,y,ramp),rng.uniform(.045,.09),rng.uniform(.7,2.0),'oil',.95)
        if rng.random()>.66*age:continue
        for yy in (-6.1,0,6.1):
            if rng.random()>.7:continue
            localx=TEE/2-.075;pts=[]
            for dx,dy in ((-.14,-.38),(.045,-.38),(.045,.38),(-.14,.38)):
                q=rr.matrix_world@Vector((localx+dx,yy+dy,0));lev=round(rr.location.z/FLOOR)
                ramp=rr.name.startswith('Ramp_') and p['ramp_limits'][0]<rr.location.x<p['ramp_limits'][1]
                q.z=deck_z(p,lev,q.x,q.y,ramp)-.1525;pts.append(tuple(q))
            stamp(pts,'rust',rng.uniform(.5,.95))
    # Seat connectors leak onto girder ledges and corbel faces. Pale mineral
    # tails accompany the dark seal at occasional failed joints.
    for rr in list(root.children):
        if not rr.name.startswith('Girder_') or rng.random()>.48*age:continue
        x,y,z=rr.location;side=-1 if y<p['joint_y'] else 1
        xx=x+rng.uniform(-2,2);yy=y+side*.164
        stamp([(xx-.10,yy,z-.67),(xx+.10,yy,z-.67),(xx+.10,yy,z-.13),(xx-.10,yy,z-.13)],'rust',.72)
    # Roost deposits below protected ledges, including vacant roof stalls.
    for s in p['stalls']:
        if rng.random()>.11*age:continue
        yy=s['y']+(-1 if s['yaw']==180 else 1)*(s['depth']/2-.6)
        for j in range(rng.randint(2,4)):
            xx=s['x']+rng.uniform(-.45,.45);y=yy+rng.uniform(-.25,.25)
            floor_mark(xx,y,deck_z(p,s['level'],xx,y,s['ramp']),rng.uniform(.06,.14),rng.uniform(.09,.20),'droppings',.9)
    # Concrete corner abrasion follows bumper contact on the end-turn shafts.
    for rr in list(root.children):
        if not rr.name.startswith('ColumnShaft_'):continue
        if rr.get('round_column'):continue # no planar deposits across the round reference form
        x,y,z=rr.location
        if rng.random()<.6*age:
            xx=x+rng.uniform(-.12,.12);w=rng.uniform(.24,.42);top=rng.uniform(.19,.34);yy=y-.382
            stamp([(xx-w/2,yy,.015),(xx+w/2,yy,.015),(xx+w/2,yy,top),(xx-w/2,yy,top)],'runoff',age*rng.uniform(.3,.55))
        if min(abs(x-a) for a in p['ramp_limits'])>.01:continue
        for lev in range(p['levels']-1):
            zz=lev*FLOOR
            for j in range(3):
                q=zz+.16+j*.20;xx=x-.31+rng.uniform(-.008,.008);yy=y-.383
                stamp([(xx-.035,yy,q),(xx+.11,yy,q),(xx+.11,yy,q+.16),(xx-.035,yy,q+.16)],'scuff',.7)
    # One damaged barrier: steel members bow inward at a bumper strike; the
    # concrete curb/post bases stay put. Reusable stock remains undamaged.
    target=next((r for r in root.children if r.name.startswith('Center guard 0 False')),None)
    if target:
        for ob in target.children_recursive:
            if ob.type!='MESH':continue
            ob.data=ob.data.copy();visited=set()
            for f in ob.data.polygons:
                if 'baked' not in ob.data.materials[f.material_index].name:continue
                for vi in f.vertices:
                    if vi in visited:continue
                    visited.add(vi)
                    v=ob.data.vertices[vi]
                    if v.co.z>.3 and abs(v.co.x)<1.8:v.co.y-=.045*math.exp(-(v.co.x/1.1)**2)
            ob.data.update()
