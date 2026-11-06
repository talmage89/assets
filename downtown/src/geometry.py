"""Batched architectural solids and measured wall openings.

Kit meshes/normals/export remain stock. This accumulator carries per-part
construction semantics and face UVs without thousands of Blender operators.
"""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix
from kit import model as G
ROLES=('Masonry','Mineral','Finish','Roof','Glass','Graphics')
COLORS={'Masonry':(.27,.10,.05),'Mineral':(.43,.39,.30),'Finish':(.055,.075,.065),'Roof':(.075,.08,.075),'Glass':(.92,.96,.97),'Graphics':(1,1,1)}


def palette(sheet):
    mats=[]
    for role in ROLES:
        m=bpy.data.materials.new('Downtown_'+role);m.use_nodes=True;m['checkpoint_placeholder']=True
        n=m.node_tree.nodes;p=n.get('Principled BSDF');l=m.node_tree.links
        p.inputs['Roughness'].default_value={'Glass':.06,'Finish':.53,'Roof':.92}.get(role,.84)
        if role=='Graphics':
            t=n.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(sheet.resolve()),check_existing=True)
            l.new(t.outputs['Color'],p.inputs['Base Color']);l.new(t.outputs['Alpha'],p.inputs['Alpha'])
            m.surface_render_method='DITHERED';m['tiling_vertex_tint']=False
        else:
            v=n.new('ShaderNodeVertexColor');v.layer_name='Tint';l.new(v.outputs['Color'],p.inputs['Base Color']);m['tiling_vertex_tint']=True
        if role=='Glass':p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.5
        mats.append(m)
    return mats


class Batch:
    def __init__(self,name,parent,materials,xf=None):
        self.name=name;self.parent=parent;self.materials=materials;self.xf=xf or (lambda v:Vector(v))
        self.v=[];self.f=[];self.c=[];self.m=[];self.uv=[]
    def geom(self,vs,fs,role='Finish',color=None,uv=None):
        base=len(self.v);self.v.extend(tuple(self.xf(v)) for v in vs)
        self.f.extend(tuple(base+i for i in face) for face in fs)
        self.c.extend([(*(color or COLORS[role]),1)]*len(vs));self.m.extend([ROLES.index(role)]*len(fs))
        self.uv.extend([uv for f in fs])
    def box(self,p,s,role='Finish',color=None,r=0):
        if min(s)<1e-6:return
        x,y,z=p;a,b,c=(v/2 for v in s)
        vs=[(x+i*a,y+j*b,z+k*c) for i,j,k in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))]
        self.geom(vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],role,color)
    def prism(self,poly,delta,role='Finish',color=None):
        poly=list(poly)
        changed=True
        while changed and len(poly)>2:
            changed=False
            for i in range(len(poly)):
                a,b,c=map(Vector,(poly[i-1],poly[i],poly[(i+1)%len(poly)]))
                if (b-a).length<1e-8 or (b-a).cross(c-b).length<1e-10:
                    poly.pop(i);changed=True;break
        if len(poly)<3:return
        n=len(poly);vs=list(poly)+[tuple(Vector(v)+Vector(delta)) for v in poly]
        self.geom(vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],role,color)
    def beam(self,a,b,w,d=None,role='Finish',color=None):
        a,b=Vector(a),Vector(b);t=b-a;q=t.to_track_quat('Z','Y').to_matrix()
        half=(w/2,(d or w)/2,t.length/2)
        vs=[(a+b)/2+q@Vector((i*half[0],j*half[1],k*half[2])) for i,j,k in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))]
        self.geom(vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],role,color)
    def tube(self,pts,r,role='Finish',color=None,n=8):
        vs=[]
        for i,pt in enumerate(pts):
            t=Vector(pts[min(i+1,len(pts)-1)])-Vector(pts[max(0,i-1)]);t.normalize()
            u=t.cross(Vector((0,0,1)) if abs(t.z)<.95 else Vector((1,0,0))).normalized();v=t.cross(u)
            vs += [Vector(pt)+r*(u*math.cos(k*math.tau/n)+v*math.sin(k*math.tau/n)) for k in range(n)]
        fs=[(j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k) for j in range(len(pts)-1) for k in range(n)]
        fs += [tuple(reversed(range(n))),tuple(range(len(vs)-n,len(vs)))]
        self.geom(vs,fs,role,color)
    def quad(self,vs,rect,role='Graphics',color=None):
        a,b,c,d=rect;self.geom(vs,[(0,1,2,3)],role,color,[(a,b),(c,b),(c,d),(a,d)])
    def finish(self):
        if not self.v:return None
        me=bpy.data.meshes.new(self.name);me.from_pydata(self.v,[],self.f);me.update()
        for m in self.materials:me.materials.append(m)
        ob=bpy.data.objects.new(self.name,me);bpy.context.collection.objects.link(ob);ob.parent=self.parent
        for p,i in zip(me.polygons,self.m):p.material_index=i
        attr=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT');attr.data.foreach_set('color',[v for c in self.c for v in c]);me.color_attributes.active_color=attr
        uv=me.uv_layers.new(name='UVMap')
        for p,coords in zip(me.polygons,self.uv):
            axes=sorted(range(3),key=lambda k:abs(p.normal[k]))[:2]
            for j,li in enumerate(p.loop_indices):
                v=me.vertices[me.loops[li].vertex_index].co
                uv.data[li].uv=coords[j] if coords else (v[axes[0]],v[axes[1]])
        bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='FIXED',ngon_method='EAR_CLIP');bm.to_mesh(me);bm.free()
        ob['asset_set']='Downtown';ob['construction_component']=self.name
        return ob


def frame(a,b):
    a,b=Vector(a),Vector(b);u=(b-a).normalized();v=Vector((-u.y,u.x,0))
    return lambda p:a+u*p[0]+v*p[1]+Vector((0,0,p[2]))


def pivot(name,p,parent=None,**props):
    o=G.pivot(name,p);o.parent=parent
    for k,v in props.items():o[k]=v
    return o


def wall(mesh,length,height,openings,thick,color):
    """Closed wall strips; openings have x0,x1,z0,z1 and optional arch rise.

    No wall exists behind the glazing. Each arch is a real curved intrados.
    """
    cuts=sorted({0,length,*[v for o in openings for v in (o['x0'],o['x1'])]})
    for x0,x1 in zip(cuts,cuts[1:]):
        mid=(x0+x1)/2;holes=sorted([o for o in openings if o['x0']-1e-6<mid<o['x1']+1e-6],key=lambda o:o['z0'])
        low=0
        for o in holes+[dict(z0=height,z1=height)]:
            if o['z0']>low:mesh.box((mid,thick/2,(low+o['z0'])/2),(x1-x0,thick,o['z0']-low),'Masonry',color)
            low=o['z1']+o.get('rise',0)
        for o in holes:
            rise=o.get('rise',0)
            if rise:
                for j in range(12):
                    aa=j/12;bb=(j+1)/12
                    xa=o['x0']+(o['x1']-o['x0'])*aa;xb=o['x0']+(o['x1']-o['x0'])*bb
                    za=o['z1']+rise*4*aa*(1-aa);zb=o['z1']+rise*4*bb*(1-bb)
                    mesh.prism([(xa,0,za),(xb,0,zb),(xb,0,o['z1']+rise),(xa,0,o['z1']+rise)],(0,thick,0),'Masonry',color)
