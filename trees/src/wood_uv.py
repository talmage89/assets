"""Branch-axis UV seams on the actual fused woody surface.

Boolean face provenance separates the authored growth axes. Each branch gets
one longitudinal seam; junction and grade boundaries open into distinct islands.
The common finalizer performs the actual angle-based unwrap and atlas pack.
"""
import math
from mathutils import Vector
from settings import BARK_UV_CUTS


def seams(ob,records,stems):
    owners=ob.data.attributes.get('GrowthOwner')
    if owners is None:raise RuntimeError('Wood union lost face growth provenance')
    axes={r['index']:[Vector(p) for p in r['points']] for r in records}
    frames={}
    for owner,points in axes.items():
        previous=None;rows=[]
        for i,p in enumerate(points):
            tangent=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized()
            if previous is None:
                seed=Vector((1,0,0)) if abs(tangent.z)>.9 else Vector((0,0,1));u=tangent.cross(seed).normalized()
            else:u=(previous-tangent*previous.dot(tangent)).normalized()
            rows.append((u,tangent.cross(u).normalized()));previous=u
        frames[owner]=rows
    def angle(p,owner):
        points=axes[owner];best=None
        for i,(a,b) in enumerate(zip(points,points[1:])):
            d=b-a;t=max(0,min(1,(p-a).dot(d)/d.length_squared));q=a+d*t;distance=(p-q).length_squared
            if best is None or distance<best[0]:best=(distance,i,t,q)
        _,i,t,q=best;u=frames[owner][i][0].lerp(frames[owner][i+1][0],t).normalized()
        v=frames[owner][i][1].lerp(frames[owner][i+1][1],t).normalized();d=p-q
        return math.atan2(d.dot(v),d.dot(u))
    face_angles={f.index:angle(f.center,owners.data[f.index].value) for f in ob.data.polygons}
    edge_faces={e.index:[] for e in ob.data.edges};edge_index={tuple(sorted(e.vertices)):e.index for e in ob.data.edges}
    for face in ob.data.polygons:
        owner=owners.data[face.index].value
        if owner not in axes:raise RuntimeError('Unknown fused growth owner')
        for pair in face.edge_keys:edge_faces[edge_index[tuple(sorted(pair))]].append(face.index)
    for e in ob.data.edges:
        faces=edge_faces[e.index];groups={owners.data[i].value for i in faces}
        boundary=len(groups)>1 or len(faces)!=2
        if not boundary:
            owner=next(iter(groups))
            # The cut follows the shared edge BETWEEN faces on opposite sides
            # of the angular wrap. Testing endpoint angles cuts rings instead.
            boundary=abs(face_angles[faces[0]]-face_angles[faces[1]])>math.pi
            if not boundary:
                # The planar grade cap gets its own small island.
                boundary=any(abs(ob.data.polygons[i].normal.z)>.999 and ob.data.polygons[i].center.z<.01 for i in faces)
            if not boundary and stems[owner].level==0:
                # Compact, undistorted eye-height island between the flare and
                # unions; no extra vertices or triangles on the source surface.
                a,b=(ob.data.polygons[i].center.z for i in faces)
                boundary=any((a-z)*(b-z)<0 for z in BARK_UV_CUTS)
        e.use_seam=boundary
    priority=ob.data.attributes.new(name='BarkUVPriority',type='FLOAT',domain='FACE')
    for f,value in zip(ob.data.polygons,priority.data):
        level=stems[owners.data[f.index].value].level
        value.value={-1:1.3,0:3.4,1:1.1,2:.72,3:.60}.get(level,.60)
    ob['uv_policy']='Provenance junction boundaries plus one transported-axis longitudinal seam per branch; angle-based unwrap'
