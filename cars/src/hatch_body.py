"""H120: one connected regular quad control sheet, evaluated before cuts.

Hood, fenders, doors, canopy, liftgate and molded ends share one parent.
All coordinates are original die controls; no reference image is loaded here.
Panel separation and real openings happen only after Catmull-Clark evaluation.
"""
import math,json
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
from mathutils.geometry import barycentric_transform
from kit import model as G
import hatch_spec as S
END_ALLOWANCE={True:.025,False:.015}


def positive(q,r=.006):return .5*(q+math.sqrt(q*q+r*r))
def smoothstep(a,b,q):
    t=max(0,min(1,(q-a)/(b-a)));return t*t*t*(10-15*t+6*t*t)
def longitudinal(y):return y

def side_station(y,t):
    # Keep transverse controls in one longitudinal plane at the hood/cowl
    # transition. The old swept rows became parallel in YZ as their crown
    # height dropped, folding the fitted chart back over the fender itself.
    straight=smoothstep(-1.75,-1.35,y)*(1-smoothstep(-1.02,-.75,y))
    return y*(1-.30*t*(1-straight))

def face_depth(z,front):
    """Physical centerline: low tucked nose; upright gate over a rolled bumper."""
    if front:
        q=z-.705
        return (.10*q*q/max(.20,1-.80*q)+.60*positive(.260-z,.010)**2/.10
                +.0015*(1-smoothstep(.55,.65,z)))
    q=z-.550
    # The lower 140 mm rolls under; the gate above the bumper is almost upright.
    return (.30*q*q+.10*positive(.410-z,.015)**2/.18+.55*positive(z-.980,.015)
            +.080*smoothstep(.98,1.075,z)+.015*smoothstep(.68,.85,z)+.020*smoothstep(1.05,1.20,z))

def locator_plan_guess(x,front):return (.325 if front else .205)*(x/.8975)**2

def side_width(y):
    return .8700+.028*sum(math.exp(-((y-a)/.38)**2) for a in [S.FRONT_AXLE,S.REAR_AXLE])

def shoulder_height(y):return .891+.012*y

def character_height(y):return .405+.082*(y-S.DOOR_FRONT)/(S.DOOR_REAR-S.DOOR_FRONT)

def side_draw(y,z):
    h=shoulder_height(y);line=character_height(y)
    d=positive(h-z,.002);tail=positive(d-(h-line),.006);c=d-tail
    lower=-.065*c-.225*c*c-.120*tail
    # The stamped door hollow dies into the rear wheel's trailing shoulder;
    # it must not emboss another horizontal ripple into the molded bumper.
    # Give the door hollow enough turn to reflect the sky at its lower edge.
    # Fade the extra draw into the wheel openings; the molded ends retain
    # their accepted relief instead of inheriting a deeper bumper crease.
    extra=.0020+.0010*smoothstep(-.40,.80,y)
    hollow=.0070+extra*smoothstep(-1.03,-.75,y)*(1-smoothstep(1.02,1.30,y))
    lower-=hollow*math.exp(-((z-line-.038)/.026)**2)*(1-smoothstep(1.60,1.97,y))
    lower-=.50*positive(.280-z,.008)
    upper=-.37*positive(z-h,.002)-.12*positive(z-h,.002)**2
    # Raised wheel crowns blend in section as well as along the car. Preserve
    # the arch edge and widest shoulder, accentuating the metal between them.
    wheel=sum(math.exp(-((y-a)/.34)**2) for a in [S.FRONT_AXLE,S.REAR_AXLE])
    swell=.004*wheel*math.exp(-((z-(h-.065))/.045)**2)
    return lower+upper+swell

def hood_draw_x(y):return .515+.235*max(0,min(1,(y+1.98)/.935))
def hood_height(x,y):
    crown=.039*math.exp(-((abs(x)-.850)/.055)**2)*math.exp(-((y+1.34)/.63)**4)
    t=max(0,min(1,(y+1.990)/.890))
    return .746+.231*(y+1.990)+.022*math.sin(math.pi*t)-.024*(x/.775)**2-.065*positive(abs(x)-hood_draw_x(y),.018)+crown

# y / belt / center crown. The roof stays level almost to the liftgate hinge.
STATIONS=[
 (-1.075,.951,.936),(-.995,.954,.952),(-.940,.958,.967),
 (-.885,.960,.992),(-.700,.964,1.098),(-.440,.969,1.245),
 (-.190,.975,1.387),(-.125,.977,1.422),(-.070,.978,1.439),
 (.150,.983,1.450),(.205,.984,1.452),(.245,.985,1.452),
 (.520,.991,1.452),(.850,.999,1.449),(1.070,1.004,1.445),
 (1.110,1.005,1.444),(1.290,1.009,1.438),(1.450,1.012,1.426),
 (1.510,1.014,1.414)]
# Translate the straight windscreen forward while retaining its accepted rake.
STATIONS=[(y-.105 if y<0 else y,belt,top-.022*smoothstep(1.12,1.51,y)) for y,belt,top in STATIONS]


def body_section(y,belt,top):
    belt=min(belt,top-.080)
    belt+=.050*smoothstep(-.80,1.35,y) if top>1.10 else 0
    belt=min(belt,top-.080)
    w=side_width(y);foot=w+side_draw(y,belt);roof_edge=foot-math.tan(math.radians(22.5))*(top-.045-belt)
    upper=top-.045;lower=min(belt+.018,upper-.012);h=min(shoulder_height(y),belt-.025);line=min(character_height(y),h-.060)
    half=[(0,y,top),(.35*w,y,top-.004),(.66*w,y,top-.014),
      (roof_edge-.026,y,top-.026),(roof_edge,y,upper),
      ((roof_edge+foot-.007)/2,y,(upper+lower)/2),(foot-.007,y,lower)]
    for i,z in enumerate([belt,h+.017,h,h-.023,h-.085,min(.665,h-.120),line+.050,line+.012,line-.020,.210]):
        t=max(0,(i-1)/8);yy=side_station(y,t)
        half.append((side_width(yy)+side_draw(y,z),yy,z))
    if top>1.15 and y<1.52:
        drop=.040*smoothstep(.40,1.40,y)
        half=[(x,yy,z-drop*(x/max(.1,roof_edge))**2) if i<=4 else (x,yy,z-drop*.5) if i==5 else (x,yy,z) for i,(x,yy,z) in enumerate(half)]
    half.insert(-1,(side_width(y)+side_draw(y,line-.055),side_station(y,.9),line-.055))
    return half

