"""One continuous, supported Catmull-Clark body cage, split AFTER evaluation.

The same cage spans nose, hood, fenders, doors, greenhouse and deck. Transverse
sections sculpt the crown/tumblehome/tuck; longitudinal supports control roof
acceleration, shoulder, fascia and deck lip. Material/part boundaries do not
interrupt subdivision. Evaluated patches retain the master's corner normals.
References are never opened by the modeling process.
"""
import math,json
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
from mathutils.geometry import barycentric_transform
from kit import model as G
import sedan_spec as S
END_ALLOWANCE={True:.052,False:.022}


def face_depth(z,front):
    """Distance inward from the bumper's leading vertical tangent.

    Physical profile controls, shared by the shell and both end grids. The
    Upper optical architecture is retained; the last lower band rolls under
    instead of retreating through the whole lower half. No separate face plate.
    """
    # One positive-curvature function per end, with no height-band blends.
    q=z-(.500 if front else .600)
    r=.008;positive=.5*(q+math.sqrt(q*q+r*r))
    if not front:return 1.95*q*q-1.60*(positive*positive-r*q/2-r*r/4)
    return 1.25*q*q+1.40*(positive*positive-r*q/2-r*r/4)


def locator_plan_guess(x,front):
    # Initial guesses for dark locators only. The control net is fitted by
    # section_field; these guesses never constrain painted body geometry.
    return (.360 if front else .235)*(x/.925)**2


def longitudinal(y):
    # Translate the accepted cabin, door cuts and axle package together. Blend
    # that translation into fixed 4900 mm bumper endpoints outside the cabin.
    fade=min(1,max(0,(y+2.45)/.65),max(0,(2.45-y)/.80))
    return y+S.CORE_SHIFT*fade

# y, shoulder half-width, belt height, roof/hood center height.
# The cabin stations retain their accepted shape. The end rows are a fair,
# monotone draw, replacing the old reverse-taper at the rear lamp corners.
STATIONS=[
 (-2.450,.850,.744,.770),(-2.425,.855,.750,.775),(-2.350,.869,.765,.786),
 (-2.200,.890,.785,.804),(-1.950,.910,.813,.843),(-1.680,.921,.843,.882),
 (-1.385,.925,.877,.916),(-1.180,.924,.903,.945),
 (-1.040,.920,.907,.955),(-.990,.918,.913,.965),
 (-.930,.918,.917,.990),(-.740,.918,.928,1.090),(-.460,.919,.942,1.250),
 (-.200,.920,.953,1.395),(-.130,.920,.956,1.425),(-.080,.920,.958,1.438),
 (.180,.921,.969,1.449),(.215,.921,.971,1.450),(.470,.923,.983,1.450),
 (.730,.925,.994,1.437),(.850,.925,1.000,1.414),(.910,.925,1.002,1.393),
 (1.105,.925,1.006,1.305),(1.125,.925,1.0065,1.295),
 (1.360,.922,1.010,1.230),(1.570,.916,1.012,1.135),
 (1.650,.911,1.011,1.105),(1.730,.905,1.010,1.065),
 (1.900,.892,1.009,1.025),(2.070,.876,1.007,1.027),
 (2.280,.856,1.002,1.035),(2.365,.848,.998,1.043),
 (2.390,.845,.992,1.044),(2.425,.841,.977,1.039),(2.450,.838,.958,1.025)]


def section(y,w,belt,top):
    """Half-section from roof center across shoulder to recessed rocker.

    Glass is a 22.5 degree tumblehome where the roof is fully developed.
    Narrowing the roof is a section control, rather than an extruded profile.
    """
    belt=min(belt,top-.085)  # monotonically descending end sections; no inverted shoulder row
    w-=.0027  # the broad axle draw, below, supplies the final 925 mm half-width
    top+=.0048*math.exp(-((y-.35)/.5)**2)
    cabin=max(0,min(1,(top-belt-.045)/.42))
    roof_edge=w-.028-math.tan(math.radians(22.5))*max(0,top-.055-belt)
    # Hood/deck breadth blends into roof breadth with the same surface rows.
    upper=top-.032-.016*cabin
    lower=min(belt+.018,upper-.012)
    lower_line=.345+.040*(y+.2)
    bulge=.006*sum(math.exp(-((longitudinal(y)-a)/.40)**2) for a in [S.FRONT_AXLE,S.REAR_AXLE])
    # Axle swell is confined below the widest shoulder, keeping the 1850 mm envelope.
    # Soft paired hood draws join the A-pillar feet. Transverse crown remains
    # 30 mm; the draws are broad enough to carry an unbroken reflection.
    end_tuck=max(0,min(1,(-y-1.8)/.65))
    bottom=.218-.043*end_tuck
    profile=[
      (0,y,top),(.35*w,y,top-.004),(.66*w,y,top-.014),
      (roof_edge-.026,y,top-.026),(roof_edge,y,upper),
      ((roof_edge+w-.025)/2,y,(upper+lower)/2),
      (w-.025,y,lower),(w-.010,y,belt),
      (w+bulge,y,belt-.024),(w+bulge-.001,y,belt-.033),
      (w-.004+bulge*.6,y,belt-.048),(w-.012,y,min(.660,belt-.100)),
      (w-.008,y,.505),(w-.044,y,lower_line+.018),
      (w-.048,y,lower_line),(w-.076,y,bottom+.017),(w-.105,y,bottom)]

    return profile


def region(y,c):
    if 4<=c<=5 and -.930<y<1.570:
        if .180<y<.215:return 'B applique'
        if 1.105<y<1.125:return 'C divider'
        if y<.180:return 'Front side glass'
        if y<1.105:return 'Rear side glass'
        return 'Quarter glass'
    if c<=2 and -.990<y<-.130:return 'Windshield'
    if c<=2 and .910<y<2.070:return 'Backlight'
    if c<=2:
        if y<-.990:return 'Hood'
        if y>2.070:return 'Trunk'
        return 'Roof'
    if c>=15:return 'Rocker'
    if c>=6:
        if S.DOOR_FRONT-S.CORE_SHIFT<y<S.DOOR_SPLIT-S.CORE_SHIFT:return 'Door F'
        if S.DOOR_SPLIT-S.CORE_SHIFT<y<S.DOOR_REAR-S.CORE_SHIFT:return 'Door R'
        return 'Front fender' if y<0 else 'Rear quarter'
    return 'Greenhouse'


def hood_draw_x(y):
    return .555+.245*max(0,min(1,(y+2.25)/1.17))


def side_width(y):
    # 28 mm die swell over each wheel, carried by the same section as the doors.
    rear_span=.48+.22*.5*(1+math.tanh((y-S.REAR_AXLE)/.18))
    return .89790+.028*(math.exp(-((y-S.FRONT_AXLE)/.48)**2)+math.exp(-((y-S.REAR_AXLE)/rear_span)**2))


def shoulder_height(y):
    return .920+.018*y


def character_height(y):
    return .430+.100*(y-S.DOOR_FRONT)/(S.DOOR_REAR-S.DOOR_FRONT)


def side_draw(y,z):
    """Progressive door crown, shallow die hollow and recessed sill return.

    These are die controls. Independent mesh sections measure the result.
    """
    def positive(q,r=.006):return .5*(q+math.sqrt(q*q+r*r))
    h=shoulder_height(y);line=character_height(y)
    d=positive(h-z);dl=h-line
    tail=positive(d-dl,.012);c=d-tail
    lower=-.065*c-.235*c*c-.120*tail
    lower-=.0040*math.exp(-((z-line-.043)/.030)**2)
    lower-=.50*positive(.275-z,.008)
    upper=-.37*positive(z-h)-.12*positive(z-h)**2
    return lower+upper


def body_section(y,w,belt,top):
    half=section(y,w,belt,top)
    physical=longitudinal(y)
    width=side_width(physical)
    delta=width-(w-.0027)
    result=[]
    for i,(x,yy,z) in enumerate(half):
        x+=delta*(x/max(w,1e-6))
        # Use the same three-dimensional door section at every station. There
        # are no door-specific bulges or width tweaks at the panel cut lines.
        if i>=7:
            h=shoulder_height(physical);line=character_height(physical)
            zs=[belt,h+.017,h,h-.023,h-.085,.690,line+.050,line+.012,line-.020,.235]
            z=zs[i-7]
            t=max(0,(i-8)/8)
            yy=physical*(1-.30*t)
            width_here=side_width(yy)
            x=width_here+side_draw(physical,z)
        # Accepted header adjustment follows the windshield's rake.
        header=math.exp(-((y+.14)/.25)**2)*max(0,min(1,(z-1.03)/.28))
        yy=(physical if i<=8 else yy)-.106*header;z-=.058*header
        if 1.3<y<2.07:
            z+=.060*math.exp(-((y-1.66)/.24)**2)*max(0,1-(abs(x)/.72)**4)
        if y>.85:
            t=max(0,min(1,(y-.85)/.70));lift=.068*t*t*(3-2*t)
            z+=lift*max(0,min(1,(z-.82)/.25))
        result.append((x,yy,z))
    result.insert(-1,(side_width(physical)+side_draw(physical,character_height(physical)-.055),physical*.73,character_height(physical)-.055))
    return result


