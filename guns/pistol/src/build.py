"""PD C9 compact: original scripted visual geometry, meters in rifle frame.

All outlines are authored parameters; reference imagery is never read here.
Internal shapes serve visible game poses, not a functional firearm design.
"""
import argparse,math,sys,json
from pathlib import Path
import bpy,bmesh
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(Path(__file__).parent))
from kit import model as M,weapon as W
from clips import build_clips

PARTS=[];MAT={};HIGH_MESHES={}
RAKE=math.tan(math.radians(22))
SLIDE_REAR=-38.0;SLIDE_FRONT=136.0;SLIDE_BOTTOM=39.5;SLIDE_TOP=66.5
BORE=53.5
HEADS={'Root':(0,0,0),'Slide':(0,-35,BORE),'Barrel':(0,127,BORE),
       'Trigger':(0,43,27),'TriggerSafety':(0,46.8,17),'SlideStop':(-13,43,31),
       'MagRelease':(0,16,10),'Magazine':(0,14.3,40.5),'Follower':(0,8.3,26.44),
       'TopRound':(0,.2,40.5),'ReserveRound':(-3.3,-2.4,31.4),'ChamberRound':(0,35,BORE),
       'Extractor':(12,26,55.5),'Takedown':(0,48,29),'RecoilGuide':(0,102,38.5)}
SOCKETS={'Socket_Muzzle':(0,137,BORE),'Socket_Foregrip':(-12,2,-1),
         'Socket_Butt':(0,-22,-15),'Socket_Eye':(0,-190,69.8),
         'Socket_Ejection':(14,22,55),'Socket_MagWell':(0,-22.7,-51),
         'Socket_Magazine':HEADS['Magazine']}

def material(name,color,metal,rough):
    m=bpy.data.materials.new(name);m.use_nodes=True
    bs=m.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
    m.diffuse_color=(*color,1)
    if name in ('CP_polymer','CP_texture'):bs.inputs['Specular IOR Level'].default_value=.22
    return m

def materials():
    # Deliberately simple checkpoint constants; no weathering or final shaders.
    for key,c,metal,r in [('nitride',(.012,.014,.017),.72,.32),
      ('polymer',(.0055,.005,.0045),0,.53),('texture',(.004,.0037,.0033),0,.77),
      ('steel',(.23,.24,.25),1,.3),('darksteel',(.022,.024,.026),.85,.4),
      ('brass',(.48,.30,.09),1,.28),('copper',(.48,.19,.09),1,.3),
      ('primer',(.35,.32,.25),1,.34),('sight',(.76,.72,.61),0,.47),
      ('follower',(.28,.055,.009),0,.6)]:MAT[key]=material('CP_'+key,c,metal,r)

def reg(ob,bone='Root',bevel=0,segments=2):
    if bevel:M.bevel(ob,bevel,segments)
    if bevel:
        mod=ob.modifiers.new('Area weighted flats','WEIGHTED_NORMAL');mod.keep_sharp=True;mod.weight=40
    M.smooth(ob,38);M.apply(ob);ob['bone']=bone;ob['asset_set']='Pistol'
    PARTS.append(ob);return ob

def box(name,lo,hi,mat='polymer',bone='Root',radius=.3,segments=2,register=True):
    lo,hi=Vector(lo),Vector(hi)
    ob=M.box(name,(lo+hi)/2,hi-lo,MAT[mat],radius=0);M.apply(ob)
    ob.data.transform(ob.matrix_world);ob.matrix_world=Matrix.Identity(4)
    if register:return reg(ob,bone,radius,segments)
    return ob

def profile(name,pts,lo,hi,mat='polymer',bone='Root',axis='X',radius=.3,segments=2,register=True):
    ob=M.profile(name,pts,lo,hi,MAT[mat],axis=axis)
    if register:return reg(ob,bone,radius,segments)
    return ob

