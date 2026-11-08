"""Batched construction primitives; one fixed mesh per placed module.

Kit materials/UV/export are retained; large earthwork avoids thousands of
operator calls. No external geometry or image tracing enters these functions.
"""
import math
import bpy
from mathutils import Vector

M={}

def root(name,location=(0,0,0),parent=None,**props):
    ob=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(ob)
    ob.parent=parent;ob.location=location
    for key,value in props.items():ob[key]=value
    return ob

def socket(rt,name,p,kind='module_end',**props):
    return root(rt.name+'__'+name,p,rt,socket_kind=kind,**props)

def constant(name,color,rough=.85,metal=0):
    ma=bpy.data.materials.new(name);ma.use_nodes=True
    bs=ma.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal
    return ma

class Batch:
    def __init__(self,name,rt=None):
        self.name=name;self.rt=rt;self.v=[];self.f=[];self.roles=[];self.uv=[];self.colors=[];self.normals=[]

    def face(self,points,role='Concrete',uv=None,tint=(1,1,1,1),normals=None):
        k=len(self.v);self.v.extend(points);self.f.append(tuple(range(k,k+len(points))));self.roles.append(role)
        a,b,c=map(Vector,points[:3]);n=(b-a).cross(c-a).normalized()
        self.normals.extend(normals or [n]*len(points))
        if uv is None:
            a,b,c=map(Vector,points[:3]);normal=(b-a).cross(c-a);axes=(0,1)
            if abs(normal.z)<max(abs(normal.x),abs(normal.y)):
                axes=(1,2) if abs(normal.x)>abs(normal.y) else (0,2)
            tile={'Asphalt':6.096,'AsphaltPolish':6.096,'Concrete':3.048,'Lawn':3.048}.get(role,3.048)
            uv=[(p[axes[0]]/tile,p[axes[1]]/tile) for p in points]
        self.uv.append(uv);self.colors.extend([tint]*len(points))

    def quad(self,points,role='Concrete',**kw):self.face(points,role,**kw)

    def surface(self,points,role='Concrete',**kw):
        """An exposed paving/terrain top; mirrored sections retain +Z winding."""
        points=list(points);a,b,c=map(Vector,points[:3])
        if (b-a).cross(c-a).z<0:
            points.reverse()
            if kw.get('uv') is not None:kw['uv']=list(reversed(kw['uv']))
            if kw.get('normals') is not None:kw['normals']=list(reversed(kw['normals']))
        self.face(points,role,**kw)

    def box(self,center,size,role='Concrete'):
        x,y,z=center;a,b,c=[v/2 for v in size]
        vs=[(x+sx*a,y+sy*b,z+sz*c) for sx,sy,sz in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
        for face in [(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)]:self.face([vs[i] for i in reversed(face)],role)

    def tube(self,points,radius,role='Steel',sides=8,caps=True):
        pts=list(map(Vector,points));rings=[]
        for i,p in enumerate(pts):
            d=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized()
            ref=Vector((0,0,1)) if abs(d.z)<.9 else Vector((0,1,0))
            a=d.cross(ref).normalized();b=d.cross(a).normalized()
            rings.append([p+radius*(a*math.cos(j*math.tau/sides)+b*math.sin(j*math.tau/sides)) for j in range(sides)])
        for index,(a,b) in enumerate(zip(rings,rings[1:])):
            for j in range(sides):
                points=[a[j],a[(j+1)%sides],b[(j+1)%sides],b[j]]
                normals=[(v-pts[index if k<2 else index+1]).normalized() for k,v in enumerate(points)]
                self.face(points,role,normals=normals)
        if caps:
            self.face(list(reversed(rings[0])),role);self.face(rings[-1],role)

    def beam(self,a,b,width,role='Steel',depth=None):
        a,b=Vector(a),Vector(b);d=(b-a).normalized()
        ref=Vector((0,0,1)) if abs(d.z)<.95 else Vector((0,1,0))
        u=d.cross(ref).normalized()*width/2;v=d.cross(u).normalized()*(depth or width)/2
        rings=[[p-u-v,p+u-v,p+u+v,p-u+v] for p in (a,b)]
        self.face(list(reversed(rings[0])),role);self.face(rings[-1],role)
        for j in range(4):self.face([rings[0][j],rings[0][(j+1)%4],rings[1][(j+1)%4],rings[1][j]],role)

    def extrude(self,section,stations,role='Bridge',axis='Y',caps=True):
        """Closed manufactured section. Stations may carry cross-section camber."""
        rings=[]
        area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(section,section[1:]+section[:1]))
        reverse=(area>0) if axis=='Y' else (area<0)
        def add(points):self.face(list(reversed(points)) if reverse else points,role)
        for sta in stations:
            s,h=sta if isinstance(sta,tuple) else (sta,0)
            rings.append([(s,u,v+h) if axis=='X' else (u,s,v+h) for u,v in section])
        for a,b in zip(rings,rings[1:]):
            for j in range(len(section)):add([a[j],a[(j+1)%len(a)],b[(j+1)%len(b)],b[j]])
        if caps:
            add(list(reversed(rings[0])));add(rings[-1])

    def finish(self):
        me=bpy.data.meshes.new(self.name);me.from_pydata(self.v,[],self.f);me.update()
        ob=bpy.data.objects.new(self.name,me);bpy.context.collection.objects.link(ob);ob.parent=self.rt
        keys=list(dict.fromkeys(self.roles))
        for role in keys:me.materials.append(M[role])
        uv=me.uv_layers.new(name='UVMap');ca=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
        for i,c in enumerate(self.colors):ca.data[i].color=c
        for p,role,coords in zip(me.polygons,self.roles,self.uv):
            p.material_index=keys.index(role)
            p.use_smooth=True
            for li,co in zip(p.loop_indices,coords):uv.data[li].uv=co
        me.normals_split_custom_set_from_vertices(self.normals)
        # Triangulate once using Blender's ngon tessellation; geometry stays
        # in meters with identity scale. Open skins have authored outward winding.
        from kit.model import apply
        mod=ob.modifiers.new('Export triangles','TRIANGULATE');apply(ob);ob.data.calc_loop_triangles()
        return ob

def curve(rt,name,points):
    """Curves are authored paths; glTF gets empties + sampled coordinates extras.

    glTF has no native path-curve primitive. JSON uses Blender coordinates and
    the socket extras explicitly supply glTF samples too.
    """
    import json
    points=[list(map(float,p)) for p in points]
    cv=bpy.data.curves.new(name,'CURVE');cv.dimensions='3D';sp=cv.splines.new('POLY');sp.points.add(len(points)-1)
    for v,p in zip(sp.points,points):v.co=(*p,1)
    ob=bpy.data.objects.new(name,cv);bpy.context.collection.objects.link(ob);ob.parent=rt
    ob.hide_render=True;ob['drive_path']=True
    sock=socket(rt,name+'_Path',points[0],kind='drive_path',points_blender_json=json.dumps(points),points_gltf_json=json.dumps([[x,z,-y] for x,y,z in points]))
    return sock

def count(rt):
    # Count each actual shared mesh once per call, then expand its instances.
    # Rewalking millions of identical foliage polygons made reporting slower
    # than building. A local cache cannot survive a later topology change.
    totals={};count=0
    for ob in [rt,*rt.children_recursive]:
        if ob.type!='MESH':continue
        key=ob.data.as_pointer()
        if key not in totals:totals[key]=sum(len(p.vertices)-2 for p in ob.data.polygons)
        count+=totals[key]
    return count
