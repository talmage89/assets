"""Garden adaptation of native chain-link alpha at its true 2in clear mesh."""
import math
from mathutils import Vector
import geometry as Q
from kit import tiling

FABRIC=None
RECT=(16/1024,16/1024,272/1024,272/1024)
TILE=.3048


def material(folder):
    global FABRIC
    FABRIC=tiling.material('ChainLink',folder,alpha=True);FABRIC.use_backface_culling=False;FABRIC.alpha_threshold=.5


def fabric(rt,w,h=1.2192):
    v=[];f=[];uvs=[];nx=max(1,math.ceil(w/TILE));nz=4
    for j in range(nz):
        z0=.0508+j*TILE;z1=min(h+.0508,z0+TILE)
        for i in range(nx):
            x0=-w/2+i*TILE;x1=min(w/2,x0+TILE);start=len(v)
            for x,z in ((x0,z0),(x1,z0),(x1,z1),(x0,z1)):
                sag=.024*math.sin(math.pi*(x+w/2)/w)*(z/h)
                v.append((x,-.024,z-sag))
            f.append(tuple(start+k for k in range(4)))
            a,b,c,d=RECT;uu=a+(c-a)*(x1-x0)/TILE;vv=b+(d-b)*(z1-z0)/TILE
            uvs.extend([(a,b),(uu,b),(uu,vv),(a,vv)])
    me=Q.G.bpy.data.meshes.new('Native pitch wire fabric');me.from_pydata(v,[],f);me.update()
    ob=Q.G.bpy.data.objects.new('Sagged wire envelope',me);Q.G.bpy.context.collection.objects.link(ob);ob.parent=rt;me.materials.append(FABRIC)
    uv=me.uv_layers.new(name='UVMap')
    for lo in me.loops:uv.data[lo.index].uv=uvs[lo.vertex_index]
    return ob


def bay(w):
    rt=Q.root('FenceBay','fence');rt['post_pitch_m']=w
    Q.cyl('1-5/8in line post',(-w/2,0,0),(-w/2,0,1.30),.041275/2,rt,s=10)
    Q.sphere('Post cap',(-w/2,0,1.30),.025,rt,'Zinc',scale=(1,1,.5),segments=10,rings=3)
    Q.cyl('1-3/8in rail',(-w/2,0,1.25),(w/2,0,1.25),.034925/2,rt,s=10)
    fabric(rt,w)
    for z in (.16,.48,.81,1.12):Q.ring('Wire post tie',z,.024,rt,'Zinc',.0015,center=(-w/2,0),segments=8)
    Q.join(rt);return rt


def gate(w):
    rt=Q.root('GardenGate','gate');gap=.04;leafw=w-.10
    for x in (-w/2,w/2):Q.cyl('2-3/8in gate terminal',(x,0,0),(x,0,1.33),.060325/2,rt,s=12)
    moving=Q.root('GateLeaf','pivot',rt);moving.location=(-w/2+.05,-.035,0);moving['pivot_axis']='Z';moving['range_degrees']=[-110,0]
    # Coordinates below are local to the actual hinge axis, not leaf centre.
    for x in (.035,leafw):Q.cyl('Gate upright',(x,0,.08),(x,0,1.24),.01746,moving,s=10)
    for z in (.08,1.24):Q.cyl('Welded gate cross tube',(.035,0,z),(leafw,0,z),.01746,moving,s=10)
    temporary=Q.root('Gate fabric center');fabric(temporary,leafw-.035,1.18);Q.join(temporary)
    ob=temporary.children[0];ob.parent=moving;ob.location=(leafw/2,0,.025)
    Q.G.bpy.data.objects.remove(temporary,do_unlink=True)
    for z in (.25,1.05):
        Q.cyl('Fixed hinge pin',(-w/2+.05,-.035,z-.035),(-w/2+.05,-.035,z+.035),.005,rt,s=8)
        Q.own(Q.G.lathe('Bored rotating hinge sleeve',[(z-.028,.0055),(z-.028,.009),(z+.028,.009),(z+.028,.0055)],Q.M['Zinc'],12,closed=True),moving)
        Q.box('Sleeve to frame welded neck',(.021,0,z),(.030,.012,.022),moving,'Zinc')
        Q.box('Hinge clamp arm',(-w/2+.025,-.018,z+.039),(.05,.032,.022),rt,'Zinc')
    Q.box('Latch keeper',(leafw-.03,-.035,.82),(.09,.018,.06),moving,'Steel')
    Q.join(moving);Q.join(rt);rt['clear_opening_m']=w-.060325;return rt


def perimeter(p,parent):
    W,D=p['size'];out=[]
    def run(a,b):
        a,b=Vector(a),Vector(b);length=(b-a).length;n=math.ceil(length/3.048);w=length/n
        prototype=bay(w);yaw=math.degrees(math.atan2(b.y-a.y,b.x-a.x))
        for i in range(n):
            loc=a.lerp(b,(i+.5)/n);r=Q.instance(prototype,'PerimeterFence',loc,yaw,parent);out.append(r)
        for o in [*prototype.children_recursive,prototype]:Q.G.bpy.data.objects.remove(o,do_unlink=True)
    half=p['gate_width']/2
    run((-W/2,-D/2,0),(-half,-D/2,0));run((half,-D/2,0),(W/2,-D/2,0))
    run((W/2,-D/2,0),(W/2,D/2,0));run((W/2,D/2,0),(-W/2,D/2,0));run((-W/2,D/2,0),(-W/2,-D/2,0))
    g=gate(p['gate_width']);g.parent=parent;g.location=(0,-D/2,0);out.append(g)
    # Garden gates sit open for the checkpoint, preserving editable closed rest.
    next(o for o in g.children if o.get('pivot_axis')).rotation_euler.z=math.radians(-85)
    return out
