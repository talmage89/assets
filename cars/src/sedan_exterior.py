"""Original S240 optics, trims and functional rigid exterior assemblies."""
import math
import bpy,bmesh
from mathutils import Vector,Matrix
from kit import model as G
from detail_helpers import box,tube,loop,print_quad,pivot
from sedan_check import mesh_tree
from sedan_fairness import field
import sedan_spec as S


def world_parent(ob,parent):
    bpy.context.view_layer.update();world=ob.matrix_world.copy();ob.parent=parent;ob.matrix_world=world


def repivot(ob,position,limits):
    bpy.context.view_layer.update();children={c:c.matrix_world.copy() for c in ob.children}
    ob.location=position;ob['range_degrees']=list(limits);bpy.context.view_layer.update()
    for c,matrix in children.items():c.matrix_world=matrix


def perimeter(ob,tolerance=.0012):
    """Ordered boundary of the actual outside skin, excluding gauge backs."""
    roles=ob.data.attributes.get('sheet_role');count=ob.get('lens_outer_faces')
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
            if (p-a-v*t).length<tolerance:
                points.pop(i);changed=True;break
    return points


def glazing_loop(b,name,points,radius,material,parent,normal):
    """Closed trim follows the pane's normal without transport flips or caps."""
    rings=[];count=12 if b.high else 4
    for i,p in enumerate(points):
        n=normal(p);t=(points[(i+1)%len(points)]-points[i-1]).normalized()
        v=t.cross(n).normalized();n=v.cross(t).normalized()
        rings.append([p+radius*(n*math.cos(math.tau*k/count)+v*math.sin(math.tau*k/count)) for k in range(count)])
    ob=G.ring_loft(name,rings,material)
    bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    return b.add(G.smooth(ob),parent,'trim')


