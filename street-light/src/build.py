"""Original municipal cobra head, reflector cells, six-foot arm and anchored steel pole."""
import sys,math
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import model as G,materials as M
from kit.prop import Build,arguments
import dimensions as D

def finish(wear,kind):
    n=M.Nodes(kind);c=M.common(n);p=c['position'];x,y,z=n.split(p);grain=n.noise(p,420,3)
    if kind=='Concrete':
        col=n.mix(grain,(.20,.215,.195),(.30,.31,.285),True)
        dirt=n.mul(wear,n.ramp(z,.08,.005),n.noise(p,65,3),.35)
        return n.finish(n.mix(dirt,col,(.075,.061,.038),True),.92,0,n.mul(grain,.0004))
    if kind=='Zinc galvanized steel':
        spangle=n.node('ShaderNodeTexVoronoi');n.feed(spangle.inputs['Vector'],p);spangle.inputs['Scale'].default_value=420
        col=n.mix(spangle.outputs['Color'],(.26,.285,.28),(.34,.36,.35),True)
        dirt=n.mul(wear,n.ramp(z,.45,.03),n.ramp(n.noise(p,55,3),.4,.75),.6)
        col=n.mix(dirt,col,(.09,.063,.031),True)
        return n.finish(col,n.mix(dirt,.58,.86),n.mix(dirt,1,0),n.mul(grain,6e-6))
    if kind=='Reflector aluminum':return n.finish((.78,.80,.78),.09,1,n.mul(grain,2e-6))
    if kind=='Optical glass':
        mat=n.finish((.94,.97,.95),.025,0,0);s=mat.node_tree.nodes['SURFACE'];s.inputs['Transmission Weight'].default_value=1;s.inputs['IOR'].default_value=1.5;return mat
    if kind=='LED phosphor':
        mat=n.finish((.82,.74,.54),.3,0,0);s=mat.node_tree.nodes['SURFACE'];s.inputs['Emission Color'].default_value=(.82,.74,.54,1);s.inputs['Emission Strength'].default_value=16;return mat
    if kind=='Photocell polymer':return n.finish((.015,.020,.021),.42,0,n.mul(grain,4e-6))
    # Corrosion belongs at casting edges, seams and exposed fasteners.
    chips=n.mul(wear,c['edge'],n.ramp(grain,.62,.77),.55)
    cavity=n.mul(wear,c['cavity'],n.ramp(n.noise(n.vec('MULTIPLY',p,(2,2,.15)),150,3),.4,.7),.22)
    col=n.mix(chips,(.38,.40,.38),(.15,.17,.16),True);col=n.mix(cavity,col,(.085,.074,.052),True)
    height=n.mul(grain,8e-6)
    if kind=='Driver tray casting':
        rib=n.mul(n.band(y,D.BACK-.145,.087,.008),n.band(x,0,.052,.004),n.ramp(n.math('COSINE',n.mul(x,math.tau/.0145)),.4,.85))
        height=n.add(height,n.mul(rib,.0013));col=n.mix(n.mul(rib,.10),col,(.21,.23,.22),True)
    return n.finish(col,n.mix(chips,.43,.68),n.mul(chips,.7),height)

def thread_finish(wear,cx,cy):
    n=M.Nodes('Galvanized anchor thread');c=M.common(n);x,y,z=n.split(c['position'])
    angle=n.math('ARCTAN2',n.add(y,-cy),n.add(x,-cx))
    phase=n.add(n.mul(z,math.tau/.003175),angle)
    groove=n.math('SINE',phase);height=n.mul(n.ramp(groove,-.8,-.15),-.0003)
    return n.finish((.30,.33,.32),.54,1,height)

def ring(name,center,z0,z1,r0,r1,material,count=12,hexagonal=False):
    vs=[]
    for z in [z0,z1]:
        for inside in [False,True]:
            for i in range(count):
                t=i*math.tau/count
                outer=r1*math.cos(math.pi/6)/math.cos(t%(math.pi/3)-math.pi/6) if hexagonal else r1
                r=r0 if inside else outer;vs.append((center[0]+r*math.cos(t),center[1]+r*math.sin(t),z))
    fs=[]
    for i in range(count):
        j=(i+1)%count
        fs += [(i,j,j+2*count,i+2*count),(i+count,i+3*count,j+3*count,j+count),(i,i+count,j+count,j),(i+2*count,j+2*count,j+3*count,i+3*count)]
    return G.mesh(name,vs,fs,material)

