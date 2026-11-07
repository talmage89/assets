"""Native library context, terrain interfaces and reusable placement helpers."""
import math,random,json
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
import geom as Q
from plan import *
ROOT=Path(__file__).resolve().parents[2]

def load(path):
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(Path(path).resolve()))
    added=set(bpy.context.scene.objects)-before
    roots=[o for o in added if o.parent not in added]
    rt=Q.root('Template_'+Path(path).stem)
    for ob in roots:
        # Some imports add a global axis transform. Keep the world matrix.
        mat=ob.matrix_world.copy();ob.parent=rt;ob.matrix_world=mat
    return rt

def clone(src,name,loc=(0,0,0),yaw=0,parent=None):
    mapping={}
    for ob in [src,*src.children_recursive]:
        cp=ob.copy()
        if ob.type=='CURVE':cp.data=ob.data.copy()
        bpy.context.collection.objects.link(cp);mapping[ob]=cp
    for ob,cp in mapping.items():
        cp.parent=mapping.get(ob.parent,parent);cp.matrix_basis=ob.matrix_basis.copy()
    rt=mapping[src];rt.name=name;rt.location=loc;rt.rotation_euler=(0,0,math.radians(yaw));rt['placement_id']=name
    return rt

def delete(rt):
    for ob in list(rt.children_recursive)[::-1]+[rt]:bpy.data.objects.remove(ob,do_unlink=True)

def along(src,name,p,s,u,zoff=0,yaw=0,parent=None):
    point=p.xyz(s,u,zoff);a=math.degrees(math.atan2(p.frame(s)[1][0],p.frame(s)[1][1]))
    return clone(src,name,point,-a+yaw,parent)

