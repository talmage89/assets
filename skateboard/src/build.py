"""Deterministic original skateboard form checkpoint. No downloaded asset input."""
import argparse,json,math,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
import bpy,bmesh
from mathutils import Vector,Matrix
from kit import model as G
from spec import spec,halfwidth,height,kick

def material(name,color,metal=0,rough=.5):
    m=bpy.data.materials.new(name);m.use_nodes=True
    p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    m.diffuse_color=(*color,1);return m

def tag(o,part,owner):
    G.attach(o,owner,asset_set='Skateboard');o['part']=part
    return o

def solidify_cast(parts,name,target):
    # Authored volumes are voxel-fused; no profile-extrusion casting shortcuts.
    for o in parts:G.apply(o)
    bpy.ops.object.select_all(action='DESELECT')
    for o in parts:o.select_set(True)
    bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();o=parts[0];o.name=name
    m=o.modifiers.new('Cast continuous rounded union','REMESH');m.mode='VOXEL';m.voxel_size=.00065;m.use_smooth_shade=True;G.apply(o)
    m=o.modifiers.new('Casting fillets','SMOOTH');m.factor=.65;m.iterations=2;G.apply(o)
    high=o.copy();high.data=o.data.copy();high.name=name+'__sculpt';bpy.context.collection.objects.link(high)
    high.hide_render=True;high.hide_set(True);high['source_only']=True;o['dense_source']=high.name
    m=o.modifiers.new('Silhouette preserving game reduction','DECIMATE');m.ratio=min(1,target/max(1,len(o.data.polygons)*2));G.apply(o)
    G.smooth(o,65)
    return o

def cast_cut(o,cutter):
    """Carry machined bores into the retained dense sculpt as well as game mesh."""
    high=bpy.data.objects[o['dense_source']];copy=cutter.copy();copy.data=cutter.data.copy();bpy.context.collection.objects.link(copy)
    for target,tool in ((o,cutter),(high,copy)):
        target.hide_set(False);m=target.modifiers.new('Machined bore','BOOLEAN');m.object=tool;m.operation='DIFFERENCE';m.solver='MANIFOLD';G.apply(target);bpy.data.objects.remove(tool,do_unlink=True)
    high.hide_set(True)
    return o

def cast_normals(o):
    """Weld reduced boolean seams; preserve machined face boundaries in normals."""
    bm=bmesh.new();bm.from_mesh(o.data)
    bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=1e-6)
    bmesh.ops.dissolve_degenerate(bm,edges=bm.edges,dist=1e-8)
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(o.data);bm.free()
    dense=bpy.data.objects[o['dense_source']]
    bm=bmesh.new();bm.from_mesh(dense.data);bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=bm.edges,dist=1e-8);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(dense.data);bm.free()
    G.smooth(dense,65);G.smooth(o,65)
    m=o.modifiers.new('Area-weighted casting normals','WEIGHTED_NORMAL');m.keep_sharp=True;m.weight=30
    G.apply(o)
    return o

def ellipsoid(name,c,sz,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=c)
    o=bpy.context.object;o.name=name;o.scale=sz;o.data.materials.append(mat)
    return o

