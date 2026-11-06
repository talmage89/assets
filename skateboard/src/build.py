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
    m=o.modifiers.new('Cast continuous rounded union','REMESH');m.mode='VOXEL';m.voxel_size=.00105;m.use_smooth_shade=True;G.apply(o)
    m=o.modifiers.new('Casting fillets','SMOOTH');m.factor=.65;m.iterations=5;G.apply(o)
    high=o.copy();high.data=o.data.copy();high.name=name+'__sculpt';bpy.context.collection.objects.link(high)
    high.hide_render=True;high.hide_set(True);high['source_only']=True;o['dense_source']=high.name
    m=o.modifiers.new('Silhouette preserving game reduction','DECIMATE');m.ratio=min(1,target/max(1,len(o.data.polygons)*2));G.apply(o)
    G.smooth(o,65)
    return o

def cast_cut(o,cutter):
    """Carry machined bores into the retained dense sculpt as well as game mesh."""
    high=bpy.data.objects[o['dense_source']];copy=cutter.copy();copy.data=cutter.data.copy();bpy.context.collection.objects.link(copy)
    G.boolean(o,cutter)
    high.hide_set(False);G.boolean(high,copy);high.hide_set(True)
    return o

def cast_normals(o):
    """Weld reduced boolean seams; preserve machined face boundaries in normals."""
    bm=bmesh.new();bm.from_mesh(o.data)
    bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=1e-6)
    bmesh.ops.dissolve_degenerate(bm,edges=bm.edges,dist=1e-8)
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(o.data);bm.free()
    dense=bpy.data.objects[o['dense_source']]
    bm=bmesh.new();bm.from_mesh(dense.data);bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=bm.edges,dist=1e-8);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(dense.data);bm.free()
    G.smooth(dense,32);G.smooth(o,32)
    m=o.modifiers.new('Area-weighted casting normals','WEIGHTED_NORMAL');m.keep_sharp=True;m.weight=30
    G.apply(o)
    return o

def ellipsoid(name,c,sz,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=c)
    o=bpy.context.object;o.name=name;o.scale=sz;o.data.materials.append(mat)
    return o

def deform_deck(s,mat,plies,grip):
    # Ends are welded poles, not coincident collapsed rows. Broad surface is a
    # cross-section grid; rail bands are the seven visible veneers only.
    ys=sorted(set([s.nose_end,s.tail_end,*[s.nose_end+.124+(s.tail_end-.112-s.nose_end-.124)*i/14 for i in range(15)],
                   *[s.nose_end+.124*(1-math.cos(math.pi/2*i/10)) for i in range(1,11)],
                   *[s.tail_end-.112*(1-math.cos(math.pi/2*i/10)) for i in range(1,11)],
                   -s.plate_y-.04,-s.plate_y+.04,s.plate_y-.04,s.plate_y+.04,0]))
    us=[-1,-.983,-.5,0,.5,.983,1]
    vs=[];faces=[];slots=[];rows=[]
    def pos(y,u,zoff):return (u*halfwidth(s,y),y,height(s,u*halfwidth(s,y),y)+zoff)
    def add(coords):
        ids=list(range(len(vs),len(vs)+len(coords)));vs.extend(coords);return ids
    # Levels include bottom, rounded lower rim, seven veneer boundaries,
    # rounded upper edge and grip thickness. No buried internal surfaces.
    levels=[s.thickness*i/7 for i in range(8)]+[s.thickness+.00055]
    for yi,y in enumerate(ys):
        if yi in (0,len(ys)-1):
            rows.append([add([pos(y,0,z)])[0] for z in levels])
        else:rows.append([add([pos(y,u,z) for u in us]) for z in (0,s.thickness+.00055)])
    # Bottom/top grid surfaces and closed laminated perimeter.
    bottom_rows=[];top_rows=[]
    for i,row in enumerate(rows):
        bottom_rows.append([row[0]] if i in (0,len(rows)-1) else row[0])
        top_rows.append([row[-1]] if i in (0,len(rows)-1) else row[1])
    for j in range(len(ys)-1):
        for surf,ma in ((bottom_rows,0),(top_rows,1)):
            a,b=surf[j:j+2]
            if len(a)==1:
                fs=[(a[0],b[k],b[k+1]) for k in range(len(b)-1)]
            elif len(b)==1:fs=[(a[k],b[0],a[k+1]) for k in range(len(a)-1)]
            else:fs=[(a[k],b[k],b[k+1],a[k+1]) for k in range(len(a)-1)]
            faces.extend(fs);slots.extend([ma]*len(fs))
    # Perimeter with bevel-shaped width shrink at outside top/bottom.
    contour=[(y,-1) for y in ys]+[(y,1) for y in reversed(ys[1:-1])]
    rings=[]
    for z in levels:
        coords=[]
        for y,u in contour:
            x=u*halfwidth(s,y)
            shrink=.00035 if z in (0,s.thickness) else (.0007 if z==s.thickness+.00055 else 0)
            x=math.copysign(max(0,abs(x)-shrink),x)
            coords.append((x,y,height(s,x,y)+z))
        rings.append(add(coords))
    for j in range(len(levels)-1):
        for i in range(len(contour)):
            faces.append((rings[j][i],rings[j][(i+1)%len(contour)],rings[j+1][(i+1)%len(contour)],rings[j+1][i]))
            slots.append(1 if j==len(levels)-2 else 2+min(6,int((levels[j]+levels[j+1])/2/s.thickness*7)))
    # Weld rim to grid and eliminate pole slivers. The surface edge is remapped
    # to the same rounded perimeter coordinates before merging.
    for surf,ring in ((bottom_rows,rings[0]),(top_rows,rings[-1])):
        lookup={(round(vs[q][1],9),-1 if vs[q][0]<0 else 1):vs[q] for q in ring}
        for i,rs in enumerate(surf):
            if len(rs)>1:
                for q,sign in ((rs[0],-1),(rs[-1],1)):vs[q]=lookup[(round(ys[i],9),sign)]
    o=G.mesh('Deck / seven ply shell and filed grip',vs,faces,mat)
    for m in [grip,*plies]:o.data.materials.append(m)
    for f,mi in zip(o.data.polygons,slots):f.material_index=mi
    bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=.00002);bmesh.ops.dissolve_degenerate(bm,edges=bm.edges,dist=.000002);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(o.data);bm.free()
    G.smooth(o,25)
    return o

