"""One continuous, supported Catmull-Clark body cage, split AFTER evaluation.

The same cage spans nose, hood, fenders, doors, greenhouse and liftgate. Transverse
sections sculpt the crown/tumblehome/tuck; longitudinal supports control roof
acceleration, shoulder, fascia and roof hinge. Material/part boundaries do not
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
import suv_spec as S
END_ALLOWANCE={True:.052,False:.022}


def face_depth(z,front):
    q=z-(.650 if front else .650)
    t=max(0,min(1,((.45-z)/.25) if front else ((.65-z)/.35)))
    ease=t*t*(3-2*t)
    # The upper gate is upright; the lower bumper turns under. Giving both
    # the same draw made a long black tail and understated its departure.
    coefficient=(1.20-.10*ease) if front else (.30+.50*ease)
    return coefficient*q*q/max(.35,1+(0.4 if front else .25)*q)





# y, shoulder half-width, belt height, roof/hood center height.
# Original longitudinal package stations; the end rows carry their shoulder
# section around the corners without raising it to the backlight header.
STATIONS=[
 (-1.18,.91,1.13,1.087),(-1.10,.91,1.13,1.096),(-1.075,.91,1.13,1.100),
 (-1.00,.91,1.13,1.145),(-.82,.91,1.14,1.251),(-.60,.91,1.14,1.380),
 (-.36,.91,1.15,1.532),(-.25,.91,1.15,1.600),(-.16,.91,1.15,1.645),
 (.05,.91,1.16,1.676),(.12,.91,1.16,1.678),(.19,.91,1.16,1.679),
 (.44,.91,1.17,1.681),(.72,.91,1.17,1.679),(1.02,.91,1.18,1.674),
 (1.09,.91,1.18,1.672),(1.30,.91,1.19,1.666),(1.64,.91,1.20,1.653),
 (1.74,.91,1.20,1.644),(1.84,.91,1.21,1.627),(1.92,.91,1.21,1.607)]





def region(y,c):
    if 4<=c<=5 and -1.00<y<1.62:
        if .12<y<.19:return 'B applique'
        if 1.02<y<1.09:return 'C divider'
        if y<.12:return 'Window surround'
        if y<1.02:return 'Window surround'
        return 'Window surround'
    if c<=2 and -1.075<y<-.25:return 'Windshield'
    if c<=2:
        if y< -1.075:return 'Hood'
        return 'Roof'
    if c>=6:
        if S.DOOR_FRONT<y<S.DOOR_SPLIT:return 'Door F'
        if S.DOOR_SPLIT<y<S.DOOR_REAR:return 'Door R'
        return 'Front fender' if y<0 else 'Rear quarter'
    return 'Greenhouse'


def hood_draw_x(y):return .52+.18*max(0,min(1,(y+2.2)/1.15))


def side_width(y):
    return .889+.027*sum(math.exp(-((y-a)/.46)**2) for a in [S.FRONT_AXLE,S.REAR_AXLE])


def shoulder_height(y):return 1.047+.022*y


def character_height(y):return .505+.058*(y-S.DOOR_FRONT)/(S.DOOR_REAR-S.DOOR_FRONT)


def side_draw(y,z):
    def pos(q,r=.006):return .5*(q+math.sqrt(q*q+r*r))
    h=shoulder_height(y);line=character_height(y)
    d=pos(h-z);tail=pos(d-(h-line),.010);c=d-tail
    flare=.0235*math.exp(-((z-.780)/.090)**2)*sum(math.exp(-((y-a)/.40)**2) for a in [S.FRONT_AXLE,S.REAR_AXLE])
    return flare-.066*c-.215*c*c-.15*tail-.0048*math.exp(-((z-line-.040)/.028)**2)-.45*pos(.315-z,.008)-.285*pos(z-h)-.10*pos(z-h)**2


def body_section(y,w,belt,top):
    w=side_width(y);h=shoulder_height(y);line=character_height(y)
    belt=min(top-.085,1.153+.025*y+.025*max(0,(y-.9)/.9)**2)
    h=min(h,belt-.050)  # the shoulder rows must remain below the belt as the canopy folds down
    edge=w-.285*(belt-h)-math.tan(math.radians(18.5))*max(0,top-.050-belt)
    result=[(0,y,top),(.35*w,y,top-.004),(.66*w,y,top-.016),
       (edge-.027,y,top-.029),(edge,y,top-.050),
       ((edge+w+side_draw(y,belt))/2,y,(top-.050+belt)/2),
       (w+side_draw(y,belt+.016),y,belt+.016)]
    for z in [belt,h+.017,h,h-.023,h-.085,.790,line+.050,line+.012,line-.020,.270]:
        result.append((w+side_draw(y,z),y*(1-.12*max(0,(len(result)-8)/8)),z))
    result.insert(-1,(w+side_draw(y,line-.055),y*.90,line-.055))
    return result


# End rows fold the same rectangular quad sheet down from the hood/roof to the
# chin. Its entire boundary is underneath. There are NO cap patches, corner
# poles, booleans/unions, shrinkwraps, end fields or post-subdivision projection.
# y/z are the centerline CONTROL polygon; the corner's longitudinal spacing is
# separately monotone so no end row collapses onto its neighbor at the side.
FRONT_ROWS=[
 (-2.17,.175,-1.99),(-2.20,.285,-1.98),(-2.26,.425,-1.96),
 (-2.30,.580,-1.93),(-2.305,.665,-1.90),(-2.29,.760,-1.87),
 (-2.25,.855,-1.84),(-2.215,.940,-1.81),(-2.20,.978,-1.79),
 (-2.18,.981,-1.77),(-2.04,.999,-1.69),(-1.83,1.025,-1.58),
 (-1.60,1.054,-1.43),(-1.38,1.082,-1.27),(-1.19,1.106,-1.22)]
REAR_ROWS=[
 (1.98,1.590,1.94),(2.03,1.525,1.95),(2.11,1.385,1.99),
 (2.185,1.245,2.03),(2.215,1.185,2.045),(2.24,1.157,2.055),
 (2.26,1.125,2.065),(2.28,1.050,2.075),(2.29,.940,2.085),
 (2.292,.800,2.095),(2.305,.665,2.105),(2.292,.570,2.11),
 (2.26,.475,2.125),(2.21,.380,2.14),(2.16,.310,2.15)]



def end_section(row,front):
    yc,zc,tangent=row;w=side_width(tangent)+side_draw(tangent,zc)
    if not front and zc>1.15:
        half=body_section(tangent,w,1.2,zc)
        result=[]
        for i,(x,y,z) in enumerate(half):
            if i<=6:
                turn=min(1,(abs(x)/max(.001,half[6][0]))**2)
                y=yc+(tangent-yc)*turn
            result.append((x,y,z))
        return result
    xs=[0,.28,.53,.69,.76,.82,.865,.895,.910]
    result=[]
    for i,x in enumerate(xs):
        x*=w/.910
        turn=1-math.sqrt(max(0,1-(x/w)**2));y=yc+(tangent-yc)*turn
        if front:
            topness=max(0,min(1,(zc-.91)/.065))
            z=(zc-.006*(x/w)**2)*(1-topness)+hood_height(x,y)*topness
        else:
            # Rear glazing follows the same folded sheet. Broad pillar sail
            # panels occupy the outer chart, leaving a 1.3 m backlight.
            z=zc-.022*(x/w)**2
            if zc>1.15:
                y=yc+(tangent-yc)*turn*.45
        result.append((x,y,z))
    outer=result[-1][2]
    for j,t in enumerate([.030,.080,.420,.640,.815,.845,.952,1]):
        yy=tangent*(1-.12*t);z=outer*(1-t)+.270*t
        result.append((side_width(yy)+side_draw(yy,z),yy,z))
    a,c=Vector(result[-2]),Vector(result[-1]);result.insert(-1,tuple(a.lerp(c,.15)))
    return result


def hood_height(x,y):
    crown=.032*math.exp(-((abs(x)-.837)/.050)**2)*math.exp(-((y+1.55)/.72)**4)
    return .978+.108*(y+2.19)-.027*(x/.80)**2-.035*max(0,abs(x)-hood_draw_x(y))+crown




def crease_rows(half,hood,backlight=False):
    a,p,c=[Vector(q) for q in half[1:4]]
    if hood:
        x=hood_draw_x(p.y);result=[]
        for xx in [x-.016,x,x+.016]:
            t=(xx-a.x)/(c.x-a.x);yy=a.y+(c.y-a.y)*t
            result.append((xx,yy,hood_height(xx,yy)))
        half=[(x,y,hood_height(x,y)) if i<=3 else (x,y,z) for i,(x,y,z) in enumerate(half)]
    else:result=[tuple(a.lerp(p,.60)),tuple(p),tuple(p.lerp(c,.45))]
    return half[:2]+result+half[3:]


def section_field(p):
    """Single continuous implicit draw used only to fit the quad control net."""
    from forms import hermite
    x,y,z=p;w=side_width(y)+side_draw(y,z)
    ft,rt=-1.68,1.72
    fd=max(.25,2.3005+ft-face_depth(z,True));rd=max(.25,2.3005-rt-face_depth(z,False))
    a=max(0,ft-y)/fd;c=max(0,y-rt)/rd
    q=(x/w)**2+a**3+c**3-1
    g=math.sqrt((2*x/w**2)**2+(3*a*a/fd if y<ft else 3*c*c/rd)**2)
    wall=q/max(1,g)
    if y< -1.075:height=hood_height(x,y)
    else:
        height=hermite(y,[(-1.075,1.0984,.108),(-1.00,1.145,.61),(-.30,1.57,.61),(-.16,1.645,.25),
         (.30,1.679,0),(1.30,1.665,-.035),(1.80,1.63,-.18),(1.90,1.595,-1.2),
         (2.16,1.165,-1.7),(2.32,.96,-1.8),(2.47,.65,-2.2)])
        height-=.023*(x/.70)**2
    top=z-height;m=max(wall,top);r=.011
    return m+r*math.log(math.exp((wall-m)/r)+math.exp((top-m)/r))


def fit_control_net(ob):
    sub=ob.modifiers.new('Refine section-fit controls','SUBSURF');sub.levels=2;G.apply(ob)
    for v in ob.data.vertices:
        p=v.co;center=Vector((0,max(-1.45,min(1.45,p.y)),.650))
        if -1.10<p.y<1.70 and abs(p.x)>.82:center=Vector((0,p.y,p.z))
        direction=p-center;lo,hi=0.,2.
        for _ in range(32):
            t=(lo+hi)/2
            if section_field(center+direction*t)>0:hi=t
            else:lo=t
        v.co=center+direction*((lo+hi)/2)
    ob.data.update()


def master(level):
    n=20;verts=[];faces=[];labels=[]
    rows=[];kinds=[]
    for row in FRONT_ROWS:
        rows.append(crease_rows(end_section(row,True),row[1]>.95));kinds.append(('front',row[0]))
    for row in STATIONS:
        if -1.18<=row[0]<=1.94:
            rows.append(crease_rows(body_section(*row),row[0]<-1.075));kinds.append(('body',row[0]))
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
                label='Liftgate' if c<=2 else 'Rear molded fascia'
            else:label='Roof' if c<=2 else 'Rear quarter'
            if label in ['Front fender','Rear quarter'] or (kind=='body' and label not in ['Hood','Roof','Liftgate','Windshield','Backlight']):label+='_'+side
            labels.append(label)
            faces.append((j*width+i,j*width+i+1,(j+1)*width+i+1,(j+1)*width+i))
    ob=G.mesh('SUV unified subdivision cage',verts,faces)
    names=sorted(set(labels))
    for name in names:ob.data.materials.append(bpy.data.materials.new('Cage region '+name))
    for face,label in zip(ob.data.polygons,labels):face.material_index=names.index(label);face.use_smooth=True
    uv=ob.data.uv_layers.new(name='Surface parameters')
    for f in ob.data.polygons:
        for li in f.loop_indices:
            vi=ob.data.loops[li].vertex_index;uv.data[li].uv=(vi%width,vi//width)
    ob['grid_width']=width;ob['grid_rows']=len(rows)
    fit_control_net(ob)
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
    step=.25 if high else 1.0
    us=sorted(set([float(width-1)]+[i*step for i in range(math.floor((width-1)/step)+1)]+[u+d for u in [(width-1)/2-10,(width-1)/2+10] for d in [-.75,-.25,.25,.75]]))
    vs=sorted(set(list(range(rows))+[j+.5 for j in range(rows-1) if high or j in [2,3,4,5,6,15,16,17,18,19,20] or j>=rows-15]))
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
    if not high:
        # A regular tensor grid around the compound A-foot. Coarse chords
        # through this narrow roof/hood transition can cross the parent.
        supports=[center+sgn*(3.5+i*.25) for sgn in [-1,1] for i in range(13)]
        grids=[sorted(set(columns+supports)) if 15<=v<=20 else columns for v,columns in zip(vs,grids)]
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
        for refinement in range(1):
            # Refine the actual lower rear plan turn in BOTH chart directions.
            # Adjacent polygons share inserted midpoints, so there are no T cracks.
            selected=set();edges={}
            for fi,face in enumerate(faces):
                p=sum((vertices[i] for i in face),Vector())/len(face)
                if len(face)==4 and 1.76<p.y<1.99 and .35<p.z<.55 and abs(p.x)>.80:
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


def arch_point(a,axle,offset=0):
    power=2/S.ARCH_POWER;c=math.cos(a);t=math.sin(a)
    return (axle+(S.ARCH_HALF+offset)*math.copysign(abs(c)**power,c),
        S.HUB_HEIGHT+(S.ARCH_RADIUS+offset)*math.copysign(abs(t)**power,t))


def trim_arch(ob,axle,segments):
    """Clip the fair outer sheet, then close its gauge; no thin-solid boolean.

    Convex polygon difference in YZ, retaining the original face planes. The
    cutter is the same inscribed polygon as the arch's circular cylinder.
    """
    radius=S.ARCH_RADIUS;inner=radius*math.cos(math.pi/segments)
    poly=[arch_point(math.tau*j/segments,axle) for j in range(segments)]
    planes=[]
    for a,c in zip(poly,poly[1:]+poly[:1]):
        ny,nz=c[1]-a[1],a[0]-c[0];length=math.hypot(ny,nz);ny/=length;nz/=length
        planes.append((ny,nz,ny*(a[0]-axle)+nz*(a[1]-S.HUB_HEIGHT)))
    vertices=[];faces=[]
    for f in ob.data.polygons:
        polygon=[ob.data.vertices[i].co.copy() for i in f.vertices]
        ys=[p.y-axle for p in polygon];zs=[p.z-S.HUB_HEIGHT for p in polygon]
        if min(ys)>S.ARCH_HALF or max(ys)<-S.ARCH_HALF or min(zs)>radius or max(zs)<-radius:
            pieces=[polygon]
        elif max((abs(y/S.ARCH_HALF)**S.ARCH_POWER+abs(z/radius)**S.ARCH_POWER) for y,z in zip(ys,zs))<.99:continue
        else:
            pieces=[]
            for ny,nz,edge in planes:
                inside=[];outside=[]
                for a,b in zip(polygon,polygon[1:]+polygon[:1]):
                    da=ny*(a.y-axle)+nz*(a.z-S.HUB_HEIGHT)-edge
                    db=ny*(b.y-axle)+nz*(b.z-S.HUB_HEIGHT)-edge
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
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-6)
    bm.to_mesh(ob.data);bm.free()


def closeable_sheet(ob):
    """Remove clipping crumbs and split point-touching surface fans.

    Two sheet regions touching at a single vertex need independent gauge rims;
    otherwise Solidify joins both rims onto one four-face non-manifold edge.
    No surface point is moved by the fan split.
    """
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-6)
    bmesh.ops.triangulate(bm,faces=list(bm.faces))
    bad=[f for f in bm.faces if f.calc_area()<1e-11]
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
    ob['inner_gauge_reduced']=maximum<=-.0004 and all(e.is_manifold for e in bm.edges)
    if ob['inner_gauge_reduced']:bm.to_mesh(ob.data)
    bm.free();ob.data.update()


def skin_gauge(ob,thickness):
    """Mark outside/back/rim explicitly through repeated projected cuts.

    A normal-angle test cannot identify sheet fronts at a compound corner:
    a legitimate coarse chord may be over 25 degrees from the limit normal.
    Solidify's material indices carry provenance without that geometric guess.
    Slots are collapsed after every aperture has been cut.
    """
    material=ob.data.materials[0]
    ob.data.materials.clear()
    for _ in range(3):ob.data.materials.append(material)
    for face in ob.data.polygons:face.material_index=0
    gauge=ob.modifiers.new('Sheet gauge','SOLIDIFY');gauge.thickness=thickness;gauge.offset=-1;gauge.use_even_offset=False
    gauge.material_offset=1;gauge.material_offset_rim=2
    G.apply(ob);ob['skin_face_provenance']=True


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
    for name in ['Front lower bumper cladding','Rear lower bumper cladding']:
        names.append(name);source.data.materials.append(bpy.data.materials.new('Cage region '+name))
    bm=bmesh.new();bm.from_mesh(source.data)
    for z in [.535,.640]:
        bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-8,
            plane_co=(0,0,z),plane_no=(0,0,1),clear_inner=False,clear_outer=False)
    cuts=[S.DOOR_FRONT,S.DOOR_SPLIT,S.DOOR_REAR]
    for line in cuts:
        for y in [line-S.PANEL_GAP/2,line+S.PANEL_GAP/2]:
            bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),
                dist=1e-8,plane_co=(0,y,0),plane_no=(0,1,0),clear_inner=False,clear_outer=False)
    for axis,line in [(0,-.745),(0,.745),(2,.700)]:
        for offset in [-S.PANEL_GAP/2,S.PANEL_GAP/2]:
            co=[0.,0.,0.];no=[0.,0.,0.];co[axis]=line+offset;no[axis]=1.
            bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-8,plane_co=co,plane_no=no,clear_inner=False,clear_outer=False)
    discard=[]
    for f in bm.faces:
        label=names[f.material_index]
        if label in ['Liftgate','Rear molded fascia']:
            p=f.calc_center_median();suffix='R' if p.x>0 else 'L'
            if abs(p.z-.700)<S.PANEL_GAP/2-1e-7 or (p.z>.700 and abs(abs(p.x)-.745)<S.PANEL_GAP/2-1e-7):discard.append(f);continue
            label=('Liftgate' if abs(p.x)<.745 else 'Rear quarter_'+suffix) if p.z>.700 else 'Rear molded fascia'
            f.material_index=names.index(label)
        elif label.startswith(('Door F','Door R','Front fender','Rear quarter')):
            p=f.calc_center_median();suffix='R' if p.x>0 else 'L'
            if any(abs(p.y-line)<S.PANEL_GAP/2-1e-7 for line in cuts):discard.append(f);continue
            label=('Front fender' if p.y<S.DOOR_FRONT else 'Door F' if p.y<S.DOOR_SPLIT else 'Door R' if p.y<S.DOOR_REAR else 'Rear quarter')+'_'+suffix
            f.material_index=names.index(label)
    for face in bm.faces:
        label=names[face.material_index];z=face.calc_center_median().z
        if label=='Front molded fascia' and z<.535:face.material_index=names.index('Front lower bumper cladding')
        if label=='Rear molded fascia' and z<.640:face.material_index=names.index('Rear lower bumper cladding')
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
    for name,y,z in [('Hood',-1.075,1.103),('Liftgate',1.90,1.61)]:
        piv=G.pivot(name,(0,y,z),'X',(-65,0) if name=='Hood' else (0,75));piv.parent=b.root;pivots[name]=piv
    for index,name in enumerate(names):
        selected=[f for f in source.data.polygons if f.material_index==index]
        if not selected:continue
        used=sorted({i for f in selected for i in f.vertices});lookup={old:i for i,old in enumerate(used)}
        verts=[points[i].copy() for i in used];faces=[tuple(lookup[i] for i in f.vertices) for f in selected]
        glass=any(k in name for k in ['glass','Windshield','Backlight'])
        dark=any(k in name for k in ['applique','divider'])
        lower='lower bumper cladding' in name
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
            if name.startswith(('Greenhouse','Window surround','Roof')):continue  # continuous welded fixed steel
            p=verts[i];inside=centroids[i]
            if any(abs(abs(p.y-line)-S.PANEL_GAP/2)<2e-6 for line in cuts):continue
            if p.y>1.80 and (abs(abs(abs(p.x)-.745)-S.PANEL_GAP/2)<2e-6 or abs(abs(p.z-.700)-S.PANEL_GAP/2)<2e-6):continue
            if inside:
                tangent=(sum(inside,Vector())/len(inside)-p)
                n=normals[used[i]];tangent-=n*tangent.dot(n)
                if tangent.length>1e-8:
                    q=p+tangent.normalized()*min(S.PANEL_GAP/2,tangent.length*.40)
                    verts[i]=tree.find_nearest(q)[0]
        if glass:verts=[p-normals[old]*.002 for p,old in zip(verts,used)]
        mat=b.m['glass'] if glass else b.m['rubber'] if dark or lower else b.m['body']
        ob=G.mesh(name+' outer' if name in ['Hood','Liftgate'] else name,verts,faces,mat)
        for face in ob.data.polygons:face.use_smooth=True
        if not glass:
            for axle in [S.FRONT_AXLE,S.REAR_AXLE]:
                if min(v.co.y for v in ob.data.vertices)<axle+S.ARCH_HALF and max(v.co.y for v in ob.data.vertices)>axle-S.ARCH_HALF:
                    trim_arch(ob,axle,128 if b.high else 64)
            if not ob.data.polygons:raise ValueError(('Arch trim discarded panel',name))
        closeable_sheet(ob)
        skin_gauge(ob,.0048 if glass else .003 if 'fascia' in name or lower else .0009)
        category='cladding' if lower else 'glass' if glass else 'pillars' if dark or name.startswith('Greenhouse') else 'doors' if name.startswith('Door') else 'fascia' if 'fascia' in name else 'body'
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
            angles=[-.10+(math.pi+.20)*i/segments for i in range(segments+1)]
            count=len(angles)
            for depth in [0,.018]:
                ring=[]
                for a in angles:
                    y,z=arch_point(a,axle)
                    hit=tree.ray_cast(Vector((sign*2,y,z)),Vector((-sign,0,0)),3)[0]
                    x=abs(hit.x) if hit else .89
                    ring.append((sign*(x-depth),y,z))
                loops.append(ring)
            ob=G.mesh('Arch hem_'+end+side,loops[0]+loops[1],[(i,i+1,count+i+1,count+i) for i in range(count-1)],b.m['body'])
            sol=ob.modifiers.new('Arch hem gauge','SOLIDIFY');sol.thickness=.001;sol.offset=-1;G.apply(ob)
            if b.high:b.add(ob,category='arches')
            else:bpy.data.objects.remove(ob,do_unlink=True)  # concealed steel hem; molded inner flange remains
            # Dark well, following the same real opening; interior detail deferred.
            inner_angles=angles[::2] if b.high else angles;count=len(inner_angles)
            verts=[(sign*x,*arch_point(a,axle,.018)) for x in [.56,.88] for a in inner_angles]
            fs=[(i,i+1,count+i+1,count+i) for i in range(count-1)]
            ob=G.mesh('Wheelwell_'+end+side,verts,fs,b.m['rubber']);sol=ob.modifiers.new('Liner thickness','SOLIDIFY');sol.thickness=.002;G.apply(ob);b.add(ob,category='liners')
            outline=[arch_point(a,axle,.018) for a in inner_angles]
            b.add(G.profile('Wheelwell inboard_'+end+side,outline,sign*.559,sign*.561,b.m['rubber'],axis='X'),category='liners')
    fascia(b,front=True,master_tree=parent_tree,surface_map=surface_map);fascia(b,front=False,master_tree=parent_tree,surface_map=surface_map)
    from suv_greenhouse import build as greenhouse
    greenhouse(b,parent_tree,surface_map)
    # Only a cavity closure is supplied at this gate, not an interior or drivetrain.
    # This temporary blackout is inside the wheel wells and tucked end skins.
    # A full-width, long rectangle projected behind the curved lower tail and
    # looked like a diffuser plate. It is not the later underbody assembly.
    floor=G.box('Form cavity closure',(0,-.05,.260),(1.10,3.55,.018),b.m['rubber'],0);b.add(floor,category='closure')
    from suv_character import mirrors
    mirrors(b)
    from suv_cladding import build as cladding
    cladding(b,tree)
    # The closed-gauge triangulator can leave a collinear triangle at a cut.
    # Dissolve only degenerate geometry (0.1 micrometre); do not weld closed
    # shells or join independent rim fans. The independent audit still gates it.
    for item in list(bpy.context.scene.objects):
        if item.type!='MESH':continue
        bm=bmesh.new();bm.from_mesh(item.data)
        bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
        bmesh.ops.triangulate(bm,faces=list(bm.faces))
        bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
        bm.to_mesh(item.data);bm.free()
    # Boolean aperture cuts can change the rim smoothing fans again. Reapply the
    # pre-cut master field to every exposed outer corner, with flat gauge edges.
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('part_category') not in ['body','doors','glass','pillars','fascia','cladding']:continue
        if ob.get('part_category')=='cladding' and 'lower bumper cladding' not in ob.name:continue
        material=next((m for m in ob.data.materials if m),None)
        if material is None:raise ValueError(('Missing form material',ob.name,len(ob.data.vertices),len(ob.data.polygons)))
        ob.data.materials.clear();ob.data.materials.append(material)
        for face in ob.data.polygons:face.material_index=0
        if not b.high and ob.get('part_category') in ['fascia','cladding']:simplify_inner_gauge(ob,tree)
        G.smooth(ob,35);custom=[];inverse=ob.matrix_world.to_3x3().transposed()
        for face in ob.data.polygons:
            center=ob.matrix_world@face.center;_,n,_,_=tree.find_nearest(center)
            face.use_smooth=abs(face.normal.dot(inverse@n))>.5
            for li in face.loop_indices:
                p=ob.matrix_world@ob.data.vertices[ob.data.loops[li].vertex_index].co
                hit,n,fi,distance=tree.find_nearest(p);ia,ib,ic=triangles[fi]
                n=barycentric_transform(hit,points[ia],points[ib],points[ic],normals[ia],normals[ib],normals[ic]).normalized()
                dot=face.normal.dot(inverse@n)
                custom.append(inverse@(n if dot>0 else -n) if distance<.010 and abs(dot)>.5 else (0,0,0))
        ob.data.normals_split_custom_set(custom)


def locator_y_guess(x,z,front):
    sign=-1 if front else 1
    return sign*(S.LENGTH/2+.008-(.27 if front else .21)*(x/.925)**2-face_depth(z,front))


def form_blank(name,rows,material,master_tree,front):
    """A sampled, conforming blank; a single n-gon chords through the crown."""
    def project(guess):
        if name.startswith('Taillamp'):
            # A lamp's horizontal guide is a height section around the corner.
            # A nearest-point query can climb the sloping backlight instead.
            direction=Vector((guess[0],max(0,guess[1]-1.45),0)).normalized()
            hit,n,_,_=master_tree.ray_cast(Vector(guess)+direction*.45,-direction,1.)
            if hit is not None:return hit,n
        hit,n,_,_=master_tree.find_nearest(Vector(guess));return hit,n
    vertices=[];nu=len(rows[0])
    for row in rows:
        for guess in row:
            hit,n=project(guess)
            if n.dot(Vector((hit.x,-.8 if front else .8,0)))<0:n.negate()
            offset=.0025 if front and abs(hit.x)<.25 else .004
            vertices.append(hit+n*offset)
    faces=[(j*nu+i,j*nu+i+1,(j+1)*nu+i+1,(j+1)*nu+i) for j in range(len(rows)-1) for i in range(nu-1)]
    ob=G.mesh(name,vertices,faces,material)
    hint=Vector((0,-1 if front else 1,0))
    if ob.data.polygons[0].normal.dot(hint)<0:
        for face in ob.data.polygons:face.flip()
    if name.startswith(('Headlamp','Taillamp')):
        # These optical guides go directly to the chart triangulator. Closing
        # and refining a Cartesian temporary blank first can collapse its tip;
        # that discarded temporary mesh must not perturb the measured border.
        ob['form_rows']=len(rows);ob['form_columns']=nu
        ob['aperture_samples']=[q for p in vertices for q in p]
        return ob
    # Refine only cells whose chords enter the painted surface. A corner's
    # 20 mm roll can cross a dark locator even when all its vertices clear.
    # BMesh splits shared edges conformingly, retaining a closed gauge later.
    bm=bmesh.new();bm.from_mesh(ob.data);original_samples=[v.co.copy() for v in bm.verts]
    for _ in range(2):
        edges=set()
        for face in bm.faces:
            center=face.calc_center_median();hit,n=project(center)
            if n.dot(Vector((hit.x,-.8 if front else .8,0)))<0:n.negate()
            if (center-hit).dot(n)<.0006:edges.update(face.edges)
        if not edges:break
        bm.edges.index_update()
        bmesh.ops.subdivide_edges(bm,edges=sorted(edges,key=lambda edge:edge.index),cuts=1,use_grid_fill=True)
        for v in bm.verts:
            hit,n=project(v.co)
            if n.dot(Vector((hit.x,-.8 if front else .8,0)))<0:n.negate()
            offset=.0025 if front and abs(hit.x)<.25 else .004
            v.co=hit+n*offset
    # Projection at a tapered optical tip can collapse neighboring sample
    # rows onto a 30-micron edge. Weld below optical manufacturing tolerance
    # before closing the gauge; a six-face edge is not a valid lens blank.
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00010)
    bmesh.ops.triangulate(bm,faces=list(bm.faces))
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-6)
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
    if ob['guide_snap_max_m']>.002:raise ValueError(('Aperture projection lost its boundary',name,ob['guide_snap_max_m']))
    vertices=snapped
    ob['form_rows']=len(rows);ob['form_columns']=nu
    ob['aperture_samples']=[q for p in vertices for q in p]
    return ob


def lamp_volume(b,front,sign,material,master_tree):
    if front:
        path=[(.52,0,.932,.125),(.60,0,.947,.120),(.71,0,.968,.105),
         (.80,0,.989,.095),(.858,-1.91,1.008,.080),(.889,-1.79,1.026,.060),(.902,-1.73,1.039,.025)]
    else:
        path=[(.32,0,1.111,.075),(.49,0,1.120,.115),(.64,0,1.105,.165),
         (.76,0,1.105,.170),(.845,0,1.105,.150),(.886,2.11,1.103,.105),(.909,1.92,1.110,.025)]
    path=[(x,locator_y_guess(x,z,front) if y==0 else y,z,h) for x,y,z,h in path]
    dense=[]
    for a,c in zip(path,path[1:]):
        dense.extend([tuple(a[k]+(c[k]-a[k])*t for k in range(4)) for t in [i/8 for i in range(8)]])
    dense.append(path[-1]);rows=[[(sign*x,y,z+h*(v-.5)) for x,y,z,h in dense] for v in [i/4 for i in range(5)]]
    if front:return [form_blank('Headlamp opening'+str(sign),rows,material,master_tree,front)]
    paths=[];cut=.745
    for inner in [True,False]:
        subset=[]
        for row in rows:
            keep=[p for p in row if (abs(p[0])<cut if inner else abs(p[0])>cut)]
            a,c=next((a,c) for a,c in zip(row,row[1:]) if abs(a[0])<=cut<=abs(c[0]))
            xx=cut+(-1 if inner else 1)*S.PANEL_GAP/2;t=(xx-abs(a[0]))/(abs(c[0])-abs(a[0]));q=tuple(a[k]+(c[k]-a[k])*t for k in range(3))
            subset.append(keep+[q] if inner else [q]+keep)
        ob=form_blank('Taillamp opening'+str(sign)+(' gate' if inner else ' quarter'),subset,material,master_tree,False)
        ob['lamp_piece']='gate' if inner else 'quarter';paths.append(ob)
    return paths


def fascia(b,front,master_tree,surface_map):
    openings=([('Upper grille',0,.780,1.19,.225,.062),('Lower intake',0,.454,1.32,.140,.055),
       ('Corner pocket L',-.767,.576,.175,.205,.048),('Corner pocket R',.767,.576,.175,.205,.048)] if front else
       [('Plate pocket',0,.931,.320,.171,.025),('Reflector L',-.69,.565,.16,.038,.015),('Reflector R',.69,.565,.16,.038,.015),('Exhaust cutout',.63,.375,.17,.075,.045)])
    from suv_character import well,bars
    for name,cx,cz,width,height,depth in openings:
        rows=[];nu=16 if width>1 else 8
        for j in range(5):
            v=j/4;z=cz+(v-.5)*height
            half=width/2
            if name=='Upper grille':half-=.115*v
            if name.startswith('Corner pocket'):half*=.70+.30*v
            r=.005;dz=max(0,abs(z-cz)-(height/2-r));half-=r-math.sqrt(max(0,r*r-dz*dz))
            rows.append([(cx+(2*i/nu-1)*half,locator_y_guess(cx+(2*i/nu-1)*half,z,front),z) for i in range(nu+1)])
        blank=form_blank(name+' opening',rows,b.m['rubber'],master_tree,front);b.add(blank,category='openings')
        ps=well(b,blank,surface_map,depth,front)
        if name in ['Upper grille','Lower intake']:bars(b,blank,ps,front)
        if name=='Plate pocket':
            # A small supported overhead plate-light housing; no markings yet.
            top=ps[-(nu+1)+(nu//2)]
            b.add(G.box('Plate lamp',(top.x,top.y+.002,top.z-.004),(.11,.022,.014),b.m['bumper'],.003,2),bpy.data.objects['Liftgate'],category='openings')
        if not b.high:
            dec=blank.modifiers.new('Hidden bed allocation','DECIMATE');dec.ratio=.3;G.apply(blank)
    lamps=[]
    from suv_apertures import regularize_blank,carve
    for side,sgn in [('L',-1),('R',1)]:
        for lamp in lamp_volume(b,front,sgn,b.m['glass'],master_tree):
            regularize_blank(lamp,surface_map,front)
            b.add(lamp,bpy.data.objects['Liftgate'] if lamp.get('lamp_piece')=='gate' else None,category='openings');lamps.append(lamp)
    from suv_apertures import outline_loop
    from suv_character import optical_case
    loops=[outline_loop(lamp,surface_map) for lamp in lamps]
    carve(front,lamps,surface_map)
    for lamp,loop in zip(lamps,loops):optical_case(b,lamp,loop,surface_map,front)


