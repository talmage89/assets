"""Civic modules: bearing masonry, sash, Tuscan order and real door leaves."""
import math
from geo import orient,text


def window(a,name,p,w=1.3716,h=2.4384,yaw=0,modern=False):
    m=a.mesh(name,kind='AluminumWindow' if modern else 'TallSash',trim_strip=2 if modern else 5)
    for s in (-1,1):
        m.box((s*(w/2+.07),.10,h/2),(.14,.18,h+.18),'Concrete')
        m.box((s*(w/2-.042),.044,h/2),(.084,.09,h),'Trim',(.33,.35,.33) if modern else (.66,.65,.59))
    for z in (.045,h-.045):m.box((0,.044,z),(w-.08,.09,.09),'Trim',(.35,.36,.34) if modern else (.66,.65,.59))
    m.box((0,-.04,-.075),(w+.40,.38,.15),'Concrete')
    m.box((0,.10,h+.10),(w+.38,.25,.20),'Concrete')
    m.box((0,.11,h/2),(w-.15,.008,h-.16),'Glass')
    # Deep dim room and varied blind heights give parallax beyond reflections.
    m.box((0,.74,h/2),(w,.025,h),'Trim',(.024,.027,.020))
    blind=h*(.18+.18*((sum(map(ord,name))%5)/4))
    m.box((0,.20,h-blind/2-.06),(w-.17,.018,blind),'Trim',(.31,.295,.245))
    m.box((0,.022,h*.49),(w-.09,.065,.085),'Trim',(.54,.53,.48))
    if not modern:
        for s in (-1,1):m.box((s*w/6,.018,h/2),(.024,.040,h-.13),'Trim',(.60,.59,.53),r=0)
        for j in (1,2,4,5):m.box((0,.016,h*j/6),(w-.10,.045,.025),'Trim',(.60,.59,.53),r=0)
    orient(m,p,yaw);ob=m.finish()
    # Switchable dim room layer sits behind the blinds and real glazing.
    import bpy
    ma=bpy.data.materials.get('CivicRoomGlow')
    if not ma:
        ma=bpy.data.materials.new('CivicRoomGlow');ma.use_nodes=True;ma['switch_kind']='interior_lights';ma['tiling_vertex_tint']=False
        bs=ma.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.055,.040,.021,1);bs.inputs['Emission Color'].default_value=(1,.68,.32,1);bs.inputs['Emission Strength'].default_value=.055
    glow=a.mesh(name+'_RoomLayer',kind='SwitchableRoomLayer')
    glow.box((0,.70,h/2),(w-.20,.008,h-.20),'Glass');orient(glow,p,yaw);gg=glow.finish();gg.data.materials.clear();gg.data.materials.append(ma)
    for f in gg.data.polygons:f.material_index=0
    return ob


def wall_bay(a,name,p,width,height,sill=.92,opening=1.3716,window_h=2.4384,yaw=0,brick=0,modern=False):
    m=a.mesh(name,kind='WallBay',brick_strip=brick,weather=True,top=p[2]+height)
    half=(width-opening)/2
    for s in (-1,1):m.box((s*(opening+half)/2,.17,height/2),(half,.34,height),'Veneer',r=0)
    if sill:m.box((0,.17,sill/2),(opening,.34,sill),'Veneer',r=0)
    head=sill+window_h
    if height>head:m.box((0,.17,(height+head)/2),(opening,.34,height-head),'Veneer',r=0)
    orient(m,p,yaw);ob=m.finish()
    window(a,name+'_Sash',(p[0]-sill*0,p[1],p[2]+sill),opening,window_h,yaw,modern)
    return ob


def cornice(a,name,p,length,yaw=0,plain=False):
    m=a.mesh(name,kind='CorniceRun',weather=True,top=p[2]+.75)
    courses=((0,.43,.24),(.15,.48,.06)) if plain else ((0,.32,.12),(.16,.44,.14),(.33,.63,.17),(.47,.76,.10),(.57,.58,.10))
    for z,depth,h in courses:
        m.box((0,-depth/2+.14,z),(length,depth,h),'Concrete',r=.007)
    if not plain:
        n=max(1,round(length/.30))
        for j in range(n):m.box((-length/2+(j+.5)*length/n,-.25,.23),(.12,.24,.14),'Concrete',r=.002)
    orient(m,p,yaw);return m.finish()


