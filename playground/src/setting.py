"""Read-only library town context, separate from the budgeted playground.

Canonical ground, houses, trees and cars are imported for presentation only.
No canonical file is written, re-exported, baked or modified on disk.
"""
import math,random
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]

def import_roots(path,keep=None):
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path));added=set(bpy.context.scene.objects)-before
    roots=[o for o in added if o.parent not in added]
    selected={}
    for rt in roots:
        name=rt.name.split('.')[0]
        if keep is None or name in keep:selected[name]=rt
        else:
            for o in [*rt.children_recursive,rt]:bpy.data.objects.remove(o,do_unlink=True)
    return selected

def clone(rt,name,loc,yaw=0):
    import geometry as F
    o=F.clone(rt,name,loc,yaw);o['presentation_only']=True;return o

def context(plan):
    from kit import model as G
    from kit.tiling import material,world_uv
    x0,y0,x1,y1=plan['surface'];back=y1+15
    ground=import_roots(ROOT/'ground/export/Ground.glb',{'Road_Straight_A','Curb_Straight','Sidewalk_A'})
    lawn=next((m for m in bpy.data.materials if 'Lawn' in m.name and m.use_nodes),None)
    if lawn:
        o=G.box('Presentation surrounding park',(0,0,-.235),(1800,1800,.20),lawn,0);world_uv(o,4)
    for i in range(-10,11):
        x=i*6.096
        clone(ground['Road_Straight_A'],'Library residential street',(x,back,-.10),90)
        for side in (-1,1):
            for dx in (-1.524,1.524):clone(ground['Curb_Straight'],'Library street curb',(x+dx,back+side*4.1148,-.10),90 if side>0 else -90)
            for dx in (-2.286,-.762,.762,2.286):clone(ground['Sidewalk_A'],'Library town sidewalk',(x+dx,back+side*6.096,-.10),90)
    asphalt=next(m for m in bpy.data.materials if 'Asphalt' in m.name and m.use_nodes)
    concrete=next(m for m in bpy.data.materials if 'Concrete' in m.name and m.use_nodes)
    # School blacktop stops at a building interface; parks have a buffered lot.
    if plan['year']==1996:
        o=G.box('School blacktop / building edge socket',(3,y1+7,-.075),(32,12,.12),asphalt,0);world_uv(o,4)
        for i in range(6):
            G.box('School game stripe',(-6+i*.7,y1+5,.002),(.018,4,.003),concrete,0)
    else:
        o=G.box('Neighborhood parking / six stalls',(x0+5,y1+7,-.075),(16,7,.12),asphalt,0);world_uv(o,4)
        for i in range(6):G.box('Parking stripe',(x0-2+i*2.5,y1+7,.002),(.065,5,.003),concrete,0)
        # A loop path skirts the containment, with a lawn buffer under shade.
        pts=[(x0-2.3,y0-1.7),(x0-3.0,y1),(x0+2,y1+2.7),(x1-2,y1+2.7),(x1+3,y1),(x1+3,y0+1),(x1-2,y0-1.7)]
        from kit.model import fillet_polygon
        line=fillet_polygon(pts,2.2,6)
        # Ribbon segments use the canonical concrete response.
        vs=[]
        for i,p in enumerate(line):
            t=Vector(line[min(i+1,len(line)-1)])-Vector(line[max(0,i-1)]);t.normalize();n=Vector((-t.y,t.x))
            vs.extend([(* (Vector(p)+n*.85),-.012),(* (Vector(p)-n*.85),-.012)])
        o=G.mesh('Park circulation loop path',vs,[(i*2,i*2+1,((i+1)%len(line))*2+1,((i+1)%len(line))*2) for i in range(len(line))],concrete)
        m=o.modifiers.new('Continuous path slab gauge','SOLIDIFY');m.thickness=.10;m.offset=-1;G.apply(o)
        uv=o.data.uv_layers.active or o.data.uv_layers.new(name='UVMap')
        for f in o.data.polygons:
            axes=sorted(range(3),key=lambda k:abs(f.normal[k]))[:2]
            for li in f.loop_indices:
                p=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(p[axes[0]]/2,p[axes[1]]/2)
    for rt in ground.values():
        for o in [*rt.children_recursive,rt]:bpy.data.objects.remove(o,do_unlink=True)
    for j,filename in enumerate(('HearthfieldRanch-11.gltf','HearthfieldCape-34.gltf')):
        house=next(iter(import_roots(ROOT/'houses/export'/filename).values()))
        for i in range(-3,4):
            if i%2!=j:continue
            clone(house,'Library house beyond park',(i*21+4,back+20,-.10),180)
        for o in [*house.children_recursive,house]:bpy.data.objects.remove(o,do_unlink=True)
    tree=next((o for o in bpy.context.scene.objects if o.name.startswith('Library_PinOak') and o.type=='EMPTY'),None)
    if tree is None:tree=next(iter(import_roots(ROOT/'trees/export/PinOak.glb').values()))
    maple=next((o for o in bpy.context.scene.objects if o.name.startswith('Library_RedMaple') and o.type=='EMPTY'),None)
    new_maple=maple is None
    if maple is None:maple=next(iter(import_roots(ROOT/'trees/export/RedMaple.glb').values()))
    rng=random.Random(plan['seed']+83)
    for i in range(-6,7):
        ob=clone(tree if i%3 else maple,'Library distant shade tree',(i*12.1+rng.uniform(-3,3),back+rng.uniform(8,16),-.10),rng.uniform(0,360));ob.scale*=rng.uniform(.82,1.10)
    for i in range(4):
        ob=clone(tree if i%2 else maple,'Library park grove',(x1+7+(i%2)*9,-4+i*11,-.10),i*113);ob.scale*=rng.uniform(.83,1.10)
    # Complete the setting around the other camera directions too. In
    # particular the stair reference looks back across the park's south edge.
    for i in range(8):
        ob=clone(tree if i%3 else maple,'Library distant shade tree / south',(-43+i*12+rng.uniform(-3,3),y0-25+rng.uniform(-3,3),-.10),rng.uniform(0,360));ob.scale*=rng.uniform(.80,1.08)
    for i in range(4):
        ob=clone(tree if i%2 else maple,'Library distant shade tree / west',(x0-22+rng.uniform(-3,3),-18+i*13,-.10),rng.uniform(0,360));ob.scale*=rng.uniform(.82,1.10)
    if new_maple:
        for o in [*maple.children_recursive,maple]:bpy.data.objects.remove(o,do_unlink=True)
    for i,filename in enumerate(('AlderH120.glb','AlderC150.glb')):
        car=next(iter(import_roots(ROOT/'cars/export'/filename).values()))
        clone(car,'Library parked car',(x0+1.5+i*7.5,y1+7,-.01),90 if i%2 else -90)
        for o in [*car.children_recursive,car]:bpy.data.objects.remove(o,do_unlink=True)
    light=next((o for o in bpy.context.scene.objects if o.name.startswith('StreetLight') and o.type=='EMPTY'),None)
    if light:
        for x in (-24,24):clone(light,'Library street light',(x,back-5,-.10),90)
