"""Measured manufactured forms. Modules run along local +Y; front is -Y."""
import math
from mathutils import Vector
import geom as Q
from plan import FT,LANE,LEFT,RIGHT,LINE,JOINT,DASH,CYCLE,BRIDGE_Z
from graphics import rect

F_SHAPE=[(-.3048,0),(.3048,0),(.3048,.0762),(.127,.254),(.0762,.8128),(-.0762,.8128),(-.127,.254),(-.3048,.0762)]
# Traditional AASHTO IV, 54 in deep, nominal 26 in flanges / 8 in web.
GIRDER=[(-.3302,0),(.3302,0),(.3302,.2032),(.1016,.4064),(.1016,1.1176),(.3302,1.2446),(.3302,1.3716),(-.3302,1.3716),(-.3302,1.2446),(-.1016,1.1176),(-.1016,.4064),(-.3302,.2032)]

def barrier(name='MedianF',length=6.096,scupper=True):
    rt=Q.root(name,module_kind='barrier');b=Q.Batch(name+'__Mesh',rt)
    if scupper:
        # Actual opening through the lower toe; not a painted black rectangle.
        a=.1524;c=.0762
        b.extrude(F_SHAPE,[-length/2,-a],'Barrier');b.extrude(F_SHAPE,[a,length/2],'Barrier')
        upper=[(-.3048,c),(.3048,c),(.127,.254),(.0762,.8128),(-.0762,.8128),(-.127,.254)]
        b.extrude(upper,[-a,a],'Barrier')
    else:b.extrude(F_SHAPE,[-length/2,length/2],'Barrier')
    # Recessed end joint represented by a real 8 mm assembly gap on placement.
    b.finish();Q.socket(rt,'S',(0,-length/2,0));Q.socket(rt,'N',(0,length/2,0));return rt

def guardrail(name='WBeam',length=3.81,terminal=False):
    rt=Q.root(name,module_kind='guardrail');b=Q.Batch(name+'__Mesh',rt)
    # 12-gauge W section, 12.25 in face envelope, 3.25 in depth; top 31 in.
    z=.7874-.155575
    sec=[(.0,z-.155575),(-.066,z-.127),(-.083,z-.076),(-.016,z),(-.083,z+.076),(-.066,z+.127),(.0,z+.155575)]
    # Two shells and hems make the 2.66 mm stamped sheet visible at its ends.
    sec=sec+[(x+.00266,h) for x,h in reversed(sec)]
    lap=0 if terminal else .1524
    b.extrude(sec,[-length/2-lap,length/2+lap],'Steel')
    post_count=round(length/1.905)
    for y in [-(post_count-1)*1.905/2+j*1.905 for j in range(post_count)]:
        # I-section W6 post, with timber/composite blockout bearing on its web.
        b.box((.28,y,.36),(.006,.102,.72),'Steel')
        for xx in (.206,.354):b.box((xx,y,.36),(.008,.152,.72),'Steel')
        b.box((.104,y,z),(.2032,.1524,.3556),'Wood')
        b.tube([(-.09,y,z),(.30,y,z)],.008,'DarkSteel',6)
    if terminal:
        # Generic NCHRP-350-era energy absorbing head, ground strut and cable.
        # Geometry illustrates construction; not a named/proprietary device.
        b.box((-.07,-length/2+.2,z),(.24,.44,.39),'Steel')
        b.box((-.196,-length/2+.17,z),(.012,.31,.36),'Yellow')
        b.beam((.29,-length/2,.10),(.29,length/2,.10),.09,'Steel',.055)
        b.tube([(.29,-length/2+.35,.10),(.17,length/2-.2,z-.04)],.01,'DarkSteel',6)
        for yy in (-length/2+.13,-length/2+.27):b.box((.28,yy,.24),(.152,.152,.48),'Wood')
    b.finish();Q.socket(rt,'S',(0,-length/2,0));Q.socket(rt,'N',(0,length/2,0));return rt

def cable(name='CableBay',length=6.096):
    rt=Q.root(name,module_kind='cable_barrier');b=Q.Batch(name+'__Mesh',rt)
    b.beam((0,0,0),(0,0,.97),.065,'Steel',.035)
    for h in (.53,.68,.83):
        b.tube([(0,-length/2,h),(0,0,h-.008),(0,length/2,h)],.0095,'DarkSteel',5)
        b.box((0,0,h),(.078,.052,.035),'Steel')
    b.finish();Q.socket(rt,'S',(0,-length/2,0));Q.socket(rt,'N',(0,length/2,0));return rt

