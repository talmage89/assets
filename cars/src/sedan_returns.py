"""Concealed unibody reveal channels, sampled on the actual exterior sheets.

The jamb and sill faces sit 35 mm behind the skin, overlap each cut by
25 mm, and have 2 mm gauge. They never change a previously approved exterior stamping.
"""
import math
import bpy,bmesh
from mathutils import Vector
from kit import model as G
from sedan_check import mesh_tree
import sedan_spec as S


def build(b):
    if not b.high:
        # The game wall omits its hidden inner sheet, retaining the real 1.5 mm
        # rim gauge where that wall meets the lens and its rear reflector.
        for ob in list(bpy.context.scene.objects):
            if not ob.name.startswith('S240 optical housing'):continue
            count=len(ob.data.polygons);sol=ob.modifiers.new('Optical rim gauge','SOLIDIFY')
            sol.thickness=.0015;sol.offset=-1;sol.use_even_offset=False;G.apply(ob)
            bm=bmesh.new();bm.from_mesh(ob.data);bm.faces.ensure_lookup_table()
            bmesh.ops.delete(bm,geom=list(bm.faces)[count:2*count],context='FACES')
            bm.to_mesh(ob.data);bm.free()
    # The wrapped outboard tip has an opaque molded shield behind the cover,
    # rather than an open path through the side of the optical cassette.
    from sedan_fairness import field
    for cover in [o for o in bpy.context.scene.objects if o.name.startswith('Headlamp opening')]:
        nu=int(cover['form_columns']);nv=int(cover['form_rows']);raw=list(cover['aperture_samples'])
        from sedan_exterior import optical_normal
        ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];normal=optical_normal(cover)
        first=min(i for i in range(nu) if sum(abs(ps[j*nu+i].x) for j in range(nv))/nv>.815)
        cols=sorted(set(round(first+(nu-1-first)*i/4) for i in range(5)))
        rows=sorted(set(round((nv-1)*j/6) for j in range(7)));stride=len(cols)
        vertices=[ps[j*nu+i]-normal(ps[j*nu+i])*.020 for j in rows for i in cols]
        faces=[(stride*j+i,stride*j+i+1,stride*(j+1)+i+1,stride*(j+1)+i) for j in range(len(rows)-1) for i in range(stride-1)]
        ob=G.mesh('S240 inner aperture liner optical side shield '+cover.name,vertices,faces,b.m['plastic'])
        ob['allow_boundary']=True;b.add(ob,category='lamps')
    # Hemmed moving closures turn down immediately behind the cut edge.
    # Their inner opening channels remain fixed; these folds travel with the lid.
    from sedan_fairness import field
    for name in ['Hood outer']:
        pane=bpy.data.objects[name];normal=field([pane]).nearest_normal
        points=max(boundary_loops(pane),key=lambda points:sum((p-q).length for p,q in zip(points,points[1:]+points[:1])))
        front=[];back=[];center=sum(points,Vector())/len(points)
        for j,p in enumerate(points):
            n=normal(p);out=(points[(j+1)%len(points)]-points[j-1]).cross(n).normalized()
            if out.dot(p-center)<0:out.negate()
            front.append(p-out*.0002-n*.0012);back.append(p-out*.0002-n*.006)
        ob=G.loft('S240 inner aperture liner moving hem '+name,[front,back],b.m['frame'],caps=False)
        ob['allow_boundary']=True
        clip_hinge_end(ob,name=='Hood outer')
        b.add(ob,pane.parent,'interior')
    # Hidden rear-corner sill closure stops ahead of the tire's rolling envelope.
    from detail_helpers import box
    for sign in [-1,1]:
        box(b,'S240 rear sill closure '+str(sign),(sign*.735,.950,.300),(.130,.100,.040),b.m['frame'],'interior',radius=0)
    skin=mesh_tree([o for o in bpy.context.scene.objects if o.type=='MESH' and
                    o.get('part_category') in ['body','doors','fascia','pillars']])
    def channel(name,rows):
        if len(rows)<2:return
        ob=G.loft(name,rows,b.m['frame']);b.add(ob,category='interior')
        ob['construction']='Concealed opening channel; measured support sections, 2 mm jamb/sill gauge, 25 mm reveal overlap'
    for side,sign in [('L',-1),('R',1)]:
        for y in [S.DOOR_FRONT,S.DOOR_SPLIT,S.DOOR_REAR]:
            rows=[]
            for z in [.282,.50,.78,1.04,1.28,1.46]:
                hits=[skin.ray_cast(Vector((sign*2,y+dy,z)),Vector((-sign,0,0)),3)[0] for dy in [-.020,.020]]
                hits=[p for p in hits if p is not None and p.x*sign>.60]
                if not hits:continue
                x=min(sign*p.x for p in hits)
                rows.append([(sign*(x-d),y+dy,z) for d,dy in [(.037,-.025),(.035,-.025),(.035,.025),(.037,.025)]])
            channel('S240 opening return '+side+' '+str(y),rows)
        rows=[]
        for i in range(13):
            y=S.DOOR_FRONT-.018+(S.DOOR_REAR-S.DOOR_FRONT+.036)*i/12
            hits=[skin.ray_cast(Vector((sign*2,y,z)),Vector((-sign,0,0)),3)[0] for z in [.280,.320]]
            hits=[p for p in hits if p is not None and p.x*sign>.65]
            if not hits:continue
            x=min(sign*p.x for p in hits)
            rows.append([(sign*(x-d),y,z) for d,z in [(.037,.279),(.035,.279),(.035,.321),(.037,.321)]])
        channel('S240 sill reveal return '+side,rows)
    for label,y in [('cowl',-1.078),('backlight sill',1.970)]:
        rows=[]
        for i in range(9):
            x=-.82+1.64*i/8
            hits=[skin.ray_cast(Vector((x,y+dy,2)),Vector((0,0,-1)),2)[0] for dy in [-.020,.020]]
            hits=[p for p in hits if p is not None and p.z>.72]
            if not hits:continue
            z=min(p.z for p in hits)-.012
            rows.append([(x,y+dy,z-d) for dy,d in [(-.022,.024),(-.022,0),(.022,0),(.022,.024)]])
        channel('S240 '+label+' opening return',rows)
    # Across the back and around both quarter returns, at the actual curved seam.
    points=[]
    for i in range(17):
        x=-.90+1.80*i/16;z=.620-.022*(x/.90)**2
        p=skin.ray_cast(Vector((x,4,z+.009)),Vector((0,-1,0)),3)[0]
        if p is not None:points.append(p-Vector((0,0,.009)))
    rows=[]
    for p in points:
        n=Vector((p.x*.40,1,0)).normalized()
        rows.append([p-n*d+Vector((0,0,dz)) for d,dz in [(.037,-.025),(.035,-.025),(.035,.025),(.037,.025)]])
    channel('S240 rear bumper seam return',rows)
    # A thin black weather strip fills the actual 4.5 mm reveal. The deeper
    # structural return remains visible behind it away from the grazing contour.
    channel('S240 rear reveal weather strip',[[p-Vector((0,d,0))+Vector((0,0,dz)) for d,dz in [(.002,-.002),(0,-.002),(0,.002),(.002,.002)]] for p in points])
    for side,sign in [('L',-1),('R',1)]:
        rows=[]
        for i in range(6):
            y=1.74+.66*i/5
            p=skin.ray_cast(Vector((sign*2,y,.608)),Vector((-sign,0,0)),3)[0]
            if p is None:continue
            p.z=.620-.022*(p.x/.90)**2
            rows.append([p-Vector((sign*d,0,0))+Vector((0,0,dz)) for d,dz in [(.037,-.025),(.035,-.025),(.035,.025),(.037,.025)]])
        channel('S240 rear quarter seam return '+side,rows)


    # Inner aperture liners are open-backed stamped strips, supported behind
    # the roof rail / posts / belt, ramping 10–70 mm behind the real seal.
    # Their open rear is hidden against that structure; it has no solid volume.
    from sedan_fairness import field
    for name in ['Windshield','Backlight','Hood outer','Trunk outer','Greenhouse_L','Greenhouse_R','Front molded fascia','Rear molded fascia','Front fender_L','Front fender_R','Rear quarter_L','Rear quarter_R','C divider_L','C divider_R']+[stem+'_'+side for side in ['L','R'] for stem in ['Front side glass','Rear side glass','Quarter glass']]:
        pane=bpy.data.objects[name];normal=field([pane]).nearest_normal
        loops=sorted(boundary_loops(pane),key=lambda points:(sum(p.y for p in points)/len(points),sum(p.z for p in points)/len(points)))
        if name in ['Hood outer','Trunk outer']:loops=[max(loops,key=lambda points:sum((p-q).length for p,q in zip(points,points[1:]+points[:1])))]
        for index,points in enumerate(loops):
            center=sum(points,Vector())/len(points);outside=[];inside=[]
            for i,p in enumerate(points):
                n=normal(p);t=points[(i+1)%len(points)]-points[i-1];out=t.cross(n).normalized()
                if name.startswith(('Front side glass','Rear side glass')):
                    if out.dot(p-center)<0:out.negate()
                    recess=.0056 if name.startswith('Front side glass') else .009
                    outside.append(p+out*.003-n*recess);inside.append(p-out*.012-n*recess)
                elif name=='Windshield':
                    if out.dot(p-center)<0:out.negate()
                    outside.append(p+out*.020-n*.025);inside.append(p-out*.030-n*.050)
                elif name.startswith('Greenhouse'):
                    outside.append(p+out*.016-n*.020);inside.append(p-out*.016-n*.020)
                elif name=='Trunk outer':
                    outside.append(p+out*.045-n*.075);inside.append(p-out*.045-n*.075)
                    for q in [outside[-1],inside[-1]]:
                        if q.y>2.18:q.z-=.030
                else:
                    if out.dot(p-center)<0:out.negate()
                    outside.append(p+out*.060-n*.020);inside.append(p-out*.030-n*.050)
            ob=G.loft('S240 inner aperture liner '+name+' '+str(index),[outside,inside],b.m['frame'],caps=False)
            ob['allow_boundary']=True;ob['construction']='Open-backed inner rail cover; no hidden back face'
            if name in ['Trunk outer','Backlight']:hinge_pockets(ob)
            if name.startswith(('Front molded','Front fender')):clip_end(ob,True)
            if name.startswith(('Rear molded','Rear quarter')):clip_end(ob,False)
            if name.startswith('Rear quarter'):clip_quarter(ob)
            if not ob.data.polygons:
                bpy.data.objects.remove(ob,do_unlink=True);continue
            parent=pane.parent if name.startswith(('Front side glass','Rear side glass')) else None
            b.add(ob,parent,category='interior')
    # Inner A-post hems bridge the cowl and door aperture at its leading edge.
    for side,sign in [('L',-1),('R',1)]:
        pane=bpy.data.objects['Front side glass_'+side]
        loop=max(boundary_loops(pane),key=len);rows=[]
        for z in [.905,.94,1.00,1.10,1.20,1.30,1.36]:
            hits=[]
            for a,c in zip(loop,loop[1:]+loop[:1]):
                if min(a.z,c.z)<=z<=max(a.z,c.z) and abs(c.z-a.z)>1e-8:hits.append(a+(c-a)*((z-a.z)/(c.z-a.z)))
            if not hits:continue
            p=min(hits,key=lambda q:q.y)
            rows.append([(sign*(abs(p.x)-d),p.y+dy,z) for d,dy in [(.037,-.036),(.035,-.036),(.035,.036),(.037,.036)]])
        channel('S240 inner A-post hem '+side,rows)
    for side,sign in [('L',-1),('R',1)]:
        from detail_helpers import box
        box(b,'S240 cowl corner reveal return '+side,(sign*.850,-1.050,.895),(.100,.044,.002),b.m['frame'],'interior',radius=0)
        hits=[skin.ray_cast(Vector((sign*2,S.DOOR_SPLIT+dy,.925)),Vector((-sign,0,0)),3)[0] for dy in [-.020,.020]]
        hits=[p for p in hits if p is not None and p.x*sign>.6]
        if not hits:raise ValueError('B-post return has no belt support')
        outer=min(abs(p.x) for p in hits)-.0018
        box(b,'S240 B-post belt pinch return '+side,(sign*(.770+.840)/2,S.DOOR_SPLIT,.919),
            (.840-.770,.0038,.012),b.m['frame'],'interior',radius=0)
        box(b,'S240 rear door belt return '+side,(sign*(.843+outer)/2,S.DOOR_SPLIT,.919),
            (outer-.843,.006,.012),b.m['frame'],'interior',bpy.data.objects['Door_R'+side],radius=0)
    # Concealed headliner rail crosses the chart seam above the rear doors.
    rows=[]
    for i in range(15):
        x=-.72+1.44*i/14;hits=[skin.ray_cast(Vector((x,y,2)),Vector((0,0,-1)),2)[0] for y in [.77,.91]]
        hits=[p for p in hits if p is not None and p.z>1.20]
        if not hits:continue
        z=min(p.z for p in hits)-.035;rows.append([(x,.77,z),(x,.91,z)])
    if len(rows)>1:
        ob=G.mesh('S240 inner rear roof rail cover',[p for row in rows for p in row],[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(rows)-1)],b.m['frame'])
        ob['allow_boundary']=True;b.add(ob,category='interior')
    # Split cut-cell loops share one manufactured quarter return in both
    # densities, so every game part has a corresponding bake source.
    for side in ['L','R']:
        prefix='S240 inner aperture liner Rear quarter_'+side+' '
        members=sorted([o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith(prefix)],key=lambda o:o.name)
        if len(members)>1:
            bpy.ops.object.select_all(action='DESELECT')
            for ob in members:ob.select_set(True)
            bpy.context.view_layer.objects.active=members[0];bpy.ops.object.join()
    fit_end_backings(b)