def cut(ob,cutter,operation='DIFFERENCE'):
    mat=ob.data.materials[0] if ob.data.materials else None
    cutter.data.materials.clear()
    if mat:cutter.data.materials.append(mat)
    M.boolean(ob,cutter,operation)
    if mat:
        ob.data.materials.clear();ob.data.materials.append(mat)
        for face in ob.data.polygons:face.material_index=0
    return ob

def cutbox(ob,lo,hi):cut(ob,box('tool',lo,hi,register=False))

def lathe(name,prof,mat='steel',bone='Root',axis='Y',center=(0,0),n=64,closed=False,register=True):
    ob=M.lathe(name,prof,MAT[mat],segments=n,axis=axis,center=center,closed=closed)
    if register:return reg(ob,bone)
    return ob

def rounded(w,h,r,n=5):return M.rounded_rectangle(w,h,r,n)

def grip_loop(z,y,hw,hd,n=48):
    pts=[]
    for i in range(n):
        t=math.tau*i/n;c=math.cos(t);s=math.sin(t)
        p=3.2 if c<0 else 2.8
        x=hw*math.copysign(abs(s)**(2/p),s)
        yy=hd*math.copysign(abs(c)**(2/p),c)
        x*=1-.08*max(0,c)**6
        pts.append((x,y+yy,z))
    return pts

# Horizontal ergonomic sections. Center-line rake is exactly 22 degrees over
# the middle grip; extra rear volume creates the palm/backstrap swell.
def grip_center(z):return 1.2+(z-8)*RAKE
def mag_center(z):return 14.3+(z-40.5)*RAKE
GRIP=[(z,grip_center(max(-51,z)),hw,hd) for z,hw,hd in
 [(-52.8,15.3,24.3),(-52.2,15.8,24.8),(-51,16.0,24.98),(-49,15.8,24.96),(-44,15.2,25.0),(-36,15.1,25.6),
  (-28,15.2,25.8),(-20,15.1,25.3),(-12,14.9,24.8),(-4,14.6,24.0),
  (4,14.3,23.7),(12,14.0,23.6),(20,13.7,25.4),(26,13.3,28.0),
  (31,12.9,29.5),(35,12.6,30.0)]]

def grip():
    g=M.loft('Frame_Grip',[grip_loop(*row,n=64) for row in GRIP],MAT['polymer'])
    reg(g)
    return g

def magwell_loop(z,hw=10.9,hd=18.4):
    return [(x,mag_center(z)+y,z) for x,y in rounded(hw*2,hd*2,2.6,7)]

def frame():
    from frame_form import sculpt
    g=next(o for o in PARTS if o.name=='Frame_Grip')
    sculpt(g,MAT['polymer'],grip_center,magwell_loop,grip_loop)
    normal_source=g.copy();normal_source.data=g.data.copy();bpy.context.collection.objects.link(normal_source)
    HIGH_MESHES[g.name]=g.data.copy()
    dec=g.modifiers.new('First person sculpt budget','DECIMATE')
    dec.ratio=9600/sum(len(f.vertices)-2 for f in g.data.polygons);M.apply(g)
    transfer=g.modifiers.new('Sculpted normal field','DATA_TRANSFER');transfer.object=normal_source
    transfer.use_loop_data=True;transfer.data_types_loops={'CUSTOM_NORMAL'};transfer.loop_mapping='POLYINTERP_NEAREST';M.apply(g)
    bpy.data.objects.remove(normal_source,do_unlink=True)
    for side in (-1,1):
        for y in (-22,73):
            x=side*10.3
            box('Frame_RailInsert',(x-.6,y-4,36.6),(x+.6,y+4,39.25),'steel',radius=.18)
    # The accessory rail's undercuts and transverse slot are molded into the
    # dense frame by frame_form, then baked. There are no attached side plates.
    # Pins remain silhouette/installation geometry; shallow marks move to bake.
    for y,z,r in [(48,35,1.4),(-17,31,1.25)]:
        for side in (-1,1):
            x=side*13.0
            lathe('Frame_Pin',[(x,0),(x,r),(x+side*.25,r),(x+side*.25,0)],'darksteel',axis='X',center=(y,z),n=16)