# End rows fold the same rectangular quad sheet down from the hood/deck to the
# chin. Its entire boundary is underneath. There are NO cap patches, corner
# poles, booleans/unions, shrinkwraps, end fields or post-subdivision projection.
# y/z are the centerline CONTROL polygon; the corner's longitudinal spacing is
# separately monotone so no end row collapses onto its neighbor at the side.
FRONT_ROWS=[
 (-2.328,.175,-2.135),(-2.350,.205,-2.125),(-2.401,.300,-2.095),
 (-2.439,.400,-2.065),(-2.4595,.490,-2.000),(-2.4475,.535,-1.985),
 (-2.397,.605,-1.970),(-2.330,.685,-1.955),
 (-2.255,.768,-1.940),(-2.240,.778,-1.935),
 (-2.150,.794,-1.865),(-1.965,.830,-1.745),(-1.760,.869,-1.610),
 (-1.540,.911,-1.465),(-1.340,.949,-1.325)]
REAR_ROWS=[
 (1.950,1.018,1.950),(2.120,1.025,2.005),(2.240,1.032,2.020),
 (2.355,1.044,2.030),(2.380,1.045,2.035),(2.394,1.031,2.040),
 (2.407,.969,2.045),(2.425,.865,2.055),(2.443,.755,2.065),
 (2.454,.625,2.075),(2.450,.575,2.085),(2.401,.460,2.095),
 (2.337,.360,2.105),(2.276,.300,2.115),(2.246,.270,2.125)]



def end_section(row,front):
    yc,zc,tangent=row
    sign=1 if front else -1
    bottom=.175 if front else .270
    xs=[0,.28,.55,.735,.815,.860,.894,.913,.921]
    # A hood's section is shallow. The same section turns around in plan at
    # the vertical fascia, instead of keeping a spurious diagonal top ridge.
    topness=max(0,min(1,(zc-(.69 if front else .965))/.075))
    result=[]
    w=side_width(tangent)
    xs=[x*w/.921 for x in xs]
    for i,x in enumerate(xs):
        turn=1-math.sqrt(max(0,1-(x/w)**2))
        y=yc+(tangent-yc)*turn
        if front:
            top=.770+.185*(y+2.245)-.031*(x/.80)**2
        else:top=deck_height(x,y)
        lower_roll=0 if front else .045*(x/w)**4*math.exp(-((zc-.218)/.120)**2)
        wall=zc-.004*(x/w)**2+lower_roll
        z=wall*(1-topness)+top*topness
        result.append((x,y,z))
    outer_z=result[-1][2]
    fractions=[0,.030,.080,.420,.640,.815,.845,.952,1]
    offsets=[0,-.002,-.014,-.033,-.044,-.038,-.039,-.075,-.100]
    for j in range(1,9):
        t=j/8
        y=tangent*(1-.30*t)
        z=outer_z*(1-fractions[j])+bottom*fractions[j]
        x=side_width(y)+offsets[j]
        result.append((x,y,z))
    a,c=Vector(result[-2]),Vector(result[-1]);result.insert(-1,tuple(a.lerp(c,.15)))
    return result


def hood_height(x,y):
    # Convex shallow crown with an outward slope change at the two draw lines.
    # A stamped fender crown is a broad draw. The former 38 mm / 55 mm
    # Gaussian ridge folded the hood/lamp corner before any panel was cut.
    crown=.045*math.exp(-((abs(x)-.875)/.100)**2)*math.exp(-((y+1.57)/.74)**4)
    return .770+.170*(y+2.245)-.050*(x/.80)**2-.065*max(0,abs(x)-hood_draw_x(y))+crown


def deck_height(x,y):
    lip=.039*math.exp(-((y-2.368)/.070)**2)
    return 1.080+.020*(y-1.970)-.032*(x/.70)**2+lip


def crease_rows(half,hood,backlight=False):
    a,p,c=[Vector(q) for q in half[1:4]]
    if hood:
        x=hood_draw_x(p.y)
        result=[]
        for xx in [x-.014,x,x+.014]:
            t=(xx-a.x)/(c.x-a.x);yy=a.y+(c.y-a.y)*t
            result.append((xx,yy,hood_height(xx,yy)))
        half=[(x,y,hood_height(x,y)) if i<=3 else (x,y,z) for i,(x,y,z) in enumerate(half)]
    else:
        result=[tuple(a.lerp(p,.60)),tuple(p),tuple(p.lerp(c,.45))]
    half=half[:2]+result+half[3:]
    if backlight:
        center,edge=half[0],half[5]
        half=[(x,y,center[2]-(center[2]-edge[2])*(x/edge[0])**2) if i<=5 else (x,y,z) for i,(x,y,z) in enumerate(half)]
    return half


def section_field(p):
    """One continuous waterline section family used to FIT control vertices.

    Cubic end terms have zero first and second derivatives at their side
    tangents. The waterline therefore continues into the doors without a
    volume join. This function never moves the evaluated/exported surface.
    """
    x,y,z=p
    def positive(q,r=.006):return .5*(q+math.sqrt(q*q+r*r))
    bumper=.040*math.exp(-((y+2.20)/.55)**2-((z-.50)/.16)**2)+.060*math.exp(-((y-2.20)/.60)**2-((z-.60)/.16)**2)
    # Preserve the held end waterlines while the door section changes. The
    # C2 station blend runs outside the door panels and through the fenders.
    t=max(0,min(1,(abs(y)-1.50)/.45));t=t*t*t*(10-15*t+6*t*t)
    if y>0:
        # Continue the door's shoulder into the hip before turning around the
        # tail. The old early blend raised the shoulder through the wheel and
        # pinched the upper quarter into a dark hollow under grazing light.
        q=max(0,min(1,(y-1.85)/.50));q=q*q*q*(10-15*q+6*q*q)
        u=max(0,min(1,(z-.620)/.120));u=u*u*u*(10-15*u+6*u*u)
        t=t*(1-u)+q*u
    h=.948+.037*y;d=positive(h-z)
    lower_knee=.61 if y<0 else h-.350
    old=-.050*(1-math.exp(-d/.10))+.010*(d/.61)**2-.43*positive(d-lower_knee,.010)-.42*positive(z-h)-.12*positive(z-h)**2
    width=side_width(y)+(1-t)*side_draw(y,z)+t*old+bumper
    if y>0:
        blend=max(0,min(1,(y-1.75)/.35));blend=blend*blend*blend*(10-15*blend+6*blend*blend)
        end_width=.912-.20*(z-.620)**2
        width=width*(1-blend)+end_width*blend
    ft,rt=-1.800,1.940
    # A smooth lower roll leaves the upper optical architecture alone. The
    # maximum length stays at the main impact band; the bottom 130 mm turns
    # under rather than ending in a full-height vertical wall.
    fd=max(.20,2.4375+ft-face_depth(z,True))
    rd=max(.20,2.4475-rt-face_depth(z,False))
    a=max(0,ft-y)/fd;c=max(0,y-rt)/rd
    power=4 if y<0 else 4.2
    q=abs(x/width)**power+a**3+c**3-1
    gradient=math.sqrt((power*abs(x/width)**(power-1)/width)**2+(3*a*a/fd if y<ft else 3*c*c/rd)**2)
    wall=q/max(1.0,gradient)
    # The crown rolls down into the same side waterline. C∞ smooth maximum
    # avoids the derivative step of the previous polynomial rounded union.
    if y< -1.08:top=z-hood_height(x,y)
    elif y>1.90:top=z-deck_height(x,y)
    else:top=-2
    r=.012 if y<0 else .014
    m=max(wall,top)
    return m+r*math.log(math.exp((wall-m)/r)+math.exp((top-m)/r))


