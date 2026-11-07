"""Garden construction vocabulary; original geometry in metres, +Z up."""
import math
import bpy
from mathutils import Vector, Matrix
from kit import model as G

M = {}


def palette():
    colors = dict(Wood=(.22,.175,.125), OldWood=(.19,.185,.16), EndWood=(.27,.235,.17),
                  Soil=(.043,.030,.018), WetSoil=(.022,.017,.011), Straw=(.34,.25,.10),
                  Chip=(.17,.105,.047), Gravel=(.22,.215,.19), Cloth=(.021,.024,.022),
                  Block=(.29,.285,.255), Zinc=(.32,.35,.36), Steel=(.075,.08,.073),
                  Brass=(.27,.16,.045), Hose=(.018,.060,.026), Red=(.32,.025,.012),
                  Green=(.045,.095,.045), Blue=(.025,.07,.13), White=(.62,.60,.52),
                  Roof=(.045,.048,.042), Stem=(.065,.15,.024), Fruit=(.42,.026,.008),
                  Unripe=(.13,.21,.018), Yellow=(.65,.36,.018), Flower=(.48,.13,.012),
                  Lawn=(.055,.09,.025), Bark=(.095,.075,.049), Glass=(.14,.20,.22))
    for name,color in colors.items():
        ma=bpy.data.materials.new('Garden_Form_'+name);ma.use_nodes=True
        bs=ma.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1)
        bs.inputs['Roughness'].default_value=.42 if name in ('Zinc','Brass','Fruit') else .82
        bs.inputs['Metallic'].default_value=.8 if name in ('Zinc','Brass','Steel') else 0
        bs.inputs['Specular IOR Level'].default_value=.24
        ma.diffuse_color=(*color,1);ma['checkpoint']=True;M[name]=ma


def root(name,kind='piece',parent=None):
    o=G.pivot(name,(0,0,0));o.parent=parent;o['kind']=kind;o['stage']='form checkpoint'
    return o


def own(o,rt,mat=None):
    o.parent=rt
    if o.modifiers:G.apply(o)
    if mat:
        o.data.materials.clear();o.data.materials.append(M[mat])
    if o.type=='MESH' and not o.data.uv_layers:
        uv=o.data.uv_layers.new(name='UVMap')
        for f in o.data.polygons:
            axes=sorted(range(3),key=lambda i:abs(f.normal[i]))[:2]
            for li in f.loop_indices:
                p=o.matrix_basis@o.data.vertices[o.data.loops[li].vertex_index].co
                uv.data[li].uv=(p[axes[0]],p[axes[1]])
    return o


def box(n,p,s,rt,mat='Wood',r=0):
    return own(G.box(n,p,s,M[mat],r,1),rt)


def cyl(n,a,b,r,rt,mat='Zinc',s=8):
    return own(G.smooth(G.cylinder(n,a,b,r,M[mat],s),60),rt)


def tube(n,pts,r,rt,mat='Zinc',s=6):
    return own(G.smooth(G.tube(n,pts,r,M[mat],s),60),rt)


def beam(n,a,b,w,rt,mat='Wood',d=None):
    a,b=Vector(a),Vector(b);ob=box(n,(a+b)/2,(w,d or w,(b-a).length),rt,mat)
    ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return ob


def mesh(n,v,f,rt,mat='Soil',upward=False):
    ob=G.mesh(n,v,f,M[mat])
    # The shared closed-solid normal recalculation cannot infer the outside
    # of an isolated ground/fabric patch. Its physical upper side is explicit.
    if upward:
        for face in ob.data.polygons:
            if face.normal.z<0:face.flip()
        ob.data.update()
    return own(ob,rt)