def wall(name='SoundPanel',length=6.096,height=4.2672):
    rt=Q.root(name,module_kind='soundwall');b=Q.Batch(name+'__Mesh',rt)
    # Stacked precast panels seated in H-posts; horizontal joints are open 12 mm.
    for j in range(3):b.box((0,0,(j+.5)*height/3),(.1524,length-.06,height/3-.012),'Barrier')
    for y in (-length/2,):
        b.box((0,y,height/2),(.14,.025,height+.12),'Steel')
        for x in (-.12,.12):b.box((x,y,height/2),(.028,.27,height+.12),'Steel')
        b.box((0,y,.05),(.58,.58,.10),'Bridge')
    # Shallow form ribs rather than a decorative flat plane.
    for y in [i*length/12-length/2+.254 for i in range(12)]:
        for s in (-1,1):
            # Ribs are trim relief, not separate solids. The checkpoint keeps
            # their exposed strip; normal baking supplies their tiny returns.
            b.face([(s*.086,y-.0225,.02),(s*.086,y+.0225,.02),(s*.086,y+.0225,height-.02),(s*.086,y-.0225,height-.02)],'Barrier')
    b.finish();Q.socket(rt,'S',(0,-length/2,0));Q.socket(rt,'N',(0,length/2,0));return rt

def sign_face(name,w,h,legend,rt,p):
    x,y,z=p;r=Q.root(name,p,rt,replaceable_panel=True,legend=legend,nominal_width_m=w,nominal_height_m=h)
    b=Q.Batch(name+'__Mesh',r);b.box((0,0,0),(w,.0032,h),'Steel')
    u0,v0,u1,v1=rect(legend)
    b.face([(-w/2,-.0022,-h/2),(w/2,-.0022,-h/2),(w/2,-.0022,h/2),(-w/2,-.0022,h/2)],'Signs',uv=[(u0,v0),(u1,v0),(u1,v1),(u0,v1)])
    for zz in (-h*.32,h*.32):b.box((0,.06,zz),(w-.12,.11,.06),'Steel')
    b.finish();Q.socket(r,'Replace',(0,0,0),'sign_face');return r

def change_legend(panel,legend):
    old=rect(panel['legend']);new=rect(legend)
    for ob in panel.children_recursive:
        if ob.type!='MESH':continue
        ob.data=ob.data.copy();uv=ob.data.uv_layers.active
        for face in ob.data.polygons:
            if ob.data.materials[face.material_index]!=Q.M['Signs']:continue
            for i in face.loop_indices:
                u,v=uv.data[i].uv
                uv.data[i].uv=(new[0]+(u-old[0])/(old[2]-old[0])*(new[2]-new[0]),new[1]+(v-old[1])/(old[3]-old[1])*(new[3]-new[1]))
    panel['legend']=legend

def truss(name='SignTruss',span=34.,cantilever=False,legend='exit',foot_bases=None,foot_depth=.26):
    rt=Q.root(name,module_kind='sign_structure');b=Q.Batch(name+'__Frame',rt)
    low=6.35;top=7.87
    xs=(-span/2,) if cantilever else (-span/2,span/2)
    for x,foot in zip(xs,foot_bases or [0]*len(xs)):
        b.box((x,0,foot+foot_depth/2),(1.35,1.35,foot_depth),'Bridge')
        b.box((x,0,foot+foot_depth+.04),(.75,.75,.08),'Steel')
        b.tube([(x,0,foot+foot_depth+.08),(x,0,top+.20)],.23,'Steel',12)
        for sx in (-.28,.28):
            for sy in (-.28,.28):b.tube([(x+sx,sy,foot+foot_depth+.08),(x+sx,sy,foot+foot_depth+.22)],.028,'DarkSteel',6)
        Q.socket(rt,'Foundation_'+str(x),(x,0,foot),'foundation_base')
    for y in (-.72,.72):
        for z in (low,top):b.tube([(-span/2,y,z),(span/2,y,z)],.085,'Steel',8)
    n=round(span/2.2)
    for j in range(n+1):
        x=-span/2+span*j/n
        for z in (low,top):b.tube([(x,-.72,z),(x,.72,z)],.048,'Steel',6)
        for y in (-.72,.72):b.tube([(x,y,low),(x,y,top)],.048,'Steel',6)
        if j<n:
            nx=x+span/n
            for y in (-.72,.72):b.tube([(x,y,low if j%2==0 else top),(nx,y,top if j%2==0 else low)],.045,'Steel',6)
            for z in (low,top):b.tube([(x,-.72,z),(nx,.72,z)],.045,'Steel',6)
    # Rear catwalk, handrail and mechanically supported lighting tray.
    b.box((0,1.05,low-.12),(span,.58,.035),'DarkSteel')
    for x in (-span/2+i*span/12 for i in range(13)):
        b.beam((x,1.30,low-.12),(x,1.30,low+.88),.035,'Steel')
    b.tube([(-span/2,1.30,low+.88),(span/2,1.30,low+.88)],.025,'Steel',6)
    b.finish()
    sign_face(name+'__Through',7.,2.74,'through',rt,(-5.,-.85,7.86))
    sign_face(name+'__Exit',5.49,2.74,legend,rt,(5.,-.85,7.86))
    sign_face(name+'__Tab',2.43,.61,'exitSmall',rt,(6.53,-.85,9.55))
    Q.socket(rt,'West',(-span/2,0,0));Q.socket(rt,'East',(span/2,0,0));return rt

