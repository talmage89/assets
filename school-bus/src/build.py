"""Scripted C75 bus construction. No imported model, mesh, image or trace.

The car family's panel, tire, lathes, glazing, lamp, paint and pivot methods
are reused. Only vehicle-specific body sections and truck steel wheels differ.
"""
import argparse,json,math,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path[:0]=[str(HERE),str(ROOT),str(ROOT/'cars/src')]
from kit import model as G
from kit.vehicle import panel,loaded_tire
from detail_helpers import box,tube,pivot,print_quad,loop
from kit.fonts import find_font
import spec as S
import finishes

class Bus:
    def __init__(self,seed):
        self.seed=seed;self.high=False;self.detail=True;self.info=S.SEEDS[seed]
        self.root=G.pivot('SchoolBus',(0,0,0));self.root['static_root']=True;self.root['seed']=seed
        self.root['passengers']=75;self.root['body_maker']='Morrow';self.root['model']='C75'
        self.m=finishes.build(self.info['wear']);self.images={}
        for key in ['school','emergency','maker','stop']+[f'{kind}-{sid}' for sid in S.SEEDS for kind in ['district','fleet','plate']]:
            self.images[key]=bpy.data.images.load(str(ROOT/'school-bus/build/markings'/f'{key}.png'))
            self.m[key]=finishes.printed(key,self.images[key])
    def add(self,ob,parent=None,category='shell'):
        G.attach(ob,parent or self.root,asset_set='SchoolBus');ob['part_category']=category
        return ob
    def box(self,name,c,size,mat='yellow',parent=None,category='shell',r=.003):
        return box(self,name,c,size,self.m[mat],category,parent,r)
    def tube(self,name,pts,r,mat='black',parent=None,category='shell',sides=8):
        return tube(self,name,pts,r,self.m[mat],category,parent,sides)
    def print(self,name,corners,mat,parent=None):return print_quad(self,name,corners,self.m[mat],'shell',parent)
    def frame_side(self,name,x,y,z,w,h,mat='black',parent=None,rail=.028):
        for yy in [y-w/2+rail/2,y+w/2-rail/2]:self.box(name+' upright',(x,yy,z),(.030,rail,h),mat,parent,r=.002)
        for zz in [z-h/2+rail/2,z+h/2-rail/2]:self.box(name+' horizontal',(x,y,zz),(.030,w-2*rail,rail),mat,parent,r=.002)
    def glass_side(self,name,x,y,z,w,h,parent=None):
        return self.box('Glass '+name,(x,y,z),(.0048,w,h),'glass',parent,category='glass',r=0)
    def socket(self,name,pos,kind='seat'):
        ob=G.pivot('Socket_'+name,pos);ob.parent=self.root;ob['socket_kind']=kind;return ob

def roof_section(y,frontcap=0):
    # Multi-radius formed roof: vertical side, round shoulder, mildly crowned center.
    # End caps contract longitudinally, preserving the structural eave height.
    half=S.WIDTH/2
    return [(x,y,z-frontcap) for x,z in [(-half,2.710),(-1.205,2.800),(-1.155,2.905),(-1.070,3.020),(-.950,3.110),(-.790,3.165),(-.54,3.190),(-.27,3.198),(0,S.HEIGHT),(.27,3.198),(.54,3.190),(.790,3.165),(.950,3.110),(1.070,3.020),(1.155,2.905),(1.205,2.800),(half,2.710)]]

