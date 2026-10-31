"""One continuous, supported Catmull-Clark body cage, split AFTER evaluation.

The same cage spans nose, hood, fenders, doors, greenhouse and deck. Transverse
sections sculpt the crown/tumblehome/tuck; longitudinal supports control roof
acceleration, shoulder, fascia and deck lip. Material/part boundaries do not
interrupt subdivision. Evaluated patches retain the master's corner normals.
References are never opened by the modeling process.
"""
import math
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
from kit import model as G
import sedan_spec as S
from forms import hermite
END_ALLOWANCE={True:.02232,False:.01652}  # compensate the evaluated cap's rounding


def face_depth(z,front):
    controls=([(.218,.095,0),(.29,.045,-.35),(.37,0,0),(.50,.020,.20),(.63,.043,.12),(.78,.048,0)] if front else
              [(.218,.100,0),(.32,.055,-.30),(.51,0,0),(.64,.015,.20),(.82,.080,0),(1.04,.012,-.40)])
    return hermite(z,controls)

# y, shoulder half-width, belt height, roof/hood center height.
# Paired physical rows support the cowl, header and crisp deck trailing lip.
STATIONS=[
 (-2.450,.900,.700,.758),(-2.430,.901,.710,.766),(-2.370,.902,.730,.775),
 (-2.200,.869,.765,.795),(-1.950,.902,.790,.820),(-1.680,.918,.815,.855),
 (-1.385,.925,.850,.885),(-1.180,.924,.880,.915),
 (-1.040,.920,.907,.940),(-.990,.918,.913,.953),
 (-.930,.918,.917,.990),(-.740,.918,.928,1.090),(-.460,.919,.942,1.250),
 (-.200,.920,.953,1.395),(-.130,.920,.956,1.425),(-.080,.920,.958,1.438),
 (.180,.921,.969,1.449),(.215,.921,.971,1.450),(.470,.923,.983,1.450),
 (.730,.925,.994,1.437),(.850,.925,1.000,1.414),(.910,.925,1.002,1.393),
 (1.105,.925,1.006,1.305),(1.125,.925,1.0065,1.295),
 (1.360,.922,1.010,1.165),(1.570,.914,1.012,1.050),
 (1.650,.908,1.011,1.027),(1.730,.899,1.010,1.024),
 (2.050,.867,1.004,1.029),(2.280,.827,.997,1.035),
 (2.365,.883,.990,1.046),(2.390,.880,.980,1.046),
 (2.425,.875,.945,1.018),(2.450,.870,.925,.990)]


def section(y,w,belt,top):
    """Half-section from roof center across shoulder to recessed rocker.

    Glass is a 22.5 degree tumblehome where the roof is fully developed.
    Narrowing the roof is a section control, rather than an extruded profile.
    """
    w-=.0036  # the broad axle draw, below, supplies the final 925 mm half-width
    top+=.0015*math.exp(-((y-.35)/.5)**2)
    cabin=max(0,min(1,(top-belt-.045)/.42))
    roof_edge=w-.028-math.tan(math.radians(22.5))*max(0,top-.055-belt)
    # Hood/deck breadth blends into roof breadth with the same surface rows.
    upper=top-.032-.016*cabin
    lower=min(belt+.018,upper-.012)
    lower_line=.345+.040*(y+.2)
    bulge=.006*sum(math.exp(-((y-a)/.40)**2) for a in [S.FRONT_AXLE,S.REAR_AXLE])
    return [
      (0,y,top),(.35*w,y,top-.004),(.66*w,y,top-.014),
      (roof_edge-.026,y,top-.026),(roof_edge,y,upper),
      ((roof_edge+w-.025)/2,y,(upper+lower)/2),
      (w-.025,y,lower),(w-.010,y,belt),
      (w+bulge,y,belt-.024),(w+bulge-.001,y,belt-.033),
      (w-.004+bulge*.6,y,belt-.048),(w-.012,y,min(.660,belt-.100)),
      (w-.008,y,.505),(w-.044,y,lower_line+.018),
      (w-.048,y,lower_line),(w-.076,y,.235),(w-.105,y,.218)]