def fit_control_net(ob):
    # Three regular refinements give the section fit enough degrees of freedom
    # at the broad plan turns. It is still an all-quad CONTROL mesh; subdivision
    # that defines the final surface happens after this fit, without projection.
    sub=ob.modifiers.new('Refine section-fit controls','SUBSURF');sub.levels=3;G.apply(ob)
    parameter_u=[0.]*len(ob.data.vertices)
    for loop in ob.data.loops:parameter_u[loop.vertex_index]=ob.data.uv_layers.active.data[loop.index].uv.x
    center_u=(ob['grid_width']-1)/2
    for v in ob.data.vertices:
        p=v.co
        # The accepted canopy retains its full section, including the low
        # backlight corners; height alone cannot identify a roof/side chart.
        def ease(t):
            t=max(0,min(1,t));return t*t*t*(10-15*t+6*t*t)
        protect=ease((p.y+1.25)/.22)*ease((2.02-p.y)/.22)
        edge_fit=ease((abs(parameter_u[v.index]-center_u)-7.5)/3.0)
        edge_fit=max(edge_fit,ease((shoulder_height(p.y)+.065-p.z)/.030))
        fit_weight=1-protect*(1-edge_fit)
        if fit_weight<1e-7:continue
        original=p.copy()
        cy=max(-1.40,min(1.40,p.y));end_center=Vector((0,cy,.43 if p.y<0 else .60))
        # A hard z=370 mm switch in the projection center folded control rows
        # at the diffuser corners. Blend the fitting frame before subdivision;
        # the limit surface and its own normals now remain continuous there.
        low=ease((.50-p.z)/.25)
        end_center.z+=(p.z-end_center.z)*low
        if p.y<0:
            # Hold the accepted hood/cowl fit; only the lower end frame needs
            # the smooth height transition. The rear hip gets the longer blend.
            center=Vector((0,p.y,p.z)).lerp(Vector((0,cy,.43)),ease((-1.00-p.y)/.24))
            center.z+=(p.z-center.z)*low*ease((-1.80-p.y)/.10)
        else:
            center=Vector((0,p.y,p.z)).lerp(end_center,ease((p.y-1.65)/.25))
        direction=p-center
        lo,hi=0.,2.
        for _ in range(30):
            t=(lo+hi)/2
            if section_field(center+direction*t)>0:hi=t
            else:lo=t
        v.co=original.lerp(center+direction*((lo+hi)/2),fit_weight)
    ob.data.update()


def fair_pillar_feet(ob):
    """Relax the fitted control net locally before evaluating its limit.

    The fit/canopy boundary used to leave a narrow normal kink at the A foot
    and C header. A smooth, compact relaxation spans those manufactured radii;
    the accepted centerline, glass width and door sections stay outside it.
    """
    adjacency=[[] for _ in ob.data.vertices]
    for e in ob.data.edges:
        a,c=e.vertices;adjacency[a].append(c);adjacency[c].append(a)
    weights=[]
    for v in ob.data.vertices:
        x,y,z=v.co
        a=math.exp(-((y+1.045)/.20)**2-((z-1.00)/.16)**2-((abs(x)-.83)/.11)**2)
        c=math.exp(-((y-.91)/.20)**2-((z-1.34)/.13)**2-((abs(x)-.69)/.13)**2)
        lamp=math.exp(-((y+2.02)/.32)**2-((z-.83)/.15)**2-((abs(x)-.75)/.19)**2)
        # The fitted side/canopy protection changes at the sail's foot. Fair
        # its control rows across the transition, rather than its normals.
        sail=math.exp(-((y-1.68)/.30)**2-((z-1.04)/.16)**2-((abs(x)-.78)/.17)**2)
        # Keep the measured shoulder envelope fixed. The sail correction
        # belongs above that die line, rather than pulling its widest row in.
        t=max(0,min(1,(z-shoulder_height(y)-.005)/.100))
        sail*=t*t*t*(10-15*t+6*t*t)
        weights.append(.55*max(a,c,lamp,sail))
    for _ in range(90):
        old=[v.co.copy() for v in ob.data.vertices]
        for v,w,neighbors in zip(ob.data.vertices,weights,adjacency):
            if w<1e-5 or len(neighbors)!=4:continue
            v.co=old[v.index].lerp(sum((old[i] for i in neighbors),Vector())/4,w)
    ob.data.update()