def body(b):
    # Continuous formed roof with a finite inner skin; open front/rear boundaries seat in caps.
    sections=[(-3.92,.20),(-3.78,.085),(-3.56,.015),(-3.38,0),(5.60,0),(5.80,.025),(5.96,.075),(6.006,.115)]
    loops=[roof_section(y,d) for y,d in sections]
    ob=G.loft('Formed roof steel',loops,b.m['yellow'],caps=False,closed=False);G.smooth(ob,50)
    sol=ob.modifiers.new('Roof sheet gauge','SOLIDIFY');sol.thickness=.0012;sol.offset=-1;b.add(ob)
    # Interior headliner has independent geometry and no outside color painted into it.
    inner=[[(x*.983,y,z-.057) for x,y,z in roof_section(yy,d)] for yy,d in sections]
    ob=G.loft('Ceiling formed liner',inner,b.m['ceiling'],caps=False,closed=False);G.smooth(ob,50);b.add(ob,category='interior')
    # Floor leaves a genuine entrance stairwell. Skirt is a folded sheet with a cut arch.
    b.box('Passenger floor',(0,1.52,1.157),(2.304,8.96,.046),'floor',category='interior',r=.002)
    b.box('Driver floor',(.43,-3.36,1.157),(1.44,.88,.046),'floor',category='interior',r=.002)
    b.box('Aisle tread',(0,1.52,1.184),(.310,8.96,.008),'floor',category='interior',r=.001)
    for sign in [-1,1]:
        x=sign*(S.WIDTH/2-.012)
        spans=[(-3.92,6.006)] if sign>0 else [(-3.92,-3.75),(-2.94,6.006)]
        for j,(ya,yb) in enumerate(spans):
            # Lower edge rises around rear tire; no panel spans the wheel opening.
            profile=[(ya,1.830),(yb,1.830),(yb,.755)]
            rr=.630;cy=S.REAR_AXLE;theta=math.asin((.755-S.HUB)/rr);dx=rr*math.cos(theta)
            if ya<cy-rr and yb>cy+rr:
                profile += [(cy+rr*math.cos(t),S.HUB+rr*math.sin(t)) for t in [theta+(math.pi-2*theta)*k/32 for k in range(33)]]
            profile += [(ya,.755)]
            if sign>0:
                # Side emergency door interrupts two lower rail segments and the steel.
                ey=S.ROW_START+S.SIDE_EXIT_ROW*S.ROW_PITCH
                if ya<ey<yb:
                    # Two solid panels and a lintel around the true 610 mm opening.
                    for a,c in [(ya,ey-.335),(ey+.335,yb)]:
                        pp=[(a,1.830),(c,1.830),(c,.755)]
                        if a<cy-.630 and c>cy+.630:
                            pp += [(cy+rr*math.cos(theta+(math.pi-2*theta)*k/32),S.HUB+rr*math.sin(theta+(math.pi-2*theta)*k/32)) for k in range(33)]
                        pp += [(a,.755)]
                        b.add(G.profile(f'Lower folded side {sign} {j} {a}',pp,x-.011,x+.011,b.m['yellow'],axis='X'))
                    b.box('Side exit lintel',(x,ey,2.702),(.026,.67,.030))
                else:b.add(G.profile(f'Lower folded side {sign} {j}',profile,x-.011,x+.011,b.m['yellow'],axis='X'))
            else:b.add(G.profile(f'Lower folded side {sign} {j}',profile,x-.011,x+.011,b.m['yellow'],axis='X'))
        # Passenger greenhouse: separate sheet posts, real openings, closed sill/header.
        b.box('Window header '+str(sign),(x,1.37,2.704),(.027,9.272,.048))
        if sign>0:
            ey=S.ROW_START+S.SIDE_EXIT_ROW*S.ROW_PITCH
            for a,c in [(-3.266,ey-.335),(ey+.335,6.006)]:b.box('Window sill '+str(sign),(x,(a+c)/2,1.823),(.032,c-a,.034))
        else:b.box('Window sill '+str(sign),(x,1.37,1.823),(.032,9.272,.034))
        for i in range(S.ROWS):
            y=S.ROW_START+i*S.ROW_PITCH
            if sign>0 and i==S.SIDE_EXIT_ROW:continue
            posty=y-S.ROW_PITCH/2;postwidth=.044
            if sign>0 and i==S.SIDE_EXIT_ROW+1:posty+=.016;postwidth=.020
            b.box(f'Body post {sign} {i}',(x,posty,2.245),(.045,postwidth,.870))
            w=S.ROW_PITCH-.052
            b.frame_side(f'Passenger sash {sign} {i}',sign*1.222,y,2.251,w,.850,'black',rail=.024)
            b.frame_side(f'Aluminum sash {sign} {i}',sign*1.224,y,2.253,w-.036,.814,'aluminum',rail=.014)
            b.box(f'Split sash meeting rail {sign} {i}',(sign*1.234,y,2.245),(.020,w-.040,.031),'aluminum',r=.002)
            for level,z in [('lower',2.040),('upper',2.456)]:
                b.glass_side(f'sash {sign} {i} {level}',sign*1.217,y,z,w-.068,.377)
            # Sash latches on actual middle rail; interior side.
            for d in [-.19,.19]:b.box(f'Sash latch {sign} {i} {d}',(sign*1.198,y+d,2.251),(.014,.043,.022),'black',r=.002)
        b.box('Last corner post '+str(sign),(x,5.94,2.250),(.046,.132,.900))
        b.box('Rear quarter window closure '+str(sign),(x,5.725,2.248),(.032,.555,.870))
        b.box('Forward window bay closure '+str(sign),(x,-2.827,2.248),(.032,.161,.870))
        # Vertical driver/door header regions fill the space ahead of passenger bays.
        if sign>0:
            b.box('Driver lower side',(x,-3.45,1.490),(.032,.92,.680))
            b.frame_side('Driver window frame',sign*1.219,-3.36,2.245,.92,.850,rail=.045)
            b.glass_side('driver',sign*1.211,-3.36,2.245,.83,.755)
            b.box('Driver slider join',(sign*1.224,-3.36,2.245),(.024,.023,.78),'aluminum')
        # Real pressed rub rails, hat section, broken around entrance/side exit and wheel arch.
        for ri,z in enumerate([.795,1.222,1.624,1.778]):
            intervals=[(-3.89,5.94)] if sign>0 else [(-2.90,5.94)]
            if sign>0:
                ey=S.ROW_START+S.SIDE_EXIT_ROW*S.ROW_PITCH
                intervals=[(-3.89,ey-.352),(ey+.352,5.94)]
            if z<1.25:
                rr=math.sqrt(max(0,.645**2-(z-S.HUB)**2)) if z-S.HUB<.645 else 0
                if rr:
                    cut=[]
                    for a,c in intervals:
                        if a<S.REAR_AXLE-rr:cut.append((a,min(c,S.REAR_AXLE-rr)))
                        if c>S.REAR_AXLE+rr:cut.append((max(a,S.REAR_AXLE+rr),c))
                    intervals=cut
            sec=[(0,-.052),(.015,-.052),(.028,-.033),(.030,.033),(.015,.052),(0,.052)]
            for j,(a,c) in enumerate(intervals):
                if c-a<.01:continue
                rings=[[(sign*(1.220+dx),yy,z+zz) for dx,zz in sec] for yy in [a,c]]
                b.add(G.loft(f'Pressed rub rail {sign} {ri} {j}',rings,b.m['black']))
        # Sheet lap seams end at the roof rail. Normal-baked rivets are added in finishes.
        for i in range(14):
            y=S.ROW_START-S.ROW_PITCH/2+i*S.ROW_PITCH
            if sign>0 and abs(y-(S.ROW_START+S.SIDE_EXIT_ROW*S.ROW_PITCH))<.35:continue
            if y>1.36 and y<2.60:continue
            b.box(f'Lower lap seam {sign} {i}',(sign*1.221,y,1.314),(.0015,.004,1.03),'black',r=0)
        # Reflective black/white aging is material-only at checkpoint, no false red rear tape.
        for j in range(18):
            y=-2.60+j*.47
            if abs(y-S.REAR_AXLE)<.65:continue
            b.box(f'Body reflective tape {sign} {j}',(sign*1.229,y,1.028),(.0018,.355,.034),'white',r=0)
        # Lettering reads outward on each side; winding is deliberately independent.
        y0,y1=-2.10,.88;z0,z1=1.405,1.567;x=sign*1.244
        corners=[(x,y0,z0),(x,y1,z0),(x,y1,z1),(x,y0,z1)]
        if sign<0:corners=[corners[1],corners[0],corners[3],corners[2]]
        b.print('District lettering '+str(sign),corners,f'district-{b.seed}')
        y=4.97;corners=[(x,y-.24,1.26),(x,y+.24,1.26),(x,y+.24,1.49),(x,y-.24,1.49)]
        if sign<0:corners=[corners[1],corners[0],corners[3],corners[2]]
        b.print('Fleet number '+str(sign),corners,f'fleet-{b.seed}')
    # Rounded rear corner caps and back panels around a genuine door opening.
    for sign in [-1,1]:
        b.box('Rear lower field '+str(sign),(sign*.855,6.006,1.260),(.729,.032,1.010),r=.010)
        b.box('Rear upper field '+str(sign),(sign*.855,6.006,2.702),(.729,.032,.157),r=.010)
        for xx in [sign*.516,sign*1.184]:b.box('Rear window jamb '+str(sign)+str(xx),(xx,6.006,2.195),(.048,.032,.86),r=.004)
        b.box('Glass rear corner '+str(sign),(sign*.855,6.013,2.220),(.602,.0048,.738),'windshield',category='glass',r=0)
        b.tube('Rear corner glass seal '+str(sign),[(sign*.540,6.027,1.835),(sign*1.169,6.027,1.835),(sign*1.169,6.027,2.605),(sign*.540,6.027,2.605),(sign*.540,6.027,1.835)],.018)
        for z in [1.624,1.222,.795]:b.box('Rear rail return '+str(sign)+str(z),(sign*.858,6.035,z),(.69,.040,.104),'black',r=.010)
    b.box('Rear lower sill',(0,6.006,.965),(1.0,.038,.420))
    b.box('Rear exit header',(0,6.006,2.690),(1.02,.038,.080))
    # Front roof cap, flattened warning-light lands and black SCHOOL BUS band.
    for front,y in [(True,-3.92),(False,6.006)]:
        section=roof_section(y,.20 if front else .115)
        poly=[(-S.WIDTH/2,2.70)]+[(x,z) for x,_,z in section[1:-1]]+[(S.WIDTH/2,2.70)]
        b.add(G.profile(('Front' if front else 'Rear')+' roof cap',poly,y-.012,y+.012,b.m['yellow'],axis='Y'))
        outward=-1 if front else 1;yy=y+outward*.023
        b.box(('Front' if front else 'Rear')+' destination black surround',(0,yy,2.868),(1.245,.016,.276),'black',r=.025)
        corners=[(-.586,yy+outward*.010,2.738),(.586,yy+outward*.010,2.738),(.586,yy+outward*.010,2.995),(-.586,yy+outward*.010,2.995)]
        if not front:corners=[corners[1],corners[0],corners[3],corners[2]]
        # Yellow legend is standard; graphic substrate is separately black.
        b.print(('Front' if front else 'Rear')+' school legend',corners,'school')
    # Cowl and windshield on a smooth original two-piece laminate die.
    b.box('Front cowl',(0,-3.893,1.837),(2.36,.16,.12),r=.025)
    b.box('Windshield header closure',(0,-3.710,2.705),(2.36,.067,.035),r=.008)
    b.box('Firewall closed front body',(0,-3.892,1.320),(2.352,.035,1.030),r=.014)
    for sign in [-1,1]:
        def glass(u,v,sign=sign):
            x=sign*(.025+1.113*u);z=1.900+.772*v
            return (x,-3.998+.273*v+.035*(x/1.138)**2,z)
        ob=panel('Glass windshield '+str(sign),glass,[i/8 for i in range(9)],[i/4 for i in range(5)],b.m['windshield'],(0,-1,0),gauge=.0048,return_depth=0);b.add(ob,category='glass')
        b.tube('Windshield outer seal '+str(sign),[glass(0,0),glass(1,0),glass(1,1),glass(0,1),glass(0,0)],.022)
        b.tube('Windshield wiper '+str(sign),[(sign*.72,-3.994,2.020),(sign*.30,-3.988,2.30),(sign*.37,-3.970,2.47)],.009)
    for sign in [-1,1]:
        b.box('Front corner structural post '+str(sign),(sign*1.174,-3.75,2.302),(.073,.20,.83),r=.016)
    b.socket('Door',(-1.25,-3.37,.40),'entrance')

