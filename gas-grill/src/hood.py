"""Pressed porcelain shell, contoured cast end caps, overlapping lip and fork hinges."""
import math
import bpy
from mathutils import Vector
from kit import model as G


def smoothstep(x):
    t=max(0,min(1,x));return t*t*(3-2*t)


def hood_profile(high):
    count=30 if high else 8
    profile=G.bezier((-.255,.895),(-.253,.948),(-.131,1.091),(-.074,1.121),count)
    profile+=G.bezier((-.074,1.121),(-.029,1.134),(.149,1.134),(.205,1.123),count)[1:]
    profile+=G.bezier((.205,1.123),(.261,1.116),(.277,1.042),(.276,.901),count)[1:]
    crown=max(z for _,z in profile)
    return [(y,.895+(z-.895)*(1.1294-.895)/(crown-.895)) for y,z in profile]


def build_hood(b):
    hinge=(0,.266,.902)
    lid=G.pivot('Lid',hinge,'X',[-104,0]);lid.parent=b.root
    profile=hood_profile(b.high);normals=[]
    for i,p in enumerate(profile):
        dy,dz=Vector(profile[min(i+1,len(profile)-1)])-Vector(profile[max(0,i-1)])
        length=math.hypot(dy,dz);normals.append((-dz/length,dy/length))
    # A 2D skin with shallow transverse crown and a pressed, radiused panel recess.
    # It is authored from manufacturing geometry, never extracted from a photo.
    xs=48 if b.high else 8
    loops=[]
    arc=0
    for j,(y,z) in enumerate(profile):
        if j:arc+=math.dist(profile[j-1],profile[j])
        row=[]
        for i in range(xs+1):
            x=-.305+i/xs*.610
            crown=.0009*(1-(x/.305)**2)
            # Rounded rectangle signed distance in developed shell coordinates.
            qx=abs(x)-.245+.018;qy=abs(arc-.147)-.071+.018
            sd=math.hypot(max(qx,0),max(qy,0))+min(max(qx,qy),0)-.018
            recess=-.00095*smoothstep(-sd/.005) if b.high and arc<.27 else 0
            offset=crown+recess
            ny,nz=normals[j];row.append((x,y+ny*offset,z+nz*offset))
        loops.append(row)
    shell=G.loft('Pressed porcelain shell',loops,b.mat('enamel'),caps=False,closed=False)
    shell.data.materials.append(b.mat('inside'))
    mod=shell.modifiers.new('1.8 mm enamel steel shell','SOLIDIFY')
    mod.thickness=.0018;mod.offset=-1;mod.material_offset=1;mod.material_offset_rim=1
    G.smooth(shell,36);b.add(shell,lid)
    # Cast caps wrap the edges with a rolled flange and a convex face/rim transition.
    outline=profile+[(.276,.884),(-.255,.884)]
    cy,cz=.026,1.006
    for sign in (-1,1):
        rings=[]
        for scale,x in [(1,.307),(1,.316),(.995,.327),(.976,.334),(.86,.334),(.30,.337),(.015,.337)]:
            rings.append([(sign*x,cy+(y-cy)*scale,cz+(z-cz)*scale) for y,z in outline])
        cap=G.loft('Contoured cast hood end cap',rings,b.mat('casting'))
        G.smooth(cap,34);cap.data.materials.append(b.mat('inside'))
        cap.data.polygons[-2].material_index=1
        G.bevel(cap,.0005,b.edges);b.add(cap,lid)
        # Visible enamel/casting reveal and the overlapping skirt.
        seam=[(sign*.3064,y,z) for y,z in profile]
        b.tube('Porcelain to cap reveal',seam,.0007,'rubber',6 if b.high else 4,lid)
        b.box('Cast cap overlapping lower skirt',(sign*.323,.011,.889),(.025,.514,.009),'casting',.002,lid)
        b.fastener('End cap rear screw',(sign*.339,.215,.928),(sign,0,0),radius=.0035,kind='cross',parent=lid,washer=False)
        # Fixed fork: two stamped steel ears straddle a moving cast hinge lug.
        ear=[(.237,.872),(.289,.872),(.289,.913),(.276,.929),(.255,.929),(.237,.911)]
        for x in (sign*.303,sign*.340):
            bracket=G.profile('Rear fork hinge bracket',ear,x-.002,x+.002,b.mat('powder'))
            if b.high:
                cut=G.cylinder('Hinge bore cutter',(x-.010,.266,.902),(x+.010,.266,.902),.0046,None,24)
                G.boolean(bracket,cut)
            G.bevel(bracket,.001,b.edges);b.add(bracket)
            b.fastener('Hinge bracket anchor',(x,.252,.883),(sign,0,0),radius=.004)
        b.lathe('Moving cast hinge lug',[(sign*.312,.0048),(sign*.312,.014),
                (sign*.331,.014),(sign*.331,.0048)],'casting',40 if b.high else 16,
                axis='X',center=(.266,.902),closed=True,parent=lid)
        b.cylinder('Hinge shoulder pin',(sign*.296,.266,.902),(sign*.347,.266,.902),.0045,'stainless',24 if b.high else 12)
        b.fastener('Hinge pin retaining head',(sign*.347,.266,.902),(sign,0,0),radius=.006,kind='socket',washer=False)
        b.box('Hinge opening stop',(sign*.323,.286,.912),(.021,.008,.016),'powder',.001)
    # Real front lip rolls over the firebox edge; back gap vents combustion gases.
    b.box('Enamel rolled front lower hem',(0,-.255,.897),(.610,.006,.006),'enamel',.002,lid)
    b.box('Rear lid vent folded lip',(0,.276,.904),(.602,.005,.009),'enamel',.0015,lid)
    for x in (-.257,.257):
        inside=G.offset_profile(profile[5:-5],-.007)
        b.tube('Lid interior pressed stiffener',[(x,y,z) for y,z in inside],.002,'inside',8 if b.high else 5,lid)
    if b.high:
        # Shallow black carbon flakes in the most heat-exposed rear inner strip.
        # Large visible flakes have geometry; the fine crack network is in shader height.
        for i in range(3):
            x=-.208+(i*.163)% .43
            j=38+(i*7)%36;y,z=profile[j];ny,nz=normals[j]
            y-=ny*.0035;z-=nz*.0035
            points=[(x-.0015,y-.001,z),(x+.001,y-.0015,z+.0005),(x+.002,y+.0005,z+.0003),(x-.001,y+.0015,z)]
            flake=G.mesh('Carbon flake lifted edge',points,[(0,1,2,3)],b.mat('soot'))
            flake['allow_boundary']=True;b.add(flake,lid)
    build_handle(b,lid,profile)
    build_badge_and_thermometer(b,lid,profile)
    return lid


