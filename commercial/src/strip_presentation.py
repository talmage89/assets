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
    # Single-frontage parcels no longer masquerade as four identical blocks.
    # The corner uses the family's real intersection recipe; the side-parking
    # site fronts the west street and presents its wrapped end to that street.
    from strip_render import ground
    records=[]
    if p['shape']=='L':
        from presentation import ground as corner_ground
        parent,record=corner_ground({**p,'yaw':0},neighborhood=True)
        parent.scale.x=-1
    else:
        before=set(bpy.context.scene.objects)
        record=ground({**p,'lot':tuple(reversed(p['lot']))} if p.get('frontage')=='west' else p)
        parent=bpy.data.objects['StripGroundContext']
        if p.get('frontage')=='west':parent.rotation_euler.z=-math.pi/2
    W,D=p['lot'];side=p.get('frontage')=='west'
    dependencies=record.setdefault('neighbor_dependencies',[])
    # Background yards and occupied streets are assembled from immutable stock.
    cases=(
        ('houses/export/HearthfieldRanch-11.gltf',[((x,D/2+18,0),0) for x in (-32,0,32,64,96)]),
        ('houses/export/HearthfieldCape-31.gltf',[((W/2+24,y,0),-90) for y in (-20,18,56)]),
        ('houses/export/HearthfieldCape-31.gltf',[((x,D/2+45,0),0) for x in (-60,-15,30,75,120)]),
        ('trees/export/PinOak.glb',[((x,D/2+8,0),x*2.1) for x in (-43,-12,24,58,91)]),
        ('trees/export/RedMaple.glb',[((W/2+12,y,0),y*1.3) for y in (-24,10,44,78)]),
    )
    context=root('StripNeighborhood',kind='CONTEXT')
    for relative,places in cases:dependencies.append(instance(REPO/relative,places,context))
    if not side:
        dependencies.append(instance(REPO/'houses/export/HearthfieldRanch-11.gltf',[((-W/2-25,y,0),90) for y in (-D/2+12,D/2-13,D/2+25)],context))
        dependencies.append(instance(REPO/'trees/export/RedMaple.glb',[((-W/2-12,y,0),y*2) for y in (-D/2+17,D/2-8,D/2+28)],context))
    if side:
        places=[((-W/2-27,y,0),90) for y in (-24,8,40,72)]
    else:places=[((x,-D/2-29,0),180) for x in (-42,-10,22,54,86)]
    dependencies.append(instance(REPO/'houses/export/HearthfieldCape-31.gltf',places,context))
    record['strip_context']='Original native frontage with occupied library neighborhood; single frontage except the two-street corner'
    return record


def cars(p):
    parent=root('ParkedVehicles',kind='CONTEXT');rows=[]
    ordinary=sorted((s for s in p['stalls'] if not s['accessible']),key=lambda s:(s['row'],s['x0']))
    rng=__import__('random').Random(p['seed']+451)
    front=[s for s in ordinary if s['row']==0]
    lower=[s for s in ordinary if s['row'] in (1,2)]
    # Twenty-six percent occupancy, biased toward entrances, with long empty
    # intervals around the hero's first two bays and ordinary diagnostic views.
    chosen=rng.sample(front,min(len(front)-3,round(p['stall_count']*.16)))
    chosen+=rng.sample(lower,round(p['stall_count']*.26)-len(chosen))
    decoder=runpy.run_path(str(REPO/'cars/src/delivery_materials.py'));templates={}
    cases=('AlderC150.glb','AlderX220.glb','AlderH120.glb');colors=('Porcelain','Atlantic','Graphite','Aluminum','Carbon','Ember')
    for i,s in enumerate(chosen):
        filename=cases[i%3];color=colors[(i//3+i)%len(colors)];key=(filename,color);path=REPO/'cars/export'/filename
        if key not in templates:
            before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path));added=set(bpy.context.scene.objects)-before
            current=[m for o in added if o.type=='MESH' for m in o.data.materials if m and m.get('paint_decode')=='reference_plus_coverage_delta']
            if current:
                material=current[0];namespace=decoder['apply'].__globals__;old=namespace['paint_material'];namespace['paint_material']=lambda:material
                options=json.loads(material['paint_colors']);selected=color if color in options else list(options)[(i+2)%len(options)]
                decoder['apply'](selected,False);namespace['paint_material']=old;color=selected
            templates[key]=({o.name:(o.copy(),o.parent.name if o.parent in added else None,o.matrix_basis.copy()) for o in added},bundle(path),color)
            for o in added:bpy.data.objects.remove(o,do_unlink=True)
        template,receipt,color=templates[key];copies={o:data[0].copy() for o,data in template.items()}
        rt=root('Parked_'+str(i),((s['x0']+s['x1'])/2,(s['y0']+s['y1'])/2-(.45 if i%3==0 else .12)*s['facing'],0),180 if (i%4==0 or s['facing']<0) else 0,parent=parent,kind='CONTEXT')
        for o,cp in copies.items():
            bpy.context.collection.objects.link(cp);_,par,xf=template[o];cp.parent=copies.get(par,rt);cp.matrix_basis=xf
        rows.append(dict(source=filename,stall_center=list(rt.location),color=color,bundle=receipt))
    return rows