def rect_ring(name,cx,cy,zlo,zhi,w,h,iw,ih,material):
    vs=[]
    for z in [zlo,zhi]:
        for width,height in [(w,h),(iw,ih)]:
            vs += [(cx+x,cy+y,z) for x,y in [(-width/2,-height/2),(width/2,-height/2),(width/2,height/2),(-width/2,height/2)]]
    fs=[]
    for i in range(4):
        j=(i+1)%4;fs += [(i,j,j+8,i+8),(i+4,i+12,j+12,j+4),(i,i+4,j+4,j),(i+8,j+8,j+12,i+12)]
    return G.mesh(name,vs,fs,material)

def reflector(name,cx,cy,base,metal,high):
    loops=[]
    for w,h,z in [(.071,.132,base),(.022,.065,base+.025),(.022,.065,base+.0256),(.071,.132,base+.0006)]:
        loops.append([(cx+x,cy+y,z) for x,y in [(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]])
    vs=[p for loop in loops for p in loop];fs=[]
    for a in range(4):
        for i in range(4):fs.append((a*4+i,a*4+(i+1)%4,((a+1)%4)*4+(i+1)%4,((a+1)%4)*4+i))
    ob=G.mesh(name,vs,fs,metal)
    if high:G.bevel(ob,.00015,2)
    return ob

def main():
    a=arguments();b=Build('StreetLight',a.quality,a.wear)
    zinc=finish(a.wear,'Zinc galvanized steel');coat=finish(a.wear,'Cast aluminum powder coat');metal=finish(a.wear,'Reflector aluminum');glass=finish(a.wear,'Optical glass');led=finish(a.wear,'LED phosphor');black=finish(a.wear,'Photocell polymer');concrete=finish(a.wear,'Concrete')
    b.add(G.cylinder('Concrete ground plinth',(0,0,0),(0,0,D.PAD_HEIGHT),.19,concrete,64 if b.high else 24))
    plate=G.box('Anchor base plate',(0,0,D.PAD_HEIGHT+D.PLATE_THICK/2),(D.PLATE,D.PLATE,D.PLATE_THICK),zinc,.004,3 if b.high else 1)
    G.apply(plate);radius=.1143
    centers=[(radius*math.cos(t),radius*math.sin(t)) for t in [math.pi/4+i*math.pi/2 for i in range(4)]]
    for i,(x,y) in enumerate(centers):
        cut=G.cylinder('Anchor hole cutter',(x,y,.04),(x,y,.10),.015,zinc,32 if b.high else 12);G.boolean(plate,cut)
    b.add(plate)
    for i,(x,y) in enumerate(centers):
        top=D.SHAFT_BASE
        b.add(G.cylinder('Anchor rod '+str(i),(x,y,.051),(x,y,.1649),.0127,thread_finish(a.wear,x,y),24 if b.high else 8))
        b.add(ring('Anchor washer '+str(i),(x,y),top,top+.004,.0133,.025,zinc,32 if b.high else 12))
        b.add(ring('Anchor hex nut '+str(i),(x,y),top+.004,top+.026,.0133,.023,zinc,36 if b.high else 12,True))
    r0=D.SHAFT_BASE_RADIUS;r1=D.SHAFT_TOP_RADIUS
    points=[(D.SHAFT_BASE,r0),(D.SHAFT_TOP,r1)]
    if b.high:points += [(D.SHAFT_TOP,r1-.00304),(D.SHAFT_BASE,r0-.00304)]
    else:points=[(D.SHAFT_BASE,0)]+points+[(D.SHAFT_TOP,0)]
    shaft=G.lathe('Tapered steel shaft',points,zinc,64 if b.high else 24,closed=b.high)
    # Source retains the 11-gauge wall; game shaft is sealed behind closed covers.
    if b.high:
        cut=G.box('Handhole cutter',(0,-r0,.54),(.052,.09,.137),zinc,.023,5);G.boolean(shaft,cut)
    b.add(shaft)
    capz=D.SHAFT_TOP
    b.add(G.lathe('Pole cap',[(capz-.004,r1+.002),(capz+.008,r1+.002),(capz+.014,.017),(capz+.016,0)],zinc,40 if b.high else 16))
    # Curved handhole cover follows the actual taper instead of floating on a flat plane.
    width=.069;height=.171;corner=.026;straight=height/2-corner
    bends=8 if b.high else 3;columns=12 if b.high else 4
    lower=[-straight-corner*math.cos(i*math.pi/(2*bends)) for i in range(bends+1)]
    levels=lower+[0]+[-v for v in reversed(lower)];rows=len(levels);stride=columns+1;layer=rows*stride;vs=[]
    for offset in [.0016,-.0016]:
        for z in levels:
            distance=max(abs(z)-straight,0);half=width/2-corner+math.sqrt(max(0,corner*corner-distance*distance))
            for i in range(stride):
                x=half*(2*i/columns-1);zz=z+.54;r=r0+(r1-r0)*(zz-D.SHAFT_BASE)/D.SHAFT_HEIGHT
                vs.append((x,-math.sqrt(r*r-x*x)-offset,zz))
    fs=[]
    for row in range(rows-1):
        for column in range(columns):
            i=row*stride+column;q=(i,i+1,i+stride+1,i+stride)
            fs += [q,tuple(v+layer for v in reversed(q))]
    boundary=list(range(stride))+[j*stride+columns for j in range(1,rows)]+[(rows-1)*stride+i for i in range(columns-1,-1,-1)]+[j*stride for j in range(rows-2,0,-1)]
    for k,i in enumerate(boundary):
        j=boundary[(k+1)%len(boundary)];fs.append((i,i+layer,j+layer,j))
    cover=G.pivot('HandholeModule',(0,0,0));cover.parent=b.root
    b.add(G.mesh('Reinforced handhole cover',vs,fs,zinc),cover)
    for zz in [.475,.605]:
        r=r0+(r1-r0)*(zz-D.SHAFT_BASE)/D.SHAFT_HEIGHT
        for ob in b.bolt('Handhole cover screw',(0,-r-.0016,zz),(0,-1,0),zinc,.003):G.attach(ob,cover,'StreetLight')
    # PBOT's paired three-bolt flange: welded pole pad and removable arm flange.
    outline=[(-.0762,D.ARM_ROOT-.111125),(.0762,D.ARM_ROOT-.111125),(.1016,D.ARM_ROOT+.111125),(-.1016,D.ARM_ROOT+.111125)]
    b.add(G.profile('Welded pole arm pad',outline,-.046,-.029,zinc,axis='Y',radius=.002 if b.high else 0))
    b.add(G.profile('Mast arm flange',outline,-.064,-.046,zinc,axis='Y',radius=.002 if b.high else 0))
    for xx,zz in [(-.0762,D.ARM_ROOT+.080),(.0762,D.ARM_ROOT+.080),(0,D.ARM_ROOT-.0978)]:b.bolt('Arm flange bolt',(xx,-.065,zz),(0,-1,0),zinc,.010)
    # Bent taper, circular stations perpendicular to the curved centerline.
    loops=[];steps=32 if b.high else 8;sides=48 if b.high else 16;length=D.ARM_LENGTH-.064
    for t in sorted(set([j/steps for j in range(steps+1)]+[.88])):
        u=min(t/.88,1);y=-.064-length*t;z=D.ARM_ROOT+D.ARM_RISE*(2*u-u*u);r=.03015+.01985*max((.88-t)/.88,0)
        dy=-length;dz=2*D.ARM_RISE*(1-u)/.88 if t<.88 else 0;norm=math.hypot(dy,dz);ny=-dz/norm;nz=dy/norm
        loops.append([(r*math.cos(i*math.tau/sides),y+ny*r*math.sin(i*math.tau/sides),z+nz*r*math.sin(i*math.tau/sides)) for i in range(sides)])
    b.add(G.smooth(G.loft('Curved tapered mast arm',loops,zinc)))
    # Original die-casting envelope, measured against the compact fixture drawing.
    sections=[(0,.127,.095),(-.020,.139,.108),(-.18,.158,.108),(-.210,.166,.105),(-.240,.177,.092),(-.270,.182,.061),(-.285,.184,.054),(-.300,.185,.052),(-.440,.191,.052),(-.465,.189,.051),(-.481,.175,.042),(-.489,.135,.023)]
    loops=[]
    for y,w,top in sections:
        h=top-.007;cross=G.rounded_rectangle(w,h,min(.018,h*.42),6 if b.high else 3)
        loops.append([(x,D.BACK+y,D.FIXTURE_BASE+.007+h/2+z) for x,z in cross])
    housing=G.smooth(G.loft('Die-cast cobra housing',loops,coat),60)
    cutter=G.box('Optics recess cutter',(0,D.BACK-.375,D.FIXTURE_BASE+.008),(.155,.146,.056),coat,0)
    G.boolean(housing,cutter)
    bore=G.cylinder('Slipfitter bore cutter',(0,D.BACK+.01,D.ARM_END),(0,D.BACK-.125,D.ARM_END),.03035,coat,48 if b.high else 12)
    G.boolean(housing,bore);b.add(housing)
    b.add(G.box('Internal slipfitter clamp jaw',(0,D.BACK-.070,D.ARM_END-.03415),(.040,.035,.008),zinc,0))
    # Bolted lower gear tray with manufactured shallow cooling ribs.
    b.add(G.box('Driver gear tray',(0,D.BACK-.145,D.FIXTURE_BASE+.0042),(.123,.210,.006),finish(a.wear,'Driver tray casting'),.008,4 if b.high else 2))
    for j in range(7):
        yy=D.BACK-.300-j*.019
        b.add(G.box('Cast heat-sink fin',(0,yy,D.FIXTURE_BASE+.0545),(.151,.003,.010),coat,.0008 if b.high else 0,2))
    for xx in [-.037,.037]:
        b.add(reflector('Folded optical reflector',xx,D.BACK-.375,D.FIXTURE_BASE+.004,metal,b.high))
        b.add(G.box('Ceramic LED support',(xx,D.BACK-.375,D.FIXTURE_BASE+.0336),(.030,.075,.0068),coat,0))
        b.add(G.box('LED phosphor emitter',(xx,D.BACK-.375,D.FIXTURE_BASE+.0296),(.021,.064,.0012),led,0))
    b.add(G.box('Tempered optical glass',(0,D.BACK-.375,D.FIXTURE_BASE+.001),(.151,.142,.002),glass,0))
    b.add(rect_ring('Compressed optics gasket',0,D.BACK-.375,D.FIXTURE_BASE+.001,D.FIXTURE_BASE+.0072,.160,.151,.149,.140,black))
    for xx in [-.0738,.0738]:b.add(G.box('Optics retaining rail',(xx,D.BACK-.375,D.FIXTURE_BASE+.0055),(.003,.140,.003),metal,0))
    # Captive fasteners, slipfitter cheeks and control socket are original geometry.
    for xx in [-.057,.057]:
        b.bolt('Tray captive screw',(xx,D.BACK-.235,D.FIXTURE_BASE+.001),(0,0,-1),zinc,.003)
    for xx in [-.038,.038]:b.bolt('Slipfitter clamp bolt',(xx,D.BACK-.025,D.FIXTURE_BASE+.006),(0,0,-1),zinc,.004)
    b.add(G.cylinder('Photocell twist-lock base',(0,D.BACK-.135,D.FIXTURE_BASE+.104),(0,D.BACK-.135,D.FIXTURE_BASE+.114),.032,black,32 if b.high else 16))
    b.add(G.lathe('Photocell weather cap',[(D.FIXTURE_BASE+.114,.0381),(D.FIXTURE_BASE+.178,.037),(D.FIXTURE_BASE+.1839,.031)],black,40 if b.high else 16,center=(0,D.BACK-.135)))
    emitter=G.pivot('LightEmitter',(0,D.BACK-.375,D.FIXTURE_BASE-.003));emitter.parent=b.root;emitter['socket_kind']='engine_light';emitter['direction']='local -Z';emitter['suggested_lumens']=4800
    b.save(a.out,a.quality)
if __name__=='__main__':main()
