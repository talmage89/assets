"""Meadow 21: all-original measured steel-deck gas mower, meters, front -Y."""
import argparse,math,sys,random
from pathlib import Path
import bpy,bmesh
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import model as G
from kit.materials import surface,print_material
from finishes import finish
OFFSET=-.41655

class Build:
    def __init__(self,high,wear):
        self.high=high;self.wear=wear;self.n=64
        self.root=G.pivot('MowerBody',(0,0,0));self.root['static_root']=True
        self.m={k:finish(k,wear) for k in ('deck','engine','bag','tire','hub','shroud','handle','recoil','grip','bag_top')}
        self.m['steel']=surface('Zinc plated hardware','stainless',wear,roughness=.44,grime=.15)
        self.m['bail']=surface('Bail safety enamel','powder',wear,color=(.30,.047,.012),roughness=.43,zones=[dict(center=(0,.526),radii=(.22,.04),axes=(0,1))])
        self.m['yellow']=surface('Oil service yellow nylon','plastic',wear,color=(.48,.30,.024),roughness=.50)
        self.m['hot']=surface('Oxidized muffler shield','stainless',wear,roughness=.57,grime=.22)
        self.m['rope']=surface('Braided recoil cord','rubber',wear,color=(.25,.22,.15),roughness=.85)
        self.m['blade']=surface('Tempered blade steel','cast_iron',wear,roughness=.67)
    def add(self,o,parent=None):return G.attach(o,parent or self.root,asset_set='Mower')
    def box(self,n,p,s,m='steel',parent=None,r=.001):return self.add(G.box(n,p,s,self.m[m],r,3 if self.high else 1),parent)
    def rod(self,n,a,b,r,m='steel',parent=None,seg=8):return self.add(G.cylinder(n,a,b,r,self.m[m],seg),parent)
    def tube(self,n,pts,r,m='handle',parent=None,sides=10):return self.add(G.tube(n,pts,r,self.m[m],sides),parent)
    def lathe(self,n,p,m='steel',axis='Z',center=(0,0),parent=None,seg=32,closed=False):return self.add(G.lathe(n,p,self.m[m],seg,axis,center,closed),parent)
    def bolt(self,n,p,d=(0,0,1),r=.004,parent=None):
        for o in G.fastener(n,p,d,self.m['steel'],r,self.high):self.add(o,parent)
    def pivot(self,n,p,axis,ran,parent=None):
        o=G.pivot(n,p,axis,ran);bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=parent or self.root;o.matrix_world=mw;return o
    def rounded(self,n,stations,m='shroud',parent=None,cx=0,cy=0,steps=4):
        loops=[[(x+cx,y+cy,z) for x,y in G.rounded_rectangle(w,h,r,steps)] for z,w,h,r in stations]
        return self.add(G.smooth(G.loft(n,loops,self.m[m]),45),parent)
    def print(self,n,stem,corners,base='shroud',parent=None):
        if self.high:
            mat=print_material(n,str(Path('build/markings',stem+'.png').resolve()),base=self.m[base]);self.add(G.plane_uv(n,corners,mat),parent)