def region(y,c):
    if 4<=c<=5 and -.930<y<1.570:
        if .180<y<.215:return 'B applique'
        if 1.105<y<1.125:return 'C divider'
        if y<.180:return 'Front side glass'
        if y<1.105:return 'Rear side glass'
        return 'Quarter glass'
    if c<=2 and -.990<y<-.130:return 'Windshield'
    if c<=2 and .910<y<1.650:return 'Backlight'
    if c<=2:
        if y<-.990:return 'Hood'
        if y>1.650:return 'Trunk'
        return 'Roof'
    if c>=15:return 'Rocker'
    if c>=6:
        if S.DOOR_FRONT<y<S.DOOR_SPLIT:return 'Door F'
        if S.DOOR_SPLIT<y<S.DOOR_REAR:return 'Door R'
        return 'Front fender' if y<0 else 'Rear quarter'
    return 'Greenhouse'


def master(level):
    n=17;verts=[]
    for row in STATIONS:
        half=section(*row)
        def swept(p):
            x,y,z=p
            forward=max(0,min(1,(-y-1.8)/.5))
            rear=max(0,min(1,(y-1.95)/.4))
            return x,y+(.270*(abs(x)/.925)**4+face_depth(z,True)-END_ALLOWANCE[True])*forward-(.185*(abs(x)/.925)**4+face_depth(z,False)-END_ALLOWANCE[False])*rear,z
        half=[swept(p) for p in half]
        # Full transverse strip, no centerline seam.
        verts.extend([(-x,y,z) for x,y,z in reversed(half[1:])]+half)
    width=2*n-1;faces=[];labels=[]
    for j in range(len(STATIONS)-1):
        y=(STATIONS[j][0]+STATIONS[j+1][0])/2
        for i in range(width-1):
            c=i-(n-1) if i>=n-1 else (n-2)-i
            side='R' if i>=n-1 else 'L'
            label=region(y,c)
            if label not in ['Hood','Roof','Trunk','Windshield','Backlight']:label+='_'+side
            labels.append(label)
            faces.append((j*width+i,j*width+i+1,(j+1)*width+i+1,(j+1)*width+i))
    # Nose and tail are cap grids sharing the shell's actual boundary vertices.
    # Subdivision rounds the entire corner before parts are split. An independent
    # face plate left an open, square corner in the rejected first clay pass.
    for front in [True,False]:
        offset=0 if front else (len(STATIONS)-1)*width
        # A rectangular Coons grid follows the roof/hood top and both actual
        # side sections. The rejected U-shaped strips converged toward the
        # rocker corners and produced reflection fans across the entire cap.
        top=[Vector(verts[offset+i]) for i in range(8,25)]
        left=[Vector(verts[offset+8-j]) for j in range(9)]
        right=[Vector(verts[offset+24+j]) for j in range(9)]
        a,c,lb,rb=top[0],top[-1],left[-1],right[-1]
        rows=[list(range(offset+8,offset+25))]
        for j in range(1,9):
            v=(a.z-left[j].z)/(a.z-lb.z);current=[offset+8-j]
            for i in range(1,16):
                u=(top[i].x-a.x)/(c.x-a.x);bottom=lb*(1-u)+rb*u
                bilinear=a*((1-u)*(1-v))+c*(u*(1-v))+lb*((1-u)*v)+rb*(u*v)
                p=top[i]*(1-v)+bottom*v+left[j]*(1-u)+right[j]*u-bilinear
                p.y=(-1 if front else 1)*(S.LENGTH/2+END_ALLOWANCE[front]-(.270 if front else .185)*(abs(p.x)/.925)**4-face_depth(p.z,front))
                current.append(len(verts));verts.append(tuple(p))
            current.append(offset+24+j);rows.append(current)
        for previous,current in zip(rows,rows[1:]):
            for i in range(16):
                faces.append((previous[i],previous[i+1],current[i+1],current[i]))
                middle=sum(verts[k][2] for k in faces[-1])/4
                labels.append('Front molded fascia' if front else 'Trunk' if middle>.680 else 'Rear molded fascia')
    ob=G.mesh('Sedan unified subdivision cage',verts,faces)
    names=sorted(set(labels));materials=[]
    for name in names:
        mat=bpy.data.materials.new('Cage region '+name);ob.data.materials.append(mat);materials.append(mat)
    for face,label in zip(ob.data.polygons,labels):face.material_index=names.index(label);face.use_smooth=True
    sub=ob.modifiers.new('Supported sculpted body','SUBSURF');sub.subdivision_type='CATMULL_CLARK';sub.levels=level;sub.render_levels=level
    G.apply(ob)
    # Whole body is one connected subdivision surface until this operation.
    ob['construction']='Continuous transverse sculpted cage; Catmull-Clark before panel separation'
    return ob,names