def boundary_loops(ob):
    """Every connected outer-skin boundary, with 3 mm hidden-land chord error."""
    roles=ob.data.attributes.get('sheet_role');limit=ob.get('lens_outer_faces');edges={}
    for face in ob.data.polygons:
        if roles and roles.data[face.index].value!=0:continue
        if limit is not None and face.index>=limit:continue
        for a,c in zip(face.vertices,list(face.vertices[1:])+[face.vertices[0]]):
            key=tuple(sorted((a,c)));edges[key]=edges.get(key,0)+1
    remaining={edge for edge,count in edges.items() if count==1};adj={}
    for a,c in remaining:adj.setdefault(a,[]).append(c);adj.setdefault(c,[]).append(a)
    result=[]
    while remaining:
        first,current=min(remaining);indices=[first];remaining.remove(tuple(sorted((first,current))))
        while current!=first:
            indices.append(current);following=next((i for i in sorted(adj[current]) if tuple(sorted((current,i))) in remaining),None)
            if following is None:raise ValueError(('Open manufactured outline',ob.name,current))
            remaining.remove(tuple(sorted((current,following))));current=following
        points=[ob.matrix_world@ob.data.vertices[i].co for i in indices]
        changed=True
        while changed and len(points)>8:
            changed=False
            for i,p in enumerate(points):
                a,c=points[i-1],points[(i+1)%len(points)];d=c-a;t=max(0,min(1,(p-a).dot(d)/max(d.length_squared,1e-15)))
                if (p-a-d*t).length<.003:points.pop(i);changed=True;break
        if sum((p-q).length for p,q in zip(points,points[1:]+points[:1]))>.020:result.append(points)
    return result


