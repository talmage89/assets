"""Street-furniture construction helpers around kit's modeling vocabulary.

Coordinates are meters in each footprint frame; every rigid part is owned by
its module or moving pivot. Source print UVs and glazing charts are retained beside the finalized opaque atlas.
"""
import math,json
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
from kit import model as G
M=None;GLASS=None;LAYOUT={};QUALITY='game'

def init():
    global M,GLASS,LAYOUT
    LAYOUT=json.loads(Path('build/graphics.json').read_text());M=bpy.data.materials.new('StreetFurniture_FormSheet');M.use_nodes=True
    p=M.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.48
    n=M.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(Path('build/T_StreetFurniture_Checkpoint.png').resolve()));M.node_tree.links.new(n.outputs['Color'],p.inputs['Base Color'])
    GLASS=bpy.data.materials.new('StreetFurniture_Glazing');GLASS.use_nodes=True;p=GLASS.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.76,.84,.81,1);p.inputs['Transmission Weight'].default_value=1;p.inputs['Roughness'].default_value=.08;p.inputs['IOR'].default_value=1.49

def root(name,loc=(0,0,0)):
    r=G.pivot(name,loc);r['static_root']=True;r['front']='-Y';r['sidewalk_grid_m']=.1524;return r

def pivot(name,pos,parent,axis='X',limits=(0,75)):
    r=G.pivot(name,pos,axis,limits);r.parent=parent;r['static_root']=False;return r

def own(ob,rt,finish='Paint'):
    ob.parent=rt;ob['solid']=True;ob['finish']=finish
    ob['bake_surface']=not any(m==GLASS for m in ob.data.materials)
    if ob.type=='MESH':
        G.apply(ob);uv=ob.data.uv_layers.get('UVMap') or ob.data.uv_layers.new(name='UVMap');r=LAYOUT.get(finish,LAYOUT['Aluminum'])
        for x in uv.data:x.uv=((r[0]+r[2])/2,(r[1]+r[3])/2)
        if not ob['bake_surface']:
            spans=[max(v.co[k] for v in ob.data.vertices)-min(v.co[k] for v in ob.data.vertices) for k in range(3)];axes=sorted(range(3),key=lambda k:spans[k],reverse=True)[:2];axes.sort();lo=[min(v.co[k] for v in ob.data.vertices) for k in axes]
            for f in ob.data.polygons:
                for li in f.loop_indices:
                    v=ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=tuple((v[k]-b)/max(spans[k],1e-8) for k,b in zip(axes,lo))
    return ob

def box(n,p,s,rt,finish='Paint',r=.001,segments=1):return own(G.box(n,p,s,M,r,segments),rt,finish)
def cyl(n,a,b,r,rt,finish='Zinc',s=12):return own(G.cylinder(n,a,b,r,M,s),rt,finish)
def tube(n,path,r,rt,finish='Paint',s=10):return own(G.tube(n,path,r,M,s),rt,finish)
def profile(n,pts,lo,hi,rt,finish='Paint',axis='X',r=0):return own(G.profile(n,pts,lo,hi,M,axis,r,1),rt,finish)
def loft(n,loops,rt,finish='Paint',caps=True):return own(G.loft(n,loops,M,caps),rt,finish)

def bolt(n,p,rt,r=.005,axis=(0,0,1)):
    p=Vector(p);a=Vector(axis);return cyl(n,p,p+a*r*.7,r,rt,'Zinc',6)

def foot(n,x,y,rt,w=.115,d=.085,z=0):
    box(n+' plate',(x,y,z+.006),(w,d,.012),rt,'Paint',.003)
    for s in (-1,1):bolt(n+' expansion anchor',(x+s*w*.31,y,z+.012),rt,.006)
    socket=G.pivot(n+'_Anchor',(x,y,z));socket.parent=rt;socket['socket_kind']='M10 expansion anchor';socket['embedded_depth_m']=.065

def frame(n,x,y,z,w,h,rt,finish='Paint',bar=.035,depth=.04):
    for s in (-1,1):box(n+' stile',(x+s*(w-bar)/2,y,z),(bar,depth,h),rt,finish,.001)
    for s in (-1,1):box(n+' rail',(x,y,z+s*(h-bar)/2),(w-2*bar,depth,bar),rt,finish,.001)

def quad(n,key,x,y,z,w,h,rt):
    ob=G.plane_uv(n,[(x-w/2,y,z-h/2),(x+w/2,y,z-h/2),(x+w/2,y,z+h/2),(x-w/2,y,z+h/2)],M);ob.parent=rt;ob['solid']=False;ob['graphic_key']=key
    uv=ob.data.uv_layers.active;uv.name='UVMap';r=LAYOUT[key]
    for poly in ob.data.polygons:
        for li in poly.loop_indices:
            v=ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=(r[0]+(v.x-x+w/2)/w*(r[2]-r[0]),r[1]+(v.z-z+h/2)/h*(r[3]-r[1]))
    return ob

def glass(n,p,s,rt):return own(G.box(n,p,s,GLASS,0),rt,'White')

def consolidate(rt,join=True):
    """One mesh per static/moving owner, at most sheet plus glass materials."""
    owners=[rt]+[p for p in rt.children_recursive if p.type=='EMPTY' and 'pivot_axis' in p]
    for owner in owners if join else []:
        for baking in (True,False):
            obs=[o for o in owner.children if o.type=='MESH' and bool(o.get('bake_surface'))==baking]
            if not obs:continue
            bpy.ops.object.select_all(action='DESELECT')
            for o in obs:o.select_set(True)
            active=obs[0];bpy.context.view_layer.objects.active=active;bpy.ops.object.join();active.name=owner.name+('_Atlas' if baking else '_GlazingGraphics')
            if baking:active['asset_set']='StreetFurniture'
            G.apply(active);mod=active.modifiers.new('Delivery triangles','TRIANGULATE');G.apply(active)
            mat=active.matrix_basis.copy();active.data.transform(mat);active.matrix_basis=Matrix.Identity(4)
    bpy.context.view_layer.update()
    points=[rt.matrix_world.inverted()@o.matrix_world@v.co for o in rt.children_recursive if o.type=='MESH' for v in o.data.vertices]
    counts=0;materials=set()
    for o in rt.children_recursive:
        if o.type=='MESH':o.data.calc_loop_triangles();counts+=len(o.data.loop_triangles);materials.update(m.name for m in o.data.materials if m)
    bounds=[[float(f(p[k] for p in points)) for k in range(3)] for f in (min,max)]
    rt['footprint_m']=[bounds[1][k]-bounds[0][k] for k in (0,1)]
    socket=G.pivot(rt.name+'_SidewalkSocket',(0,0,0));socket.parent=rt;socket['socket_kind']='Footprint center / finished walk grade';socket['grid_m']=.1524
    return dict(triangles=counts,materials=sorted(materials),bounds_m=bounds,pivots=[dict(name=o.name,position=list(o.location),axis=o['pivot_axis'],range_degrees=list(o['range_degrees'])) for o in owners[1:]])
