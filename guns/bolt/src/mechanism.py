"""Original external visual mechanism; not a functioning firearm design."""
import math
import bpy
from mathutils import Vector,Matrix
from geometry import *

def action_barrel():
    # A connected two-surface tube cage preserves the machined cylindrical
    # sections without a decimator collapsing the long internal clearway.
    stations=[45,45.5,47,81.7,100,172,187,197.8,198,206,206.2,222,223.5,224]
    n=64;vs=[];faces=[];outer=[]
    for inside in (False,True):
        for y in stations:
            for k in range(n):
                t=math.tau*k/n;c=math.cos(t);s=math.sin(t)
                r=17.5 if 47<=y<=222 else (17+(min(y-45,224-y)/2)*.5)
                if inside:
                    race=max(8.95,min(13.35,4.5/max(abs(c),1e-6)))
                    f=max(0,min(1,(y-197.8)/.2))*max(0,min(1,(206.2-y)/.2))
                    r=race+(13.35-race)*f
                vs.append((r*c,y,65+r*s))
    total=len(vs)//2
    for i in range(len(stations)-1):
        mid=(stations[i]+stations[i+1])/2
        for k in range(n):
            t=math.tau*(k+.5)/n;angle=(math.degrees(t)+180)%360-180
            # Rounded axial lead-in/out gives small radii at the port ends.
            hole=False
            if hole:continue
            q=(i*n+k,i*n+(k+1)%n,(i+1)*n+(k+1)%n,(i+1)*n+k)
            outer.append(q);faces.append(q);faces.append(tuple(v+total for v in reversed(q)))
    edges={}
    for f in outer:
        for a,b in zip(f,f[1:]+f[:1]):
            key=tuple(sorted((a,b)));edges[key]=edges.get(key,0)+1
    for (a,b),count in edges.items():
        if count==1:faces.append((a,b,b+total,a+total))
    receiver=M.mesh('Receiver',vs,faces,MAT['steel'])
    roundcut(receiver,(0,100,49),(30,172,91),4)
    roundcut(receiver,(-13.4,57,40),(13.4,137,60),3)
    roundcut(receiver,(14,4,59),(21,21,76),2);reg(receiver)
    # Barrel length is measured chamber face to muzzle, not exposed tube.
    muzzle=(1.210-(1.210-.900)*21/23)*25.4/2
    barrel=lathe('Barrel',[(210,6.2),(210,15.367),(286.2,15.367),
        (818.7,muzzle),(819.6,muzzle-.65),(819.6,8.6),(818.2,8.1),
        (817.5,4.0),(262,4.0),(261,4.55),(254.5,4.55),(249.5,6.2)],
        closed=True,n=64,raw=True)
    reg(barrel)
    # Recoil lug is supported by the bedding; not an ornamental floating plate.
    lug=box('Recoil_Lug',(-18,220,28),(18,224,68),r=0,raw=True)
    cut(lug,lathe('tool',[(217,0),(217,15.9),(227,15.9),(227,0)],raw=True,n=48));reg(lug,radius=.5)
    bolt=lathe('Bolt_Body',[(28,0),(28,8.65),(207.5,8.65),(209.5,7.9),(209.5,0)],'bolt','Bolt',n=56)
    cut(bolt,lathe('tool',[(24,0),(24,3.6),(41,3.6),(41,0)],n=32,raw=True))
    # Weld Boolean slivers below the export's useful precision, before normals.
    bm=bmesh.new();bm.from_mesh(bolt.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.003)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.003)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(bolt.data);bm.free();M.smooth(bolt,42)
    # The two visible lugs engage the actual pocket's rear-facing seats.
    for side in (-1,1):
        x0,x1=sorted((side*8.2,side*12.65))
        box('Bolt_Lug', (x0,198,61.5),(x1,205,68.5),'bolt','Bolt',r=.18)
    # A forged collar, swept stem, tapered cylindrical shroud and LOWER tail
    # replace the first checkpoint's ball-shaped rear and square top block.
    lathe('Bolt_HandleCollar',[(28,8.66),(28,10),(30,10.8),(40.5,10.8),(43,9.8),(43,8.66)],
          bone='Bolt',n=48,closed=True)
    path=[(8,34.5,65,6.0,4.2),(12,31.5,52.5,5.5,3.2),(24,24.5,47,4.8,3.2),
          (34,18.5,33,4,3.8),(43,13,31,3.6,3.8),(51,11,31,3.6,3.8)]
    loops=[]
    for i,(x,y,z,ry,rn) in enumerate(path):
        a=Vector((path[max(0,i-1)][0],path[max(0,i-1)][2]));b=Vector((path[min(len(path)-1,i+1)][0],path[min(len(path)-1,i+1)][2]))
        t=(b-a).normalized();norm=Vector((-t.y,t.x))
        loops.append([(x+rn*math.sin(t)*norm.x,y+ry*math.cos(t),z+rn*math.sin(t)*norm.y)
                     for t in [math.tau*j/20 for j in range(20)]])
    reg(M.loft('Bolt_Handle',loops,MAT['steel']),'Bolt')
    knob=lathe('Bolt_Knob',[(-12,0),(-11,5.5),(-8,10),(0,11.5),(8,10),(11,5.5),(12,0)],
        'steel','Bolt',axis='X',center=(11,31),n=40,raw=True)
    for v in knob.data.vertices:v.co.x+=58
    reg(knob,'Bolt')
    shroud=lathe('Bolt_Shroud',[(-1,3.7),(-1,6.0),(1,6.9),(9,8.5),
          (21,8.9),(25,8.9),(26.7,8.35),(26.7,3.7)],
          'steel','BoltTravel',n=56,closed=True)
    roundcut(shroud,(-3.5,-5,44),(3.5,28,64),.6)
    tail=M.profile('Cocking_Piece',[(-1,50),(-1,53),(9,56),(13,64),
          (22,64),(22,53),(8,50)],-2.7,2.7,MAT['bolt'],axis='X')
    reg(tail,'CockingPiece',.45,3)
    lathe('Cocking_Shaft',[(-1,0),(-1,3.1),(26,3.1),(26,0)],'bolt','CockingPiece',n=32)
    # A single rounded tongue under the cocking tail, as seen in the sharp
    # rear-action photo (detail_032), rather than two exposed parallel horns.
    # Its shallow top clears the accepted tail's whole withdrawal path.
    tang=M.profile('Action_Tang',[(-6,-12),(-8.5,-8),(-8.5,49),
        (-7,55),(7,55),(8.5,49),(8.5,-8),(6,-12)],48.5,49.2,
        MAT['steel'],axis='Z')
    reg(tang,radius=.25,segments=3)
    # Steel bottom metal surrounds, rather than fills, the well.
    plate=box('Bottom_Metal',(-18,-10,15),(18,158,22),raw=True)
    M.bevel(plate,2.8,5);freeze(plate)
    roundcut(plate,(-13.3,54,10),(13.3,137.2,27),2);roundcut(plate,(-6.5,10,10),(6.5,54,28),2)
    roundcut(plate,(-7.1,45,10),(7.1,59,28),1.2)
    reg(plate,radius=.65,segments=3)
    # Machined bow with broad flat faces and small rounded section corners.
    outline=(M.bezier((2,18),(2,-10),(2,-12),(20,-12),12)+
             M.bezier((20,-12),(31,-12),(37,-12),(39,-8),8)[1:]+
             M.bezier((39,-8),(42,-4),(42,8),(42,18),10)[1:])
    loops=[]
    for i,(y,z) in enumerate(outline):
        a=Vector(outline[max(0,i-1)]);b=Vector(outline[min(len(outline)-1,i+1)])
        tangent=(b-a).normalized();norm=Vector((-tangent.y,tangent.x))
        loops.append([(x,y+v*norm.x,z+v*norm.y) for x,v in rounded_loop(14.5,7.6,24,5)])
    reg(M.loft('Trigger_Guard',loops,MAT['steel']))
    from trigger import build as trigger_blade
    trigger_blade()
    lathe('Trigger_Pin',[(-7,0),(-7,1.8),(7,1.8),(7,0)],axis='X',center=(26.69,23),n=16)
    box('BoltRelease',(-5.5,12,12),(-1,24,15),'steel','BoltRelease',r=.7)
    box('Magazine_Release',( -6.5,51.8,1),(6.5,56,24),'steel','MagRelease',r=1.1)
    box('Magazine_Catch',(-4.8,54.2,25.8),(4.8,56.2,29.8),'steel','MagRelease',r=.1)
    # Two-position safety: rounded thumb flag on a short stamped stalk.
    lathe('Safety_PivotPin',[(13,0),(13,1.3),(19,1.3),(19,0)],axis='X',center=(14,62),n=16)
    tube('Safety_Stem',[(17,14,62),(19.2,13,75),(19.2,15,79)],1.7,'steel','Safety',10)
    box('Safety_Pad',(17.7,9,77),(22.7,20,80),'steel','Safety',r=1)
    for y in (-6,153):screw('Action_Screw',(0,y,15),r=3,direction=-1)
    # Sling studs with actual eye holes; bipod uses the forward one.
    for y,z in [(-255,-34.5),(410,22)]:
        stud=lathe('Sling_Stud',[ (z-9,0),(z-9,3.5),(z-4,3.5),(z-3,5),(z,5),(z,0)],
                   axis='Z',center=(0,y),n=24,raw=True)
        cut(stud,lathe('tool',[(-6,0),(-6,1.65),(6,1.65),(6,0)],axis='X',center=(y,z-6),n=16,raw=True))
        reg(stud)