# Front/end controls run from the underbody boundary over the face to the hood.
FRONT_ROWS=[
 (-2.060,.165,-1.920),(-2.092,.205,-1.910),(-2.143,.300,-1.890),
 (-2.171,.400,-1.860),(-2.188,.475,-1.820),(-2.172,.525,-1.800),
 (-2.126,.595,-1.780),(-2.065,.670,-1.760),(-2.000,.743,-1.740),
 (-1.980,.756,-1.725),(-1.875,.775,-1.640),(-1.690,.810,-1.480),
 (-1.475,.850,-1.300),(-1.240,.895,-1.240)]
# Glass is on the steep folded portion. No sedan deck is retained.
REAR_ROWS=[
 (1.570,1.393,1.560),(1.605,1.365,1.585),(1.690,1.285,1.610),
 (1.785,1.185,1.635),(1.880,1.085,1.660),(1.925,1.035,1.685),
 (1.954,1.010,1.710),(1.980,.985,1.735),(2.070,.900,1.760),
 (2.130,.775,1.785),(2.172,.645,1.810),(2.188,.550,1.835),
 (2.173,.475,1.860),(2.140,.390,1.885),(2.070,.300,1.910),
 (1.985,.215,1.935)]
REAR_ROWS=[(y-.018*smoothstep(1.02,1.40,z),z-.018*smoothstep(1.02,1.40,z),tangent) for y,z,tangent in REAR_ROWS]


def end_section(row,front):
    yc,zc,tangent=row;w=side_width(tangent);bottom=.165 if front else .205
    if not front:
        # The backlight, quarters and upright gate keep identical chart rows.
        # Clamp every lower station below its predecessor, so the sheet never
        # folds back upward when the end descends through the shoulder.
        half=body_section(tangent,1.014,zc)
        for i,(x,y,z) in enumerate(half):
            y=yc+(tangent-yc)*min(1,(x/max(.82,w))**3)
            if i>=7:y=tangent*(1-.30*max(0,(i-8)/8))
            half[i]=(x,y,z)
        return half
    xs=[0,.28,.55,.735,.815,.860,.894,.913,.921]
    xs=[x*w/.921 for x in xs]
    # The rear glazing's cross crown stays shallow until the outboard D-pillar.
    topness=max(0,min(1,(zc-.67)/.075)) if front else 0
    result=[]
    for i,x in enumerate(xs):
        turn=1-math.sqrt(max(0,1-(x/w)**2))
        if not front and zc>1.00:
            # Frontward wrap at the outer D pillars, not a broad flat tail cap.
            y=yc+(tangent-yc)*turn
            z=zc-.031*(x/w)**2
        else:
            y=yc+(tangent-yc)*turn
            z=(zc-.004*(x/w)**2)*(1-topness)+hood_height(x,y)*topness
        result.append((x,y,z))
    outer_z=result[-1][2]
    fractions=[0,.030,.080,.420,.640,.815,.845,.952,1]
    for j in range(1,9):
        t=j/8;yy=side_station(tangent,t)
        z=outer_z*(1-fractions[j])+bottom*fractions[j]
        result.append((side_width(yy)+side_draw(yy,z),yy,z))
    a,c=Vector(result[-2]),Vector(result[-1]);result.insert(-1,tuple(a.lerp(c,.15)))
    return result


def crease_rows(half,hood):
    a,p,c=[Vector(q) for q in half[1:4]]
    if hood:
        x=hood_draw_x(p.y);result=[]
        for xx in [x-.014,x,x+.014]:
            t=(xx-a.x)/(c.x-a.x);yy=a.y+(c.y-a.y)*t
            result.append((xx,yy,hood_height(xx,yy)))
        half=[(x,y,hood_height(x,y)) if i<=3 else (x,y,z) for i,(x,y,z) in enumerate(half)]
    else:result=[tuple(a.lerp(p,.60)),tuple(p),tuple(p.lerp(c,.45))]
    return half[:2]+result+half[3:]


def region(y,c):
    if 4<=c<=5 and -.990<y<1.290:
        if .205<y<.245:return 'B applique'
        if 1.070<y<1.110:return 'C divider'
        if y<.205:return 'Front side glass'
        if y<1.070:return 'Rear side glass'
        return 'Quarter glass'
    if c<=2 and -1.100<y<-.230:return 'Windshield'
    if c<=2:return 'Hood' if y<-1.100 else 'Roof'
    if c>=15:return 'Rocker'
    if c>=6:
        if S.DOOR_FRONT<y<S.DOOR_SPLIT:return 'Door F'
        if S.DOOR_SPLIT<y<S.DOOR_REAR:return 'Door R'
        return 'Front fender' if y<0 else 'Rear quarter'
    return 'Greenhouse'


def gate_crease_height(x):
    return .905-.025*(x/.640)**2


def gate_relief(x,z):
    hollow=.0485*math.exp(-((z-.835)/.047)**2)*math.exp(-(x/.320)**4)
    # A narrow die ridge bounds the retained concavity below the lamps. Its
    # ends follow the lamps' lower sweep; this is formed into the same skin.
    q=z-gate_crease_height(x)
    ridge=.45*(positive(q+.020,.003)-2*positive(q,.003)+positive(q-.020,.003))
    return hollow-ridge*(1-smoothstep(.50,.75,abs(x)))


