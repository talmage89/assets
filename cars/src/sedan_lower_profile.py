"""A broad lower front molding with one fair side-view tangent.

The original rounded plan let the grille remove that tangent above the beam.
Flatten its central waterlines after the original conforming cuts, applying the
same invertible mold to every assembled source part and its sampled guides.
The held upper sheet (Z >= 660 mm), wheelhouses and rear are unchanged.
"""
import math
import bmesh
from mathutils import Vector
from mathutils.geometry import barycentric_transform


def falling(a,b,value):
    t=max(0.,min(1.,(value-a)/(b-a)))
    return 1-t*t*t*(10-15*t+6*t*t),-30*t*t*(1-t)*(1-t)/(b-a)


class LowerNoseMold:
    def __init__(self,surface):
        self.surface=surface;self.cache={}

    def front(self,x,z):
        s=self.surface;p,_,index,_=s['tree'].ray_cast(Vector((x,-4,z)),Vector((0,1,0)),4)
        if p is None or p.y> -1.75:return None
        a,c,d=s['triangles'][index]
        n=barycentric_transform(p,s['points'][a],s['points'][c],s['points'][d],s['normals'][a],s['normals'][c],s['normals'][d]).normalized()
        return p,n

    def shape(self,x,z):
        key=(round(abs(x),7),round(z,7))
        if key not in self.cache:
            xx=abs(x);wx,dwx=falling(.72,.84,xx);wz,dwz=falling(.53,.66,z)
            result=(0.,0.,0.)
            if wx*wz>0:
                side=self.front(xx,z);center=self.front(0,z)
                if side and center:
                    p,n=side;c,cn=center
                    if n.y<-.025 and cn.y<-.025:
                        loss=max(0.,p.y-c.y)
                        dx=-n.x/n.y;dz=-n.z/n.y+cn.z/cn.y
                        result=(loss*wx*wz,(dx*wx+loss*dwx)*wz,(dz*wz+loss*dwz)*wx)
            self.cache[key]=result
        value,dx,dz=self.cache[key]
        return value,dx*(1 if x>=0 else -1),dz

    def point(self,p):
        if p.y>=-1.86 or p.z>=.66 or abs(p.x)>=.84:return p.copy()
        value,_,_=self.shape(p.x,p.z);wy,_=falling(-2.06,-1.86,p.y)
        return p-Vector((0,value*wy,0))

    def normal(self,p,n):
        value,dx,dz=self.shape(p.x,p.z);wy,dwy=falling(-2.06,-1.86,p.y)
        determinant=1-value*dwy
        if determinant<.99:raise ValueError('Lower mold is not invertible')
        yy=n.y/determinant
        return Vector((n.x+dx*wy*yy,yy,n.z+dz*wy*yy)).normalized()

    def apply(self,objects):
        for ob in objects:
            if ob.type!='MESH':continue
            mesh=ob.data;world=ob.matrix_world;inverse=world.inverted()
            positions=[world@v.co for v in mesh.vertices]
            mapped=[self.point(p) for p in positions]
            changed={i for i,(p,q) in enumerate(zip(positions,mapped)) if (p-q).length>1e-9}
            if not changed:continue
            old=[n.vector.copy() for n in mesh.corner_normals]
            to_world=world.to_3x3().inverted().transposed();to_local=world.to_3x3().transposed()
            normals=[]
            for loop,n in zip(mesh.loops,old):
                i=loop.vertex_index
                normals.append((to_local@self.normal(positions[i],(to_world@n).normalized())).normalized() if i in changed else n)
            for i in changed:mesh.vertices[i].co=inverse@mapped[i]
            mesh.update();mesh.normals_split_custom_set(normals)
            for name in ['aperture_samples','well_mouth_samples']:
                if name not in ob:continue
                raw=list(ob[name]);points=[self.point(Vector(raw[i:i+3])) for i in range(0,len(raw),3)]
                ob[name]=[v for p in points for v in p]
            ob['lower_mold_max_shift_m']=max((mapped[i]-positions[i]).length for i in changed)


def finish_sheet(ob):
    """Retile distorted cut cells and reseat protected game gauge backs."""
    roles=ob.data.attributes.get('sheet_role')
    if roles is None:return
    def key(p):return tuple(round(v,7) for v in p)
    wanted={key(ob.data.vertices[ob.data.loops[li].vertex_index].co):ob.data.corner_normals[li].vector.copy()
            for face in ob.data.polygons if roles.data[face.index].value==0 for li in face.loop_indices}
    bm=bmesh.new();bm.from_mesh(ob.data);layer=bm.faces.layers.int['sheet_role']
    bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.normal_update()
    def score(face):
        normal=sum((wanted.get(key(v.co),face.normal) for v in face.verts),Vector()).normalized()
        return face.normal.dot(normal)
    flips=0
    for iteration in range(12):
        bad=[f for f in bm.faces if f[layer]==0 and f.calc_area()>1e-10 and score(f)<.05]
        if not bad:break
        face=bad[0];fixed=False;bm.edges.index_update()
        for edge in sorted(face.edges,key=lambda e:e.index):
            if len(edge.link_faces)!=2 or any(f[layer]!=0 for f in edge.link_faces):continue
            result=bmesh.ops.rotate_edges(bm,edges=[edge],use_ccw=False)
            if not result['edges']:continue
            rotated=result['edges'][0];bm.normal_update()
            if all(score(f)>.05 for f in rotated.link_faces):flips+=1;fixed=True;break
            bmesh.ops.rotate_edges(bm,edges=[rotated],use_ccw=True);bm.normal_update()
        if not fixed:
            bm.verts.index_update()
            for vertex in list(face.verts):
                if vertex.is_boundary or any(f[layer]!=0 for f in vertex.link_faces):continue
                trial=bm.copy();trial.verts.ensure_lookup_table();trial_layer=trial.faces.layers.int['sheet_role']
                bmesh.ops.dissolve_verts(trial,verts=[trial.verts[vertex.index]],use_face_split=False,use_boundary_tear=False)
                bmesh.ops.triangulate(trial,faces=list(trial.faces));trial.normal_update()
                if all(score(f)>.05 for f in trial.faces if f[trial_layer]==0 and f.calc_area()>1e-10):
                    bm.free();bm=trial;layer=trial_layer;fixed=True;flips+=1;break
                trial.free()
        if not fixed:raise ValueError(('Lower molding needs a finer physical cell',ob.name))
    bm.to_mesh(ob.data);bm.free()
    roles=ob.data.attributes['sheet_role'];material=ob.data.materials[0]
    while len(ob.data.materials)<3:ob.data.materials.append(material)
    for face in ob.data.polygons:face.material_index=roles.data[face.index].value
    from sedan_detail import seat_inner_sheet
    seat_inner_sheet(ob)
    normals=[]
    for face in ob.data.polygons:
        for li in face.loop_indices:
            p=ob.data.vertices[ob.data.loops[li].vertex_index].co
            normals.append(wanted.get(key(p),(0,0,0)) if roles.data[face.index].value==0 else (0,0,0))
        face.material_index=0
    ob.data.materials.clear();ob.data.materials.append(material);ob.data.normals_split_custom_set(normals)
    ob['lower_mold_repaired_diagonals']=flips
    print('S240_LOWER_MOLD_DIAGONALS',flips,flush=True)
