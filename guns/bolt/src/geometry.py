"""B24 authored visual geometry. Millimeters until build.py's single scale pass."""
import math
import bpy,bmesh
from mathutils import Vector,Matrix
from kit import model as M
PARTS=[];HIGH={};MAT={}

def palette():
    for key,c,metal,rough in [
        ('steel',(.018,.022,.026),.85,.35),('alloy',(.012,.016,.021),.75,.38),
        ('stock',(.17,.15,.095),0,.62),('rubber',(.008,.009,.010),0,.78),
        ('bolt',(.26,.28,.30),1,.28),('brass',(.42,.265,.075),1,.3),
        ('copper',(.40,.14,.065),1,.32),('marks',(.58,.60,.56),0,.65),
        ('reticle',(.0002,.0002,.0002),0,1),('glass',(.12,.25,.23),0,.04)]:
        mat=bpy.data.materials.new('CP_'+key);mat.use_nodes=True
        bs=mat.node_tree.nodes.get('Principled BSDF')
        bs.inputs['Base Color'].default_value=(*c,1);bs.inputs['Metallic'].default_value=metal
        bs.inputs['Roughness'].default_value=rough;mat.diffuse_color=(*c,1)
        if key=='glass':
            # Thin game optic proxy: alpha coating preserves the crisp black
            # etched pattern without pretending these flat discs refract a view.
            bs.inputs['Transmission Weight'].default_value=0
            bs.inputs['Alpha'].default_value=.06
            mat.surface_render_method='DITHERED'
        if key=='reticle':bs.inputs['Specular IOR Level'].default_value=0
        MAT[key]=mat

def freeze(ob):
    M.apply(ob);bpy.context.view_layer.update();ob.data.transform(ob.matrix_world)
    ob.matrix_world=Matrix.Identity(4);return ob

def reg(ob,bone='Root',radius=0,segments=2):
    freeze(ob)
    if radius:
        M.bevel(ob,radius,segments)
        m=ob.modifiers.new('Machined flats','WEIGHTED_NORMAL');m.keep_sharp=True;m.weight=40
    M.smooth(ob,42);M.apply(ob);ob['bone']=bone;ob['asset_set']='B24';PARTS.append(ob);return ob

def box(name,lo,hi,mat='steel',bone='Root',r=.3,raw=False):
    lo,hi=Vector(lo),Vector(hi)
    ob=M.box(name,(lo+hi)/2,hi-lo,MAT[mat],0);freeze(ob)
    return ob if raw else reg(ob,bone,r)

def lathe(name,points,mat='steel',bone='Root',axis='Y',center=(0,65),n=48,closed=False,raw=False):
    ob=M.lathe(name,points,MAT[mat],n,axis,center,closed)
    return ob if raw else reg(ob,bone)

def cut(ob,tool,operation='DIFFERENCE'):
    mat=ob.data.materials[0] if ob.data.materials else MAT['steel']
    tool.data.materials.clear();tool.data.materials.append(mat)
    # Closed visual solids use Blender 5.2's manifold solver. Exact produced
    # open junctions where the voxel mold met planar tool faces.
    mod=ob.modifiers.new('Fabricated visual cavity','BOOLEAN');mod.object=tool
    mod.operation=operation;mod.solver='MANIFOLD';M.apply(ob)
    bpy.data.objects.remove(tool,do_unlink=True)
    ob.data.materials.clear();ob.data.materials.append(mat)
    for f in ob.data.polygons:f.material_index=0
    return ob

def cutbox(ob,lo,hi):return cut(ob,box('tool',lo,hi,raw=True))

def roundcut(ob,lo,hi,r=2):
    tool=box('Radiused mold tool',lo,hi,raw=True)
    M.bevel(tool,r,5);freeze(tool);return cut(ob,tool)

def detail_source(base,extras):
    """Keep small authored relief on the dense source, off the game silhouette."""
    vs=[];fs=[]
    for ob in [base]+extras:
        start=len(vs);vs.extend(tuple(v.co) for v in ob.data.vertices)
        fs.extend(tuple(start+i for i in f.vertices) for f in ob.data.polygons)
    guide=M.mesh('Authored relief guide',vs,fs,base.data.materials[0])
    HIGH[base.name]=guide.data.copy();bpy.data.objects.remove(guide,do_unlink=True)
    for ob in extras:PARTS.remove(ob);bpy.data.objects.remove(ob,do_unlink=True)

def tube(name,path,r,mat='steel',bone='Root',n=12):
    return reg(M.tube(name,path,r,MAT[mat],sides=n),bone)