def build(b):
    source,names=master(3 if b.high else 2)
    source.data.calc_loop_triangles()
    # Preserve master vertex normals across face-group separation and shut lines.
    points=[v.co.copy() for v in source.data.vertices]
    normals=[v.normal.copy() for v in source.data.vertices]
    triangles=[tuple(t.vertices) for t in source.data.loop_triangles]
    tree=BVHTree.FromPolygons(points,triangles,all_triangles=True)
    pivots={}
    for side,sign in [('L',-1),('R',1)]:
        for end,y in [('F',S.DOOR_FRONT),('R',S.DOOR_SPLIT)]:
            piv=G.pivot('Door_'+end+side,(sign*.875,y,.74),'Z',(-72,0) if sign>0 else (0,72));piv.parent=b.root;pivots['Door '+end+'_'+side]=piv
    for name,y,z in [('Hood',-.990,.95),('Trunk',1.650,1.025)]:
        piv=G.pivot(name,(0,y,z),'X',(-65,0) if name=='Hood' else (0,75));piv.parent=b.root;pivots[name]=piv
    for index,name in enumerate(names):
        selected=[f for f in source.data.polygons if f.material_index==index]
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
        for i in boundary:
            p=verts[i];inside=[verts[j] for j in adj[i] if j not in boundary]
            if inside:
                tangent=(sum(inside,Vector())/len(inside)-p)
                n=normals[used[i]];tangent-=n*tangent.dot(n)
                if tangent.length>1e-8:verts[i]=p+tangent.normalized()*S.PANEL_GAP/2
        if glass:verts=[p-normals[old]*.002 for p,old in zip(verts,used)]
        mat=b.m['glass'] if glass else b.m['rubber'] if dark else b.m['body']
        ob=G.mesh(name+' outer' if name in ['Hood','Trunk'] else name,verts,faces,mat)
        if not b.high:
            # Keep the evaluated seam stations fixed. Interior reduction spends
            # density on silhouette/curvature rather than redundant sheet grids.
            group=ob.vertex_groups.new(name='Interior reduction')
            inside=[i for i in range(len(verts)) if i not in boundary]
            if inside:group.add(inside,1,'REPLACE')
            dec=ob.modifiers.new('Curvature budget','DECIMATE');dec.ratio=.27 if not glass else .20
            dec.vertex_group=group.name;dec.vertex_group_factor=1000;dec.use_collapse_triangulate=True
            G.apply(ob)
        for face in ob.data.polygons:face.use_smooth=True
        gauge=ob.modifiers.new('Sheet gauge','SOLIDIFY');gauge.thickness=.0048 if glass else .0009;gauge.offset=-1;gauge.use_even_offset=False
        G.apply(ob)
        if name.startswith(('Front fender','Rear quarter','Door R')):
            for end,axle in [('F',S.FRONT_AXLE),('R',S.REAR_AXLE)]:
                if (end=='F')!=name.startswith('Front fender'):continue
                bpy.ops.mesh.primitive_cylinder_add(vertices=64 if not b.high else 128,radius=S.ARCH_RADIUS,depth=3,location=(0,axle,S.HUB_HEIGHT),rotation=(0,math.pi/2,0))
                cut=bpy.context.object;mod=ob.modifiers.new('Trim true wheel opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;G.apply(ob);bpy.data.objects.remove(cut,do_unlink=True)
                if not ob.data.polygons:raise ValueError(('Arch trim discarded panel',name,end))
            # Exact circle/sheet intersections can leave sub-micron coincident
            # vertices at tangent stations. Weld them rather than waiving the
            # independent zero-area/sliver audit; the 0.9 mm gauge is untouched.
            bm=bmesh.new();bm.from_mesh(ob.data)
            bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
            bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
            bm.to_mesh(ob.data);bm.free()
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
            angles=[-.31+(math.pi+.62)*i/48 for i in range(49)]
            for depth in [0,.018]:
                ring=[]
                for a in angles:
                    y=axle+S.ARCH_RADIUS*math.cos(a);z=S.HUB_HEIGHT+S.ARCH_RADIUS*math.sin(a)
                    hit=tree.ray_cast(Vector((sign*2,y,z)),Vector((-sign,0,0)),3)[0]
                    x=abs(hit.x) if hit else .89
                    ring.append((sign*(x-depth),y,z))
                loops.append(ring)
            ob=G.mesh('Arch flange_'+end+side,loops[0]+loops[1],[(i,i+1,50+i,49+i) for i in range(48)],b.m['body'])
            sol=ob.modifiers.new('Arch hem gauge','SOLIDIFY');sol.thickness=.001;sol.offset=-1;G.apply(ob);b.add(ob,category='arches')
            # Dark well, following the same real opening; interior detail deferred.
            verts=[(sign*x,axle+(S.ARCH_RADIUS+.012)*math.cos(a),S.HUB_HEIGHT+(S.ARCH_RADIUS+.012)*math.sin(a)) for x in [.56,.88] for a in angles]
            fs=[(i,i+1,50+i,49+i) for i in range(48)]
            ob=G.mesh('Wheelwell_'+end+side,verts,fs,b.m['rubber']);sol=ob.modifiers.new('Liner thickness','SOLIDIFY');sol.thickness=.002;G.apply(ob);b.add(ob,category='liners')
            outline=[(axle+(S.ARCH_RADIUS+.012)*math.cos(a),S.HUB_HEIGHT+(S.ARCH_RADIUS+.012)*math.sin(a)) for a in angles]
            b.add(G.profile('Wheelwell inboard_'+end+side,outline,sign*.559,sign*.561,b.m['rubber'],axis='X'),category='liners')
    fascia(b,front=True,master_tree=tree);fascia(b,front=False,master_tree=tree)
    # Only a cavity closure is supplied at this gate, not an interior or drivetrain.
    floor=G.box('Form cavity closure',(0,.05,.235),(1.62,3.95,.025),b.m['rubber'],0);b.add(floor,category='closure')
    handles(b)
    # Boolean aperture cuts can change the rim smoothing fans again. Reapply the
    # pre-cut master field to every exposed outer corner, with flat gauge edges.
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('part_category') not in ['body','doors','glass','pillars','fascia']:continue
        material=next((m for m in ob.data.materials if m),None)
        if material is None:raise ValueError(('Missing form material',ob.name,len(ob.data.vertices),len(ob.data.polygons)))
        ob.data.materials.clear();ob.data.materials.append(material)
        for face in ob.data.polygons:face.material_index=0
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


def face_y(x,z,front):
    sign=-1 if front else 1
    sweep=.270 if front else .185
    return sign*(S.LENGTH/2+END_ALLOWANCE[front]-sweep*(abs(x)/.925)**4-face_depth(z,front))


def form_blank(name,rows,material,master_tree,front):
    """A sampled, conforming blank; a single n-gon chords through the crown."""
    vertices=[];nu=len(rows[0])
    for row in rows:
        for guess in row:
            hit,n,_,_=master_tree.find_nearest(Vector(guess))
            if n.dot(Vector((hit.x,-.8 if front else .8,0)))<0:n.negate()
            vertices.append(hit+n*.003)
    faces=[(j*nu+i,j*nu+i+1,(j+1)*nu+i+1,(j+1)*nu+i) for j in range(len(rows)-1) for i in range(nu-1)]
    ob=G.mesh(name,vertices,faces,material)
    hint=Vector((0,-1 if front else 1,0))
    if ob.data.polygons[0].normal.dot(hint)<0:
        for face in ob.data.polygons:face.flip()
    sol=ob.modifiers.new('Form blank gauge','SOLIDIFY');sol.thickness=.0015;sol.offset=-1;sol.use_even_offset=False
    return ob


def lamp_volume(b,front,sign,material,master_tree):
    path=[]
    for t in [0,.12,.35,.62,.84,1]:
        x=.425+.471*t;z=(.714+.017*t if front else .955+.003*t)
        path.append((x,face_y(x,z,front),z,.076-.034*t if front else .080-.020*t))
    path += [(.910,-2.130 if front else 2.130,.752 if front else .968,.040 if front else .058),
             (.915,-2.015 if front else 2.015,.768 if front else .980,.030 if front else .045)]
    dense=[]
    for a,c in zip(path,path[1:]):
        dense.extend([tuple(a[k]+(c[k]-a[k])*t for k in range(4)) for t in [0,.5]])
    dense.append(path[-1])
    rows=[[(sign*x,y,z+h*(v-.5)) for x,y,z,h in dense] for v in [0,.5,1]]
    return form_blank(('Headlamp' if front else 'Taillamp')+' opening'+str(sign),rows,material,master_tree,front)


def fascia(b,front,master_tree):
    """Compound molding sampled across crown and vertical support sections."""
    sign=-1 if front else 1
    ob=bpy.data.objects['Front molded fascia' if front else 'Rear molded fascia']
    openings=([('Low wide grille',(0,-2.43,.492),(1.24,.34,.235),.040),
               ('Lower intake',(0,-2.41,.293),(1.45,.32,.065),.018),
               ('DRL pocket L',(-.743,-2.34,.404),(.160,.30,.105),.025),
               ('DRL pocket R',(.743,-2.34,.404),(.160,.30,.105),.025)] if front else
              [('Diffuser',(0,2.43,.325),(1.45,.32,.140),.026),('Plate pocket',(0,2.43,.815),(.35,.23,.18),.022)])
    for name,center,size,radius in openings:
        # Form locators, like the lamp blanks below. Cutting detailed wells into
        # thin high-density shells belongs to the next construction stage.
        rows=[];nu=24 if size[0]>1 else 12;r=radius*.7
        for j in range(5):
            zz=(j/4-.5)*(size[2]-.010);dz=max(0,abs(zz)-((size[2]-.010)/2-r))
            cut=r-math.sqrt(max(0,r*r-dz*dz));half=(size[0]-.010)/2-cut;z=center[2]+zz
            rows.append([(center[0]+(2*i/nu-1)*half,face_y(center[0]+(2*i/nu-1)*half,z,front),z) for i in range(nu+1)])
        backing=form_blank(name+' opening',rows,b.m['rubber'],master_tree,front)
        b.add(backing,category='openings')
    # Conforming lamp blanks establish the aperture outline at this form gate.
    # Full optical seats belong with the later lamp construction. Swept boolean
    # subtraction was unstable at the inner corner on the high source; a failed
    # cut must never silently discard an entire quarter or fender.
    for side,sgn in [('L',-1),('R',1)]:
        lamp=lamp_volume(b,front,sgn,b.m['glass'],master_tree);b.add(lamp,category='openings')


def handles(b):
    for side,sign in [('L',-1),('R',1)]:
        for end,y in [('F',-.02),('R',1.08)]:
            # Recess proxy only; full handle and latch construction is deferred.
            pocket=G.box('Handle opening_'+end+side,(sign*.911,y,.945 if end=='F' else .995),(.006,.155,.032),b.m['rubber'],.010,3)
            b.add(pocket,bpy.data.objects['Door_'+end+side],category='openings')
