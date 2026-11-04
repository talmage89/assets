"""Original H120 optics, trims and functional rigid exterior assemblies."""
import math
import bpy,bmesh
from mathutils import Vector,Matrix
from kit import model as G
from detail_helpers import box,tube,loop,print_quad,pivot
from hatch_check import mesh_tree
from hatch_fairness import field
import hatch_spec as S


def world_parent(ob,parent):
    bpy.context.view_layer.update();world=ob.matrix_world.copy();ob.parent=parent;ob.matrix_world=world


def repivot(ob,position,limits):
    bpy.context.view_layer.update();children={c:c.matrix_world.copy() for c in ob.children}
    ob.location=position;ob['range_degrees']=list(limits);bpy.context.view_layer.update()
    for c,matrix in children.items():c.matrix_world=matrix


def perimeter(ob):
    """Ordered boundary of the actual outside skin, excluding gauge backs."""
    roles=ob.data.attributes.get('sheet_role');count=ob.get('lens_outer_faces',ob.get('outer_skin_faces'))
    edges={}
    for f in ob.data.polygons:
        if roles is not None and roles.data[f.index].value!=0:continue
        if count is not None and f.index>=count:continue
        for a,c in zip(f.vertices,list(f.vertices[1:])+[f.vertices[0]]):
            edge=tuple(sorted((a,c)));edges[edge]=edges.get(edge,0)+1
    adjacent={}
    for (a,c),num in edges.items():
        if num==1:adjacent.setdefault(a,[]).append(c);adjacent.setdefault(c,[]).append(a)
    first=min(adjacent);indices=[first];previous=None;current=first
    for _ in range(len(adjacent)+1):
        nxt=next((i for i in adjacent[current] if i!=previous),None)
        if nxt is None or nxt==first:break
        indices.append(nxt);previous,current=current,nxt
    points=[ob.matrix_world@ob.data.vertices[i].co for i in indices]
    # Retain corners and curves while eliminating submillimeter short chords.
    changed=True
    while changed and len(points)>8:
        changed=False
        for i,p in enumerate(points):
            a,c=points[i-1],points[(i+1)%len(points)];v=c-a
            t=max(0,min(1,(p-a).dot(v)/max(v.length_squared,1e-12)))
            if (p-a-v*t).length<.0025:
                points.pop(i);changed=True;break
    return points


def optical_normal(ob):
    """Only the authored outer lens participates; inner laminate is excluded."""
    from mathutils.bvhtree import BVHTree
    from mathutils.geometry import barycentric_transform
    ob.data.calc_loop_triangles();points=[];normals=[];triangles=[]
    nm=ob.matrix_world.to_3x3().inverted().transposed()
    for tri in ob.data.loop_triangles:
        if tri.polygon_index>=ob.get('lens_outer_faces',ob.get('outer_skin_faces')):continue
        start=len(points)
        for vi,li in zip(tri.vertices,tri.loops):
            points.append(ob.matrix_world@ob.data.vertices[vi].co)
            normals.append((nm@ob.data.corner_normals[li].vector).normalized())
        triangles.append((start,start+1,start+2))
    tree=BVHTree.FromPolygons(points,triangles,all_triangles=True)
    def normal(p):
        hit,_,fi,_=tree.find_nearest(p);a,c,d=triangles[fi]
        return barycentric_transform(hit,points[a],points[c],points[d],normals[a],normals[c],normals[d]).normalized()
    return normal