def bearing(b,name,center,axis,parent,half=.028,extension=.017):
    """A real pin inside a hollow sleeve; the caller supplies its structural feet."""
    ob=G.lathe(name+' sleeve',[(-half,.013),(half,.013),(half,.0064),(-half,.0064)],b.m['black'],12,axis=axis,closed=True)
    ob.location=center;b.add(ob,parent)
    v=Vector((1,0,0) if axis=='X' else (0,0,1));c=Vector(center)
    b.add(G.cylinder(name+' fixed pin',c-v*(half+extension),c+v*(half+extension),.006,b.m['aluminum'],12))

def hatch(b,name,y):
    # Cut the source roof with a true hole and surround it with a bolted curb.
    roof=bpy.data.objects['Formed roof steel'];liner=bpy.data.objects['Ceiling formed liner']
    for ob in [roof,liner]:
        cutter=G.box('Temporary hatch cut',(0,y,3.20),(.56,.64,.55),None,0);G.boolean(ob,cutter)
    b.box(name+' curb',(0,y,3.192),(.62,.70,.020),'black',r=.020)
    # Curb frame is hollow: remove center before the lid is added.
    curb=bpy.data.objects[name+' curb'];G.boolean(curb,G.box('Curb hole',(0,y,3.192),(.54,.62,.10),None,0))
    p=pivot(b,name,(0,y+.35,3.220),axis='X',limits=(-80,0))
    b.box(name+' lid',(0,y,3.215),(.595,.675,.026),'white',p,r=.025)
    b.box(name+' interior release',(0,y,3.175),(.15,.07,.025),'red',p,category='interior',r=.006)
    bearing(b,name+' hinge',(0,y+.35,3.220),'X',p,half=.280,extension=.057)
    b.box(name+' hinge moving leaf',(0,y+.33,3.2305),(.50,.080,.005),'aluminum',p,r=.001)
    for sign in [-1,1]:
        b.box(name+' hinge foot',(sign*.317,y+.364,3.212),(.014,.022,.033),'aluminum',r=.001)
        b.box(name+' curb hinge flange',(sign*.306,y+.349,3.195),(.044,.050,.010),'aluminum',r=.001)