def section_field(p):
    x,y,z=p
    bumper=.055*math.exp(-((y+1.98)/.50)**2-((z-.48)/.16)**2)+.042*math.exp(-((y-1.98)/.52)**2)*(1-smoothstep(.60,.82,z))
    width=side_width(y)+side_draw(y,z)+bumper
    ft=-1.560;rt=1.660-.32*smoothstep(1.0,1.40,z)
    fd=max(.15,S.LENGTH/2+.0055+ft-face_depth(z,True))
    gate=gate_relief(x,z)
    # The lower hem retains the accepted envelope. Its shadow comes from an
    # inset bumper shoulder beneath it, not a bolt-on lip outside the package.
    bumper_crease=.045*math.exp(-((z-.610)/.034)**2)*(1-smoothstep(.60,.88,abs(x)))
    rd=max(.15,S.LENGTH/2+.0005-rt-face_depth(z,False)-gate-bumper_crease)
    a=max(0,ft-y)/fd;c=max(0,y-rt)/rd
    # Keep the fuller accepted lower-bumper plan while blending its corners
    # into the sculpted gate; changing the entire rear moved the upper profile.
    rear_power=4.55-1.55*smoothstep(.65,1.40,z)+1.65*(1-smoothstep(.56,1.0,z))
    q=(x/width)**2+a**3+c**rear_power-1
    gradient=math.sqrt((2*x/(width*width))**2+(3*a*a/fd if y<ft else rear_power*c**(rear_power-1)/rd)**2)
    wall=q/max(1,gradient)
    top=z-hood_height(x,y) if y<-.995 else -2
    r=.012;m=max(wall,top)
    return m+r*math.log(math.exp((wall-m)/r)+math.exp((top-m)/r))


def fit_control_net(ob):
    sub=ob.modifiers.new('Refine section-fit controls','SUBSURF');sub.levels=3;G.apply(ob)
    parameter_u=[0.]*len(ob.data.vertices)
    for loop in ob.data.loops:parameter_u[loop.vertex_index]=ob.data.uv_layers.active.data[loop.index].uv.x
    center_u=(ob['grid_width']-1)/2
    for v in ob.data.vertices:
        p=v.co
        # Preserve roof and glass's compound crown. Fit doors/ends underneath.
        u=abs(parameter_u[v.index]-center_u)
        side_weight=smoothstep(6.0,9.5,u)
        # A 20 mm handoff displaced the hood controls by almost their own
        # spacing and folded the cowl patch. Spread that positional blend
        # across the hood; the untouched windshield starts at the same end.
        front_weight=1-smoothstep(-1.200,-1.080,p.y)
        rear_weight=smoothstep(1.48,1.70,p.y)
        weight=1-(1-side_weight)*(1-front_weight)*(1-rear_weight)
        if weight<1e-9:continue
        # Blend the fitting ray's origin as continuously as the sheet itself.
        # A hard side/end switch at y=1.60 produced a small D-pillar pinch even
        # though every point lay on the requested section field.
        wf=1-smoothstep(-.995,-.975,p.y);wr=smoothstep(1.25,1.90,p.y)
        cy=p.y*(1-wf-wr)-1.30*wf+1.30*wr
        cz=p.z*(1-wf-wr)+.43*wf+.55*wr
        center=Vector((0,cy,cz))
        direction=p-center;lo,hi=0.,2.
        for _ in range(30):
            t=(lo+hi)/2
            if section_field(center+direction*t)>0:hi=t
            else:lo=t
        v.co=p.lerp(center+direction*((lo+hi)/2),weight)
    ob.data.update()