def deform_deck(s,mat,plies,grip):
    # A single closed pressed shell. XY offset rings form a full half-gauge
    # roundover; veneer boundaries follow that roundover rather than stripes
    # painted onto a square edge. No internal duplicate ply faces.
    ys=sorted(set([s.nose_end,s.tail_end,-.20,0,.20,
        *[q*v for q in (-1,1) for v in (s.plate_y+.018,s.plate_y+.033,s.plate_y+.048,s.plate_y+.063,s.plate_y+.078)],
        *[s.nose_end+.124*(1-math.cos(math.pi/2*i/16)) for i in range(1,17)],
        *[s.tail_end-.112*(1-math.cos(math.pi/2*i/16)) for i in range(1,17)]]))
    contour=[Vector((-halfwidth(s,y),y)) for y in ys]+[Vector((halfwidth(s,y),y)) for y in reversed(ys[1:-1])]
    inward=[]
    for i,p in enumerate(contour):
        tangent=(contour[(i+1)%len(contour)]-contour[i-1]).normalized()
        inward.append(Vector((tangent.y,-tangent.x)))
    vs=[];faces=[];slots=[];rings=[];R=s.thickness/2
    levels=[s.thickness*i/7 for i in range(8)]+[s.thickness+.00055]
    for z in levels:
        inset=R-math.sqrt(max(0,R*R-(min(s.thickness,z)-R)**2))
        if z>s.thickness:inset+=.0007
        ring=[]
        for p,n in zip(contour,inward):
            q=p+n*inset;ring.append(len(vs));vs.append((q.x,q.y,height(s,q.x,q.y)+z))
        rings.append(ring)
    for j in range(len(rings)-1):
        for i in range(len(contour)):
            k=(i+1)%len(contour);faces.append((rings[j][i],rings[j][k],rings[j+1][k],rings[j+1][i]));slots.append(1 if j==7 else 2+j)
    # Enough cross-section chords for continuous concave at a held distance.
    us=[-1,-.88,-.70,-.48,-.24,0,.24,.48,.70,.88,1]
    for ring,ma,z in ((rings[0],0,0),(rings[-1],1,levels[-1])):
        rows=[]
        for j,y in enumerate(ys):
            li=j;ri=0 if j==0 else (len(ys)-1 if j==len(ys)-1 else len(contour)-j)
            if j in (0,len(ys)-1):rows.append([ring[j]]);continue
            left=Vector(vs[ring[li]]);right=Vector(vs[ring[ri]]);row=[]
            for k,u in enumerate(us):
                if k==0:row.append(ring[li])
                elif k==len(us)-1:row.append(ring[ri])
                else:
                    p=left.lerp(right,(u+1)/2);row.append(len(vs));vs.append((p.x,p.y,height(s,p.x,p.y)+z))
            rows.append(row)
        for a,b in zip(rows,rows[1:]):
            fs=([(a[0],b[k],b[k+1]) for k in range(len(b)-1)] if len(a)==1 else
                [(a[k],b[0],a[k+1]) for k in range(len(a)-1)] if len(b)==1 else
                [(a[k],b[k],b[k+1],a[k+1]) for k in range(len(a)-1)])
            faces.extend(fs);slots.extend([ma]*len(fs))
    o=G.mesh('Deck / seven ply shell and filed grip',vs,faces,mat)
    for m in [grip,*plies]:o.data.materials.append(m)
    for f,mi in zip(o.data.polygons,slots):f.material_index=mi
    G.smooth(o,65)
    return o

def allen_high(name,x,y,z,mat):
    """Closed countersunk head: round 12-gon perimeter, real six-sided drive.
    Explicit ring transition avoids boolean slivers and wastes no hidden cap.
    """
    vertices=[]
    for n,r,zz in [(12,.0022,z-.0017),(12,.0043,z+.0007),(6,.00145,z+.0007),(6,.00145,z-.0007)]:
        vertices.extend([(x+r*math.cos(math.tau*i/n),y+r*math.sin(math.tau*i/n),zz) for i in range(n)])
    faces=[tuple(reversed(range(12))),tuple(range(30,36))]
    for i in range(12):faces.append((i,(i+1)%12,(i+1)%12+12,i+12))
    for k in range(6):
        j=(k+1)%6;i=12+2*k;mid=12+(2*k+1)%12;end=12+(2*k+2)%12
        faces.extend([(i,mid,24+k),(mid,end,24+j,24+k),(24+k,24+j,30+j,30+k)])
    return G.mesh(name,vertices,faces,mat)

def allen_head(name,x,y,z,mat):
    # Twelve-sided visible head, six-sided buried cone, real six-sided drive.
    # 56 triangles: keep the mouth shadow and spend no sides under the grip.
    vs=[]
    for count,radius,zz in ((6,.0022,z-.0017),(12,.0043,z+.0007),(6,.00145,z+.0007),(6,.00145,z-.0007)):
        vs.extend((x+radius*math.cos(math.tau*i/count),y+radius*math.sin(math.tau*i/count),zz) for i in range(count))
    fs=[tuple(reversed(range(6))),tuple(range(24,30))]
    for k in range(6):
        j=(k+1)%6;a=6+2*k;m=6+(2*k+1)%12;b=6+(2*k+2)%12
        fs.extend([(k,a,m),(k,m,b,j),(a,m,18+k),(m,b,18+j,18+k),(18+k,18+j,24+j,24+k)])
    return G.mesh(name,vs,fs,mat)

