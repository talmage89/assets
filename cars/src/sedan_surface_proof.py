"""Fresh GLB surfaces for expanded fairness views; source supplies names only."""
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

CATEGORIES={'body','doors','fascia','pillars','glass','openings','arches','lamps','tires','wheels'}


def delivery_parts(source,glb):
    bpy.ops.wm.open_mainfile(filepath=str(source))
    points=[];triangles=[];owners=[];properties={}
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('asset_set')!='Sedan':continue
        ob.data.calc_loop_triangles();start=len(points)
        points.extend(ob.matrix_world@v.co for v in ob.data.vertices)
        properties[ob.name]={k:ob[k] for k in ['part_category','lens_outer_faces'] if k in ob}
        roles=ob.data.attributes.get('sheet_role')
        for tri in ob.data.loop_triangles:
            triangles.append(tuple(start+i for i in tri.vertices))
            role=roles.data[tri.polygon_index].value if roles else (0 if tri.polygon_index<ob.get('lens_outer_faces',len(ob.data.polygons)) else 1)
            owners.append((ob.name,role))
    tree=BVHTree.FromPolygons(points,triangles,all_triangles=True)
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(glb))
    groups={};maximum=0.;samples=0
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH':continue
        me=ob.data;me.calc_loop_triangles();normal_matrix=ob.matrix_world.to_3x3().inverted().transposed()
        for tri in me.loop_triangles:
            ps=[ob.matrix_world@me.vertices[i].co for i in tri.vertices]
            ns=[(normal_matrix@me.corner_normals[i].vector).normalized() for i in tri.loops]
            center=sum(ps,Vector())/3;_,_,fi,distance=tree.find_nearest(center)
            maximum=max(maximum,distance);samples+=1;name,role=owners[fi]
            if properties[name].get('part_category') not in CATEGORIES:continue
            groups.setdefault(name,[]).append((ps,ns,role))
    for ob in list(bpy.context.scene.objects):bpy.data.objects.remove(ob,do_unlink=True)
    result=[]
    for name,rows in groups.items():
        vertices=[];faces=[];normals=[];lookup={};roles=[]
        for ps,ns,role in rows:
            face=[]
            for p,n in zip(ps,ns):
                key=tuple(round(c,7) for c in p)
                if key not in lookup:lookup[key]=len(vertices);vertices.append(p)
                face.append(lookup[key]);normals.append(n)
            faces.append(face);roles.append(role)
        me=bpy.data.meshes.new(name+' actual delivery triangles');me.from_pydata(vertices,[],faces);me.update()
        ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);ob['asset_set']='Sedan'
        for key,value in properties[name].items():ob[key]=value
        layer=me.attributes.new('sheet_role','INT','FACE')
        for face,role in zip(me.polygons,roles):layer.data[face.index].value=role;face.use_smooth=role!=2
        me.normals_split_custom_set(normals);result.append(ob)
        exact=me.attributes.new('DeliveryNormal','FLOAT_VECTOR','CORNER')
        for item,n in zip(exact.data,normals):item.vector=n
    if maximum>.00001:raise ValueError('Delivery naming correspondence exceeds 10 micrometers: '+str(maximum))
    return result,dict(triangles=samples,maximum_source_name_distance_m=maximum,
        scope='Source supplies part names/outer-face selection only; geometry and corner normals are freshly imported GLB data; float-vector corner attributes avoid a second packed-normal encoding')
