"""Fuel flap sampled along the quarter's actual shoulder, not a flat ngon."""
import math
import bpy
from mathutils import Vector
from mathutils.geometry import delaunay_2d_cdt
from hatch_reference_surface import field
from hatch_body import shoulder_height


def build(b):
    count=48 if b.high else 24;parent=field();origin_y,origin_z=1.62,.91;radius=.070
    rows=([-.065,-.055,-.045,-.030,-.018,-.009,0,.009,.018,.030,.045,.055,.065] if b.high else [-.060,-.035,-.018,-.009,0,.009,.018,.035,.060])
    columns=11 if b.high else 7;uv=[];constraints=[];boundary=set();slope=.012;delta=shoulder_height(origin_y)-origin_z
    # v = z - shoulder(y). Exact row constraints keep the reflected crease
    # continuous through the disk, without the radial fan's central pimple.
    for v in rows:
        a=1+slope*slope;bb=2*slope*(v+delta);c=(v+delta)**2-radius*radius;disc=bb*bb-4*a*c
        if disc<=0:continue
        lo=(-bb-math.sqrt(disc))/(2*a);hi=(-bb+math.sqrt(disc))/(2*a);ids=[]
        for k in range(columns):ids.append(len(uv));uv.append(Vector((lo+(hi-lo)*k/(columns-1),v)))
        boundary.update([ids[0],ids[-1]]);constraints.extend(zip(ids,ids[1:]))
    for i in range(count):
        angle=math.tau*i/count;y=radius*math.cos(angle);z=radius*math.sin(angle)
        q=Vector((y,z-delta-slope*y))
        if min((q-uv[j]).length for j in boundary)<.0015:continue
        boundary.add(len(uv));uv.append(q)
    perimeter=sorted(boundary,key=lambda i:math.atan2(uv[i].y+delta+slope*uv[i].x,uv[i].x))
    constraints.extend(zip(perimeter,perimeter[1:]+perimeter[:1]))
    coords,_,faces,*_=delaunay_2d_cdt(uv,constraints,[],1,1e-7)
    faces=list({tuple(sorted(f)):tuple(reversed(f)) for f in faces}.values())
    used=sorted({i for f in faces for i in f});remap={v:i for i,v in enumerate(used)};coords=[coords[i] for i in used];faces=[tuple(remap[i] for i in f) for f in faces]
    points=[];normals=[]
    for q in coords:
        y=origin_y+q.x;z=shoulder_height(y)+q.y;sample=parent((-2,y,z),(1,0,0))
        if sample is None:raise ValueError('Fuel flap missed parent')
        p,n,_=sample;points.append(p+n*.0013);normals.append(n)
    outer=len(faces);num=len(points);edges={}
    for f in faces:
        for a,c in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted((a,c))),[]).append((a,c))
    boundary=sorted({i for e,rr in edges.items() if len(rr)==1 for i in e})
    if b.high:
        points += [p-n*.0009 for p,n in zip(points,normals)];faces += [tuple(i+num for i in reversed(f)) for f in faces[:outer]];back={i:i+num for i in boundary}
    else:
        back={i:num+k for k,i in enumerate(boundary)};points += [points[i]-normals[i]*.0009 for i in boundary]
    faces += [(c,a,back[a],back[c]) for rr in edges.values() if len(rr)==1 for a,c in rr]
    mesh=bpy.data.meshes.new('H120 shoulder aligned fuel flap');mesh.from_pydata(points,[],faces);mesh.update();mesh.materials.append(b.m['body'])
    ob=bpy.data.objects.new('H120 fuel flap',mesh);bpy.context.collection.objects.link(ob);custom=[]
    for f in mesh.polygons:
        f.use_smooth=f.index<outer or b.high and f.index<2*outer
        for li in f.loop_indices:
            vi=mesh.loops[li].vertex_index
            custom.append(normals[vi] if f.index<outer else -normals[vi-num] if b.high and f.index<2*outer else f.normal)
    mesh.normals_split_custom_set(custom);ob['outer_skin_faces']=outer
    if not b.high:ob['allow_boundary']=True;ob['boundary_reason']='Buried reverse fuel-flap skin omitted against the quarter; compound disk and gauge return retained'
    b.add(ob,category='trim')