def deck(b):
    # 2 mm deep-drawn shell, open underside, central shaft clearance, rolled hem.
    profile=[(.184,.023),(.184,.117),(.179,.147),(.153,.207),(.145,.258),(.137,.275),(.120,.280),(.059,.280),(.054,.284),(.052,.289),(.049,.289),(.047,.285),(.050,.279),(.059,.278),(.120,.278),(.135,.273),(.143,.257),(.151,.206),(.177,.147),(.182,.117),(.182,.023)]
    ob=G.lathe('Deep drawn 2mm deck with rolled hem',profile,b.m['deck'],64,closed=True)
    # Slight longitudinal draw, not a flat circular plate.
    for v in ob.data.vertices:v.co.y*=1.10
    # Open rear discharge throat and side port, with closing mulch flap outside.
    G.boolean(ob,G.box('Rear discharge die cut',(0,.30,.113),(.295,.16,.128),b.m['deck'],0))
    G.boolean(ob,G.box('Side port die cut',(.29,-.015,.098),(.10,.17,.064),b.m['deck'],0))
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    b.add(ob)
    # Engine mounting emboss and three-bolt vertical-shaft load path.
    for i,a in enumerate((20,140,260)):
        t=math.radians(a);x,y=.098*math.cos(t),.098*math.sin(t)
        b.lathe('Engine raised mounting pad '+str(i),[(.181,0),(.181,.017),(.190,.016),(.190,0)],'deck',center=(x,y),seg=16)
        b.bolt('Engine mounting bolt '+str(i),(x,y,.206))
    b.lathe('Blade spindle adapter',[(.080,0),(.080,.018),(.194,.018),(.194,0)],'engine',seg=20)
    blade=b.box('21 inch mulching blade',(0,0,.077),(.5334,.048,.004),'blade',r=.0005)
    for s in (-1,1):
        wing=G.sheet('Blade upturned sail '+('L' if s<0 else 'R'),[(s*.018,.079),(s*.024,.081),(s*.038,.099)],.089,.0035,b.m['blade'])
        wing.location.x=s*.220;b.add(wing)
    b.bolt('Blade retaining bolt',(0,0,.073),(0,0,-1),.008)
    # Front stamped bumper / rake follows deck arc and physically meets the pan.
    b.tube('Front rolled bumper',[(-.21,-.235,.110),(-.16,-.293,.105),(0,-.321,.103),(.16,-.293,.105),(.21,-.235,.110)],.009,'handle',sides=10)
    for x in (-.15,-.075,0,.075,.15):b.box('Front grass comb tooth',(x,-.320,.084),(.018,.019,.033),'shroud',r=.003)
    # Side port blanked by detachable molded mulch cover; actual hinge and spring.
    cover=b.rounded('Closed side mulch cover',[(.065,.027,.198,.009),(.075,.039,.205,.012),(.122,.032,.196,.010),(.143,.020,.177,.008)],'shroud',cx=.287,cy=-.015)
    # Rounded() runs Z, so this is a molded outboard port cover following sidewall.
    b.rod('Side flap hinge pin',(.285,-.123,.145),(.285,.094,.145),.003,'steel')
    for y in (-.092,.062):b.rod('Side cover hinge knuckle',(.285,y-.012,.145),(.285,y+.012,.145),.006,'shroud',seg=12)
    for z in (.084,.103,.122):b.rod('Mulch cover molded rib',(.307,-.085,z),(.307,.055,z),.0018,'handle',seg=6)
    # Rear chute: open throat, folded cheeks, real bag mouth above.
    for x in (-.153,.153):
        o=G.profile('Rear discharge tunnel cheek',[(.225,.075),(.225,.155),(.34,.300),(.37,.300),(.36,.18)],x-.001,x+.001,b.m['deck'],'X');b.add(o)
    b.add(G.sheet('Rear discharge tunnel roof',[(.225,.15),(.340,.303),(.372,.306)],.306,.002,b.m['deck']))
    b.rod('Rear bag retaining cross pin',(-.201,.354,.305),(.201,.354,.305),.004,'steel')
    # Rear door rests on frame top when bag is installed, sheds grass onto bag mouth.
    b.add(G.sheet('Rear spring flap',[(.244,.195),(.274,.228),(.341,.311),(.363,.315)],.350,.003,b.m['shroud']))
    b.tube('Rear door lifting grip',[(-.050,.302,.270),(-.050,.334,.302),(.050,.334,.302),(.050,.302,.270)],.004,'handle')