def slide():
    sec=rounded(25.5,27,2.0,8)
    loops=[]
    for y,inset in [(-38,.5),(-37.4,0),(132,0),(136,1.1)]:
        loops.append([(x*(25.5-2*inset)/25.5,y,53+z*(27-2*inset)/27) for x,z in sec])
    s=M.loft('Slide_Shell',loops,MAT['nitride'])
    cutbox(s,(-10.8,-36.4,35),(10.8,129.2,64.9))
    port=M.fillet_polygon([(33,48.5),(33,69),(65,69),(68,64.5),(68,48.5)],1.0,segments=5)
    cut(s,profile('tool',port,-9.2,18,register=False))
    opening=lathe('tool',[(128,0),(128,8.3),(140,8.3),(140,0)],center=(0,BORE),n=56,register=False)
    opening.data.transform(Matrix.Translation((0,0,BORE))@Matrix.Diagonal((1,1,1.15,1))@Matrix.Translation((0,0,-BORE)))
    cut(s,opening)
    cut(s,lathe('tool',[(128,0),(128,2.9),(139,2.9),(139,0)],center=(0,38.5),n=32,register=False))
    # Small radii on port/nose; the 2 mm section radii carry broad shoulder highlights.
    M.bevel(s,.45,3);M.apply(s)
    # Original diagonal channels stay entirely on the flat side. Rounded capsule
    # ends do not cut a row of teeth into the curved shoulder.
    for side in (-1,1):
        for y in [*range(-30,1,3),*range(90,121,3)]:
            points=M.fillet_polygon([(y-.58,41.7),(y+.58,41.7),(y+2.55,66.8),(y+1.39,66.8)],.52,segments=4)
            x0,x1=sorted((side*11.75,side*15))
            cut(s,profile('tool',points,x0,x1,register=False))
    # The cover is flush in a closed shallow rear seat, with a narrow perimeter.
    cover_section=[(x,z+51.8) for x,z in rounded(18.0,17.3,1.5,6)]
    cut(s,profile('tool',cover_section,-39,-36.9,axis='Y',register=False))
    cutbox(s,(11.1,20,51),(15,33.2,59))
    # The lock notch is visible and exposes a real rear engagement face.
    cut(s,profile('tool',[(46.05,39),(52.5,39),(52.5,43.4),(47,43.4),(47,41.3),(46.05,39.5)],-15,-10.65,register=False))
    # Actual transverse undercut dovetails, not rectangular slots.
    for yc in (-28,124):
        dovetail=[(yc-3.1,65.05),(yc+3.1,65.05),(yc+2.25,67.0),(yc-2.25,67.0)]
        cut(s,profile('tool',dovetail,-15,15,register=False))
    reg(s,'Slide',bevel=.16,segments=2)
    dec=s.modifiers.new('Slide planar detail budget','DECIMATE');dec.ratio=9000/sum(len(f.vertices)-2 for f in s.data.polygons);M.apply(s)
    s.data.normals_split_custom_set([(0,0,0)]*len(s.data.loops));M.smooth(s,38)
    wn=s.modifiers.new('Slide area normals','WEIGHTED_NORMAL');wn.keep_sharp=True;M.apply(s)
    plate=profile('Slide_StrikerCover',[(x,z+51.8) for x,z in rounded(17.8,17.1,1.4,6)],
                  -38,-37.0,'darksteel','Slide',axis='Y',radius=.13,segments=3)
    # Solid breech wall in the open port; fine face marks belong in the normal map.
    b=box('Slide_BreechFace',(-9,30.5,46.2),(9,33,60.5),'darksteel','Slide',radius=.3)
    profile('Extractor',[(21.5,51.3),(32.7,51.3),(33.3,53.5),(32.5,58.2),(22,58.2)],
            11.3,12.8,'darksteel','Extractor',radius=.35,segments=3)
    for yc,front in [(-28,False),(124,True)]:
        foot=[(yc-3.0,65.15),(yc+3.0,65.15),(yc+2.22,66.95),(yc-2.22,66.95)]
        profile('Sight_Dovetail',foot,-12.35,12.35,'darksteel','Slide',radius=.12,segments=2)
        if front:
            box('Sight_Front',(-1.6,yc-2.4,66.5),(1.6,yc+2.4,72.0),'nitride','Slide',radius=.5,segments=4)
            lathe('Sight_FrontDot',[(yc-2.45,0),(yc-2.45,.78),(yc-2.35,.78),(yc-2.35,0)],
                  'sight','Slide',center=(0,69.8),n=16)
        else:
            rear=profile('Sight_Rear',M.fillet_polygon([(-8.9,66.5),(8.9,66.5),(8.1,72),(-8.1,72)],.5,5),
                         yc-2.8,yc+2.8,'darksteel','Slide',axis='Y',register=False)
            notch=[(x,z+70.8) for x,z in rounded(3.8,4.6,.32,5)]
            cut(rear,profile('tool',notch,yc-4,yc+4,axis='Y',register=False))
            reg(rear,'Slide',bevel=.22,segments=3)