def master(level):
    n=20;verts=[];faces=[];labels=[];rows=[];kinds=[]
    for row in FRONT_ROWS:rows.append(crease_rows(end_section(row,True),row[1]>.72));kinds.append(('front',row[0]))
    for row in STATIONS:rows.append(crease_rows(body_section(*row),row[0]<-1.100));kinds.append(('body',row[0]))
    for row in REAR_ROWS:rows.append(crease_rows(end_section(row,False),False));kinds.append(('rear',row[0]))
    for half in rows:
        assert len(half)==n,len(half)
        verts.extend([(-x,y,z) for x,y,z in reversed(half[1:])]+half)
    width=2*n-1
    for j in range(len(rows)-1):
        kind,y=kinds[j];next_kind,yn=kinds[j+1];y=(y+yn)/2
        for i in range(width-1):
            c=i-(n-1) if i>=n-1 else (n-2)-i
            c=c if c<2 else 2 if c<5 else c-2
            side='R' if i>=n-1 else 'L'
            if kind=='body' and next_kind=='body':label=region(y,c)
            elif kind=='front':label='Front molded fascia' if j<8 else 'Hood' if c<=2 else 'Front fender'
            elif kind=='rear':
                ri=j-len(FRONT_ROWS)-len(STATIONS)
                label=('Backlight' if ri<5 else 'Liftgate') if c<=2 else 'Rear quarter'
                if ri>=10:label='Rear molded fascia'
            else:label='Backlight' if c<=2 else 'Rear quarter'
            if label in ['Front fender','Rear quarter'] or (kind=='body' and label not in ['Hood','Roof','Windshield','Backlight']):label+='_'+side
            labels.append(label);faces.append((j*width+i,j*width+i+1,(j+1)*width+i+1,(j+1)*width+i))
    ob=G.mesh('Hatch unified subdivision cage',verts,faces);names=sorted(set(labels))
    for name in names:ob.data.materials.append(bpy.data.materials.new('Cage region '+name))
    for face,label in zip(ob.data.polygons,labels):face.material_index=names.index(label);face.use_smooth=True
    uv=ob.data.uv_layers.new(name='Surface parameters')
    for f in ob.data.polygons:
        for li in f.loop_indices:
            vi=ob.data.loops[li].vertex_index;uv.data[li].uv=(vi%width,vi//width)
    ob['grid_width']=width;ob['grid_rows']=len(rows)
    fit_control_net(ob)
    bm=bmesh.new();bm.from_mesh(ob.data);quads=sum(len(f.verts)==4 for f in bm.faces)
    assert quads==len(bm.faces) and all(len(v.link_edges)==4 for v in bm.verts if not v.is_boundary)
    unseen=set(bm.verts);components=0
    while unseen:
        components+=1;stack=[unseen.pop()]
        while stack:
            for e in stack.pop().link_edges:
                for v in e.verts:
                    if v in unseen:unseen.remove(v);stack.append(v)
    ob['cage_report']=json.dumps(dict(vertices=len(bm.verts),quads=quads,connected_components=components,interior_valence_four=True,fit='Control vertices only; no evaluated projection'))
    bm.free();sub=ob.modifiers.new('Fair continuous quad sheet','SUBSURF');sub.levels=level;sub.render_levels=level;G.apply(ob)
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
    step=.25 if high else 1.0
    us=sorted(set([i*step for i in range(round((width-1)/step)+1)]+[u+d for u in [(width-1)/2-10,(width-1)/2+10] for d in [-.75,-.25,.25,.75]]))
    vs=sorted(set(list(range(rows))+[j+.5 for j in range(rows-1) if high or j in [2,3,4,5,6] or j>=rows-19]))
    if not high:
        rear_start=len(FRONT_ROWS)+len(STATIONS)
        vs=sorted(set(vs+[rear_start+j/4 for j in [39,41,43,45]]))
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
    if not high:
        # Resolve the gate's designed top edge in the actual surface, instead
        # of spreading its normal transition across a broad diagonal chord.
        center=(width-1)/2;rear_start=len(FRONT_ROWS)+len(STATIONS)
        for z in [.875,.895,.905,.915,.935]:
            lo,hi=rear_start+5,rear_start+10
            for _ in range(20):
                mid=(lo+hi)/2;p,_=sample(center,mid)
                if p.z>z:lo=mid
                else:hi=mid
            v=(lo+hi)/2
            vs=[old for old in vs if abs(old-v)>.08]+[v]
        vs=sorted(vs)
    # Spend the extra transverse samples on the rear turn, not across every
    # door. One stitched transition uses triangles; the parent stays all quads.
    center=(width-1)/2
    extra=[center+sign*(5.25+j*.25) for sign in [-1,1] for j in range(15)]
    coarse=sorted(set([float(i) for i in range(width)] + [center+d for d in [-16.5,-15.5,15.5,16.5]]+[u+d for u in [(width-1)/2-10,(width-1)/2+10] for d in [-.75,-.25,.25,.75]]+[min(us),max(us)]))
    # Broad central canopy needs fewer chords than a tight bumper turn.
    coarse=[u for u in coarse if abs(u-center)>=5 or abs(u-center)%2<1e-7]
    grids=[(sorted(set(us+extra)) if v>=rows-19 or v<8 else us if v<13 else coarse) if not high else us for v in vs]
    if not high:
        lamp_corner=[center+sign*(2.25+j*.25) for sign in [-1,1] for j in range(15)]
        grids=[sorted(set(columns+lamp_corner)) if 7<=v<14 else columns for v,columns in zip(vs,grids)]
        gate_center=[center+sign*j*.25 for sign in [-1,1] for j in range(1,9)]
        rear_start=len(FRONT_ROWS)+len(STATIONS)
        grids=[sorted(set(columns+gate_center)) if rear_start+6<=v<=rear_start+11 else columns for v,columns in zip(vs,grids)]
        # Place samples on each side of the actual shoulder and die-line turn.
        # Coarse chart rows previously interpolated a sharp parent normal over
        # a broad door chord, erasing the line in the game surface.
        for row,v in enumerate(vs):
            if not 11<=v<rows-9:continue
            added=[]
            for feature,offset in [('shoulder',-.018),('shoulder',0),('shoulder',.018),
                                   ('lower',.010),('lower',.037),('lower',.065)]:
                lo,hi=center+8,center+18
                for _ in range(18):
                    mid=(lo+hi)/2;p,_=sample(mid,v)
                    target=(shoulder_height(p.y) if feature=='shoulder' else character_height(p.y))+offset
                    if p.z>target:lo=mid
                    else:hi=mid
                u=(lo+hi)/2;p,_=sample(u,v)
                if abs(p.y)<1.75 and p.x>.80 and center+8.01<u<center+17.99:
                    added.extend([u,2*center-u])
            # Replace nearby chart samples rather than adding nearly coincident
            # sliver cells. Every replacement is sampled on the same parent.
            grids[row]=sorted([u for u in grids[row] if not any(abs(u-q)<.14 for q in added)]+added)
        for row,v in enumerate(vs):
            added=[]
            for a,c in zip(grids[row],grids[row][1:]):
                if c-a<.40:continue
                u=(a+c)/2;p,_=sample(u,v)
                corner=abs(p.x)>.65 and (p.y>1.75 and p.z<.78 or p.y<-1.75 and .66<p.z<.84)
                if corner:added.append(u)
            grids[row]=sorted(grids[row]+added)
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
        # Refine the lower rear turn and the tight hood/lamp junction in BOTH
        # chart directions. Transverse samples alone leave a long chord at
        # the inner lamp corner, visible as a pinched rim in the front view.
        # Adjacent polygons share inserted midpoints, so there are no T cracks.
        selected=set();edges={}
        for fi,face in enumerate(faces):
            p=sum((vertices[i] for i in face),Vector())/len(face)
            rear_turn=1.76<p.y<1.99 and .35<p.z<.55 and abs(p.x)>.80
            lamp_corner=p.y<-2.0 and .69<p.z<.78 and .48<abs(p.x)<.69
            cowl=False
            if .65<abs(p.x) and -1.65<p.y<-1.02 and p.z>.75:
                u=sum(chart[i][0] for i in face)/len(face);v=sum(chart[i][1] for i in face)/len(face)
                q,fi_parent=sample(u,v)
                # Tangential chart stretch is not a shape error. Refine only
                # the missed normal height on hood/fender skins.
                label=mesh.materials[mesh.polygons[fi_parent].material_index].name
                cowl=('Hood' in label or 'Front fender' in label) and abs((q-p).dot(mesh.polygons[fi_parent].normal))>.0015
            if len(face) in [3,4] and (rear_turn or lamp_corner or cowl):
                selected.add(fi)
                for a,b in zip(face,face[1:]+face[:1]):edges[tuple(sorted((a,b)))]=None
        for edge in edges:
            a,b=edge;u=(chart[a][0]+chart[b][0])/2;v=(chart[a][1]+chart[b][1])/2
            edges[edge]=len(vertices);vertices.append(sample(u,v)[0]);chart.append((u,v))
        refined=[]
        for fi,face in enumerate(faces):
            if fi in selected:
                if len(face)==3:
                    a,b,c=face
                    ab,bc,ca=[edges[tuple(sorted(pair))] for pair in [(a,b),(b,c),(c,a)]]
                    refined.extend([(a,ab,ca),(ab,b,bc),(ca,bc,c),(ab,bc,ca)])
                    continue
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


def conform_edges(bm,tolerance=5e-7):
    """Split shared edges at clipping-generated T vertices before sheet closing."""
    bm.verts.ensure_lookup_table();bm.verts.index_update();verts=list(bm.verts)
    kd=KDTree(len(verts))
    for i,v in enumerate(verts):kd.insert(v.co,i)
    kd.balance();weld={}
    for edge in list(bm.edges):
        a,c=edge.verts;delta=c.co-a.co;length=delta.length
        if length<2*tolerance:continue
        candidates=[]
        for co,index,_ in kd.find_range((a.co+c.co)/2,length/2+2*tolerance):
            v=verts[index]
            if v==a or v==c:continue
            t=(co-a.co).dot(delta)/(length*length)
            if 1e-5<t<1-1e-5 and (co-a.co-delta*t).length<tolerance:candidates.append((t,v))
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


def closeable_sheet(ob,weld=True):
    """Remove clipping crumbs and split point-touching surface fans.

    Two sheet regions touching at a single vertex need independent gauge rims;
    otherwise Solidify joins both rims onto one four-face non-manifold edge.
    No surface point is moved by the fan split.
    """
    bm=bmesh.new();bm.from_mesh(ob.data)
    if weld:bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
    bad=[f for f in bm.faces if f.calc_area()<1e-12]
    if bad:bmesh.ops.delete(bm,geom=bad,context='FACES')
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



def simplify_inner_gauge(ob,tree):
    """Reduce unseen gauge backs without touching exposed skin or cut rims.

    Only edges whose entire vertex fans face inward are eligible. This saves
    the doubled tessellation of the thickness backs for exterior reflections.
    """
    bm=bmesh.new();bm.from_mesh(ob.data);bm.normal_update()
    matrix=ob.matrix_world;inverse_normal=matrix.to_3x3().transposed()
    inward=set()
    for f in bm.faces:
        _,n,_,_=tree.find_nearest(matrix@f.calc_center_median())
        if f.normal.dot(inverse_normal@n)<-.7:inward.add(f)
    bm.verts.index_update()
    pure={v for v in bm.verts if v.link_faces and all(f in inward for f in v.link_faces)}
    edges=[e for e in bm.edges if all(v in pure for v in e.verts) and len(e.link_faces)==2]
    bmesh.ops.dissolve_limit(bm,angle_limit=math.radians(2),verts=sorted(pure,key=lambda v:v.index),edges=edges,use_dissolve_boundaries=False,delimit={'MATERIAL'})
    # Curved inner chords must stay inside the painted sheet. Concave regions
    # can cross a sub-millimeter gauge despite small dihedral angles; reject
    # the whole reduction if centroid/edge probes lose 0.4 mm of inward depth.
    maximum=-1.
    for loops in bm.calc_loop_triangles():
        center=sum((loop.vert.co for loop in loops),Vector())/3
        _,n,_,_=tree.find_nearest(matrix@center)
        if loops[0].face.normal.dot(inverse_normal@n)>-.7:continue
        ps=[loop.vert.co for loop in loops]
        for q in [center]+[(a+c)/2 for a,c in zip(ps,ps[1:]+ps[:1])]:
            q=matrix@q;hit,n,_,_=tree.find_nearest(q)
            maximum=max(maximum,(q-hit).dot(n))
    ob['inner_gauge_probe_depth_m']=-maximum
    ob['inner_gauge_reduced']=maximum<=-.0004
    if ob['inner_gauge_reduced']:bm.to_mesh(ob.data)
    bm.free();ob.data.update()


def remove_buried_backs(ob,tree):
    """Fixed skins retain their visible surface and cut-edge gauge returns.

    Their buried reverse tessellation is replaced later by cabin/bumper liners,
    not drawn twice beneath those liners. Moving closures keep closed gauge.
    The resulting boundaries are explicitly tagged and separately audited.
    """
    bm=bmesh.new();bm.from_mesh(ob.data);bm.faces.ensure_lookup_table()
    matrix=ob.matrix_world;normal_matrix=matrix.to_3x3().inverted().transposed()
    outer_count=ob['outer_skin_faces'];remove=[]
    role=bm.faces.layers.int.new('hatch_outer_skin')
    for face in bm.faces:face[role]=int(face.index<outer_count)
    for face in bm.faces:
        if face.index<outer_count:continue
        if any(other[role] for edge in face.edges for other in edge.link_faces):continue
        _,n,_,_=tree.find_nearest(matrix@face.calc_center_median())
        if (normal_matrix@face.normal).dot(n)<-.65:remove.append(face)
    removed_triangles=sum(len(f.verts)-2 for f in remove)
    bmesh.ops.delete(bm,geom=remove,context='FACES')
    # All painted parent faces are still present; only reverse-facing gauge
    # faces were eligible. No decimation or movement of the outer skin occurs.
    if any(len(e.link_faces)>2 for e in bm.edges):raise ValueError('Non-manifold fixed stamping: '+ob.name)
    bm.to_mesh(ob.data);bm.free();ob.data.update()
    ob['allow_boundary']=True
    ob['boundary_reason']='Buried reverse skin omitted; visible skin and gauge returns retained'
    ob['removed_hidden_triangles']=removed_triangles


def build(b):
    print('HATCH master',flush=True)
    source,names=master(2)
    print('HATCH sample/cut',flush=True)
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
    surface_map=dict(tree=parent_tree,points=parent_points,normals=parent_normals,triangles=parent_triangles,uvs=parent_uvs,high=b.high)
    bm=bmesh.new();bm.from_mesh(source.data)
    cuts=[S.DOOR_FRONT,S.DOOR_SPLIT,S.DOOR_REAR]
    for line in cuts:
        for y in [line-S.PANEL_GAP/2,line+S.PANEL_GAP/2]:
            bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),
                dist=1e-8,plane_co=(0,y,0),plane_no=(0,1,0),clear_inner=False,clear_outer=False)
    for axis,line in [(0,-.640),(0,.640),(2,.645)]:
        for offset in [-S.PANEL_GAP/2,S.PANEL_GAP/2]:
            co=[0.,0.,0.];no=[0.,0.,0.];co[axis]=line+offset;no[axis]=1.
            bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-8,plane_co=co,plane_no=no,clear_inner=False,clear_outer=False)
    # Glazing is trimmed on the fair sheet. The rear side pane terminates
    # on a swept D-pillar, while the rear glass has its own tapered aperture.
    for co,no in [((1.18,0,0),(1,0,.43)),((-1.18,0,0),(-1,0,.43)),((0,2.08,0),(0,1,.58))]:
        bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-8,plane_co=co,plane_no=no,clear_inner=False,clear_outer=False)
    # The die boundary is underneath. Remove the buried projected end tails
    # before closing the sheet gauge; this is a physical trimmed lower edge.
    bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-8,plane_co=(0,0,.190),plane_no=(0,0,1),clear_inner=True,clear_outer=False)
    for sign in [-1,1]:
        bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-8,plane_co=(0,0,.070),plane_no=(-sign*.20,0,1),clear_inner=True,clear_outer=False)
    discard=[]
    for f in bm.faces:
        label=names[f.material_index];p=f.calc_center_median()
        if label=='Backlight' and abs(p.x)+.43*p.z>1.18:
            label='Greenhouse_'+('R' if p.x>0 else 'L');f.material_index=names.index(label)
        if 'glass_' in label and p.y+.58*p.z>2.08:
            label='Greenhouse_'+('R' if p.x>0 else 'L');f.material_index=names.index(label)
        if label in ['Liftgate','Rear molded fascia'] or (label.startswith('Rear quarter') and f.calc_center_median().y>1.67 and f.calc_center_median().z<1.01):
            p=f.calc_center_median();suffix='R' if p.x>0 else 'L'
            if abs(p.z-.645)<S.PANEL_GAP/2-1e-7 or (p.z>.645 and abs(abs(p.x)-.640)<S.PANEL_GAP/2-1e-7):discard.append(f);continue
            label=('Liftgate' if abs(p.x)<.640 else 'Rear quarter_'+suffix) if p.z>.645 else 'Rear molded fascia'
            f.material_index=names.index(label)
        elif label.startswith(('Door F','Door R','Front fender','Rear quarter')):
            p=f.calc_center_median();suffix='R' if p.x>0 else 'L'
            if any(abs(p.y-line)<S.PANEL_GAP/2-1e-7 for line in cuts):discard.append(f);continue
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
    incident_regions={i:set() for i in range(len(points))}
    for f in source.data.polygons:
        for vi in f.vertices:incident_regions[vi].add(names[f.material_index])
    def fixed_join(vi):
        regions=incident_regions[vi]
        return len(regions)>1 and all(n=='Roof' or n.startswith(('Greenhouse','Rear quarter','Front fender')) for n in regions)
    pivots={}
    for side,sign in [('L',-1),('R',1)]:
        for end,y in [('F',S.DOOR_FRONT),('R',S.DOOR_SPLIT)]:
            piv=G.pivot('Door_'+end+side,(sign*.875,y,.74),'Z',(-72,0) if sign>0 else (0,72));piv.parent=b.root;pivots['Door '+end+'_'+side]=piv
    for name,y,z in [('Hood',-1.100,.958),('Liftgate',1.510,1.414)]:
        piv=G.pivot(name,(0,y,z),'X',(-65,0) if name=='Hood' else (-95,0));piv.parent=b.root;pivots[name]=piv
        if name=='Liftgate':pivots['Backlight']=piv
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
            # Welded roof rail/quarter skin shares its parent edge. There is no
            # real shut line around a painted patch behind the quarter pane.
            if fixed_join(used[i]):continue
            if any(abs(abs(p.y-line)-S.PANEL_GAP/2)<2e-6 for line in cuts):continue
            if p.y>1.67 and (abs(abs(abs(p.x)-.640)-S.PANEL_GAP/2)<2e-6 or abs(abs(p.z-.645)-S.PANEL_GAP/2)<2e-6):continue
            if inside:
                tangent=(sum(inside,Vector())/len(inside)-p)
                n=normals[used[i]];tangent-=n*tangent.dot(n)
                if tangent.length>1e-8:
                    q=p+tangent.normalized()*S.PANEL_GAP/2
                    verts[i]=parent_tree.find_nearest(q)[0]
        if glass:verts=[p-normals[old]*.002 for p,old in zip(verts,used)]
        mat=b.m['glass'] if glass else b.m['rubber'] if dark else b.m['body']
        ob=G.mesh(name+' outer' if name in ['Hood','Liftgate'] else name,verts,faces,mat)
        for face in ob.data.polygons:face.use_smooth=True
        if name.startswith(('Front fender','Rear quarter','Door R','Front molded fascia','Rear molded fascia','Rocker')):
            for end,axle in [('F',S.FRONT_AXLE),('R',S.REAR_AXLE)]:
                if not name.startswith('Rocker') and (end=='F')!=name.startswith(('Front fender','Front molded fascia')):continue
                trim_arch(ob,axle,128 if b.high else 64)
                if not ob.data.polygons:raise ValueError(('Arch trim discarded panel',name,end))
        # The folded lower end can leave a disconnected clipping scrap below
        # the rocker. A door is one connected stamping; retain its largest
        # connected sheet and report the discarded area rather than sealing
        # hidden fragments into non-manifold gauge solids.
        if name.startswith('Door'):
            bm=bmesh.new();bm.from_mesh(ob.data);todo=set(bm.faces);groups=[]
            while todo:
                stack=[todo.pop()];group=list(stack)
                while stack:
                    for edge in stack.pop().edges:
                        for face in edge.link_faces:
                            if face in todo:todo.remove(face);stack.append(face);group.append(face)
                groups.append(group)
            groups.sort(key=lambda g:sum(f.calc_area() for f in g),reverse=True)
            scraps=[f for group in groups[1:] for f in group]
            ob['removed_disconnected_area_m2']=sum(f.calc_area() for f in scraps)
            if scraps:bmesh.ops.delete(bm,geom=scraps,context='FACES')
            bm.to_mesh(ob.data);bm.free()
        closeable_sheet(ob)
        ob['outer_skin_faces']=len(ob.data.polygons)
        gauge=ob.modifiers.new('Sheet gauge','SOLIDIFY');gauge.thickness=.0048 if glass else .004 if 'fascia' in name else .0009;gauge.offset=-1;gauge.use_even_offset=False
        G.apply(ob)
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
            if abs(face.normal.dot(inverse_normal@center_n))<.5:face.use_smooth=False
            for li in face.loop_indices:
                p=ob.matrix_world@ob.data.vertices[ob.data.loops[li].vertex_index].co
                hit,n,fi,distance=tree.find_nearest(p)
                ia,ib,ic=triangles[fi]
                n=barycentric_transform(hit,points[ia],points[ib],points[ic],normals[ia],normals[ib],normals[ic]).normalized()
                if distance<.008 and abs(face.normal.dot(inverse_normal@n))>.5:
                    custom.append(inverse_normal@(n if face.normal.dot(inverse_normal@n)>0 else -n))
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
            verts=[(sign*x,axle+(S.ARCH_RADIUS+.012)*math.cos(a),S.HUB_HEIGHT+(S.ARCH_RADIUS+.012)*math.sin(a)) for x in [.56,.88] for a in inner_angles]
            fs=[(i,i+1,count+i+1,count+i) for i in range(count-1)]
            ob=G.mesh('Wheelwell_'+end+side,verts,fs,b.m['rubber']);sol=ob.modifiers.new('Liner thickness','SOLIDIFY');sol.thickness=.002;G.apply(ob);b.add(ob,category='liners')
            outline=[(axle+(S.ARCH_RADIUS+.012)*math.cos(a),S.HUB_HEIGHT+(S.ARCH_RADIUS+.012)*math.sin(a)) for a in inner_angles]
            b.add(G.profile('Wheelwell inboard_'+end+side,outline,sign*.559,sign*.561,b.m['rubber'],axis='X'),category='liners')
    print('HATCH apertures',flush=True)
    fascia(b,front=True,master_tree=parent_tree,surface_map=surface_map);fascia(b,front=False,master_tree=parent_tree,surface_map=surface_map)
    # Only a cavity closure is supplied at this gate, not an interior or drivetrain.
    # This temporary blackout is inside the wheel wells and tucked end skins.
    # A full-width, long rectangle projected behind the curved lower tail and
    # looked like a diffuser plate. It is not the later underbody assembly.
    floor=G.box('Form cavity closure',(0,-.05,.260),(1.05,3.20,.018),b.m['rubber'],0);b.add(floor,category='closure')
    from hatch_character import mirrors
    mirrors(b)
    from hatch_character import spoiler
    spoiler(b,parent_tree)
    # Boolean aperture cuts can change the rim smoothing fans again. Reapply the
    # pre-cut master field to every exposed outer corner, with flat gauge edges.
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('part_category') not in ['body','doors','glass','pillars','fascia']:continue
        material=next((m for m in ob.data.materials if m),None)
        if material is None:raise ValueError(('Missing form material',ob.name,len(ob.data.vertices),len(ob.data.polygons)))
        ob.data.materials.clear();ob.data.materials.append(material)
        for face in ob.data.polygons:face.material_index=0
        if not b.high and ob.parent==b.root and ob.get('part_category') in ['body','fascia','pillars']:
            remove_buried_backs(ob,parent_tree)
        if ob.name=='Rear molded fascia':
            # Material construction boundary on the parent sheet: Corolla-like
            # black lower center, leaving the painted upper band and corners.
            bm=bmesh.new();bm.from_mesh(ob.data)
            planes=[((0,0,.570),(0,0,1))]
            for sign in [-1,1]:
                planes += [((sign*.850,0,0),(sign,0,.35)),((sign*1.130,0,0),(sign,0,.90))]
            for co,no in planes:
                faces=[f for f in bm.faces if no[0]==0 or min(v.co.z for v in f.verts)<.57001]
                verts={v for f in faces for v in f.verts};edges={e for f in faces for e in f.edges}
                bm.verts.index_update();bm.edges.index_update()
                bmesh.ops.bisect_plane(bm,geom=sorted(verts,key=lambda v:v.index)+sorted(edges,key=lambda e:e.index)+faces,dist=1e-8,plane_co=co,plane_no=no,clear_inner=False,clear_outer=False)
            bm.to_mesh(ob.data);bm.free()
        G.smooth(ob,35);custom=[];inverse=ob.matrix_world.to_3x3().transposed()
        for face in ob.data.polygons:
            center=ob.matrix_world@face.center;_,n,_,_=tree.find_nearest(center)
            face.use_smooth=abs(face.normal.dot(inverse@n))>.5
            for li in face.loop_indices:
                p=ob.matrix_world@ob.data.vertices[ob.data.loops[li].vertex_index].co
                hit,n,fi,distance=parent_tree.find_nearest(p);ia,ib,ic=parent_triangles[fi]
                n=barycentric_transform(hit,parent_points[ia],parent_points[ib],parent_points[ic],parent_normals[ia],parent_normals[ib],parent_normals[ic]).normalized()
                dot=face.normal.dot(inverse@n)
                custom.append(inverse@(n if dot>0 else -n) if distance<.010 and abs(dot)>.5 else (0,0,0))
        ob.data.normals_split_custom_set(custom)
        if ob.name=='Rear molded fascia':
            ob.data.materials.append(b.m['rubber'])
            for face in ob.data.polygons:
                p=ob.matrix_world@face.center
                if p.z<.570 and abs(p.x)+.35*p.z<.850 and abs(p.x)+.90*p.z<1.130:
                    face.material_index=1


