"""Fresh GLB surfaces for expanded fairness views; source supplies names only."""
import bpy
from mathutils import Vector
from mathutils.kdtree import KDTree

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
    # Nearest-surface BVHs can miss very slender gauge triangles. Match whole
    # triangles by centroid candidates and both directions of vertex distance;
    # attribution must not silently jump from a thin cap onto its side wall.
    centers=KDTree(len(triangles))
    for i,ids in enumerate(triangles):centers.insert(sum((points[k] for k in ids),Vector())/3,i)
    centers.balance()
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(glb))
    groups={};maximum=0.;maximum_center=0.;samples=0
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH':continue
        me=ob.data;me.calc_loop_triangles();normal_matrix=ob.matrix_world.to_3x3().inverted().transposed()
        for tri in me.loop_triangles:
            ps=[ob.matrix_world@me.vertices[i].co for i in tri.vertices]
            ns=[(normal_matrix@me.corner_normals[i].vector).normalized() for i in tri.loops]
            center=sum(ps,Vector())/3;candidates=centers.find_range(center,.00001)
            def vertex_error(index):
                qs=[points[k] for k in triangles[index]]
                return max(max(min((p-q).length for q in qs) for p in ps),max(min((q-p).length for p in ps) for q in qs))
            if not candidates:raise ValueError('Delivery triangle has no source centroid within 10 micrometers: '+str(tuple(center)))
            _,fi,center_distance=min(candidates,key=lambda row:vertex_error(row[1]));distance=vertex_error(fi)
            if distance>.00001:raise ValueError('Delivery triangle vertex correspondence exceeds 10 micrometers: '+str(distance))
            maximum=max(maximum,distance);maximum_center=max(maximum_center,center_distance);samples+=1;name,role=owners[fi]
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
    return result,dict(triangles=samples,maximum_source_name_vertex_distance_m=maximum,maximum_source_name_centroid_distance_m=maximum_center,
        matching='Whole-triangle centroid candidates and bidirectional vertex correspondence, each within 10 micrometers',
        scope='Source supplies part names/outer-face selection only; geometry and corner normals are freshly imported GLB data; float-vector corner attributes avoid a second packed-normal encoding')