def doors(b):
    # Outward-opening entrance leaves: hinge axes at opposite jambs.
    ya,yc=-3.750,-2.940
    for label,y,hinge,limits in [('front',-3.549,ya,(0,98)),('rear',-3.141,yc,(-98,0))]:
        p=pivot(b,'Entrance_'+label,(-1.241,hinge,.37),axis='Z',limits=limits)
        b.frame_side('Entrance '+label,-1.241,y,1.535,.393,2.350,'black',p,rail=.038)
        b.box('Entrance '+label+' middle',(-1.245,y,1.61),(.038,.323,.075),'yellow',p)
        for level,z,h in [('lower',.965,1.12),('upper',2.146,.94)]:b.glass_side('entrance '+label+' '+level,-1.242,y,z,.310,h,p)
        for z in [.55,1.55,2.50]:
            b.tube('Entrance '+label+' hinge barrel',[(-1.241,hinge,z-.035),(-1.241,hinge,z+.035)],.012,'black',p)
    # Real stacked steps occupy the gap left by the raised floor.
    for i in range(4):
        x=-1.118+i*.205;z=.340+i*.210
        b.box('Entrance step riser '+str(i),(x,-3.345,z-.098),(.207,.780,.196),'yellow',category='interior',r=.002)
        b.box('Worn entrance tread '+str(i),(x,-3.345,z+.006),(.207,.780,.016),'floor',category='interior',r=.002)
        b.box('Step safety nosing '+str(i),(x-.102,-3.345,z+.009),(.025,.778,.013),'white',category='interior',r=.002)
    b.tube('Entrance grab rail',[(-1.10,-2.975,.354),(-1.10,-2.975,.65),(-.96,-2.975,1.42),(-.50,-2.975,1.72),(-.35,-2.975,1.72),(-.35,-2.878,1.72)],.016,'aluminum',category='interior',sides=10)
    b.box('Grab rail barrier flange',(-.35,-2.874,1.72),(.065,.008,.065),'aluminum',category='interior',r=.002)
    # Rear emergency door occupies the physical 37 x 52-inch opening.
    p=pivot(b,'Emergency_rear',(-.485,6.060,1.198),axis='Z',limits=(0,105))
    b.box('Rear emergency lower leaf',(0,6.026,1.474),(.9398,.037,.535),'yellow',p,r=.005)
    b.box('Rear emergency upper leaf',(0,6.026,2.499),(.9398,.037,.259),'yellow',p,r=.004)
    b.box('Rear emergency top sash',(0,6.026,2.330),(.9398,.037,.090),'yellow',p,r=.004)
    for x in [-.455,.455]:b.box('Rear emergency stile '+str(x),(x,6.026,2.030),(.030,.037,.650),'yellow',p)
    for xx in [-.438,.438]:b.box('Rear door glass seal vertical '+str(xx),(xx,6.036,2.002),(.025,.014,.628),'black',p,r=.007)
    for zz in [1.700,2.304]:b.box('Rear door glass seal horizontal '+str(zz),(0,6.036,zz),(.900,.014,.025),'black',p,r=.007)
    b.box('Glass rear emergency',(0,6.035,2.002),(.845,.0048,.570),'windshield',p,category='glass',r=0)
    for x in [-.477,.477]:b.box('Rear jamb backed reveal '+str(x),(x,5.987,1.920),(.047,.014,1.480),'black',r=.002)
    for z in [1.193,2.638]:b.box('Rear header backed reveal '+str(z),(0,5.987,z),(.98,.014,.044),'black',r=.002)
    for z in [1.29,2.47]:
        bearing(b,'Rear door hinge '+str(z),(-.485,6.060,z),'Z',p)
        b.box('Rear hinge moving leaf',(-.462,6.047,z),(.047,.008,.045),'aluminum',p,r=.001)
        for dz in [-.039,.039]:b.box('Rear hinge fixed foot',(-.505,6.042,z+dz),(.060,.055,.014),'aluminum',r=.001)
    b.tube('Rear exit handle',[(.36,6.065,1.72),(.24,6.090,1.72),(.24,6.090,1.66)],.012,'red',p)
    b.print('Rear emergency label',[(.44,6.052,2.51),(-.44,6.052,2.51),(-.44,6.052,2.59),(.44,6.052,2.59)],'emergency',p)
    # Left side exit removes one three-place bench, leaving 75 passenger places.
    y=S.ROW_START+S.SIDE_EXIT_ROW*S.ROW_PITCH
    p=pivot(b,'Emergency_side',(1.246,y-.332,1.18),axis='Z',limits=(-105,0))
    b.box('Side emergency forward jamb',(1.207,y-.332,2.247),(.045,.018,.876),'yellow',r=.002)
    b.box('Side emergency lower',(1.229,y,1.504),(.032,.640,.648),'yellow',p)
    b.frame_side('Side emergency upper frame',1.242,y,2.252,.642,.850,'yellow',p,rail=.045)
    b.glass_side('side emergency',1.236,y,2.252,.540,.746,p)
    b.tube('Side exit latch',[(1.268,y-.23,1.71),(1.292,y-.08,1.71)],.012,'red',p)
    for z in [1.40,1.95,2.50]:
        bearing(b,'Side door hinge '+str(z),(1.246,y-.332,z),'Z',p)
        for dz in [-.039,.039]:b.box('Side hinge fixed foot',(1.232,y-.341,z+dz),(.036,.036,.014),'aluminum',r=.001)
    b.print('Side exit label',[(1.268,y-.29,1.722),(1.268,y+.29,1.722),(1.268,y+.29,1.795),(1.268,y-.29,1.795)],'emergency',p)
    for name,yy in [('Roof_hatch_front',-1.4),('Roof_hatch_rear',3.9)]:hatch(b,name,yy)

def bumper(b,name,front,width,depth,z0,z1):
    """Six-millimeter pressed steel C section, swept back around both corners."""
    end=S.FRONT if front else S.REAR;direction=1 if front else -1;g=.006
    rings=[]
    for x,wrap in [(-width/2,.09),(-width/2+.12,.02),(-width/2+.20,0),(width/2-.20,0),(width/2-.12,.02),(width/2,.09)]:
        y=end+direction*wrap
        section=[(y,z0),(y,z1),(y+direction*depth,z1),(y+direction*depth,z1-g),(y+direction*g,z1-g),(y+direction*g,z0+g),(y+direction*depth,z0+g),(y+direction*depth,z0)]
        rings.append([(x,yy,zz) for yy,zz in section])
    ob=G.loft(name,rings,b.m['black']);G.bevel(ob,.0015,1);b.add(ob)

