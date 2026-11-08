"""House construction helpers and immutable library imports, used in place.

The existing house indexed mesh builds measured gauged skins efficiently.
Only this family's meshes are consolidated; imported meshes retain instancing.
"""
import importlib.util
import math
from pathlib import Path
import sys
import bpy,bmesh
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
_path=sys.path[:];_saved={n:sys.modules.pop(n,None) for n in ('plan','additions','glb_budget')}
sys.path.insert(0,str(ROOT/'houses/src'))
try:
    spec=importlib.util.spec_from_file_location('_trailer_house_mesh',ROOT/'houses/src/build.py')
    H=importlib.util.module_from_spec(spec);spec.loader.exec_module(H)
finally:
    sys.path[:]=_path
    for n,v in _saved.items():
        sys.modules.pop(n,None)
        if v:sys.modules[n]=v
spec=importlib.util.spec_from_file_location('_trailer_native_library',ROOT/'apartments/src/presentation.py')
P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
class Library(P.Library):
    def load(self,path):
        path=Path(path)
        from dependencies import ready
        if not ready(path):
            try:fallback=ROOT/'trailer-park/build/library'/path.relative_to(ROOT)
            except ValueError:fallback=path
            if not fallback.is_file():raise FileNotFoundError(f'Missing native delivery {path}; run make model to prepare immutable inputs')
            path=fallback
        objects=super().load(path)
        # The native presentation adapter discovers imports through a set.
        # Stabilize copy/export order here without changing that shared file.
        objects.sort(key=lambda o:o.name)
        return objects
ROLES=H.ROLES


def palette():
    from PIL import Image
    path=Path('textures/checkpoint/T_ManufacturedForm.png');path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists():Image.new('RGB',(8,8),'white').save(path)
    im=bpy.data.images.load(str(path.resolve()),check_existing=True);out=[]
    for role in ROLES:
        ma=bpy.data.materials.get('ManufacturedForm_'+role)
        if not ma:
            ma=bpy.data.materials.new('ManufacturedForm_'+role);ma.use_nodes=True
            ma['checkpoint_placeholder']=True;ma['tiling_vertex_tint']=True
            ns,ls=ma.node_tree.nodes,ma.node_tree.links;bs=ns.get('Principled BSDF')
            vc=ns.new('ShaderNodeVertexColor');vc.layer_name='Tint'
            tx=ns.new('ShaderNodeTexImage');tx.image=im
            mix=ns.new('ShaderNodeMix');mix.data_type='RGBA';mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
            ls.new(tx.outputs['Color'],mix.inputs[6]);ls.new(vc.outputs['Color'],mix.inputs[7]);ls.new(mix.outputs[2],bs.inputs['Base Color'])
            bs.inputs['Roughness'].default_value=.84 if role!='Glass' else .13
            if role=='Glass':bs.inputs['Transmission Weight'].default_value=1;bs.inputs['IOR'].default_value=1.5
        out.append(ma)
    return out


class Mesh(H.Mesh):
    def box(self,p,s,role='Trim',color=None,r=0,xf=None):return super().box(p,s,role,color,r,xf)
    def finish(self):
        ob=super().finish()
        if ob:
            ob['asset_set']='Manufactured';ob['component']=self.props.get('component',self.name.split('__')[-1])
            if Path('textures/ship/T_Manufactured_Normal.png').exists():
                from surfaces import finish
                finish(ob)
        return ob


class Assembly:
    def __init__(self,name,colors=None):
        self.root=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(self.root)
        self.root['asset_set']='Manufactured';self.root['static_root']=True
        self.colors=dict(Siding=(.4,.4,.32),Shingles=(.065,.06,.05),Veneer=(.2,.16,.10),Concrete=(.28,.27,.24),Trim=(.6,.59,.51),Glass=(.78,.83,.82))
        self.colors.update(colors or {});self.materials=palette();self.moving={};self.objects=[]
    def mesh(self,name,**props):return Mesh(self,self.root.name+'__'+name,**props)
    def socket(self,name,p,kind='attachment',yaw=0,**extras):
        o=bpy.data.objects.new(self.root.name+'__'+name,None);bpy.context.collection.objects.link(o);o.parent=self.root;o.location=p
        o.rotation_euler.z=math.radians(yaw);o['socket_kind']=kind
        for k,v in extras.items():o[k]=v
        return o
    def pivot(self,name,p,limits=(-100,0)):
        o=self.socket(name,p,'hinge');o['pivot_axis']='Z';o['range_degrees']=limits;o['static_root']=False
        self.moving[o.name]=o;return o