def wheels(b):
    for rear,y,r in [(False,-.270,.0889),(True,.260,.1016)]:
        for s in (-1,1):
            key=('R' if rear else 'F')+('L' if s<0 else 'R');x=s*.269
            p=b.pivot('Wheel_'+key,(x,y,r),'X',(0,360))
            b.box('Wheel outrigger shelf '+key,(s*.170,y,.132),(.112,.074,.002),'deck',r=.0006)
            b.box('Wheel outrigger return '+key,(s*.219,y,.117),(.002,.074,.032),'deck',r=.0006)
            # Bore is empty: axle contact is a real cylindrical bearing, not a buried rod.
            q=[(-.023,r-.023),(-.023,r-.015),(-.019,r-.004),(-.011,r),(.011,r),(.020,r-.004),(.024,r-.015),(.024,r-.023)]
            b.lathe('Tire '+key,[(x+a,rr) for a,rr in q],'tire','X',(y,r),p,48 if b.high else 32,True)
            # Pressed/molded wheel web, recessed face, raised central boss and radial ribs.
            q=[(-.021,.0045),(-.021,.017),(-.013,.028),(-.013,r-.017),(.017,r-.017),(.017,r-.025),(.004,.030),(.021,.016),(.025,.016),(.025,.0045)]
            b.lathe('Wheel dish '+key,[(x+s*a,rr) for a,rr in q],'hub','X',(y,r),p,32 if b.high else 24,True)
            for i in range(8):
                t=math.tau*i/8;rr=(r-.010)/2
                a=(x+s*.010,y+.025*math.cos(t),r+.025*math.sin(t));d=(x+s*.017,y+(r-.023)*math.cos(t),r+(r-.023)*math.sin(t))
                b.rod('Wheel molded radial rib '+key,a,d,.004,'hub',p,6)
            b.rod('Wheel axle '+key,(s*.210,y,r),(x+s*.031,y,r),.004,'steel',seg=12)
            b.bolt('Axle nut '+key,(x+s*.026,y,r),(s,0,0),.006)
            # The high source lugs project into a matching smooth tire envelope.
            if b.high:
                for i in range(44):
                    t=i*math.tau/44
                    for side in (-1,1):
                        o=G.box('Tread lug '+key,(x+side*.010,y+(r-.0008)*math.cos(t),r+(r-.0008)*math.sin(t)),(.021,.006,.0028),b.m['tire'],.0006,1)
                        o.rotation_euler.x=t-math.pi/2;o.rotation_euler.z=side*.25;b.add(o,p)
            # Spring-steel height plate with locking sector and grasp tab, one per wheel.
            b.box('Axle height carrier '+key,(s*.216,y,r+.012),(.004,.095,.061),'steel',r=.003)
            b.rod('Height carrier pivot '+key,(s*.203,y+.028,r+.018),(s*.228,y+.028,r+.018),.007,'steel')
            b.tube('Spring height adjust lever '+key,[(s*.222,y,r),(s*.220,y+.027,r+.065),(s*.223,y+.020,r+.112)],.003,'steel',sides=6)
            b.box('Height lever grip '+key,(s*.223,y+.020,r+.110),(.013,.021,.034),'shroud',r=.004)
            for i in range(5):
                if b.high:b.box('Height index notch '+key,(s*.219,y-.027+i*.014,r+.052),(.006,.006,.006),'handle',r=.0005)

