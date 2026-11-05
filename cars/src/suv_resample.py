"""Constrained post-cut chart tessellation; positions come from the fair parent.

Cut extensions used to leave long thin triangle chains and mix plane-interpolated
and limit-projected points. Rebuild only their exterior disk with boundary edges
as constraints. Hole membership is measured in the old chart, never guessed from
the convex hull. This changes geometry, not the curvature diagnostic.
"""
import math
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import delaunay_2d_cdt
from kit import model as G


def remesh(ob,surface,step=.5):
    from suv_apertures import surface_uv,evaluate_chart
    from suv_body import skin_gauge,closeable_sheet
    mesh=ob.data;mesh.calc_loop_triangles();world=ob.matrix_world;inverse=world.inverted()
    triangles=[tuple(t.vertices) for t in mesh.loop_triangles if t.material_index==0]
    used=sorted({i for f in triangles for i in f});lookup={v:i for i,v in enumerate(used)}
    points=[world@mesh.vertices[i].co for i in used]
    uv=[surface_uv(p,surface)[0] for p in points]
    triangles=[tuple(lookup[i] for i in f) for f in triangles]
    domain=BVHTree.FromPolygons(uv,triangles,all_triangles=True)
    edges={}
    for f in triangles:
        for a,c in zip(f,f[1:]+f[:1]):
            e=tuple(sorted((a,c)));edges[e]=edges.get(e,0)+1
    boundary=[e for e,n in edges.items() if n==1]
    retained=sorted({i for e in boundary for i in e});index={v:i for i,v in enumerate(retained)}
    coords=[uv[i].to_2d() for i in retained]
    constraints=[tuple(index[i] for i in e) for e in boundary]
    border_points=[p.copy() for p in coords]
    for j in range(math.ceil(min(p.y for p in uv)/step),math.floor(max(p.y for p in uv)/step)+1):
        for i in range(math.ceil(min(p.x for p in uv)/step),math.floor(max(p.x for p in uv)/step)+1):
            q=Vector(((i+.5*(j%2))*step,j*step,0))
            hit,_,_,dist=domain.find_nearest(q)
            if hit is not None and dist<1e-6 and min((q.to_2d()-p).length for p in border_points)>step*.32:
                coords.append(q.to_2d())
    result,_,faces,originals,*_=delaunay_2d_cdt(coords,constraints,[],0,1e-7)
    faces=[tuple(f) for f in faces if domain.find_nearest(Vector((*((sum((result[i] for i in f),Vector((0,0)))/len(f))),0)))[3]<1e-6]
    selected=sorted({i for f in faces for i in f});new={v:i for i,v in enumerate(selected)};verts=[]
    for i in selected:
        original=next((j for j in originals[i] if j<len(retained)),None)
        p=evaluate_chart(result[i],surface)[0]
        verts.append(inverse@p)
    candidate=bpy.data.meshes.new(mesh.name+' constrained chart');candidate.from_pydata(verts,[],[tuple(new[i] for i in f) for f in faces]);candidate.update()
    candidate.materials.append(mesh.materials[0]);ob.data=candidate
    for f in candidate.polygons:
        _,n=surface_uv(world@f.center,surface)
        if (world.to_3x3()@f.normal).dot(n)<0:f.flip()
    closeable_sheet(ob)
    skin_gauge(ob,.003 if ob.get('part_category') in ['fascia','cladding'] else .0009)
    ob['cut_resampling']='Boundary-constrained chart CDT; parent positions; unsmoothed measured curvature'
    if mesh.users==0:bpy.data.meshes.remove(mesh)