def label(a,text,p,size=.18,color=(.63,.61,.51),yaw=0):
    from kit.fonts import find_font
    curve=bpy.data.curves.new('Fictional lettering','FONT');curve.body=text;curve.size=size;curve.align_x='CENTER';curve.resolution_u=2
    curve.font=bpy.data.fonts.load(str(find_font('DejaVu Sans','Book')))
    ob=bpy.data.objects.new(a.root.name+'__Label_'+text,curve);bpy.context.collection.objects.link(ob);ob.parent=a.root
    ob.location=p;ob.rotation_euler=(math.pi/2,0,math.radians(yaw));ob.data.materials.append(a.materials[4])
    bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH')
    ob['asset_set']='Manufactured';attr=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT');ob.data.color_attributes.active_color=attr
    for v in attr.data:v.color=(*color,1)
    for old_uv in list(ob.data.uv_layers):ob.data.uv_layers.remove(old_uv)
    uv=ob.data.uv_layers.new(name='UVMap')
    for f in ob.data.polygons:
        for li in f.loop_indices:
            v=ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=(v.x,v.y)
    if Path('textures/ship/T_Manufactured_Normal.png').exists():
        from surfaces import finish
        finish(ob)
    return ob


def place(root,p=(0,0,0),yaw=0,parent=None):
    root.parent=parent;root.location=p;root.rotation_euler.z=math.radians(yaw);return root


def consolidate(root=None):
    bpy.context.view_layer.update()
    scope=set([root,*root.children_recursive]) if root else set(bpy.context.scene.objects)
    for parent in sorted([o for o in scope if o.type=='EMPTY' and o.get('asset_set')=='Manufactured'],key=lambda o:o.name):
        obs=sorted([o for o in parent.children if o.type=='MESH' and o.get('asset_set')=='Manufactured'],key=lambda o:o.name)
        if not obs:continue
        if len(obs)==1 and obs[0].get('consolidated'):continue
        bpy.ops.object.select_all(action='DESELECT')
        for ob in obs:ob.select_set(True)
        bpy.context.view_layer.objects.active=obs[0]
        if len(obs)>1:
            bpy.ops.object.join();bpy.context.object['component']='fixed_assembly'
        ob=bpy.context.object;ob.name=parent.name+'__Mesh';ob.data.transform(ob.matrix_basis);ob.matrix_basis=Matrix.Identity(4);ob['consolidated']=True
    seen=set()
    for ob in list(root.children_recursive) if root else bpy.context.scene.objects:
        if ob.type!='MESH' or ob.data in seen:continue
        seen.add(ob.data)
        # Imported mesh normals/leaf cards remain exactly as delivered.
        if ob.get('asset_set')=='Manufactured':
            bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free();ob.data.update()
            tint=ob.data.color_attributes.get('Tint')
            if tint:ob.data.color_attributes.render_color_index=ob.data.color_attributes.find('Tint')


class Instances:
    """Build a bounded variant once, collapse its fixed parts, share meshes."""
    def __init__(self):self.templates={}
    def get(self,key,name,factory):
        if key not in self.templates:
            root=factory().root;consolidate(root);self.templates[key]=root
            root['instance_template']=str(key);return root
        template=self.templates[key];mapping={}
        for old in [template,*sorted(template.children_recursive,key=lambda o:o.name)]:
            ob=old.copy();bpy.context.collection.objects.link(ob);mapping[old]=ob
            ob.name=old.name.replace(template.name,name,1)
        for old,ob in mapping.items():
            ob.parent=mapping.get(old.parent);ob.matrix_basis=old.matrix_basis.copy()
        rt=mapping[template];rt['instance_template']=str(key);return rt


def native(lib,path,name,p=(0,0,0),yaw=0,select=None,parent=None):
    root=lib.place(ROOT/path,name,p,yaw,select=select);root.parent=parent;root['presentation_only']=False
    # The grill's glTF importer creates a material-less custom bone display
    # sphere. It is an editor helper, absent from its evaluated game geometry.
    for ob in list(root.children_recursive):
        if ob.type=='MESH' and not ob.data.materials and 'Icosphere' in ob.name:bpy.data.objects.remove(ob,do_unlink=True)
    root['reused_library']=path
    return root
