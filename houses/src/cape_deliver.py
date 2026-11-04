"""Cape delivery: bake causal color to vertices, retain shared PBR manufacture.

Only Cape files are published. Existing family PNGs remain immutable. Source
shader texture color is replaced by unit white during the vertex emission bake,
so tiled manufacture is applied exactly once by the delivered PBR material.
"""
import argparse,json,sys,hashlib
from pathlib import Path
import bpy
import bmesh
import numpy as np
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit import tiling,gpu
from lookdev import materials
from deliver import externalize
from glb_budget import compact,read
from ranch_uv import resolve

ROOT=Path('build/cape/delivery')


def aged_orm(mat,constant=False):
    """Reuse the family's matte paint / oxidized-metal ORM, without new pixels."""
    nt=mat.node_tree
    node=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and n.image and '_ORM' in n.image.name)
    node.image=bpy.data.images.load(str(Path('textures/ranch-ship/T_RanchTrim_ORM.png').resolve()),check_existing=True);node.image.colorspace_settings.name='Non-Color'
    if constant:
        uv=nt.nodes.new('ShaderNodeTexCoord');mapping=nt.nodes.new('ShaderNodeMapping')
        mapping.inputs['Location'].default_value=(.12,.05,0);mapping.inputs['Scale'].default_value=(.00001,.00001,1)
        nt.links.new(uv.outputs['UV'],mapping.inputs['Vector']);nt.links.new(mapping.outputs['Vector'],node.inputs['Vector'])


def discard_loose(ob):
    me=ob.data;used={i for p in me.polygons for i in p.vertices};count=len(me.vertices)-len(used)
    if not count:return 0
    # Dissolution can leave unreferenced samples. They are not geometry and
    # glTF omits them; remove them explicitly from the audited game source.
    stored=me.attributes.new(name='_DeliveryNormals',type='FLOAT_VECTOR',domain='CORNER')
    stored.data.foreach_set('vector',np.array([n.vector[:] for n in me.corner_normals],dtype='float32').ravel())
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bm.to_mesh(me);bm.free();me.update()
    me.normals_split_custom_set([v.vector.normalized() for v in me.attributes['_DeliveryNormals'].data]);me.attributes.remove(me.attributes['_DeliveryNormals'])
    me.color_attributes.active_color=me.color_attributes['Tint'];return count


def weld_uv_slivers(ob):
    """Remove only unresolvable UV edges shorter than half a micrometer."""
    me=ob.data;me.calc_loop_triangles();uv=me.uv_layers.active;bad=[]
    for tri in me.loop_triangles:
        a,b,c=[Vector(uv.data[i].uv) for i in tri.loops];d=b-a;e=c-a
        if abs(d.x*e.y-d.y*e.x)>=2e-14:continue
        pairs=[(i,j) for i,j in ((tri.vertices[0],tri.vertices[1]),(tri.vertices[1],tri.vertices[2]),(tri.vertices[2],tri.vertices[0])) if (me.vertices[i].co-me.vertices[j].co).length<5e-7]
        bad.extend(pairs)
    if not bad:return 0
    saved=me.attributes.new(name='_CleanupNormals',type='FLOAT_VECTOR',domain='CORNER');saved.data.foreach_set('vector',np.array([n.vector[:] for n in me.corner_normals],dtype='float32').ravel())
    bm=bmesh.new();bm.from_mesh(me);bm.verts.ensure_lookup_table();indices={i for p in bad for i in p};before=len(bm.verts)
    bmesh.ops.remove_doubles(bm,verts=[bm.verts[i] for i in indices],dist=5e-7);count=before-len(bm.verts);bm.to_mesh(me);bm.free();me.update()
    me.normals_split_custom_set([v.vector.normalized() for v in me.attributes['_CleanupNormals'].data]);me.attributes.remove(me.attributes['_CleanupNormals']);me.color_attributes.active_color=me.color_attributes['Tint'];return count


