"""Original Alder lighting, grille, trim and bed hardware, in vehicle meters."""
import math
import bpy
from mathutils import Vector
from kit import model as G
from kit.vehicle import samples
import pickup_spec as S
from forms import side_x,nose_y,lamp_surface,windshield,fair,hood_z
from detail_helpers import box,tube,loop,pivot,print_quad


def build(b):
    # The existing shared seat is the protective clear lens, not an outboard box.
    for sign,side in [(-1,'L'),(1,'R')]:
        def back(u,v,sign=sign):
            p=Vector(lamp_surface(u,v));du=Vector(lamp_surface(u+1e-4,v))-Vector(lamp_surface(u-1e-4,v));dv=Vector((0,0,1));normal=du.cross(dv).normalized()
            p-=normal*.075
            return sign*p.x,p.y,p.z
        b.skin('Headlamp housing back_'+side,back,20,6,b.m['plastic'],(sign,-1,0),category='lamps',gauge=.002,return_depth=.020)
        for number,z in enumerate([.972,1.096]):
            x=sign*.817;yf=nose_y(x,z)+.018;yb=yf+.048
            cup=G.lathe('Headlamp reflector_'+side+str(number),[(yb,.014),(yb,.026),(yf,.050),(yf,.049),(yb+.001,.014)],b.m['chrome'],32 if b.high else 20,axis='Y',center=(x,z),closed=True)
            b.add(cup,category='lamps')
            lens=G.lathe('Projector optic_'+side+str(number),[(yf-.004,0),(yf-.001,.033),(yf+.004,.038),(yf+.010,.033),(yf+.013,0)],b.m['lens'],32 if b.high else 20,axis='Y',center=(x,z))
            b.add(lens,category='lamps')
            emitter=G.lathe('Projector emitter_'+side+str(number),[(yb-.004,0),(yb-.004,.018),(yb,.018),(yb,0)],b.m['headlight'],16,axis='Y',center=(x,z))
            b.add(emitter,category='lamps')
        # One angular running-light signature, wrapping with the lens seat.
        uv=[(.06,.91),(.50,.91),(.87,.91),(.93,.87),(.94,.24),(.91,.18),(.61,.18)]
        path=[]
        for a,c in zip(uv,uv[1:]):
            for t in samples(3)[:-1]:
                u,v=[a[k]+(c[k]-a[k])*t for k in range(2)];x,y,z=lamp_surface(u,v)
                path.append((sign*(x-.005),y+.006,z))
        x,y,z=lamp_surface(*uv[-1]);path.append((sign*(x-.005),y+.006,z))
        tube(b,'Alder running signature_'+side,path,.0042,b.m['drl'],'lamps',sides=6)
        # The side marker is inside the wrap, behind the same protective lens.
        x,y,z=lamp_surface(.89,.46)
        box(b,'Amber side marker_'+side,(sign*(x-.004),y+.005,z),(.010,.035,.070),b.m['amber'],'lamps',radius=.006)
        # Replace the rear block with a housing, curved red optic and internal strip.
        old=bpy.data.objects.get('Taillamp envelope_'+side)
        if old:bpy.data.objects.remove(old,do_unlink=True)
        x=sign*.922
        box(b,'Taillamp housing_'+side,(x,2.830,1.181),(.133,.066,.415),b.m['plastic'],'lamps',radius=.018)
        loops=[]
        for y,w,h in [(2.853,.116,.397),(2.871,.115,.391),(2.875,.102,.377)]:
            loops.append([(x+u,y,1.181+v) for u,v in G.rounded_rectangle(w,h,.017,5 if b.high else 3)])
        lens=G.loft('Taillamp red lens_'+side,loops,b.m['red_lens']);b.add(lens,category='lamps')
        box(b,'Rear lamp reverse optic_'+side,(x,2.879,1.143),(.094,.008,.055),b.m['lens'],'lamps',radius=.006)
        for zz in [1.025,1.265]:
            box(b,'Rear LED rail_'+side+str(zz),(x,2.862,zz),(.079,.006,.073),b.m['brakelight'],'lamps',radius=.007)
        # Tall molded housing on a substantial door sail, with an actual rear lens.
        door=bpy.data.objects['Door_F'+side]
        sail=G.profile('Mirror sail_'+side,[(-1.354,1.390),(-1.13,1.39),(-1.14,1.54),(-1.25,1.51)],sign*.959,sign*1.066,b.m['plastic'],axis='X',radius=.004)
        b.add(sail,door,'mirrors');sail['bounds_exclude']=True
        fold=pivot(b,'Mirror_'+side,(sign*1.041,-1.225,1.461),door,'Z',(-65,0) if sign<0 else (0,65))
        center=sign*1.11936;loops=[]
        for y,w,h in [(-1.337,.050,.095),(-1.329,.110,.183),(-1.313,.166,.246),(-1.283,.210,.290),(-1.205,.220,.300),(-1.137,.203,.277)]:
            loops.append([(center+u,y,1.495+v) for u,v in G.rounded_rectangle(w,h,min(.038,w*.45,h*.45),6 if b.high else 3)])
        housing=G.smooth(G.loft('Molded mirror shell_'+side,loops,b.m['bumper']));b.add(housing,fold,'mirrors');housing['bounds_exclude']=True;housing['housing_sections']=len(loops);housing['section_vertices']=len(loops[0]);G.smooth(housing,65)
        def mirror(u,v,center=center):
            s,t=2*u-1,2*v-1
            return center+.086*s,-1.133+.002*(1-s*s-t*t),1.495+.117*t
        ob=b.skin('Mirror glass_'+side,mirror,8,8,b.m['mirror'],(0,1,0),fold,'mirrors',gauge=.002,return_depth=.002);ob['bounds_exclude']=True
        # Handles belong to their doors; A bowed stand-off leaves a real grip gap.
        for end,y in [('F',-.287),('R',.704)]:
            door=bpy.data.objects['Door_'+end+side];z=1.270;x=side_x(y,z)
            back=box(b,'Handle pocket_'+end+side,(sign*(x+.003),y,z),(.006,.178,.061),b.m['plastic'],'trim',door,.021)
            pts=[(sign*(side_x(y+dy,z)+off),y+dy,z+.006) for dy,off in [(-.072,.010),(-.056,.023),(0,.027),(.056,.023),(.072,.010)]]
            tube(b,'Pull handle_'+end+side,pts,.0105,b.m['body'],'trim',door,sides=8)
        # Small original model applique on the rear of the front fender.
        y=-1.620;z=1.292;x=side_x(y,z)+.0015
        box(b,'C150 badge backing_'+side,(sign*x,y,z),(.004,.190,.043),b.m['chrome'],'trim',radius=.004)
        xx=sign*(x+.0025)
        ys=[y-sign*.091,y+sign*.091]
        print_quad(b,'C150 fictional badge_'+side,[(xx,ys[0],z-.018),(xx,ys[1],z-.018),(xx,ys[1],z+.018),(xx,ys[0],z+.018)],b.m['model'])
        # Bed tie-downs are forged loops supported on the actual inner wall.
        for y in [1.235,2.635]:
            box(b,'Tie-down bracket_'+side+str(y),(sign*.825,y,1.156),(.010,.064,.075),b.m['frame'],'bed_hardware',radius=.002)
            loop(b,'Bed tie-down_'+side+str(y),(sign*.800,y,1.156),(1,0,0),(0,0,1),(.024,.029),.0045,b.m['chrome'],'bed_hardware',segments=12,sides=6)
        box(b,'Rear step pad_'+side,(sign*.602,2.827,.840),(.530,.114,.012),b.m['rubber'],'bed_hardware',radius=.009)
    # Fuel flap follows the stamped flank and has its own forward hinge.
    y,z=1.222,1.192;flap=pivot(b,'Fuel_Door',(-.980,y-.074,z),axis='Z',limits=(0,95))
    outline=[(y+.076*math.cos(t),z+.076*math.sin(t)) for t in [i*math.tau/28 for i in range(28)]]
    plate=G.profile('Fuel flap',outline,0,.002,b.m['body'],axis='X')
    for v in plate.data.vertices:v.co.x=-(side_x(v.co.y,v.co.z)+.0013+v.co.x)
    for face in plate.data.polygons:face.flip()
    b.add(plate,flap,'trim')
    # Original two-wing grille. Fine repeating perforations stay shader relief.
    grille=bpy.data.objects['Grille form surround'];grille.data.materials[0]=b.m['chrome']
    old=bpy.data.objects.get('Grille envelope')
    if old:bpy.data.objects.remove(old,do_unlink=True)
    print_quad(b,'Alder grille perforation field',[(-.654,-2.832,.863),(.654,-2.832,.863),(.654,-2.800,1.153),(-.654,-2.800,1.153)],b.m['grille'])
    box(b,'Grille cavity',(0,-2.801,1.008),(1.31,.018,.302),b.m['frame'],'grille',radius=.006)
    for number,z in enumerate([.928,1.099]):
        loops=[]
        for x in [-.635,-.48,0,.48,.635]:
            y=nose_y(x,z)-.012;zz=z+(.014 if number==0 else -.014)*(1-abs(x)/.635)
            loops.append([(x,y+dy,zz+dz) for dy,dz in [(0,-.007),(0,.007),(.012,.007),(.012,-.007)]])
        b.add(G.loft('Alder grille wing_'+str(number),loops,b.m['chrome']),category='grille')
    box(b,'Alder grille badge',(0,-2.856,1.016),(.253,.018,.064),b.m['plastic'],'grille',radius=.009)
    print_quad(b,'Alder front badge',[(-.117,-2.866,.994),(.117,-2.866,.994),(.117,-2.866,1.038),(-.117,-2.866,1.038)],b.m['badge'],'grille')
    # Real US-size plate carriers. The rear carrier sits inside the bumper opening.
    for end,sgn,y,z in [('F',-1,-2.928,.686),('R',1,2.869,.710)]:
        box(b,'Plate recess surround_'+end,(0,y-sgn*.012,z),(.337,.027,.178),b.m['plastic'],'trim',radius=.010)
        box(b,'Plate blank_'+end,(0,y,z),(.305,.002,.1524),b.m['wheel'],'trim',radius=.003)
        corners=[(-.150,y+sgn*.0015,z-.074),(.150,y+sgn*.0015,z-.074),(.150,y+sgn*.0015,z+.074),(-.150,y+sgn*.0015,z+.074)]
        if sgn>0:corners=[corners[i] for i in [1,0,3,2]]
        print_quad(b,'Fictional plate_'+end,corners,b.m['plate'])
    for sign in [-1,1]:
        # Forged horizontal recovery loops, supported by the front crossmember.
        loop(b,'Front tow hook_'+str(sign),(sign*.486,-2.877,.590),(1,0,0),(0,1,0),(.039,.055),.008,b.m['frame'],'trim',segments=16,sides=6)
        box(b,'Tow hook bracket_'+str(sign),(sign*.486,-2.796,.590),(.065,.104,.040),b.m['frame'],'trim',radius=.003)
    # Parked wipers lie against points on our windshield, with hinge normals.
    for i,(lo,hi) in enumerate([(.055,.465),(.515,.93)]):
        pts=[]
        for t in samples(6):
            p=Vector(windshield(lo+(hi-lo)*t,.065));p+=Vector((0,-.003,.004));pts.append(tuple(p))
        base=Vector(windshield((lo+hi)/2+.10,0))+Vector((0,-.008,.013))
        root=pivot(b,'Wiper_'+str(i),base,axis='Z',limits=(0,80));root.rotation_euler=Vector((0,-.62,.78)).to_track_quat('Z','Y').to_euler()
        tube(b,'Wiper rubber_'+str(i),pts,.0035,b.m['rubber'],'trim',root,sides=6)
        tube(b,'Wiper spring back_'+str(i),[(x,y-.003,z+.005) for x,y,z in pts],.004,b.m['frame'],'trim',root,sides=6)
        middle=Vector(pts[3])+Vector((0,-.004,.012))
        tube(b,'Wiper arm_'+str(i),[tuple(base),tuple((base+middle)/2+Vector((0,-.016,.012))),tuple(middle)],.0055,b.m['frame'],'trim',root,sides=6)
    # Rear handle, raised original badge and upper brake light.
    gate=bpy.data.objects['Tailgate']
    box(b,'Tailgate handle pocket',(0,2.852,1.350),(.235,.025,.071),b.m['plastic'],'bed_hardware',gate,.013)
    tube(b,'Tailgate pull',[(-.079,2.866,1.352),(-.060,2.878,1.352),(.060,2.878,1.352),(.079,2.866,1.352)],.007,b.m['bumper'],'bed_hardware',gate,sides=6)
    box(b,'Tailgate Alder backing',(0,2.839,1.165),(.275,.007,.067),b.m['chrome'],'trim',gate,.006)
    print_quad(b,'Tailgate Alder name',[(.129,2.843,1.141),(-.129,2.843,1.141),(-.129,2.843,1.189),(.129,2.843,1.189)],b.m['badge'],'trim',gate)
    box(b,'Upper brake housing',(0,.996,1.859),(.270,.027,.046),b.m['plastic'],'lamps',radius=.010)
    box(b,'Upper brake lens',(0,1.011,1.859),(.243,.006,.029),b.m['red_lens'],'lamps',radius=.008)
    box(b,'Upper brake LED',(0,1.008,1.859),(.187,.003,.017),b.m['brakelight'],'lamps',radius=.004)
    # Welded 2-inch receiver tube, with open bore and safety-chain eyes.
    for label,center,size in [('top',(0,2.811,.493),(.063,.224,.006)),('bottom',(0,2.811,.436),(.063,.224,.006)),
                              ('left',(-.0285,2.811,.4645),(.006,.224,.051)),('right',(.0285,2.811,.4645),(.006,.224,.051))]:
        box(b,'Receiver '+label,center,size,b.m['frame'],'bed_hardware',radius=.0005)
    box(b,'Hitch cross tube',(0,2.690,.514),(1.16,.075,.075),b.m['frame'],'bed_hardware',radius=.003)
    for sign in [-1,1]:loop(b,'Safety chain eye_'+str(sign),(sign*.079,2.792,.449),(1,0,0),(0,1,0),(.023,.041),.006,b.m['frame'],'bed_hardware',segments=12,sides=6)
