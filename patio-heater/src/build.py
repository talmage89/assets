"""Scripted steel mushroom heater; never reads the optional owner's cylinder."""
import argparse,math,json,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import model as G
from kit.materials import surface,print_material
from settings import *
from finishes import paint,thermal,perforated,hardware,latch_handle

class Build:
    # Match macro radial stations across high/game: a .9 mm reflector shell
    # cannot tolerate a cage larger than its gauge. Source-only screw drives,
    # bevels, print, vents and shader relief still transfer to game normals.
    def __init__(self,high,wear):
        self.high=high;self.wear=wear;self.n=64
        self.root=G.pivot('HeaterBody',(0,0,0));self.root['static_root']=True
        self.steel=surface('Drawn brushed stainless','stainless',wear,grime=.08,dust=.03,roughness=.33)
        self.hardware=hardware(wear);self.latch=latch_handle(wear)
        self.paint=paint(wear);self.rubber=surface('EPDM and molded polymer','rubber',wear,dust=.08)
        self.black=surface('Control ABS','plastic',wear,zones=[dict(center=(0,0),radii=(.03,.03))])
        self.brass=surface('Machined brass LPG fitting','brass',wear)
    def add(self,ob,parent=None):return G.attach(ob,parent or self.root,asset_set='Heater')
    def box(self,name,p,s,mat=None,parent=None,r=.001):
        return self.add(G.box(name,p,s,mat or self.steel,r,3 if self.high else 1),parent)
    def lathe(self,name,pts,mat=None,seg=None,axis='Z',center=(0,0),parent=None,closed=False):
        return self.add(G.lathe(name,pts,mat or self.steel,max(6,round((seg or self.n)*.5)),axis,center,closed),parent)
    def rod(self,name,a,b,r,mat=None,sides=12,parent=None):
        return self.add(G.cylinder(name,a,b,r,mat or self.steel,max(6,round(sides*.65))),parent)
    def bolt(self,name,p,d=(0,0,1),r=.004,parent=None):
        for ob in G.fastener(name,p,d,self.hardware,r,self.high,kind='cross'):self.add(ob,parent)
    def shell(self,name,profile,start,end,mat=None,parent=None,steps=None):
        # Closed, gauged cross section swept over an arc, with capped radial ends.
        steps=steps or max(8,round(self.n*(end-start)/360))
        steps=max(4,round(steps*.75))
        loops=[[(r*math.cos(math.radians(a)),r*math.sin(math.radians(a)),z) for z,r in profile]
               for a in [start+(end-start)*i/steps for i in range(steps+1)]]
        return self.add(G.smooth(G.loft(name,loops,mat or self.steel)),parent)