def barrel():
    # Short, inexpensive deep bore. The crown receives the visible radial detail.
    outer=[(35,7.5),(64,7.5),(66,7.2),(135.1,7.2),(137,6.85),(137,5.35),(136.2,4.55)]
    inner=[(127,4.5),(55,4.5),(35,4.9)]
    b=lathe('Barrel_Tube',outer+inner,'darksteel','Barrel',center=(0,BORE),n=32,closed=True)
    h=box('Barrel_Hood',(-8.6,35,45.5),(10.5,65.5,65.75),'steel','Barrel',register=False)
    cut(h,lathe('tool',[(33,0),(33,4.9),(68,4.9),(68,0)],center=(0,BORE),n=32,register=False))
    cutbox(h,(-10,60,43),(10,67,49.9))
    for owner in (h,b):
        cut(owner,lathe('tool',[(55,0),(55,1.15),(69,1.15),(69,0)],axis='Z',center=(0,36),n=16,register=False))
    M.smooth(b,40);M.bevel(b,.13,2);M.apply(b);reg(h,'Barrel',bevel=.45,segments=2)
    profile('Barrel_LockingFoot',[(38,45.5),(52,45.5),(51,39),(47,37),(42,37),(39,40)],
            -4.2,4.2,'darksteel','Barrel',radius=.65,segments=3)
    # Only the first few visible lands remain geometry; fine/deep bore detail is baked later.
    for k in range(6):
        path=[]
        for i in range(5):
            y=130+i*6/4;t=math.tau*k/6+(y-130)*.02
            path.append((4.53*math.cos(t),y,BORE+4.53*math.sin(t)))
        reg(M.tube('Crown_Land',path,.09,MAT['darksteel'],sides=4),'Barrel')
    # Visible, supported guide assembly: a telescoping representation, not a spring simulation.
    lathe('Recoil_GuideRear',[(56,0),(56,1.5),(94,1.5),(94,0)],'darksteel','Root',center=(0,38.5),n=20)
    lathe('Recoil_GuideFront',[(86,1.6),(86,2.1),(134.4,2.1),(134.4,2.8),(135.5,2.4),(135.5,0),(133.8,0),(133.8,1.6)],
          'darksteel','Slide',center=(0,38.5),n=24,closed=True)
    # A coarse original wound surface reads as the recoil spring in an open action.
    path=[]
    for i in range(129):
        t=math.tau*12*i/128;y=74+42.1*i/128
        path.append((2.48*math.cos(t),y,38.5+2.48*math.sin(t)))
    reg(M.tube('Recoil_Spring',path,.30,MAT['steel'],sides=4),'RecoilGuide')