def hinge_pockets(ob):
    """Two real gooseneck slots in the rear opening's inner return."""
    polygons=[[ob.matrix_world@ob.data.vertices[i].co for i in f.vertices] for f in ob.data.polygons]
    for x in [-.480,.480]:
        planes=[(1,0,-(x-.022)),(-1,0,x+.022),(0,1,-1.82),(0,-1,2.18)];result=[]
        for polygon in polygons:
            for nx,ny,d in planes:
                inside=[];outside=[]
                for a,c in zip(polygon,polygon[1:]+polygon[:1]):
                    da=nx*a.x+ny*a.y+d;dc=nx*c.x+ny*c.y+d
                    (inside if da>=0 else outside).append(a)
                    if da*dc<0:
                        p=a+(c-a)*(da/(da-dc));inside.append(p);outside.append(p)
                if len(outside)>=3:result.append(outside)
                polygon=inside
                if len(polygon)<3:break
        polygons=result
    vertices=[];faces=[];inverse=ob.matrix_world.inverted()
    for polygon in polygons:
        start=len(vertices);vertices.extend(inverse@p for p in polygon);faces.append(tuple(range(start,len(vertices))))
    old=ob.data;mesh=bpy.data.meshes.new('Gooseneck clearance slots');mesh.from_pydata(vertices,[],faces);mesh.update()
    for material in old.materials:mesh.materials.append(material)
    ob.data=mesh
    if old.users==0:bpy.data.meshes.remove(old)
    ob['gooseneck_slot_width_m']=.044