def cabinet(b):
    b.lathe('Stamped weighted base pan',[(0,0),(0,.218),(.005,BASE_RADIUS),(.013,BASE_RADIUS),(.025,.223),(.058,.198),(.061,.19),(.061,0)],b.paint)
    b.lathe('Tank support floor',[(.060,0),(.060,.19),(.064,.19),(.064,0)],b.paint,64)
    # Three skids contact the canonical foot ring without enclosing it.
    for i in range(3):
        t=math.radians(30+120*i);x,y=.124*math.cos(t),.124*math.sin(t)
        b.box('Tank foot ring stop '+str(i),(x,y,.071),(.018,.018,.014),b.rubber,r=.002)
    b.shell('Rolled cabinet body',[(.082,.2032),(.777,.2032),(.777,.2017),(.082,.2017)],-29,209,b.paint)
    # Narrow rear closure avoids the cyclic seam of the arc primitive.
    b.shell('Cabinet rear closing seam',[(.082,.2033),(.777,.2033),(.777,.2016),(.082,.2016)],208,211,b.paint,steps=2)
    b.lathe('Housing lower rolled hem',[(.076,.199),(.076,.205),(.082,.206),(.087,.203),(.087,.199)],b.paint,closed=True)
    b.lathe('Housing shoulder pressed cap',[(.777,.201),(.777,.204),(.788,.204),(.803,.194),(.816,.18),(.826,.047),(.833,.041),(.833,.0385),(.828,.0385),(.820,.046),(.812,.179),(.799,.191),(.786,.200)],b.paint,closed=True)
    # Internal load path carries the post behind/above the tank, never through it.
    for i,t in enumerate((0,90,180)):
        a=math.radians(t);x,y=.180*math.cos(a),.180*math.sin(a)
        b.rod('Internal stanchion '+str(i),(x,y,.064),(x,y,.70),.008,b.steel,8)
        b.add(G.tube('Post support spider '+str(i),[(x,y,.69),(x*.58,y*.58,.765),(x*.2,y*.2,.814)],.008,b.steel,8))
        b.bolt('Spider base fastener '+str(i),(x,y,.065))
    door=G.pivot('TankDoor',DOOR_HINGE,'Z',DOOR_RANGE);door.parent=b.root
    doorpaint=paint(b.wear,True)
    b.shell('Curved tank door',[(.093,.2057),(.774,.2057),(.774,.2042),(.093,.2042)],-149,-31,doorpaint,door)
    # Return folds stiffen the long free edges; real 1.5 mm sheet, no solid slab.
    for a in (-148.5,-31.5):
        rad=math.radians(a);r=.198
        ob=G.box('Door vertical return', (r*math.cos(rad),r*math.sin(rad),.4345),(.013,.0015,.655),doorpaint,.0005,1)
        ob.rotation_euler.z=rad;b.add(ob,door)
    for z in (.110,.758):b.shell('Door folded edge',[(z,.2057),(z,.193),(z+.0015,.193),(z+.0015,.2057)],-148,-32,doorpaint,door)
    hx,hy,_=DOOR_HINGE
    for z in (.190,.660):
        
        for dz in (-.018,.018):
            b.add(G.tube('Fixed hinge strap',[(hx,hy,z+dz),(hx-.003,hy+.019,z+dz),(hx+.007,hy+.024,z+dz)],.002,b.steel,8))
        b.box('Door hinge leaf',(hx+.014,hy-.004,z),(.030,.004,.014),b.steel,door,r=.0008)
        b.rod('Fixed hinge pin',(hx,hy,z-.027),(hx,hy,z+.027),.0025,b.steel,12)
        for dz,pa in [(-.018,None),(0,door),(.018,None)]:
            b.lathe('Door hinge sleeve' if pa else 'Fixed hinge sleeve',[(z+dz-.007,.0028),(z+dz-.007,.005),(z+dz+.007,.005),(z+dz+.007,.0028)],b.steel,16,center=(hx,hy),parent=pa,closed=True)
    # Quarter-turn latch plate tangent to the curved door.
    t=math.radians(-40);x,y=.208*math.cos(t),.208*math.sin(t)
    a=(x,y,.435);q=(x*1.07,y*1.07,.435)
    b.rod('Door latch bezel',a,q,.012,b.steel,24,door)
    handle=b.box('Door latch wing',(x*1.09,y*1.09,.435),(.031,.008,.009),b.latch,door,r=.002)
    # Long axes tangent to cabinet.
    # Three actual vertical drain bores through floor and ballast pan.
    for i,(x,y) in enumerate(((-.13,-.13),(0,-.185),(.13,-.13))):
        for name in ('Tank support floor','Stamped weighted base pan'):
            ob=bpy.data.objects[name]
            G.boolean(ob,G.cylinder('Drain cutter',(x,y,-.001),(x,y,.067),.003,b.steel,12 if b.high else 8))
            bm=bmesh.new();bm.from_mesh(ob.data)
            bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
            bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
            bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    # Small slotted high-source ventilation recesses transfer to normal/colour.
    # Physical air enters below the open shell hem and through its door margins.
    for row,z in enumerate((.705,.719,.733)):
        for i in range(18):
            t=math.radians(-142+i*6);r=.206
            if b.high:
                vent=G.box('Baked door vent %d %d'%(row,i),(r*math.cos(t),r*math.sin(t),z),(.009,.0006,.0028),b.black,.001,2)
                vent.rotation_euler.z=t+math.pi/2;b.add(vent,door)
    # Badge is a source print over solid backing; no separate delivery texture.
    b.box('Maker badge backing',(0,-.207,.580),(.115,.002,.043),b.black,door,r=.003)
    m=print_material('Original evening badge',str(Path('build/markings/badge.png').resolve()),base=b.black)
    b.add(G.plane_uv('Maker badge print',[(-.056,-.2082,.559),(.056,-.2082,.559),(.056,-.2082,.601),(-.056,-.2082,.601)],m),door)
    # Tilt transport wheels are independent real pivots, stationary above grade.
    for sign in (-1,1):
        x=sign*.173;z=.059;y=.194
        b.box('Wheel mounting ear',(x,y-.020,.063),(.003,.110,.065),b.paint,r=.001)
        b.rod('Wheel axle',(x-sign*.008,y,z),(x+sign*.037,y,z),.004,b.steel,12)
        wheel=G.pivot('TransportWheel_'+('L' if sign<0 else 'R'),(x+sign*.021,y,z),'X',(0,360));wheel.parent=b.root
        b.lathe('Transport wheel tire',[(x+sign*.009,0),(x+sign*.009,.034),(x+sign*.014,.041),(x+sign*.031,.041),(x+sign*.035,.034),(x+sign*.035,0)],b.rubber,24,'X',(y,z),wheel)
        b.rod('Wheel molded hub',(x+sign*.008,y,z),(x+sign*.037,y,z),.014,b.black,16,wheel)
    tank=G.pivot('tank_socket',TANK_ORIGIN);tank.parent=b.root;tank['socket_kind']='owner_20lb_cylinder';tank['orientation']='identity; +Z up, valve -Y'