def screw(name,pos,axis='Z',r=2.2,bone='Root',direction=1):
    x,y,z=pos
    center=(y,z) if axis=='X' else ((x,z) if axis=='Y' else (x,y))
    h={'X':x,'Y':y,'Z':z}[axis]
    ob=lathe(name,[(h-1,0),(h-1,r*.83),(h-.5,r),(h+.5,r),(h+.8,r*.8),(h+.8,0)],
             bone=bone,axis=axis,center=center,n=16,raw=True)
    # A recessed hex socket, with softened machined perimeter.
    cut(ob,lathe('tool',[(h-.1,0),(h-.1,r*.47),(h+2,r*.47),(h+2,0)],axis=axis,center=center,n=6,raw=True))
    if direction<0:
        k='XYZ'.index(axis)
        for v in ob.data.vertices:v.co[k]=2*h-v.co[k]
        bm=bmesh.new();bm.from_mesh(ob.data)
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    return reg(ob,bone)

def rounded_loop(w,h,n=48,power=2.6):
    return [(w/2*math.copysign(abs(math.cos(t))**(2/power),math.cos(t)),
             h/2*math.copysign(abs(math.sin(t))**(2/power),math.sin(t))) for t in [math.tau*i/n for i in range(n)]]

def flow(rows,substeps=5):
    """Bounded cubic station interpolation: no planar spans or overshoot."""
    def slope(i,k):
        if i==0 or i==len(rows)-1:return 0
        a=(rows[i][k]-rows[i-1][k])/(rows[i][0]-rows[i-1][0])
        b=(rows[i+1][k]-rows[i][k])/(rows[i+1][0]-rows[i][0])
        return 2*a*b/(a+b) if a*b>0 else 0
    out=[]
    for i in range(len(rows)-1):
        a,b=rows[i:i+2];span=b[0]-a[0]
        for j in range(substeps):
            t=j/substeps;out.append([a[0]+span*t]+[
                (2*t**3-3*t*t+1)*a[k]+(t**3-2*t*t+t)*span*slope(i,k)+
                (-2*t**3+3*t*t)*b[k]+(t**3-t*t)*span*slope(i+1,k) for k in range(1,len(a))])
    return out+[rows[-1]]

