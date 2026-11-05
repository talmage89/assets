"""Resolve the small C-pillar reflection scallop on the held parent surface.

The dense, script-generated form supplies positions and corner normals. Only
interior edges in the narrow shoulder termination are split; cut outlines,
package, panel construction and every retained sample stay fixed.
"""
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform


def refine(b):
    if b.high:return
    path=Path(__file__).resolve().parents[1]/'build/hatch/high.blend'
    names=['Rear quarter_L','Rear quarter_R','Hood outer','Front fender_L','Front fender_R']
    with bpy.data.libraries.load(str(path),link=False) as (source,destination):destination.objects=list(names)
    dense=destination.objects;references={}
    for ob in dense:bpy.context.collection.objects.link(ob)
    bpy.context.view_layer.update()
    for name,ob in zip(names,dense):
        mesh=ob.data;mesh.calc_loop_triangles();ps=[];ns=[];fs=[]
        for tri in mesh.loop_triangles:
            if tri.polygon_index>=ob['outer_skin_faces']:continue
            offset=len(ps)
            for vi,li in zip(tri.vertices,tri.loops):
                ps.append(ob.matrix_world@mesh.vertices[vi].co)
                ns.append((ob.matrix_world.to_3x3().inverted().transposed()@mesh.corner_normals[li].vector).normalized())
            fs.append((offset,offset+1,offset+2))
        references[name]=(BVHTree.FromPolygons(ps,fs,all_triangles=True),ps,ns,fs)
    for name in names:
        ob=bpy.data.objects[name];tree,ps,ns,fs=references[name];matrix=ob.matrix_world;inverse=matrix.inverted()
        def sample(p):
            hit,_,fi,_=tree.find_nearest(p);a,c,d=fs[fi]
            normal=barycentric_transform(hit,ps[a],ps[c],ps[d],ns[a],ns[c],ns[d]).normalized()
            return hit,normal
        saved=ob.data.attributes.new('H120 held corner normals','FLOAT_VECTOR','CORNER')
        for row,n in zip(saved.data,ob.data.corner_normals):row.vector=n.vector
        if not ob.data.attributes.get('hatch_outer_skin'):
            role=ob.data.attributes.new('hatch_outer_skin','INT','FACE')
            for f in ob.data.polygons:role.data[f.index].value=int(f.index<ob['outer_skin_faces'])
        bm=bmesh.new();bm.from_mesh(ob.data);outer=bm.faces.layers.int.get('hatch_outer_skin')
        def zone(p):
            if name.startswith('Rear'):return 1.29<p.y<1.67 and .86<p.z<.965 and abs(p.x)>.80
            return -2.06<p.y<-1.20 and p.z>.70 and abs(p.x)>.54
        candidates=[]
        for e in bm.edges:
            p=matrix@((e.verts[0].co+e.verts[1].co)/2)
            if outer and len(e.link_faces)==2 and all(f[outer] for f in e.link_faces) and zone(p) and e.calc_length()>.018:candidates.append(e)
        bm.edges.index_update();added=0;max_move=0
        for e in sorted(candidates,key=lambda e:e.index)[:(48 if name.startswith('Rear') else 32)]:
            a,c=e.verts;p=matrix@((a.co+c.co)/2);hit,n=sample(p)
            if (hit-p).length>.002:continue
            _,v=bmesh.utils.edge_split(e,a,.5);v.co=inverse@hit;added+=1;max_move=max(max_move,(hit-p).length)
        bmesh.ops.triangulate(bm,faces=[f for f in bm.faces if len(f.verts)>3])
        bm.to_mesh(ob.data);bm.free();saved=ob.data.attributes['H120 held corner normals'];roles=ob.data.attributes.get('hatch_outer_skin')
        normal_matrix=matrix.to_3x3().transposed();custom=[]
        for face in ob.data.polygons:
            for li in face.loop_indices:
                p=matrix@ob.data.vertices[ob.data.loops[li].vertex_index].co
                custom.append(normal_matrix@sample(p)[1] if roles.data[face.index].value and zone(p) else saved.data[li].vector[:])
        ob.data.normals_split_custom_set(custom);ob.data.attributes.remove(saved)
        ob['detail_reflection_samples']=added;ob['detail_reflection_max_projection_m']=max_move
    for ob in dense:bpy.data.objects.remove(ob,do_unlink=True)