def fuel(b):
    # Canonical valve face is relative to tank foot bottom. All fuel parts are ours.
    face=Vector(TANK_ORIGIN)+Vector(VALVE_FACE)
    reg=G.pivot('regulator_attach',face);reg.parent=b.root;reg['socket_kind']='tank_valve_mating_face'
    b.lathe('Type 1 black handwheel',[(-.042,.012),(-.048,.023),(-.074,.023),(-.078,.017)],b.black,24,'Y',(0,face.z),closed=True)
    b.rod('Regulator brass nipple',(0,-.073,face.z),(0,-.092,face.z),.009,b.brass,12)
    b.lathe('Zinc diaphragm regulator',[(-.089,0),(-.089,.026),(-.095,.032),(-.108,.032),(-.114,.020),(-.114,0)],surface('Regulator diecast zinc','cast_aluminum',b.wear),32,'Y',(0,face.z))
    b.rod('Regulator hose barb',(0,-.103,face.z+.012),(.035,-.103,face.z+.012),.006,b.brass,12)
    points=G.bezier((.035,-.103,face.z+.012),(.125,-.11,.54),(.135,-.08,.66),(0,0,.705),20)
    b.add(G.tube('Static LPG hose',points,.0052,b.rubber,10))
    b.root['hose_path_m']=sum((list(p) for p in points),[])
    b.rod('Gas feed inside post',(0,0,.705),(0,0,1.783),.0052,b.rubber,8)