def hood(b):
    # Compound molded hood: each section is independently rounded across width and down both cheeks.
    # No extrusion of a side-view polygon; transverse crown changes along its length.
    stations=[(-5.916,.725,1.520,1.060),(-5.87,.755,1.565,1.035),(-5.55,.780,1.642,1.015),(-4.95,.800,1.765,1.045),(-4.38,.825,1.860,1.145),(-3.96,.858,1.888,1.240)]
    loops=[]
    for y,w,top,bottom in stations:
        sec=[(-w,bottom),(-w,top-.145),(-w*.98,top-.078),(-w*.91,top-.026),(-w*.76,top),(-w*.42,top+.017),(0,top+.025),(w*.42,top+.017),(w*.76,top),(w*.91,top-.026),(w*.98,top-.078),(w,top-.145),(w,bottom)]
        loops.append([(x,y,z) for x,z in sec])
    ob=G.loft('Compound hood shell',loops,b.m['yellow'],caps=False,closed=False);G.smooth(ob,50)
    mod=ob.modifiers.new('Molded hood wall','SOLIDIFY');mod.thickness=.006;mod.offset=-1;b.add(ob)
    # Sealed front wall around the recessed grille instead of an uncut box.
    y=-5.922
    for sign in [-1,1]:b.box('Front nose cheek '+str(sign),(sign*.622,y,1.303),(.245,.035,.439),r=.045)
    b.box('Nose top land',(0,y,1.511),(1.025,.035,.066),r=.020)
    b.box('Nose lower land',(0,y,1.071),(1.08,.035,.075),r=.018)
    b.box('Front lower molded chin',(0,-5.871,.890),(1.65,.11,.27),'yellow',r=.055)
    b.box('Front recessed valance',(0,-5.960,.799),(2.05,.10,.10),'black',r=.027)
    # Narrow rounded grille molding, its back and cell webs all behind the nose lands.
    contour=G.rounded_rectangle(.994,.392,.065,5)
    rings=[[(x,y+.010,z+1.294) for x,z in contour],[(x*.967,y+.018,1.294+z*.92) for x,z in contour],[(x*.967,y+.050,1.294+z*.92) for x,z in contour]]
    ob=G.ring_loft('Seated grille molding',rings,b.m['black']);b.add(ob)
    b.box('Grille radiator bed',(0,-5.826,1.294),(.976,.018,.366),'black',r=.055)
    # Import the accepted hatchback's recessed open-web manufacturing method.
    # Only authored scale/bow/pitch differ; no car source or delivery is modified.
    from hatch_grille import lattice,face_y
    b.m['grille_bar']=b.m['frame']
    lattice(b,'C75 recessed diamond web',.585,.942,.348,17,3,.0035,.014)
    web=bpy.data.objects['C75 recessed diamond web'];web['part_category']='shell'
    for v in web.data.vertices:
        xx,yy,zz=v.co
        # Keep depth, compress the hatch's bow and place it in the bus opening.
        v.co.y=-5.878+.4*(face_y(xx,zz)-face_y(0,.585))+(yy-face_y(xx,zz)-.026)
        v.co.z+=1.294-.585
    # Front fenders are rounded annular moldings with a deep wheelhouse.
    for sign in [-1,1]:
        def quarter(u,v,sign=sign):
            yy=-4.42+.515*u;d=yy-S.FRONT_AXLE
            lower=max(.755,S.HUB+math.sqrt(max(0,.69**2-d*d)))
            xx=.86+.34*u+.31*(1-u)*(1-v)**2
            zz=lower+(1.85+.03*u-lower)*v
            return (sign*xx,yy,zz)
        ob=panel('Compound fender cowl '+str(sign),quarter,[i/8 for i in range(9)],[0,.12,.3,.5,.72,.9,1],b.m['yellow'],(sign,0,0),gauge=.004,return_depth=.018);b.add(ob)
        loops=[]
        for x,r in [(sign*.785,.680),(sign*.91,.727),(sign*1.080,.733),(sign*1.174,.700),(sign*1.196,.648),(sign*1.170,.622)]:
            loops.append([(x,S.FRONT_AXLE+r*math.cos(t),S.HUB+r*math.sin(t)) for t in [math.radians(-15+210*i/40) for i in range(41)]])
        n=len(loops[0]);m=len(loops);vs=[p for ring in loops for p in ring]
        fs=[(j*n+k,j*n+k+1,((j+1)%m)*n+k+1,((j+1)%m)*n+k) for j in range(m) for k in range(n-1)]
        fs += [tuple(j*n for j in reversed(range(m))),tuple(j*n+n-1 for j in range(m))]
        ob=G.mesh('Molded front fender '+str(sign),vs,fs,b.m['yellow']);G.smooth(ob,45);b.add(ob)
        # Corner lamp enclosure: closed yellow molded fairing, sealed lens on its face.
        b.box('Front optical housing '+str(sign),(sign*.948,-5.688,1.052),(.400,.185,.365),r=.070)
        b.box('Headlamp gasket '+str(sign),(sign*.948,-5.791,1.066),(.325,.015,.203),'black',r=.034)
        b.box('Lamp front lowbeam '+str(sign),(sign*.948,-5.801,1.066),(.277,.006,.157),'headlight',category='lamps',r=.026)
        def cover(u,v,sign=sign):
            xx=sign*.948+(u-.5)*.281;zz=1.066+(v-.5)*.161
            return (xx,-5.808-.006*math.sin(math.pi*u)*math.sin(math.pi*v),zz)
        ob=panel('Glass sealed headlamp cover '+str(sign),cover,[0,.15,.35,.65,.85,1],[0,.25,.75,1],b.m['windshield'],(0,-1,0),gauge=.0024,return_depth=0);b.add(ob,category='glass')
        b.box('Front amber signal '+str(sign),(sign*.948,-5.798,.906),(.230,.009,.073),'amber',category='lamps',r=.017)
        b.box('Hood shut line '+str(sign),(sign*.849,-4.005,1.646),(.008,.022,.320),'black')
        b.box('Hood rubber latch '+str(sign),(sign*.855,-4.18,1.476),(.030,.060,.155),'black',r=.008)
        b.tube('Hood latch loop '+str(sign),[(sign*.865,-4.20,1.54),(sign*.875,-4.20,1.62),(sign*.866,-4.16,1.65)],.007,'aluminum')
    # Broad pressed steel bumpers wrap the corners and carry the crossing-arm actuator.
    bumper(b,'Front pressed bumper',True,2.35,.204,.470,.790)
    bumper(b,'Rear pressed bumper',False,2.43,.180,.500,.800)
    b.print('Front maker badge',[(-.23,-5.948,1.437),(.23,-5.948,1.437),(.23,-5.948,1.492),(-.23,-5.948,1.492)],'maker')
    for end,yy in [('Front',S.FRONT-.001),('Rear',S.REAR+.001)]:
        low=.4725 if end=='Front' else .57;high=low+.155
        corners=[(-.155,yy,low),(.155,yy,low),(.155,yy,high),(-.155,yy,high)]
        if end=='Rear':corners=[corners[1],corners[0],corners[3],corners[2]]
        b.print(end+' fictional license',corners,f'plate-{b.seed}')

def wheel(b,code,x,y,sign,steer=False):
    parent=b.root
    if steer:parent=pivot(b,'Steer_'+code,(x,y,S.HUB),axis='Z',limits=(-40,40))
    spin=pivot(b,'Wheel_'+code,(x,y,S.HUB),parent,axis='X',limits=(-360,360))
    tire=loaded_tire('Tire_'+code,(x,y,S.HUB),S.TIRE_WIDTH,S.TIRE_ASPECT,S.RIM,b.m['tire'],96,
                     profile_indices=[0,1,3,4,5,7,9,10,11,13,14],rolling_radius=S.HUB)
    b.add(tire,spin,'wheels')
    r=S.RIM*.0254/2
    # Car-family lathe method, sized as a deep 22.5-inch truck steel disc.
    pr=[(-.100,r-.017),(-.100,r+.004),(-.085,r+.004),(.088,r-.008),(.109,r+.009),(.117,r-.004),(.112,r-.025),(.083,r-.027)]
    # The car's graded-ring method retains 128 stations only at exposed rolled lips.
    counts=[16,16,16,32,64,64,32,16] if code.endswith('inner') else [32,32,32,64,128,128,64,32];vs=[];starts=[];fs=[]
    for (ax,rr),num in zip(pr,counts):
        starts.append(len(vs));vs.extend((x+sign*ax,y+rr*math.cos(math.tau*k/num),S.HUB+rr*math.sin(math.tau*k/num)) for k in range(num))
    for j,num in enumerate(counts):
        jj=(j+1)%len(counts);other=counts[jj];i=k=0
        while i<num or k<other:
            va=starts[j]+i%num;vb=starts[jj]+k%other
            if (i+1)*other==(k+1)*num:fs.append((va,starts[j]+(i+1)%num,starts[jj]+(k+1)%other,vb));i+=1;k+=1
            elif (i+1)*other<(k+1)*num:fs.append((va,starts[j]+(i+1)%num,vb));i+=1
            else:fs.append((va,starts[jj]+(k+1)%other,vb));k+=1
    ob=G.mesh('Truck rim '+code,vs,fs,b.m['wheel']);G.smooth(ob,35);b.add(ob,spin,'wheels')
    # Dished pressed disc and ten recessed ventilation holes, rather than passenger alloy spokes.
    pr=[(.080,.080),(.080,.124),(.035,.198),(.059,.247),(.080,.256),(.090,.247),(.059,.199),(.112,.125),(.112,.080)]
    disc=G.lathe('Pressed wheel disc '+code,[(x+sign*a,rr) for a,rr in pr],b.m['wheel'],64,axis='X',center=(y,S.HUB),closed=True)
    # Through holes use modest round cutters in the actual steel dish.
    for k in range(8):
        t=math.tau*k/8;cy=y+.187*math.cos(t);cz=S.HUB+.187*math.sin(t)
        cut=G.cylinder('Temporary vent',(x-.18,cy,cz),(x+.18,cy,cz),.027,None,12);G.boolean(disc,cut)
    G.smooth(disc,40);b.add(disc,spin,'wheels')
    profile=[(.074,.078),(.074,.089),(.135,.089),(.153,.065),(.153,0),(.144,0),(.144,.078)]
    if code.endswith('inner'):profile=[(.074,.078),(.074,.089),(.135,.089),(.144,.078)]
    hub=G.lathe('Truck hub '+code,[(x+sign*a,rr) for a,rr in profile],b.m['frame'],32,axis='X',center=(y,S.HUB),closed=True);b.add(hub,spin,'wheels')
    if steer:
        b.tube('Front spindle '+code,[(x-sign*.067,y,S.HUB),(x+sign*.136,y,S.HUB)],.077,'frame',parent,category='chassis',sides=24)
    for k in range(10):
        t=math.tau*k/10;cy=y+.1143*math.cos(t);cz=S.HUB+.1143*math.sin(t)
        ob=G.cylinder('Wheel lug '+code+str(k),(x+sign*.100,cy,cz),(x+sign*.131,cy,cz),.012,b.m['aluminum'],6);b.add(ob,spin,'wheels')