def light(name='DavitLight'):
    rt=Q.root(name,module_kind='light');b=Q.Batch(name+'__Mesh',rt)
    b.box((0,0,.12),(.66,.66,.24),'Bridge');b.box((0,0,.27),(.45,.45,.06),'Steel')
    # Hollow tapered steel envelope, curved arm at true 12 m mounting height.
    rings=[]
    for z,r in ((.30,.14),(10.8,.065)):
        rings.append([(r*math.cos(i*math.tau/12),r*math.sin(i*math.tau/12),z) for i in range(12)])
    for i in range(12):b.face([rings[0][i],rings[0][(i+1)%12],rings[1][(i+1)%12],rings[1][i]],'Steel')
    b.tube([(0,0,10.8),(0,-.18,11.3),(0,-.65,11.7),(0,-1.25,11.95),(0,-2.4,12.0)],.06,'Steel',8)
    b.box((0,-2.55,12.),(.34,.80,.18),'Steel');b.box((0,-2.55,11.904),(.27,.64,.012),'White')
    for x in (-.16,.16):
        for y in (-.16,.16):b.tube([(x,y,.30),(x,y,.40)],.018,'DarkSteel',6)
    b.finish();Q.socket(rt,'LightEmitter',(0,-2.55,11.90),'engine_light');return rt

def attenuator(name='GoreAttenuator'):
    rt=Q.root(name,module_kind='attenuator');b=Q.Batch(name+'__Mesh',rt)
    # Telescoping cartridges on a guide rail, backed by a concrete anchor.
    b.box((0,2.8,.40),(1.00,.70,.80),'Barrier')
    for j in range(6):
        b.box((0,-2.3+j*.78,.35),(.86,.64,.68),'Steel')
        for side in (-1,1):b.box((side*.48,-2.3+j*.78,.37),(.06,.80,.52),'DarkSteel')
    b.beam((0,-2.6,.10),(0,3,.10),.16,'DarkSteel',.08)
    for y in (-2.3,2.4):b.box((0,y,.03),(.35,.35,.06),'Steel')
    sign_face(name+'__Nose',.91,.76,'chevron',rt,(0,-2.66,.43))
    b.finish();return rt

def girder(name='PrestressedGirder24',length=23.49):
    rt=Q.root(name,module_kind='bridge_girder');b=Q.Batch(name+'__Mesh',rt)
    b.extrude(GIRDER,[(-length/2+length*j/24,.018*math.sin(math.pi*j/24)) for j in range(25)],'Bridge',axis='X')
    b.finish()
    for label,x in [('W',-length/2),('E',length/2)]:Q.socket(rt,label,(x,0,0)).rotation_euler.z=-math.pi/2
    return rt

def pier(name='PierBent'):
    rt=Q.root(name,module_kind='bridge_pier');b=Q.Batch(name+'__Mesh',rt)
    seat=7.10-1.3716-.15
    for y in (-7.,0,7.):
        b.tube([(0,y,-.05),(0,y,seat-1.12)],.60,'Bridge',32)
        b.tube([(0,y,seat-1.12),(0,y,seat-.98)],.67,'Bridge',24)
    b.box((0,0,seat-.57),(2.,19.8,1.10),'Bridge');b.finish()
    Q.socket(rt,'BearingTop',(0,0,seat-.02),'bearing_top');return rt

def gore(name='GorePaving36'):
    rt=Q.root(name,module_kind='gore');b=Q.Batch(name+'__Mesh',rt)
    b.surface([(0,-18,0),(.3,-18,0),(6,18,-.12),(0,18,0)],'Asphalt')
    for j in range(9):
        y=-12+j*3;w=.3+(y+18)/36*5.7
        b.surface([(.1,y,.007),(w-.1,y+1,-.02*w+.007),(w-.1,y+1.6,-.02*w+.007),(.1,y+.6,.007)],'White')
    b.finish();Q.socket(rt,'S',(0,-18,0));Q.socket(rt,'N',(0,18,0));return rt

