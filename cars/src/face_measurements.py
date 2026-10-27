"""Independent vertex/surface measurements of the source front checkpoint.

No shape controls are returned as measurements. Optical width means the front
projection; developed length includes the additional wrap onto the fender.
"""
import math
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def points(ob):return [ob.matrix_world@v.co for v in ob.data.vertices]
def tree(names):
    ps=[];fs=[]
    for name in names:
        ob=bpy.data.objects[name];offset=len(ps);ps+=points(ob)
        fs += [tuple(offset+i for i in f.vertices) for f in ob.data.polygons]
    return BVHTree.FromPolygons(ps,fs)


def collect():
    errors=[];frame=tree(['Fascia shared frame']);fp=points(bpy.data.objects['Fascia shared frame'])
    def hit(x,z):return frame.ray_cast(Vector((x,-4,z)),Vector((0,1,0)),4)[0]
    def transition(a,c,z=None,x=None):
        initial=hit(a,z) is not None if z is not None else hit(x,a) is not None
        for _ in range(35):
            m=(a+c)/2;state=hit(m,z) is not None if z is not None else hit(x,m) is not None
            if state==initial:a=m
            else:c=m
        return (a+c)/2
    lo=hit(0,.825);hi=hit(0,1.275)
    slope=(hi.y-lo.y)/(hi.z-lo.z)
    rake=math.degrees(math.atan(slope))
    def baseline(z):return lo.y+slope*(z-lo.z)
    widths=[]
    for z in [.940,1.05,1.16]:
        inner=transition(.40,.55,z=z);outer=transition(.55,.64,z=z)
        qs=[hit(inner+.0001+(outer-inner-.0002)*j/80,z) for j in range(81)]
        widths.append(sum((c-a).length for a,c in zip(qs,qs[1:]) if a is not None and c is not None))
    top=transition(1.26,1.34,x=0);itop=transition(1.20,1.26,x=0)
    bottom=transition(.76,.82,x=0);ibottom=transition(.83,.90,x=0)
    lands=dict(top_m=top-itop,bottom_m=ibottom-bottom,side_surface_widths_m=widths)
    rear=frame.ray_cast(Vector((0,-2,1.275)),Vector((0,-1,0)),2)[0]
    section=rear.y-hi.y
    nose=tree(['Fascia body lower_R'])
    corner=nose.ray_cast(Vector((.950,-4,1.02)),Vector((0,1,0)),4)[0]
    sweep=corner.y-baseline(corner.z)
    lamps=[]
    for sign in [-1,1]:
        ob=bpy.data.objects['Headlamp envelope_'+str(sign)];ps=points(ob)[:ob['sheet_vertex_count']]
        nu=sorted(ob.data.polygons[0].vertices)[2]
        rows=[ps[i:i+nu] for i in range(0,len(ps),nu)]
        centers=[(rows[0][i]+rows[-1][i])/2 for i in range(nu)]
        inboard_heights=[rows[-1][i].z-rows[0][i].z for i in range(max(3,nu//4))]
        j=min(range(nu),key=lambda i:abs(abs(centers[i].x)-.950) if i<nu*.80 else 9)
        # Nearest vertex to the front/return tangent, then the aft-most edge.
        front=centers[j];end=centers[-1]
        row=dict(side=sign,front_projected_width_m=max(p.x for p in ps)-min(p.x for p in ps),
                 inboard_height_m=max(inboard_heights),outboard_edge_height_m=rows[-1][-1].z-rows[0][-1].z,
                 developed_centerline_length_m=sum((c-a).length for a,c in zip(centers,centers[1:])),
                 front_corner_point_m=list(front),wrap_end_point_m=list(end),
                 corner_return_fore_aft_m=end.y-front.y,corner_return_centerline_m=sum((c-a).length for a,c in zip(centers[j:],centers[j+1:])))
        lamps.append(row)
        if not .380<=row['front_projected_width_m']<=.450:errors.append('Lamp front width '+str(sign))
        if not .130<=row['inboard_height_m']<=.160:errors.append('Lamp inboard height '+str(sign))
        if not .150<=row['corner_return_fore_aft_m']<=.200:errors.append('Lamp wrap '+str(sign))
    recess=[]
    supports=[]
    for k in range(4):
        ob=bpy.data.objects['Alder grille lamella_'+str(k)];ps=points(ob)
        # Actual section has rear depth too; select the first face edge on
        # each station, then compare against the surround plane plus its crown.
        ds=[p.y-baseline(p.z) for i,p in enumerate(ps) if i%4 in [0,1] and abs(p.x)<.01]
        recess.append(dict(part=ob.name,front_recess_min_m=min(ds),front_recess_max_m=max(ds)))
        if not .060<=min(ds)<=.100:errors.append('Grille recess '+ob.name)
        for sign in [-1,1]:
            mount='Grille end mount_'+str(sign);cross=len(tree([mount]).overlap(tree([ob.name])))
            supports.append(dict(parts=[mount,ob.name],crossing_triangle_pairs=cross))
            if not cross:errors.append('Grille blade support '+ob.name+' / '+mount)
    for sign in [-1,1]:
        mount='Grille end mount_'+str(sign);cross=len(tree([mount]).overlap(frame))
        supports.append(dict(parts=[mount,'Fascia shared frame'],crossing_triangle_pairs=cross))
        if not cross:errors.append('Grille rail support '+mount)
        side='left' if sign<0 else 'right'
        connections=[('Front bumper beam bracket_'+str(sign),'Front crash beam'),
                     ('Front bumper beam bracket_'+str(sign),'Front bumper '+side),
                     ('Tow hook bracket_'+str(sign),'Front crash mount '+str(sign)),
                     ('Front tow hook_'+str(sign),'Tow hook bracket_'+str(sign))]
        for one,two in connections:
            cross=len(tree([one]).overlap(tree([two])))
            supports.append(dict(parts=[one,two],crossing_triangle_pairs=cross))
            if not cross:errors.append('Front assembly support '+one+' / '+two)
    hood=bpy.data.objects['Hood outer'];hp=points(hood)[:hood['sheet_vertex_count']]
    nu=sorted(hood.data.polygons[0].vertices)[2];front=hp[:nu]
    brow=tree(['Fascia shared frame','Fascia body upper_R','Fascia body upper_L'])
    gaps=[brow.find_nearest(p)[3] for p in front]
    hood_gap=dict(samples=len(gaps),min_m=min(gaps),max_m=max(gaps),leading_edge_height_range_m=max(p.z for p in front)-min(p.z for p in front))
    if min(gaps)<.003 or max(gaps)>.008:errors.append('Hood/front reveal')
    if hood_gap['leading_edge_height_range_m']>.0001:errors.append('Hood leading-edge height')
    bumper=[p for name in ['Front bumper left','Front bumper right','Front bumper upper','Front bumper lower'] for p in points(bpy.data.objects[name])]
    bh=max(p.z for p in bumper)-min(p.z for p in bumper)
    gw=max(p.x for p in fp)-min(p.x for p in fp)
    facewidth=2*max(abs(p.x) for p in bumper)
    if not 6<=rake<=10:errors.append('Face rake')
    if not .100<=sweep<=.140:errors.append('Face sweep')
    if not .060<=lands['top_m']<=.080 or not .060<=lands['bottom_m']<=.080:errors.append('Surround top/bottom lands')
    if not all(.060<=w<=.080 for w in widths):errors.append('Surround side land')
    if not .060<=section<=.105:errors.append('Surround section')
    if not .58<=gw/facewidth<=.64:errors.append('Grille/face width')
    if not .220<=bh<=.280:errors.append('Bumper height')
    return dict(method='actual outer-sheet vertex rows, BVH rays, arc sums and triangle intersections; source construction only',
                face_sweep_m=sweep,face_sweep_at_x_m=corner.x,face_rake_degrees=rake,
                grille_width_m=gw,face_width_m=facewidth,grille_width_fraction=gw/facewidth,
                frame_land_widths=lands,frame_section_depth_m=section,bumper_height_m=bh,
                lamp_dimensions=lamps,grille_recess=recess,hood_shutline=hood_gap,support_intersections=supports,
                passed=not errors,errors=errors)