def fixed_sails(b):
    """The forward triangular panes stay in the A-post; the doors carry the rest.

    Separation changes ownership, not the held glazing surface or silhouette.
    A 2 mm bonded reveal follows the existing pane in the physical surface.
    """
    from mathutils.bvhtree import BVHTree
    from mathutils.geometry import barycentric_transform
    for side in ['L','R']:
        ob=bpy.data.objects['Front side glass_'+side];matrix=ob.matrix_world.copy();inverse=matrix.inverted()
        count=ob['outer_skin_faces'];ob.data.calc_loop_triangles()
        triangles=[t for t in ob.data.loop_triangles if t.polygon_index<count]
        points=[];normals=[];faces=[]
        for t in triangles:
            start=len(points)
            for vi,li in zip(t.vertices,t.loops):
                points.append(matrix@ob.data.vertices[vi].co)
                normals.append((matrix.to_3x3().inverted().transposed()@ob.data.corner_normals[li].vector).normalized())
            faces.append((start,start+1,start+2))
        tree=BVHTree.FromPolygons(points,faces,all_triangles=True)
        def normal(p):
            hit,_,fi,_=tree.find_nearest(p);a,c,d=faces[fi]
            return barycentric_transform(hit,points[a],points[c],points[d],normals[a],normals[c],normals[d]).normalized()
        for moving in [False,True]:
            mesh=bpy.data.meshes.new('H120 partitioned front glass');mesh.from_pydata(points,[],faces);mesh.update()
            bm=bmesh.new();bm.from_mesh(mesh);bpy.data.meshes.remove(mesh)
            bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
            bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-8,
                plane_co=(0,-.875+(.001 if moving else -.001),0),plane_no=(0,1,0),clear_inner=moving,clear_outer=not moving)
            mesh=bpy.data.meshes.new('H120 fixed sail' if not moving else 'H120 door pane');bm.to_mesh(mesh);bm.free()
            new=bpy.data.objects.new('H120 fixed front pane_'+side,mesh);bpy.context.collection.objects.link(new);mesh.materials.append(b.m['side_glass'])
            nface=len(mesh.polygons);nvert=len(mesh.vertices)
            sol=new.modifiers.new('Laminated glazing gauge','SOLIDIFY');sol.thickness=.0048;sol.offset=-1;sol.use_even_offset=False;G.apply(new)
            # Modifier application replaces mesh data.
            mesh=new.data;custom=[]
            for f in mesh.polygons:
                f.use_smooth=f.index<2*nface
                for li in f.loop_indices:
                    p=mesh.vertices[mesh.loops[li].vertex_index].co
                    custom.append(normal(p)*(1 if f.index<nface else -1) if f.index<2*nface else (0,0,0))
            mesh.normals_split_custom_set(custom);new['outer_skin_faces']=nface
            b.add(new,bpy.data.objects['Door_F'+side] if moving else b.root,'glass')
            if moving:
                bpy.data.objects.remove(ob,do_unlink=True);new.name='Front side glass_'+side