def locator_y_guess(x,z,front):
    sign=-1 if front else 1
    return sign*(S.LENGTH/2+END_ALLOWANCE[front]-locator_plan_guess(x,front)-face_depth(z,front))


def form_blank(name,rows,material,master_tree,front):
    """A sampled, conforming blank; a single n-gon chords through the crown."""
    vertices=[];nu=len(rows[0])
    def locate(p):
        if name.startswith('Diffuser'):
            hit,n,fi,d=master_tree.ray_cast(Vector((p[0],3,p[2])),Vector((0,-1,0)),6)
            if hit is None:raise ValueError(('Diffuser axial projection missed',tuple(p)))
            return hit,n,fi,d
        return master_tree.find_nearest(Vector(p))
    for row in rows:
        for guess in row:
            hit,n,_,_=locate(guess)
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
            hit,n,_,_=locate(v.co)
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
    return ob


def lamp_volume(b,front,sign,material,master_tree):
    """Original rising front blades / broad split rear wings, on the parent."""
    if front:
        path=[(.590,0,.700,.170),(.64,0,.724,.160),(.72,0,.756,.140),
              (.80,-1.800,.798,.105),(.848,-1.690,.824,.085),
              (.873,-1.590,.850,.050),(.881,-1.510,.870,.020)]
    else:
        path=[(.335,0,.938,.055),(.48,0,.946,.095),(.64,0,.952,.140),
              (.75,0,.959,.160),(.824,0,.966,.145),(.866,1.880,.976,.115),
              (.884,1.765,.984,.080),(.890,1.670,.991,.025)]
    path=[(x,locator_y_guess(x,z,front) if y==0 else y,z,h) for x,y,z,h in path]
    dense=[]
    for a,c in zip(path,path[1:]):
        dense.extend(tuple(a[k]+(c[k]-a[k])*t for k in range(4)) for t in [0,.5])
    dense.append(path[-1]);rows=[[(sign*x,y,z+h*(v-.5)) for x,y,z,h in dense] for v in [i/4 for i in range(5)]]
    if front:return [form_blank('Headlamp opening'+str(sign),rows,material,master_tree,front)]
    cut=.640;paths=[]
    for inner in [True,False]:
        subset=[]
        for row in rows:
            keep=[p for p in row if (abs(p[0])<cut if inner else abs(p[0])>cut)]
            a,c=next((a,c) for a,c in zip(row,row[1:]) if abs(a[0])<=cut<=abs(c[0]))
            xx=cut+(-1 if inner else 1)*S.PANEL_GAP/2;t=(xx-abs(a[0]))/(abs(c[0])-abs(a[0]));p=tuple(a[k]+(c[k]-a[k])*t for k in range(3))
            subset.append(keep+[p] if inner else [p]+keep)
        ob=form_blank('Taillamp opening'+str(sign)+(' gate' if inner else ' quarter'),subset,material,master_tree,False)
        ob['lamp_piece']='gate' if inner else 'quarter';paths.append(ob)
    return paths


