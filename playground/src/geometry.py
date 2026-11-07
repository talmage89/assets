"""Small asset-specific construction vocabulary; meters, footprint roots, -Y entry.

Only original analytic sections. kit supplies sweeps, manufactured edges and mesh
normal recalculation. Optional baked manufacture charts retain period vertex tints.
"""
import math
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
from kit import model as G
M={}
COLORS=dict(steel=(.026,.105,.062,1),rail=(.65,.35,.025,1),red=(.54,.029,.018,1),blue=(.018,.145,.36,1),green=(.023,.21,.13,1),yellow=(.84,.51,.035,1),deck=(.022,.026,.025,1),zinc=(.34,.38,.40,1),rubber=(.008,.010,.009,1),fiber=(.31,.18,.075,1),wood=(.12,.071,.034,1),rubberfloor=(.035,.13,.115,1),accent=(.41,.17,.065,1),concrete=(.33,.34,.32,1))

FINISHES=('steel','rail','red','green','blue','yellow','deck','zinc','rubber','fiber','wood','rubberfloor','accent','concrete','custom')

LOOK=False

def init(look=False):
    global LOOK
    LOOK=look
    if look:
        from uv_finish import init as finish_init
        M.update(finish_init());return
    for key,rough,metal in [('Frame',.43,0),('Molded',.31,0),('Site',.86,0)]:
        mat=bpy.data.materials.new('Playground_Quick'+key);mat.use_nodes=True
        p=mat.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
        n=mat.node_tree.nodes.new('ShaderNodeVertexColor');n.layer_name='Tint';mat.node_tree.links.new(n.outputs['Color'],p.inputs['Base Color']);M[key]=mat
    mat=bpy.data.materials.new('Playground_QuickChain');mat.use_nodes=True
    p=mat.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.54
    im=bpy.data.images.new('T_Playground_CheckpointChain',64,512,alpha=True)
    values=[]
    for y in range(512):
        for x in range(64):
            xx=(x-31.5)/17.4;yy=((y+16)%64-32)/16.2
            ellipse=abs((xx*xx+yy*yy)**.5-1)<.23
            edge=abs(x-31.5)<5.3 and abs((y+48)%64-32)<20
            a=1 if ellipse or edge else 0
            values.extend([.18,.19,.18,a])
    im.pixels[:]=values;im.filepath_raw=str(Path('build/T_Playground_CheckpointChain.png').resolve());im.file_format='PNG';im.save()
    tex=mat.node_tree.nodes.new('ShaderNodeTexImage');tex.image=im
    mat.node_tree.links.new(tex.outputs['Color'],p.inputs['Base Color']);mat.node_tree.links.new(tex.outputs['Alpha'],p.inputs['Alpha']);mat.surface_render_method='DITHERED';mat.use_backface_culling=False;M['Chain']=mat
    # Original pin perforation diagnostic. No photograph or downloaded texel.
    mat=bpy.data.materials.new('Playground_QuickPerforated');mat.use_nodes=True
    p=mat.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.68
    im=bpy.data.images.new('T_Playground_CheckpointDeck',128,128,alpha=False)
    a=[]
    for y in range(128):
        for x in range(128):
            d=((x%16-8)**2+(y%16-8)**2)**.5
            v=.018 if d>3 else .002
            a.extend([v,v*1.08,v,1])
    im.pixels[:]=a;im.filepath_raw=str(Path('build/T_Playground_CheckpointDeck.png').resolve());im.file_format='PNG';im.save()
    tex=mat.node_tree.nodes.new('ShaderNodeTexImage');tex.image=im;tex.interpolation='Linear';mat.node_tree.links.new(tex.outputs['Color'],p.inputs['Base Color']);M['Deck']=mat

def root(name,kind=None):
    o=G.pivot(name,(0,0,0));o['module']=kind or name;o['static_root']=True;o['asset_set']='Playground';return o

def empty(parent,name,pos,kind,axis=None,limits=None):
    o=G.pivot(name,pos,axis,limits);o.parent=parent;o['socket_kind']=kind if axis is None else 'motion_pivot';return o

def own(ob,parent,finish='steel',material='Frame'):
    ob.parent=parent;ob['solid']=True;ob['construction']=ob.name;ob['finish_key']=finish if isinstance(finish,str) else 'custom';ob['material_family']=material
    G.apply(ob)
    fc=ob.data.attributes.new(name='FinishCode',type='INT',domain='FACE')
    for d in fc.data:d.value=FINISHES.index(finish) if finish in FINISHES else 14
    c=(1,1,1,1) if LOOK and (finish=='zinc' or (finish=='deck' and material=='Frame')) else COLORS.get(finish,finish)
    tint=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER')
    for d in tint.data:d.color=c
    uv=ob.data.uv_layers.active or ob.data.uv_layers.new(name='UVMap')
    # Checkpoint UVs tile by manufactured surface; final atlases are deferred.
    for f in ob.data.polygons:
        axes=sorted(range(3),key=lambda k:abs(f.normal[k]))[:2]
        for li in f.loop_indices:
            v=ob.matrix_basis@ob.data.vertices[ob.data.loops[li].vertex_index].co
            uv.data[li].uv=(v[axes[0]]/.16,v[axes[1]]/.16)
    ob.data.materials.clear();ob.data.materials.append(M[material])
    if LOOK:
        from uv_finish import assign
        assign(ob,finish,material)
    return ob