def chassis(b):
    for sign in [-1,1]:
        # Open C-channel frame, actual gauge and flanges rather than massive bars.
        sec=[(-.041,-.129),(.041,-.129),(.041,-.121),(-.033,-.121),(-.033,.121),(.041,.121),(.041,.129),(-.041,.129)]
        loops=[[(sign*.402+sign*x,y,.865+z) for x,z in sec] for y in [-5.79,5.90]]
        b.add(G.loft('Chassis C rail '+str(sign),loops,b.m['frame']),category='chassis')
    for y in [-5.3,-3.7,-2.0,0,1.4,3.2,4.8,5.8]:b.box('Chassis crossmember '+str(y),(0,y,.889),(.80,.067,.146),'frame',category='chassis',r=.005)
    for sign in [-1,1]:
        for label,y,z in [('Front',-5.87,.77),('Rear',5.91,.76)]:b.box(label+' bumper frame bracket '+str(sign),(sign*.402,y,z),(.085,.26,.11),'frame',category='chassis',r=0)
    for label,y in [('Front',S.FRONT_AXLE),('Rear',S.REAR_AXLE)]:
        span=.95 if label=='Front' else 1.20
        b.tube(label+' axle',[(-span,y,S.HUB),(span,y,S.HUB)],.077,'frame',category='chassis',sides=24)
        if label=='Rear':
            ob=G.lathe('Differential housing',[(-.22,0),(-.22,.115),(-.12,.185),(.13,.185),(.22,.10),(.22,0)],b.m['frame'],16,axis='X',center=(y,S.HUB));b.add(ob,category='chassis')
        for sign in [-1,1]:
            for k in range(4):
                length=1.24-k*.14
                ps=[(sign*.415,y-length/2+length*j/8,.662+.092*(2*j/8-1)**2+k*.010) for j in range(9)]
                # True measured spring width ~76mm, finite steel strips.
                loops=[[(p[0]+dx,p[1],p[2]+dz) for dx,dz in [(-.038,-.004),(.038,-.004),(.038,.004),(-.038,.004)]] for p in ps]
                b.add(G.loft(label+' leaf spring '+str(sign)+' '+str(k),loops,b.m['frame']),category='chassis')
            for dy in [-.62,.62]:b.box(label+' spring hanger '+str(sign)+str(dy),(sign*.415,y+dy,.770),(.095,.080,.19),'frame',category='chassis',r=.009)
    wheel(b,'FL',1.015,S.FRONT_AXLE,1,True);wheel(b,'FR',-1.015,S.FRONT_AXLE,-1,True)
    for sign,side in [(-1,'R'),(1,'L')]:
        for label,x in [('outer',1.057),('inner',.748)]:wheel(b,'R'+side+'_'+label,sign*x,S.REAR_AXLE,sign)
        for y in [S.FRONT_AXLE+.75,S.REAR_AXLE+.68]:
            b.box('Mud flap '+side+str(y),(sign*.985,y,.465),(.40,.018,.48),'black',category='chassis',r=.008)
            width=.44 if y<0 else .48
            b.box('Mud flap mounting clamp '+side+str(y),(sign*.985,y,.7275),(width,.04,.055),'frame',category='chassis',r=.002)
    b.box('Fuel tank',(0,4.52,.743),(.69,1.40,.40),'frame',category='chassis',r=.065)
    for yy in [4.05,4.98]:b.box('Fuel tank strap '+str(yy),(0,yy,.751),(.72,.045,.427),'aluminum',category='chassis',r=.02)
    b.tube('Propeller shaft',[(0,-3.9,.60),(0,S.REAR_AXLE,.523)],.044,'frame',category='chassis',sides=10)
    exhaust=[(-.32,-3.5,.65),(-.32,.8,.60),(-.32,2.70,.55),(-.70,3.2,.54),(-.91,5.5,.54),(-1.30,5.67,.50)]
    b.tube('Exhaust tailpipe',exhaust,.044,'frame',category='chassis',sides=12)
    for y in [0,3.4,5.4]:
        a,c=next((a,c) for a,c in zip(exhaust,exhaust[1:]) if a[1]<=y<=c[1]);t=(y-a[1])/(c[1]-a[1]);x=a[0]+t*(c[0]-a[0]);z=a[2]+t*(c[2]-a[2])
        b.tube('Exhaust hanger '+str(y),[(-.402,y,.740),(x+.05,y,z-.05),(x,y,z-.044)],.009,'black',category='chassis')