def bored_ring(name,at,axis,profile,mat,n=20):
    o=G.lathe(name,profile,mat,n,closed=True)
    o.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler();o.location=at
    return o

def ring(name,at,axis,ro,ri,depth,mat,n=20):
    return bored_ring(name,at,axis,[(0,ri),(0,ro),(depth,ro),(depth,ri)],mat,n)

def annulus(name,at,axis,ro,ri,mat,n=12):
    o=G.mesh(name,[(r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),0) for r in (ri,ro) for i in range(n)],[(i+n,(i+1)%n+n,(i+1)%n,i) for i in range(n)],mat)
    o.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler();o.location=at;return o

def nut(name,at,axis,r,depth,bore,mat,nylon,owner,part):
    o=bored_ring(name,at,axis,[(0,r),(depth,r),(depth,bore)],mat,6)
    # Remove the buried conical return; visible wrench flats and annular
    # face remain. Inner threading transfers through the normal map.
    bm=bmesh.new();bm.from_mesh(o.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=list(bm.faces)[12:],context='FACES_ONLY');bm.to_mesh(o.data);bm.free()
    tag(o,part,owner)
    q=Vector(at)+Vector(axis)*(depth-.0005)
    internal=annulus(name+' nylon insert',q,axis,r*.73,bore,nylon,6)
    tag(internal,part,owner);del internal['asset_set'];internal['source_only']=True;internal.hide_render=True;internal.hide_set(True)
    return o

def exposed_axle(name,s,ay,az,mat):
    """Twelve-sided exposed steel ends; buried center/caps stay in high source."""
    vs=[];fs=[];n=12
    for side in (-1,1):
        first=len(vs)
        for x in (side*(s.hanger_width/2-.001),side*s.axle_width/2):
            vs.extend((x,ay+.004*math.cos(math.tau*i/n),az+.004*math.sin(math.tau*i/n)) for i in range(n))
        c=len(vs);vs.append((side*s.axle_width/2,ay,az))
        for i in range(n):
            j=(i+1)%n
            face=(first+i,first+j,first+n+j,first+n+i)
            cap=(first+n+i,first+n+j,c)
            fs.append(face if side>0 else tuple(reversed(face)));fs.append(cap if side>0 else tuple(reversed(cap)))
    return G.smooth(G.mesh(name,vs,fs,mat),65)