def fascia(b,front,master_tree,surface_map):
    openings=([('Low wide grille',(0,.585),(1.25,.225),.012,.070),
               ('Lower intake',(0,.300),(1.23,.120),.012,.055),
               ('Corner pocket L',(-.756,.438),(.185,.220),.018,.050),
               ('Corner pocket R',(.756,.438),(.185,.220),.018,.050)] if front else
              [('Diffuser',(0,.275),(1.43,.130),.015,.014),
               ('Plate pocket',(0,.465),(.330,.180),.004,.025)])
    from hatch_character import well,bars
    for name,(cx,cz),(ww,hh),radius,depth in openings:
        rows=[];nu=16 if ww>1 else 8;r=radius
        for j in range(5):
            v=j/4;zz=(v-.5)*(hh-.010);dz=max(0,abs(zz)-((hh-.010)/2-r))
            cut=r-math.sqrt(max(0,r*r-dz*dz));half=(ww-.010)/2-cut;z=cz+zz
            if name=='Low wide grille':half-=.035*v
            if name.startswith('Corner pocket'):
                half*=.45+.55*(1-v);xcenter=cx+math.copysign(.030*v,cx)
            else:xcenter=cx
            rows.append([(xcenter+(2*i/nu-1)*half,locator_y_guess(xcenter+(2*i/nu-1)*half,z,front),z) for i in range(nu+1)])
        backing=form_blank(name+' opening',rows,b.m['body'] if name=='Liftgate garnish' else b.m['rubber'],master_tree,front)
        b.add(backing,bpy.data.objects['Liftgate'] if name=='Liftgate garnish' else None,category='openings');ps=well(b,backing,surface_map,depth,front)
        if name in ['Low wide grille','Lower intake']:bars(b,backing,ps,front)
        if name=='Low wide grille':
            from hatch_character import surround
            surround(b,backing,surface_map)
        # Broad visible beds must retain their crown. Collapsing their grids
        # into long diagonal fans made false dents under studio reflections.
        if not b.high and name not in ['Diffuser','Low wide grille','Lower intake','Plate pocket','Liftgate garnish']:
            dec=backing.modifiers.new('Hidden pocket bed allocation','DECIMATE');dec.ratio=.25;G.apply(backing)
    lamps=[]
    from hatch_apertures import regularize_blank,carve
    for side,sgn in [('L',-1),('R',1)]:
        for lamp in lamp_volume(b,front,sgn,b.m['glass'],master_tree):
            regularize_blank(lamp,surface_map,front)
            b.add(lamp,bpy.data.objects['Liftgate'] if lamp.get('lamp_piece')=='gate' else None,category='openings');lamps.append(lamp)
    carve(front,lamps,surface_map)
    if not front:
        # Plate lamp / lower reflector blanks and an inset exhaust cutout are
        # the requested rear form cues, with no optical internals or badges.
        p=master_tree.ray_cast(Vector((0,3,.560)),Vector((0,-1,0)),3)[0]
        b.add(G.box('Plate lamp envelope',(0,p.y-.014,.555),(.065,.018,.012),b.m['glass'],.002,1),category='openings')
        for sign in [-1,1]:
            rows=[]
            for j in range(9):
                z=.335+.200*j/8;xc=.790+.12*(.535-z)
                rows.append([(sign*x,locator_y_guess(sign*x,z,False),z) for x in [xc-.012,xc,xc+.012]])
            ob=form_blank('Rear reflector'+str(sign),rows,b.m['glass'],master_tree,False)
            b.add(ob,category='openings');well(b,ob,surface_map,.008,False)
        rows=[[(x,locator_y_guess(x,z,False),z) for x in [-.80,-.765,-.73]] for z in [.235,.260,.285]]
        ob=form_blank('Exhaust cutout',rows,b.m['rubber'],master_tree,False);b.add(ob,category='openings');well(b,ob,surface_map,.035,False)