def engine(b):
    b.rounded('Cast crankcase sump',[(.190,.185,.182,.035),(.204,.210,.202,.035),(.259,.205,.198,.027),(.284,.182,.175,.023)],'engine',cy=-.023)
    if b.high:
        for x in (-.067,0,.067):b.rod('Cast sump stiffening rib',(x,-.120,.210),(x,-.120,.264),.0025,'engine',seg=6)
        b.tube('Sump parting line',[(-.084,-.113,.223),(0,-.124,.223),(.084,-.113,.223)],.0012,'engine',sides=6)
    b.lathe('Vertical cylinder barrel',[(.25,0),(.25,.078),(.36,.078),(.36,0)],'engine',center=(0,-.047),seg=32)
    # Thin fin stacks, separated air spaces; retained in game silhouette.
    for i in range(7):
        b.rounded('Engine cooling fin '+str(i),[(.267+i*.010,.225,.177,.025),(.270+i*.010,.225,.177,.025)],'engine',cy=-.025,steps=2)
    b.rounded('Pressed engine blower shroud',[(.335,.285,.278,.050),(.354,.290,.300,.055),(.411,.271,.287,.065),(.425,.227,.241,.070)],'shroud',cy=-.028)
    b.lathe('Recoil starter dome',[(.418,0),(.418,.096),(.429,.097),(.449,.082),(.459,.057),(.460,0)],'recoil',center=(0,-.052),seg=48)
    # Recessed radial intake slots are procedural relief in the high normal bake.
    b.lathe('Recoil center disk',[(.460,0),(.460,.034),(.463,.034),(.463,0)],'shroud',center=(0,-.052),seg=32)
    # Rear side tank, cap neck and ribbed cap above a fuel-wetted shoulder.
    b.rounded('Molded fuel tank',[(.300,.155,.141,.024),(.400,.160,.147,.025),(.418,.146,.128,.024)],'shroud',cx=-.078,cy=.095)
    b.lathe('Fuel filler neck',[(.414,0),(.414,.023),(.435,.023),(.435,0)],'shroud',center=(-.078,.095),seg=24)
    b.lathe('Fuel cap',[(.431,0),(.431,.029),(.436,.031),(.450,.031),(.454,.026),(.454,0)],'handle',center=(-.078,.095),seg=24)
    for i in range(12):
        if b.high:
            t=math.tau*i/12;b.rod('Fuel cap grip rib',(-.078+.031*math.cos(t),.095+.031*math.sin(t),.435),(-.078+.031*math.cos(t),.095+.031*math.sin(t),.448),.0018,'handle',seg=6)
    b.rounded('Air filter body',[(.287,.089,.156,.015),(.357,.098,.165,.020)],'shroud',cx=-.152,cy=-.095)
    b.box('Air filter removable cover',(-.200,-.095,.326),(.014,.148,.069),'shroud',r=.008)
    for y in (-.145,-.120,-.095,-.070,-.045):b.rod('Air filter rib',(-.208,y,.304),(-.208,y,.349),.0016,'handle',seg=6)
    b.bolt('Air cover captive screw',(-.209,-.095,.329),(-1,0,0),.0035)
    # Exhaust cylinder, real pressed perforated heat guard outside the head.
    b.box('Muffler body',(.146,-.066,.294),(.073,.125,.084),'engine',r=.012)
    b.box('Muffler pressed shield',(.187,-.066,.298),(.0025,.141,.096),'hot',r=.001)
    if b.high:
        for row in range(5):
            for col in range(6):
                yy=-.119+col*.021;zz=.266+row*.016
                b.rod('Muffler guard dark perforation',(.1884,yy,zz),(.1888,yy,zz),.004,'handle',seg=8)
    for yy in (-.122,-.010):b.bolt('Heat shield screw',(.189,yy,.298),(1,0,0),.003)
    b.tube('Oil dipstick fill tube',[(.080,.038,.219),(.113,.100,.283),(.113,.122,.348)],.010,'shroud',sides=12)
    b.lathe('Yellow oil dipstick cap',[(.341,0),(.341,.018),(.352,.019),(.363,.016),(.363,0)],'yellow',center=(.113,.122),seg=16)
    b.box('Oil cap finger tab',(.113,.122,.365),(.033,.009,.012),'yellow',r=.002)
    b.rod('Spark plug ceramic',(.03,-.115,.285),(.03,-.151,.292),.006,'steel')
    b.tube('Spark plug ignition boot',[(.03,-.146,.292),(.03,-.161,.295),(.055,-.158,.315),(.072,-.117,.347)],.005,'handle',sides=8)

