"""Signed discrete mean curvature of the H120 game skins, in inverse meters.

Measures actual triangle geometry, never the authored shading normals. Uses
the cotangent Laplace--Beltrami operator and mixed Voronoi dual areas, with
half/quarter areas for obtuse triangles. H = -dot(L(position), normal)/2.
This avoids an area-dependent bias on irregular aperture triangles without
spatial smoothing. Open cut boundaries have incomplete
neighborhoods and are gray, not silently assigned zero curvature. No smoothing
or outlier removal is applied. Gauge rims and separate inserts remain gray.
"""
import json,math
from collections import defaultdict
import bpy
from mathutils import Vector

COLORS=[(-1,(.035,.07,.55,1)),(-.5,(.02,.55,.95,1)),(0,(.12,.55,.16,1)),(.5,(1,.65,.02,1)),(1,(.7,.015,.025,1))]

def color(value):
    t=max(-1,min(1,math.asinh(value/2)/math.asinh(40/2)))
    for (a,ca),(b,cb) in zip(COLORS,COLORS[1:]):
        if a<=t<=b:return tuple(x+(y-x)*(t-a)/(b-a) for x,y in zip(ca,cb))
    return COLORS[0 if t<0 else -1][1]


def outer_faces(ob):
    mesh=ob.data
    role=mesh.attributes.get('hatch_outer_skin')
    if role:return {f.index for f in mesh.polygons if role.data[f.index].value}
    count=ob.get('outer_skin_faces')
    if count is not None:return set(range(min(count,len(mesh.polygons))))
    return set()


def measure(ob):
    mesh=ob.data;mesh.calc_loop_triangles();outer=outer_faces(ob)
    points=[ob.matrix_world@v.co for v in mesh.vertices]
    areas=defaultdict(float);edges=defaultdict(list);faces=[];normal_error=[]
    laplace=defaultdict(Vector);normals=defaultdict(Vector)
    nm=ob.matrix_world.to_3x3().inverted().transposed()
    for t in mesh.loop_triangles:
        if t.polygon_index not in outer:continue
        ids=tuple(t.vertices);a,b,c=[points[i] for i in ids]
        cross=(b-a).cross(c-a);area=cross.length/2
        if area<1e-14:continue
        n=cross.normalized();faces.append((ids,n,area,t.polygon_index))
        ps=[a,b,c]
        cot=[(ps[(i+1)%3]-ps[i]).dot(ps[(i+2)%3]-ps[i])/cross.length for i in range(3)]
        obtuse=next((i for i,v in enumerate(cot) if v<0),None)
        for k,i in enumerate(ids):
            j,l=(k+1)%3,(k+2)%3
            areas[i]+=(area*(.5 if k==obtuse else .25) if obtuse is not None else
                       ((ps[j]-ps[k]).length_squared*cot[l]+(ps[l]-ps[k]).length_squared*cot[j])/8)
            normals[i]+=cross
            laplace[i]+=(ps[j]-ps[k])*cot[l]+(ps[l]-ps[k])*cot[j]
        for i,j in zip(ids,ids[1:]+ids[:1]):edges[tuple(sorted((i,j)))].append((i,j,n))
        shading=sum(((nm@mesh.corner_normals[li].vector).normalized() for li in t.loops),Vector()).normalized()
        normal_error.append((math.degrees(n.angle(shading)),area,list((a+b+c)/3),t.polygon_index))
    boundary=set();nonmanifold=0
    for edge,rows in edges.items():
        if len(rows)!=2:
            boundary.update(edge);nonmanifold+=len(rows)>2;continue
    values={i:-laplace[i].dot(normals[i].normalized())/(4*area) for i,area in areas.items() if i not in boundary and area>1e-12}
    worst=sorted(((abs(v),v,list(points[i]),i) for i,v in values.items()),reverse=True)[:30]
    return values,boundary,dict(vertices=len(values),boundary_vertices=len(boundary),nonmanifold_edges=nonmanifold,
       range_m_inv=[min(values.values(),default=0),max(values.values(),default=0)],
       worst=[dict(H_m_inv=v,point_m=p,vertex=i) for _,v,p,i in worst],
       normal_mismatch=sorted(normal_error,reverse=True)[:30])


def apply():
    """Color actual game exterior triangles; retain original scene geometry."""
    mat=bpy.data.materials.new('H120 signed mean curvature');mat.use_nodes=True
    n=mat.node_tree.nodes;l=mat.node_tree.links;n.clear()
    attr=n.new('ShaderNodeVertexColor');attr.layer_name='H120 mean curvature'
    emission=n.new('ShaderNodeEmission');l.new(attr.outputs['Color'],emission.inputs['Color'])
    output=n.new('ShaderNodeOutputMaterial');l.new(emission.outputs[0],output.inputs['Surface'])
    gray=bpy.data.materials.new('Curvature unmeasured');gray.diffuse_color=(.08,.08,.08,1)
    records={}
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('studio'):continue
        if not outer_faces(ob):values={};outer=set()
        else:
            values,boundary,record=measure(ob);records[ob.name]=record
        layer=ob.data.color_attributes.new(name='H120 mean curvature',type='FLOAT_COLOR',domain='CORNER')
        ob.data.color_attributes.active_color=layer
        outer=outer_faces(ob)
        for face in ob.data.polygons:
            face.material_index=0
            for li in face.loop_indices:
                vi=ob.data.loops[li].vertex_index
                layer.data[li].color=color(values[vi]) if face.index in outer and vi in values else (.08,.08,.08,1)
        ob.data.materials.clear();ob.data.materials.append(mat)
    return dict(method=__doc__,scale_m_inv=[-40,40],mapping='asinh(H/2) / asinh(20); blue negative, green zero, red positive; gray incomplete or unmeasured',parts=records)


def calibrate():
    """Independent analytic plane, cylinder and unit-sphere checks."""
    records={}
    for name,expected in [('plane',0.0),('cylinder',1/.6),('sphere',1.0)]:
        if name=='sphere':
            bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,radius=1)
            ob=bpy.context.object
        else:
            nu,nv=(16,16) if name=='plane' else (64,12)
            ps=[((i/nu,j/nv,0) if name=='plane' else
                 (.3*math.cos(math.tau*i/nu),.3*math.sin(math.tau*i/nu),j/nv))
                for j in range(nv+1) for i in range(nu if name=='cylinder' else nu+1)]
            stride=nu if name=='cylinder' else nu+1
            fs=[(j*stride+i,j*stride+(i+1)%stride,(j+1)*stride+(i+1)%stride,(j+1)*stride+i)
                for j in range(nv) for i in range(nu)]
            mesh=bpy.data.meshes.new('Curvature calibration');mesh.from_pydata(ps,[],fs);mesh.update()
            ob=bpy.data.objects.new('Curvature calibration',mesh);bpy.context.scene.collection.objects.link(ob)
        ob['outer_skin_faces']=len(ob.data.polygons);values,_,_=measure(ob)
        error=max(abs(v-expected) for v in values.values())
        records[name]=dict(expected_m_inv=expected,measured_range_m_inv=[min(values.values()),max(values.values())],maximum_error_m_inv=error,passed=error<.005)
        mesh=ob.data;bpy.data.objects.remove(ob,do_unlink=True);bpy.data.meshes.remove(mesh)
    if not all(r['passed'] for r in records.values()):raise AssertionError(records)
    return records


if __name__=='__main__':print(json.dumps(calibrate(),indent=2))