def trigger():
    # +Y is the muzzle: the working face hollows rearward at mid-height,
    # then the toe curls FORWARD. Broad 7 mm blade, radiused lateral edges.
    front=([(44.8,27.5),(55.0,27.5),(55.0,26.3)]
           +M.bezier((55.0,26.3),(51.5,26.3),(49.2,25),(49.2,23),4)[1:]
           +M.bezier((49.2,23),(45.8,17),(46.5,9),(50.0,3.5),12)[1:])
    back=(M.bezier((47.6,3.5),(42.9,11),(42.3,18),(45.0,23),12)
          +M.bezier((45.0,23),(44,24.8),(42,25.6),(40.2,26),4)[1:])
    toe=M.bezier((50.0,3.5),(50.8,2.3),(49.4,2.0),(47.6,3.5),6)
    tr=profile('Trigger_Shoe',front+toe[1:]+back[1:],-3.5,3.5,'polymer','Trigger',register=False)
    # The hidden upper land meets the existing slot end at rest; pulling
    # rotates it away from that stop without changing the frame or pivot.
    # A curved pocket leaves a continuous rear web, including behind the
    # depressed blade. It opens through the muzzle-facing surface only.
    pocket=M.bezier((46.5,24.5),(42.0,18),(44.0,10),(47.0,6.0),12)
    cut(tr,profile('tool',pocket+[(55,6),(55,24.5)],-.92,.92,register=False))
    reg(tr,'Trigger',bevel=.48,segments=2)
    face=M.bezier((49.4,22),(47.1,17),(47.7,12),(49.4,7),10)
    # The hidden hinge land reaches the unchanged safety pivot at Y46.8/Z17.
    backface=[(y-.9-1.7*math.exp(-((z-17)/2.6)**2),z) for y,z in reversed(face)]
    safety=profile('Trigger_SafetyBlade',face+backface,-.63,.63,'darksteel','TriggerSafety',register=False)
    cut(safety,lathe('tool',[(-2,0),(-2,.60),(2,.60),(2,0)],axis='X',center=(46.8,17),n=16,register=False))
    reg(safety,'TriggerSafety',bevel=.16,segments=2)
    lathe('Trigger_SafetyPivot',[(-3.5,0),(-3.5,.45),(3.5,.45),(3.5,0)],'darksteel','Trigger',axis='X',center=(46.8,17),n=12)
def controls():
    trigger()
    # A thin stamping bends along the flank; the thumb pad stands proud.
    outline=M.fillet_polygon([(4,30.2),(17,30.4),(17,33.6),(13,35.1),(4,34.2)],.8,5)
    st=profile('SlideStop_Lever',outline,-15.9,-14.9,'darksteel','SlideStop',register=False)
    for v in st.data.vertices:v.co.x+=.24*math.sin((v.co.y-4)/13*math.pi)
    for z in (31.1,32.2,33.3):
        cutbox(st,(-16.2,4.8,z),(-15.67,15.8,z+.38))
    reg(st,'SlideStop',bevel=.16,segments=2)
    arm=profile('SlideStop_Arm',[(11,30.2),(43,29.8),(43,31.2),(13,32.2)],-13.7,-12.9,'darksteel','SlideStop',register=False)
    for v in arm.data.vertices:v.co.x+=.8+.28*math.sin((v.co.y-11)/32*math.pi)
    reg(arm,'SlideStop',bevel=.16,segments=2)
    box('SlideStop_BentBridge',(-15.1,13.8,31.2),(-12.6,16.2,32.1),'darksteel','SlideStop',radius=.15,segments=2)
    # Author the lug in the LOCKED pose so its rear face meets the actual notch.
    lug=box('SlideStop_Lug',(-13.8,13,36.8),(-10.9,16.0,41.5),'darksteel','SlideStop',radius=.12,segments=2)
    pivot=Vector(HEADS['SlideStop']);lug.data.transform(Matrix.Translation(pivot)@Matrix.Rotation(math.radians(7),4,'X')@Matrix.Translation(-pivot))
    mr=profile('MagRelease_Button',M.fillet_polygon([(12,4),(21,4),(21,16),(12,16)],.8,6),
               -15.2,-14.2,'polymer','MagRelease',radius=.35,segments=2)
    for side in (-1,1):
        x0,x1=sorted((side*14.1,side*14.9))
        profile('Takedown_Tab',M.fillet_polygon([(45,28.7),(50.7,29.0),(50.7,32.7),(45,32.4)],.55,4),
                x0,x1,'darksteel','Takedown',radius=.2,segments=2)