def build(s):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mat=material('Checkpoint bottom / red oxide',(.23,.024,.012),0,.47)
    grip=material('Checkpoint grip / carbon',(.012,.013,.012),0,.86)
    plies=[material('Maple veneer '+str(i+1),(.43+i*.006,.28+i*.004,.115+i*.002) if i not in (2,4) else (.32,.21,.095),0,.58) for i in range(7)]
    al=material('Checkpoint cast aluminum',(.48,.50,.52),1,.44)
    steel=material('Checkpoint zinc steel',(.31,.33,.35),1,.28)
    black=material('Checkpoint black hardware',(.018,.02,.021),.6,.36)
    ure=material('Checkpoint urethane / amber',(.24,.080,.018),0,.43)
    rubber=material('Checkpoint rubber',(.009,.011,.012),0,.73)
    wheelmat=material('Checkpoint wheel / ivory urethane',(.55,.49,.34),0,.49)
    shield=material('Checkpoint bearing shield',(.035,.075,.085),.20,.43)
    root=G.pivot('Skateboard',(0,0,0));root['static_root']=True;root['seed']=s.seed;root['age_state']=s.state;root['checkpoint']='form only; no baked texture'
    deck=deform_deck(s,mat,plies,grip)
    # Actual through bores with conical countersinks. Do not stop at bolt discs.
    for sign in (-1,1):
        cy=sign*s.plate_y
        for x in (-s.pitch_x/2,s.pitch_x/2):
            for y in (cy-s.pitch_y/2,cy+s.pitch_y/2):
                z=height(s,x,y)+s.thickness
                cutter=G.lathe('Deck bore tool',[(z-.025,.0025),(z-.0012,.0025),(z+.00055,.00445),(z+.015,.00445)],None,12)
                cutter.location.x=x;cutter.location.y=y
                # Exact in this Blender build reverses a curved closed shell
                # and adds the cutter. Manifold retains positive volume and
                # open through-holes; independent rays verify all eight.
                mod=deck.modifiers.new('Drilled countersink','BOOLEAN');mod.object=cutter;mod.operation='DIFFERENCE';mod.solver='MANIFOLD';G.apply(deck);bpy.data.objects.remove(cutter,do_unlink=True)
                # Head cone fills seat; socket is a real hex recess.
                head=allen_head('Flush Allen bolt head',x,y,z,black);tag(head,'mount_hardware',root)
                shank=G.cylinder('10-32 mounting bolt',(x,y,z+.0007-.0254),(x,y,s.underside-s.riser-.009),.002413,black,4);tag(shank,'mount_hardware',root)
                nut('Mount locknut',(x,y,s.underside-s.riser-.006),(0,0,-1),.0055,.0048,.002413,steel,rubber,root,'mount_hardware')
    G.smooth(deck,65)
    for edge in deck.data.edges:
        p0,p1=[deck.data.vertices[i].co for i in edge.vertices]
        if any(math.hypot((p0.x+p1.x)/2-x,(p0.y+p1.y)/2-y)<.006 for x in (-s.pitch_x/2,s.pitch_x/2) for q in (-1,1) for y in (q*s.plate_y-s.pitch_y/2,q*s.plate_y+s.pitch_y/2)):edge.use_edge_sharp=True
    tag(deck,'deck',root)
    for sign,label in ((-1,'Front'),(1,'Rear')):
        cy=sign*s.plate_y;az=s.axle_z;ay=sign*s.axle_y;z=s.underside-s.riser
        # Cast baseplate, kingpin tower and pivot pedestal fuse into ONE curved casting.
        plate=G.box('Plate seed',(0,cy,z-.0025),(.058,.080,.005),al,.003,3)
        # Kingpin top is inward; its shaft inclines toward the axle as it
        # travels down to the road-side nut (traditional street truck).
        kaxis=Vector((0,sign*math.sin(math.radians(20)),-math.cos(math.radians(20))))
        kbase=Vector((0,cy-sign*.012,z-.0035))
        # Pivot cup center to bushing yoke center defines virtual steering axis.
        pc=Vector((0,cy+sign*.025,z-.009))
        yc=pc+Vector((0,-sign*.040,-.029))
        # Point kingpin at yoke; adjust its base using that physically seated stack.
        kbase=yc-kaxis*.018
        tower=G.loft('Flared cast pedestal seed', [[(x,y+cy0,zz) for x,y in G.rounded_rectangle(w,h,r,5)] for cy0,zz,w,h,r in [(cy,z-.003,.038,.060,.006),(cy,z-.007,.033,.052,.006),(kbase.y,z-.018,.025,.032,.004),(kbase.y,z-.024,.022,.027,.004)]],al)
        ped=ellipsoid('Pivot socket boss seed',pc,(.009,.010,.009),al)
        base=solidify_cast([plate,tower,ped],label+' cast baseplate',730)
        for sx in (-1,1):
            pocket=G.box('Cast side pocket tool',(sx*.019,cy,z-.012),(.010,.035,.012),None,.003,3)
            cast_cut(base,pocket)
        # Four real mounting bores, plus blind pivot cup pocket.
        for x in (-s.pitch_x/2,s.pitch_x/2):
            for y in (cy-s.pitch_y/2,cy+s.pitch_y/2):
                cast_cut(base,G.cylinder('Plate bore tool',(x,y,z-.012),(x,y,z+.012),.0027,None,12))
        # Pivot stems aim into a rounded blind rubber cup in the plate pedestal.
        steer=(yc-pc).normalized()
        cast_cut(base,G.cylinder('Cup pocket tool',pc-steer*.007,pc+steer*.023,.0065,None,16))
        for ob in (base,bpy.data.objects[base['dense_source']]):
            for v in ob.data.vertices:
                world=ob.matrix_world@v.co
                if world.z>z-.0012:world.z=z
                v.co=ob.matrix_world.inverted()@world
        # Cut real cylindrical wrench/nut reliefs. Projecting nearby vertices
        # onto the bearing plane stretched the boss into thin sliver faces.
        for bx in (-s.pitch_x/2,s.pitch_x/2):
            for by in (cy-s.pitch_y/2,cy+s.pitch_y/2):
                cast_cut(base,G.cylinder('Machined nut land tool',(bx,by,z-.055),(bx,by,z-.006),.008,None,16))
        m=base.modifiers.new('Post-bore casting reduction','DECIMATE');m.ratio=.35;G.apply(base);G.smooth(base,65)
        cast_normals(base)
        tag(base,'baseplates',root)
        tag(ring(label+' pivot cup',pc-steer*.005,steer,.0065,.0047,.009,rubber,16),'truck_hardware',root)
        tag(G.cylinder(label+' steel kingpin',kbase-kaxis*.003,kbase+kaxis*.044,.0047625,steel,14),'truck_hardware',root)
        # Fixed lower bushing; moving upper stack is only a visual flex proxy.
        tag(bored_ring(label+' barrel bushing',kbase+kaxis*.003,kaxis,[(0,.0049),(0,.0114),(.001,.012),(.0117,.012),(.0127,.0114),(.0127,.0049)],ure,16),'bushings',root)
        tag(bored_ring(label+' bottom cupped washer',kbase+kaxis*.0015,kaxis,[(0,.0049),(0,.0123),(.0025,.0131),(.0015,.0049)],steel,12),'truck_hardware',root)
        pivot=G.pivot('Hanger_'+label,pc);pivot.parent=root
        pivot.rotation_euler=steer.to_track_quat('Z','Y').to_euler();pivot['pivot_axis']='Z';pivot['range_degrees']=[-s.lean_limit,s.lean_limit];pivot['axis_world']=list(steer);pivot['pivot_cup_m']=list(pc);pivot['yoke_center_m']=list(yc)
        # Axle tube swells at the center. Curved wings flow toward the yoke.
        hw=s.hanger_width/2
        barrel=G.lathe('Axle barrel seed',[(-hw,0),(-hw,.0066),(-hw+.005,.008),(-.027,.010),(0,.0108),(.027,.010),(hw-.005,.008),(hw,.0066),(hw,0)],al,32,axis='X',center=(ay,az))
        loops=[]
        for frac,ry,rz,blend in [(-1,.0068,.0065,0),(-.82,.008,.007,0),(-.48,.010,.008,.35),(-.22,.013,.007,.85),(0,.016,.007,1),(.22,.013,.007,.85),(.48,.010,.008,.35),(.82,.008,.007,0),(1,.0068,.0065,0)]:
            cy0=ay+(yc.y-ay)*blend;cz0=az+(yc.z-az)*blend
            loops.append([(frac*hw,cy0+ry*math.cos(a),cz0+rz*math.sin(a)) for a in [math.tau*i/24 for i in range(24)]])
        pieces=[barrel,G.loft('Swept cast wing web seed',loops,al)]
        # The outer face is a continuous triangular cast web from the axle
        # housing to the pivot nose. Oval sections bow across both Y and Z;
        # this is a compound casting surface, not an extruded side cutout.
        web=[]
        for fraction in (-1,-.94,-.72,-.46,-.22,0,.22,.46,.72,.94,1):
            taper=max(0,1-abs(fraction))
            upper=az+.0065+(pc.z-az-.018)*taper
            lower=az-.0065
            centerz=(upper+lower)/2
            centery=ay+(pc.y+steer.y*.018-ay)*taper
            radiusy=.0026+.0010*taper
            section=G.rounded_rectangle(2*radiusy,upper-lower,min(.0015,radiusy*.6),4)
            web.append([(fraction*hw,centery+u+.08*v,centerz+v) for u,v in section])
        pieces.append(G.loft('Triangular drafted outer hanger web',web,al))
        seat=bored_ring('Drafted annular kingpin seat',yc-kaxis*.0039,kaxis,[(0,.0065),(0,.0175),(.001,.018),(.0068,.018),(.0078,.0175),(.0078,.0065)],al,48);pieces.append(seat)
        arm=G.lathe('Tapered cast pivot arm seed',[(0,0),(0,.0045),(.010,.0045),(.025,.0055),(.040,.0065),((yc-pc).length,.0065),((yc-pc).length,0)],al,24);arm.location=pc-steer*.003;arm.rotation_euler=steer.to_track_quat('Z','Y').to_euler();pieces.append(arm)
        hanger=solidify_cast(pieces,label+' sculpted hanger',950)
        cast_cut(hanger,G.cylinder('Open kingpin yoke tool',yc-kaxis*.05,yc+kaxis*.05,.0065,None,16))
        # Counterbored bushing seats leave a 7.8 mm annular web. The cast
        # shoulders flare away from the kingpin hardware's steering envelope.
        for direction,start,radius in [(1,.0055,.0123),(-1,.0023,.0124)]:
            tool=G.lathe('Bushing seat and hardware relief',[(0,0),(0,radius),(.020,.016),(.050,.022),(.050,0)],None,20)
            tool.location=yc+kaxis*direction*start;tool.rotation_euler=(kaxis*direction).to_track_quat('Z','Y').to_euler();cast_cut(hanger,tool)
        m=hanger.modifiers.new('Post-seat casting reduction','DECIMATE');m.ratio=.50;G.apply(hanger);G.smooth(hanger,65)
        # Solid ring yoke carries bushings around its OPEN center, not through a block.
        # Cast ring is allowed to meet central barrel on its far side.
        cast_normals(hanger)
        tag(hanger,'hangers',pivot)
        tag(exposed_axle(label+' continuous axle',s,ay,az,steel),'axles',pivot)
        upper=kbase+kaxis*.0235
        tag(bored_ring(label+' cone bushing',upper,kaxis,[(0,.0049),(0,.0118),(.0102,.0088),(.0102,.0049)],ure,16),'bushings',root)
        tag(bored_ring(label+' top cupped washer',upper+kaxis*.0102,kaxis,[(0,.0049),(-.0008,.0109),(.0008,.0112),(.0015,.0049)],steel,12),'truck_hardware',root)
        nut(label+' kingpin locknut',upper+kaxis*.0117,kaxis,.0083,.0065,.00476,steel,rubber,root,'truck_hardware')
        if s.riser:
            pad=G.profile(label+' riser pad',[(x,y+cy) for x,y in G.rounded_rectangle(.059,.081,.003,2)],s.underside-s.riser,s.underside,rubber,axis='Z')
            for x in (-s.pitch_x/2,s.pitch_x/2):
                for y in (cy-s.pitch_y/2,cy+s.pitch_y/2):G.boolean(pad,G.cylinder('Riser bore',(x,y,z-.002),(x,y,z+.01),.0029,None,6))
            # Retain the solid pad in the source. The game keeps its exposed
            # perimeter; top/bottom and bolt bores are buried in the clamped stack.
            G.apply(pad);solid=pad.copy();solid.data=pad.data.copy();solid.name=label+' riser pad__solid';bpy.context.collection.objects.link(solid)
            solid['source_only']=True;solid.hide_render=True;solid.hide_set(True);pad['dense_source']=solid.name
            bm=bmesh.new();bm.from_mesh(pad.data)
            hidden=[f for f in bm.faces if abs(f.normal.z)>.2 or (abs(f.calc_center_median().x)<.026 and abs(f.calc_center_median().y-cy)<.037)]
            bmesh.ops.delete(bm,geom=hidden,context='FACES_ONLY');bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bm.to_mesh(pad.data);bm.free()
            tag(pad,'riser',root)
        for side,side_label in ((-1,'L'),(1,'R')):
            # Inner ring faces: hanger exit + .5 mm speed ring; 7 + 10 + 7 mm.
            centerx=side*(hw+.0005+.012)
            wr=G.pivot('Wheel_'+label+'_'+side_label,(centerx,ay,az),'X',(0,360));wr['continuous']=True
            bpy.context.view_layer.update();mw=wr.matrix_world.copy();wr.parent=pivot;wr.matrix_world=mw
            r=s.wheel_diameter/2;w=s.wheel_width/2;patch=s.contact_width/2
            profile=[(-w,.011),(-w,.020),(-w+.0016,r-.0022),(-patch,r),(patch,r),(w-.0016,r-.0022),(w,.020),(w,.011)]
            wheel=G.lathe('Urethane '+label+' '+side_label,profile,wheelmat,64,axis='X',center=(ay,az),closed=True);wheel.location.x=centerx
            G.smooth(wheel,80)
            tag(wheel,'wheels',wr)
            for bs in (-1,1):
                at=Vector((centerx+bs*.005,ay,az));axis=(bs,0,0)
                # Only the shield-facing race and inner bore can be seen.
                # Omit the race's buried outer cylinder and back face.
                race=annulus('608 '+label+side_label+str(bs)+' bearing races',at+Vector(axis)*.007,axis,.011,.004,steel,20)
                tag(race,'bearings',wr)
                tag(annulus('608 '+label+side_label+str(bs)+' shield',at+Vector(axis)*.00705,axis,.0096,.0069,shield,20),'bearings',wr)
            # The 10 mm tubular spacer is wholly enclosed by the axle/bearings
            # and wheel core. Its hidden faces are omitted from the game mesh.
            internal=ring('Bearing spacer '+label+side_label,(centerx-.005,ay,az),(1,0,0),.0055,.004,.010,steel,12)
            tag(internal,'spacers',pivot);del internal['asset_set'];internal['source_only']=True;internal.hide_render=True;internal.hide_set(True)
            internal=annulus('Buried outboard speed ring '+label+side_label,(side*(hw+.025),ay,az),(side,0,0),.006,.004,steel,12)
            tag(internal,'spacers',pivot);del internal['asset_set'];internal['source_only']=True;internal.hide_render=True;internal.hide_set(True)
            # The outboard speed ring is completely covered by the nut.
            for distance in (hw,):
                tag(annulus('Axle speed ring '+label+side_label,(side*(distance+.0005),ay,az),(side,0,0),.006,.004,steel,10),'spacers',pivot)
            nut('Axle nut '+label+side_label,(side*(hw+.025),ay,az),(side,0,0),.0073,.0058,.004,steel,rubber,pivot,'axle_nuts')
    if s.state!='new':
        # Tail abrasion compresses the actual shell towards its top surface.
        age=.42 if s.state=='season' else 1.0
        for v in deck.data.vertices:
            y=v.co.y;u=max(0,min(1,(y-(s.tail_end-.042))/.042));u=u*u*(3-2*u)
            top=height(s,v.co.x,y)+s.thickness
            if v.co.z<top:v.co.z=top-(top-v.co.z)*(1-.62*age*u)
        # Impact chips at the rear kick and opposite nose rail. Upper veneers
        # lose more width; the lower bands remain visible under the fracture.
        for v in deck.data.vertices:
            x,y,z0=v.co;h=height(s,x,y);tier=max(0,min(1,((z0-h)/s.thickness-.30)/.70))
            for side,cy0,span in ((1,s.tail_end-.024,.009),(-1,s.nose_end+.035,.008)):
                band=max(0,1-abs(y-cy0)/span)
                edge=max(0,min(1,(side*x/max(.001,halfwidth(s,y))-.80)/.20))
                v.co.x-=side*.0040*age*band*edge*tier
        if s.state=='beat':
            for k,(cx,yy) in enumerate(((-.014,s.tail_end-.013),(.011,s.tail_end-.009))):
                loops=[]
                for y0,width,drop in ((yy-.012,.014,0),(yy-.004,.013,-.0007),(yy+.002,.008,-.0015)):
                    u=max(0,min(1,(y0-(s.tail_end-.042))/.042));u=u*u*(3-2*u)
                    z0=height(s,cx,y0)+s.thickness-s.thickness*(1-.62*u)+drop
                    loops.append([(cx-width/2,y0,z0),(cx+width/2,y0,z0),(cx+width/2,y0,z0+.00045),(cx-width/2,y0,z0+.00045)])
                flap=G.loft('Tail separated maple splinter '+str(k+1),loops,plies[k]);tag(flap,'delamination',root)
        # Coning is axial material loss from repeated heel/toe turning. Keep
        # one tread edge at the original radius so the wheel remains grounded.
        for o in bpy.context.scene.objects:
            if o.get('part')!='wheels':continue
            for v in o.data.vertices:
                axial=v.co.x;rad=math.hypot(v.co.y,v.co.z)
                if rad>.019:
                    loss=age*.0012*max(0,min(1,(axial+s.contact_width/2)/s.contact_width))
                    v.co.y*=1-loss/rad;v.co.z*=1-loss/rad
            if s.state=='beat' and o.name=='Urethane Front L':
                # One locked-wheel skid leaves an actual planar 1.4 mm flat,
                # parked at 135 degrees so the board still rests on round tread.
                direction=Vector((0,-math.sqrt(.5),math.sqrt(.5)))
                plane=s.wheel_diameter/2-.0014
                for v in o.data.vertices:
                    cut=v.co.dot(direction)-plane
                    if cut>0:v.co-=direction*cut
                o['flat_spot_depth_m']=.0014
                o['flat_spot_normal_local']=list(direction)
    for name,xyz,kind,rot in [('Foot_Front',(0,-.12,s.underside+s.thickness+.00055),'foot',(0,0,90)),('Foot_Rear',(0,.255,height(s,0,.255)+s.thickness+.00055),'foot',(0,0,90)),('Hand_Carry',(-halfwidth(s,0),0,height(s,-halfwidth(s,0),0)+s.thickness/2),'hand',(0,90,0)),('Rest_Ground',(0,0,0),'ground',(0,0,0))]:
        o=G.pivot('Socket_'+name,xyz);o.parent=root;o['socket_kind']=kind;o.rotation_euler=tuple(math.radians(v) for v in rot)
    # A real wall-rest alignment frame, derived from all evaluated surfaces.
    # Align this socket to a wall frame rotated -90° about X, at its recorded
    # height. The board then leans 78° with both floor and wall contact.
    bpy.context.view_layer.update();tilt=Matrix.Rotation(math.radians(-78),4,'X')
    posed=[tilt@o.matrix_world@v.co for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')=='Skateboard' for v in o.data.vertices]
    ground_z=min(p.z for p in posed);wall_y=min(p.y for p in posed);hits=[p for p in posed if abs(p.y-wall_y)<1e-6];contact_z=sum(p.z for p in hits)/len(hits)
    socket=G.pivot('Socket_Rest_Wall',tilt.inverted()@Vector((0,wall_y,contact_z)));socket.parent=root;socket.rotation_euler.x=math.radians(-12);socket['socket_kind']='wall';socket['wall_alignment_height_m']=contact_z-ground_z;socket['rest_root_rotation_degrees']=[-78,0,0]
    return root

def main():
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=0);p.add_argument('--state',choices=['new','season','beat'],default='season');p.add_argument('--out',default='build/skateboard.blend');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);s=spec(a.seed,a.state)
    build(s);out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True)
    # Keep dense sources in a hidden collection, never in the game export.
    sources=bpy.data.collections.new('SOURCE / retained manufacturing detail');bpy.context.scene.collection.children.link(sources)
    for o in list(bpy.context.scene.objects):
        if o.get('source_only'):
            for c in list(o.users_collection):c.objects.unlink(o)
            sources.objects.link(o)
    report={'spec':s.dict(),'parts':{},'objects':{},'scope':'Form checkpoint; quick material palette; no UV/bake claim'}
    for o in bpy.context.scene.objects:
        if o.type!='MESH' or o.get('source_only'):continue
        G.apply(o);o.data.calc_loop_triangles();n=len(o.data.loop_triangles);part=o['part'];report['parts'][part]=report['parts'].get(part,0)+n;report['objects'][o.name]=n
    report['triangles']=sum(report['parts'].values())
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    bpy.ops.object.select_all(action='DESELECT')
    for o in bpy.context.scene.objects:
        if not o.get('source_only'):o.select_set(True)
    glb=out.with_suffix('.glb')
    bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,export_extras=True,export_apply=True,export_yup=True,export_animations=False)
    report['glb_bytes']=glb.stat().st_size;report['glb_sha256']=hashlib.sha256(glb.read_bytes()).hexdigest()
    out.with_suffix('.json').write_text(json.dumps(report,indent=2));print('CHECKPOINT',report['triangles'],report['parts'])
if __name__=='__main__':main()