def master(level):
    n=20;verts=[];faces=[];labels=[]
    rows=[];kinds=[]
    for row in FRONT_ROWS:
        rows.append(crease_rows(end_section(row,True),row[1]>.74));kinds.append(('front',row[0]))
    for row in STATIONS:
        if -1.18<=row[0]<=1.90:
            rows.append(crease_rows(body_section(*row),row[0]<-.99,backlight=row[0]>.85));kinds.append(('body',row[0]))
    for row in REAR_ROWS:
        rows.append(crease_rows(end_section(row,False),False));kinds.append(('rear',row[0]))
    for half in rows:
        verts.extend([(-x,y,z) for x,y,z in reversed(half[1:])]+half)
    width=2*n-1
    for j in range(len(rows)-1):
        kind,y=kinds[j];next_kind,yn=kinds[j+1];y=(y+yn)/2
        for i in range(width-1):
            c=i-(n-1) if i>=n-1 else (n-2)-i
            c=c if c<2 else 2 if c<5 else c-2
            side='R' if i>=n-1 else 'L'
            if kind=='body' and next_kind=='body':label=region(y,c)
            elif kind=='front':
                label=('Front molded fascia' if j<8 else 'Hood' if c<=2 else 'Front fender')
            elif kind=='rear':
                label='Trunk' if j-len(FRONT_ROWS)-sum(1 for r in STATIONS if -1.18<=r[0]<=1.90)<6 and c<=2 else 'Rear molded fascia'
            else:label='Backlight' if c<=2 else 'Rear quarter'
            if label in ['Front fender','Rear quarter'] or (kind=='body' and label not in ['Hood','Roof','Trunk','Windshield','Backlight']):label+='_'+side
            labels.append(label)
            faces.append((j*width+i,j*width+i+1,(j+1)*width+i+1,(j+1)*width+i))
    ob=G.mesh('Sedan unified subdivision cage',verts,faces)
    names=sorted(set(labels))
    for name in names:ob.data.materials.append(bpy.data.materials.new('Cage region '+name))
    for face,label in zip(ob.data.polygons,labels):face.material_index=names.index(label);face.use_smooth=True
    uv=ob.data.uv_layers.new(name='Surface parameters')
    for f in ob.data.polygons:
        for li in f.loop_indices:
            vi=ob.data.loops[li].vertex_index;uv.data[li].uv=(vi%width,vi//width)
    ob['grid_width']=width;ob['grid_rows']=len(rows)
    fit_control_net(ob)
    fair_pillar_feet(ob)
    bm=bmesh.new();bm.from_mesh(ob.data)
    quads=sum(len(f.verts)==4 for f in bm.faces)
    if quads!=len(bm.faces) or any(len(v.link_edges)!=4 for v in bm.verts if not v.is_boundary):raise AssertionError('The parent control sheet must be regular quads')
    unseen=set(bm.verts);components=0
    while unseen:
        components+=1;stack=[unseen.pop()]
        while stack:
            for e in stack.pop().link_edges:
                for v in e.verts:
                    if v in unseen:unseen.remove(v);stack.append(v)
    ob['cage_report']=json.dumps(dict(vertices=len(bm.verts),quads=quads,connected_components=components,interior_valence_four=True,fit='Control vertices only; no evaluated projection'))
    bm.free()
    sub=ob.modifiers.new('Fair continuous quad sheet','SUBSURF');sub.subdivision_type='CATMULL_CLARK';sub.levels=level;sub.render_levels=level
    G.apply(ob)
    ob['construction']='One regular all-quad sheet folded over both ends; Catmull-Clark before projected cuts'
    return ob,names


def tessellate(parent,high=False):
    """Resample the subdivision limit in its original two-dimensional chart.

    Regular feature-aligned quads replace QEM collapse. This keeps reflection
    derivatives represented across shallow doors even when their position
    error would let a decimator replace the entire panel with two triangles.
    """
    mesh=parent.data;mesh.calc_loop_triangles();uvs=[None]*len(mesh.vertices)
    layer=mesh.uv_layers.active.data
    for loop in mesh.loops:
        uv=layer[loop.index].uv;uvs[loop.vertex_index]=Vector((uv.x,uv.y,0))
    ts=[tuple(t.vertices) for t in mesh.loop_triangles]
    tree=BVHTree.FromPolygons(uvs,ts,all_triangles=True)
    width=int(parent['grid_width']);rows=int(parent['grid_rows'])
    step=.25 if high else .5
    us=sorted(set([i*step for i in range(round((width-1)/step)+1)]+[u+d for u in [(width-1)/2-10,(width-1)/2+10] for d in [-.75,-.25,.25,.75]]))
    vs=sorted(set(list(range(rows))+[j+.5 for j in range(rows-1) if high or j in [2,3,4,5,6] or j>=rows-15]))
    # Keep the actual parent extrema, so regular sampling cannot miss a narrow
    # shoulder maximum or a bumper tangent and silently shrink the envelope.
    for axis in range(3):
        for choose in [min,max]:
            vi=choose(range(len(mesh.vertices)),key=lambda i:mesh.vertices[i].co[axis])
            u,v=uvs[vi].x,uvs[vi].y
            if min(abs(u-q) for q in us)>.001:us.append(u)
            if min(abs(v-q) for q in vs)>.001:vs.append(v)
    us=sorted(us);vs=sorted(vs)
    def sample(u,v):
        p=Vector((u,v,0));hit,_,fi,_=tree.find_nearest(p);a,c,d=ts[fi]
        return barycentric_transform(hit,uvs[a],uvs[c],uvs[d],mesh.vertices[a].co,mesh.vertices[c].co,mesh.vertices[d].co),mesh.loop_triangles[fi].polygon_index
    # Spend the extra transverse samples on the rear turn, not across every
    # door. One stitched transition uses triangles; the parent stays all quads.
    center=(width-1)/2
    extra=[center+sign*d for sign in [-1,1] for d in [6.25,6.75,7.25,7.75,8.25]]
    coarse=sorted(set([float(i) for i in range(width)] + [center+d for d in [-16.5,-15.5,15.5,16.5]]+[u+d for u in [(width-1)/2-10,(width-1)/2+10] for d in [-.75,-.25,.25,.75]]+[min(us),max(us)]))
    # Broad central canopy needs fewer chords than a tight bumper turn.
    coarse=[u for u in coarse if abs(u-center)>=5 or abs(u-center)%2<1e-7]
    grids=[(sorted(set(us+extra)) if v>=rows-15 or v<8 else us if v<13 else coarse) if not high else us for v in vs]
    vertices=[];chart=[];offsets=[]
    for v,columns in zip(vs,grids):
        offsets.append(len(vertices))
        for u in columns:vertices.append(sample(u,v)[0]);chart.append((u,v))
    faces=[]
    for row,(aa,bb) in enumerate(zip(grids,grids[1:])):
        i=j=0;a0,b0=offsets[row:row+2]
        while i<len(aa)-1 or j<len(bb)-1:
            na=aa[i+1] if i<len(aa)-1 else math.inf
            nb=bb[j+1] if j<len(bb)-1 else math.inf
            if abs(na-nb)<1e-8:
                faces.append((a0+i,a0+i+1,b0+j+1,b0+j));i+=1;j+=1
            elif na<nb:faces.append((a0+i,a0+i+1,b0+j));i+=1
            else:faces.append((a0+i,b0+j+1,b0+j));j+=1
    if not high:
        # Refine the actual lower rear plan turn in BOTH chart directions.
        # Adjacent polygons share inserted midpoints, so there are no T cracks.
        selected=set();edges={}
        for fi,face in enumerate(faces):
            p=sum((vertices[i] for i in face),Vector())/len(face)
            rear_roll=1.76<p.y<1.99 and .35<p.z<.55 and abs(p.x)>.80
            a_foot=-1.17<p.y<-.83 and .96<p.z<1.19 and abs(p.x)>.70
            c_header=.70<p.y<1.14 and 1.25<p.z<1.45 and abs(p.x)>.60
            lamp_crest=-2.13<p.y<-1.64 and .74<p.z<.93 and abs(p.x)>.70
            if len(face)==4 and (rear_roll or a_foot or c_header or lamp_crest):
                selected.add(fi)
                for a,b in zip(face,face[1:]+face[:1]):edges[tuple(sorted((a,b)))]=None
        for edge in edges:
            a,b=edge;u=(chart[a][0]+chart[b][0])/2;v=(chart[a][1]+chart[b][1])/2
            edges[edge]=len(vertices);vertices.append(sample(u,v)[0]);chart.append((u,v))
        refined=[]
        for fi,face in enumerate(faces):
            if fi in selected:
                u=sum(chart[i][0] for i in face)/4;v=sum(chart[i][1] for i in face)/4
                ci=len(vertices);vertices.append(sample(u,v)[0]);chart.append((u,v))
                for i,a in enumerate(face):
                    b=face[(i+1)%4];c=face[i-1]
                    refined.append((a,edges[tuple(sorted((a,b)))],ci,edges[tuple(sorted((c,a)))]))
            else:
                polygon=[]
                for a,b in zip(face,face[1:]+face[:1]):
                    polygon.append(a);mid=edges.get(tuple(sorted((a,b))))
                    if mid is not None:polygon.append(mid)
                refined.append(tuple(polygon))
        faces=refined
    ob=G.mesh('Fair game surface samples',vertices,faces)
    for mat in mesh.materials:ob.data.materials.append(mat)
    for face in ob.data.polygons:
        u=sum(chart[i][0] for i in face.vertices)/len(face.vertices)
        v=sum(chart[i][1] for i in face.vertices)/len(face.vertices)
        _,fi=sample(u,v);face.material_index=mesh.polygons[fi].material_index;face.use_smooth=True
    return ob,uvs


def conform_edges(bm):
    """Split shared edges at clipping-generated T vertices before sheet closing."""
    bm.verts.ensure_lookup_table();bm.verts.index_update();verts=list(bm.verts)
    kd=KDTree(len(verts))
    for i,v in enumerate(verts):kd.insert(v.co,i)
    kd.balance();weld={}
    for edge in list(bm.edges):
        a,c=edge.verts;delta=c.co-a.co;length=delta.length
        if length<1e-6:continue
        candidates=[]
        for co,index,_ in kd.find_range((a.co+c.co)/2,length/2+1e-6):
            v=verts[index]
            if v==a or v==c:continue
            t=(co-a.co).dot(delta)/(length*length)
            if 1e-5<t<1-1e-5 and (co-a.co-delta*t).length<5e-7:candidates.append((t,v))
        # Split from the far end so the original edge's a-to-new length shrinks.
        previous=1.
        for t,v in sorted(candidates,reverse=True,key=lambda p:p[0]):
            new_edge,new_vert=bmesh.utils.edge_split(edge,a,t/previous)
            new_vert.co=v.co;weld[new_vert]=v;edge=new_edge;previous=t
    if weld:bmesh.ops.weld_verts(bm,targetmap=weld)


def trim_arch(ob,axle,segments):
    """Clip the fair outer sheet, then close its gauge; no thin-solid boolean.

    Convex polygon difference in YZ, retaining the original face planes. The
    cutter is the same inscribed polygon as the arch's circular cylinder.
    """
    radius=S.ARCH_RADIUS;inner=radius*math.cos(math.pi/segments)
    planes=[(math.cos((j+.5)*math.tau/segments),math.sin((j+.5)*math.tau/segments)) for j in range(segments)]
    vertices=[];faces=[]
    for f in ob.data.polygons:
        polygon=[ob.data.vertices[i].co.copy() for i in f.vertices]
        ys=[p.y-axle for p in polygon];zs=[p.z-S.HUB_HEIGHT for p in polygon]
        if min(ys)>radius or max(ys)<-radius or min(zs)>radius or max(zs)<-radius:
            pieces=[polygon]
        elif max(y*y+z*z for y,z in zip(ys,zs))<inner*inner:continue
        else:
            pieces=[]
            for ny,nz in planes:
                inside=[];outside=[]
                for a,b in zip(polygon,polygon[1:]+polygon[:1]):
                    da=ny*(a.y-axle)+nz*(a.z-S.HUB_HEIGHT)-inner
                    db=ny*(b.y-axle)+nz*(b.z-S.HUB_HEIGHT)-inner
                    (outside if da>=0 else inside).append(a)
                    if da*db<0:
                        q=a+(b-a)*(da/(da-db));inside.append(q);outside.append(q)
                if len(outside)>=3:pieces.append(outside)
                polygon=inside
                if len(polygon)<3:break
        for piece in pieces:
            offset=len(vertices);vertices.extend(piece);faces.append(tuple(range(offset,len(vertices))))
    mesh=bpy.data.meshes.new('Projected arch trim');mesh.from_pydata(vertices,[],faces);mesh.update()
    material=ob.data.materials[0];old=ob.data;ob.data=mesh;ob.data.materials.append(material)
    if old.users==0:bpy.data.meshes.remove(old)
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
    conform_edges(bm)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
    bm.to_mesh(ob.data);bm.free()


def closeable_sheet(ob):
    """Remove clipping crumbs and split point-touching surface fans.

    Two sheet regions touching at a single vertex need independent gauge rims;
    otherwise Solidify joins both rims onto one four-face non-manifold edge.
    No surface point is moved by the fan split.
    """
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
    bad=[f for f in bm.faces if f.calc_area()<1e-12]
    if bad:bmesh.ops.delete(bm,geom=bad,context='FACES')
    # Adjacent convex clipping fragments can encode the same tiny facet twice
    # after a T intersection is welded. Remove duplicate coverage, then trim
    # only submillimeter clipping crumbs at a three-face edge before gauging.
    bm.verts.index_update();seen=set();duplicates=[]
    for f in bm.faces:
        key=tuple(sorted(v.index for v in f.verts))
        if key in seen:duplicates.append(f)
        else:seen.add(key)
    if duplicates:bmesh.ops.delete(bm,geom=duplicates,context='FACES')
    crumbs=0
    while True:
        edges=[e for e in bm.edges if len(e.link_faces)>2]
        if not edges:break
        removable={min(e.link_faces,key=lambda f:f.calc_area()) for e in edges}
        removable={f for f in removable if f.calc_area()<1e-7 and max(e.calc_length() for e in f.edges)<.002}
        if not removable:raise ValueError(('Non-sheet clipping intersection',ob.name,len(edges)))
        crumbs+=len(removable);bmesh.ops.delete(bm,geom=list(removable),context='FACES')
    bm.verts.ensure_lookup_table();bm.verts.index_update()
    vertices=[v.co.copy() for v in bm.verts]
    faces=[list(v.index for v in f.verts) for f in bm.faces]
    incident={i:[] for i in range(len(vertices))};edges={}
    for fi,face in enumerate(faces):
        for i in face:incident[i].append(fi)
        for a,c in zip(face,face[1:]+face[:1]):edges.setdefault(tuple(sorted((a,c))),[]).append(fi)
    splits=0;replacements={}
    for vi,indices in incident.items():
        if len(indices)<2:continue
        graph={i:set() for i in indices}
        for fi in indices:
            face=faces[fi]
            for neighbor in [face[(face.index(vi)-1)%len(face)],face[(face.index(vi)+1)%len(face)]]:
                for other in edges[tuple(sorted((vi,neighbor)))]:
                    if other!=fi:graph[fi].add(other)
        unseen=set(indices);groups=[]
        while unseen:
            stack=[unseen.pop()];group=[]
            while stack:
                i=stack.pop();group.append(i)
                for other in graph[i]:
                    if other in unseen:unseen.remove(other);stack.append(other)
            groups.append(group)
        for group in groups[1:]:
            new=len(vertices);vertices.append(vertices[vi]);splits+=1
            for fi in group:replacements[(fi,vi)]=new
    faces=[[replacements.get((fi,i),i) for i in face] for fi,face in enumerate(faces)]
    bm.free()
    old=ob.data;mesh=bpy.data.meshes.new(old.name+' closed fans');mesh.from_pydata(vertices,[],faces);mesh.update()
    for mat in old.materials:mesh.materials.append(mat)
    ob.data=mesh
    if old.users==0:bpy.data.meshes.remove(old)
    ob['point_fans_split']=splits
    ob['duplicate_clip_facets_removed']=len(duplicates)
    ob['submillimeter_clip_crumbs_removed']=crumbs



def sheet_gauge(ob,thickness):
    """Keep an unambiguous outer/back/rim role through every aperture cut."""
    mat=ob.data.materials[0]
    while len(ob.data.materials)<3:ob.data.materials.append(mat)
    gauge=ob.modifiers.new('Sheet gauge','SOLIDIFY');gauge.thickness=thickness;gauge.offset=-1;gauge.use_even_offset=False
    gauge.material_offset=1;gauge.material_offset_rim=2;G.apply(ob)
    ob['sheet_roles']=True


def simplify_inner_gauge(ob,tree,minimum_depth=.0004,max_collapses=1000,max_iterations=16):
    """Collapse only hidden back edges, with local depth and link checks.

    Exposed skin vertices and cut rims are locked. Each new back triangle is
    probed against the parent before collapse; the manifold link condition
    prevents bridges across adjacent apertures. No broad dissolve can encode
    a hole as a repeated-vertex n-gon.
    """
    bm=bmesh.new();bm.from_mesh(ob.data);bm.normal_update()
    matrix=ob.matrix_world;inverse_normal=matrix.to_3x3().transposed()
    inward=[]
    for f in bm.faces:
        if f.material_index==1:inward.append(f)
    bmesh.ops.triangulate(bm,faces=inward)
    inward=set(inward)
    # Triangulation creates new faces; classify once more, including those.
    bm.normal_update();inward=set()
    for f in bm.faces:
        if f.material_index==1:inward.add(f)
    pure={v for v in bm.verts if v.link_faces and all(f in inward for f in v.link_faces)}
    count=0;minimum=1.
    for iteration in range(max_iterations):
        bm.edges.index_update();used=set();changed=0
        candidates=sorted([e for e in bm.edges if len(e.link_faces)==2 and all(v in pure for v in e.verts)
                           and all(len(f.verts)==3 for f in e.link_faces)],key=lambda e:(e.calc_length(),e.index))
        for e in candidates:
            if count>=max_collapses:break
            if not e.is_valid:continue
            a,c=e.verts
            if a in used or c in used or e.calc_length()>.12:continue
            na={v for ed in a.link_edges for v in ed.verts if v!=a}
            nc={v for ed in c.link_edges for v in ed.verts if v!=c}
            if len(na&nc)!=2:continue
            neighbors=na|nc|{a,c}
            if neighbors&used:continue
            point=(a.co+c.co)/2;valid=True;depth_min=1.
            for f in set(a.link_faces)|set(c.link_faces):
                if f in e.link_faces:continue
                ps=[point if v==a or v==c else v.co for v in f.verts]
                normal=(ps[1]-ps[0]).cross(ps[2]-ps[0])
                if normal.length<1e-10 or normal.normalized().dot(f.normal)<.70:valid=False;break
                probes=[sum(ps,Vector())/3]+[(p+q)/2 for p,q in zip(ps,ps[1:]+ps[:1])]
                for q in probes:
                    q=matrix@q;hit,n,_,_=tree.find_nearest(q);depth=-(q-hit).dot(n)
                    if depth<minimum_depth:valid=False;break
                    depth_min=min(depth_min,depth)
                if not valid:break
            if not valid:continue
            bmesh.ops.collapse(bm,edges=[e],uvs=False)
            used|=neighbors;count+=1;changed+=1;minimum=min(minimum,depth_min)
        if not changed or count>=max_collapses:break
        pure={v for v in pure if v.is_valid};bm.normal_update()
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-8)
    # Reject any topology regression; the original outer sheet remains intact.
    valid=all(e.is_manifold for e in bm.edges)
    valid=valid and all((tri[1].vert.co-tri[0].vert.co).cross(tri[2].vert.co-tri[0].vert.co).length>2e-12 for tri in bm.calc_loop_triangles())
    ob['inner_gauge_reduced']=valid and count>0
    ob['inner_back_collapses']=count if valid else 0
    ob['inner_gauge_probe_depth_m']=minimum if count else 0.
    if valid:bm.to_mesh(ob.data)
    bm.free();ob.data.update()


