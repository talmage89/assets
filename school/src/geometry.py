"""Use the houses' indexed construction mesh without changing its delivery.

The six house roles are temporary semantic slots: CMU, roof, brick, mineral,
equipment/paint, glazing. The shared image is explicitly a form placeholder.
"""
import importlib.util
from pathlib import Path
import sys,math
import bpy,bmesh
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
_saved_path=sys.path[:];_saved={n:sys.modules.pop(n,None) for n in ('plan','additions','glb_budget')}
sys.path.insert(0,str(ROOT/'houses/src'))
try:
    spec=importlib.util.spec_from_file_location('_school_house_mesh',ROOT/'houses/src/build.py')
    H=importlib.util.module_from_spec(spec);spec.loader.exec_module(H)
finally:
    sys.path[:]=_saved_path
    for n,v in _saved.items():
        sys.modules.pop(n,None)
        if v:sys.modules[n]=v
ROLES=H.ROLES


def palette():
    from PIL import Image
    folder=Path('textures/checkpoint');folder.mkdir(parents=True,exist_ok=True)
    path=folder/'T_School_Form.png'
    if not path.exists():Image.new('RGB',(8,8),'white').save(path)
    im=bpy.data.images.load(str(path.resolve()),check_existing=True);out=[]
    for role in ROLES:
        ma=bpy.data.materials.get('SchoolForm_'+role)
        if not ma:
            ma=bpy.data.materials.new('SchoolForm_'+role);ma.use_nodes=True;ma['checkpoint_placeholder']=True
            ns,ls=ma.node_tree.nodes,ma.node_tree.links;bs=ns.get('Principled BSDF')
            tx=ns.new('ShaderNodeTexImage');tx.image=im
            vc=ns.new('ShaderNodeVertexColor');vc.layer_name='Tint'
            mix=ns.new('ShaderNodeMix');mix.data_type='RGBA';mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
            ls.new(tx.outputs['Color'],mix.inputs[6]);ls.new(vc.outputs['Color'],mix.inputs[7]);ls.new(mix.outputs[2],bs.inputs['Base Color'])
            ma['tiling_vertex_tint']=True
            bs.inputs['Roughness'].default_value=.86 if role in ('Veneer','Siding','Concrete','Shingles') else .48
            if role=='Glass':bs.inputs['Transmission Weight'].default_value=1;bs.inputs['Roughness'].default_value=.12
        out.append(ma)
    return out


class Mesh(H.Mesh):
    def box(self,p,s,role='Trim',color=None,r=0,xf=None):return super().box(p,s,role,color,r,xf)
    def finish(self):
        ob=super().finish()
        if ob:ob['asset_set']='School';ob['solid']=self.props.get('solid',True)
        return ob


class Assembly:
    def __init__(self,name,colors=None,parent=None):
        from kit.model import pivot
        self.root=pivot(name,(0,0,0));self.root.parent=parent;self.root['asset_set']='School';self.root['static_root']=True
        self.colors=dict(Siding=(.34,.32,.26),Shingles=(.085,.085,.074),Veneer=(.235,.082,.040),Concrete=(.32,.32,.285),Trim=(.065,.12,.17),Glass=(.75,.82,.81))
        self.colors.update(colors or {});self.materials=palette();self.moving={};self.objects=[]
    def mesh(self,name,**props):return Mesh(self,self.root.name+'__'+name,**props)
    def pivot(self,name,point,yaw=0,axis='Z',limits=(-100,0)):
        from kit.model import pivot
        ob=pivot(self.root.name+'__'+name,point);ob.parent=self.root
        # Mesh points are global construction coordinates. Apply face yaw in
        # vertices before the stock Mesh rebases them to this physical hinge.
        ob['pivot_axis']=axis;ob['range_degrees']=limits;ob['static_root']=False
        self.moving[ob.name]=ob;return ob
    def socket(self,name,point,kind='walk',yaw=0):
        from kit.model import pivot
        ob=pivot(self.root.name+'__'+name,point);ob.parent=self.root;ob.rotation_euler.z=math.radians(yaw);ob['socket_kind']=kind;return ob


def orient(m,origin,yaw):
    a=math.radians(yaw);c,s=math.cos(a),math.sin(a)
    if len(origin)==2:origin=(*origin,0)
    m.v=[(origin[0]+x*c-y*s,origin[1]+x*s+y*c,origin[2]+z) for x,y,z in m.v];return m


def label(a,text,p,size=.24,color=(.68,.69,.64),yaw=0):
    from kit.fonts import find_font
    curve=bpy.data.curves.new('School original lettering','FONT');curve.body=text;curve.size=size;curve.align_x='CENTER';curve.extrude=.004;curve.resolution_u=1
    curve.font=bpy.data.fonts.load(str(find_font('DejaVu Sans','Book')))
    ob=bpy.data.objects.new(a.root.name+'__Letters_'+text,curve);bpy.context.collection.objects.link(ob);ob.parent=a.root
    ob['asset_set']='School'
    ob.location=p;ob.rotation_euler=(math.pi/2,0,math.radians(yaw));ob.data.materials.append(a.materials[4])
    bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH')
    attr=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
    ob.data.color_attributes.active_color=attr
    for v in attr.data:v.color=(*color,1)
    uv=ob.data.uv_layers.new(name='UVMap')
    for f in ob.data.polygons:
        axes=sorted(range(3),key=lambda k:abs(f.normal[k]))[:2]
        for li in f.loop_indices:
            v=ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]],v[axes[1]])
    return ob


def consolidate(asset_set='School'):
    """Static parts join by ownership; operating leaves retain their hinge."""
    bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH':continue
        if ob.modifiers:
            ob.data=bpy.data.meshes.new_from_object(ob.evaluated_get(dg),depsgraph=dg,preserve_all_data_layers=True);ob.modifiers.clear()
    # Imported instanced modules are already consolidated. School construction
    # is the only data joined here; joining botanical copies destroys sharing.
    for parent in sorted([o for o in bpy.context.scene.objects if o.get('asset_set')==asset_set and o.type=='EMPTY'],key=lambda o:o.name):
        obs=sorted([o for o in parent.children if o.type=='MESH' and o.get('asset_set')==asset_set],key=lambda o:o.name)
        if not obs:continue
        bpy.ops.object.select_all(action='DESELECT')
        for ob in obs:ob.select_set(True)
        bpy.context.view_layer.objects.active=obs[0]
        if len(obs)>1:bpy.ops.object.join()
        ob=bpy.context.object;ob.name=parent.name+'__Mesh'
        if ob.data.users>1:ob.data=ob.data.copy()
        ob.data.transform(ob.matrix_basis);ob.matrix_basis=Matrix.Identity(4)
    seen=set()
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.data in seen:continue
        if not ob.data.uv_layers:
            uv=ob.data.uv_layers.new(name='UVMap')
            for f in ob.data.polygons:
                axes=sorted(range(3),key=lambda k:abs(f.normal[k]))[:2]
                for li in f.loop_indices:
                    v=ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]],v[axes[1]])
        bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free();ob.data.update();seen.add(ob.data)
