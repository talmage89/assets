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
    from fascia import details
    details(b)
    for sign,side in [(-1,'L'),(1,'R')]:
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
        # Tapered aerodynamic cap, separate black glass case and inset bezel.
        center=sign*1.11936;loops=[]
        sections=[(-1.385,.050,.090),(-1.372,.110,.166),(-1.345,.183,.227),(-1.285,.225,.262),(-1.211,.220,.267),(-1.197,.217,.264),(-1.140,.201,.249)]
        for y,w,h in sections:
            offset=sign*(-.022 if y< -1.34 else -.007 if y< -1.28 else 0)
            loops.append([(center+offset+u,y,1.497+v) for u,v in G.rounded_rectangle(w,h,min(.036,w*.45,h*.45),6 if b.high else 3)])
        housing=G.smooth(G.loft('Molded mirror shell_'+side,loops,b.m['bumper']))
        housing.data.materials.append(b.m['body'])
        for face in housing.data.polygons:
            # The painted cap stops short of the black gasket/glass case.
            if face.index<4*len(loops[0]):face.material_index=1
        b.add(housing,fold,'mirrors');housing['bounds_exclude']=True;housing['housing_sections']=len(loops);housing['section_vertices']=len(loops[0]);G.smooth(housing,65)
        arm=tube(b,'Mirror support arm_'+side,[(sign*1.033,-1.230,1.431),(sign*1.079,-1.217,1.409),(sign*1.117,-1.200,1.414)],.024,b.m['plastic'],'mirrors',fold,sides=8);arm['bounds_exclude']=True
        # Bezel has a real rounded aperture and a short return to the glass.
        paths=[]
        for w,h,y in [(.202,.250,-1.138),(.183,.231,-1.132),(.180,.228,-1.136)]:
            paths.append([(center+u,y,1.497+v) for u,v in G.rounded_rectangle(w,h,.026,5 if b.high else 3)])
        bezel=G.loft('Mirror glass bezel_'+side,paths,b.m['plastic'],caps=False)
        gauge=bezel.modifiers.new('Bezel gauge','SOLIDIFY');gauge.thickness=.0015;gauge.use_even_offset=False
        b.add(bezel,fold,'mirrors');bezel['bounds_exclude']=True
        outline=[(center+u,1.497+v) for u,v in G.rounded_rectangle(.179,.227,.025,5 if b.high else 3)]
        glass=G.profile('Mirror glass_'+side,outline,-1.135,-1.133,b.m['mirror'],axis='Y');b.add(glass,fold,'mirrors');glass['bounds_exclude']=True
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