def allen_head(name,x,y,z,mat):
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

def bored_ring(name,at,axis,profile,mat,n=20):
    o=G.lathe(name,profile,mat,n,closed=True)
    o.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler();o.location=at
    return o

def ring(name,at,axis,ro,ri,depth,mat,n=20):
    return bored_ring(name,at,axis,[(0,ri),(0,ro),(depth,ro),(depth,ri)],mat,n)

def annulus(name,at,axis,ro,ri,mat,n=12):
    o=G.mesh(name,[(r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),0) for r in (ri,ro) for i in range(n)],[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat)
    o.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler();o.location=at;return o

def nut(name,at,axis,r,depth,bore,mat,nylon,owner,part):
    o=bored_ring(name,at,axis,[(0,bore),(0,r),(depth,r),(depth,bore)],mat,6)
    tag(o,part,owner)
    q=Vector(at)+Vector(axis)*(depth-.0005)
    tag(annulus(name+' nylon insert',q,axis,r*.73,bore,nylon,6),part,owner)
    return o

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
    shield=material('Checkpoint bearing shield',(.048,.074,.092),.55,.34)
    root=G.pivot('Skateboard',(0,0,0));root['static_root']=True;root['seed']=s.seed;root['age_state']=s.state;root['checkpoint']='form only; no baked texture'
    deck=deform_deck(s,mat,plies,grip)
    # Actual through bores with conical countersinks. Do not stop at bolt discs.
    for sign in (-1,1):
        cy=sign*s.plate_y
        for x in (-s.pitch_x/2,s.pitch_x/2):
            for y in (cy-s.pitch_y/2,cy+s.pitch_y/2):
                z=height(s,x,y)+s.thickness
                cutter=G.lathe('Deck bore tool',[(z-.025,.0025),(z-.0012,.0025),(z+.00055,.00445),(z+.015,.00445)],None,12)
                cutter.location.x=x;cutter.location.y=y;G.boolean(deck,cutter)
                # Head cone fills seat; socket is a real hex recess.
                head=allen_head('Flush Allen bolt head',x,y,z,black);tag(head,'mount_hardware',root)
                shank=G.cylinder('10-32 mounting bolt',(x,y,z+.0007-.0254),(x,y,s.underside-s.riser-.0045),.002413,black,6);tag(shank,'mount_hardware',root)
                nut('Mount locknut',(x,y,s.underside-s.riser-.006),(0,0,-1),.0055,.0048,.002413,steel,rubber,root,'mount_hardware')
    m=deck.modifiers.new('Dissolve nearly planar stance and rail runs','DECIMATE');m.decimate_type='DISSOLVE';m.angle_limit=math.radians(1.25);m.delimit={'MATERIAL','NORMAL'};G.apply(deck)
    G.smooth(deck,25)
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
        base=solidify_cast([plate,tower,ped],label+' cast baseplate',260)
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
                # Four machined nut lands beneath the mounting flange. Their
                # bearing plane is 6 mm below the deck-side mounting plane.
                near_bolt=min(math.hypot(world.x-bx,world.y-by) for bx in (-s.pitch_x/2,s.pitch_x/2) for by in (cy-s.pitch_y/2,cy+s.pitch_y/2))
                if near_bolt<.008 and world.z<z-.006:world.z=z-.006
                v.co=ob.matrix_world.inverted()@world
        m=base.modifiers.new('Post-bore casting reduction','DECIMATE');m.ratio=.82;G.apply(base);G.smooth(base,65)
        cast_normals(base)
        tag(base,'baseplates',root)
        tag(ring(label+' pivot cup',pc-steer*.005,steer,.0065,.0047,.009,rubber,16),'truck_hardware',root)
        tag(G.cylinder(label+' steel kingpin',kbase-kaxis*.003,kbase+kaxis*.044,.0047625,steel,14),'truck_hardware',root)
        # Fixed lower bushing; moving upper stack is only a visual flex proxy.
        tag(bored_ring(label+' barrel bushing',kbase+kaxis*.003,kaxis,[(0,.0049),(0,.0114),(.001,.012),(.0117,.012),(.0127,.0114),(.0127,.0049)],ure,12),'bushings',root)
        tag(ring(label+' bottom cupped washer',kbase+kaxis*.0015,kaxis,.0128,.0049,.0015,steel,12),'truck_hardware',root)
        pivot=G.pivot('Hanger_'+label,pc);pivot.parent=root
        pivot.rotation_euler=steer.to_track_quat('Z','Y').to_euler();pivot['pivot_axis']='Z';pivot['range_degrees']=[-s.lean_limit,s.lean_limit];pivot['axis_world']=list(steer);pivot['pivot_cup_m']=list(pc);pivot['yoke_center_m']=list(yc)
        # Axle tube swells at the center. Curved wings flow toward the yoke.
        hw=s.hanger_width/2
        barrel=G.lathe('Axle barrel seed',[(-hw,0),(-hw,.0066),(-hw+.005,.008),(-.027,.010),(0,.0108),(.027,.010),(hw-.005,.008),(hw,.0066),(hw,0)],al,32,axis='X',center=(ay,az))
        loops=[]
        for frac,ry,rz,blend in [(-1,.0068,.0065,0),(-.82,.008,.007,0),(-.48,.011,.010,.2),(-.22,.018,.013,.5),(0,.022,.014,.6),(.22,.018,.013,.5),(.48,.011,.010,.2),(.82,.008,.007,0),(1,.0068,.0065,0)]:
            cy0=ay+(yc.y-ay)*blend;cz0=az+(yc.z-az)*blend
            loops.append([(frac*hw,cy0+ry*math.cos(a),cz0+rz*math.sin(a)) for a in [math.tau*i/24 for i in range(24)]])
        pieces=[barrel,G.loft('Swept cast wing web seed',loops,al)]
        pieces.append(ellipsoid('Yoke ring seed',yc,(.019,.018,.009),al))
        arm=G.lathe('Tapered cast pivot arm seed',[(0,0),(0,.0045),(.010,.0045),(.025,.0055),(.040,.0065),((yc-pc).length,.0065),((yc-pc).length,0)],al,24);arm.location=pc-steer*.003;arm.rotation_euler=steer.to_track_quat('Z','Y').to_euler();pieces.append(arm)
        hanger=solidify_cast(pieces,label+' sculpted hanger',450)
        cast_cut(hanger,G.cylinder('Open kingpin yoke tool',yc-kaxis*.05,yc+kaxis*.05,.0065,None,16))
        # Counterbored bushing seats leave a 7.8 mm annular web. The cast
        # shoulders flare away from the kingpin hardware's steering envelope.
        for direction,start,radius in [(1,.0055,.0123),(-1,.0023,.0124)]:
            tool=G.lathe('Bushing seat and hardware relief',[(0,0),(0,radius),(.020,.016),(.050,.022),(.050,0)],None,20)
            tool.location=yc+kaxis*direction*start;tool.rotation_euler=(kaxis*direction).to_track_quat('Z','Y').to_euler();cast_cut(hanger,tool)
        m=hanger.modifiers.new('Post-seat casting reduction','DECIMATE');m.ratio=.80;G.apply(hanger);G.smooth(hanger,65)
        # Solid ring yoke carries bushings around its OPEN center, not through a block.
        # Cast ring is allowed to meet central barrel on its far side.
        cast_normals(hanger)
        tag(hanger,'hangers',pivot)
        tag(G.cylinder(label+' continuous axle',(-s.axle_width/2,ay,az),(s.axle_width/2,ay,az),.004,steel,8),'axles',pivot)
        upper=kbase+kaxis*.0235
        tag(bored_ring(label+' cone bushing',upper,kaxis,[(0,.0049),(0,.0118),(.0102,.0088),(.0102,.0049)],ure,12),'bushings',root)
        tag(ring(label+' top cupped washer',upper+kaxis*.0102,kaxis,.0104,.0049,.0015,steel,12),'truck_hardware',root)
        nut(label+' kingpin locknut',upper+kaxis*.0117,kaxis,.0083,.0065,.00476,steel,rubber,root,'truck_hardware')
        if s.riser:
            pad=G.profile(label+' riser pad',[(x,y+cy) for x,y in G.rounded_rectangle(.059,.081,.003,2)],s.underside-s.riser,s.underside,rubber,axis='Z')
            for x in (-s.pitch_x/2,s.pitch_x/2):
                for y in (cy-s.pitch_y/2,cy+s.pitch_y/2):G.boolean(pad,G.cylinder('Riser bore',(x,y,z-.002),(x,y,z+.01),.0029,None,6))
            tag(pad,'riser',root)
        for side,side_label in ((-1,'L'),(1,'R')):
            # Inner ring faces: hanger exit + .5 mm speed ring; 7 + 10 + 7 mm.
            centerx=side*(hw+.0005+.012)
            wr=G.pivot('Wheel_'+label+'_'+side_label,(centerx,ay,az),'X',(0,360));wr['continuous']=True
            bpy.context.view_layer.update();mw=wr.matrix_world.copy();wr.parent=pivot;wr.matrix_world=mw
            r=s.wheel_diameter/2;w=s.wheel_width/2;patch=s.contact_width/2
            profile=[(-w,.011),(-w,.0195),(-w+.0005,r-.0045),(-patch-.002,r-.001),(-patch,r),(patch,r),(patch+.002,r-.001),(w-.0005,r-.0045),(w,.0195),(w,.011),(.005,.011),(.005,.0095),(-.005,.0095),(-.005,.011)]
            wheel=G.lathe('Urethane '+label+' '+side_label,profile,wheelmat,28,axis='X',center=(ay,az),closed=True);wheel.location.x=centerx
            G.smooth(wheel,80)
            tag(wheel,'wheels',wr)
            for bs in (-1,1):
                at=Vector((centerx+bs*.005,ay,az));axis=(bs,0,0)
                # Only the shield-facing race and inner bore can be seen.
                # Omit the race's buried outer cylinder and back face.
                race=G.mesh('608 '+label+side_label+str(bs)+' bearing races',[(rr*math.cos(math.tau*i/20),rr*math.sin(math.tau*i/20),zz) for zz,rr in [(0,.004),(.007,.004),(.007,.011)] for i in range(20)],[(j*20+i,j*20+(i+1)%20,(j+1)*20+(i+1)%20,(j+1)*20+i) for j in range(2) for i in range(20)],steel)
                race.location=at;race.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler();tag(race,'bearings',wr)
                tag(annulus('608 '+label+side_label+str(bs)+' shield',at+Vector(axis)*.00705,axis,.0098,.0054,shield,16),'bearings',wr)
            tag(ring('Bearing spacer '+label+side_label,(centerx-.005,ay,az),(1,0,0),.0055,.004,.010,steel,6),'spacers',pivot)
            for distance in (hw,hw+.0245):
                tag(annulus('Axle speed ring '+label+side_label,(side*(distance+.0005),ay,az),(side,0,0),.006,.004,steel,12),'spacers',pivot)
            nut('Axle nut '+label+side_label,(side*(hw+.025),ay,az),(side,0,0),.0073,.0058,.004,steel,rubber,pivot,'axle_nuts')
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
    sources=bpy.data.collections.new('SOURCE / sculpted casting unions');bpy.context.scene.collection.children.link(sources)
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