def optics(b):
    lamps=[o for o in bpy.context.scene.objects if o.name.startswith(('Headlamp opening','Taillamp opening'))]
    for cover in lamps:
        front=cover.name.startswith('Headlamp');parent=cover.parent
        raw=list(cover['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
        nu,nv=cover['form_columns'],cover['form_rows'];normal=optical_normal(cover)
        if front:
            inverse=cover.matrix_world.inverted()
            for v in cover.data.vertices:
                p=cover.matrix_world@v.co;v.co=inverse@(p-normal(p)*.0018)
            ps=[p-normal(p)*.0018 for p in ps];cover['aperture_samples']=[q for p in ps for q in p]
        boundary=perimeter(cover);ns=[normal(p) for p in boundary]
        depth=.100 if front else .035
        rings=[[p-n*d for p,n in zip(boundary,ns)] for d in [.004,depth]]
        if cover.get('lamp_piece')=='gate':
            for ring in rings:
                for p in ring:p.x=max(-.607,min(.607,p.x))
        housing=G.loft('H120 optical housing '+cover.name,rings,b.m['plastic'],caps=False)
        sol=housing.modifiers.new('Optical housing wall','SOLIDIFY');sol.thickness=.0015;sol.offset=-1;sol.use_even_offset=False;G.apply(housing)
        b.add(housing,parent,'lamps')
        back=G.mesh('H120 optical back '+cover.name,rings[-1],[tuple(range(len(rings[-1])))],b.m['dark_chrome'] if front else b.m['chrome'])
        sol=back.modifiers.new('Optical backing gauge','SOLIDIFY');sol.thickness=.0015;sol.offset=-1;sol.use_even_offset=False;G.apply(back)
        bm=bmesh.new();bm.from_mesh(back.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
        if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
        bm.to_mesh(back.data);bm.free()
        b.add(back,parent,'lamps')
        cover.data.materials.clear();cover.data.materials.append(b.m['lens'] if front else b.m['rear_cover'])
        cover['part_category']='glass' if front else 'lamps'
        lower=(nv-1)//2;upper=nv//2
        mid=[(ps[lower*nu+i]+ps[upper*nu+i])*.5 for i in range(nu)]
        def at(fraction):
            t=max(0,min(nu-1,fraction*(nu-1)));i=min(nu-2,int(t))
            return mid[i].lerp(mid[i+1],t-i)
        lens_tree=mesh_tree([cover])
        for direction,label in [(-1,'lower'),(1,'upper')]:
            path=[]
            for i,p in enumerate(mid):
                n=normal(p);up=(Vector((0,0,1))-n*n.z).normalized()
                height=(ps[(nv-1)*nu+i]-ps[i]).length
                path.append(lens_tree.find_nearest(p+up*(direction*height*.40))[0])
            if not b.high and not front and cover.get('lamp_piece')=='gate':
                path=path[::2]+([path[-1]] if path[::2][-1]!=path[-1] else [])
            # A 9 mm original twin-blade signature, following the swept cover.
            guide=[p-normal(p)*(.012 if front else .008) for p in path]
            tube(b,'H120 '+label+' light guide '+cover.name,guide,.0045 if front else .004,b.m['drl'] if front else b.m['brakelight'],'lamps',parent,sides=4)
        if front:
            for fraction,radius,label in [(.15,.026,'low')]:
                p=at(fraction)-normal(at(fraction))*.010;n=Vector((.06*(1 if p.x>0 else -1),-1,.05)).normalized()
                # Closed formed reflector, convex optic and phosphor behind it.
                for part,profile,mat in [
                    ('reflector',[(-.050,0),(-.048,radius*.55),(-.023,radius*1.12),(-.012,radius*1.12),(-.012,radius*.96),(-.045,radius*.46),(-.046,0)],b.m['chrome']),
                    ('optic',[(-.018,0),(-.018,radius*.85),(-.011,radius*.91),(-.007,radius*.65),(-.005,0)],b.m['lens']),
                    ('phosphor',[(-.040,0),(-.040,radius*.45),(-.037,radius*.45),(-.037,0)],b.m['headlight'])]:
                    ob=G.lathe('H120 '+label+' '+part+' '+cover.name,profile,mat,32 if b.high else 16)
                    ob.location=p;ob.rotation_euler=n.to_track_quat('Z','Y').to_euler();b.add(ob,parent,'lamps')
            # Amber reflector follows the outer return, seated behind the cover.
            path=[at(.80+.17*i/3) for i in range(4)]
            path=[p-normal(p)*.014 for p in path]
            tube(b,'H120 amber side marker '+cover.name,path,.008,b.m['amber'],'lamps',parent,sides=4)
        else:
            # A bright reverse window inside the red wing, on the lid half.
            if cover.get('lamp_piece')=='gate':
                path=[p-normal(p)*.006 for p in (mid[1:-1] if b.high else mid[1:-1:2])]
                tube(b,'H120 reverse optic '+cover.name,path,.007,b.m['lens'],'lamps',parent,sides=4)
    for ob in list(bpy.context.scene.objects):
        if ob.name.startswith('Rear reflector'):
            ob.data.materials.clear();ob.data.materials.append(b.m['red_lens'])
        if ob.name.startswith('Mirror pane_'):
            ob.data.materials.clear();ob.data.materials.append(b.m['mirror'])
        if ob.name.startswith('Mirror housing_'):G.smooth(ob,70)
        if 'cascade vane' in ob.name and ob.name.startswith('Low wide grille'):
            ob.data.materials.clear();ob.data.materials.append(b.m['grille_bar'])
    grille=bpy.data.objects['Low wide grille opening'];grille.data.materials.clear();grille.data.materials.append(b.m['grille'])
    uv=grille.data.uv_layers.new(name='Original grille relief')
    for f in grille.data.polygons:
        for li in f.loop_indices:
            p=grille.matrix_world@grille.data.vertices[grille.data.loops[li].vertex_index].co
            uv.data[li].uv=(p.x/1.28+.5,(p.z-.477)/.215)
    raw=list(grille['well_mouth_samples']);rim=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    surround=bpy.data.objects['Grille proud surround']
    surround.data.materials.clear();surround.data.materials.append(b.m['dark_chrome'])


def trim(b):
    body=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('part_category') in ['body','doors','fascia','pillars']]
    tree=mesh_tree(body)
    def side_point(sign,y,z):
        p,n,_,_=tree.ray_cast(Vector((sign*2,y,z)),Vector((-sign,0,0)),4)
        if p is None:raise ValueError(('No trim support',y,z))
        return p,n
    for side,sign in [('L',-1),('R',1)]:
        for end,y in [('F',-.12),('R',1.12)]:
            old=bpy.data.objects.get('Handle opening_'+end+side)
            if old:bpy.data.objects.remove(old,do_unlink=True)
            parent=bpy.data.objects['Door_'+end+side];z=.960 if end=='F' else .985
            path=[]
            for dy,off in [(-.072,.002),(-.056,.016),(0,.021),(.056,.016),(.072,.002)]:
                p,n=side_point(sign,y+dy,z);path.append(p+n*off)
            tube(b,'H120 pull handle '+end+side,path,.0075,b.m['body'],'trim',parent,sides=6)
            # Shallow dark molded finger cup, following the actual upper door.
            rings=[]
            for d in [0,.002]:
                rings.append([side_point(sign,y+u,z+v)[0]+Vector((sign*d,0,0)) for u,v in G.rounded_rectangle(.16,.041,.013,2)])
            b.add(G.loft('H120 handle cup '+end+side,rings,b.m['plastic']),parent,'trim')
        for name,parent_name in [('Front side glass_'+side,'Door_F'+side),('Rear side glass_'+side,'Door_R'+side),('Quarter glass_'+side,S.NAME)]:
            glass=bpy.data.objects[name];world_parent(glass,bpy.data.objects[parent_name]);points=perimeter(glass)
            normal=field([glass]).nearest_normal
            center=sum(points,Vector())/len(points)
            seal=[p+normal(p)*.003+(center-p).normalized()*.002 for p in points]
            tube(b,'H120 window seal '+name,seal+[seal[0]],.002,b.m['rubber'],'trim',glass.parent,sides=4)
            # Dark chrome retains a thin bright edge, rather than a white frame.
            bright=[p+normal(p)*.005 for p in points]+[points[0]+normal(points[0])*.005]
            if not b.high:
                # Only the belt molding changes silhouette at game distance.
                low=min(p.z for p in points)
                ends=sorted([p for p in points if p.z<low+.040],key=lambda p:p.y)
                bright=[ends[0]+normal(ends[0])*.005,ends[-1]+normal(ends[-1])*.005]
            tube(b,'H120 window brightwork '+name,bright,.0018,b.m['dark_chrome'],'trim',glass.parent,sides=4)
        # A static, flush fuel flap with a causal black reveal.
        y,z=1.62,.91;boundary=[]
        for i in range(20):
            a=math.tau*i/20;p,n=side_point(sign,y+.070*math.cos(a),z+.070*math.sin(a));boundary.append(p+n*.001)
        if side=='L':
            tube(b,'H120 fuel door reveal',boundary+[boundary[0]],.0018,b.m['rubber'],'trim',sides=4)
            p,n=side_point(sign,y,z);rings=[[q+n*d for q in boundary] for d in [.0003,.0013]]
            b.add(G.loft('H120 fuel flap',rings,b.m['body']),category='trim')
    for name in ['Windshield','Backlight']:
        glass=bpy.data.objects[name];points=perimeter(glass);normal=optical_normal(glass)
        center=sum(points,Vector())/len(points)
        seal=[p+normal(p)*(-.009 if name=='Backlight' else .001)+(center-p).normalized()*.003 for p in points]
        tube(b,'H120 bonded seal '+name,seal+[seal[0]],(.003 if name=='Backlight' else .0018),b.m['rubber'],'trim',glass.parent,sides=4)
    # Parked wipers lie on the actual glass, just behind the hood's rear edge.
    windshield=mesh_tree([bpy.data.objects['Windshield']])
    for i,(lo,hi) in enumerate([(-.69,-.08),(.05,.66)]):
        path=[]
        for j in range(7):
            x=lo+(hi-lo)*j/6;p=windshield.ray_cast(Vector((x,-1.025,2)),Vector((0,0,-1)),3)[0]
            if p is not None:path.append(p+Vector((0,0,.005)))
        if len(path)<3:raise ValueError('Parked wiper missed its glass')
        tube(b,'H120 wiper blade '+str(i),path,.0033,b.m['rubber'],'trim',sides=6)
        tube(b,'H120 wiper arm '+str(i),[path[-1]+Vector((0,.015,.005)),path[len(path)//2]+Vector((0,-.003,.012))],.004,b.m['frame'],'trim',sides=6)
    hood=mesh_tree([bpy.data.objects['Hood outer']])
    for x in [-.36,.36]:
        p=hood.ray_cast(Vector((x,-1.16,2)),Vector((0,0,-1)),3)[0]
        box(b,'H120 washer nozzle '+str(x),p+Vector((0,0,.002)),(.012,.017,.005),b.m['plastic'],'trim',bpy.data.objects['Hood'],.002)
    roof=mesh_tree([bpy.data.objects['Roof']]);p=roof.ray_cast(Vector((0,.69,2)),Vector((0,0,-1)),3)[0]
    rings=[]
    for z,w,length,yshift in [(0,.050,.14,0),(.012,.046,.13,.005),(.057,.008,.045,.015)]:
        rings.append([(p.x+u,p.y+v+yshift,p.z+z) for u,v in G.rounded_rectangle(w,length,min(w*.4,.015),2)])
    b.add(G.smooth(G.loft('H120 shark fin',rings,b.m['body'])),category='trim')

def build(b):
    fixed_sails(b)
    # Distinct glass, rubber, dark chrome and optics replace form-only materials.
    for o in bpy.context.scene.objects:
        if o.type!='MESH':continue
        if o.name=='Windshield':material=b.m['glass']
        elif o.name=='Backlight':material=b.m['rear_glass']
        elif o.name.startswith('Front side glass'):material=b.m['side_glass']
        elif o.name.startswith(('Rear side glass','Quarter glass')):material=b.m['privacy']
        else:continue
        o.data.materials.clear();o.data.materials.append(material)
    optics(b);trim(b);grille(b);plate(b)


def grille(b):
    """Curved gloss-black chevrons, a fine diamond back mesh and Alder badge."""
    for ob in list(bpy.context.scene.objects):
        if ' blade ' in ob.name and ob.name.startswith('Low wide grille'):
            bpy.data.objects.remove(ob,do_unlink=True)
    bed=bpy.data.objects['Low wide grille opening'];tree=mesh_tree([bed])
    # Interleaved swept vanes share the recessed bed's actual plan curvature.
    for k in range(-9,10):
        x=k*.061
        path=[]
        for z in [.490,.527,.566,.604,.645,.674]:
            xx=x+.012*abs((z-.582)/.092)
            hit=tree.ray_cast(Vector((xx,-3,z)),Vector((0,1,0)),3)[0]
            if hit is not None:path.append(hit+Vector((0,-.010,0)))
        if not b.high and len(path)>3:path=[path[0],path[len(path)//2],path[-1]]
        if len(path)>2:tube(b,'H120 grille swept vane '+str(k),path,.0035,b.m['grille_bar'],'trim',sides=4)
    hit=tree.ray_cast(Vector((0,-3,.593)),Vector((0,1,0)),3)[0]
    c=hit+Vector((0,-.023,0));box(b,'H120 emblem carrier',c,(.104,.016,.035),b.m['dark_chrome'],'trim',radius=.006)
    y=c.y-.009
    ob=print_quad(b,'H120 original grille emblem',[(-.047,y,c.z-.012),(.047,y,c.z-.012),(.047,y,c.z+.012),(-.047,y,c.z+.012)],b.m['badge'])
    ob['allow_boundary']=True
    gate=mesh_tree([bpy.data.objects['Liftgate outer']])
    for label,x,z,w,h,mat in [('model',-.40,.755,.110,.025,b.m['model']),('name',0,.974,.092,.023,b.m['badge'])]:
        corners=[]
        for xx,zz in [(x+w/2,z-h/2),(x-w/2,z-h/2),(x-w/2,z+h/2),(x+w/2,z+h/2)]:
            p=gate.ray_cast(Vector((xx,3,zz)),Vector((0,-1,0)),3)[0]
            if p is None:raise ValueError('Rear badge misses its gate stamping')
            corners.append(p+Vector((0,.001,0)))
        ob=print_quad(b,'H120 original rear '+label,corners,mat,parent=bpy.data.objects['Liftgate']);ob['allow_boundary']=True


def plate(b):
    """A dealer promotional insert in a physical 12 x 6 inch frame."""
    pocket=bpy.data.objects['Plate pocket opening'];tree=mesh_tree([pocket])
    hit=tree.ray_cast(Vector((0,3,.465)),Vector((0,-1,0)),3)[0]
    c=hit+Vector((0,.002,0))
    frame=box(b,'H120 plate frame',c,(.309,.008,.157),b.m['plastic'],'trim',radius=.004)
    y=c.y+.0045
    ob=print_quad(b,'H120 dealer insert',[(.1524,y,.3888),(-.1524,y,.3888),(-.1524,y,.5412),(.1524,y,.5412)],b.m['dealer'])
    ob['allow_boundary']=True
