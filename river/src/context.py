"""Read-only native library context, linked within each crossing export.

School's existing form caches are original family geometry, not external art.
They are temporary low-detail presentation resources, explicitly costed apart.
"""
import math
import random
from pathlib import Path
import bpy
from mathutils import Matrix
import geometry as G

REPO=Path(__file__).resolve().parents[2]
CACHE={}


def template(path,select=None):
    key=(str(path),select)
    if key in CACHE:return CACHE[key]
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(Path(path).resolve()))
    obs=set(bpy.context.scene.objects)-before
    if select:
        pick=next(o for o in obs if o.name==select or o.name.endswith('__'+select))
        keep=set(G.descendants(pick));world=pick.matrix_world.copy();pick.parent=None;pick.matrix_world=world
        for ob in obs-keep:bpy.data.objects.remove(ob,do_unlink=True)
        obs=keep
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


def add(p,parent):
    rt=G.root('TownContext',parent=parent);rng=random.Random(p.seed+97)
    native=REPO/'school/build/context'
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
        for side in (-1,1):
            for i in range(-5,6):
                y=i*14
                if abs(y)<15:continue
                key=f'Midwest_411_{1+(i%6):02d}.gltf';path=REPO/'downtown/export'/key
                instance(path,'MainStreetBack_'+str(side)+'_'+str(i),(side*47,y,3.7),rt,90 if side<0 else -90)
        for side in (-1,1):
            for x in (-17,17):
                instance(native/'light.glb','Parapet light',(x,side*(p.deck_width/2-.23),p.deck_z+.90),rt)
        for i,y in enumerate((-44,-22,22,46)):
            x=p.center(y)-p.halfwidth(y)-5.2
            instance(native/'furniture.glb','Riverwalk bench '+str(i),(x,y,2.65),rt,90,select='Bench')
    else:
        for i in range(12):
            x=(-1 if i%2 else 1)*(57+(i%3)*22);y=-67+(i//2)*28
            style='houses-ranch.glb' if i%2 else 'houses-cape.glb'
            instance(native/style,'Floodplain neighbor '+str(i),(x,y,2.20),rt,90 if x>0 else -90)
        instance(native/'furniture.glb','Fishing bench',(-25,34,2.15),rt,90,select='Bench')
    # Only the delivered native RedMaple and PinOak species. Red maple near
    # water; oak on higher ground. No invented willow or generic new tree.
    veg=G.root('NativeVegetation',parent=parent)
    for i in range(86 if p.kind=='edge' else 55):
        y=rng.uniform(-160,165);side=-1 if i%2 else 1
        near=i<32;x=p.center(y)+side*(p.halfwidth(y)+(rng.uniform(3,11) if near else rng.uniform(30,95)))
        if abs(y)<12:continue
        z=p.bed(x,y);species='RedMaple' if near or i%3 else 'PinOak'
        ob=instance(REPO/f'trees/export/{species}.glb','Native_'+species+'_'+str(i),(x,y,z-.04),veg,rng.uniform(0,360),rng.uniform(.63,1.1),category='vegetation')
        if near and p.kind=='edge':ob.rotation_euler.y=side*math.radians(rng.uniform(-6,-2))
    return rt