def interior(b):
    # Rows have molded curved backs with radiused corners and finite cushions.
    for i in range(S.ROWS):
        y=S.ROW_START+i*S.ROW_PITCH
        for sign in [-1,1]:
            if sign>0 and i==S.SIDE_EXIT_ROW:continue
            x=sign*.657;name=f'Bench_{i:02d}_'+('L' if sign>0 else 'R')
            b.box(name+' cushion',(x,y-.07,1.590),(.9906,.452,.128),'vinyl',category='interior',r=.060)
            # Compound cross sections taper gently across and through the padded crown.
            rings=[]
            for z,w,dy,depth in [(1.57,.455,.08,.040),(1.72,.475,.085,.063),(1.96,.475,.105,.069),(2.285,.465,.122,.065),(2.335,.425,.128,.025)]:
                contour=G.rounded_rectangle(w*2,depth*2,min(depth*.75,.035),3)
                rings.append([(x+xx,y+dy+yy,z) for xx,yy in contour])
            ob=G.loft(name+' padded back',rings,b.m['vinyl']);G.smooth(ob,50);b.add(ob,category='interior')
            for dx in [-.345,.345]:
                b.box(name+' foot plate '+str(dx),(x+dx,y-.17,1.183),(.055,.065,.006),'frame',category='interior',r=0)
                b.tube(name+' support '+str(dx),[(x+dx,y-.17,1.185),(x+dx,y-.17,1.52),(x+dx,y+.11,1.58),(x+dx,y+.13,1.92)],.015,'frame',category='interior',sides=6)
            # One socket for the bench and individual passenger locations.
            b.socket(name,(x,y-.08,1.70))
            for j in range(3):b.socket(name+f'_Place{j}',(x+(j-1)*.310,y-.08,1.70))
    # Forward barrier and driver enclosure avoid a window over an empty hull.
    b.box('Front passenger barrier',(-.685,-2.82,1.815),(.960,.100,1.04),'vinyl',category='interior',r=.045)
    b.box('Driver seat cushion',(.695,-3.43,1.67),(.51,.48,.13),'black',category='interior',r=.055)
    back=b.box('Driver high back',(.695,-3.14,1.99),(.51,.14,.70),'black',category='interior',r=.055);back.rotation_euler.x=-.08
    b.box('Driver suspension pedestal',(.695,-3.39,1.41),(.30,.30,.46),'frame',category='interior',r=.025)
    b.socket('Driver',(.695,-3.40,1.76),'driver')
    b.box('Molded dash',(0,-3.825,1.849),(2.17,.37,.28),'dash',category='interior',r=.065)
    b.box('Driver instrument binnacle',(.68,-3.70,1.99),(.60,.24,.20),'dash',category='interior',r=.045)
    b.tube('Steering column',[(.695,-3.78,1.180),(.695,-3.43,1.935)],.034,'black',category='interior',sides=10)
    loop(b,'Steering wheel',(.695,-3.43,1.935),(1,0,0),(0,.82,.57),(.227,.227),.016,b.m['black'],'interior',segments=40,sides=8)
    for dx,dy in [(-.20,0),(.20,0),(0,-.17)]:b.tube('Steering spoke '+str(dx),[(.695,-3.43,1.935),(.695+dx,-3.43+dy*.82,1.935+dy*.57)],.014,'black',category='interior')
    b.box('Driver switch console',(1.02,-3.31,1.71),(.21,.70,.15),'dash',category='interior',r=.020)
    for i in range(7):b.box('Rocker door control '+str(i),(.975,-3.54+i*.063,1.793),(.025,.035,.012),'red' if i==0 else 'black',category='interior',r=.003)
    for y in [-2.4,-.7,1,2.7,4.4]:
        for sign in [-1,1]:b.box('Ceiling dome '+str(sign)+str(y),(sign*.56,y,3.119),(.23,.15,.022),'dome',category='interior',r=.030)