def build(b):
    source,names=master(2)
    b.root['surface_cage']=source['cage_report']
    # Project straight side shut lines through the already fair sheet. The
    # front/rear/hood/greenhouse boundaries follow its longitudinal cage charts;
    # the door boundaries are independent of the cage's station spacing.
    source.data.calc_loop_triangles()
    parent_points=[v.co.copy() for v in source.data.vertices]
    parent_normals=[v.normal.copy() for v in source.data.vertices]
    parent_triangles=[tuple(t.vertices) for t in source.data.loop_triangles]
    parent_tree=BVHTree.FromPolygons(parent_points,parent_triangles,all_triangles=True)
    dense=source;source,parent_uvs=tessellate(dense,b.high);bpy.data.objects.remove(dense,do_unlink=True)
    surface_map=dict(tree=parent_tree,points=parent_points,normals=parent_normals,triangles=parent_triangles,uvs=parent_uvs)
    bm=bmesh.new();bm.from_mesh(source.data)
    # Cut a narrow backlight out of the same canopy, retaining the continuous
    # painted sail panels. Their widening feet become the quarter shoulders;
    # no overlay shell or replacement volume changes the accepted roof line.
    for sign in [-1,1]:
        fs=[f for f in bm.faces if names[f.material_index]=='Backlight']
        es={e for f in fs for e in f.edges};vs={v for f in fs for v in f.verts}
        bm.verts.index_update();bm.edges.index_update()
        bmesh.ops.bisect_plane(bm,geom=sorted(vs,key=lambda v:v.index)+sorted(es,key=lambda e:e.index)+fs,
            dist=1e-8,plane_co=(sign*.586,0,0),plane_no=(sign,-.025,0),clear_inner=False,clear_outer=False)
    for f in bm.faces:
        if names[f.material_index]=='Backlight':
            p=f.calc_center_median()
            if abs(p.x)>.586+.025*p.y:
                f.material_index=names.index('Greenhouse_'+('R' if p.x>0 else 'L'))
    cuts=[S.DOOR_FRONT,S.DOOR_SPLIT,S.DOOR_REAR]
    for line in cuts:
        for y in [line-S.PANEL_GAP/2,line+S.PANEL_GAP/2]:
            bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),
                dist=1e-8,plane_co=(0,y,0),plane_no=(0,1,0),clear_inner=False,clear_outer=False)
    for axis,line in [(0,-.615),(0,.615),(2,.620)]:
        if axis==2:
            # A slightly arched parting line follows the convex bumper crown.
            # Cutting in this temporary coordinate only determines the reveal;
            # new intersections are returned to the original fair sheet.
            fs=[f for f in bm.faces if names[f.material_index] in ['Trunk','Rear molded fascia']]
            es={e for f in fs for e in f.edges};vs={v for f in fs for v in f.verts}
            for v in vs:v.co.z+=.022*(v.co.x/.90)**2
        for offset in [-S.PANEL_GAP/2,S.PANEL_GAP/2]:
            co=[0.,0.,0.];no=[0.,0.,0.];co[axis]=line+offset;no[axis]=1.
            if axis==2:
                fs=[f for f in bm.faces if names[f.material_index] in ['Trunk','Rear molded fascia']]
                es={e for f in fs for e in f.edges};vs|={v for f in fs for v in f.verts}
                bm.verts.index_update();bm.edges.index_update()
                geom=sorted(vs,key=lambda v:v.index)+sorted(es,key=lambda e:e.index)+fs
            else:geom=list(bm.verts)+list(bm.edges)+list(bm.faces)
            bmesh.ops.bisect_plane(bm,geom=geom,dist=1e-8,plane_co=co,plane_no=no,clear_inner=False,clear_outer=False)
        if axis==2:
            vs|={v for f in bm.faces if names[f.material_index] in ['Trunk','Rear molded fascia'] for v in f.verts}
            for v in vs:v.co.z-=.022*(v.co.x/.90)**2
    physical_doors=getattr(b,'physical_doors',False)
    if physical_doors:
        # The form chart's old rocker boundary is not a manufactured door
        # edge. Cut a real sill reveal in the same evaluated sheet before
        # separating/gauging it, retaining every exterior surface position.
        for z in [.300-S.PANEL_GAP/2,.300+S.PANEL_GAP/2]:
            fs=[f for f in bm.faces if names[f.material_index].startswith(('Door F','Door R','Rocker','Front fender','Rear quarter'))
                and S.DOOR_FRONT-.003<=f.calc_center_median().y<=S.DOOR_REAR+.003]
            es={e for f in fs for e in f.edges};vs={v for f in fs for v in f.verts}
            bmesh.ops.bisect_plane(bm,geom=list(vs)+list(es)+fs,dist=1e-8,plane_co=(0,0,z),plane_no=(0,0,1),clear_inner=False,clear_outer=False)
    discard=[]
    for f in bm.faces:
        label=names[f.material_index]
        if label in ['Trunk','Rear molded fascia']:
            p=f.calc_center_median();suffix='R' if p.x>0 else 'L'
            zsplit=.620-.022*(p.x/.90)**2
            if abs(p.z-zsplit)<S.PANEL_GAP/2-1e-7 or (p.z>zsplit and abs(abs(p.x)-.615)<S.PANEL_GAP/2-1e-7):discard.append(f);continue
            label=('Trunk' if abs(p.x)<.615 else 'Rear quarter_'+suffix) if p.z>zsplit else 'Rear molded fascia'
            f.material_index=names.index(label)
        elif label.startswith(('Door F','Door R','Front fender','Rear quarter')) or (physical_doors and label.startswith('Rocker')):
            p=f.calc_center_median();suffix='R' if p.x>0 else 'L'
            if any(abs(p.y-line)<S.PANEL_GAP/2-1e-7 for line in cuts) and (not physical_doors or p.z>.300-S.PANEL_GAP/2):discard.append(f);continue
            if physical_doors and S.DOOR_FRONT<p.y<S.DOOR_REAR:
                if abs(p.z-.300)<S.PANEL_GAP/2-1e-7:discard.append(f);continue
                label='Rocker_'+suffix if p.z<.300 else ('Door F' if p.y<S.DOOR_SPLIT else 'Door R')+'_'+suffix
            elif not label.startswith('Rocker'):
                label=('Front fender' if p.y<S.DOOR_FRONT else 'Door F' if p.y<S.DOOR_SPLIT else 'Door R' if p.y<S.DOOR_REAR else 'Rear quarter')+'_'+suffix
            f.material_index=names.index(label)
    bmesh.ops.delete(bm,geom=discard,context='FACES')
    bm.to_mesh(source.data);bm.free();source.data.update()
    source.data.calc_loop_triangles()
    # Preserve master vertex normals across face-group separation and shut lines.
    points=[v.co.copy() for v in source.data.vertices]
    normals=[]
    for p in points:
        hit,_,fi,_=parent_tree.find_nearest(p);ia,ib,ic=parent_triangles[fi]
        normals.append(barycentric_transform(hit,parent_points[ia],parent_points[ib],parent_points[ic],parent_normals[ia],parent_normals[ib],parent_normals[ic]).normalized())
    triangles=[tuple(t.vertices) for t in source.data.loop_triangles]
    tree=BVHTree.FromPolygons(points,triangles,all_triangles=True)
    pivots={}
    for side,sign in [('L',-1),('R',1)]:
        for end,y in [('F',S.DOOR_FRONT),('R',S.DOOR_SPLIT)]:
            piv=G.pivot('Door_'+end+side,(sign*.875,y,.74),'Z',(-72,0) if sign>0 else (0,72));piv.parent=b.root;pivots['Door '+end+'_'+side]=piv
    for name,y,z in [('Hood',-.990+S.CORE_SHIFT,.965),('Trunk',2.070+S.CORE_SHIFT,1.027)]:
        piv=G.pivot(name,(0,y,z),'X',(-65,0) if name=='Hood' else (0,75));piv.parent=b.root;pivots[name]=piv
    for index,name in enumerate(names):
        selected=[f for f in source.data.polygons if f.material_index==index]
        if not selected:continue
        used=sorted({i for f in selected for i in f.vertices});lookup={old:i for i,old in enumerate(used)}
        verts=[points[i].copy() for i in used];faces=[tuple(lookup[i] for i in f.vertices) for f in selected]
        glass=any(k in name for k in ['glass','Windshield','Backlight'])
        dark=any(k in name for k in ['applique','divider'])
        # 2.25 mm tangential edge setback creates panel reveals after the master
        # smoothing. No per-panel bevel or independent subdivision changes flow.
        edges={};adj={i:set() for i in range(len(used))}
        for face in faces:
            for a,c in zip(face,face[1:]+face[:1]):
                key=tuple(sorted((a,c)));edges[key]=edges.get(key,0)+1
                adj[a].add(c);adj[c].add(a)
        boundary={i for e,num in edges.items() if num==1 for i in e}
        centroids={i:[] for i in boundary}
        for f in faces:
            center=sum((verts[j] for j in f),Vector())/len(f)
            for i in f:
                if i in centroids:centroids[i].append(center)
        for i in boundary:
            p=verts[i];inside=centroids[i]
            # The lower nose and fender are one faired surface at the arch.
            # This chart boundary is not a manufactured parting line.
            if name.startswith(('Front molded fascia','Front fender')) and p.y<-1.50 and p.z<.700:continue
            if any(abs(abs(p.y-line)-S.PANEL_GAP/2)<2e-6 for line in cuts):continue
            if physical_doors and S.DOOR_FRONT<p.y<S.DOOR_REAR and abs(abs(p.z-.300)-S.PANEL_GAP/2)<2e-6:continue
            if p.y>1.80 and (abs(abs(abs(p.x)-.615)-S.PANEL_GAP/2)<2e-6 or abs(abs(p.z+.022*(p.x/.90)**2-.620)-S.PANEL_GAP/2)<.0003):continue
            if inside:
                tangent=(sum(inside,Vector())/len(inside)-p)
                n=normals[used[i]];tangent-=n*tangent.dot(n)
                if tangent.length>1e-8:
                    q=p+tangent.normalized()*S.PANEL_GAP/2
                    verts[i]=tree.find_nearest(q)[0]
        if glass:verts=[p-normals[old]*.002 for p,old in zip(verts,used)]
        mat=b.m['glass'] if glass else b.m['rubber'] if dark else b.m['body']
        ob=G.mesh(name+' outer' if name in ['Hood','Trunk'] else name,verts,faces,mat)
        for face in ob.data.polygons:face.use_smooth=True
        if name.startswith(('Front fender','Rear quarter','Door R','Front molded fascia','Rear molded fascia','Rocker')):
            for end,axle in [('F',S.FRONT_AXLE),('R',S.REAR_AXLE)]:
                if name.startswith(('Front fender','Front molded fascia')) and end!='F':continue
                if name.startswith(('Rear quarter','Rear molded fascia','Door R')) and end!='R':continue
                trim_arch(ob,axle,128 if b.high else 64)
                if not ob.data.polygons:raise ValueError(('Arch trim discarded panel',name,end))
        closeable_sheet(ob)
        sheet_gauge(ob,.0048 if glass else .003 if 'fascia' in name else .0009)
        category='glass' if glass else 'pillars' if dark or name.startswith('Greenhouse') else 'doors' if name.startswith('Door') else 'fascia' if 'fascia' in name else 'body'
        # Retain the continuous master normals after the sheet closing changes
        # its smoothing fans. The same field must survive the shut-line split.
        b.add(ob,pivots.get(name),category)
        G.smooth(ob,35)
        custom=[]
        inverse_normal=ob.matrix_world.to_3x3().transposed()
        for face in ob.data.polygons:
            face.use_smooth=True
            center=ob.matrix_world@face.center
            _,center_n,_,_=tree.find_nearest(center)
            role=face.material_index;face.use_smooth=role!=2
            for li in face.loop_indices:
                p=ob.matrix_world@ob.data.vertices[ob.data.loops[li].vertex_index].co
                hit,n,fi,distance=tree.find_nearest(p)
                ia,ib,ic=triangles[fi]
                n=barycentric_transform(hit,points[ia],points[ib],points[ic],normals[ia],normals[ib],normals[ic]).normalized()
                if role!=2:
                    custom.append(inverse_normal@(n if role==0 else -n))
                else:custom.append((0,0,0))
        ob.data.normals_split_custom_set(custom)
    bpy.data.objects.remove(source,do_unlink=True)
    # Actual inward arch flange follows the evaluated master, not a flat stuck-on ring.
    for side,sign in [('L',-1),('R',1)]:
        for end,axle in [('F',S.FRONT_AXLE),('R',S.REAR_AXLE)]:
            loops=[]
            segments=48 if b.high else 24
            angles=[-.31+(math.pi+.62)*i/segments for i in range(segments+1)]
            count=len(angles)
            for depth in [0,.018]:
                ring=[]
                for a in angles:
                    y=axle+S.ARCH_RADIUS*math.cos(a);z=S.HUB_HEIGHT+S.ARCH_RADIUS*math.sin(a)
                    hit=tree.ray_cast(Vector((sign*2,y,z)),Vector((-sign,0,0)),3)[0]
                    x=abs(hit.x) if hit else .89
                    ring.append((sign*(x-depth),y,z))
                loops.append(ring)
            ob=G.mesh('Arch flange_'+end+side,loops[0]+loops[1],[(i,i+1,count+i+1,count+i) for i in range(count-1)],b.m['body'])
            sol=ob.modifiers.new('Arch hem gauge','SOLIDIFY');sol.thickness=.001;sol.offset=-1;G.apply(ob);b.add(ob,category='arches')
            # Dark well, following the same real opening; interior detail deferred.
            inner_angles=angles[::2] if b.high else angles;count=len(inner_angles)
            inner_x=.48 if end=='F' else .56
            well_radius=S.ARCH_RADIUS+(.025 if end=='F' else .014)
            outer_x=.88 if end=='F' else .875
            verts=[(sign*x,axle+well_radius*math.cos(a),S.HUB_HEIGHT+well_radius*math.sin(a)) for x in [inner_x,outer_x] for a in inner_angles]
            fs=[(i,i+1,count+i+1,count+i) for i in range(count-1)]
            ob=G.mesh('Wheelwell_'+end+side,verts,fs,b.m['rubber']);sol=ob.modifiers.new('Liner thickness','SOLIDIFY');sol.thickness=.002;G.apply(ob);b.add(ob,category='liners')
            outline=[(axle+well_radius*math.cos(a),S.HUB_HEIGHT+well_radius*math.sin(a)) for a in inner_angles]
            b.add(G.profile('Wheelwell inboard_'+end+side,outline,sign*(inner_x-.001),sign*(inner_x+.001),b.m['rubber'],axis='X'),category='liners')
    fascia(b,front=True,master_tree=tree,surface_map=surface_map);fascia(b,front=False,master_tree=tree,surface_map=surface_map)
    # Only a cavity closure is supplied at this gate, not an interior or drivetrain.
    # This temporary blackout is inside the wheel wells and tucked end skins.
    # A full-width, long rectangle projected behind the curved lower tail and
    # looked like a diffuser plate. It is not the later underbody assembly.
    floor=G.box('Form cavity closure',(0,-.05,.220),(1.10,3.55,.100),b.m['rubber'],0);b.add(floor,category='closure')
    # Black end closures prevent a view through the unfinished cabin/underbody
    # to the opposite painted chin. Both lie beyond the tires' swept Y bounds.
    # The lower rear closure rolls forward and upward at its ends. A rectangular
    # black box here still reads as an aftermarket plate under the bumper.
    rings=[]
    for i in range(17):
        x=-.71+1.42*i/16;q=(x/.71)**2;bottom_q=(max(0,abs(x)-.50)/.21)**2
        rings.append([(x,y,z) for y,z in [(2.24-.25*q,.315+.01*q),(2.21-.25*q,.285+.015*q),
             (2.14-.22*q,.260+.035*bottom_q),(2.04-.20*q,.245+.050*bottom_q),(1.82,.240+.050*bottom_q),(1.82,.310+.010*q)]])
    b.add(G.loft('Rear form underbody closure',rings,b.m['rubber']),category='closure')
    handles(b)
    from sedan_character import mirrors
    mirrors(b)
    # Sample the dense parent directly. Re-interpolating the coarser game's
    # normal field after every pocket cut made triangular highlights along
    # otherwise fair rims, even when their positions remained on the sheet.
    tree=parent_tree;points=parent_points;normals=parent_normals;triangles=parent_triangles
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('part_category') not in ['body','doors','glass','pillars','fascia']:continue
        material=next((m for m in ob.data.materials if m),None)
        if material is None:raise ValueError(('Missing form material',ob.name,len(ob.data.vertices),len(ob.data.polygons)))
        if not b.high and ob.get('part_category')=='fascia':simplify_inner_gauge(ob,tree)
        G.smooth(ob,35);custom=[];inverse=ob.matrix_world.to_3x3().transposed()
        roles=ob.data.attributes.new('sheet_role','INT','FACE')
        for face in ob.data.polygons:
            center=ob.matrix_world@face.center;_,n,_,_=tree.find_nearest(center)
            role=face.material_index;roles.data[face.index].value=role;face.use_smooth=role!=2
            for li in face.loop_indices:
                p=ob.matrix_world@ob.data.vertices[ob.data.loops[li].vertex_index].co
                hit,n,fi,distance=tree.find_nearest(p);ia,ib,ic=triangles[fi]
                n=barycentric_transform(hit,points[ia],points[ib],points[ic],normals[ia],normals[ib],normals[ic]).normalized()
                custom.append(inverse@(n if role==0 else -n) if role!=2 else (0,0,0))
        ob.data.normals_split_custom_set(custom)
        ob.data.materials.clear();ob.data.materials.append(material)
        for face in ob.data.polygons:face.material_index=0