def magazine():
    loops=[]
    for z,hw,hd in [(-53.2,10.2,17.5),(-51,10.0,17.4),(21,9.8,17),(30,9.2,16.8),(39.2,7.25,16.4)]:
        loops.append([(x,mag_center(z)+y,z-(3.2*y/hd if z==39.2 else 0))
                      for x,y in rounded(hw*2,hd*2,2.4,7)])
    mag=M.loft('Magazine_Body',loops,MAT['polymer'])
    inner=[]
    for z,hw,hd in [(-50.5,8.7,16.2),(29,8.5,16.1),(34,8.5,16.1),(39.2,6.55,15.7),(48,6.55,15.7)]:
        inner.append([(x,mag_center(z)+y,z) for x,y in rounded(hw*2,hd*2,1.7,7)])
    cut(mag,M.loft('tool',inner,None))
    # The rear spine stands above the front wall. Each hole goes through the
    # spine's actual gauge, rather than being a dark disk on its surface.
    for z in (-36,-23,-10,3,16):
        rear=mag_center(z)-17.0
        cut(mag,lathe('tool',[(rear-4,0),(rear-4,1.25),(rear+4,1.25),(rear+4,0)],
                       axis='Y',center=(0,z),n=12,register=False))
    notch=[(x,z+42.8) for x,z in rounded(8.4,10.0,2.2,7)]
    cut(mag,profile('tool',notch,-9,.35,axis='Y',register=False))
    reg(mag,'Magazine',bevel=.20,segments=2)
    for side in (-1,1):
        # Thin curled steel lips continue the body's side walls. The retaining
        # edge follows the accepted cartridge rather than capping it with a block.
        theta=math.acos(3.6/4.99)
        innerarc=[(4.99*math.cos(theta*j/12),40.5+4.99*math.sin(theta*j/12)) for j in range(13)]
        outerarc=[((4.99+.65)*math.cos(theta*j/12),40.5+(4.99+.65)*math.sin(theta*j/12)) for j in range(13)]
        pts=[(7.25,36.2),(7.25,38.4),*outerarc,*reversed(innerarc),(6.55,37.8),(6.55,36.2)]
        profile('Magazine_FeedLip',[(side*x,z) for x,z in pts],.4,17.8,'darksteel','Magazine',axis='Y',radius=.10,segments=2)
    yc=mag_center(-53)
    plate=[(x,y+yc+.7) for x,y in rounded(27.2,40.5,3.5,7)]
    profile('Magazine_Floorplate',plate,-56,-52.7,'polymer','Magazine',axis='Z',radius=.35,segments=2)
    box('Magazine_Follower',(-6.5,-3.2,24.04),(6.5,19.8,26.44),'follower','Follower',radius=.6,segments=3)
    cartridge('Magazine_TopRound',(0,.2,40.5),'TopRound',n=20)
    cartridge('Magazine_SecondRound',(-3.3,-3.0,31.4),'ReserveRound',n=14)
    cartridge('ChamberRound',(0,35,BORE),'ChamberRound',n=16)