def handle_bag(b):
    # Two lower steel tubes flatten into deck mounting brackets.
    for s in (-1,1):
        b.box('Lower handle deck bracket',(s*.225,.250,.205),(.005,.102,.105),'deck',r=.003)
        b.tube('Lower handle tube',[(s*.226,.263,.204),(s*.226,.333,.266),(s*.239,.650,.550)],.011,'handle',sides=10)
        b.bolt('Handle deck bolt',(s*.244,.279,.232),(s,0,0),.005)
    fold=b.pivot('HandleFold',(0,.650,.550),'X',(0,135))
    # Tight radiused continuous U, a real 22 mm round steel tube.
    pts=[(-.239,.650,.550),(-.239,1.130,.982),(-.235,1.160,1.008),(-.216,1.176,1.023),(.216,1.176,1.023),(.235,1.160,1.008),(.239,1.130,.982),(.239,.650,.550)]
    b.tube('Upper folding U handle',pts,.011,'handle',fold,sides=12)
    b.rod('Cushioned operator grip',(-.205,1.176,1.023),(.205,1.176,1.023),.016,'grip',fold,16)
    for s in (-1,1):
        b.rod('Fold joint bolt',(s*.225,.65,.55),(s*.269,.65,.55),.004,'steel')
        b.box('Handle fold wing knob',(s*.272,.65,.55),(.014,.049,.017),'shroud',r=.005)
        b.bolt('Fold bolt head',(s*.222,.65,.55),(-s,0,0),.006)
    # A coated 9 mm steel rod, spring-held forward of the operator grip.
    bail=b.pivot('OperatorBail',(0,1.080,.937),'X',(-64.5,0),fold)
    b.tube('Operator presence steel bail',[(-.222,1.080,.937),(-.222,1.067,.956),(-.222,1.028,1.035),(-.204,1.025,1.052),(.204,1.025,1.052),(.222,1.028,1.035),(.222,1.067,.956),(.222,1.080,.937)],.0045,'bail',bail,sides=10)
    for sign in (-1,1):
        b.rod('Bail pivot boss '+str(sign),(sign*.224,1.080,.937),(sign*.246,1.080,.937),.009,'handle',fold,12)
        b.rod('Bail pivot rivet '+str(sign),(sign*.214,1.080,.937),(sign*.250,1.080,.937),.0034,'steel',fold)
    # Sheathed brake cable follows the outside of the right handle under clips.
    upper=[(.253,1.069,.936),(.257,1.024,.894),(.257,.948,.826),(.257,.862,.748),(.257,.778,.672),(.257,.699,.601),(.257,.650,.556)]
    b.tube('Upper brake cable sheath',upper,.0028,'handle',fold,sides=8)
    lower=[(.257,.650,.556),(.254,.585,.494),(.252,.518,.434),(.249,.449,.372),(.246,.385,.316)]
    b.tube('Lower handle brake sheath',lower,.0028,'handle',sides=8)
    for i,(yy,zz) in enumerate(((.980,.855),(.819,.709))):
        b.tube('Brake cable wrap clip '+str(i),[(.225,yy,zz),(.235,yy-.008,zz+.009),(.255,yy-.008,zz+.009),(.260,yy,zz),(.254,yy+.008,zz-.009),(.234,yy+.008,zz-.009)],.0015,'handle',fold,sides=6)
    b.tube('Brake cable lower wrap clip',[(.220,.449,.372),(.228,.441,.381),(.246,.441,.381),(.250,.449,.372),(.242,.457,.363),(.224,.457,.363)],.0015,'handle',sides=6)
    # Depart below the catcher mouth, sagging away from the handle into a loop.
    points=G.bezier((.246,.385,.316),(.242,.285,.186),(.158,.148,.173),(.113,.108,.276),14)
    b.tube('Lower brake cable service loop',points,.0028,'handle',sides=8)['export_part']='ServiceSpans'
    b.box('Engine brake cable bracket',(.100,.090,.277),(.044,.062,.004),'steel',r=.0008)
    b.rod('Brake sheath ferrule',(.113,.118,.262),(.113,.108,.282),.0048,'steel')
    # Retracted recoil cord: the pull rests at the engine outlet, not across the bag.
    b.tube('Recoil starter rope',[(.064,.018,.442),(.085,.052,.452),(.088,.066,.453)],.0015,'rope',sides=6)
    b.rod('Recoil pull outlet boss',(.067,.024,.435),(.083,.052,.445),.009,'shroud')
    b.rod('Recoil pull stem',(.088,.066,.453),(.088,.078,.463),.006,'shroud')
    b.rod('Recoil T pull handle',(.055,.078,.463),(.121,.078,.463),.009,'handle',seg=12)
    # Bag mouth is supported on cross-pin by hooked 6 mm steel rods.
    for s in (-1,1):
        b.tube('Bag mouth hook',[(s*.187,.355,.287),(s*.187,.347,.313),(s*.187,.362,.322),(s*.187,.380,.315)],.003,'handle',sides=8)
    mouth=[(-.187,.367,.150),(-.187,.367,.312),(.187,.367,.312),(.187,.367,.150),(-.187,.367,.150)]
    b.tube('Bag mouth steel frame',mouth,.003,'handle',sides=8)
    # Long sloping frame rods carry a tapered 1.9 bushel-class cloth catcher.
    for s in (-1,1):b.tube('Bag top support rod',[(s*.187,.368,.312),(s*.182,.825,.630),(s*.178,.855,.610)],.003,'handle',sides=8)
    b.tube('Bag rear frame hoop',[(-.182,.825,.630),(.182,.825,.630),(.194,.854,.245),(-.194,.854,.245),(-.182,.825,.630)],.003,'handle',sides=8)
    # Fabric panels stretch at the frame and bulge between its members. Five
    # longitudinal stations and sixteen perimeter points carry the silhouette.
    stations=[(.375,.377,.153,.310,0),(.460,.414,.148,.397,.65),(.640,.438,.128,.518,1),(.790,.435,.160,.623,.75),(.855,.407,.216,.630,0)]
    section=[(-.88,0),(-.45,-.035),(0,-.055),(.45,-.035),(.88,0),(1,.10),(1.04,.38),(1.02,.68),(.96,.94),(.85,1),(.42,1),(0,1),(-.42,1),(-.85,1),(-.96,.94),(-1.02,.68),(-1.04,.38),(-1,.10)]
    loops=[]
    for j,(yy,w,lo,hi,tension) in enumerate(stations):
        loop=[]
        for i,(u,v) in enumerate(section):
            side=abs(u)>.9;h=hi-lo
            xx=u*w/2
            # Loaded side panels bulge at mid-height, pinched into the top welt.
            bulge=.012*tension*math.sin(math.pi*max(0,min(1,v))) if side else 0
            xx+=math.copysign(bulge,u) if side else 0
            zz=lo+v*h
            corner=.005*math.sin(4.1*j+9*v)*tension if side else 0
            loop.append((xx,yy+corner,zz))
        loops.append(loop)
    cloth=G.loft('Sewn grass catcher textile',loops,b.m['bag'])
    bm=bmesh.new();bm.from_mesh(cloth.data);bm.faces.ensure_lookup_table()
    front,back=bm.faces[-2],bm.faces[-1];rim=list(back.verts)
    bmesh.ops.delete(bm,geom=[front,back],context='FACES_ONLY')
    belly=bm.verts.new((0,.882,.407))
    for i,v in enumerate(rim):bm.faces.new((v,rim[(i+1)%len(rim)],belly))
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    # Explicit shared diagonals keep curved cloth projection identical in high
    # and game; implicit renderer/UV triangulations need not choose the same quad.
    bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY')
    bm.to_mesh(cloth.data);bm.free();cloth['allow_boundary']=True
    b.add(G.smooth(cloth,70))
    # Crowned 2.5 mm molded polypropylene canopy. Returned edges meet the
    # cloth welt; the carrying handle is part of this rigid top, not a wire loop.
    canopy=[]
    for yy,w,lo,hi,tension in stations:
        top=[(u*w/2,yy,hi+.003+.010*(1-u*u)) for u in (-1,-.85,0,.85,1)]
        canopy.append(top+[(x,y,z-(.011 if i in (0,4) else .0025)) for i,(x,y,z) in reversed(list(enumerate(top)))])
    cap=G.smooth(G.loft('Molded bag top canopy',canopy,b.m['bag_top']),50)
    if b.high:G.bevel(cap,.0006,2)
    b.add(cap)
    b.tube('Molded bag carrying handle',[(-.065,.566,.477),(-.065,.566,.515),(-.045,.566,.527),(.045,.566,.527),(.065,.566,.515),(.065,.566,.477)],.008,'bag_top',sides=8)
    for sign in (-1,1):
        b.box('Bag handle molded foot',(sign*.063,.566,.479),(.027,.030,.012),'bag_top',r=.003)
        # Welt/stitched seams and corner gathers are baked relief, not four
        # additional thin tube meshes consuming silhouette budget.

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--wear',type=float,default=.35);p.add_argument('--quality',choices=['high','game'],default='high');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True);b=Build(a.quality=='high',a.wear)
    deck(b);wheels(b);engine(b);handle_bag(b)
    asset=G.pivot('LawnMower',(0,0,0));b.root.parent=asset;b.root.location.y=OFFSET;b.root.location.x=-.0044
    sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc['quality']=a.quality;sc['asset']='LawnMower';sc['wear']=a.wear;sc['seed']=21
    bpy.context.view_layer.update();bpy.ops.file.pack_all();Path(a.out).parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
if __name__=='__main__':main()