def sculpt_stock():
    # Broad changing oval/superellipse stations; grip joins as a separate
    # volumetric seed, then voxel union and relaxation make one molding.
    # The comb nose flows down BEFORE the rearward shroud, instead of carving
    # a cylinder-ended trough through it. Butt height 127 mm is a trimmed class
    # medium pad; the cheek and wrist sections taper in width and curvature.
    rows=[(-285,43.5,-49,78),(-272,44,-46,79),(-245,43,-31,79),
          (-214,40,-15,79),(-195,38,-5,76),(-178,36,8,67),
          (-162,34,18,54),(-145,33,24,46),(-125,33,22,45),
          (-95,33,20,46),(-65,34,18,47.5),(-40,35,16,47.5),
          (-20,36,15,47.5),(10,40,20,55),(48,47,19,60),(100,54,18,61),
          (175,61,18,62),(260,63,19,62),(360,62,20,61),(420,57,22,58),
          (437,48,26,54),(444,34,33,48)]
    loops=[]
    for y,w,lo,hi in flow(rows,7):
        loop=[];middle=(lo+hi)/2
        for x,z0 in rounded_loop(w,hi-lo,128,2.05+2.15*max(0,min(1,(y-10)/230))):
            z=middle+z0
            if y>=218 and z0>0:
                radius=16.87-max(0,y-286.2)*1.17/(460-286.2)
                channel=65-math.sqrt(radius**2-x*x) if abs(x)<radius else 65+3*(abs(x)-radius)
                t=max(0,min(1,(y-218)/20));k=3.5*t*t*(3-2*t)
                if k:
                    h=max(0,min(1,.5+.5*(channel-z)/k))
                    z=channel*(1-h)+z*h-k*h*(1-h)
                else:z=min(z,channel)
            loop.append((x,y,z))
        loops.append(loop)
    ob=M.loft('Stock_Mold',loops,MAT['stock'])
    griprows=[(-42,32,-26,36),(-38,36,-25,42),(-20,38,-21,45),(0,37,-17,46),
              (22,33,-12,44),(40,31,-9,36),(46,29,-8,30)]
    grip=M.loft('Grip volume seed',[[(x,yc+y,z) for x,y in rounded_loop(w,d,64,2.35)]
        for z,w,yc,d in flow(griprows)],MAT['stock'])
    freeze(grip);cut(ob,grip,'UNION')
    rem=ob.modifiers.new('Sculpt union','REMESH');rem.mode='VOXEL';rem.voxel_size=.65;rem.use_smooth_shade=True;M.apply(ob)
    mod=ob.modifiers.new('Mold flow','SMOOTH');mod.factor=.65;mod.iterations=18;M.apply(ob)
    cut(ob,lathe('tool',[(43.5,0),(43.5,17.65),(225,17.65),(225,0)],raw=True,n=96))
    cut(ob,lathe('Shroud clearance tool',[(-3,0),(-3,9.3),(45,9.3),(45,0)],raw=True,n=64))
    # The channel and its rounded lands are already sculpted into the sections.
    # A smooth minimum blends the cylindrical floor into the broad shoulders;
    # it does not rely on a bevel clamped by tiny voxel/Boolean boundary edges.
    roundcut(ob,(-13.3,102,-70),(13.3,184.2,60),2)
    cutbox(ob,(-7,20,10),(7,40,53))
    cutbox(ob,(-7.2,9,9),(7.2,106,28))
    cutbox(ob,(-6,99,23),(6,107,32))
    roundcut(ob,(-8.8,-12.3,48.1),(8.8,55.3,64),3)
    # Smooth tang pocket and radiused handle notch, with no high thin shoulder.
    cut(ob,lathe('Rounded bolt notch tool',[(4,0),(4,16.5),(40,16.5),(40,0)],
        axis='X',center=(33,55.5),n=64,raw=True))
    roundcut(ob,(14,4,57),(22,22,82),3)
    roundcut(ob,(8,97,50),(39,175,90),4)
    # Only the plate's shallow inlet is removed: never cut away the grip below it.
    roundcut(ob,(-18.2,-11.1,14.7),(18.2,205.2,22.2),2.8)
    edge=ob.modifiers.new('Rounded channel lands','BEVEL');edge.width=2.0
    edge.segments=4;edge.limit_method='ANGLE';edge.angle_limit=math.radians(38);M.apply(ob)
    # Re-voxel the finished mold to heal Boolean junctions before reduction.
    rem=ob.modifiers.new('Finished mold topology','REMESH');rem.mode='VOXEL';rem.voxel_size=.5;rem.use_smooth_shade=True;M.apply(ob)
    mod=ob.modifiers.new('Cavity edge rounding','SMOOTH');mod.factor=.5;mod.iterations=6;M.apply(ob)
    # A mold radius blends the tang reveal into the handle relief. Independent
    # cylindrical and planar tools otherwise leave a thin pointed saddle here.
    vg=ob.vertex_groups.new(name='Tang shoulder blend')
    for v in ob.data.vertices:
        x,y,z=v.co
        def ramp(a,b,t):
            t=max(0,min(1,(t-a)/(b-a)));return t*t*(3-2*t)
        weight=(ramp(3,9,x)*(1-ramp(20,27,x))*ramp(-12,-2,y)*
                (1-ramp(29,43,y))*ramp(36,43,z))
        if weight>0:vg.add([v.index],weight,'REPLACE')
    mod=ob.modifiers.new('Molded tang shoulder radius','SMOOTH')
    mod.vertex_group=vg.name;mod.factor=.65;mod.iterations=160;M.apply(ob)
    ob.vertex_groups.clear()
    M.smooth(ob,60)
    HIGH[ob.name]=ob.data.copy()
    count=sum(len(f.vertices)-2 for f in ob.data.polygons)
    dec=ob.modifiers.new('Game sculpt reduction','DECIMATE');dec.ratio=min(1,9000/count);M.apply(ob)
    # Transfer dense sculpt normals before baking; reject opposing corners later.
    dense=bpy.data.objects.new('Dense normal guide',HIGH[ob.name]);bpy.context.collection.objects.link(dense)
    dt=ob.modifiers.new('Continuous mold normal field','DATA_TRANSFER');dt.object=dense;dt.use_loop_data=True
    dt.data_types_loops={'CUSTOM_NORMAL'};dt.loop_mapping='POLYINTERP_NEAREST';M.apply(ob)
    bpy.data.objects.remove(dense,do_unlink=True);reg(ob)
    # Separate molded rubber pad, curved face and taper; 25 mm class thickness.
    loops=[]
    for y,w,lo,hi in [(-310,40,-46,75),(-307,43.5,-49,78),(-290,43.5,-49,78),(-285.1,43.5,-49,78)]:
        loops.append([(x,y,z+(hi+lo)/2) for x,z in rounded_loop(w,hi-lo,64,2.05)])
    pad=M.loft('Recoil_Pad',loops,MAT['rubber'])
    for z in (-12,48):
        cut(pad,lathe('Pad head recess',[(-312,0),(-312,2.7),(-308.1,2.7),(-308.1,0)],
                      axis='Y',center=(0,z),n=24,raw=True))
    reg(pad)
    for z in (-12,48):screw('Pad_Screw',(0,-309.1,z),axis='Y',r=2.5,direction=-1)

