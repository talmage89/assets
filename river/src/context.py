"""Read-only native library context, linked within each crossing export.

School's existing form caches are original family geometry, not external art.
They are temporary low-detail presentation resources, explicitly costed apart.
"""
import math
import random
import json
from pathlib import Path
import bpy
from mathutils import Matrix
import geometry as G
from channel import surface_z

REPO=Path(__file__).resolve().parents[2]
CACHE={}


def template(path,select=None):
    key=(str(path),select)
    if key in CACHE:return CACHE[key]
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(Path(path).resolve()))
    obs=sorted(set(bpy.context.scene.objects)-before,key=lambda ob:ob.name)
    if select:
        pick=next(o for o in obs if o.name==select or o.name.endswith('__'+select))
        keep=set(G.descendants(pick));world=pick.matrix_world.copy();pick.parent=None;pick.matrix_world=world
        for ob in obs:
            if ob not in keep:bpy.data.objects.remove(ob,do_unlink=True)
        obs=sorted(keep,key=lambda ob:ob.name)
    rt=G.root('Template_'+Path(path).stem)
    for o in obs:
        if o.parent not in obs:o.parent=rt
    # Native cache files carry no scene-placement transform; selected roots may.
    if select:
        for o in rt.children:o.location=(0,0,0)
    CACHE[key]=rt;return rt


def instance(path,name,pos,parent=None,yaw=0,scale=1,select=None,category='context'):
    src=template(path,select);mapping={}
    for old in G.descendants(src):
        ob=old.copy();ob.name=name if old==src else name+'__'+old.name
        bpy.context.collection.objects.link(ob);mapping[old]=ob;ob['river_category']=category
    for old,ob in mapping.items():ob.parent=mapping.get(old.parent,parent)
    rt=mapping[src];rt.location=pos;rt.rotation_euler=(0,0,math.radians(yaw));rt.scale=(scale,)*3
    return rt


def clear_templates():
    for rt in CACHE.values():
        for ob in reversed(G.descendants(rt)):bpy.data.objects.remove(ob,do_unlink=True)
    CACHE.clear()


def paving_skirts(batch,points,edges,role):
    """Visible 75mm paving/base edges, embedded 5mm into the soil.

    Edges follow the top's counterclockwise boundary. No buried underside
    or repeated internal bay walls are added.
    """
    for a,c in edges:
        va,vc=points[a],points[c]
        batch.geom([va,(va[0],va[1],va[2]-.08),(vc[0],vc[1],vc[2]-.08),vc],[(0,1,2,3)],role)