def bridge(name='Overpass'):
    rt=Q.root(name,module_kind='bridge');b=Q.Batch(name+'__Mesh',rt)
    # 48 m between abutment axes, two 24 m spans. Actual bearing contacts.
    deck_bottom=7.10;gb=deck_bottom-1.3716;seat=gb-.15
    bent=pier(name+'__PierBent');bent.parent=rt
    for side in (-1,1):
        b.box((side*24,0,seat-1.22),(1.35,21.34,2.40),'Bridge')
        b.box((side*24.5,0,(seat+7.35)/2),(.40,21.34,7.35-seat),'Bridge')
        for yy in (-10.55,10.55):
            b.box((side*27.0,yy,6.0),(6.5,.40,2.4),'Bridge')
        # 1:1.6 concrete slope paving below each end, no grass penetrating.
        for j in range(12):
            x0=side*(13.5+j*10/12);x1=side*(13.5+(j+1)*10/12)
            z0=(abs(x0)-13.5)*.68;z1=(abs(x1)-13.5)*.68
            for k in range(12):
                y0=-10.4+k*20.8/12;y1=y0+20.8/12
                b.surface([(x0,y0,z0),(x1,y0,z1),(x1,y1,z1),(x0,y1,z0)],'Concrete')
    for side in (-1,1):
        x0,x1=(.16,23.65) if side>0 else (-23.65,-.16)
        for yi in range(7):
            y=(yi-3)*3.048
            beam=girder(name+'__Girder_%s_%s'%(side,yi),x1-x0);beam.parent=rt;beam.location=((x0+x1)/2,y,gb)
            for x in (side*.65,side*23.6):
                camber=.018*math.sin(math.pi*(x-x0)/(x1-x0))
                b.box((x,y,gb-.075+camber/2),(.68,.58,.15+camber),'Rubber')
                b.box((x,y,gb-.16),(.78,.68,.02),'Steel')
        for x in (side*1.55,side*22.7):
            # End diaphragms between webs, above bearing/seat level.
            for j in range(6):b.box((x,(j-2.5)*3.048,6.42),(.22,2.8448,.90),'Bridge')
    # Deck segments have real top crown and thickened sidewalk strips.
    for j in range(24):
        xa=-24+j*2;xb=xa+2
        for ya,yb in [(-10.668,-8.382),(-8.382,0),(0,8.382),(8.382,10.668)]:
            z0=BRIDGE_Z-.02*min(abs(ya),8.382);z1=BRIDGE_Z-.02*min(abs(yb),8.382)
            b.face([(xa,ya,z0),(xb,ya,z0),(xb,yb,z1),(xa,yb,z1)],'Asphalt' if abs(ya+yb)<16.7 else 'Concrete')
            b.face([(xa,yb,deck_bottom),(xb,yb,deck_bottom),(xb,ya,deck_bottom),(xa,ya,deck_bottom)],'Bridge')
    for side in (-1,1):
        # Pedestrian walk, F parapet, 8 ft safety fence on outer rail.
        base=BRIDGE_Z-.02*8.382
        inner=side*8.6868;outer=side*10.5918
        b.extrude([(inner+u,base+v) for u,v in F_SHAPE],[-24,24],'Barrier',axis='X')
        b.box((0,outer,base+.30),(48,.1524,.60),'Bridge')
        for x in range(-24,25,2):b.tube([(x,outer,base+.59),(x,outer,base+2.44)],.025,'Steel',8)
        for h in (base+.60,base+1.52,base+2.44):b.tube([(-24,outer,h),(24,outer,h)],.020,'Steel',6)
        # Safety fence diamond wire at 150 mm spacing; construction checkpoint
        # uses coarse wires. Final will reuse chain-link alpha instead.
        for x in [i*.30-24 for i in range(161)]:
            for dx in (-1.8,1.8):
                end=min(24,max(-24,x+dx))
                if abs(end-x)<.01:continue
                b.tube([(x,outer,base+.60),(end,outer,base+.60+abs(end-x)/1.8*1.84)],.003,'DarkSteel',3)
        # Scupper throat, vertical drain and outlet, attached to the fascia.
        for x in (-16,16):
            b.box((x,side*8.40,7.18),(.40,.22,.09),'Drain')
            b.tube([(x,side*8.55,7.18),(x,side*8.86,6.95),(x,side*8.86,5.75),(x+.7,side*8.86,5.5)],.075,'DarkSteel',8)
    # Approach slabs, exposed joints, wall thickness at fascia.
    for s in (-1,1):
        b.box((s*27,0,7.15),(6.,21.336,.24),'Bridge')
        b.box((s*24.05,0,7.325),(.05,20.8,.05),'Joint')
        for side in (-1,1):b.box((0,side*10.668,7.10),(48,.08,.42),'Bridge')
    b.finish()
    for label,x in [('W',-30),('E',30)]:Q.socket(rt,label,(x,0,7.35)).rotation_euler.z=-math.pi/2
    Q.socket(rt,'PierBearing',(0,0,seat),'bearing_top');return rt

def library():
    return [barrier(),guardrail(),guardrail('GuardrailEnd',7.62,True),cable(),wall(),
            truss(),truss('Cantilever',18,True),light(),attenuator(),bridge(),girder(),pier(),gore()]