def bake_weather(objects):
    sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=1;gpu.enable()
    sc.render.bake.target='VERTEX_COLORS'
    used={m for o in objects for m in o.data.materials}
    for mat in used:
        nt=mat.node_tree
        white=nt.nodes.new('ShaderNodeRGB');white.outputs[0].default_value=(1,1,1,1)
        for node in list(nt.nodes):
            if node.type=='TEX_IMAGE' and node.image and 'BaseColor' in node.image.name:
                for link in list(node.outputs['Color'].links):nt.links.new(white.outputs[0],link.to_socket)
        # Fine mineral / unit variation belongs to the manufacturing tile.
        # Evaluating it at isolated vertices aliases it into large blotches.
        for name,value in (('fine_noise',.5),('manufacture_variation',1.195),('manufacture_granule',.95)):
            channel=nt.nodes.get('OUT_'+name)
            if channel:
                constant=nt.nodes.new('ShaderNodeValue');constant.outputs[0].default_value=value
                for link in list(channel.outputs[0].links):nt.links.new(constant.outputs[0],link.to_socket)
        output=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL')
        emit=nt.nodes.new('ShaderNodeEmission');emit.inputs['Strength'].default_value=1
        channel=nt.nodes.get('OUT_base')
        if channel:nt.links.new(channel.outputs[0],emit.inputs['Color'])
        else:emit.inputs['Color'].default_value=(1,1,1,1)
        nt.links.new(emit.outputs[0],output.inputs['Surface'])
    # A joined evaluation copy avoids a separate Cycles synchronization for
    # every small fitting. Integer vertex IDs restore results to the unjoined
    # source assembly, so its construction and moving pivots remain auditable.
    bpy.ops.object.select_all(action='DESELECT');copies=[];cursor=0
    for ob in objects:
        copy=ob.copy();copy.data=ob.data.copy();bpy.context.collection.objects.link(copy)
        identity=copy.data.attributes.new(name='CapeVertexID',type='INT',domain='POINT')
        identity.data.foreach_set('value',np.arange(cursor,cursor+len(copy.data.vertices),dtype='int32'));cursor+=len(copy.data.vertices)
        copy.select_set(True);copies.append(copy)
    bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();proxy=bpy.context.object
    color=proxy.data.color_attributes.new(name='CapeBaked',type='FLOAT_COLOR',domain='POINT');proxy.data.color_attributes.active_color=color
    bpy.ops.object.bake(type='EMIT')
    a=np.empty(len(color.data)*4,dtype='float32');color.data.foreach_get('color',a);a=a.reshape(-1,4)
    identity=np.empty(len(color.data),dtype='int32');proxy.data.attributes['CapeVertexID'].data.foreach_get('value',identity)
    ordered=np.empty_like(a);ordered[identity]=a
    clipped=int((a[:,:3]>1).any(axis=1).sum());largest=float(a[:,:3].max());cursor=0
    for ob in objects:
        me=ob.data;dst=me.color_attributes['Tint'];count=len(me.vertices);values=ordered[cursor:cursor+count].copy();cursor+=count
        values[:,:3]=np.clip(values[:,:3],0,1);values[:,3]=1;dst.data.foreach_set('color',values.ravel());me.color_attributes.active_color=dst
    bpy.data.objects.remove(proxy,do_unlink=True)
    return dict(vertices=sum(len(o.data.vertices) for o in objects),clipped_vertices=clipped,unclamped_maximum=largest,
                scope='Cycles emission evaluation at existing vertices, with unit manufacture color; fine fields remain in the shared maps')