def clip_end(ob,front):
    """End returns stop before the wheelhouse, leaving the tire envelope clear."""
    polygons=[]
    for face in ob.data.polygons:
        points=[ob.matrix_world@ob.data.vertices[i].co for i in face.vertices];clipped=[]
        for a,c in zip(points,points[1:]+points[:1]):
            da=(-2.03-a.y) if front else (a.y-2.03);dc=(-2.03-c.y) if front else (c.y-2.03)
            if da>=0:clipped.append(a)
            if da*dc<0:clipped.append(a+(c-a)*(da/(da-dc)))
        if len(clipped)>=3:polygons.append(clipped)
    old=ob.data;inverse=ob.matrix_world.inverted();vertices=[];faces=[]
    for points in polygons:
        start=len(vertices);vertices.extend(inverse@p for p in points);faces.append(tuple(range(start,len(vertices))))
    mesh=bpy.data.meshes.new('Stamped end-return land');mesh.from_pydata(vertices,[],faces);mesh.update()
    for material in old.materials:mesh.materials.append(material)
    ob.data=mesh
    if old.users==0:bpy.data.meshes.remove(old)


def clip_quarter(ob):
    """The fixed quarter return ends outside the opening lid's real split."""
    sign=-1 if ob.name.find('_L')>=0 else 1
    for vertex in ob.data.vertices:
        p=ob.matrix_world@vertex.co
        limit=.624
        if sign*p.x<limit:p.x=sign*limit;vertex.co=ob.matrix_world.inverted()@p


