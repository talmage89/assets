"""Fair molded glazing in its own injective optical chart.

The stamped-body UV chart folds at the A-foot and backlight corners. A glass
disk must not inherit those folds. Retain its projected physical perimeter,
fit its own smooth manufactured sag, and triangulate in YZ (side) or XZ (rear).
Both laminate layers share the same parametric normal field.
"""
import json
import bpy
import numpy as np
from mathutils import Vector
from mathutils.geometry import delaunay_2d_cdt
from kit import model as G


def normal(rec,u,v):
    a=(u-rec['center'][0])/rec['scale'][0];b=(v-rec['center'][1])/rec['scale'][1]
    du=sum(c*i*a**(i-1)*b**j for (i,j),c in zip(rec['powers'],rec['coefficients']) if i)/rec['scale'][0]
    dv=sum(c*j*a**i*b**(j-1) for (i,j),c in zip(rec['powers'],rec['coefficients']) if j)/rec['scale'][1]
    return Vector((-du,1,-dv) if rec['rear'] else (rec['sign'],-du,-dv)).normalized()


def field(ob):
    rec=json.loads(ob['optical_patch']);me=ob.data
    uv=me.attributes['OpticalParam'];ns=me.attributes.get('BodyNormal') or me.attributes.new('BodyNormal','FLOAT_VECTOR','POINT')
    for d,q in zip(ns.data,uv.data):d.vector=normal(rec,q.vector.x,q.vector.y)
    # The explicit roles are generated on this disk, not inferred from a folded
    # steel chart. Its independently constructed winding is consistent.
    inverse=ob.matrix_world.to_3x3().transposed();role=me.attributes['skin_face_role'];custom=[]
    for f in me.polygons:
        r=role.data[f.index].value;f.use_smooth=r!=2
        for li in f.loop_indices:
            vi=me.loops[li].vertex_index;n=ns.data[vi].vector
            custom.append(f.normal if r==2 else inverse@(n if r==0 else -n))
    me.normals_split_custom_set(custom)
    ob['normal_basis']='Own C2 optical sag patch; shared OpticalParam on entrance/exit; flat gauge rims'