def optics(b):
    from mathutils.bvhtree import BVHTree
    from sedan_upper_surface import ease
    def back_direction(p):
        radial=Vector((p.x,p.y-1.42,0)).normalized()
        return Vector((0,1,0)).lerp(radial,ease(.64,.78,abs(p.x))).normalized()
    def guide_curve(points):
        """Bound every authored station against its final chord, in meters."""
        def distance(p,a,c):
            d=c-a;t=max(0,min(1,(p-a).dot(d)/max(d.length_squared,1e-15)))
            return (p-a-d*t).length
        def split(first,last):
            if last-first<2:return [first,last]
            error,index=max((distance(points[i],points[first],points[last]),i) for i in range(first+1,last))
            if error<=.0003:return [first,last]
            return split(first,index)[:-1]+split(index,last)
        ids=list(range(len(points))) if b.high else split(0,len(points)-1)
        measured=max((min(distance(p,points[a],points[c]) for a,c in zip(ids,ids[1:])) for p in points),default=0.)
        return [points[i] for i in ids],measured
    skin_points=[];skin_faces=[];skin_gauges=[]
    for panel in bpy.context.scene.objects:
        if panel.type!='MESH' or panel.get('part_category') not in ['body','doors','fascia']:continue
        roles=panel.data.attributes.get('sheet_role')
        if roles is None:continue
        panel.data.calc_loop_triangles();start=len(skin_points)
        skin_points.extend(panel.matrix_world@v.co for v in panel.data.vertices)
        for tri in panel.data.loop_triangles:
            if roles.data[tri.polygon_index].value!=0:continue
            skin_faces.append(tuple(start+i for i in tri.vertices));skin_gauges.append(.003 if panel.get('part_category')=='fascia' else .0009)
    skin_tree=BVHTree.FromPolygons(skin_points,skin_faces,all_triangles=True)
    lamps=[o for o in bpy.context.scene.objects if o.name.startswith(('Headlamp opening','Taillamp opening'))]
    for cover in lamps:
        front=cover.name.startswith('Headlamp');parent=cover.parent
        raw=list(cover['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
        nu,nv=cover['form_columns'],cover['form_rows'];normal=field([cover]).nearest_normal
        if front:
            inverse=cover.matrix_world.inverted()
            for v in cover.data.vertices:
                p=cover.matrix_world@v.co;v.co=inverse@(p-normal(p)*.0010)
            ps=[p-normal(p)*.0010 for p in ps];cover['aperture_samples']=[q for p in ps for q in p]
        boundary=perimeter(cover,.0004 if not front else .0012);ns=[normal(p) for p in boundary]
        if front:
            sign=1 if ps[0].x>0 else -1
            bucket_direction=Vector((sign*.12,-.65,.75)).normalized()
            ns=[bucket_direction for p in boundary]
        else:
            # The shallow tail cassette draws horizontally into the body.
            # Following the deck's rapidly turning normal folds its chrome
            # bed and return through the painted lower edge of the opening.
            ns=[back_direction(p) for p in boundary]
        depth=.100 if front else .016
        rings=[[p-n*d for p,n in zip(boundary,ns)] for d in [.001,depth]]
        if front or cover.get('lamp_piece'):
            support=skin_tree;gauges=skin_gauges
            if not front:
                owner='Trunk outer' if cover.get('lamp_piece')=='lid' else 'Rear quarter_'+('L' if ps[0].x<0 else 'R')
                panel=bpy.data.objects[owner];panel.data.calc_loop_triangles();roles=panel.data.attributes['sheet_role']
                support=BVHTree.FromPolygons([panel.matrix_world@v.co for v in panel.data.vertices],
                    [tuple(t.vertices) for t in panel.data.loop_triangles if roles.data[t.polygon_index].value==0],all_triangles=True)
                gauges=None
            center=sum(boundary,Vector())/len(boundary)
            def mount(p,tangent):
                direction=bucket_direction if front else back_direction(p)
                if not front and abs(abs(p.x)-(.61275 if cover.get('lamp_piece')=='lid' else .61725))<.00015:
                    seat=p-direction*.004
                    return seat,(seat-(p-direction*.0022)).length
                outward=tangent.cross(normal(p)).normalized()
                if outward.dot(p-center)<0:outward.negate()
                actual_support=skin_tree if not front and cover.get('lamp_piece')=='quarter' else support
                # Rear flanges overlap the stamping by a nominal 6 mm.
                # Merely snapping a sparse ring onto the cut edge leaves
                # triangular gaps wherever that edge curves between stations.
                hit,n,fi,_=actual_support.find_nearest(p+outward*(.006 if front else .010))
                seat=hit-n*((gauges[fi] if gauges is not None else .0009)+.00025)
                span=(seat-(p-direction*.0022)).length
                land=.040 if front else .030
                if span>land:raise ValueError(('Optical flange exceeds its mounting land',cover.name,span,land))
                return seat,span
            entries=[(p,*mount(p,boundary[(i+1)%len(boundary)]-boundary[i-1])) for i,p in enumerate(boundary)]
            boundary=[r[0] for r in entries];mouth=[r[1] for r in entries]
            ns=[bucket_direction if front else back_direction(p) for p in boundary]
            rings=[[p-normal(p)*.0015 for p in boundary],mouth,[p-(bucket_direction if front else normal(p))*depth for p in boundary]]
            cover['casing_flange_max_span_m']=max(r[2] for r in entries)
            cover['casing_mounting_curve_vertices']=len(entries)
        if cover.get('lamp_piece')=='lid':
            # The hidden cassette clears the lid hinge envelope. The bonded
            # lip and mounting land reach the actual .61275 m lens edge;
            # clamping those as well leaves a visible hole into the cabin.
            for p in rings[-1]:p.x=max(-.607,min(.607,p.x))
        if front:
            # The drawn bucket closes directly from lens rim to rear shell.
            # Its mounting flange branches outward; routing the bucket wall
            # through that flange left a tunnel behind the wrapped outer tip.
            count=len(boundary);vertices=[p for ring in rings for p in ring];faces=[]
            for target in [1,2]:
                for i in range(count):
                    j=(i+1)%count;faces.append((i,j,target*count+j,target*count+i))
            housing=G.mesh('S240 optical housing '+cover.name,vertices,faces,b.m['plastic'])
        else:housing=G.loft('S240 optical housing '+cover.name,rings,b.m['plastic'],caps=False)
        if b.high:
            sol=housing.modifiers.new('Optical housing wall','SOLIDIFY');sol.thickness=.0015;sol.offset=-1;sol.use_even_offset=False;G.apply(housing)
        else:housing['allow_boundary']=True
        b.add(housing,parent,'lamps')
        if front:
            # Close the whole swept rim, rather than a ruled strip between
            # two guide rows. That strip left the curved side borders open.
            from mathutils.geometry import delaunay_2d_cdt
            back_points=[p.copy() for p in rings[-1]];count=len(back_points)
            back_points += [ps[(nv//2)*nu+i]-bucket_direction*depth for i in range(1,nu-1,3)]
            u=bucket_direction.cross(Vector((0,0,1))).normalized();v=bucket_direction.cross(u).normalized()
            coords=[Vector((p.dot(u),p.dot(v))) for p in back_points];outline=list(range(count))
            result,_,back_faces,original,*_=delaunay_2d_cdt(coords,list(zip(outline,outline[1:]+outline[:1])),[outline],1,1e-8)
            if any(not ids for ids in original):raise ValueError('Front cassette closure created an unowned vertex')
            back_points=[back_points[ids[0]] for ids in original]
        else:
            # Close the actual cassette rim. The former ruled strip joined
            # only its first/last rows, leaving holes where the lens's curved
            # side borders departed from that chord. A constrained physical
            # disk shares every back-rim vertex with the housing return.
            from mathutils.geometry import delaunay_2d_cdt
            from sedan_optical_surface import chart
            back_points=[p.copy() for p in rings[-1]];count=len(back_points)
            back_points += [ps[(nv//2)*nu+i]-normal(ps[(nv//2)*nu+i])*depth for i in range(1,nu-1,3)]
            coords=[chart(p,False).to_2d() for p in back_points];outline=list(range(count))
            result,_,back_faces,original,*_=delaunay_2d_cdt(coords,list(zip(outline,outline[1:]+outline[:1])),[outline],1,1e-8)
            if any(not ids for ids in original):raise ValueError('Cassette closure created an unowned vertex')
            back_points=[back_points[ids[0]] for ids in original]
            if sum((back_points[f[1]]-back_points[f[0]]).cross(back_points[f[2]]-back_points[f[0]]).y for f in back_faces)<0:back_faces=[tuple(reversed(f)) for f in back_faces]
        back=G.mesh('S240 optical back '+cover.name,back_points,back_faces,b.m['dark_chrome'] if front else b.m['chrome'])
        if b.high:
            sol=back.modifiers.new('Optical backing gauge','SOLIDIFY');sol.thickness=.0015;sol.offset=-1;sol.use_even_offset=False;G.apply(back)
        else:back['allow_boundary']=True
        bm=bmesh.new();bm.from_mesh(back.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
        if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
        bm.to_mesh(back.data);bm.free()
        G.smooth(back,70)
        b.add(back,parent,'lamps')
        cover.data.materials.clear();cover.data.materials.append(b.m['lens'] if front else b.m['rear_cover'])
        cover['part_category']='glass' if front else 'lamps'
        fractions=list(cover.get('form_row_fractions',[j/(nv-1) for j in range(nv)]))
        from bisect import bisect_right
        lower=max(0,min(nv-2,bisect_right(fractions,.5)-1));upper=lower+1
        mix=(.5-fractions[lower])/(fractions[upper]-fractions[lower])
        mid=[ps[lower*nu+i].lerp(ps[upper*nu+i],mix) for i in range(nu)]
        def at(fraction):
            t=max(0,min(nu-1,fraction*(nu-1)));i=min(nu-2,int(t))
            return mid[i].lerp(mid[i+1],t-i)
        lens_tree=mesh_tree([cover])
        for direction,label in [(-1,'lower'),(1,'upper')]:
            path=[]
            for i,p in enumerate(mid):
                if front:
                    width=(ps[(nv-1)*nu+i]-ps[i]).length
                    if width<(.026 if direction<0 else .014):continue
                    margin=max(.12,.006/width)
                    row=margin if direction<0 else 1-margin if width>=.026 else .5
                    lo=max(0,min(nv-2,bisect_right(fractions,row)-1));t=(row-fractions[lo])/(fractions[lo+1]-fractions[lo])
                    path.append(ps[lo*nu+i].lerp(ps[(lo+1)*nu+i],t))
                else:
                    row=.10 if direction<0 else .90
                    lo=max(0,min(nv-2,bisect_right(fractions,row)-1));t=(row-fractions[lo])/(fractions[lo+1]-fractions[lo])
                    path.append(ps[lo*nu+i].lerp(ps[(lo+1)*nu+i],t))
            if not b.high and not front and cover.get('lamp_piece')=='lid':
                path=path[::2]+([path[-1]] if path[::2][-1]!=path[-1] else [])
            # A 9 mm original twin-blade signature, following the swept cover.
            guide=[p-normal(p)*.012 if front else p-back_direction(p)*.008 for p in path]
            guide,chord_error=guide_curve(guide)
            guide_ob=tube(b,'S240 '+label+' light guide '+cover.name,guide,.0045 if front else .004,b.m['drl'] if front else b.m['brakelight'],'lamps',parent,sides=4)
            guide_ob['measured_guide_chord_error_m']=chord_error
        if front:
            for fraction,radius,label in [(.15,.026,'low')]:
                p=at(fraction)-normal(at(fraction))*.045;n=Vector((.06*(1 if p.x>0 else -1),-1,.05)).normalized()
                # Closed formed reflector, convex optic and phosphor behind it.
                for part,profile,mat in [
                    ('reflector',[(-.050,0),(-.048,radius*.55),(-.023,radius*1.12),(-.012,radius*1.12),(-.012,radius*.96),(-.045,radius*.46),(-.046,0)],b.m['chrome']),
                    ('optic',[(-.018,0),(-.018,radius*.85),(-.011,radius*.91),(-.007,radius*.65),(-.005,0)],b.m['lens']),
                    ('phosphor',[(-.040,0),(-.040,radius*.45),(-.037,radius*.45),(-.037,0)],b.m['headlight'])]:
                    ob=G.lathe('S240 '+label+' '+part+' '+cover.name,profile,mat,32 if b.high else 16)
                    ob.location=p;ob.rotation_euler=n.to_track_quat('Z','Y').to_euler();b.add(ob,parent,'lamps')
            # Amber reflector follows the outer return, seated behind the cover.
            path=[at(.72+.10*i/3) for i in range(4)]
            path=[p-normal(p)*.014 for p in path]
            tube(b,'S240 amber side marker '+cover.name,path,.0035,b.m['amber'],'lamps',parent,sides=4)
        else:
            # A bright reverse window inside the red wing, on the lid half.
            if cover.get('lamp_piece')=='lid':
                path=[p-normal(p)*.006 for p in (mid[1:-1] if b.high else mid[1:-1:2])]
                tube(b,'S240 reverse optic '+cover.name,path,.007,b.m['lens'],'lamps',parent,sides=4)
    for ob in list(bpy.context.scene.objects):
        if ob.name.startswith('Rear reflector_'):
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
            uv.data[li].uv=(p.x/1.28+.5,(p.z-.535)/.21)
    raw=list(grille['well_mouth_samples']);rim=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    surround=bpy.data.objects['Low wide grille opening molded return']
    surround.data.materials.clear();surround.data.materials.append(b.m['dark_chrome'])
    for side in ['L','R']:
        pocket=bpy.data.objects['DRL pocket '+side+' opening'];raw=list(pocket['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
        nu=pocket['form_columns'];tube(b,'S240 corner DRL '+side,ps[3*nu+1:4*nu-1],.0045,b.m['drl'],'lamps',sides=4)


def trim(b):
    body=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('part_category') in ['body','doors','fascia','pillars']]
    tree=mesh_tree(body)
    def side_point(sign,y,z):
        p,n,_,_=tree.ray_cast(Vector((sign*2,y,z)),Vector((-sign,0,0)),4)
        if p is None:raise ValueError(('No trim support',y,z))
        return p,n
    for side,sign in [('L',-1),('R',1)]:
        # Real cap width is carried outboard of the fixed A-pillar foot.
        # Preserve its outer extent and compound rings while narrowing the
        # unnecessarily long inboard throat of the form-stage locator.
        cap=bpy.data.objects['Mirror housing_'+side]
        for ob in [cap,bpy.data.objects['Mirror pane_'+side]]:
            inverse=ob.matrix_world.inverted()
            positions=[ob.matrix_world@v.co for v in ob.data.vertices]
            lo=min(abs(p.x) for p in positions);hi=max(abs(p.x) for p in positions)
            for v,p in zip(ob.data.vertices,positions):
                fraction=(abs(p.x)-lo)/(hi-lo)
                p.z=.990+(p.z-.990)*.65
                t=max(0,min(1,(p.z-.950)/.085));t=t*t*(3-2*t)
                target=.925-.055*t
                hit=tree.ray_cast(Vector((sign*2,p.y,p.z)),Vector((-sign,0,0)),4)[0]
                if hit is not None:target=max(target,abs(hit.x)+.008)
                if ob!=cap:target+=.005
                p.x=sign*(target+fraction*(hi-target));v.co=inverse@p
        G.smooth(cap,70)
        old=bpy.data.objects['Mirror stalk_'+side];bpy.data.objects.remove(old,do_unlink=True)
        p,n=side_point(sign,-.925,.925)
        tube(b,'Mirror stalk_'+side,[p+n*.004,(sign*.945,-.91,.95),(sign*.960,-.85,.978)],.013,b.m['rubber'],'mirrors',bpy.data.objects['Door_F'+side],sides=8)
        for end,y in [('F',-.16),('R',1.00)]:
            old=bpy.data.objects.get('Handle opening_'+end+side)
            if old:bpy.data.objects.remove(old,do_unlink=True)
            parent=bpy.data.objects['Door_'+end+side];z=.940 if end=='F' else .966
            path=[]
            for dy,off in [(-.072,.002),(-.056,.016),(0,.021),(.056,.016),(.072,.002)]:
                p,n=side_point(sign,y+dy,z);path.append(p+n*off)
            tube(b,'S240 pull handle '+end+side,path,.0075,b.m['body'],'trim',parent,sides=6)
            # Shallow dark molded finger cup, following the actual upper door.
            rings=[]
            for d in [0,.002]:
                rings.append([side_point(sign,y+u,z+v)[0]+Vector((sign*d,0,0)) for u,v in G.rounded_rectangle(.16,.041,.013,2)])
            b.add(G.loft('S240 handle cup '+end+side,rings,b.m['plastic']),parent,'trim')
        for name,parent_name in [('Front side glass_'+side,'Door_F'+side),('Rear side glass_'+side,'Door_R'+side),('Quarter glass_'+side,S.NAME)]:
            glass=bpy.data.objects[name];world_parent(glass,bpy.data.objects[parent_name]);points=perimeter(glass)
            normal=field([glass]).nearest_normal
            center=sum(points,Vector())/len(points)
            seal=[]
            for i,p in enumerate(points):
                n=normal(p)
                if name.startswith('Front side glass'):
                    tangent=points[(i+1)%len(points)]-points[i-1]
                    inward=n.cross(tangent).normalized()
                    if inward.dot(center-p)<0:inward.negate()
                    offset=inward*.0028
                else:offset=(center-p).normalized()*.002
                seal.append(p+n*.003+offset)
            glazing_loop(b,'S240 window seal '+name,seal,.002,b.m['rubber'],glass.parent,normal)
            # Dark chrome retains a thin bright edge, rather than a white frame.
            bright=[]
            for i,p in enumerate(points):
                n=normal(p);t=points[(i+1)%len(points)]-points[i-1];inward=n.cross(t).normalized()
                if inward.dot(center-p)<0:inward.negate()
                bright.append(p+n*.005+inward*(.003 if name.startswith('Front side glass') else 0))
            glazing_loop(b,'S240 window brightwork '+name,bright,.0018,b.m['dark_chrome'],glass.parent,normal)
        # A static, flush fuel flap with a causal black reveal.
        y,z=1.65,.91;boundary=[]
        for i in range(20):
            a=math.tau*i/20;p,n=side_point(sign,y+.070*math.cos(a),z+.070*math.sin(a));boundary.append(p+n*.001)
        if side=='L':
            tube(b,'S240 fuel door reveal',boundary+[boundary[0]],.0018,b.m['rubber'],'trim',sides=4)
            p,n=side_point(sign,y,z);rings=[[q+n*d for q in boundary] for d in [.0003,.0013]]
            b.add(G.loft('S240 fuel flap',rings,b.m['body']),category='trim')
    for name in ['Windshield','Backlight']:
        glass=bpy.data.objects[name];points=perimeter(glass);normal=field([glass]).nearest_normal
        center=sum(points,Vector())/len(points)
        # Molded glass has its own crown; a real urethane mounting bead bridges
        # that laminate to the cut steel. Do not bend the glass into the rail's
        # tight roll just to force its border onto the stamped-body normals.
        from mathutils.bvhtree import BVHTree
        ps=[];fs=[]
        for panel in bpy.context.scene.objects:
            if panel.type!='MESH' or panel.name=='Hood outer' or panel.get('part_category') not in ['body','pillars']:continue
            roles=panel.data.attributes.get('sheet_role')
            if roles is None:continue
            panel.data.calc_loop_triangles();start=len(ps);ps.extend(panel.matrix_world@v.co for v in panel.data.vertices)
            fs.extend(tuple(start+i for i in t.vertices) for t in panel.data.loop_triangles if roles.data[t.polygon_index].value==0)
        support=BVHTree.FromPolygons(ps,fs,all_triangles=True);bed=[];laminate=[];distances=[]
        for i,p in enumerate(points):
            n=normal(p);tangent=points[(i+1)%len(points)]-points[i-1]
            outward=tangent.cross(n).normalized()
            if outward.dot(p-center)<0:outward.negate()
            hit,sn,_,distance=support.find_nearest(p+outward*.004)
            if distance>.025:raise ValueError(('Bonded glazing has no nearby steel mounting land',name,distance))
            laminate.append(p-n*.0047);bed.append(hit-sn*.0012);distances.append(distance)
        adhesive=G.loft('S240 urethane mounting bead '+name,[laminate,bed],b.m['rubber'],caps=False)
        sol=adhesive.modifiers.new('Bonded urethane gauge','SOLIDIFY');sol.thickness=.001;sol.offset=-1;sol.use_even_offset=False;G.apply(adhesive)
        b.add(adhesive,glass.parent,'trim');glass['measured_mounting_land_max_distance_m']=max(distances)
        seal=[p+normal(p)*.001+(center-p).normalized()*.003 for p in points]
        tube(b,'S240 bonded seal '+name,seal+[seal[0]],.0018,b.m['rubber'],'trim',sides=4)
    # Parked wipers lie on the actual glass, just behind the hood's rear edge.
    windshield=mesh_tree([bpy.data.objects['Windshield']])
    for i,(lo,hi) in enumerate([(-.69,-.08),(.05,.66)]):
        path=[]
        for j in range(7):
            x=lo+(hi-lo)*j/6;p=windshield.ray_cast(Vector((x,-1.025,2)),Vector((0,0,-1)),3)[0]
            if p is not None:path.append(p+Vector((0,0,.005)))
        if len(path)<3:raise ValueError('Parked wiper missed its glass')
        tube(b,'S240 wiper blade '+str(i),path,.0033,b.m['rubber'],'trim',sides=6)
        tube(b,'S240 wiper arm '+str(i),[path[-1]+Vector((0,.015,.005)),path[len(path)//2]+Vector((0,-.003,.012))],.004,b.m['frame'],'trim',sides=6)
    hood=mesh_tree([bpy.data.objects['Hood outer']])
    for x in [-.36,.36]:
        p=hood.ray_cast(Vector((x,-1.16,2)),Vector((0,0,-1)),3)[0]
        box(b,'S240 washer nozzle '+str(x),p+Vector((0,0,.002)),(.012,.017,.005),b.m['plastic'],'trim',bpy.data.objects['Hood'],.002)
    roof=mesh_tree([bpy.data.objects['Roof']]);p=roof.ray_cast(Vector((0,.69,2)),Vector((0,0,-1)),3)[0]
    rings=[]
    for z,w,length,yshift in [(0,.050,.14,0),(.012,.046,.13,.005),(.057,.008,.045,.015)]:
        rings.append([(p.x+u,p.y+v+yshift,p.z+z) for u,v in G.rounded_rectangle(w,length,min(w*.4,.015),2)])
    b.add(G.smooth(G.loft('S240 shark fin',rings,b.m['body'])),category='trim')
    # The existing stamped plate carries a fictional dealer insert and frame
    # relief in the atlas. Keep its physical size, fasteners and lid ownership.
    plate=bpy.data.objects['Plate blank 12x6 inch']
    plate.data.materials.clear();plate.data.materials.append(b.m['dealer'])
    ps=[plate.matrix_world@v.co for v in plate.data.vertices]
    center=sum(ps,Vector())/len(ps);u=Vector((1,0,0))
    n=next((plate.matrix_world.to_3x3()@f.normal).normalized() for f in plate.data.polygons if (plate.matrix_world.to_3x3()@f.normal).y>.5)
    up=u.cross(n).normalized()
    uv=plate.data.uv_layers.new(name='Original dealer insert')
    for face in plate.data.polygons:
        for li in face.loop_indices:
            q=ps[plate.data.loops[li].vertex_index]-center
            uv.data[li].uv=(.5-q.dot(u)/.3048,.5+q.dot(up)/.1524)
    # A molded frame returns to the plate at its inner back edge. Its hidden
    # rear is open against that substrate, rather than spending hidden faces.
    rings=[];count=None
    for width,height,depth in [(.308,.156,.0005),(.308,.156,.0035),(.292,.140,.0035),(.292,.140,.0005)]:
        outline=G.rounded_rectangle(width,height,.003,3 if b.high else 1)
        rings.append([center+u*x+up*z+n*depth for x,z in outline]);count=len(outline)
    frame=G.loft('S240 molded dealer frame',rings,b.m['plastic'],caps=False)
    if frame.data.polygons[count].normal.dot(n)<0:
        for f in frame.data.polygons:f.flip()
        frame.data.update()
    frame['allow_boundary']=True;frame['plate_contact_vertices']=list(range(3*count,4*count));frame['plate_backing']=plate.name
    b.add(frame,bpy.data.objects['Trunk'],'trim')
    # A fictional family badge in the recessed upper grille.
    g=bpy.data.objects['Low wide grille opening'];raw=list(g['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    nu=g['form_columns'];c=ps[(g['form_rows']//2)*nu+nu//2]+Vector((0,-.012,0))
    box(b,'S240 front emblem carrier',c,(.085,.012,.027),b.m['dark_chrome'],'trim',radius=.006)
    q=c+Vector((0,-.007,0))
    ob=print_quad(b,'S240 original Alder emblem',[(q.x-.039,q.y,q.z-.011),(q.x+.039,q.y,q.z-.011),(q.x+.039,q.y,q.z+.011),(q.x-.039,q.y,q.z+.011)],b.m['badge'])
    ob['allow_boundary']=True
    trunk=tree.ray_cast(Vector((-.40,4,.80)),Vector((0,-1,0)),5)[0]
    if trunk is not None:
        y=trunk.y+.002
        ob=print_quad(b,'S240 model badge',[(-.475,y,.786),(-.325,y,.786),(-.325,y,.817),(-.475,y,.817)],b.m['model'],parent=bpy.data.objects['Trunk'])
        ob['allow_boundary']=True


def hinges(b):
    for name in ['Plate pocket opening','Plate pocket opening molded return']:
        world_parent(bpy.data.objects[name],bpy.data.objects['Trunk'])
    for side,sign in [('L',-1),('R',1)]:
        for end,y in [('F',S.DOOR_FRONT-.010),('R',S.DOOR_SPLIT+.015)]:
            door=bpy.data.objects['Door_'+end+side]
            limit=60 if end=='F' else 68
            repivot(door,(sign*(.880 if end=='F' else .865),y,.74),(-limit,0) if sign>0 else (0,limit))
            # Keep the child mesh frame in vehicle coordinates. The hinge's
            # arbitrary axis is explicit for quaternion animation; this also
            # avoids inflating world bounds by rotating a local mesh AABB.
            door['pivot_axis']='CUSTOM'
            door['hinge_axis_vehicle']=list(Vector((sign*.14,0,1)).normalized())
        # Gooseneck is carried by the trunk pivot at its actual forward axis.
        lid=mesh_tree([bpy.data.objects['Trunk outer']])
        contact=lid.ray_cast(Vector((sign*.48,2.13,.7)),Vector((0,0,1)),1)[0]
        if contact is None:raise ValueError('Gooseneck misses the actual lid underside')
        contact.z+=.0003
        tube(b,'S240 trunk gooseneck '+side,[(sign*.48,1.72,1.01),(sign*.48,1.63,.74),(sign*.48,2.10,.74),contact],.012,b.m['frame'],'hinges',bpy.data.objects['Trunk'],sides=8)
        box(b,'S240 trunk bearing support '+side,(sign*.509,1.72,.8125),(.024,.050,.395),b.m['frame'],'hinges',radius=0)
        box(b,'S240 trunk hinge bearing '+side,(sign*.48,1.72,1.01),(.05,.055,.035),b.m['frame'],'hinges',radius=.005)
    repivot(bpy.data.objects['Trunk'],(0,1.72,1.01),(0,72))
    repivot(bpy.data.objects['Hood'],(0,-1.080,.977),(-62,0))
    for side,sign in [('L',-1),('R',1)]:
        lower=Vector((sign*.66,-1.045,.70))
        hood_surface=mesh_tree([bpy.data.objects['Hood outer']])
        contact=hood_surface.ray_cast(Vector((sign*.66,-1.65,2)),Vector((0,0,-1)),3)[0]
        upper=contact-Vector((0,0,.020));direction=(upper-lower).normalized()
        box(b,'S240 hood strut upper bracket '+side,upper+Vector((0,0,.010)),(.028,.035,.020),b.m['frame'],'hinges',bpy.data.objects['Hood'],radius=0)
        box(b,'S240 hood strut lower bracket '+side,lower+Vector((0,.006,0)),(.028,.025,.030),b.m['frame'],'hinges',radius=0)
        for label,position,target,parent,mat,radius in [('sleeve',lower,upper,b.root,b.m['frame'],.011),('rod',upper,lower,bpy.data.objects['Hood'],b.m['chrome'],.005)]:
            root=pivot(b,'S240 hood strut '+label+' '+side,position,parent,axis='Z',limits=(0,0))
            root.rotation_euler=(target-position).to_track_quat('Z','Y').to_euler()
            # Reapply world pose after parenting to the hood's translated frame.
            world=Matrix.Translation(position)@(target-position).to_track_quat('Z','Y').to_matrix().to_4x4();root.matrix_world=world
            endpoint=pivot(b,'S240 strut target '+label+' '+side,target,bpy.data.objects['Hood'] if label=='sleeve' else b.root)
            con=root.constraints.new('DAMPED_TRACK');con.target=endpoint;con.track_axis='TRACK_Z'
            if label=='sleeve':
                ob=G.lathe('S240 telescoping sleeve '+side,[(0,0),(0,.011),(.45,.011),(.45,.0062),(.035,.0062),(.035,0)],mat,12 if b.high else 8)
                ob.matrix_world=world
            else:ob=G.cylinder('S240 telescoping '+label+' '+side,position,position+(target-position).normalized()*.45,radius,mat,10 if b.high else 8)
            b.add(ob,root,'hinges')
            root['support_target']=endpoint.name;root['closed_length_m']=(target-position).length;root['member_length_m']=.45


def build(b):
    # Distinct glass, rubber, dark chrome and optics replace form-only materials.
    for o in bpy.context.scene.objects:
        if o.type!='MESH':continue
        if o.name=='Windshield':material=b.m['glass']
        elif o.name=='Backlight':material=b.m['rear_glass']
        elif o.name.startswith('Front side glass'):material=b.m['side_glass']
        elif o.name.startswith(('Rear side glass','Quarter glass')):material=b.m['privacy']
        else:continue
        o.data.materials.clear();o.data.materials.append(material)
    optics(b);seat_returns(b);seat_finisher(b);trim(b);hinges(b)


def seat_returns(b):
    """Seat molded well mouths on actual cut steel, not their old locators."""
    from mathutils.bvhtree import BVHTree
    vertices=[];faces=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('part_category') not in ['body','doors','fascia']:continue
        roles=ob.data.attributes.get('sheet_role')
        if roles is None:continue
        start=len(vertices);vertices.extend(ob.matrix_world@v.co for v in ob.data.vertices);ob.data.calc_loop_triangles()
        faces.extend(tuple(start+i for i in tri.vertices) for tri in ob.data.loop_triangles if roles.data[tri.polygon_index].value==0)
    support=BVHTree.FromPolygons(vertices,faces,all_triangles=True)
    for old in [o for o in bpy.context.scene.objects if o.name.endswith(' opening molded return')]:
        blank=bpy.data.objects[old.name.removesuffix(' molded return')];raw=list(blank['well_mouth_samples']);points=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];count=len(points)
        if len(old.data.vertices)!=4*count:raise ValueError(('Unexpected molded return gauge',old.name,len(old.data.vertices),count))
        back=[old.matrix_world@old.data.vertices[count+i].co for i in range(count)]
        center=sum(points,Vector())/count;mouth=[];depths=[]
        for i,p in enumerate(points):
            _,n,_,_=support.find_nearest(p);t=points[(i+1)%count]-points[i-1];out=t.cross(n).normalized()
            if out.dot(p-center)<0:out.negate()
            hit,n,_,_=support.find_nearest(p+out*.012);q=hit-n*.0045;mouth.append(q)
            actual,normal,_,_=support.find_nearest(q);depths.append(-(q-actual).dot(normal))
        name=old.name;parent=old.parent;material=old.data.materials[0]
        bpy.data.objects.remove(old,do_unlink=True)
        ob=G.loft(name,[mouth,back],material,caps=False)
        sol=ob.modifiers.new('Molded return gauge','SOLIDIFY');sol.thickness=.002;sol.offset=-1;G.apply(ob)
        b.add(ob,parent,'openings');ob['actual_mounting_depth_min_max_m']=[min(depths),max(depths)]
        print('S240_RETURN_SEAT',name,min(depths),max(depths),flush=True)


def seat_finisher(b):
    """The rolled finisher clears the actual painted side silhouette.

    Probe real outer-triangle plane intersections at its vertices and edge
    midpoints. Its old flat lip stood 6–7 mm beyond the rolling valance.
    """
    ob=bpy.data.objects['Rear molded fascia'];me=ob.data;roles=me.attributes['sheet_role'];positions=[ob.matrix_world@v.co for v in me.vertices]
    edges={tuple(sorted((a,c))) for face in me.polygons if roles.data[face.index].value==0 for a,c in zip(face.vertices,list(face.vertices[1:])+[face.vertices[0]])}
    segments=[(positions[a],positions[c]) for a,c in edges];cache={}
    def outline(z):
        key=round(z,7)
        if key not in cache:
            ys=[a.y+(c.y-a.y)*(z-a.z)/(c.z-a.z) for a,c in segments if min(a.z,c.z)<=z<=max(a.z,c.z) and abs(c.z-a.z)>1e-10]
            cache[key]=max(ys) if ys else None
        return cache[key]
    lip=bpy.data.objects['Exhaust finisher rolled lip'];ps=[lip.matrix_world@v.co for v in lip.data.vertices]
    probes=ps+[(ps[e.vertices[0]]+ps[e.vertices[1]])/2 for e in lip.data.edges]
    before=min(limit-p.y for p in probes if (limit:=outline(p.z)) is not None);shift=max(0,.003-before)
    for name in ['Exhaust finisher rolled lip','Exhaust dark bore']:
        part=bpy.data.objects[name];inverse=part.matrix_world.inverted().to_3x3();delta=inverse@Vector((0,-shift,0))
        for v in part.data.vertices:v.co+=delta
        part.data.update()
    actual=[lip.matrix_world@v.co for v in lip.data.vertices];actual += [(actual[e.vertices[0]]+actual[e.vertices[1]])/2 for e in lip.data.edges]
    after=min(limit-p.y for p in actual if (limit:=outline(p.z)) is not None)
    lip['measured_side_envelope_setback_before_after_m']=[before,after];lip['measured_seating_translation_y_m']=-shift
    print('S240_FINISHER_SEAT',before,after,-shift,flush=True)
