"""Original construction checkpoint. No material images, no asset imports.

Fast, indexed primitive assembly keeps vertex tint and part identities. Fine
manufactured grooves are deliberately reserved for the shared family maps.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
import bmesh
from mathutils import Matrix, Vector

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path[:0]=[str(ROOT),str(HERE)]
from kit import model as G
from kit import tiling
from kit.fonts import find_font
from plan import clip,subtract,roof_faces,roof_junctions,roof_blocks,wall_frame,openings,load,serialize

ROLES=('Siding','Shingles','Veneer','Concrete','Trim','Glass')


def materials():
    out=[]
    for name in ROLES:
        m=bpy.data.materials.new('House_'+name);m.use_nodes=True
        m['checkpoint_placeholder']=True;m['tiling_vertex_tint']=True
        ns,ls=m.node_tree.nodes,m.node_tree.links
        p=ns.get('Principled BSDF');p.inputs['Roughness'].default_value=.65
        v=ns.new('ShaderNodeVertexColor');v.layer_name='Tint';ls.new(v.outputs['Color'],p.inputs['Base Color'])
        if name=='Shingles':p.inputs['Roughness'].default_value=.9
        if name=='Concrete':p.inputs['Roughness'].default_value=.91
        if name=='Glass':
            p.inputs['Roughness'].default_value=.22
            p.inputs['Transmission Weight'].default_value=1.0
            p.inputs['IOR'].default_value=1.5
        out.append(m)
    return out


class Mesh:
    def __init__(self,builder,name,part='Static',**properties):
        self.builder=builder;self.name=name;self.part=part;self.props=properties
        self.v=[];self.f=[];self.mat=[];self.col=[]

    def geom(self,vs,fs,role='Trim',color=None):
        off=len(self.v);self.v.extend(tuple(v) for v in vs)
        self.f.extend(tuple(i+off for i in f) for f in fs)
        self.mat.extend([ROLES.index(role)]*len(fs))
        c=color or self.builder.colors.get(role,(.4,.4,.4))
        self.col.extend([(*c,1)]*len(vs))

    def box(self,p,s,role='Trim',color=None,r=.0015,xf=None):
        h=[x/2 for x in s]
        if min(h)<=0:return
        r=min(r,min(h)*.45)
        if r:
            vs=[];indices={}
            for x in (-1,1):
                for y in (-1,1):
                    for z in (-1,1):
                        signs=(x,y,z)
                        for axis in range(3):
                            indices[(signs,axis)]=len(vs)
                            vs.append([signs[k]*(h[k] if k==axis else h[k]-r) for k in range(3)])
            fs=[]
            for axis in range(3):
                others=[k for k in range(3) if k!=axis]
                for sign in (-1,1):
                    face=[]
                    for u,v in ((-1,-1),(1,-1),(1,1),(-1,1)):
                        signs=[sign]*3;signs[others[0]]=u;signs[others[1]]=v
                        face.append(indices[(tuple(signs),axis)])
                    fs.append(face)
            for a,b in ((0,1),(0,2),(1,2)):
                c=3-a-b
                for sa in (-1,1):
                    for sb in (-1,1):
                        v=[]
                        for sc,axis in ((-1,a),(1,a),(1,b),(-1,b)):
                            signs=[0]*3;signs[a]=sa;signs[b]=sb;signs[c]=sc
                            v.append(indices[(tuple(signs),axis)])
                        fs.append(v)
            for signs in ((x,y,z) for x in (-1,1) for y in (-1,1) for z in (-1,1)):
                fs.append([indices[(signs,k)] for k in range(3)])
        else:
            vs=[(x*h[0],y*h[1],z*h[2]) for x,y,z in
                [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
            fs=[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)]
        vs=[Vector(p)+Vector(v) for v in vs]
        if xf:vs=[xf(v) for v in vs]
        self.geom(vs,fs,role,color)

    def prism(self,poly,axis,depth,role='Trim',color=None):
        """A closed gauged skin. axis is the inward thickness vector."""
        v=[Vector(p) for p in poly]
        # Analytic clipping can introduce redundant collinear boundary points.
        # Remove those before the solid's side walls are made, not afterwards
        # by deleting arbitrary triangles from an otherwise broken solid.
        changed=True
        while changed and len(v)>=3:
            changed=False
            for i in range(len(v)):
                a,c,d=v[i-1],v[i],v[(i+1)%len(v)]
                if (c-a).length<1e-7 or (d-c).length<1e-7 or (c-a).cross(d-c).length<1e-10:
                    v.pop(i);changed=True;break
        n=len(v)
        if n<3:return
        v += [p+Vector(axis)*depth for p in v]
        fs=[tuple(range(n)),tuple(reversed(range(n,2*n)))]
        fs += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
        self.geom(v,fs,role,color)

    def beam(self,a,b,width,depth=None,role='Trim',color=None,r=.001):
        a,b=Vector(a),Vector(b);delta=b-a
        rot=delta.to_track_quat('Z','Y').to_matrix()
        self.box((0,0,0),(width,depth or width,delta.length),role,color,r,
                 xf=lambda v:(a+b)/2+rot@v)

    def tube(self,points,radius,role='Trim',color=None,sides=12,closed=True):
        pts=list(map(Vector,points));vs=[]
        previous=None
        for i,p in enumerate(pts):
            t=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized()
            u=t.cross(Vector((0,0,1)) if abs(t.z)<.9 else Vector((1,0,0))).normalized() if previous is None else (previous-t*previous.dot(t)).normalized()
            v=t.cross(u);previous=u
            vs += [p+radius*(u*math.cos(k*math.tau/sides)+v*math.sin(k*math.tau/sides)) for k in range(sides)]
        fs=[(j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k)
            for j in range(len(pts)-1) for k in range(sides)]
        if closed:fs += [tuple(reversed(range(sides))),tuple(range(len(vs)-sides,len(vs)))]
        self.geom(vs,fs,role,color)

    def finish(self):
        if not self.v:return None
        me=bpy.data.meshes.new(self.name);me.from_pydata(self.v,[],self.f);me.update()
        bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(me);bm.free()
        ob=bpy.data.objects.new(self.name,me);bpy.context.collection.objects.link(ob)
        for mat in self.builder.materials:me.materials.append(mat)
        for p,i in zip(me.polygons,self.mat):p.material_index=i
        attr=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
        attr.data.foreach_set('color',[c for row in self.col for c in row])
        # Meter UVs are a staging chart, never called a finished trim unwrap.
        uv=me.uv_layers.new(name='UVMap')
        for p in me.polygons:
            axis=max(range(3),key=lambda k:abs(p.normal[k]));axes=[k for k in range(3) if k!=axis]
            for li in p.loop_indices:
                v=me.vertices[me.loops[li].vertex_index].co
                uv.data[li].uv=(v[axes[0]],v[axes[1]])
        me.color_attributes.active_color=attr
        ob['asset_set']='Houses';ob['part']=self.part
        # Curtains, open drain mouths, folded ridge caps and sheet upstands are
        # intentional skins. Do not call them closed-solid topology evidence.
        if self.props.get('component') in ('window','drainage','ridge','valley','flashing','roof_vent','services'):
            ob['allow_boundary']=True
        for k,v in self.props.items():ob[k]=v
        ob.parent=self.builder.moving.get(self.part,self.builder.root)
        if self.part in self.builder.moving:
            bpy.context.view_layer.update();me.transform(ob.parent.matrix_world.inverted())
        self.builder.objects.append(ob)
        return ob


class Builder:
    def __init__(self,plan):
        self.plan=plan;self.objects=[];self.materials=materials();self.openings=openings(plan)
        self.colors=dict(Siding=plan['spec']['colors']['siding'],Shingles=(.048,.050,.047),
                         Veneer=(.255,.115,.065),Concrete=(.29,.28,.25),Trim=plan['spec']['colors']['trim'],Glass=(.83,.86,.83))
        self.root=G.pivot('House',(0,0,0));self.root['static_root']=True
        self.root['seed']=plan['seed'];self.root['checkpoint']='form / placeholder materials'
        main=plan['blocks'][0]
        self.door=G.pivot('FrontDoor',(plan['door_x']-.9144/2+.004,main.y0+.153,.514),'Z',(0,105))
        if plan['spec']['type']=='ranch':
            self.door.location.z=main.floor+.006
        self.door.parent=self.root
        self.moving={'FrontDoor':self.door}
        for name,p in plan['sockets'].items():
            ob=G.pivot('Socket_'+name,p);ob.parent=self.root;ob['socket_kind']=name
        self.drains=[]

    def mesh(self,name,part='Static',**props):return Mesh(self,name,part,**props)

    def frame(self,b,face):
        o,t,n,length=wall_frame(b,face)
        def xf(v):return Vector((o[0]+t[0]*v[0]+n[0]*v[1],o[1]+t[1]*v[0]+n[1]*v[1],v[2]))
        return xf,n,length


def wall_sections(b,block,face):
    """Piecewise-linear wall outline with adjoining block/roof removed."""
    xf,n,length=b.frame(block,face);p0=xf((0,.001,0));p1=xf((length,.001,0));t=(p1-p0)/length
    cuts={0.,length}
    for other in b.plan['blocks']:
        if abs(t.x)>.5:cuts.update([other.x0-p0.x,other.x1-p0.x,other.cx-p0.x])
        else:cuts.update([other.y0-p0.y,other.y1-p0.y,other.cy-p0.y])
        planes=other.planes()
        for i,p in enumerate(planes):
            for q in planes[i+1:]:
                slope=(p[0]-q[0])*t.x+(p[1]-q[1])*t.y
                if abs(slope)>1e-9:
                    cuts.add(-((p[0]-q[0])*p0.x+(p[1]-q[1])*p0.y+p[2]-q[2])/slope)
    cuts=sorted(v for v in cuts if 0<=v<=length)
    result=[]
    for a,c in zip(cuts,cuts[1:]):
        if c-a<1e-5:continue
        mid=xf(((a+c)/2,.002,0))
        neighbor=next((other for other in b.plan['blocks'] if other is not block and other.contains(mid.x,mid.y)),None)
        bottom=[];top=[]
        for u in (a,c):
            p=xf((u,0,0));bottom.append(neighbor.height(p.x,p.y)-.012 if neighbor else max(.02,block.floor-.205))
            top.append(block.height(p.x,p.y)-.140)
        # Top/bottom may cross at the valley. Clip rather than lose a triangle.
        poly=[(a,bottom[0]),(c,bottom[1]),(c,top[1]),(a,top[0])]
        if top[0]<bottom[0] and top[1]<bottom[1]:continue
        if (top[0]-bottom[0])*(top[1]-bottom[1])<0:
            f=(top[0]-bottom[0])/((top[0]-bottom[0])-(top[1]-bottom[1]));u=a+f*(c-a)
            z=top[0]+f*(top[1]-top[0])
            poly=[(a,bottom[0]),(u,z),(a,top[0])] if top[0]>bottom[0] else [(u,z),(c,bottom[1]),(c,top[1])]
        result.append((poly,neighbor is not None))
    return result


def shell(b):
    for block in b.plan['blocks']:
        for face in ('front','back','left','right'):
            xf,n,length=b.frame(block,face)
            wall=b.mesh(block.name+'_'+face+'_Wall',component='wall',block=block.name,face=face)
            foundation=b.mesh(block.name+'_'+face+'_Foundation',component='foundation',block=block.name,face=face)
            caps=b.mesh(block.name+'_'+face+'_VeneerCap',component='veneer_cap')
            for poly,adjoining in wall_sections(b,block,face):
                parts=[poly]
                holes=[o for o in b.openings if o['block']==block.name and o['face']==face]
                for o in holes:
                    cuts=[(1,0,-o['u']+o['w']/2),(-1,0,o['u']+o['w']/2),(0,1,-o['z']),(0,-1,o['z']+o['h'])]
                    parts=[p for v in parts for p in subtract(v,cuts)]
                for p in parts:
                    veneer=b.plan['spec']['cladding'][block.name][face]=='veneer'
                    for role,part in ([('Veneer',clip(p,0,-1,.99)),('Siding',clip(p,0,1,-.99))] if veneer else [('Siding',p)]):
                        if part:
                            wall.prism([xf((u,.012 if role=='Siding' else .072,z)) for u,z in part],(-n[0],-n[1],0),.165,role)
                            if role=='Veneer':
                                for a,c in zip(part,part[1:]+part[:1]):
                                    if abs(a[1]-.99)<1e-7 and abs(c[1]-.99)<1e-7:
                                        lo,hi=sorted((a[0],c[0]))
                                        caps.prism([xf((lo,.025,1.034)),xf((hi,.025,1.034)),xf((hi,.13,1.019)),xf((lo,.13,1.019))],(0,0,-1),.040,'Veneer',(.255,.14,.085))
                if not adjoining:
                    lo=min(v[0] for v in poly);hi=max(v[0] for v in poly)
                    ztop=block.floor-.205
                    if ztop>0:
                        foundation.prism([xf((lo,-.024,0)),xf((hi,-.024,0)),xf((hi,-.024,ztop)),xf((lo,-.024,ztop))],(-n[0],-n[1],0),.18,'Concrete')
                        foundation.box(((lo+hi)/2,-.016,ztop-.022),(hi-lo,.024,.044),'Trim',(.35,.34,.31),r=.001,xf=xf)
            wall.finish();foundation.finish();caps.finish()
        trims=b.mesh(block.name+'_CornerPosts',component='corner_posts')
        for x in (block.x0,block.x1):
            for y in (block.y0,block.y1):
                if any(other is not block and other.contains(x,y, .0001) for other in b.plan['blocks']):continue
                z0=max(.02,block.floor-.2);z1=block.eave-.15
                sx=-1 if x==block.x0 else 1;sy=-1 if y==block.y0 else 1
                trims.box((x+sx*.022,y-sy*.035,(z0+z1)/2),(.035,.105,z1-z0),r=.002)
                trims.box((x-sx*.035,y+sy*.022,(z0+z1)/2),(.105,.035,z1-z0),r=.002)
        trims.finish()


def window(b,o):
    if b.plan['spec']['type']=='ranch':
        from ranch_build import window as ranch_window
        return ranch_window(b,o)
    block=next(v for v in b.plan['blocks'] if v.name==o['block']);xf,n,length=b.frame(block,o['face'])
    me=b.mesh(o['id'],component='window',opening=json.dumps(o))
    u,z,w,h=o['u'],o['z'],o['w'],o['h']
    def box(uu,v,zz,ww,dd,hh,color=None,r=.0015,role='Trim'):
        me.box((uu,v,zz),(ww,dd,hh),role,color,r,xf)
    # True reveal, interior cheek lining, a 290 mm deep room beyond glazing.
    for s in (-1,1):box(u+s*(w/2-.018),-.10,z+h/2,.036,.20,h,(.48,.46,.40))
    box(u,-.10,z+h-.019,w-.072,.20,.038,(.48,.46,.40),0)
    box(u,-.28,z+h/2,w-.04,.015,h-.04,(.045,.043,.034),0)
    # Side/top casing + receiving J-channel outside the structural opening.
    for s in (-1,1):
        box(u+s*(w/2+.04445),.052,z+h/2,.0889,.058,h+.11)
        box(u+s*(w/2+.097),.023,z+h/2,.019,.025,h+.145,r=.0008)
    box(u,.055,z+h+.04445,w+.1778,.063,.0889)
    box(u,.024,z+h+.103,w+.214,.024,.022,r=.0006)
    box(u,.091,z-.020,w+.23,.19,.041)
    box(u,.052,z-.068,w+.13,.045,.058)
    # Flashed head with bent drip lip, sill has a real outward fall.
    sill=me
    sill.prism([xf((u-w/2-.115,.013,z+.004)),xf((u+w/2+.115,.013,z+.004)),
                xf((u+w/2+.115,.174,z-.012)),xf((u-w/2-.115,.174,z-.012))],(0,0,-1),.012)
    box(u,.095,z+h+.097,w+.22,.12,.009,(.48,.48,.45),0)
    # Double-hung tracks, physically offset upper/lower sash and meeting rails.
    inner=w-.072;sh=(h-.082)/2
    for row in (0,1):
        zz=z+.036+row*(h-.072)/2;v=.018-row*.026
        for s in (-1,1):box(u+s*(inner/2-.025),v,zz+sh/2,.050,.033,sh)
        for zh in (zz+.025,zz+sh-.025):box(u,v,zh,inner-.10,.036,.050)
        box(u,v-.019,zz+sh/2,inner-.10,.004,sh-.10,b.colors['Glass'],0,'Glass')
        # Grilles are between the glass, rather than heavy exterior jail bars.
        for q in (-1,1):box(u+q*(inner-.1)/6,v-.022,zz+sh/2,.012,.010,sh-.1,r=0)
        box(u,v-.022,zz+sh/2,inner-.1,.010,.012,r=0)
    box(u,.032,z+h/2,w-.07,.042,.027)
    # Curtains are shallow softly pleated surfaces, not rigid opaque panels.
    mode=int(o['id'].split('_')[-1])%4
    if mode in (0,2):
        curtain=(.34,.31,.24) if mode==0 else (.47,.46,.40)
        for sign in (-1,1):
            vs=[];rows=3;cols=10
            for j in range(rows+1):
                zz=z+.04+(h-.08)*j/rows
                for k in range(cols+1):
                    xx=u+sign*(.19*w+(.29*w)*k/cols)
                    depth=-.15-.013*math.cos(k*math.pi*1.5)-.008*math.sin(j*.8+k*.3)
                    vs.append(xf((xx,depth,zz-.018*math.sin(k*.7)**2*(1-j/rows))))
            fs=[(j*(cols+1)+k,j*(cols+1)+k+1,(j+1)*(cols+1)+k+1,(j+1)*(cols+1)+k) for j in range(rows) for k in range(cols)]
            me.geom(vs,fs,'Trim',curtain)
    elif mode==1:
        # A part-lowered blind, individual bottom rail, texture slats later.
        lowered=.25+((b.plan['seed']*13+int(o['id'].split('_')[-1])*17)%47)/100
        box(u,-.13,z+h*(1-lowered/2),w-.13,.012,h*lowered,(.39,.38,.33),0)
        box(u,-.115,z+h*(1-lowered),w-.12,.018,.018,(.42,.41,.35),0)
    if o['shutters']:
        c=b.plan['spec']['colors']['shutter'];sw=w/2
        for side in (-1,1):
            xx=u+side*(w/2+.11+sw/2)
            box(xx,.020,z+h/2,sw,.016,h,c,r=.002)
            for s in (-1,1):box(xx+s*(sw/2-.026),.035,z+h/2,.052,.016,h,c)
            for zh in (z+.033,z+h*.5,z+h-.033):box(xx,.035,zh,sw-.104,.016,.057,c)
            # Only the deep breaks survive as geometry; fine louvers use maps.
            for zh in (z+h*.25,z+h*.75):box(xx,.0305,zh,sw-.112,.006,h*.40,tuple(v*.78 for v in c),r=0)
            for zh in (z+.16,z+h-.16):
                box(xx-side*.11,.046,zh,.015,.006,.015,tuple(v*.60 for v in c),r=0)
    me.finish()


def panel(me,xf,u,v,z,w,h,color):
    # Low-cost stamped raised island with a genuine sloping shoulder.
    vs=[]
    for inset,dep in ((0,v),(.018,v+.009),(.037,v+.012)):
        vs += [xf((u+sx*(w/2-inset),dep,z+sz*(h/2-inset))) for sx,sz in ((-1,-1),(1,-1),(1,1),(-1,1))]
    fs=[(j*4+k,j*4+(k+1)%4,(j+1)*4+(k+1)%4,(j+1)*4+k) for j in (0,1) for k in range(4)]+[(8,9,10,11)]
    me.geom(vs,fs,'Trim',color)


def doors(b):
    main,garage=b.plan['blocks']
    for o in b.openings:
        if o['kind']=='window':window(b,o);continue
        if o['kind'] in ('patio','service'):continue
        block=main if o['block']=='Main' else garage
        xf,n,length=b.frame(block,o['face']);u,z,w,h=o['u'],o['z'],o['w'],o['h']
        static=b.mesh(o['id']+'_Jamb',component='door_frame')
        masonry=b.plan['spec']['type']=='ranch' and b.plan['spec']['cladding'][block.name][o['face']]=='veneer'
        for sign in (-1,1):
            static.box((u+sign*(w/2+(.031 if masonry else .06)),-.052 if masonry else .068,z+h/2),(.055 if masonry else .12,.05 if masonry else .11,h+.04 if masonry else h+.12),r=.002,xf=xf)
            static.box((u+sign*(w/2+.012),-.012 if masonry else -.052,z+h/2),(.024,.080 if masonry else .17,h),r=.001,xf=xf)
        static.box((u,-.052 if masonry else .069,z+h+.025 if masonry else z+h+.065),(w+.055 if masonry else w+.24,.05 if masonry else .11,.05 if masonry else .13),r=.002,xf=xf)
        static.box((u,-.02,z-.005),(w,.30 if o['kind']=='garage' else .24,.01),'Trim',(.40,.41,.38),r=.001,xf=xf)
        if o['kind']=='door':
            me=b.mesh('FrontDoor_Leaf','FrontDoor',component='front_door')
            c=b.plan['spec']['colors']['door']
            door_xf=lambda v:xf((v[0],v[1]-.122,v[2]))
            me.box((u,-.006,z+h/2),(w-.008,.044,h-.012),'Trim',c,.002,door_xf)
            for row,hh in ((.22,.60),(.62,.64),(.88,.24)):
                for side in (-1,1):panel(me,door_xf,u+side*w*.225,.017,z+row*h,w*.36,hh,c)
            # Three hinge knuckles lie on the documented physical pivot axis.
            for zh in (.23,1.02,1.80):
                p=door_xf((u-w/2+.004,-.031,z+zh))
                me.tube([p-Vector((0,0,.04)),p+Vector((0,0,.04))],.0035,color=(.18,.17,.13),sides=10)
            xx=u+w*.35
            for zz,rr in ((z+1.01,.025),(z+1.18,.020)):
                me.tube([door_xf((xx,.017,zz)),door_xf((xx,.043,zz))],rr,color=(.29,.25,.16),sides=12)
            me.tube([door_xf((xx,.041,z+1.01)),door_xf((xx-.075,.041,z+1.01))],.009,color=(.29,.25,.16))
            me.finish()
            # Structural opening remains clear when the leaf swings inward.
            if not masonry:static.box((u,.032,z+h+.15),(w+.34,.09,.055),r=.002,xf=xf)
        else:
            me=b.mesh('GarageDoor_Closed',component='garage_door',width_m=w,height_m=h)
            c=tuple(v*.94 for v in b.colors['Trim'])
            for row in range(4):
                zz=z+(row+.5)*h/4
                me.box((u,-.021,zz),(w-.016,.042,h/4-.007),'Trim',c,.001,xf)
                for col in range(8):panel(me,xf,u-w/2+(col+.5)*w/8,.002,zz,w/8-.095,h/4-.13,c)
            me.box((u,.004,z+.018),(w,.024,.03),'Trim',(.025,.026,.023),0,xf)
            for side in (-1,1):me.box((u+side*.24,.027,z+.72),(.11,.015,.021),'Trim',(.11,.12,.115),.002,xf)
            me.finish()
        static.finish()


def exterior_edges(block,faces):
    """Merge fragmented perimeter intervals so roof clipping cannot double trim."""
    o=block.overhang;result=[]
    for axis,value,n in ((0,block.x0-o,(-1,0)),(0,block.x1+o,(1,0)),(1,block.y0-o,(0,-1)),(1,block.y1+o,(0,1))):
        ranges=[]
        for row in faces:
            if row['block']!=block.name:continue
            poly=row['polygon']
            for p,q in zip(poly,poly[1:]+poly[:1]):
                if abs(p[axis]-value)<1e-6 and abs(q[axis]-value)<1e-6:
                    ranges.append(sorted((p[1-axis],q[1-axis])))
        merged=[]
        for lo,hi in sorted(ranges):
            if merged and lo<=merged[-1][1]+1e-6:merged[-1][1]=max(hi,merged[-1][1])
            else:merged.append([lo,hi])
        for lo,hi in merged:
            if hi-lo<.01:continue
            # Gable rake breaks at its ridge: no fascia cutting through the attic.
            middle=block.cy if axis==0 else block.cx
            # A horizontal hip eave is one run, with no spurious center outlet.
            def at(t):return block.height(value,t) if axis==0 else block.height(t,value)
            bent=abs(at((lo+hi)/2)-(at(lo)+at(hi))/2)>.001
            stops=[lo]+([middle] if bent and lo+1e-6<middle<hi-1e-6 else [])+[hi]
            for a,c in zip(stops,stops[1:]):
                pts=[]
                for t in (a,c):
                    x,y=(value,t) if axis==0 else (t,value)
                    pts.append((x,y,block.height(x,y)))
                result.append((pts,n))
    return result


def drain(b,me,a,c,n,block,index):
    """Open gauged K gutter with fall, outlet, two elbows, straps, splash block."""
    if b.plan['spec']['type']=='ranch':
        from ranch_drain import drain as ranch_drain
        return ranch_drain(b,me,a,c,n,block,index)
    a,c=Vector(a),Vector(c);normal=Vector((*n,0));direction=(c-a).normalized()
    # Choose an end whose wall-side pipe is outside every neighboring footprint.
    choices=[]
    for p in (a,c):
        pipe=p-normal*(block.overhang-(.125 if b.plan['spec']['type']=='ranch' else .066))
        if abs(n[0])>.5:pipe.y=max(block.y0+.09,min(block.y1-.09,pipe.y))
        else:pipe.x=max(block.x0+.09,min(block.x1-.09,pipe.x))
        if block.name=='Porch':
            # The pipe is strapped to a structural column, not empty space.
            x=block.x0+.21 if p.x<block.cx else block.x1-.21
            pipe=Vector((x,block.y0+.20,p.z))+normal*.105
        valid=not any(other is not block and other.contains(pipe.x,pipe.y,.012) for other in b.plan['blocks'])
        choices.append((valid,p,pipe))
    valid,end,pipe=max(choices,key=lambda v:(v[0],-v[1].y if block.name=='Porch' else abs(v[1].x)))
    if not valid:raise ValueError('No unblocked downspout on '+block.name)
    # Both end elevations are computed from their distance to the drain.
    ends=[p+Vector((0,0,-.055+.0025*(p-end).length)) for p in (a,c)]
    # K silhouette: vertical rear, sloped toe, ogee front and folded bead.
    profile=[(.006,0),(.006,-.126),(.081,-.126),(.121,-.077),(.137,-.047),(.137,.0),
             (.127,.0),(.127,-.044),(.112,-.075),(.077,-.125),(.007,-.125),(.007,0)]
    vs=[p+normal*u+Vector((0,0,z)) for p in ends for u,z in profile];nn=len(profile)
    fs=[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn)]+[tuple(reversed(range(nn))),tuple(range(nn,nn*2))]
    me.geom(vs,fs)
    reuse=next((row for row in b.drains if row['block']==block.name and math.dist(row['centerline'][3][:2],pipe[:2])<(.40 if b.plan['spec']['type']=='ranch' else .16)),None)
    if reuse:
        b.drains.append({**reuse,'gutter':[list(a),list(c)],'normal':n,'shared_column_outlet':True})
        return
    start=end+normal*.059+Vector((0,0,-.17))
    walltop=Vector((pipe.x,pipe.y,start.z-.40))
    finish=Vector((pipe.x,pipe.y,.22));outlet=finish+normal*.32+Vector((0,0,-.10))
    path=[start,start+Vector((0,0,-.07)),walltop+Vector((0,0,.08)),walltop,finish,finish+normal*.12+Vector((0,0,-.09)),outlet]
    # Real rectangular section, with open ends and 1 mm walls at the shoe.
    v=[];wide=direction.normalized()
    for i,p in enumerate(path):
        tangent=(path[min(i+1,len(path)-1)]-path[max(i-1,0)]).normalized()
        section_u=(wide-tangent*wide.dot(tangent)).normalized()
        across=tangent.cross(section_u).normalized()
        for sw,sd in ((-1,-1),(1,-1),(1,1),(-1,1)):
            v.append(p+section_u*sw*.0381+across*sd*.0254)
    fs=[(j*4+i,j*4+(i+1)%4,(j+1)*4+(i+1)%4,(j+1)*4+i) for j in range(len(path)-1) for i in range(4)]
    me.geom(v,fs)
    # Outlet mouth has a dark inset with a metal edge, not a white cap.
    v=[p for p in v[-4:]]
    center=sum(v,Vector())/4
    me.geom([center+(p-center)*.92-(outlet-finish).normalized()*.025 for p in v],[(0,1,2,3)],color=(.028,.029,.026))
    for z in [v for v in (1.,2.8,4.6) if v<walltop.z-.1]:
        pos=Vector((pipe.x,pipe.y,z))
        me.box(pos,(.092 if abs(wide.x)>.5 else .058,.058 if abs(wide.x)>.5 else .092,.025),r=.001)
        me.beam(pos,pos-normal*(.14 if b.plan['spec']['type']=='ranch' else .078),.022,.018,r=.001)
    splash=b.mesh(f'{block.name}_Splash_{index}',component='splash_block')
    mid=outlet+normal*.12;mid.z=.0225
    sx,sy=(.31,.60) if abs(n[1])>.5 else (.60,.31)
    splash.box(mid,(sx,sy,.045),'Concrete',r=.01)
    splash.finish()
    b.drains.append(dict(block=block.name,gutter=[list(a),list(c)],normal=n,
                         fall=.0025,centerline=[list(p) for p in path],outlet=list(outlet)))


def roofs(b):
    structural=[b.plan['roof_envelope']] if b.plan.get('roof_envelope') else roof_blocks(b.plan['blocks'])
    blocks=structural+[b.plan['porch']] if b.plan.get('roof_envelope') else b.plan['blocks']+[b.plan['porch']]
    # Porch is below upper windows, with its rear planes terminated at the wall.
    faces=roof_faces(structural+[b.plan['porch']]) if b.plan['spec']['type']=='ranch' else roof_faces(structural)+roof_faces([b.plan['porch']])
    for row in faces:
        if row['block']=='Porch':row['polygon']=clip(row['polygon'],0,-1,b.plan['blocks'][0].y0-.012)
    faces=[row for row in faces if row['polygon']]
    for row in faces:
        p=row['plane'];poly=row['polygon']
        me=b.mesh(f"{row['block']}_Roof_{row['index']}_{faces.index(row)}",component='roof',block=row['block'])
        me.prism([(x,y,p[0]*x+p[1]*y+p[2]) for x,y in poly],(0,0,-1),.14,
                 'Trim' if row['block']=='Cricket' else 'Shingles',(.16,.17,.16) if row['block']=='Cricket' else None)
        me.finish()
    for block in blocks:
        trim=b.mesh(block.name+'_RoofEdges',component='eave_rake_soffit')
        gutters=b.mesh(block.name+'_Drainage',component='drainage')
        edges=exterior_edges(block,faces)
        for index,(pts,n) in enumerate(edges):
            a,c=map(Vector,pts);normal=Vector((*n,0))
            if block.name=='Porch' and n==(0,1):continue
            # A rake follows its actual two slopes; eave fascia is vertical.
            trim.prism([a+Vector((0,0,-.023)),c+Vector((0,0,-.023)),c+Vector((0,0,-.204)),a+Vector((0,0,-.204))],normal,.021)
            inner=[Vector((max(block.x0,min(block.x1,p.x)),max(block.y0,min(block.y1,p.y)),p.z)) for p in (a,c)]
            soffit=[a+Vector((0,0,-.195)),c+Vector((0,0,-.195)),inner[1]+Vector((0,0,-.195)),inner[0]+Vector((0,0,-.195))]
            trim.prism(soffit,(0,0,-1),.009)
            # Receiving bead and vent strip volume; perforation reserved for map.
            trim.beam(soffit[2],soffit[3],.021,.018,r=.0006)
            vent=[p-normal*.12+Vector((0,0,-.202)) for p in (a,c)]
            trim.beam(*vent,.055,.004,color=(.24,.25,.23),r=0)
            # Two thin shingle edges and a folded drip hem read at street range.
            trim.beam(a+Vector((0,0,.003)),c+Vector((0,0,.003)),.024,.012,'Shingles',r=0)
            trim.beam(a+normal*.015+Vector((0,0,-.021)),c+normal*.015+Vector((0,0,-.021)),.014,.017,color=(.43,.43,.40),r=0)
            if abs(a.z-c.z)<.005:
                drain(b,gutters,a,c,n,block,index)
        trim.finish();gutters.finish()
    junctions=roof_junctions(structural+[b.plan['porch']]) if b.plan['spec']['type']=='ranch' else roof_junctions(structural)+roof_junctions([b.plan['porch']])
    for i,row in enumerate(junctions):
        if row['kind']=='ridge' and row['blocks']==['Cricket','Cricket']:continue
        me=b.mesh('RoofJunction_'+str(i),component=row['kind'])
        a,c=map(Vector,row['points']);delta=c-a;side=delta.cross(Vector((0,0,1))).normalized()
        if row['kind']=='valley':
            # Recessed exposed metal center, roofing is clipped at the same line.
            me.prism([a-side*.08+Vector((0,0,.006)),c-side*.08+Vector((0,0,.006)),c+side*.08+Vector((0,0,.006)),a+side*.08+Vector((0,0,.006))],(0,0,-1),.002,'Trim',(.16,.17,.16))
        else:
            # Folded cap, 280 mm wide. Ridge vent only along horizontal ridge.
            raised=.063 if abs(delta.z)<.02 else .032
            vs=[]
            for p in (a,c):vs += [p-side*.14+Vector((0,0,-.025)),p+Vector((0,0,raised)),p+side*.14+Vector((0,0,-.025))]
            me.geom(vs,[(0,3,4,1),(1,4,5,2)],'Shingles',(.033,.035,.032))
            if raised>.04:me.beam(a+Vector((0,0,.013)),c+Vector((0,0,.013)),.20,.028,'Shingles',(.017,.018,.016),r=0)
        me.finish()
    # Roof-to-wall step-flashing upstands follow evaluated roof heights.
    for block in b.plan['blocks']:
        for face in ('front','back','left','right'):
            xf,n,l=b.frame(block,face);me=b.mesh(block.name+'_'+face+'_Flashing',component='flashing')
            for poly,adj in wall_sections(b,block,face):
                if not adj:continue
                p,q=poly[0],poly[1]
                if abs(p[0]-q[0])<.005:continue
                a=xf((p[0],.012,p[1]));c=xf((q[0],.012,q[1]))
                me.prism([a,c,c+Vector((0,0,.13)),a+Vector((0,0,.13))],(*n,0),.002,'Trim',(.24,.25,.23))
            me.finish()
    vents=b.mesh('Plumbing_RoofVents',component='roof_vent')
    main=b.plan['blocks'][0]
    for x,y in ((main.cx-2.,main.cy+1.5),(main.cx+1.2,main.cy+2.5)):
        z=main.height(x,y)
        pts=[(x+sx*.175,y+sy*.22) for sx,sy in ((-1,-1),(1,-1),(1,1),(-1,1))]
        vents.prism([(xx,yy,main.height(xx,yy)+.006) for xx,yy in pts],(0,0,-1),.006,'Trim',(.10,.105,.095))
        vents.tube([(x,y,z),(x,y,z+.46)],.045,'Trim',(.075,.078,.071),sides=12,closed=False)
        vents.tube([(x,y,z+.41),(x,y,z+.46)],.049,'Trim',(.075,.078,.071),sides=12,closed=False)
    vents.finish()


def porch(b):
    p=b.plan['porch'];main=b.plan['blocks'][0]
    me=b.mesh('Porch_Concrete',component='porch_steps')
    # Three equal 160 mm risers; landing is 28 mm below threshold.
    me.box((p.cx,p.cy,.24),(2.74,p.depth+.06,.48),'Concrete',r=.008)
    for i,z in enumerate((.16,.32)):
        y=p.y0-.6096+(i+.5)*.3048
        me.box((p.cx,y,z/2),(1.82,.3048,z),'Concrete',r=.005)
        me.box((p.cx,y-.006,z-.008),(1.86,.325,.016),'Concrete',r=.004)
    me.finish()
    columns=b.mesh('Porch_Columns',component='porch_structure')
    for x in (p.x0+.21,p.x1-.21):
        y=p.y0+.20
        columns.box((x,y,(.48+2.88)/2),(.1397,.1397,2.4),r=.004)
        for z in (.51,2.85):columns.box((x,y,z),(.205,.205,.06),r=.003)
        columns.box((x,y,.63),(.166,.166,.22),r=.002)
    columns.box((p.cx,p.y0+.20,2.88),(p.width-.24,.19,.20),r=.002)
    for x in (p.x0+.21,p.x1-.21):columns.box((x,p.cy,2.88),(.14,p.depth-.2,.20),r=.002)
    columns.box((p.cx,p.cy,2.97),(p.width,p.depth,.04),r=.001)
    columns.finish()


def fixture(me,xf,u,z):
    black=(.028,.032,.030)
    me.box((u,.028,z),(.14,.032,.24),'Trim',black,.01,xf)
    me.box((u,.18,z-.025),(.17,.17,.235),'Glass',(.28,.26,.18),.006,xf)
    for side in (-1,1):
        me.box((u+side*.088,.18,z-.025),(.015,.19,.25),'Trim',black,.002,xf)
        me.box((u,.18+side*.089,z-.025),(.19,.014,.25),'Trim',black,.002,xf)
    me.box((u,.18,z+.11),(.23,.23,.035),'Trim',black,.006,xf)
    me.box((u,.18,z-.16),(.19,.19,.045),'Trim',black,.005,xf)
    me.beam(xf((u,.028,z+.045)),xf((u,.18,z+.045)),.023,.025,color=black)
    me.tube([xf((u,.18,z-.11)),xf((u,.18,z-.055))],.007,color=black,sides=8)
    me.tube([xf((u,.18,z-.05)),xf((u,.18,z+.03))],.020,color=(.58,.53,.36),sides=12)


def services(b):
    main,garage=b.plan['blocks'];me=b.mesh('Services',component='services')
    xf,n,l=b.frame(main,'front')
    for u in (main.width/2-.82,main.width/2+.82):fixture(me,xf,u,2.08)
    xf2,n2,l2=b.frame(garage,'front')
    for u in (garage.width/2-2.85,garage.width/2+2.85):fixture(me,xf2,u,2.40)
    face='right' if b.plan['spec']['garage']['side']=='right' else 'left'
    xf,n,l=b.frame(garage,face)
    me.box((l*.50,.068,1.37),(.29,.13,.47),'Trim',(.28,.30,.28),.015,xf)
    center=xf((l*.50,.13,1.51));normal=Vector((*n,0))
    me.tube([center,center+normal*.09],.105,'Trim',(.43,.45,.43),sides=20)
    me.tube([center+normal*.092,center+normal*.10],.079,'Glass',(.22,.28,.25),sides=20)
    me.tube([xf((l*.50,.08,0)),xf((l*.50,.08,1.14))],.022,'Trim',(.30,.32,.30),sides=10)
    me.box((l*.50,.07,2.28),(.085,.075,.075),'Trim',(.26,.28,.26),.004,xf)
    me.tube([xf((l*.50,.07,1.61)),xf((l*.50,.07,2.28))],.016,'Trim',(.30,.32,.30),sides=10)
    xf,n,l=b.frame(main,'back')
    # Hood bends down over an actual dark throat.
    me.box((l*.23,.031,.67),(.17,.038,.17),'Trim',(.23,.24,.22),.005,xf)
    me.prism([xf((l*.23-.095,.06,.76)),xf((l*.23+.095,.06,.76)),xf((l*.23+.095,.17,.64)),xf((l*.23-.095,.17,.64))],(0,0,-1),.006,'Trim',(.31,.33,.30))
    me.tube([xf((l*.72,.022,.61)),xf((l*.72,.13,.61)),xf((l*.72,.16,.56))],.014,'Trim',(.24,.20,.09),sides=10)
    me.box((l*.72,.09,.66),(.075,.075,.012),'Trim',(.20,.13,.055),.002,xf)
    me.finish()
    # Open-license local font; house number is fictional, with no real address.
    curve=bpy.data.curves.new('House number','FONT');curve.body=str(410+b.plan['seed']%400)
    curve.font=bpy.data.fonts.load(str(find_font('DejaVu Sans','Book')));curve.size=.10;curve.extrude=.001;curve.resolution_u=3
    ob=bpy.data.objects.new('HouseNumber',curve);bpy.context.collection.objects.link(ob)
    ob.location=(main.cx-.13,main.y0-.105,2.81);ob.rotation_euler=(math.pi/2,0,0)
    ob.data.materials.append(b.materials[4]);ob.parent=b.root
    bpy.context.view_layer.objects.active=ob;ob.select_set(True);bpy.ops.object.convert(target='MESH');ob.select_set(False)
    attr=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
    for d in attr.data:d.color=(.07,.075,.065,1)
    while len(ob.data.uv_layers)>1:ob.data.uv_layers.remove(ob.data.uv_layers[-1])
    if not ob.data.uv_layers:ob.data.uv_layers.new(name='UVMap')
    ob.data.uv_layers.active.name='UVMap';b.objects.append(ob)
    ob['asset_set']='Houses';ob['part']='Static';ob['component']='number'


def build(plan):
    if plan['spec']['type']=='ranch':
        from ranch_build import build as ranch_build
        return ranch_build(plan)
    b=Builder(plan);shell(b);doors(b);porch(b);roofs(b);services(b)
    from additions import build_additions
    build_additions(b)
    bpy.context.view_layer.update()
    return b


def save(b,out,export=True):
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()))
    triangle_count=0;components={};digest=hashlib.sha256()
    bounds=[]
    for ob in b.objects:
        # Triangulate the actual shipping topology, including concave caps.
        bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.triangulate(bm,faces=bm.faces[:]);bm.to_mesh(ob.data);bm.free()
        ob.data.calc_loop_triangles();count=len(ob.data.loop_triangles);triangle_count+=count
        component=ob.get('component','number');components[component]=components.get(component,0)+count
        bounds.extend([tuple(ob.matrix_world@v.co) for v in ob.data.vertices])
        digest.update(ob.name.encode());digest.update(str([tuple(v.co) for v in ob.data.vertices]).encode())
    report=serialize(b.plan)
    report.update(triangles=triangle_count,components=components,materials=6,meshes=len(b.objects),
                  bounds=[list(map(min,zip(*bounds))),list(map(max,zip(*bounds)))],
                  geometry_sha256=digest.hexdigest(),drains=b.drains,
                  stage='construction checkpoint; no baked or shipped textures')
    out.with_suffix('.json').write_text(json.dumps(report,indent=2))
    # Save again after deterministic triangulation; source and GLB are identical.
    bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()))
    if export:
        # Source keeps diagnostic components; only the fixed shell and moving
        # door survive as draw-call groups in the checkpoint GLB.
        static=[ob for ob in b.objects if ob.parent not in b.moving.values()]
        bpy.ops.object.select_all(action='DESELECT')
        for ob in static:ob.select_set(True)
        bpy.context.view_layer.objects.active=static[0]
        bpy.ops.object.join();static[0].name='House_Static';static[0]['component']='static'
        tiling.export(out.with_suffix('.glb'))
        from glb_budget import compact
        compact(out.with_suffix('.glb'))
    print('HOUSE_REPORT',json.dumps({k:report[k] for k in ('seed','triangles','materials','meshes','bounds','geometry_sha256')}))
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=27);p.add_argument('--plan',type=Path);p.add_argument('--type',choices=('builder_colonial','ranch'))
    p.add_argument('--out',type=Path,default=Path('build/house.blend'));p.add_argument('--no-export',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.read_factory_settings(use_empty=True)
    save(build(load(a.seed,a.plan,a.type)),a.out,not a.no_export)