def cartridge(name,base,bone,fired=False,n=20):
    x,y,z=base
    if fired:
        # A repeated-object mesh: 12-sided silhouette, actual thin open mouth,
        # primer seat and struck cup; fine extractor/soot detail belongs in bake.
        case=[(0,1.8),(0,4.96),(1.1,4.96),(1.1,4.15),(2.1,4.15),(2.1,4.91),
              (18.7,4.74),(19.15,4.72),(19.15,4.35),(1.6,4.35),(1.6,1.8),(.3,1.8)]
        ob=lathe(name+'_Case',[(y+h,r) for h,r in case],'brass',bone,center=(x,z),n=12,closed=True)
        primer=[(.09,0),(.09,.22),(-.01,.55),(-.01,1.75),(.14,1.75),(.14,0)]
        lathe(name+'_Primer',[(y+h,r) for h,r in primer],'primer',bone,center=(x,z),n=12)
    else:
        case=[(0,1.8),(0,4.96),(1.1,4.96),(1.3,4.15),(2.1,4.15),(2.4,4.91),(19.15,4.72),(19.15,0)]
        lathe(name+'_Case',[(y+h,r) for h,r in case],'brass',bone,center=(x,z),n=n)
        lathe(name+'_Primer',[(y-.01,0),(y-.01,1.7),(y+.08,1.7),(y+.08,0)],'primer',bone,center=(x,z),n=12)
        prof=[(18.8,0),(18.8,4.5),(23,4.5),(25.3,3.9),(27.5,2.7),(29.5,0)]
        lathe(name+'_Bullet',[(y+h,r) for h,r in prof],'copper',bone,center=(x,z),n=n)