def box(parent,n,p,s,finish='steel',r=.001,mat='Frame'):
    return own(G.box(n,p,s,M[mat],r,1),parent,finish,mat)
def cyl(parent,n,a,b,r,finish='steel',s=12,mat='Frame'):
    return own(G.cylinder(n,a,b,r,M[mat],s),parent,finish,mat)
def tube(parent,n,pts,r,finish='rail',s=8,mat='Frame'):
    return own(G.tube(n,pts,r,M[mat],s),parent,finish,mat)
def loft(parent,n,loops,finish='red',mat='Molded',caps=True,closed=True):
    return own(G.smooth(G.loft(n,loops,M[mat],caps,closed),65),parent,finish,mat)
def lathe(parent,n,section,finish='steel',s=16,center=(0,0),axis='Z',mat='Frame',closed=False):
    return own(G.lathe(n,section,M[mat],s,axis,center,closed),parent,finish,mat)
def bolt(parent,p,axis=(0,-1,0),r=.008):
    p=Vector(p);return cyl(parent,'Recessed M10 pin bolt',p,p+Vector(axis)*.007,r,'zinc',6)

def clamp(parent,x,y,z,yaw=0):
    # Smooth split cast collars, radiused rim and a recessed pin-socket boss.
    before=set(bpy.context.scene.objects)
    section=[(.0639,-.025),(.070,-.028),(.074,-.018),(.074,.018),(.0639,.025)]
    for side in (0,1):
        angles=[side*math.pi+.009+i*(math.pi-.018)/8 for i in range(9)]
        loops=[[(x+r*math.cos(t),y+r*math.sin(t),z+h) for r,h in section] for t in angles]
        own(G.smooth(G.loft('Radiused split cast collar',loops,M['Frame'],caps=True),55),parent)
    lathe(parent,'Open counterbored cast mounting boss',[(y-.130,.013),(y-.130,.022),(y-.123,.027),(y-.063,.029),(y-.063,.0048)],s=8,axis='Y',center=(x,z),closed=True)
    own(G.smooth(G.cylinder('Socket cap / pin drive',(x,y-.122,z),(x,y-.129,z),.008,M['Frame'],8),65),parent,'zinc')
    cyl(parent,'M10 minor-diameter shank into casting',(x,y-.122,z),(x,y-.061,z),.0045,'zinc',4)
    if yaw:
        rot=Matrix.Rotation(math.radians(yaw),4,'Z');center=Vector((x,y,z))
        for o in set(bpy.context.scene.objects)-before:
            if o.type=='MESH':
                transform=Matrix.Translation(center)@rot@Matrix.Translation(-center)@o.matrix_basis
                o.data.transform(transform);o.matrix_basis=Matrix.Identity(4);o.data.update()
    extent=max((o.matrix_basis@v.co-Vector((x,y,z))).length for o in set(bpy.context.scene.objects)-before if o.type=='MESH' for v in o.data.vertices)
    assert extent<.17,('Displaced collar component',extent)
    parent['measured_source_clamp_max_radius_m']=max(float(parent.get('measured_source_clamp_max_radius_m',0)),extent)


def join_owner(owner):
    obs=[o for o in owner.children if o.type=='MESH']
    if not obs:return
    bpy.ops.object.select_all(action='DESELECT')
    for o in obs:o.select_set(True)
    bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();o=obs[0];o.name=owner.name+'_Mesh'
    G.apply(o);o.data.transform(o.matrix_basis);o.matrix_basis=Matrix.Identity(4)
    m=o.modifiers.new('Game triangles','TRIANGULATE');G.apply(o)

def finish(rt):
    owners=[o for o in [rt,*list(rt.children_recursive)] if o.type=='EMPTY']
    for o in owners:join_owner(o)
    bpy.context.view_layer.update()
    pts=[rt.matrix_world.inverted()@o.matrix_world@v.co for o in rt.children_recursive if o.type=='MESH' for v in o.data.vertices]
    count=0
    for o in rt.children_recursive:
        if o.type=='MESH':o.data.calc_loop_triangles();count+=len(o.data.loop_triangles)
    return dict(triangles=count,bounds_m=[[float(f(p[k] for p in pts)) for k in range(3)] for f in (min,max)],pivots=[dict(name=o.name,axis=o['pivot_axis'],range_degrees=list(o['range_degrees']),position=list(o.location)) for o in rt.children_recursive if 'pivot_axis' in o],sockets=[dict(name=o.name,kind=o['socket_kind'],position=list(o.location)) for o in rt.children_recursive if 'socket_kind' in o and 'pivot_axis' not in o])

def clone(source,name,pos=(0,0,0),yaw=0,tint=None):
    obs=[source,*source.children_recursive];cp={o:o.copy() for o in obs}
    for a,b in cp.items():bpy.context.collection.objects.link(b);b.name=name if a==source else name+'__'+a.name;b.parent=cp.get(a.parent);b.matrix_basis=a.matrix_basis.copy()
    rt=cp[source];rt.location=pos;rt.rotation_euler.z=math.radians(yaw)
    if tint:
        from finishes import placed
        for o in cp.values():
            if o.type=='MESH':o.data=o.data.copy();placed(o,tint)
    return rt