def optic():
    # A single machined rail base, relieved underside and original slot pattern.
    # Extend the one-piece rear tail under the accepted rear-ring location.
    # Both ring feet physically seat on this rail; screws land on receiver bridges.
    base=box('Scope_Base',(-10.5,-30,82),(10.5,218,89),'steel',r=0,raw=True)
    for y in range(-25,211,10):
        # Leave solid lands around recessed base fasteners, including their
        # seats; a cross-slot must not remove half a screw's bearing surface.
        if any(y-2.5<s<y+6.5 for s in (60,82,193,209)):continue
        cutbox(base,(-13,y,86.5),(13,y+4,92))
    cut(base,lathe('Receiver-matched base saddle',[(45,0),(45,17.5),(225,17.5),(225,0)],n=64,raw=True))
    for y in (60,82,193,209):
        cut(base,lathe('Base screw counterbore',[(87.5,0),(87.5,2.15),(92,2.15),(92,0)],
                       axis='Z',center=(0,y),n=24,raw=True))
    low=base.data.copy()
    reg(base,radius=.12,segments=1)
    HIGH[base.name]=base.data.copy();base.data=low;M.smooth(base,42);M.apply(base)
    for y in (60,82,193,209):screw('Base_Screw',(0,y,88.5),r=2)
    # Hollow revolved tube with separate power/diopter rings and glass.
    prof=[(-125,18.9),(-125,21.6),(-119,21.8),(-88,21.3),(-71,20),
          (-42,15),(132,15),(170,17),(201,25),(230,25.5),(232,24.6),
          (232,22),(224,22),(201,21.8),(166,13.4),(-39,13.4),(-71,18.2),(-119,18.9)]
    lathe('Scope_Body',prof,'alloy',center=(0,113),n=64,closed=True)
    for y,bone,r0,r1 in [(-78,'PowerRing',20.75,22.2),(-119,'Diopter',21.8,22.7)]:
        base=lathe('Scope_'+bone,[(y, r0),(y,r1),(y+8,r1),(y+8,r0)],'alloy',bone,center=(0,113),n=64,closed=True)
        detail_start=len(PARTS)
        for j in range(24):
            t=math.tau*j/24
            # Broad low ribs are silhouette detail; fine knurl waits for bake.
            x=r1*math.cos(t);z=113+r1*math.sin(t)
            tube('Scope_GripRib',[(x,y+1,z),(x,y+7,z)],.55,'alloy',bone,6)
        detail_source(base,PARTS[detail_start:].copy())
    tube('Scope_ThrowLever',[(-22,-74,119),(-28,-74,122)],2,'alloy','PowerRing',12)
    lathe('Scope_ThrowTip',[(-31,0),(-31,3.2),(-26,3.2),(-26,0)],'alloy','PowerRing',axis='X',center=(-74,122),n=16)
    # Two split rings: contiguous inner radius seats directly on 30 mm tube.
    for y in (-18,123):
        for cap,lo,hi in [('Lower',math.pi,math.tau),('Upper',0,math.pi)]:
            n=32;inner=[(15*math.cos(lo+(hi-lo)*i/n),113+15*math.sin(lo+(hi-lo)*i/n)) for i in range(n+1)]
            outer=[(19*math.cos(lo+(hi-lo)*i/n),113+19*math.sin(lo+(hi-lo)*i/n)) for i in range(n+1)]
            ring=M.profile('Ring_'+cap,inner+list(reversed(outer)),y-8,y+8,MAT['steel'],axis='Y')
            cutbox(ring,(-25,y-9,112.7),(25,y+9,113.3));reg(ring)
        box('Ring_Foot',(-13,y-9,89),(13,y+9,95),'steel',r=.5)
        box('Ring_Saddle',(-8,y-8,94.5),(8,y+8,98),'steel',r=.4)
        for x in (-20,20):
            box('Ring_EarLower',(x-3.1,y-8,109.5),(x+3.1,y+8,112.7),'steel',r=.45)
            box('Ring_EarCap',(x-3.1,y-8,113.3),(x+3.1,y+8,116),'steel',r=.45)
            for dy in (-4.8,4.8):screw('Ring_Screw',(x,y+dy,116),r=2)
        lathe('Ring_Crossbolt',[(-16,0),(-16,2),(13,2),(13,0)],axis='X',center=(y,91),n=12)
        box('Ring_BaseClamp',(-14.5,y-7,87.5),(-10.5,y+7,94.5),r=.45)
        lathe('Ring_ClampWasher',[(-15.4,2.05),(-15.4,4.3),(-14.5,4.3),(-14.5,2.05)],axis='X',center=(y,91),n=24,closed=True)
        lathe('Ring_CrossboltNut',[(-18.8,2),(-18.8,3.7),(-18.3,4.1),(-15.5,4.1),(-15.2,3.7),(-15.2,2)],
              axis='X',center=(y,91),n=6,closed=True)
    # Turrets have axial shoulders, numbers later live in the original atlas.
    block=box('Turret_Block',(-16.5,45,99),(16.5,79,129),'alloy',raw=True)
    M.bevel(block,3,2);freeze(block)
    cut(block,lathe('Clear optical passage',[(42,0),(42,13.4),(82,13.4),(82,0)],
                    center=(0,113),n=64,raw=True))
    reg(block)
    for axis,bone,center,start in [('Z','Elevation',(0,62),129),('X','Windage',(62,113),16.5),('X','Parallax',(62,113),-39)]:
        length=22.5
        base=lathe('Turret_'+bone,[(start,0),(start,12),(start+3,12),(start+3,14.5),
            (start+length-2,14.5),(start+length,13),(start+length,0)],'alloy',bone,axis=axis,center=center,n=56)
        detail_start=len(PARTS)
        for j in range(32):
            t=math.tau*j/32;r=14.55
            if axis=='Z':a=(r*math.cos(t),62+r*math.sin(t),start+11);b=(a[0],a[1],start+19)
            else:a=(start+11,62+r*math.cos(t),113+r*math.sin(t));b=(start+19,a[1],a[2])
            tube('Turret_Grip', [a,b],.5,'alloy',bone,5)
        detail_source(base,PARTS[detail_start:].copy())
    # Coated thin optical elements remain simple glass at the checkpoint.
    for name,y,r in [('Ocular',-122,18.8),('Objective',229,21.9)]:
        lathe('Lens_'+name,[(y,0),(y,r),(y+.5,r),(y+.5,0)],'glass',center=(0,113),n=64)
    # Original split-post reticle, physically visible in the direct aimed view.
    # A game may hide Reticle and draw its own same-centered UI pattern.
    for sign in (-1,1):
        box('Reticle_Post',(min(sign*12,sign*.9),-108.1,112.89),
            (max(sign*12,sign*.9),-108,113.11),'reticle','Reticle',r=0)
    box('Reticle_Vertical',(-.11,-108.1,101),(.11,-108,125),'reticle','Reticle',r=0)
    for z in (109,105,117,121):box('Reticle_Hash',(-.9,-108.1,z-.09),(.9,-108,z+.09),'reticle','Reticle',r=0)
    # These original scale faces are checkpoint overlays. They move with their
    # control and become bake-source markings at the authorized finish stage.
    from kit.fonts import find_font
    font=bpy.data.fonts.load(find_font('DejaVu Sans','Book'))
    for j in range(12):
        t=math.tau*j/12;radial=Vector((math.cos(t),math.sin(t),0));up=Vector((0,0,1))
        tangent=Vector((-math.sin(t),math.cos(t),0))
        origin=Vector((0,62,134))+radial*14.61
        cu=bpy.data.curves.new('Original turret scale','FONT');cu.body=str(j);cu.size=2.9
        cu.align_x='CENTER';cu.font=font;cu.resolution_u=2
        ob=bpy.data.objects.new('Turret_Number',cu);bpy.context.collection.objects.link(ob)
        ob.matrix_world=Matrix.Translation(origin)@Matrix((tangent,up,radial)).transposed().to_4x4()
        ob.data.materials.append(MAT['marks']);bpy.context.view_layer.objects.active=ob;ob.select_set(True)
        bpy.ops.object.convert(target='MESH');ob=bpy.context.view_layer.objects.active
        ob.select_set(False);reg(ob,'Elevation');ob['allow_boundary']=True
        for k in range(4):
            a=t+k*math.tau/48
            p=Vector((0,62,132))+Vector((math.cos(a),math.sin(a),0))*14.62
            # Tiny raised ink bars have finite section, not sharp unattached rods.
            tube('Turret_ScaleTick',[p,p+up*(1.5 if k==0 else .7)],.085,'marks','Elevation',4)

