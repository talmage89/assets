"""Small batched meshes. Reuse the kit's stock sections and glTF exporter."""
import math
import bpy
import bmesh
from mathutils import Vector
from kit import model

M={}


def root(name, pos=(0,0,0), parent=None, **props):
    ob=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(ob)
    ob.location=pos;ob.parent=parent
    for k,v in props.items(): ob[k]=v
    return ob


def descendants(ob): return [ob]+list(ob.children_recursive)


class Batch:
    def __init__(self,name,parent=None,category='bridge'):
        self.name=name;self.parent=parent;self.category=category
        self.v=[];self.f=[];self.roles=[];self.colors=[];self.uv=[];self.smooth=[]

    def geom(self,vs,fs,role='concrete',color=(1,1,1,1),uv=None,smooth=False,up=False):
        vs=[tuple(p) for p in vs];n=len(self.v);self.v.extend(vs)
        for f in fs:
            if up and (Vector(vs[f[1]])-Vector(vs[f[0]])).cross(Vector(vs[f[2]])-Vector(vs[f[0]])).z<0:
                f=tuple(reversed(f))
            self.f.append(tuple(n+i for i in f));self.roles.append(role)
            self.colors.append(color);self.uv.append(uv);self.smooth.append(smooth)

    def box(self,p,s,role='concrete',color=(1,1,1,1)):
        x,y,z=p;a,b,c=[q/2 for q in s]
        vs=[(x+i*a,y+j*b,z+k*c) for i,j,k in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))]
        self.geom(vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],role,color)

    def loft(self,rings,role='concrete',color=(1,1,1,1),caps=True,smooth=False):
        n=len(rings[0]);vs=[p for r in rings for p in r]
        fs=[(j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k) for j in range(len(rings)-1) for k in range(n)]
        if caps: fs.extend([tuple(reversed(range(n))),tuple(range(len(vs)-n,len(vs)))])
        self.geom(vs,fs,role,color,smooth=smooth)

    def tube(self,pts,r,role='steel',n=8,thickness=0,caps=True):
        pts=list(map(Vector,pts));rings=[];inner=[]
        for i,p in enumerate(pts):
            t=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized()
            u=t.cross(Vector((0,0,1)) if abs(t.z)<.95 else Vector((1,0,0))).normalized();v=t.cross(u)
            rings.append([p+r*(u*math.cos(j*math.tau/n)+v*math.sin(j*math.tau/n)) for j in range(n)])
            if thickness:inner.append([p+(r-thickness)*(u*math.cos(j*math.tau/n)+v*math.sin(j*math.tau/n)) for j in range(n)])
        if thickness:self.loft(rings+list(reversed(inner))+[rings[0]],role,caps=False,smooth=True)
        else:self.loft(rings,role,smooth=True,caps=caps)

    def cylinder(self,p,r,h,role='concrete',n=24,caps=True):
        x,y,z=p
        self.loft([[(x+r*math.cos(i*math.tau/n),y+r*math.sin(i*math.tau/n),z+zz) for i in range(n)] for zz in (-h/2,h/2)],role,smooth=True,caps=caps)

    def beam(self,a,b,w,d=None,role='steel',caps=True):
        a,b=Vector(a),Vector(b);q=(b-a).to_track_quat('Z','Y').to_matrix();p=(a+b)/2
        vs=[p+q@Vector((i*w/2,j*(d or w)/2,k*(b-a).length/2)) for i,j,k in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))]
        fs=[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
        self.geom(vs,([(0,3,2,1),(4,5,6,7)]+fs) if caps else fs,role)

    def finish(self):
        me=bpy.data.meshes.new(self.name);me.from_pydata(self.v,[],self.f);me.update()
        roles=list(dict.fromkeys(self.roles))
        for role in roles: me.materials.append(M[role])
        uv=me.uv_layers.new(name='UVMap');vc=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER')
        for f,role,col,coords,sm in zip(me.polygons,self.roles,self.colors,self.uv,self.smooth):
            f.material_index=roles.index(role);f.use_smooth=sm
            axes=sorted(range(3),key=lambda k:abs(f.normal[k]))[:2]
            coverage=6.096 if role=='asphalt' else 3.048 if role in ('concrete','bridge_concrete','zinc','grass') else 2
            for j,li in enumerate(f.loop_indices):
                v=me.vertices[me.loops[li].vertex_index].co
                if role.startswith('paint_'):
                    paintuv=[(.005,.755),(.495,.755),(.495,.995),(.005,.995)]
                    uv.data[li].uv=paintuv[j]
                else:uv.data[li].uv=coords[j] if coords else (v[axes[0]]/coverage,v[axes[1]]/coverage)
                vc.data[li].color=col
        bm=bmesh.new();bm.from_mesh(me);bm.normal_update()
        # Solid components need outward recalculation. Isolated authored
        # terrain/decal faces have no inside: retain their explicit winding.
        authored={f:f.normal.copy() for f in bm.faces if all(e.is_boundary for e in f.edges)}
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
        bmesh.ops.reverse_faces(bm,faces=[f for f,n in authored.items() if f.normal.dot(n)<0])
        bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='FIXED',ngon_method='EAR_CLIP');bm.to_mesh(me);bm.free();me.update()
        ob=bpy.data.objects.new(self.name,me);bpy.context.collection.objects.link(ob);ob.parent=self.parent
        ob['river_category']=self.category;ob['asset_set']='River'
        return ob


def path(name,points,parent,kind,**props):
    # glTF has no curve primitive. Samples are local to this identity root.
    import json
    ob=root(name,parent=parent,socket_kind=kind,points_blender_m=json.dumps(points),
            points_gltf_m=json.dumps([(x,z,-y) for x,y,z in points]),**props)
    return ob