def sphere(n,p,r,rt,mat='Fruit',scale=(1,1,1),segments=10,rings=6):
    loops=[]
    # Tiny end rings avoid zero-area pole triangles.
    for j in range(rings+1):
        a=.008+(math.pi-.016)*j/rings
        loops.append([(p[0]+r*scale[0]*math.sin(a)*math.cos(k*math.tau/segments),
                       p[1]+r*scale[1]*math.sin(a)*math.sin(k*math.tau/segments),
                       p[2]+r*scale[2]*math.cos(a)) for k in range(segments)])
    return own(G.smooth(G.loft(n,loops,M[mat]),75),rt)


def ring(n,z,r,rt,mat='Zinc',wire=.0025,center=(0,0),segments=24):
    return tube(n,[(center[0]+r*math.cos(k*math.tau/segments),center[1]+r*math.sin(k*math.tau/segments),z) for k in range(segments+1)],wire,rt,mat,4)


def join(rt):
    """Consolidate immediate fixed children, preserving physical moving roots."""
    obs=[o for o in rt.children if o.type=='MESH']
    if not obs:return
    for o in obs:
        if o.data.users>1:o.data=o.data.copy()
        attr=o.data.attributes.new('GardenNormal','FLOAT_VECTOR','CORNER')
        xf=o.matrix_basis.to_3x3().inverted().transposed()
        for row,n in zip(attr.data,o.data.corner_normals):row.vector=(xf@n.vector).normalized()
    bpy.ops.object.select_all(action='DESELECT')
    for o in obs:o.select_set(True)
    bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();o=obs[0];o.name=rt.name+'__Mesh'
    o.data.transform(o.matrix_basis);o.matrix_basis=Matrix.Identity(4)
    tr=o.modifiers.new('Export triangles','TRIANGULATE');tr.keep_custom_normals=True;G.apply(o)
    a=o.data.attributes.get('GardenNormal')
    if a:o.data.normals_split_custom_set([r.vector[:] for r in a.data]);o.data.attributes.remove(a)
    # Deduplicate slots after joining many timbers or botanical axes.
    mats=[];mapping={}
    for i,ma in enumerate(o.data.materials):
        if ma not in mats:mats.append(ma)
        mapping[i]=mats.index(ma)
    ids=[mapping[f.material_index] for f in o.data.polygons]
    o.data.materials.clear()
    for ma in mats:o.data.materials.append(ma)
    for f,i in zip(o.data.polygons,ids):f.material_index=i
    return o


def instance(src,n,loc=(0,0,0),yaw=0,parent=None):
    copies={o:o.copy() for o in [src,*src.children_recursive]}
    for o,c in copies.items():
        bpy.context.collection.objects.link(c);c.parent=copies.get(o.parent,parent);c.matrix_basis=o.matrix_basis.copy()
    rt=copies[src];rt.name=n;rt.location=loc;rt.rotation_mode='XYZ';rt.rotation_euler=(0,0,math.radians(yaw))
    return rt


def count(rt):
    total=0
    for o in [rt,*rt.children_recursive]:
        if o.type=='MESH':o.data.calc_loop_triangles();total+=len(o.data.loop_triangles)
    return total


def socket(rt,name,p,kind='gardener'):
    o=root(name,'socket',rt);o.location=p;o['socket_kind']=kind
    return o


def text(rt,body,p,size=.08,mat='White',rotation=(math.pi/2,0,0)):
    from kit.fonts import find_font
    font=bpy.data.fonts.get('Garden font')
    if font is None:font=bpy.data.fonts.load(find_font('Noto Sans'));font.name='Garden font'
    cu=bpy.data.curves.new('Fictional marking','FONT');cu.body=body;cu.font=font;cu.size=size;cu.align_x='CENTER';cu.resolution_u=2
    ob=bpy.data.objects.new('Fictional '+body,cu);bpy.context.collection.objects.link(ob);ob.location=p;ob.rotation_euler=rotation
    bpy.context.view_layer.objects.active=ob;ob.select_set(True);bpy.ops.object.convert(target='MESH');ob=bpy.context.object;ob.select_set(False)
    return own(ob,rt,mat)