def add(p,parent):
    rt=G.root('TownContext',parent=parent);rng=random.Random(p.seed+97);lots=[]
    native=REPO/'school/build/context'
    # A few neutral 1.8m people are scale references, on the actual walk.
    from kit.studio import human
    for i,x in enumerate((-p.length/2-2,-8,16)):
        person=G.root('WalkScalePerson_'+str(i),(x+1.03,-4.2672-.24,p.deck_z+.085344),rt)
        for ob in human():ob.parent=person;ob['river_category']='context';ob.pop('studio',None)
    # Two actual original vehicle bodies, alternating direction and spaced by
    # weekday headways, plus the street behind the river. Static snapshot only.
    for i,x in enumerate(range(-106,115,17 if p.kind=='downtown' else 25)):
        y=-1.6764 if i%2==0 else 1.6764
        z=p.deck_z-.02*abs(y)
        ob=instance(native/'car.glb',f'Traffic_{i}',(x+rng.uniform(-2,2),y,z),rt,
                    90 if y<0 else -90,category='cars')
        # Preserve original form materials; varied local paint is an object material.
        for child in ob.children_recursive:
            if child.type!='MESH':continue
            for slot in child.material_slots:
                if slot.material and 'paint' in slot.material.name:
                    ma=slot.material.copy();ma.name='Traffic paint '+str(i)
                    ma.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*[(.30,.31,.30),(.018,.024,.021),(.28,.055,.034),(.72,.71,.63),(.035,.08,.13)][i%5],1)
                    slot.link='OBJECT';slot.material=ma
    # Downtown brick backs line an actual alley behind the riverwalk. The
    # approach street passes through the gap, rather than through a building.
    if p.kind=='downtown':
        from urban import add as urban
        lots=urban(p,rt);front=rt['main_street_front_m']
        for side in (-1,1):
            for x in (-17,17):
                instance(native/'light.glb','Parapet light',(x,side*(p.deck_width/2-.3048),p.deck_z+.90),rt,0 if side>0 else 180)
        for i,y in enumerate((-44,-22,22,46)):
            x=p.center(y)-p.halfwidth(y)-3.65
            instance(native/'furniture.glb','Riverwalk bench '+str(i),(x,y,.65),rt,90,select='Bench')
    else:
        for i in range(12):
            x=(-1 if i%2 else 1)*(58+(i//4)*29);y=(-1 if i%4<2 else 1)*rng.uniform(25,38)
            style='houses-ranch.glb' if i%2 else 'houses-cape.glb'
            instance(native/style,'Floodplain neighbor '+str(i),(x,y,surface_z(p,x,y)-.025),rt,90 if x>0 else -90)
            lots.append((x-12,x+12,y-12,y+12))
        instance(native/'furniture.glb','Fishing bench',(-25,34,2.15),rt,90,select='Bench')
        from rural import add as rural
        rural(p,rt,lots)
    signs=REPO/'street-signs/export/set/RoadSigns.gltf'
    if signs.exists():
        for side in (-1,1):
            instance(signs,'Native 35mph approach sign '+str(side),
                     (side*(p.length/2+18),-side*5.4,p.deck_z),rt,
                     90 if side<0 else -90,select='RoadSign_speed35')
    # Only the delivered native RedMaple and PinOak species. Red maple near
    # water; oak on higher ground. No invented willow or generic new tree.
    veg=G.root('NativeVegetation',parent=parent)
    for i in range(310 if p.kind=='edge' else 30):
        y=rng.uniform(-160,165);side=-1 if i%2 else 1
        near=i<250;x=p.center(y)+side*(p.halfwidth(y)+(rng.uniform(3,17) if near else rng.uniform(30,95)))
        if abs(y)<12:continue
        if any(a<x<b and c<y<d for a,b,c,d in lots):continue
        if p.kind=='downtown' and front+1<abs(x)<front+12:continue
        # Leave actual camera/bridge sightlines as maintained access/clear
        # banks. The town still encloses the views outside these narrow cones.
        hy=-59 if p.kind=='edge' else -64
        hx=p.center(hy)-p.halfwidth(hy)-(7 if p.kind=='edge' else 2.6)
        corridors=[((hx,-59 if p.kind=='edge' else -64),(0,0),5.5)]
        corridors += [((23.65,-106.72),(0,0),7)] if p.kind=='downtown' else [((-67.87,-38.24),(0,0),7)]
        occludes=False
        for (ax,ay),(bx,by),radius in corridors:
            dx,dy=bx-ax,by-ay;t=((x-ax)*dx+(y-ay)*dy)/(dx*dx+dy*dy)
            if 0<t<1 and math.hypot(x-ax-t*dx,y-ay-t*dy)<radius:occludes=True
        if occludes:continue
        z=surface_z(p,x,y);species='RedMaple' if near or i%3 else 'PinOak'
        ob=instance(REPO/f'trees/export/{species}.glb','Native_'+species+'_'+str(i),(x,y,z-.04),veg,rng.uniform(0,360),rng.uniform(.36,1.10),category='vegetation')
        if near and p.kind=='edge':ob.rotation_euler.y=side*math.radians(rng.uniform(-6,-2))
    for i in range(650 if p.kind=='edge' else 45):
        y=rng.uniform(-149,149);side=(-1,1)[i%2]
        if abs(y)<14:continue
        x=p.center(y)+side*(p.halfwidth(y)+rng.uniform(1.9,15.5))
        if p.kind=='downtown':continue
        if side<0 and abs(abs(x-p.center(y))-p.halfwidth(y)-7)<1.4:continue
        instance(native/'shrub.glb','Native bank shrub '+str(i),(x,y,surface_z(p,x,y)-.02),veg,
                 rng.uniform(0,360),rng.uniform(.75,2.1),category='vegetation')
    return rt