def fair(ob,high=False):
    old=ob.data;world=ob.matrix_world;inverse=world.inverted()
    rear=ob.name=='Backlight';axis=1 if rear else 0;sgn=1 if rear or ob.name.endswith('_R') else -1
    # These original authored construction guides precede the folded steel-UV
    # hull. Use their real ordered border, never that hull's crossed projection.
    raw=list(ob['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    coords=[Vector((p.x if rear else p.y,p.z)) for p in ps]
    from suv_apertures import boundary_indices
    outline=boundary_indices(ob['form_columns'],ob['form_rows'])[::2]
    xy=np.array([tuple(p) for p in coords]);center=xy.mean(axis=0);scale=np.maximum(xy.std(axis=0),.1);q=(xy-center)/scale
    degree=5 if rear else 3;powers=[(i,total-i) for total in range(degree+1) for i in range(total+1)]
    A=np.column_stack([q[:,0]**i*q[:,1]**j for i,j in powers]);w=np.array([p[axis]*sgn-(0 if rear else .006) for p in ps])
    co=np.linalg.lstsq(A,w,rcond=None)[0];residual=A@co-w
    rec=dict(rear=rear,sign=sgn,center=center.tolist(),scale=scale.tolist(),powers=powers,coefficients=co.tolist(),fit_residual_p50_p95_max_m=np.percentile(abs(residual),[50,95,100]).tolist(),inset_m=.0015)
    # An inward collar makes every curved border segment connect to a nearby
    # interior sample. Unconstrained CDT otherwise makes long, almost-collinear
    # three-border-vertex fans whose 3D chords face against the glass normal.
    collar=[];middle=sum((coords[i] for i in outline),Vector((0,0)))/len(outline)
    for i in outline:
        p=coords[i];collar.append(len(coords));coords.append(p.lerp(middle,min(.25,.026/(p-middle).length)))
    constraints=list(zip(outline,outline[1:]+outline[:1]))+list(zip(collar,collar[1:]+collar[:1]))+list(zip(outline,collar))
    def away(p):
        distances=[]
        for a,c in zip(outline,outline[1:]+outline[:1]):
            edge=coords[c]-coords[a];t=max(0,min(1,(p-coords[a]).dot(edge)/edge.length_squared));distances.append((p-coords[a]-edge*t).length)
        return min(distances)>.014
    if not high:
        # Uniform chart coverage, not a geometric decimator that can flatten a
        # whole shallow pane. Boundary stations are retained, then farthest
        # points fill the interior; shared analytic normals survive both layers.
        keep=set(outline+collar);target=max(len(keep)+1,96 if rear else 50 if ob.name.startswith('Front') else 32)
        available=[i for i,p in enumerate(coords) if i not in keep and away(p)]
        while len(keep)<target and available:
            i=max(available,key=lambda i:min((coords[i]-coords[j]).length_squared for j in keep))
            available.remove(i)
            keep.add(i)
        keep=sorted(keep);lookup={old:i for i,old in enumerate(keep)}
        coords=[coords[i] for i in keep];outline=[lookup[i] for i in outline];constraints=[(lookup[a],lookup[c]) for a,c in constraints]
    else:
        # Retain denser high interior coverage, but discard the redundant
        # near-border steel-guide points that recreate tiny curved-edge ears.
        keep=sorted(set(outline+collar+[i for i,p in enumerate(coords) if away(p)]));lookup={old:i for i,old in enumerate(keep)}
        coords=[coords[i] for i in keep];outline=[lookup[i] for i in outline];constraints=[(lookup[a],lookup[c]) for a,c in constraints]
    result,_,tris,*_=delaunay_2d_cdt(coords,constraints,[outline],1,1e-7)
    used=sorted({i for f in tris for i in f});remap={v:i for i,v in enumerate(used)}
    result=[result[i] for i in used];tris=[tuple(remap[i] for i in f) for f in tris]
    vertices=[]
    for p in result:
        a=(p.x-center[0])/scale[0];b=(p.y-center[1])/scale[1]
        sag=sum(c*a**i*b**j for c,(i,j) in zip(co,powers))-.0015
        point=Vector((p.x,sag,p.y)) if rear else Vector((sgn*sag,p.x,p.y))
        vertices.append(inverse@point)
    me=bpy.data.meshes.new(old.name+' fair optical patch');me.from_pydata(vertices,[],tris);me.update()
    for mat in old.materials:me.materials.append(mat)
    ob.data=me
    direction=Vector((0,1,0)) if rear else Vector((sgn,0,0))
    for f in me.polygons:
        if (world.to_3x3()@f.normal).dot(direction)<0:f.flip()
    uv=me.attributes.new('OpticalParam','FLOAT_VECTOR','POINT')
    for d,p in zip(uv.data,result):d.vector=(*p,0)
    # Attribute provenance survives Solidify and the later game reduction.
    for _ in range(2):me.materials.append(me.materials[0])
    sol=ob.modifiers.new('Fair optical laminate','SOLIDIFY');sol.thickness=.0048;sol.offset=-1;sol.use_even_offset=False;sol.material_offset=1;sol.material_offset_rim=2;G.apply(ob)
    role=ob.data.attributes.new('skin_face_role','INT','FACE')
    for f in ob.data.polygons:role.data[f.index].value=f.material_index;f.material_index=0
    mat=ob.data.materials[0];ob.data.materials.clear();ob.data.materials.append(mat)
    ob['optical_patch']=json.dumps(rec);ob['optical_construction']='Own injective YZ/XZ disk and C2 sag, retaining generated physical perimeter; 4.8 mm laminate'
    field(ob)
    if old.users==0:bpy.data.meshes.remove(old)


def build(high=False):
    for ob in list(bpy.context.scene.objects):
        if ob.type=='MESH' and ('side glazing_' in ob.name or ob.name=='Backlight'):fair(ob,high)
