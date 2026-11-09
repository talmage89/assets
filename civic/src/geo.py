"""Indexed native construction mesh, physical shared charts and owned tint."""
import importlib.util,math,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];LOCAL=ROOT/'civic'
sys.path.insert(0,str(ROOT))
saved=sys.path[:];modules={n:sys.modules.pop(n,None) for n in ('plan','additions','glb_budget')}
sys.path.insert(0,str(ROOT/'houses/src'))
spec=importlib.util.spec_from_file_location('_civic_native_mesh',ROOT/'houses/src/build.py')
H=importlib.util.module_from_spec(spec);spec.loader.exec_module(H)
sys.path[:]=saved
for n,v in modules.items():
    sys.modules.pop(n,None)
    if v:sys.modules[n]=v
spec=importlib.util.spec_from_file_location('_civic_shared_charts',ROOT/'downtown/src/surfaces.py')
DS=importlib.util.module_from_spec(spec);spec.loader.exec_module(DS)
ROLES=H.ROLES


def root(name,parent=None,p=(0,0,0)):
    ob=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(ob)
    ob.parent=parent;ob.location=p;ob['asset_set']='Civic';return ob


def palette():
    from kit.tiling import material
    from io_scene_gltf2.blender.imp.pbrMetallicRoughness import get_settings_group
    get_settings_group();out=[]
    for role in ROLES:
        key='Civic_'+role;ma=bpy.data.materials.get(key)
        if not ma:
            if role=='Glass':
                ma=bpy.data.materials.new(key);ma.use_nodes=True;ma['tiling_vertex_tint']=False
                bs=ma.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.94,.97,.96,1)
                bs.inputs['Transmission Weight'].default_value=1;bs.inputs['IOR'].default_value=1.5;bs.inputs['Roughness'].default_value=.025
            else:
                family='commercial' if role=='Siding' else 'downtown'
                name='CommercialCMU' if role=='Siding' else 'DowntownMasonry' if role=='Veneer' else 'DowntownFinish' if role=='Trim' else 'DowntownMineralRoof'
                ma=material(name,LOCAL/'textures/shared'/family/'textures/ship',tint=True);ma.name=key
                if role=='Siding':next(n for n in ma.node_tree.nodes if n.type=='NORMAL_MAP').inputs['Strength'].default_value=.25
        out.append(ma)
    return out


class Mesh(H.Mesh):
    def geom(self,vs,fs,role='Trim',color=None):
        if role=='Veneer':
            for f in fs:
                for poly,uv in DS.masonry_faces([tuple(vs[i]) for i in f],self.props.get('brick_strip',0)):
                    super().geom(poly,[tuple(range(len(poly)))],role,color)
        else:super().geom(vs,fs,role,color)

    def finish(self):
        ob=super().finish()
        if not ob:return
        ob['asset_set']='Civic';ob['module_kind']=self.props.get('kind',self.name.split('__')[-1])
        me=ob.data;uv=me.uv_layers.active
        attr=me.color_attributes.get('Tint');values=[tuple(c.color[:3]) for c in attr.data]
        me.color_attributes.remove(attr);attr=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER');me.color_attributes.active_color=attr
        for f in me.polygons:
            role=ROLES[f.material_index];axis=max(range(3),key=lambda k:abs(f.normal[k]));a,b=[(1,2),(0,2),(0,1)][axis]
            span=max(me.vertices[i].co[b] for i in f.vertices)-min(me.vertices[i].co[b] for i in f.vertices)
            low=min(me.vertices[i].co[b] for i in f.vertices)
            for li in f.loop_indices:
                i=me.loops[li].vertex_index;q=me.vertices[i].co;c=values[i];factor=1
                if self.props.get('weather'):
                    reach=.43+.09*math.sin(q.x*7+q.y*4)
                    factor-=.36*max(0,1-max(0,q.z-.05)/reach)
                    top=self.props.get('top',9);fall=max(0,top-q.z)
                    joint=abs((q[a]+.3)%2.4384-1.2192)
                    factor-=.24*math.exp(-(joint/.15)**2)*math.exp(-fall/.65)
                if role=='Veneer':
                    strip=self.props.get('brick_strip',0);k=math.floor((low+1e-6)/1.2192)
                    vv=(q.z/1.2192-k) if b==2 else (q[b]-low)/max(span,1e-6)
                    uv.data[li].uv=(q[a]/4.8768,strip/4+8/2048+max(0,min(1,vv))*(.25-16/2048))
                elif role=='Siding':uv.data[li].uv=(q[a]/2.4384,q[b]/2.4384);c=tuple(v/.278 for v in c)
                elif role=='Glass':uv.data[li].uv=(q[a],q[b]);c=(1,1,1)
                else:
                    n=8 if role=='Trim' else 4
                    strip=self.props.get('trim_strip',1) if role=='Trim' else 2 if role=='Shingles' else self.props.get('stone_strip',0)
                    uv.data[li].uv=(q[a]/4,strip/n+8/2048+(q[b]-low)/max(span,1e-6)*(1/n-16/2048))
                attr.data[li].color=(*(max(0,min(1,v*factor)) for v in c),1)
        bm=bmesh.new();bm.from_mesh(me);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
        return ob


class Assembly:
    def __init__(self,name):
        self.root=root(name);self.root['static_root']=True;self.objects=[];self.moving={};self.materials=palette()
        self.colors=dict(Veneer=(1,1,1),Concrete=(.48,.46,.405),Trim=(.065,.082,.073),Glass=(1,1,1),Siding=(.32,.31,.285),Shingles=(.095,.098,.091))
    def mesh(self,name,**props):return Mesh(self,self.root.name+'__'+name,**props)
    def pivot(self,name,p,axis='Z',limits=(0,100)):
        ob=root(self.root.name+'__'+name,self.root,p);ob['pivot_axis']=axis;ob['range_degrees']=limits
        self.moving[name]=ob;return ob
    def socket(self,name,p,kind='attachment'):
        ob=root(self.root.name+'__Socket_'+name,self.root,p);ob['socket_kind']=kind;return ob


def orient(m,p,yaw):
    r=math.radians(yaw);c,s=math.cos(r),math.sin(r)
    m.v=[(p[0]+x*c-y*s,p[1]+x*s+y*c,p[2]+z) for x,y,z in m.v];return m


def text(a,name,string,p,size,color=(.1,.105,.09)):
    from kit.fonts import find_font
    cv=bpy.data.curves.new(name,'FONT');cv.body=string;cv.size=size;cv.align_x='CENTER';cv.resolution_u=2;cv.extrude=.003
    cv.font=bpy.data.fonts.load(str(find_font('DejaVu Serif','Book')))
    ob=bpy.data.objects.new(a.root.name+'__'+name,cv);bpy.context.collection.objects.link(ob);ob.parent=a.root
    ob.location=p;ob.rotation_euler.x=math.pi/2;cv.materials.append(a.materials[4]);ob['asset_set']='Civic'
    bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH')
    ma=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT');ob.data.color_attributes.active_color=ma
    for c in ma.data:c.color=(*color,1)
    uv=ob.data.uv_layers.new(name='UVMap')
    for row in uv.data:row.uv=(.125,.18)
    a.objects.append(ob);return ob