def ammunition(name,base,bone,n=24,fired=False):
    x,y,z=base
    # Only visual case exterior, open mouth for the cheap fired variant.
    if fired:
        profile=[(0,2.35),(0,6.005),(1.3,6.005),(1.3,5.1),(2.6,5.1),(2.6,5.96),
                 (39.5,5.72),(44.5,4.37),(51.18,4.37),(51.18,4.03),(45,4.03),(39,5.35),
                 (3,5.35),(3,2.35)]
        # Spend the case budget at the visible shoulder and open mouth. The
        # recessed primer pocket and hidden inner base need fewer radial steps.
        counts=[16,24,24,16,16,24,32,32,40,40,32,24,16,16]
        verts=[];rings=[];faces=[]
        for (h,r),count in zip(profile,counts):
            rings.append(list(range(len(verts),len(verts)+count)))
            verts.extend((x+r*math.cos(math.tau*i/count),y+h,z+r*math.sin(math.tau*i/count)) for i in range(count))
        for j,a in enumerate(rings):
            b=rings[(j+1)%len(rings)];i=k=0
            # Angular zipper: all transitions are manifold; no T junctions.
            while i<len(a) or k<len(b):
                if k==len(b) or (i<len(a) and (i+1)/len(a)<=(k+1)/len(b)):
                    faces.append((a[i%len(a)],b[k%len(b)],a[(i+1)%len(a)]));i+=1
                else:
                    faces.append((a[i%len(a)],b[k%len(b)],b[(k+1)%len(b)]));k+=1
        ob=M.mesh(name+'_Case',verts,faces,MAT['brass'])
        bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
        reg(ob,bone)
        # Analytic revolution normals remove the uneven triangle weighting at
        # unequal-count ring joins. Preserve real sharp rim/groove boundaries;
        # smoothly shade only profile turns below the existing 42-degree limit.
        owner={vertex:j for j,ring in enumerate(rings) for vertex in ring}
        section=[]
        for j,(h,r) in enumerate(profile):
            hh,rr=profile[(j+1)%len(profile)];section.append(Vector((-(rr-r),hh-h)).normalized())
        normals=[None]*len(ob.data.loops)
        for face in ob.data.polygons:
            ids={owner[v] for v in face.vertices}
            band=next(j for j in ids if (j+1)%len(profile) in ids)
            for li in face.loop_indices:
                v=ob.data.vertices[ob.data.loops[li].vertex_index];j=owner[v.index]
                other=(j-1)%len(profile) if j==band else j
                a,b=section[band],section[other]
                s=(a+b).normalized() if a.dot(b)>math.cos(math.radians(42)) else a
                angle=math.atan2(v.co.z-z,v.co.x-x)
                normal=Vector((s.y*math.cos(angle),s.x,s.y*math.sin(angle)))
                assert normal.dot(face.normal)>.06,(name,face.index)
                normals[li]=normal
        ob.data.normals_split_custom_set(normals)
        lathe(name+'_Primer',[(y+.12,0),(y+.12,.3),(y+.02,.8),(y+.02,2.3),(y+.2,2.3),(y+.2,0)],
              'bolt',bone,center=(x,z),n=8)
    else:
        profile=[(0,0),(0,6.005),(1.3,6.005),(1.3,5.1),(2.6,5.1),(2.6,5.96),
                 (39.5,5.72),(44.5,4.37),(51.18,4.37),(51.18,0)]
        lathe(name+'_Case',[(y+h,r) for h,r in profile],'brass',bone,center=(x,z),n=n)
        lathe(name+'_Bullet',[(y+h,r) for h,r in [(45,0),(45,3.45),(48,3.91),(55,3.91),
             (59,3.65),(64,2.8),(68,1.65),(71.12,.1),(71.12,0)]],'copper',bone,center=(x,z),n=n)

