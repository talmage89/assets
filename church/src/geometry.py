"""Batched construction solids, authored UVs, pivots and reusable modules."""
import math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector,Matrix

ROOT=Path(__file__).resolve().parents[2]
MATS={}
STYLE='gothic'
PLAN={}


def root(name,point=(0,0,0),parent=None,**props):
    ob=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(ob)
    ob.location=point;ob.parent=parent
    for k,v in props.items():ob[k]=v
    return ob


def clone(source,name,point=(0,0,0),yaw=0,parent=None):
    mapping={}
    for old in [source,*source.children_recursive]:
        ob=old.copy();bpy.context.collection.objects.link(ob);mapping[old]=ob
        ob.name=name if old==source else name+'__'+old.name
    for old,ob in mapping.items():ob.parent=mapping.get(old.parent,parent)
    ob=mapping[source];ob.location=point;ob.rotation_euler=(0,0,math.radians(yaw));return ob


class Mesh:
    def __init__(self,name,parent=None,**props):
        self.name=name;self.parent=parent;self.props=props
        self.v=[];self.f=[];self.role=[];self.colors=[];self.uv=[];self.smooth=[]
    def geom(self,vs,fs,role='iron',color=(1,1,1),uv=None,smooth=False):
        if role=='brick' and STYLE=='chapel':role='siding'
        off=len(self.v);self.v.extend(tuple(v) for v in vs)
        for i,f in enumerate(fs):
            self.f.append(tuple(off+k for k in f));self.role.append(role)
            self.colors.append(color);self.uv.append(uv[i] if uv else None);self.smooth.append(smooth)
    def box(self,p,s,role='iron',color=(1,1,1)):
        x,y,z=p;a,b,c=[q/2 for q in s]
        self.geom([(x+i*a,y+j*b,z+k*c) for i,j,k in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))],
                  [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],role,color)
    def prism(self,poly,depth,role='stone',color=(1,1,1)):
        poly=[Vector(p) for p in poly]
        changed=True
        while changed and len(poly)>=3:
            changed=False
            for i,p in enumerate(poly):
                a=poly[i-1];b=poly[(i+1)%len(poly)]
                if (p-a).length<1e-7 or (b-p).length<1e-7 or (p-a).cross(b-p).length<1e-10:
                    poly.pop(i);changed=True;break
        if len(poly)<3:return
        if (poly[1]-poly[0]).cross(poly[2]-poly[0]).dot(Vector(depth))<0:poly.reverse()
        n=len(poly);self.geom([*poly,*[Vector(p)+Vector(depth) for p in poly]],
            [tuple(reversed(range(n))),tuple(range(n,2*n)),*[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]],role,color)
    def loft(self,rings,role='iron',caps=True,smooth=False,color=(1,1,1)):
        n=len(rings[0]);vs=[p for ring in rings for p in ring]
        fs=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(rings)-1) for i in range(n)]
        self.geom(vs,fs,role,color,smooth=smooth)
        if caps:self.geom(vs,[tuple(reversed(range(n))),tuple(range(len(vs)-n,len(vs)))],role,color)
    def tube(self,pts,r,role='iron',sides=8,color=(1,1,1)):
        pts=list(map(Vector,pts));rings=[]
        for i,p in enumerate(pts):
            t=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized()
            u=t.cross(Vector((0,0,1)) if abs(t.z)<.95 else Vector((1,0,0))).normalized();v=t.cross(u)
            rings.append([p+r*(u*math.cos(k*math.tau/sides)+v*math.sin(k*math.tau/sides)) for k in range(sides)])
        self.loft(rings,role,smooth=True,color=color)
    def beam(self,a,b,w,d=None,role='timber',color=(1,1,1)):
        a,b=Vector(a),Vector(b);delta=b-a;q=delta.to_track_quat('Z','Y').to_matrix();p=(a+b)/2
        temp=Mesh('beam');temp.box((0,0,0),(w,d or w,delta.length),role,color)
        self.geom([p+q@Vector(v) for v in temp.v],temp.f,role,color)
    def lathe(self,profile,role='bronze',n=32):
        self.loft([[(r*math.cos(k*math.tau/n),r*math.sin(k*math.tau/n),z) for k in range(n)] for z,r in profile],role,caps=False,smooth=True)
    def panel(self,x,y,z,w,h,role,rect=None):
        coords=None if rect is None else [[(rect[0],rect[1]),(rect[2],rect[1]),(rect[2],rect[3]),(rect[0],rect[3])]]
        self.geom([(x-w/2,y,z-h/2),(x+w/2,y,z-h/2),(x+w/2,y,z+h/2),(x-w/2,y,z+h/2)],[(0,1,2,3)],role,uv=coords)
    def finish(self):
        from surfaces import charts,tint
        from weather import color as age
        matrix=Matrix.Identity(4);ancestor=self.parent
        while ancestor:
            matrix=ancestor.matrix_basis@matrix;ancestor=ancestor.parent
        # Preserve authored outward winding. Recalculating normals after UV
        # splitting treats every face as an isolated island and flips some.
        rounded={}
        def key(p):return tuple(round(float(v),8) for v in p)
        for f,sm in zip(self.f,self.smooth):
            if not sm:continue
            pts=[Vector(self.v[i]) for i in f];normal=(pts[1]-pts[0]).cross(pts[2]-pts[0])
            for p in pts:rounded[key(p)]=rounded.get(key(p),Vector())+normal
        # Author final triangles first. UVs follow each original face's physical
        # coordinates; source walls contain true apertures rather than decals.
        vs=[];fs=[];uvs=[];cols=[];roles=[];smooth=[]
        for f,role,col,uv,sm in zip(self.f,self.role,self.colors,self.uv,self.smooth):
            points=[self.v[i] for i in f]
            refine=self.name.startswith(('Front rose gable','Pierced tower shaft','Low brick sidewall'))
            for pp,tt in ([(points,uv)] if uv else charts(points,role,weather_grid=refine)):
                n=len(vs);vs.extend(pp);fs.append(tuple(range(n,n+len(pp))));uvs.append(tt)
                normal=(Vector(pp[1])-Vector(pp[0])).cross(Vector(pp[2])-Vector(pp[0])).normalized()
                props=dict(self.props,name=self.name,normal_z=normal.z)
                cols.append([age(tuple(matrix@Vector(p)),role,tint(p,role,col,self.props),props) for p in pp]);roles.append(role);smooth.append(sm)
        me=bpy.data.meshes.new(self.name);me.from_pydata(vs,[],fs);me.update()
        keys=list(dict.fromkeys(roles))
        for r in keys:me.materials.append(MATS[r])
        uv=me.uv_layers.new(name='UVMap');t=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER');me.color_attributes.active_color=t
        for face,tt,cc,r,sm in zip(me.polygons,uvs,cols,roles,smooth):
            face.material_index=keys.index(r);face.use_smooth=sm
            for li,tx,co in zip(face.loop_indices,tt,cc):uv.data[li].uv=tx;t.data[li].color=(*co,1)
        bm=bmesh.new();bm.from_mesh(me);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
        if rounded:
            normals=[None]*len(me.loops)
            for face in me.polygons:
                for li in face.loop_indices:
                    p=me.vertices[me.loops[li].vertex_index].co
                    normals[li]=tuple(rounded.get(key(p),face.normal).normalized() if face.use_smooth else face.normal)
            me.normals_split_custom_set(normals)
        ob=bpy.data.objects.new(self.name,me);bpy.context.collection.objects.link(ob);ob.parent=self.parent
        ob['asset_set']='Church'
        if self.props.get('sheet'):ob['allow_boundary']=True
        for k,v in self.props.items():ob[k]=v
        return ob


def transform(m,point=(0,0,0),yaw=0):
    c,s=math.cos(math.radians(yaw)),math.sin(math.radians(yaw));x0,y0,z0=point
    m.v=[(x0+c*x-s*y,y0+s*x+c*y,z0+z) for x,y,z in m.v];return m
