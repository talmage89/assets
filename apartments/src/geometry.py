"""Reuse the house family's batched construction mesh and six-role contract.

The import is scoped: no mutation of its sources, materials, plans or deliveries.
The house Mesh supplies gauged prisms, bevels, beams, tubes and metric charts.
"""
import importlib.util
import sys
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[2]
_saved_path=sys.path[:];_saved={n:sys.modules.pop(n,None) for n in ('plan','additions','glb_budget')}
sys.path.insert(0,str(ROOT/'houses/src'))
try:
    spec=importlib.util.spec_from_file_location('_apartments_house_construction',ROOT/'houses/src/build.py')
    H=importlib.util.module_from_spec(spec);spec.loader.exec_module(H)
finally:
    sys.path[:]=_saved_path
    for n,value in _saved.items():
        sys.modules.pop(n,None)
        if value:sys.modules[n]=value
ROLES=H.ROLES


class Mesh(H.Mesh):
    def finish(self):
        ob=super().finish()
        if ob:ob['asset_set']='Apartments'
        return ob


class Assembly:
    def __init__(self,name,colors=None,parent=None,loc=(0,0,0),yaw=0,materials=None):
        from kit.model import pivot
        self.root=pivot(name,loc);self.root.parent=parent;self.root.rotation_euler.z=__import__('math').radians(yaw)
        self.root['static_root']=True;self.root['asset_set']='Apartments'
        self.colors=dict(Siding=(.32,.34,.28),Shingles=(.055,.045,.035),Veneer=(.26,.115,.065),Concrete=(.29,.28,.25),Trim=(.55,.54,.48),Glass=(.85,.87,.86))
        self.colors.update(colors or {});self.materials=materials or palette();self.moving={};self.objects=[]
    def mesh(self,name,**props):return Mesh(self,self.root.name+'__'+name,**props)
    def pivot(self,name,p,slide=False,yaw=0):
        from kit.model import pivot
        ob=pivot(self.root.name+'__'+name,p);ob.parent=self.root;ob.rotation_euler.z=__import__('math').radians(yaw)
        ob['slide_axis' if slide else 'pivot_axis']='X' if slide else 'Z'
        ob['range_m' if slide else 'range_degrees']=(0,.86) if slide else (0,100)
        # Mesh.finish expects pivots in world coordinates; construction is local.
        self.moving[ob.name]=ob;return ob
    def socket(self,name,p,kind='walk',yaw=0):
        from kit.model import pivot
        ob=pivot(self.root.name+'__'+name,p);ob.parent=self.root;ob['socket_kind']=kind
        ob.rotation_euler.z=__import__('math').radians(yaw);return ob


def palette():
    # Quick materials, no look-dev. Same external diagnostic image for all roles.
    from PIL import Image
    folder=Path('export/shared');folder.mkdir(parents=True,exist_ok=True)
    path=folder/'T_Apartments_FormWhite.png'
    if not path.exists():Image.new('RGB',(8,8),'white').save(path)
    image=bpy.data.images.load(str(path.resolve()),check_existing=True)
    mats=[]
    for role in ROLES:
        existing=bpy.data.materials.get('ApartmentsForm_'+role)
        if existing:mats.append(existing);continue
        m=bpy.data.materials.new('ApartmentsForm_'+role);m.use_nodes=True;m['checkpoint_placeholder']=True
        ns,ls=m.node_tree.nodes,m.node_tree.links;p=ns.get('Principled BSDF')
        v=ns.new('ShaderNodeVertexColor');v.layer_name='Tint'
        t=ns.new('ShaderNodeTexImage');t.image=image
        mix=ns.new('ShaderNodeMix');mix.data_type='RGBA';mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
        ls.new(t.outputs['Color'],mix.inputs[6]);ls.new(v.outputs['Color'],mix.inputs[7]);ls.new(mix.outputs[2],p.inputs['Base Color'])
        p.inputs['Roughness'].default_value=.85 if role in ('Siding','Veneer','Shingles','Concrete') else .48
        if role=='Glass':p.inputs['Transmission Weight'].default_value=1;p.inputs['Roughness'].default_value=.13
        mats.append(m)
    return mats


def finish_local(m):
    # House geometry was authored in world coordinates. Rebase here in the local
    # building frame before its final placement, retaining physical door pivots.
    if m.part in m.builder.moving:
        pivot=m.builder.moving[m.part]
        old=pivot.matrix_world.copy();bpy.context.view_layer.update()
        # Temporarily treat the building as an identity frame for house finish.
        xf=m.builder.root.matrix_world.copy();m.v=[tuple(xf@Vector(v)) for v in m.v]
    return m.finish()


def label(a,text,p,size=.10,color=(.7,.68,.58),yaw=0):
    from kit.fonts import find_font
    import math
    curve=bpy.data.curves.new('Unit numbering','FONT');curve.body=text;curve.size=size;curve.align_x='CENTER';curve.extrude=0
    curve.font=bpy.data.fonts.load(str(find_font('DejaVu Sans','Book')))
    ob=bpy.data.objects.new(a.root.name+'__Label_'+text,curve);bpy.context.collection.objects.link(ob);ob.parent=a.root
    ob.location=p;ob.rotation_euler=(math.pi/2,0,math.radians(yaw));ob.data.materials.append(a.materials[4])
    bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH')
    for uv in list(ob.data.uv_layers):ob.data.uv_layers.remove(uv)
    attr=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
    for v in attr.data:v.color=(*color,1)
    a.objects.append(ob);return ob