def magazine():
    start=len(PARTS)
    # Primary five-round reference: 2.52 in rear height, 3.055 in outside length.
    # Ribs are pressed into both faces of a nominal 1 mm sheet, not glued strips.
    front=58+3.055*25.4;bottom=46-2.52*25.4
    body=box('Magazine_Shell',(-12.3,58,bottom+1.5),(12.3,front,46),'steel',r=0,raw=True)
    M.bevel(body,.8,3);freeze(body)
    for side in (-1,1):
        for y in (77,116):
            x0,x1=sorted((side*11,side*13.1))
            rib=box('Pressed rib tool',(x0,y-2.5,-11),(x1,y+2.5,31),raw=True)
            M.bevel(rib,1,4);freeze(rib);cut(body,rib,'UNION')
    cutbox(body,(-11.3,59,bottom+2.5),(11.3,front-1,55))
    # The formed lips define the upper sides. Tall straight walls here would
    # obscure the retained round and read as a solid brick in the open port.
    cutbox(body,(-14,61,39),(14,front-1.1,55))
    for side in (-1,1):
        for y in (77,116):
            x0,x1=sorted((side*10.2,side*12.1))
            roundcut(body,(x0,y-1.6,-10.1),(x1,y+1.6,30.1),.8)
    cutbox(body,(-14,58,37),(14,62,50))
    cutbox(body,(-7,front-3,35),(7,front+2,50))
    roundcut(body,(-5.2,56,19.8),(5.2,60,23.5),.4)
    reg(body,'Magazine')
    floor=box('Magazine_Floorplate',(-13.5,56.8,bottom),(13.5,front+1.2,bottom+4.2),'steel',raw=True)
    roundcut(floor,(-12.4,57.9,bottom+1.2),(12.4,front+.1,bottom+6),.6)
    reg(floor,'Magazine',.4,3)
    for side in (-1,1):
        # Curled lip follows the case's upper quadrants, 8 mm aperture < 12 mm case.
        th=math.acos(4/6.04)
        outer=[(side*(6.69*math.cos(th*i/12)),39+6.69*math.sin(th*i/12)) for i in range(13)]
        inner=[(side*(6.04*math.cos(th*i/12)),39+6.04*math.sin(th*i/12)) for i in range(13)]
        pts=[(side*12.3,35),(side*12.3,39),*outer,*reversed(inner),(side*11.3,38),(side*11.3,35)]
        reg(M.profile('Magazine_FeedLip',pts,61,72,MAT['steel'],axis='Y'), 'Magazine',.12)
    box('Magazine_Follower',(-5.3,62,17.05),(5.3,131.5,21.20),'alloy','Follower',r=.6)
    # Two representative rounds; capacity is semantic, not five hidden meshes.
    ammunition('Magazine_TopRound',(0,63,39),'TopRound',24)
    ammunition('Magazine_ReserveRound',(3.7,63,27.2),'ReserveRound',18)
    ammunition('ChamberRound',(0,209.5,65),'ChamberRound',20)
    ammunition('CycleCase',(0,209.5,65),'CycleCase',fired=True)
    # Feed height is just below the closed bolt, so the retained top round reads
    # through the port. Bone frames/sockets and the catch's accepted pose stay put.
    for ob in PARTS[start:]:
        if ob['bone'] in ('Magazine','Follower','TopRound','ReserveRound'):
            for v in ob.data.vertices:v.co.z+=7
    # The catch tooth engages an actual shoulder on the removable shell.
    box('Magazine_CatchShoulder',(-5.2,56.2,26),(5.2,59.1,26.8),'steel','Magazine',r=.12)


def correct_feed_box():
    """Move the complete seated box, keep its outside dimensions and catch."""
    from feed import MAG_SHIFT,ROUND_SHIFT,FEED_RISE
    for ob in PARTS:
        bone=ob['bone']
        if bone not in ('Magazine','Follower','TopRound','ReserveRound'):continue
        shift=ROUND_SHIFT if bone in ('TopRound','ReserveRound') else MAG_SHIFT
        for v in ob.data.vertices:
            v.co.y+=shift
            if bone in ('Follower','TopRound','ReserveRound') or ob.name.startswith('Magazine_FeedLip'):
                v.co.z+=FEED_RISE
                if ob.name.startswith('Magazine_FeedLip') and v.co.z<.1+35+7+FEED_RISE:v.co.z-=.7
    # Front binder leaves the cited 72.898 mm usable interior length.
    box('Magazine_Binder',(-11.3,178.898,-8),(11.3,181.597,42),'steel','Magazine',r=0)