def locator_y_guess(x,z,front):
    sign=-1 if front else 1
    return sign*(S.LENGTH/2+END_ALLOWANCE[front]-locator_plan_guess(x,front)-face_depth(z,front))


def form_blank(name,rows,material,master_tree,front,axial=False):
    """A sampled, conforming blank; a single n-gon chords through the crown."""
    vertices=[];nu=len(rows[0])
    for row in rows:
        for guess in row:
            if axial:
                sign=-1 if front else 1
                hit,n,_,_=master_tree.ray_cast(Vector((guess[0],sign*4,guess[2])),Vector((0,-sign,0)),6)
                if hit is None or hit.y*sign<1.5:raise ValueError(('Fascia guide missed end skin',name,guess))
            else:hit,n,_,_=master_tree.find_nearest(Vector(guess))
            if n.dot(Vector((hit.x,-.8 if front else .8,0)))<0:n.negate()
            offset=.0025 if front and abs(hit.x)<.25 else .004
            vertices.append(hit+n*offset)
    faces=[(j*nu+i,j*nu+i+1,(j+1)*nu+i+1,(j+1)*nu+i) for j in range(len(rows)-1) for i in range(nu-1)]
    ob=G.mesh(name,vertices,faces,material)
    hint=Vector((0,-1 if front else 1,0))
    if ob.data.polygons[0].normal.dot(hint)<0:
        for face in ob.data.polygons:face.flip()
    # Refine only cells whose chords enter the painted surface. A corner's
    # 20 mm roll can cross a dark locator even when all its vertices clear.
    # BMesh splits shared edges conformingly, retaining a closed gauge later.
    bm=bmesh.new();bm.from_mesh(ob.data);original_samples=[v.co.copy() for v in bm.verts]
    for _ in range(2):
        edges=set()
        for face in bm.faces:
            center=face.calc_center_median();hit,n,_,_=master_tree.find_nearest(center)
            if n.dot(Vector((hit.x,-.8 if front else .8,0)))<0:n.negate()
            if (center-hit).dot(n)<.0006:edges.update(face.edges)
        if not edges:break
        bm.edges.index_update()
        bmesh.ops.subdivide_edges(bm,edges=sorted(edges,key=lambda edge:edge.index),cuts=1,use_grid_fill=True)
        for v in bm.verts:
            hit,n,_,_=master_tree.find_nearest(v.co)
            if n.dot(Vector((hit.x,-.8 if front else .8,0)))<0:n.negate()
            offset=.0025 if front and abs(hit.x)<.25 else .004
            v.co=hit+n*offset
    # Projection at a tapered optical tip can collapse neighboring sample
    # rows onto a 30-micron edge. Weld below optical manufacturing tolerance
    # before closing the gauge; a six-face edge is not a valid lens blank.
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00010)
    bmesh.ops.triangulate(bm,faces=list(bm.faces))
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
    bad=[f for f in bm.faces if f.calc_area()<1e-11]
    if bad:bmesh.ops.delete(bm,geom=bad,context='FACES')
    loose=[v for v in bm.verts if not v.link_faces]
    if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
    conform_edges(bm)
    bm.verts.ensure_lookup_table();bm.verts.index_update()
    lookup=KDTree(len(bm.verts))
    for i,v in enumerate(bm.verts):lookup.insert(v.co,i)
    lookup.balance()
    vertices=[lookup.find(p)[0].copy() for p in original_samples]
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    # Optical guides are triangulated in the injective parent chart next.
    # Their projected Cartesian grid can fold at a thin tip; do not close that
    # temporary grid and then throw the gauge away in regularize_blank().
    if not name.startswith(('Headlamp opening','Taillamp opening')):
        closeable_sheet(ob)
        sol=ob.modifiers.new('Form blank gauge','SOLIDIFY');sol.thickness=.0015;sol.offset=-1;sol.use_even_offset=False
        G.apply(ob)
    used={i for f in ob.data.polygons for i in f.vertices};actual=KDTree(len(used))
    for j,i in enumerate(sorted(used)):actual.insert(ob.data.vertices[i].co,j)
    actual.balance();snapped=[actual.find(p)[0].copy() for p in vertices]
    ob['guide_snap_max_m']=max((p-q).length for p,q in zip(vertices,snapped))
    if ob['guide_snap_max_m']>.002:raise ValueError('Aperture projection lost its boundary')
    vertices=snapped
    ob['form_rows']=len(rows);ob['form_columns']=nu
    ob['aperture_samples']=[q for p in vertices for q in p]
    ob['fascia_axial']=axial
    return ob