def bipod():
    # Saddle rests on stock underside; steel clamp captures the sling eye.
    saddle=box('Bipod_Saddle',(-18,393,12),(18,427,21.9),'steel',r=1,raw=True)
    cutbox(saddle,(-4,402,13),(4,418,23));reg(saddle)
    lathe('Bipod_StudPin',[(-6,0),(-6,1.6),(6,1.6),(6,0)],axis='X',center=(410,16),n=20)
    box('Bipod_Yoke',(-18,404,-1),(18,416,8),'steel',r=2)
    lathe('Bipod_Axle',[(-27.5,0),(-27.5,2),(27.5,2),(27.5,0)],axis='X',center=(410,2),n=20)
    lathe('Bipod_ClampKnob',[(-4,0),(-4,8),(4,8),(4,0)],axis='Z',center=(0,410),n=28)
    for side,label in [(-1,'L'),(1,'R')]:
        x=side*24;hinge='Bipod'+label;bone='BipodSplay'+label;ext='BipodExtend'+label
        lathe('Bipod_Hinge',[(x-5,2.15),(x-5,8),(x+5,8),(x+5,2.15)],axis='X',center=(410,2),n=32,bone=hinge,closed=True)
        screw('Bipod_HingeScrew',(x+side*5,410,2),axis='X',r=3,bone=hinge,direction=side)
        # Hollow sleeve and sliding rod: no solid-in-solid telescoping overlap.
        lathe('Bipod_Sleeve',[(419,5.05),(419,7.25),(518,7.25),(520,6.8),(520,5.05)],
            center=(x,2),n=28,closed=True,bone=bone)
        profile=[(420,0),(420,4.75)]
        for y in (449.8,475.2,500.6):
            profile.extend([(y,4.75),(y+.35,3.65),(y+1.35,3.65),(y+1.7,4.75)])
        profile.extend([(552,4.75),(552,0)])
        lathe('Bipod_Extension',profile,'bolt',ext,center=(x,2),n=20)
        lathe('Bipod_Foot',[(547,0),(547,6.8),(549,7.8),(561,9.8),
            (561.4,11.9),(563,12.4),(564.6,12.4),(566.5,11.4),(567,10.5),(567,0)],
            'rubber',ext,center=(x,2),n=24)
        lathe('Bipod_StopCollar',[(514,5.1),(514,8.4),(521,8.4),(521,5.1)],
            bone=bone,center=(x,2),n=24,closed=True)
        box('Bipod_Detent',(x-3,512,8.5),(x+3,519,11),'steel',bone,r=1)
        # Torsion return coil is attached around the hinge axis. Its two legs
        # end in the yoke and the sleeve, rather than hanging in free space.
        path=[]
        for j in range(49):
            t=math.tau*3*j/48
            path.append((x-3+6*j/48,410+9*math.cos(t),2+9*math.sin(t)))
        tube('Bipod_ReturnSpring',path,.7,'bolt',hinge,6)
        tube('Bipod_SpringTail',[(x,410,-7),(x,420,-7),(x,427,-4.2)],.7,'bolt',bone,6)