def town(p):
    rt=Q.root('TownContext',module_kind='context');rng=random.Random(p.seed);ground=7.0 if p.kind=='diamond' else 0
    b=Q.Batch('Town native-surface streets',rt)
    # Parallel local streets and connected driveways continue out of view.
    xs=(-122.,122.) if p.kind=='diamond' else (-67.,81.)
    for x in xs:
        for side in (-1,1):
            b.surface([(x+side*3.6576,-p.length/2,ground+.007),(x,-p.length/2,ground+.083),(x,p.length/2,ground+.083),(x+side*3.6576,p.length/2,ground+.007)],'Asphalt')
            b.box((x+side*4.19,0,ground+.076),(.1524,p.length,.1524),'Concrete')
            b.surface([(x+side*6.,-p.length/2,ground+.16),(x+side*7.524,-p.length/2,ground+.175),(x+side*7.524,p.length/2,ground+.175),(x+side*6.,p.length/2,ground+.16)],'Concrete')
    house=[load('build/context/Ranch.glb'),load('build/context/Cape.glb')]
    # Different lot arrangement, orientation and side access in each seed.
    for i in range(18 if p.kind=='diamond' else 26):
        side=(-1,1)[i%2];s=((i//2)-4.5)*31 if p.kind=='diamond' else ((i//2)-6)*35+17
        if p.kind=='diamond' and abs(s)<28:continue
        u=side*(143 if p.kind=='diamond' else (90 if side>0 else 78))
        point=list(p.center(s));point[0]+=u;point[2]=ground+.16
        clone(house[i%2],'Lot_'+str(i),point,90 if side>0 else -90,rt)
        # Driveway touches the native street and the house frontage.
        roadx=xs[0 if side<0 else 1];xa,xb=sorted([roadx+side*3.66,point[0]-side*6.])
        b.surface([(xa,point[1]-1.524,ground+.03),(xb,point[1]-1.524,ground+.03),(xb,point[1]+1.524,ground+.03),(xa,point[1]+1.524,ground+.03)],'Concrete')
    for lib in house:delete(lib)
    # A modest commercial parcel fronts the arterial in the diamond.
    if p.kind=='diamond':
        gas=load('build/context/Gas.glb');clone(gas,'ArterialGasStation',(170,45,ground+.05),180,rt);delete(gas)
    # Four intact native botanical crowns; no generated replacement trees.
    tree=[load('build/context/TreeOak.glb'),load('build/context/TreeMaple.glb')]
    placements=[(-48,-62),(49,48),(-154,115),(156,-110)] if p.kind=='diamond' else [(-45,-75),(49,-120),(-48,62),(50,138)]
    for i,(x,y) in enumerate(placements[:2]):
        c=p.center(y);clone(tree[i%2],'NativeTree_'+str(i),(c[0]+x,c[1],ground),rng.uniform(0,360),rt)
    for lib in tree:delete(lib)
    utility=load('build/context/Utility.glb')
    poles=[]
    for i in range(7):
        x=130 if p.kind=='diamond' else 73;y=(i-3)*42.672
        c=p.center(y);poles.append((c[0]+x,c[1],ground));clone(utility,'JointUsePole_'+str(i),poles[-1],0,rt)
    delete(utility)
    for a,c in zip(poles,poles[1:]):
        for x,z,r in [(-.975,10.0,.005),(0,10.14,.005),(.975,10.,.005),(0,7.94,.004),(0,6.62,.0185)]:
            pts=[]
            for j in range(17):
                t=j/16;pts.append((a[0]+x+(c[0]-a[0])*t,a[1]+(c[1]-a[1])*t,a[2]+z-.65*4*t*(1-t)))
            b.tube(pts,r,'DarkSteel',4)
    b.finish();return rt

def traffic(p):
    rt=Q.root('Traffic',module_kind='traffic');templates=[load('build/context/Hatch.glb'),load('build/context/SUV.glb')];hero=load('build/context/HeroHatch.glb')
    locations=[(1,0,-26),(-1,1,32),(1,1,-80),(-1,0,88),(1,0,128),(-1,1,-134),(1,1,235),(-1,0,-238)]
    if p.kind=='soundwall':locations=[(1,1,-22),(-1,0,40),(1,0,-94),(-1,1,122),(1,1,180),(-1,0,-210),(1,0,277),(-1,1,-300)]
    for i,(side,lane,s) in enumerate(locations[:6]):
        ob=along(hero if i==0 else templates[i%2],'Traffic_'+str(i),p,s,p.lane(side,lane),.025,180 if side>0 else 0,rt)
        # Vehicle source floor is ground Z=0. Give the whole vehicle the road's
        # actual bank; wheel/plane contact is independently ray measured later.
        ob.rotation_euler.y=math.atan(p.bank if p.bank else -side*.02)
    for lib in [*templates,hero]:delete(lib)
    return rt

def terminal_signals(p):
    rt=Q.root('RampTerminalSignals',module_kind='signals');lib=load('build/context/Signal.glb')
    # Two arterial far-side mast pairs, plus a ramp-facing mast at each T.
    for side in (-1,1):
        x=side*p.terminal
        for j,(dx,y,yaw) in enumerate(((8.8,-10.0,90),(-8.8,10.,-90),(9.2,11.,0 if side>0 else 180))):
            clone(lib,'Terminal_'+str(side)+'_Mast'+str(j),(x+dx,y,7.35),yaw,rt)
    delete(lib);return rt

def row_fence(p):
    """ROW woven wire, native family convention: steel poles + alpha panel.

    A quick panel is used until the shared fence bake is available locally.
    No residential four-foot fabric is stretched into a freeway sound wall.
    """
    rt=Q.root('RightOfWayFence',module_kind='fence');b=Q.Batch('ROW posts and fabric',rt)
    for side in (-1,1):
        u=side*(106 if p.kind=='diamond' else 40.)
        for s in seq(-p.length/2,p.length/2,3.048):
            x,y,z=p.xyz(s,u);z=7.0 if p.kind=='diamond' else 0
            b.tube([(x,y,z),(x,y,z+1.83)],.024,'Steel',4)
        chain=seq(-p.length/2,p.length/2,6.096)
        for a,c in zip(chain,chain[1:]):
            x0,y0,_=p.xyz(a,u);x1,y1,_=p.xyz(c,u);z=7.0 if p.kind=='diamond' else 0
            # Original chain-link's physical 0.3048 m repeat, shared across
            # all placements. It represents manufacture, not repeated wear.
            b.face([(x0,y0,z+.06),(x1,y1,z+.06),(x1,y1,z+1.80),(x0,y0,z+1.80)],'Fence',uv=[(a/.3048,0),(c/.3048,0),(c/.3048,1.74/.3048),(a/.3048,1.74/.3048)])
        for h in (.06,1.80):
            pts=[]
            for s in seq(-p.length/2,p.length/2,12.192):
                x,y,z=p.xyz(s,u);pts.append((x,y,(7.0 if p.kind=='diamond' else 0)+h))
            b.tube(pts,.0025,'DarkSteel',3)
    b.finish();return rt

def seq(a,b,step):
    n=math.ceil((b-a)/step);return [a+(b-a)*i/n for i in range(n+1)]