def lamp_volume(b,front,sign,material,master_tree):
    path=[]
    # A 630 mm surface envelope including a 230 mm fender return. The top
    # follows the curved hood edge; the aperture tapers at its rear tip.
    if front:
        path=[(.570,0,.699,.150),(.60,0,.717,.145),(.69,0,.744,.125),
              (.77,0,.772,.110),(.845,-1.940,.798,.090),(.880,-1.840,.824,.075),
              (.902,-1.730,.847,.050),(.912,-1.675,.868,.022)]
    else:
        path=[(.300,0,.996,.055),(.48,0,.981,.115),(.66,0,.971,.172),
              (.78,0,.977,.184),(.852,0,.984,.182),(.886,2.110,.990,.166),
              (.910,1.965,1.002,.105),(.919,1.820,1.022,.024)]
    path=[(x,locator_y_guess(x,z,front) if y==0 else y,z,h) for x,y,z,h in path]
    dense=[]
    for index,(a,c) in enumerate(zip(path,path[1:])):
        ts=[0,.25,.5,.75] if index>=3 else [0,.5]
        dense.extend([tuple(a[k]+(c[k]-a[k])*t for k in range(4)) for t in ts])
    dense.append(path[-1])
    rows=[[(sign*x,y,z+h*(v-.5)) for x,y,z,h in dense] for v in [i/4 for i in range(5)]]
    if front:return [form_blank('Headlamp opening'+str(sign),rows,material,master_tree,front)]
    cut=.615
    # Insert a sample at either side of the physical lid reveal.
    paths=[]
    for inner in [True,False]:
        subset=[]
        for row in rows:
            keep=[p for p in row if (abs(p[0])<cut if inner else abs(p[0])>cut)]
            a,c=next((a,c) for a,c in zip(row,row[1:]) if abs(a[0])<=cut<=abs(c[0]))
            xx=cut+(-1 if inner else 1)*S.PANEL_GAP/2
            t=(xx-abs(a[0]))/(abs(c[0])-abs(a[0]));p=tuple(a[k]+(c[k]-a[k])*t for k in range(3))
            subset.append(keep+[p] if inner else [p]+keep)
        ob=form_blank('Taillamp opening'+str(sign)+(' lid' if inner else ' quarter'),subset,material,master_tree,False)
        ob['lamp_piece']='lid' if inner else 'quarter'
        paths.append(ob)
    return paths