def fittings(b):
    # Eight warning lamps at each end, red outside and amber inboard, with black visors.
    for front,y in [(True,-3.957),(False,6.035)]:
        outward=-1 if front else 1
        for sign in [-1,1]:
            for label,x,mat in [('red',.997,'warning_red'),('amber',.736,'amber')]:
                p=(sign*x,y,2.876)
                ob=G.cylinder(('Front' if front else 'Rear')+' warning housing '+label+str(sign),(p[0],y-outward*.045,p[2]),(p[0],y+outward*.007,p[2]),.118,b.m['black'],32);b.add(ob)
                ob=G.cylinder(('Front' if front else 'Rear')+' warning emitter '+label+str(sign),(p[0],y+outward*.009,p[2]),(p[0],y+outward*.016,p[2]),.098,b.m[mat],40);b.add(ob,category='lamps')
                b.box('Lamp visor '+str(front)+label+str(sign),(sign*x,y+outward*.03,3.000),(.243,.135,.020),'black',r=.008)
        for x in [-.10,0,.10]:b.box('Roof clearance marker '+str(front)+str(x),(x,y,3.065),(.06,.025,.034),'amber' if front else 'warning_red',category='lamps',r=.009)
    for sign in [-1,1]:
        for y in [-2.82,5.7]:b.box('Side marker '+str(sign)+str(y),(sign*1.237,y,1.115),(.023,.10,.055),'amber' if y<0 else 'warning_red',category='lamps',r=.01)
        for z in [1.05,1.41]:
            ob=G.cylinder('Rear round tail '+str(sign)+str(z),(sign*.88,6.032,z),(sign*.88,6.050,z),.086,b.m['warning_red'],32);b.add(ob,category='lamps')
        b.box('Rear reverse '+str(sign),(sign*.87,6.043,.886),(.12,.018,.07),'headlight',category='lamps',r=.015)
    b.box('Strobe foot',(0,1.1,3.219),(.16,.16,.035),'black',r=.02)
    ob=G.lathe('Roof strobe dome',[(0,0),(0,.066),(.075,.066),(.092,.045),(.092,0)],b.m['strobe'],24);ob.location=(0,1.1,3.238);b.add(ob,category='lamps')
    # Side mirrors: two triangular braces bolt to the windshield/side pillars.
    for sign in [-1,1]:
        for z in [1.91,2.51]:
            b.tube('Mirror triangular support '+str(sign)+str(z),[(sign*1.19,-3.80,z),(sign*1.55,-4.10,z+.08),(sign*1.52,-4.17,2.24)],.013,'black',sides=8)
            b.box('Mirror support foot '+str(sign)+str(z),(sign*1.19,-3.80,z),(.040,.10,.080),'black',r=.008)
        b.box('Side mirror backing '+str(sign),(sign*1.55,-4.17,2.286),(.25,.115,.65),'black',r=.045)
        # Mirror faces forward slightly toward the driver rather than straight sideways.
        b.box('Side mirror plane '+str(sign),(sign*1.55,-4.235,2.397),(.218,.007,.377),'mirror',r=.026)
        b.box('Side convex mirror '+str(sign),(sign*1.55,-4.238,2.074),(.218,.008,.213),'mirror',r=.030)
        # Crossover mirror has a true curved ellipsoidal face and two supports.
        b.tube('Crossview mirror bracket '+str(sign),[(sign*.780,-5.59,1.37),(sign*1.38,-5.90,1.69),(sign*1.36,-6.02,1.94)],.013,'black')
        b.tube('Crossview mirror brace '+str(sign),[(sign*.757,-5.80,1.43),(sign*1.38,-5.90,1.69)],.011,'black')
        b.box('Crossview primary foot '+str(sign),(sign*.783,-5.59,1.37),(.014,.075,.080),'black',r=.004)
        b.box('Crossview brace foot '+str(sign),(sign*.766,-5.80,1.43),(.014,.070,.070),'black',r=.004)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=(sign*1.36,-6.04,1.985));ob=bpy.context.object;ob.name='Convex crossview '+str(sign);ob.scale=(.157,.059,.125);ob.data.materials.append(b.m['mirror']);G.smooth(ob);b.add(ob)
    # Stop arm folds flat rearwards on the driver's side, swings out 90 degrees.
    p=pivot(b,'Stop_arm',(1.302,-2.70,1.78),axis='Z',limits=(-90,0))
    b.box('Stop arm actuator',(1.252,-2.70,1.77),(.070,.17,.22),'black',r=.019)
    for z in [1.59,1.97]:b.tube('Stop arm hinge '+str(z),[(1.302,-2.70,z-.03),(1.302,-2.70,z+.03)],.015,'black',p)
    for z in [1.63,1.93]:b.box('Stop arm mounting strap',(1.295,-2.615,z),(.012,.180,.040),'aluminum',p,r=.002)
    cy=-2.36;cz=1.78;across=.500;radius=across/(2*math.cos(math.pi/8))
    poly=[(cy+radius*math.cos(math.pi/8+k*math.tau/8),cz+radius*math.sin(math.pi/8+k*math.tau/8)) for k in range(8)]
    b.add(G.profile('Stop octagon white border',poly,1.286,1.297,b.m['white'],axis='X'),p)
    rr=radius-.016/math.cos(math.pi/8);inner=[(cy+rr*math.cos(math.pi/8+k*math.tau/8),cz+rr*math.sin(math.pi/8+k*math.tau/8)) for k in range(8)]
    for sign,x in [(-1,1.284),(1,1.299)]:
        b.add(G.profile('Stop red reflective face '+str(sign),inner,x-.001,x+.001,b.m['red'],axis='X'),p)
        corners=[(x+sign*.002,cy-.212,cz-.135),(x+sign*.002,cy+.212,cz-.135),(x+sign*.002,cy+.212,cz+.135),(x+sign*.002,cy-.212,cz+.135)]
        if sign<0:corners=[corners[1],corners[0],corners[3],corners[2]]
        b.print('Stop legend '+str(sign),corners,'stop',p)
        for z in [cz-.172,cz+.172]:
            ob=G.cylinder('Stop red lamp '+str(sign)+str(z),(x,cy,z),(x+sign*.014,cy,z),.038,b.m['warning_red'],24);b.add(ob,p,'lamps')
    # Crossing gate: long yellow U-loop, rests along front bumper then swings forward.
    p=pivot(b,'Crossing_arm',(-1.01,S.FRONT-.043,.71),axis='Z',limits=(-90,0))
    b.box('Crossing arm actuator',(-1.01,S.FRONT+.035,.71),(.22,.090,.20),'black',r=.020)
    ob=G.lathe('Crossing gate bearing',[(-.038,.024),(.038,.024),(.038,.0129),(-.038,.0129)],b.m['black'],16,closed=True);ob.location=(-1.01,S.FRONT-.043,.71);b.add(ob)
    b.tube('Crossing gate spindle',[(-1.01,S.FRONT-.043,.63),(-1.01,S.FRONT-.043,.79)],.012,'aluminum',p,sides=16)
    b.box('Crossing gate mounting tab',(-1.01,S.FRONT+.0045,.71),(.070,.051,.070),'frame',r=.002)
    b.tube('Crossing arm U loop',[(-1.005,S.FRONT-.060,.765),(.77,S.FRONT-.060,.765),(.83,S.FRONT-.060,.71),(.77,S.FRONT-.060,.655),(-1.005,S.FRONT-.060,.655)],.012,'yellow',p,sides=10)
    for sign in [-1,1]:
        for name,y,z,w,h in [('Battery service',-.99,.960,.88,.28),('Skirt service',3.31,.960,.76,.28),('Fuel door',4.82,1.12,.24,.27)]:
            b.box(name+' seam '+str(sign),(sign*1.229,y,z),(.004,w+.012,h+.012),'black',r=.005)
            b.box(name+' sheet '+str(sign),(sign*1.233,y,z),(.005,w,h),'yellow',r=.004)
            b.box(name+' latch '+str(sign),(sign*1.244,y+w*.35,z),(.012,.040,.030),'aluminum',r=.003)

def finish_scene(b,out):
    bpy.context.view_layer.update();counts={};parts={}
    # Bake stable rest coordinates on every original part, before UV packing/joining.
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or 'asset_set' not in ob:continue
        G.apply(ob)
        # Reject zero-area construction crumbs before they become an optical shard.
        bm=bmesh.new();bm.from_mesh(ob.data)
        bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
        bmesh.ops.dissolve_degenerate(bm,dist=1e-8,edges=list(bm.edges))
        bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY')
        bad=[f for f in bm.faces if f.calc_area()<1e-12]
        if bad:bmesh.ops.delete(bm,geom=bad,context='FACES')
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
        attr=ob.data.attributes.new('VehicleRest','FLOAT_VECTOR','POINT')
        for row,v in zip(attr.data,ob.data.vertices):row.vector=ob.matrix_world@v.co
        ob.data.calc_loop_triangles();n=len(ob.data.loop_triangles);parts[ob.name]=n
        cat=ob['part_category'];counts[cat]=counts.get(cat,0)+n
    data=dict(seed=b.seed,triangles=sum(counts.values()),categories=counts,parts=parts,
              stage='form/construction checkpoint; quick source materials, no final look development')
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    Path(out).with_suffix('.counts.json').write_text(json.dumps(data,indent=2))
    bpy.context.scene['stage']='form checkpoint';bpy.ops.wm.save_as_mainfile(filepath=str(Path(out).resolve()))
    print('BUS_BUILD',json.dumps({k:v for k,v in data.items() if k!='parts'}),flush=True)

def fleet_templates(b):
    """Three markings on one atlas; parked templates never ship as extra meshes."""
    candidates=[o for o in bpy.context.scene.objects if o.type=='MESH' and any(m and any(t in m.name for t in ['district-','fleet-','plate-']) for m in o.data.materials)]
    for ob in candidates:
        ob['variant_id']=101;ob['bake_offset']=(0,0,0)
        original=ob.data.materials[0].name.split()[-1].rsplit('-',1)[0]
        for seed,offset in [(102,16.),(103,32.)]:
            cp=ob.copy();cp.data=ob.data.copy();bpy.context.collection.objects.link(cp);cp.name=ob.name+' seed '+str(seed)
            cp.data.materials.clear();cp.data.materials.append(b.m[f'{original}-{seed}'])
            for v in cp.data.vertices:v.co.x+=offset
            cp['variant_id']=seed;cp['bake_offset']=(offset,0,0);cp['bake_only']=True

def main():
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=101);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.read_factory_settings(use_empty=True)
    b=Bus(a.seed);body(b);doors(b);hood(b);chassis(b);interior(b);fittings(b);fleet_templates(b);finish_scene(b,a.out)
if __name__=='__main__':main()
