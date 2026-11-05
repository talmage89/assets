"""Read-only library neighborhood and parked vehicles; never center exports."""
import json,math,runpy
from pathlib import Path
import bpy
from geometry import root
from context import bundle
from ground_adapter import FLOW
REPO=Path(__file__).resolve().parents[2]


def ready():
    return all((REPO/p).exists() for p in ('houses/export/HearthfieldSplit-51.gltf','houses/export/HearthfieldCape-31.gltf','houses/export/HearthfieldRanch-11.gltf','trees/export/PinOak.glb','trees/export/RedMaple.glb'))


def instance(source,placements,parent):
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(source.resolve()));added=set(bpy.context.scene.objects)-before
    template={o:(o.parent,o.matrix_basis.copy()) for o in added}
    for i,(loc,yaw) in enumerate(placements):
        rt=root('Presentation_'+source.stem+'_'+str(i),loc,yaw,parent=parent,kind='CONTEXT');copies={o:o.copy() for o in added}
        for o,cp in copies.items():
            bpy.context.collection.objects.link(cp);par,xf=template[o];cp.parent=copies.get(par,rt);cp.matrix_basis=xf
    for o in added:bpy.data.objects.remove(o,do_unlink=True)
    return bundle(source)


def neighborhood(p):
    from presentation import ground
    import paving
    original=paving.context_road;cache={}
    def cached_road(ob,kind):
        if ob.type!='MESH' or not any(m and m.name.startswith('Asphalt') for m in ob.data.materials):return
        key=(ob.data.as_pointer(),kind)
        if key in cache:ob.data=cache[key]
        else:original(ob,kind);cache[key]=ob.data
    # The family correction uses only immutable mesh-local UV/position and
    # section kind. Repeated copies therefore share its exact corrected data.
    paving.context_road=cached_road
    try:parent,record=ground({**p,'yaw':0},neighborhood=True)
    finally:paving.context_road=original
    W,D=p['lot'];corner=any(dr['edge']=='east' for dr in p['driveways'])
    if corner:parent.scale.x=-1
    # Restore the corner quadrant omitted for the station-owned interface.
    # The strip has straight frontage, so this native public corner belongs
    # wholly to the presentation streets, including its planted center.
    src=REPO/'ground/export/Ground.glb';before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(src));added=set(bpy.context.scene.objects)-before;lib={o.name:o for o in added if o.parent not in added};native_count=0
    def native(kind,loc,scale=(1,1,1)):
        nonlocal native_count
        source=lib[kind];copies={o:o.copy() for o in (source,*source.children_recursive)}
        for o,cp in copies.items():bpy.context.collection.objects.link(cp);cp.parent=copies.get(o.parent,parent);cp.matrix_basis=o.matrix_basis.copy()
        rt=copies[source];rt.location=loc;rt.rotation_mode='XYZ';rt.rotation_euler=(0,0,0);rt.scale=scale;native_count+=1
    for kind in ('Curb_Corner','Sidewalk_Corner','Lawn_CornerStrip','Lawn_CornerYard'):native(kind,(-W/2+1.2192,-D/2+1.2192,FLOW))
    if not corner:
        for kind,offset,step in (('Curb_Straight',3.3528,3.048),('Lawn_Strip',3.2004,3.048),('Sidewalk_A',1.3716,1.524)):
            for i in range(math.ceil(D/step)):
                lo=max(-D/2+i*step,-D/2+1.2192);hi=min(D/2,-D/2+(i+1)*step)
                if hi>lo:native(kind,(-W/2-offset,(lo+hi)/2,FLOW),(1,(hi-lo)/step,1))
    for o in added:bpy.data.objects.remove(o,do_unlink=True)
    record['strip_added_native_roots']=native_count
    # Stagger a second background block behind the first street, so gaps
    # between the near houses reveal occupied streets rather than a field.
    for relative,places in (
        ('houses/export/HearthfieldRanch-11.gltf',[((145,y,0),-90) for y in (-40,8,56,104)]),
        ('houses/export/HearthfieldCape-31.gltf',[((145,y,0),-90) for y in (-16,32,80)]),
        ('trees/export/PinOak.glb',[((134,y,0),y*1.7) for y in (-28,-4,20,44,68,92)]),
        ('houses/export/HearthfieldCape-31.gltf',[((x,105,0),0) for x in (-36,17,70,123)]),
        ('trees/export/RedMaple.glb',[((x,92,0),x*1.3) for x in (-15,38,91,144)])):
        record['neighbor_dependencies'].append(instance(REPO/relative,places,parent))
    record['strip_context']='Full library neighborhood, native streets, houses, trees and street lights; presentation only'
    return record


def cars(p):
    parent=root('ParkedVehicles',kind='CONTEXT');rows=[]
    cases=(('AlderC150.glb','Porcelain'),('AlderX220.glb','Atlantic'),('AlderH120.glb','Graphite'))
    ordinary=sorted((s for s in p['stalls'] if not s['accessible'] and s['row']==0),key=lambda s:s['x0'])
    # A few occupied bays leave windows visible, with varied empty intervals.
    selections=[(0,1),(1,5),(2,8),(0,12),(1,17),(2,21)]
    decoder=runpy.run_path(str(REPO/'cars/src/delivery_materials.py'))
    for i,(kind,index) in enumerate(selections):
        if index>=len(ordinary):continue
        filename,color=cases[kind];color='Aluminum' if i==3 else 'Carbon' if i==4 else color;path=REPO/'cars/export'/filename
        if not path.exists():continue
        before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path));added=set(bpy.context.scene.objects)-before
        # Point the family decoder at this import only. Its definition uses a
        # global paint-material lookup, so isolate prior originals temporarily.
        current=[m for o in added if o.type=='MESH' for m in o.data.materials if m and m.get('paint_decode')=='reference_plus_coverage_delta']
        if current:
            material=current[0];namespace=decoder['apply'].__globals__;old=namespace['paint_material'];namespace['paint_material']=lambda:material
            options=json.loads(material['paint_colors']);selected=color if color in options else list(options)[(i+2)%len(options)]
            decoder['apply'](selected,False);namespace['paint_material']=old
        s=ordinary[index]
        if i in (3,4):
            lower=sorted((q for q in p['stalls'] if q['row']==1 and not q['accessible']),key=lambda q:q['x0']);s=lower[min(index,len(lower)-1)]
        rt=root('Parked_'+str(i),((s['x0']+s['x1'])/2,(s['y0']+s['y1'])/2-(.45 if kind==0 else .12)*s['facing'],0),180 if i%2 else 0,parent=parent,kind='CONTEXT')
        for o in added:
            if o.parent not in added:o.parent=rt
        rows.append(dict(source=filename,stall_center=list(rt.location),color=color,bundle=bundle(path)))
    return rows
