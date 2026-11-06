"""Checkpoint construction vocabulary. Meters, +Z up, local -Y approaches.

All shapes are original analytic surfaces. Mesh UVs are provisional metric
charts for the later tile/trim pass; no photograph is ever a material input.
"""
import math
import bpy
from mathutils import Vector, Matrix
from kit import model as G

M={}

def material(name,color,rough=.7,metal=0):
    m=bpy.data.materials.new(name);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
    m.diffuse_color=(*color,1);m['stage']='quick form material; no final finish';return m

def palette():
    for k,c,r,m in [('Concrete',(.32,.315,.295),.72,0),('Side',(.24,.245,.23),.84,0),
                   ('Steel',(.12,.135,.14),.37,.85),('Paint',(.025,.055,.05),.58,.15),
                   ('Tile',(.035,.10,.14),.28,0),('Grout',(.21,.22,.20),.88,0),
                   ('Coping',(.34,.33,.29),.67,0),('Composite',(.14,.105,.073),.72,0),
                   ('Zinc',(.35,.38,.39),.52,.85),('Joint',(.065,.059,.047),.9,0),
                   ('Asphalt',(.075,.08,.078),.91,0),('Lawn',(.055,.082,.023),.93,0),
                   ('White',(.65,.64,.58),.67,0),('Black',(.012,.016,.014),.73,0)]:
        M[k]=material('Skate_Form_'+k,c,r,m)

def root(name,kind='skating'):
    o=G.pivot(name,(0,0,0));o['module_kind']=kind;o['grid_m']=.1524;o['stage']='form checkpoint';return o

def own(o,rt,kind=None):
    o.parent=rt
    if kind:o['construction_role']=kind
    if o.modifiers:G.apply(o)
    if o.type=='MESH' and not o.data.uv_layers:
        uv=o.data.uv_layers.new(name='UVMap')
        for f in o.data.polygons:
            axes=sorted(range(3),key=lambda k:abs(f.normal[k]))[:2];axes.sort()
            for li in f.loop_indices:
                p=o.matrix_basis@o.data.vertices[o.data.loops[li].vertex_index].co
                uv.data[li].uv=(p[axes[0]]/3.048,p[axes[1]]/3.048)
    return o

def mesh(n,v,f,rt,mat='Concrete',smooth=False):
    o=G.mesh(n,v,f,M[mat]);own(o,rt)
    if smooth:G.smooth(o,35)
    return o

def box(n,p,s,rt,mat='Concrete',r=.002):return own(G.box(n,p,s,M[mat],r,1),rt)
def cyl(n,a,b,r,rt,mat='Steel',s=12):return own(G.smooth(G.cylinder(n,a,b,r,M[mat],s),40),rt)
def tube(n,pts,r,rt,mat='Steel',s=12):return own(G.smooth(G.tube(n,pts,r,M[mat],s),40),rt)
def profile(n,pts,lo,hi,rt,mat='Concrete',axis='X'):return own(G.profile(n,pts,lo,hi,M[mat],axis=axis),rt)

def beam(n,a,b,w,rt,mat='Zinc',d=None):
    a,b=Vector(a),Vector(b);o=box(n,(a+b)/2,(w,d or w,(b-a).length),rt,mat,0)
    o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o

def socket(rt,name,pos,direction=(0,1,0),kind='ride_line'):
    o=G.pivot(rt.name+'__'+name,(0,0,0));o.parent=rt;o.location=pos
    o.rotation_euler=Vector(direction).to_track_quat('Y','Z').to_euler();o['socket_kind']=kind
    o['direction_local']=direction;return o

def describe(rt,footprint,**kw):
    rt['footprint_m']=footprint
    for k,v in kw.items():rt[k]=v
    return rt

def join(rt):
    """One fixed mesh per module, preserving physical moving children."""
    for owner in [rt]+[o for o in rt.children_recursive if 'pivot_axis' in o]:
        obs=[o for o in owner.children if o.type=='MESH']
        if not obs:continue
        if len(obs)==1 and all(len(f.vertices)==3 for f in obs[0].data.polygons) and obs[0].matrix_basis==Matrix.Identity(4):
            continue  # Already finalized linked library instance: retain sharing.
        for ob in obs:
            if ob.data.users>1:ob.data=ob.data.copy()
        # Carry normals as ordinary corner data through join/triangulation;
        # Blender 5.2 can otherwise re-encode them against new smoothing fans.
        for ob in obs:
            saved=ob.data.attributes.get('CheckpointNormal') or ob.data.attributes.new('CheckpointNormal','FLOAT_VECTOR','CORNER')
            to_owner=ob.matrix_basis.to_3x3().inverted().transposed()
            for row,n in zip(saved.data,ob.data.corner_normals):row.vector=(to_owner@n.vector).normalized()
        bpy.ops.object.select_all(action='DESELECT')
        for o in obs:o.select_set(True)
        bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();o=obs[0];o.name=owner.name+'_Mesh'
        o.data.transform(o.matrix_basis);o.matrix_basis=Matrix.Identity(4)
        mod=o.modifiers.new('Actual triangles','TRIANGULATE');mod.keep_custom_normals=True;G.apply(o)
        saved=o.data.attributes.get('CheckpointNormal')
        if saved:
            o.data.normals_split_custom_set([row.vector[:] for row in saved.data]);o.data.attributes.remove(saved)

def count(rt):
    n=0
    for o in [rt,*rt.children_recursive]:
        if o.type=='MESH':o.data.calc_loop_triangles();n+=len(o.data.loop_triangles)
    return n

def instance(src,name,loc=(0,0,0),yaw=0,parent=None):
    copies={o:o.copy() for o in [src,*src.children_recursive]}
    for o,c in copies.items():
        bpy.context.collection.objects.link(c);c.parent=copies.get(o.parent,parent);c.matrix_basis=o.matrix_basis.copy()
    rt=copies[src];rt.name=name;rt.location=loc
    # glTF imports use quaternion mode even for an identity construction frame.
    # Euler assignments are ignored until the active rotation mode is changed.
    rt.rotation_mode='XYZ';rt.rotation_euler=(0,0,math.radians(yaw));return rt