def fascia(b,front,master_tree,surface_map):
    """Compound molding sampled across crown and vertical support sections."""
    sign=-1 if front else 1
    ob=bpy.data.objects['Front molded fascia' if front else 'Rear molded fascia']
    openings=([('Low wide grille',(0,-2.43,.640),(1.28,.34,.210),.018,.064),
               ('Lower intake',(0,-2.41,.325),(1.40,.32,.150),.018,.060),
               ('DRL pocket L',(-.780,-2.34,.465),(.205,.30,.155),.026,.042),
               ('DRL pocket R',(.780,-2.34,.465),(.205,.30,.155),.026,.042)] if front else
              [('Diffuser',(0,2.43,.335),(1.44,.32,.110),.035,.014),
               ('Plate pocket',(0,2.43,.865),(.330,.23,.180),.004,.031)])
    from sedan_character import well,bars
    for name,center,size,radius,depth in openings:
        rows=[];nu=16 if size[0]>1 else 8;r=radius*.7
        for j in range(5):
            zz=(j/4-.5)*(size[2]-.010);dz=max(0,abs(zz)-((size[2]-.010)/2-r))
            cut=r-math.sqrt(max(0,r*r-dz*dz));half=(size[0]-.010)/2-cut;z=center[2]+zz
            if name=='Low wide grille':half-=.155*(j/4)
            shift=0
            if name.startswith('DRL pocket'):
                half*=.55+.45*j/4
                shift=(1 if center[0]>0 else -1)*.020*(j/4-.5)
            rows.append([(center[0]+shift+(2*i/nu-1)*half,locator_y_guess(center[0]+shift+(2*i/nu-1)*half,z,front),z) for i in range(nu+1)])
            if name=='Diffuser':
                # The low edge rises gently into the quarter returns, leaving
                # a real molded border below the inserts rather than a plate.
                rows[-1]=[(x,y,zz+.025*(x/.72)**4*(1-j/4)) for x,y,zz in rows[-1]]
        backing=form_blank(name+' opening',rows,b.m['rubber'],master_tree,front,axial=True)
        b.add(backing,category='openings')
        ps=well(b,backing,surface_map,depth,front)
        if name=='Plate pocket':
            from sedan_character import plate_lamp
            plate_lamp(b,backing,ps)
        if name in ['Low wide grille','Lower intake']:bars(b,backing,ps,front)
        if not b.high:
            dec=backing.modifiers.new('Hidden pocket bed allocation','DECIMATE');dec.ratio=.65 if name=='Diffuser' else .20;G.apply(backing)
            G.smooth(backing,35)
    # Optical envelopes sit behind actual projected skin apertures. Their
    # reflectors, emitters and optical seats remain a later detail stage.
    lamps=[]
    from sedan_apertures import regularize_blank
    for side,sgn in [('L',-1),('R',1)]:
        for lamp in lamp_volume(b,front,sgn,b.m['glass'],master_tree):
            regularize_blank(lamp,surface_map,front,b.high)
            b.add(lamp,bpy.data.objects['Trunk'] if lamp.get('lamp_piece')=='lid' else None,category='openings');lamps.append(lamp)
    from sedan_apertures import carve
    carve(front,lamps,surface_map)
    if not front:
        from sedan_character import rear_trim
        rear_trim(b,master_tree)


def handles(b):
    for side,sign in [('L',-1),('R',1)]:
        for end,y in [('F',-.02),('R',1.08)]:
            # Recess proxy only; full handle and latch construction is deferred.
            pocket=G.box('Handle opening_'+end+side,(sign*.911,y+S.CORE_SHIFT,.945 if end=='F' else .995),(.006,.155,.032),b.m['rubber'],.010,1)
            b.add(pocket,bpy.data.objects['Door_'+end+side],category='openings')
