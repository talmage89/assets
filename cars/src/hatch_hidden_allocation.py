"""Retire redundant interior gauge samples; exterior corners stay byte-held."""
import bpy,bmesh,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform


def reduce(b):
    if b.high:return
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('part_category') not in ['body','doors','fascia','pillars']:continue
        me=ob.data;count=ob.get('outer_skin_faces')
        if count is None:continue
        role=me.attributes.get('hatch_outer_skin')
        if role is None:
            role=me.attributes.new('hatch_outer_skin','INT','FACE')
            for f in me.polygons:role.data[f.index].value=int(f.index<count)
        saved=me.attributes.new('H120 allocation held normals','FLOAT_VECTOR','CORNER')
        for row,n in zip(saved.data,me.corner_normals):row.vector=n.vector
        me.calc_loop_triangles();points=[];normals=[];faces=[]
        for t in me.loop_triangles:
            if not role.data[t.polygon_index].value:continue
            start=len(points)
            for vi,li in zip(t.vertices,t.loops):points.append(me.vertices[vi].co.copy());normals.append(me.corner_normals[li].vector.copy())
            faces.append((start,start+1,start+2))
        tree=BVHTree.FromPolygons(points,faces,all_triangles=True)
        accepted=False;retired=0;worst=0
        for angle in [5,2,1,.5]:
            bm=bmesh.new();bm.from_mesh(me);outer=bm.faces.layers.int['hatch_outer_skin']
            inner=[v for v in bm.verts if v.link_faces and all(not f[outer] and f.smooth for f in v.link_faces)]
            edges=[e for e in bm.edges if len(e.link_faces)==2 and all(not f[outer] and f.smooth for f in e.link_faces)]
            before=sum(len(f.verts)-2 for f in bm.faces)
            bmesh.ops.dissolve_limit(bm,angle_limit=math.radians(angle),use_dissolve_boundaries=False,verts=inner,edges=edges,delimit={'MATERIAL'})
            bmesh.ops.triangulate(bm,faces=[f for f in bm.faces if len(f.verts)>3]);bm.normal_update()
            maximum=-1
            for f in bm.faces:
                if f[outer] or not f.smooth:continue
                ps=[v.co for v in f.verts];center=sum(ps,Vector())/len(ps)
                for q in [center]+[(a+c)/2 for a,c in zip(ps,ps[1:]+ps[:1])]:
                    hit,_,fi,_=tree.find_nearest(q);a,c,d=faces[fi]
                    n=barycentric_transform(hit,points[a],points[c],points[d],normals[a],normals[c],normals[d]).normalized()
                    if f.normal.dot(n)>-.7:continue
                    maximum=max(maximum,(q-hit).dot(n))
            if maximum<=-.00035:
                retired=before-sum(len(f.verts)-2 for f in bm.faces);worst=maximum;bm.to_mesh(me);accepted=True;bm.free();break
            bm.free()
        saved=me.attributes['H120 allocation held normals']
        me.normals_split_custom_set([r.vector for r in saved.data]);me.attributes.remove(saved)
        me.calc_loop_triangles();ob['retired_inner_triangles']=retired
        ob['inner_allocation_accepted']=accepted;ob['inner_allocation_max_outward_m']=worst
        print('H120_INNER_ALLOCATION',ob.name,ob['retired_inner_triangles'],flush=True)


def covered_door_backs(b):
    """Cull only back faces proved covered by the actual moving door card."""
    if b.high:return
    from hatch_check import mesh_tree
    for side in ['L','R']:
        for end in ['F','R']:
            ob=bpy.data.objects['Door '+end+'_'+side];card=bpy.data.objects['H120 door card '+end+side]
            tree=mesh_tree([card]);me=ob.data;role=me.attributes.get('hatch_outer_skin');saved=me.attributes.new('H120 cull held normals','FLOAT_VECTOR','CORNER')
            for row,n in zip(saved.data,me.corner_normals):row.vector=n.vector
            bm=bmesh.new();bm.from_mesh(me);outer=bm.faces.layers.int['hatch_outer_skin'];remove=[];nm=ob.matrix_world.to_3x3().inverted().transposed()
            for f in bm.faces:
                if f[outer] or not f.smooth:continue
                # Back faces point into the cabin. Rims are held by their
                # adjacency to the outward sheet and never eligible.
                if any(other[outer] for e in f.edges for other in e.link_faces):continue
                direction=(nm@f.normal).normalized()
                if direction.x*(1 if side=='R' else -1)>-.65:continue
                ps=[ob.matrix_world@v.co for v in f.verts];center=sum(ps,Vector())/len(ps)
                probes=[center]+ps+[(a+c)/2 for a,c in zip(ps,ps[1:]+ps[:1])]
                if all(tree.ray_cast(p+direction*.001,direction,.10)[0] is not None for p in probes):remove.append(f)
            retired=sum(len(f.verts)-2 for f in remove)
            bmesh.ops.delete(bm,geom=remove,context='FACES');bm.to_mesh(me);bm.free()
            saved=me.attributes['H120 cull held normals'];me.normals_split_custom_set([r.vector for r in saved.data]);me.attributes.remove(saved)
            ob['allow_boundary']=True;ob['boundary_reason']='Reverse skin culled only where nine or fewer surface probes hit the moving inner door card within 100 mm; gauge returns retained'
            ob['covered_back_triangles_removed']=retired
            print('H120_COVERED_DOOR_BACK',ob.name,retired,flush=True)