def column(a,name,p,height=5.0292,diameter=.6096,pilaster=False):
    m=a.mesh(name,kind='Pilaster' if pilaster else 'TuscanColumn',stone_strip=0)
    if pilaster:m.box((0,0,height/2),(diameter,.24,height),'Concrete')
    else:
        levels=[(0,.62),(.10,.62),(.16,.54),(.22,.50),(.30,.49),(.38,.48),(.55,.465),(height*.35,.458),(height*.65,.422),(height-.36,.385),(height-.28,.385),(height-.23,.44),(height-.16,.47),(height-.10,.48)]
        vs=[];n=24
        for z,r in levels:
            for j in range(n):vs.append((math.cos(j*math.tau/n)*r*diameter,math.sin(j*math.tau/n)*r*diameter,z))
        fs=[tuple(reversed(range(n))),tuple(range(len(vs)-n,len(vs)))]
        fs += [(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(levels)-1) for i in range(n)]
        m.geom(vs,fs,'Concrete')
    for z in (.05,height-.05):m.box((0,0,z),(diameter*1.3,diameter*1.3,.10),'Concrete',r=.004)
    orient(m,p,0);ob=m.finish()
    if not pilaster:
        for f in ob.data.polygons:
            if abs(f.normal.z)<.3:f.use_smooth=True
    return ob


def front_door(a,name,p,width=.9652,height=2.4384,yaw=0):
    m=a.mesh(name+'_Frame',kind='EntryFrame',trim_strip=2)
    for s in (-1,1):
        if name.endswith('_DoorR') and s==-1:continue
        m.box((s*(width/2+.045),.08,height/2),(.09,.18,height+.12),'Concrete')
    m.box((0,.08,height+.05),(width+.18,.18,.10),'Concrete')
    orient(m,p,yaw);m.finish()
    rad=math.radians(yaw);width-=.010
    hinge=(p[0]-width/2*math.cos(rad)-.115*math.sin(rad),p[1]-width/2*math.sin(rad)+.115*math.cos(rad),p[2])
    a.pivot(name,hinge,limits=(0,90))
    leaf=a.mesh(name+'_Leaf',part=name,kind='FrontDoor',trim_strip=2)
    for s in (-1,1):leaf.box((s*(width/2-.045),.08,height/2),(.09,.055,height),'Trim',(.095,.115,.105))
    for z in (.11,.72,height-.07):leaf.box((0,.08,z),(width-.15,.055,.13),'Trim',(.095,.115,.105))
    leaf.box((0,.08,height*.65),(width-.18,.012,height*.50),'Glass')
    leaf.box((0,.08,.40),(width-.17,.055,.52),'Trim',(.10,.12,.11))
    leaf.box((width*.29,.018,1.02),(.034,.040,.28),'Trim',(.45,.47,.44))
    leaf.box((0,.043,.12),(width-.19,.006,.15),'Trim',(.43,.45,.43))
    orient(leaf,p,yaw);leaf.finish();a.socket(name+'_Threshold',p,'door')


def steps(a,p,width=8.6,count=6,rise=.1524,going=.3302):
    m=a.mesh('EntryStoneStair',kind='StoneStair',weather=True)
    for j in range(count):
        y=-going*(count-j-.5)
        m.box((0,y,(j+1)*rise/2),(width,going-.006,(j+1)*rise),'Concrete',r=.006)
    for s in (-1,1):
        m.box((s*(width/2+.20),-count*going/2,count*rise/2),(.4,count*going,count*rise),'Concrete')
        m.box((s*(width/2+.20),-count*going/2,count*rise+.055),(.47,count*going+.08,.11),'Concrete')
    orient(m,p,0);m.finish()
    rail=a.mesh('StairHandrails',kind='Handrail',trim_strip=2)
    for x in (-width/2+.16,0,width/2-.16):
        pts=[(x,-count*going-.30,.88),(x,-count*going,.88),(x,-.05,count*rise+.88),(x,.25,count*rise+.88)]
        rail.tube(pts,.021,'Trim',(.045,.050,.044),sides=8)
        for j in (0,2,4):rail.tube([(x,-count*going+j*going,j*rise),(x,-count*going+j*going,j*rise+.88)],.019,'Trim',sides=8)
    orient(rail,p,0);return rail.finish()