def clip_hinge_end(ob,hood):
    # A folded edge stops short of the hinge/cowl or backlight corner.
    old=ob.data;polygons=[]
    for face in old.polygons:
        points=[ob.matrix_world@old.vertices[i].co for i in face.vertices];clipped=[]
        for a,c in zip(points,points[1:]+points[:1]):
            da=(-1.18-a.y) if hood else (a.y-2.03);dc=(-1.18-c.y) if hood else (c.y-2.03)
            if da>=0:clipped.append(a)
            if da*dc<0:clipped.append(a+(c-a)*(da/(da-dc)))
        if len(clipped)>=3:polygons.append(clipped)
    inverse=ob.matrix_world.inverted();vertices=[];faces=[]
    for points in polygons:
        start=len(vertices);vertices.extend(inverse@p for p in points);faces.append(tuple(range(start,len(vertices))))
    mesh=bpy.data.meshes.new('Closure hem hinge clearance');mesh.from_pydata(vertices,[],faces);mesh.update()
    for material in old.materials:mesh.materials.append(material)
    ob.data=mesh
    if old.users==0:bpy.data.meshes.remove(old)


def fit_end_backings(b):
    """Keep concealed strips 3 mm inside the measured painted side profile.

    The open underside of the uncut die cannot certify this silhouette. Use
    supporting lines of the actual outer-fascia projection, including its chin.
    """
    def hull(points):
        points=sorted(set(points))
        def cross(a,c,d):return (c[0]-a[0])*(d[1]-a[1])-(c[1]-a[1])*(d[0]-a[0])
        lower=[];upper=[]
        for p in points:
            while len(lower)>1 and cross(lower[-2],lower[-1],p)<=1e-12:lower.pop()
            lower.append(p)
        for p in reversed(points):
            while len(upper)>1 and cross(upper[-2],upper[-1],p)<=1e-12:upper.pop()
            upper.append(p)
        return lower[:-1]+upper[:-1]
    for end,front in [('Front',True),('Rear',False)]:
        panel=bpy.data.objects[end+' molded fascia'];roles=panel.data.attributes['sheet_role']
        ids={i for face in panel.data.polygons if roles.data[face.index].value==0 for i in face.vertices}
        outline=hull([(p.y,p.z) for i in ids for p in [panel.matrix_world@panel.data.vertices[i].co]])
        planes=[]
        for a,c in zip(outline,outline[1:]+outline[:1]):
            normal=Vector((0,c[1]-a[1],a[0]-c[0])).normalized();planes.append((Vector((0,*a)),normal))
        for ob in list(bpy.context.scene.objects):
            if not ob.name.startswith('S240 inner aperture liner '+end+' molded fascia'):continue
            inverse=ob.matrix_world.inverted();moved=0;minimum=float('inf')
            for vertex in ob.data.vertices:
                p=ob.matrix_world@vertex.co
                if p.z>.66:continue
                start=p.copy()
                for iteration in range(40):
                    worst=0.
                    for origin,n in planes:
                        excess=(p-origin).dot(n)+.003;worst=max(worst,excess)
                        if excess>0:p-=n*(excess+1e-7)
                    if worst<1e-7:break
                depth=min(-(p-origin).dot(n) for origin,n in planes);minimum=min(minimum,depth)
                if depth<.00299:raise ValueError(('End backing outside painted profile',ob.name,depth))
                vertex.co=inverse@p;moved+=(p-start).length>1e-7
            ob.data.update()
            if not math.isfinite(minimum):continue
            ob['measured_side_profile_setback_min_m']=minimum
            print('S240_END_BACKING_FIT',ob.name,moved,minimum,flush=True)