def finish_normals(ob):
    # The bent stamping's Boolean caps can leave nanometer-wide duplicate
    # strips. Weld/dissolve those in millimeter modeling space before export
    # precision changes their winding. Preserve the authored corner field.
    if ob.name=='SlideStop_Lever':
        saved=ob.data.attributes.new('Pre-clean normals','FLOAT_VECTOR','CORNER')
        for row,n in zip(saved.data,ob.data.corner_normals):row.vector=n.vector
        bm=bmesh.new();bm.from_mesh(ob.data)
        bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.002)
        bmesh.ops.dissolve_degenerate(bm,dist=.002,edges=list(bm.edges))
        bm.to_mesh(ob.data);bm.free()
        ob.data.normals_split_custom_set([row.vector[:] for row in ob.data.attributes['Pre-clean normals'].data])
        ob.data.attributes.remove(ob.data.attributes['Pre-clean normals'])
    # Keep the continuous high mold field, but never transfer a neighboring
    # cavity's inward normal across a thin wall. Repair only opposing corners
    # using their actual finalized triangle normal, before export.
    tri=ob.modifiers.new('Final triangulation','TRIANGULATE');tri.keep_custom_normals=True;M.apply(ob)
    normals=[n.vector.copy() for n in ob.data.corner_normals];fixed=0
    for face in ob.data.polygons:
        for j in face.loop_indices:
            if normals[j].dot(face.normal)<.05:
                normals[j]=face.normal.copy();fixed+=1
    ob.data.normals_split_custom_set(normals)
    if fixed:print('NORMAL CORNERS REPAIRED',ob.name,fixed,flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='build/pistol.blend');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True);materials()
    grip();frame();slide();barrel();controls();magazine()
    # All modeling happens in mm for stable boolean cuts. Final data is meters.
    for ob in PARTS:
        finish_normals(ob)
        ob.data.transform(Matrix.Scale(.001,4));ob.matrix_world=Matrix.Identity(4)
    heads={k:tuple(v*.001 for v in pos) for k,pos in HEADS.items()}
    arm=W.armature('PistolArmature',heads,parents={'TriggerSafety':'Trigger','Extractor':'Slide',
                        'Follower':'Magazine','TopRound':'Magazine','ReserveRound':'Magazine','ChamberRound':'Barrel'})
    for ob in PARTS:W.rigid_bind(ob,arm,ob['bone'])
    sockets=W.sockets(arm,{k:tuple(v*.001 for v in pos) for k,pos in SOCKETS.items()}, {'Socket_Magazine':'Magazine'})
    build_clips(arm)
    scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
    scene['stage']='FORM CHECKPOINT: unbaked constants, no delivery textures'
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    low_data={name:bpy.data.objects[name].data for name in HIGH_MESHES}
    for name,mesh in HIGH_MESHES.items():
        mesh.transform(Matrix.Scale(.001,4));ob=bpy.data.objects[name];ob.data=mesh
        ob.vertex_groups.clear();vg=ob.vertex_groups.new(name=ob['bone']);vg.add(list(range(len(mesh.vertices))),1,'REPLACE')
    bpy.ops.wm.save_as_mainfile(filepath=str(out.parent/'sculpt.blend'))
    for name,mesh in low_data.items():
        ob=bpy.data.objects[name];ob.data=mesh
        ob.vertex_groups.clear();vg=ob.vertex_groups.new(name=ob['bone']);vg.add(list(range(len(mesh.vertices))),1,'REPLACE')
    # Inspection GLBs prove rig/clip/socket serialization; no claim of final delivery.
    joined=W.joined_copy(PARTS,'Pistol');joined.parent=arm
    mod=joined.modifiers.new('Weapon skin','ARMATURE');mod.object=arm
    W.export(out.with_suffix('.glb'),[arm,joined]+sockets)
    bpy.data.objects.remove(joined,do_unlink=True)
    magparts=[o for o in PARTS if o['bone'] in ('Magazine','TopRound','Follower','ReserveRound')]
    for filename,clip,pose_frame in [('magazine_loaded.glb','Idle',0),('magazine_empty.glb','IdleOpen',0)]:
        W.pose(arm,clip,pose_frame)
        mag=W.detachable(magparts,arm,'Magazine','Magazine')
        W.export(out.parent/filename,[mag],animations=False);bpy.data.objects.remove(mag,do_unlink=True)
    W.pose(arm,None,0)
    # Fired-case standalone never contributes to the pistol's geometry budget.
    old=list(PARTS);cartridge('FiredCase',(0,0,0),'Root',True)
    cases=[o for o in PARTS if o not in old]
    for ob in cases:
        finish_normals(ob)
        ob.data.normals_split_custom_set([(0,0,0)]*len(ob.data.loops));M.smooth(ob,35)
        ob.data.transform(Matrix.Scale(.001,4))
    case=W.joined_copy(cases,'FiredCase');case.parent=None
    # Analytic revolved normals keep the cheap 12-sided body optically round.
    # Annular faces stay flat; inner wall normals point into the mouth.
    normals=[n.vector.copy() for n in case.data.corner_normals]
    for f in case.data.polygons:
        radial=math.hypot(f.normal.x,f.normal.z)
        for j in f.loop_indices:
            p=case.data.vertices[case.data.loops[j].vertex_index].co
            r=math.hypot(p.x,p.z)
            if abs(f.normal.y)>.5 or r<1e-8 or radial<1e-8:normals[j]=f.normal.copy()
            else:
                sign=1 if f.normal.x*p.x+f.normal.z*p.z>0 else -1
                normals[j]=Vector((sign*p.x/r,f.normal.y/radial,sign*p.z/r)).normalized()
    case.data.normals_split_custom_set(normals)
    W.export(out.parent/'case.glb',[case],animations=False)
    counts={o.name:sum(len(f.vertices)-2 for f in o.data.polygons) for o in old}
    (out.parent/'triangles.json').write_text(json.dumps({'total':sum(counts.values()),'parts':counts},indent=2))
    print('PISTOL TRIANGLES',sum(counts.values()),flush=True)
if __name__=='__main__':main()