def upper(b):
    b.lathe('Pole lower flange',[(.818,.0378),(.818,.061),(.822,.062),(.828,.061),(.828,.0378)],b.steel,64,closed=True)
    b.lathe('Hollow 3 inch post',[(.824,.0381),(1.637,.0381),(1.637,.0369),(.824,.0369)],b.steel,64,closed=True)
    for t in (30,150,270):
        a=math.radians(t);b.bolt('Pole flange bolt',(.052*math.cos(a),.052*math.sin(a),.829))
    b.lathe('Post upper socket',[(1.624,.0385),(1.624,.045),(1.644,.045),(1.644,.0385)],b.steel,48,closed=True)
    b.lathe('Control sleeve',[(1.642,.043),(1.816,.043),(1.816,.0415),(1.642,.0415)],b.steel,48,closed=True)
    b.box('Folded control panel',(0,-.046,1.727),(.073,.012,.177),b.steel,r=.003)
    b.box('Control graphic backing',(0,-.0524,1.731),(.064,.001,.160),b.steel,r=.001)
    m=print_material('Original control legends',str(Path('build/markings/controls.png').resolve()),base=b.steel)
    b.add(G.plane_uv('Control legends print',[(-.032,-.0531,1.651),(.032,-.0531,1.651),(.032,-.0531,1.811),(-.032,-.0531,1.811)],m))
    knob=G.pivot('ControlKnob',KNOB_CENTER,'Y',(-135,0));knob.parent=b.root
    b.rod('Knob valve spindle',(0,-.047,1.757),(0,-.063,1.757),.003,b.brass,12)
    b.lathe('Knob molded grip',[(-.057,.0034),(-.057,.016),(-.064,.020),(-.077,.020),(-.080,.017),(-.080,0),(-.076,0),(-.076,.0034)],b.black,48,'Y',(0,1.757),knob,closed=True)
    b.box('Knob indicator',(0,-.0804,1.768),(.002,.0008,.008),b.steel,knob,r=.0003)
    b.rod('Piezo bezel',(0,-.0532,1.691),(0,-.060,1.691),.010,b.steel,24)
    red=surface('Piezo red molded cap','plastic',b.wear,color=(.24,.016,.009),roughness=.35)
    b.rod('Piezo push button',(0,-.058,1.691),(0,-.066,1.691),.0075,red,24)
    for x in (-.028,.028):
        for z in (1.648,1.812):b.bolt('Control panel screw',(x,-.052,z),(0,-1,0),.0025)
    b.lathe('Burner air mixing bowl',[(1.815,.043),(1.820,.054),(1.850,.108),(1.864,.134),(1.878,.139),(1.880,.137),(1.864,.132),(1.852,.105),(1.822,.052),(1.818,.043)],b.steel,64,closed=True)
    hot=thermal('Heat tinted emitter collars',b.wear,'emitter')
    for z in (1.877,2.116):
        b.lathe('Rolled emitter retaining band',[(z,.131),(z,.139),(z+.012,.139),(z+.015,.136),(z+.015,.131)],hot,64,closed=True)
    b.lathe('Emitter perforated screen',[(1.892,.132),(2.116,.132),(2.116,.1312),(1.892,.1312)],perforated(b.wear),96,closed=True)
    # Single folded back overlap seam, shallow beads, external spaced guard rods.
    b.box('Emitter back seam',(0,.133,2.004),(.007,.002,.222),hot,r=.0006)
    for z in (1.902,2.104):
        b.lathe('Emitter rolled circumferential bead',[(z,.133),(z+.001,.134),(z+.003,.134),(z+.004,.133)],hot,96,closed=True)
    for i in range(8):
        a=math.tau*i/8;x,y=.144*math.cos(a),.144*math.sin(a)
        b.rod('Burner guard upright '+str(i),(x,y,1.881),(x,y,2.132),.0018,b.steel,8)
    for i in range(8):
        a=math.tau*i/8
        for j,z in enumerate((1.886,2.131)):
            b.rod('Guard radial mount %d %d'%(j,i),(.136*math.cos(a),.136*math.sin(a),z),(.144*math.cos(a),.144*math.sin(a),z),.002,b.steel,6)
    for z in (1.886,2.131):
        b.lathe('Burner guard hoop',[(z-.0018,.144),(z,.1458),(z+.0018,.144),(z,.1422)],b.steel,96,closed=True)
    b.lathe('Burner top closure',[(2.126,0),(2.126,.138),(2.131,.138),(2.137,.126),(2.137,0)],hot,64)
    # Three 50 mm studs stand off the hood from the top closure.
    for i in range(3):
        a=math.radians(30+120*i);x,y=.106*math.cos(a),.106*math.sin(a)
        b.rod('Reflector support stud '+str(i),(x,y,2.133),(x,y,2.258),.003,b.steel,12)
        b.bolt('Reflector support nut '+str(i),(x,y,2.2568),r=.005)
        b.lathe('Reflector stand off washer '+str(i),[(2.2544,.0032),(2.2544,.008),(2.2568,.008),(2.2568,.0032)],b.steel,16,center=(x,y),closed=True)
    hood=thermal('Spun aluminum heat spread / underside tint',b.wear,'hood')
    # Three pressed petals; lapped radial seams and central crown cap, .9 mm gauge.
    outer=[(2.169,.417),(2.172,.4191),(2.177,.417),(2.179,.410),(2.204,.295),(2.233,.170),(2.237,.148)]
    section=outer+[(z-.0009,r) for z,r in reversed(outer)]
    for i in range(3):
        b.shell('Reflector aluminum petal '+str(i),section,-30+i*120,90+i*120,hood,steps=32)
        a=math.radians(-30+i*120)
        pts=[(r*math.cos(a),r*math.sin(a),z+.0006) for z,r in reversed(outer[:-1])]
        b.add(G.tube('Lapped reflector seam '+str(i),pts,.0011,hood,6))
        for r,z in ((.395,2.183),(.185,2.230)):
            b.bolt('Petal joining screw',(r*math.cos(a),r*math.sin(a),z),r=.0032)
    b.lathe('Reflector shallow crown cap',[(2.233,.155),(2.239,.155),(2.248,.140),(2.254,.120),(2.257,.035),(2.257,0),(2.2561,0),(2.2531,.12),(2.2471,.14),(2.2381,.1541),(2.233,.1541)],hood,96,closed=True)
    for i in range(3):
        a=math.radians(30+120*i);r=.139
        b.bolt('Crown screw',(r*math.cos(a),r*math.sin(a),2.2483),r=.003)

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--wear',type=float,default=.35);p.add_argument('--quality',choices=['high','game'],default='high');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True);b=Build(a.quality=='high',a.wear)
    cabinet(b);fuel(b);upper(b)
    asset=G.pivot('PatioHeater',(0,0,0));b.root.parent=asset
    sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc['quality']=a.quality;sc['asset']='PatioHeater';sc['wear']=a.wear;sc['seed']=89
    bpy.context.view_layer.update();bpy.ops.file.pack_all();Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
if __name__=='__main__':main()