def export_house(seed,paint_control=None):
    source=Path(f'build/cape/house-{seed}.blend');bpy.ops.wm.open_mainfile(filepath=str(source.resolve()))
    meta=json.loads(source.with_suffix('.json').read_text());objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]
    suffix=f'{seed}-control' if paint_control else str(seed)
    if paint_control:
        meta['paint_control']=list(paint_control)
        for ob in objects:
            changed=set();attr=ob.data.color_attributes['Tint']
            for p in ob.data.polygons:
                if ob.data.materials[p.material_index].name.split('.')[0] not in ('HouseSiding','CapeShingle'):continue
                for vi in p.vertices:
                    if vi not in changed:attr.data[vi].color=(*paint_control,1);changed.add(vi)
    from cape_render import views
    meta['chimney_camera']=views(meta).get('chimney')
    chimney=bpy.data.objects.get('Brick_Chimney')
    if chimney:
        points=[chimney.matrix_world@chimney.data.vertices[i].co for p in chimney.data.polygons if chimney.data.materials[p.material_index].name.split('.')[0] in ('HouseVeneer','RanchBrick') for i in p.vertices]
        meta['brick_patch_target']=[(min(p.x for p in points)+max(p.x for p in points))/2,min(p.y for p in points)+.001,max(p.z for p in points)-.45]
    roof_colors={o.name:tuple(o.data.color_attributes['Tint'].data[0].color) for o in objects if o.get('component')=='roof'}
    meta['weather_bake']=bake_weather(objects)
    original=materials(Path('textures/ship'));skin=meta['spec']['siding']
    aged_orm(original['Trim'])
    if skin in ('wood','aluminum'):aged_orm(original['Siding'],constant=True)
    original['Shingles']=tiling.material('RanchRoof',Path('textures/ranch-ship'),tint=True)
    from cape_masonry import dielectric
    original['Veneer']=dielectric('CapeBrick',Path('textures/cape-ship'))
    original['Concrete']=dielectric('CapeConcrete',Path('textures/cape-ship'))
    if skin in ('cedar','cement'):original['Siding']=dielectric('CapeCedar' if skin=='cedar' else 'CapeCement',Path('textures/cape-ship'))
    else:next(n for n in original['Siding'].node_tree.nodes if n.type=='NORMAL_MAP').inputs['Strength'].default_value=.15
    p=original['Glass'].node_tree.nodes.get('Principled BSDF');nt=original['Glass'].node_tree
    for link in list(p.inputs['Base Color'].links):nt.links.remove(link)
    p.inputs['Base Color'].default_value=(.96,.98,.96,1);p.inputs['IOR'].default_value=1.52
    rough=p.inputs['Roughness'].links[0].from_socket;mul=nt.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=.010/(9/255)
    nt.links.new(rough,mul.inputs[0]);nt.links.new(mul.outputs[0],p.inputs['Roughness'])
    chart={};reduction={};assignments={};roof_objects=[]
    from ranch_reduce import reduce
    for ob in objects:
        names=[m.name.split('.')[0] for m in ob.data.materials]
        used={names[p.material_index] for p in ob.data.polygons}
        if 'RanchRoof' in used:
            # First coarsen the source's planar grid, before its chart cuts.
            row=reduce(ob,meta,tolerance=.015)
            if row:reduction[ob.name]=row
            whole=ob.get('component')=='roof'
            if whole:
                # Recombine coplanar weather-grid triangles before clipping
                # courses. Their old diagonal is not a construction feature.
                bm=bmesh.new();bm.from_mesh(ob.data)
                bmesh.ops.join_triangles(bm,faces=list(bm.faces),cmp_materials=True,cmp_uvs=True,angle_face_threshold=.001,angle_shape_threshold=2.8)
                bm.to_mesh(ob.data);bm.free();ob.data.update()
            ob.data.calc_loop_triangles();area=sum(t.area for t in ob.data.loop_triangles)
            chart[ob.name]=resolve(ob,meta['spec']['roof_age']=='newer',True,absolute_area_tolerance=5e-8 if area<1e-4 else 0,use_polygons=whole)
        # Each wall-shingle region is a standalone rectangular image. Metric
        # UVs repeat directly, with no half-atlas seam geometry or runtime math.
        if ob.get('component') in ('roof','eave_rake_soffit','ridge','wall'):
            row=reduce(ob,meta,tolerance=.025,passes=18,include_front=True)
            if row:reduction[ob.name+'_after_charts']=row
        assignments[ob.name]=names
        if ob.get('component')=='roof':roof_objects.append(ob)
    for ob in roof_objects:
        me=ob.data;block=next((b for b in meta['blocks'] if b['name']==ob.get('block')),meta['blocks'][0])
        rest=me.attributes.get('CapeRest') or me.attributes.new(name='CapeRest',type='FLOAT_VECTOR',domain='POINT')
        context=me.attributes.get('CapeContext') or me.attributes.new(name='CapeContext',type='FLOAT_VECTOR',domain='POINT')
        for v in me.vertices:
            rest.data[v.index].vector=ob.matrix_world@v.co;context.data[v.index].vector=(0,block['eave'],1 if meta['spec']['roof_age']=='tired' else .15)
            me.color_attributes['Tint'].data[v.index].color=roof_colors[ob.name]
    if roof_objects:meta['roof_weather_resample']=bake_weather(roof_objects)
    if meta['spec']['roof_age']=='tired':
        # A bounded reconstruction of the same causal weather field restores
        # contrast lost to linear chart interpolation and fine-field averaging.
        # Keep hue, stay within 20% darkening / 18% brightening, and retain the
        # original mean-manufacture palette ceiling (with a 4% filter allowance).
        weights=np.array((.2126,.7152,.0722));factors=[]
        for ob in roof_objects:
            color=ob.data.color_attributes['Tint'];expected=float(np.array(roof_colors[ob.name][:3])@weights)*1.195*.95
            for item in color.data:
                c=np.array(item.color[:3]);f=float(c@weights)/max(expected,1e-8)
                target=np.clip(1.10*(f+.75*(f-.55)),.001,1.04)
                factor=float(np.clip(target/max(f,1e-8),.80,1.18));item.color=(*(c*factor),1);factors.append(factor)
        meta['roof_weather_transfer']=dict(method='Bounded contrast reconstruction of existing causal field; no added noise or texture',contrast=.75,pivot=.55,gain=1.10,ceiling=1.04,factor_range=list(map(float,(min(factors),max(factors)))),factor_percentiles=np.quantile(factors,[.1,.5,.9]).tolist())

    for ob in objects:
        for i,name in enumerate(assignments[ob.name]):
            role={'RanchRoof':'Shingles','RanchBrick':'Veneer','CapeShingle':'Siding'}.get(name,name.removeprefix('House'))
            ob.data.materials[i]=original[role]
        for attribute in list(ob.data.attributes):
            if attribute.name.startswith('Cape'):ob.data.attributes.remove(attribute)
    meta['submicrometer_uv_welds']={ob.name:n for ob in objects if (n:=weld_uv_slivers(ob))}
    meta['removed_unreferenced_vertices']={ob.name:n for ob in objects if (n:=discard_loose(ob))}
    keep={m for ob in objects for m in ob.data.materials}
    for mat in list(bpy.data.materials):
        if mat not in keep:bpy.data.materials.remove(mat,do_unlink=True)
    for role,mat in original.items():
        if mat in keep:mat.name=('CapeCedar' if skin=='cedar' else 'CapeCement') if role=='Siding' and skin in ('cedar','cement') else 'RanchRoof' if role=='Shingles' else 'CapeBrick' if role=='Veneer' else 'CapeConcrete' if role=='Concrete' else 'House'+role
    triangles=0
    for ob in objects:ob.data.calc_loop_triangles();triangles+=len(ob.data.loop_triangles)
    meta.update(stage='baked Cape delivery; shared external PBR maps',triangles=triangles,charts=chart,reduction=reduction)
    ROOT.mkdir(parents=True,exist_ok=True);game=ROOT/f'game-{suffix}.blend';game.with_suffix('.json').write_text(json.dumps(meta,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(game.resolve()))
    moving={bpy.data.objects[n] for n in ('FrontDoor','ServiceDoor')};static=[o for o in objects if o.parent not in moving]
    bpy.ops.object.select_all(action='DESELECT')
    for ob in static:ob.select_set(True)
    bpy.context.view_layer.objects.active=static[0];bpy.ops.object.join();static[0].name='House_Static'
    embedded=ROOT/f'house-{suffix}.glb';tiling.export(embedded);compact(embedded)
    known=ROOT/'images';known.mkdir(exist_ok=True)
    for folder in ('textures/ship','textures/ranch-ship','textures/cape-ship'):
        for path in Path(folder).glob('T_*.png'):(known/path.name).write_bytes(path.read_bytes())
    out=Path(f'export/HearthfieldCape-{suffix}.gltf');sizes=externalize(embedded,out,known,max_images=18,min_images=11)
    out.with_suffix('.json').write_text(json.dumps(meta,indent=2));doc,_=read(embedded)
    row=dict(seed=seed,triangles=triangles,materials=len(doc['materials']),meshes=len(doc['meshes']),**sizes)
    print('CAPE_DELIVERED',row,flush=True);return row


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seeds',default='31,32,33,34,35,36');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    rows=[export_house(int(s)) for s in a.seeds.split(',')]
    controls=[]
    if 34 in map(int,a.seeds.split(',')):controls.append(export_house(34,paint_control=(.61,.60,.55)))
    (ROOT/'delivery.json').write_text(json.dumps(dict(rows=rows,auxiliary_paint_controls=controls),indent=2))