def mount_at(profile,fraction):
    # Match to the high-detail analytic profile for identical positions at both qualities.
    points=hood_profile(True);index=round(fraction*30)
    y,z=points[index]
    dy,dz=Vector(points[index+1])-Vector(points[index-1])
    return y-.001,z,-math.atan2(dy,dz)


def build_handle(b,lid,profile):
    controls=((- .238,-.328,.958),(-.19,-.4024,.958),(.19,-.4024,.958),(.238,-.328,.958))
    for x in (-.238,.238):
        y,z,angle=mount_at(profile,.24)
        # Broad molded heat-resistant mounting feet with visible recessed screws.
        foot=G.box('Handle mounting saddle',(x,y-.002,z),(.033,.014,.031),b.mat('plastic'),.005,b.edges)
        foot.rotation_euler.x=angle;b.add(foot,lid)
        b.tube('Handle cast standoff',G.bezier((x,y-.007,z),(x,-.277,.962),(x,-.299,.958),(x,-.329,.958),14 if b.high else 5),
               .008,'casting',16 if b.high else 8,lid)
        b.fastener('Handle saddle socket screw',(x,y-.012,z+.007),(0,-1,.15),radius=.0035,kind='socket',parent=lid,washer=False)
    def point(t):
        p,q,r,s=controls
        return tuple((1-t)**3*p[k]+3*(1-t)**2*t*q[k]+3*(1-t)*t*t*r[k]+t**3*s[k] for k in range(3))
    b.tube('Handle stainless tube',G.bezier(*controls,40 if b.high else 16),.0088,'chrome',16 if b.high else 8,lid)
    count=40 if b.high else 14
    grip=[point(.14+.72*i/count) for i in range(count+1)]
    b.tube('Handle molded insulating grip',grip,.012,'handle',20 if b.high else 8,lid)
    for t in (.14,.86):
        center=point(t);b.cylinder('Grip molded collar',(center[0]-.001,center[1],center[2]),(center[0]+.001,center[1],center[2]),.0126,'plastic',24 if b.high else 10,lid)
    if b.high:
        for k in range(23):
            t=.22+k*.025
            x,y,z=point(t)
            b.tube('Grip underside mold texture',[(x,y-.007,z-.009),(x,y+.003,z-.011),(x,y+.008,z-.007)],.00025,'plastic',5,lid)


def build_badge_and_thermometer(b,lid,profile):
    # A solid enamel badge, restrained thickness, fictional lettering.
    badge=G.pivot('Hood badge',(0,0,0))
    b.box('Badge stamped backing',(0,0,0),(.142,.0014,.035),'stainless',.003,badge)
    b.add(G.plane_uv('Original maker badge',[(-.068,-.0009,-.014),(.068,-.0009,-.014),(.068,-.0009,.014),(-.068,-.0009,.014)],b.mat('badge_print')),badge)
    y,z,angle=mount_at(profile,.67);badge.location=(-.16,y,z);badge.rotation_euler.x=angle
    bpy.context.view_layer.update();world=badge.matrix_world.copy();badge.parent=lid;badge.matrix_world=world
    gauge=G.pivot('Thermometer',(0,0,0))
    b.lathe('Thermometer rolled bezel',[(0,.021),(.001,.026),(.004,.027),(.007,.026),(.008,.024),(.007,.022)],
            'chrome',80 if b.high else 24,closed=True,parent=gauge)
    disk=G.lathe('Thermometer dial',[(.003,0),(.003,.0223),(.0035,.0223),(.0035,0)],b.mat('dial_print'),64 if b.high else 24)
    uv=disk.data.uv_layers.new(name='PrintUV')
    for p in disk.data.polygons:
        for li in p.loop_indices:
            co=disk.data.vertices[disk.data.loops[li].vertex_index].co;uv.data[li].uv=(co.x/.0446+.5,co.y/.0446+.5)
    b.add(disk,gauge)
    b.profile('Thermometer needle',[(-.0006,-.003),(.0006,-.003),(.0003,.017),(-.0003,.017)],.004,.0045,'red',axis='Z',radius=0,parent=gauge)
    b.cylinder('Needle pivot',(0,0,.0042),(0,0,.0049),.0017,'chrome',12,gauge)
    y,z,angle=mount_at(profile,.88);gauge.location=(.075,y,z);gauge.rotation_euler.x=angle+math.pi/2
    bpy.context.view_layer.update();world=gauge.matrix_world.copy();gauge.parent=lid;gauge.matrix_world=world
