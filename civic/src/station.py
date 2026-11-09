"""Period apparatus hall, tracked sectional doors and a shallow service bay."""
import math
from geo import Assembly,orient,text
from buildings import shell
from parts import cornice


def overhead(a,name,x,y,z,w=4.2672,h=4.2672):
    count=8;ph=h/count
    for j in range(count):
        pivot=name+'_Section_'+str(j)
        rt=a.pivot(pivot,(x,y+.07,z+j*ph),axis='X',limits=(0,90))
        rt['overhead_door']=name;rt['section_index']=j;rt['panel_pitch_m']=ph
        rt['door_width_m']=w;rt['door_height_m']=h;rt['track_radius_m']=.42
        m=a.mesh(pivot+'_Mesh',part=pivot,kind='OverheadDoorSection',trim_strip=5)
        color=(.43,.055,.028) if j>0 else (.30,.043,.025)
        if j in (4,5):
            for k in range(5):
                xx=-w/2+(k+.5)*w/5
                m.box((xx,y+.07,z+j*ph+ph/2),(w/5-.08,.015,ph-.11),'Glass')
                for side in (-1,1):m.box((xx+side*(w/10-.022),y+.07,z+j*ph+ph/2),(.044,.055,ph-.012),'Trim',color)
            for zz in (j*ph+.024,(j+1)*ph-.024):m.box((0,y+.07,z+zz),(w,.065,.048),'Trim',color)
        else:m.box((0,y+.07,z+j*ph+ph/2),(w,.07,ph-.012),'Trim',color,r=.006)
        # Skin relief belongs to normal charts; hinges/rollers change silhouette.
        for xx in (-w/2+.055,w/2-.055):
            m.tube([(xx,y+.14,z+j*ph+.04),(xx,y+.22,z+j*ph+.04)],.027,'Trim',(.42,.43,.40),sides=10)
            m.box((xx,y+.13,z+j*ph+.08),(.06,.02,.12),'Trim',(.40,.42,.39))
        for xx in (-w*.25,w*.25):m.box((xx,y+.115,z+j*ph+.07),(.055,.02,.13),'Trim',(.38,.40,.38))
        m.v=[(vx+x,vy,vz) for vx,vy,vz in m.v];m.finish()
    track=a.mesh(name+'_Tracks',kind='BayDoorTrack',trim_strip=2)
    for xx in (x-w/2-.07,x+w/2+.07):
        pts=[(xx,y+.22,z),(xx,y+.22,z+h-.25)]
        pts += [(xx,y+.64-.42*math.cos(t),z+h-.25+.42*math.sin(t)) for t in [i*math.pi/16 for i in range(1,9)]]
        pts += [(xx,y+5.1,z+h+.17)]
        track.tube(pts,.034,'Trim',(.43,.45,.43),sides=8)
    for yy in (1.1,3.9):
        track.box((x,y+yy,z+h+.31),(w+.32,.09,.09),'Trim',(.36,.38,.36))
        for xx in (x-w/2-.07,x+w/2+.07):track.beam((xx,y+yy,z+h+.31),(xx,y+yy,z+h+1.1),.035,role='Trim')
    track.finish()


def interior(a,p,x0,y0):
    from services import gear
    w=p['bayblock'];d=p['depth'];z=p['floor']
    m=a.mesh('ApparatusInterior',kind='BayInterior',trim_strip=2)
    m.box((x0+w/2,y0+d/2,z-.08),(w-.5,d-.4,.16),'Concrete',(.29,.285,.255),r=0)
    for yy in (y0+3,y0+8,y0+13,y0+17):
        m.box((x0+w/2,yy,5.55),(w-.5,.16,.28),'Trim',(.18,.20,.18))
        for xx in (x0+.45,x0+w-.45):m.box((xx,yy,2.9),(.14,.14,5.5),'Trim',(.18,.20,.18))
    for j in range(p['bays']):
        x=x0+.4572+(j+.5)*p['bay_width']
        # Exhaust duct is supported by a rail; flexible drop hangs in a slack bend.
        m.tube([(x+1.35,y0+1.8,5.6),(x+1.35,y0+15.8,5.6)],.075,'Trim',(.43,.45,.42),sides=10)
        pts=[(x+1.35,y0+5,5.55),(x+1.35,y0+5,4.7),(x+1.45,y0+5.02,3.6),(x+1.7,y0+5.2,2.1),(x+1.85,y0+5.65,.85)]
        m.tube(pts,.090,'Trim',(.66,.35,.018),sides=12)
        m.box((x+1.85,y0+5.65,.76),(.23,.23,.25),'Trim',(.025,.028,.025))
        for k in range(3):gear(a,'Gear_'+str(j)+'_'+str(k),(x-1+k*.75,y0+d-1.1,z))
    m.finish()


def tower(a,p,x,y):
    shell(a,'HoseTower',(x-1.8288,x+1.8288,y-1.8288,y+1.8288),12.8,.1524,3.6576,3,1,False,True)
    m=a.mesh('TowerPlatforms',kind='TrainingTower',trim_strip=2)
    for zz in (4.4,8.2):
        m.box((x+2.45,y,zz),(1.35,2.7,.14),'Trim',(.28,.30,.28))
        for yy in (y-1.35,y+1.35):
            m.beam((x+1.7,yy,zz-1.2),(x+3.1,yy,zz),.065,role='Trim')
            m.tube([(x+1.9,yy,zz+1.05),(x+3.05,yy,zz+1.05)],.022,'Trim',sides=8)
            for xx in (x+1.95,x+3.05):m.tube([(xx,yy,zz),(xx,yy,zz+1.05)],.022,'Trim',sides=8)
        m.tube([(x+3.05,y-1.35,zz+1.05),(x+3.05,y+1.35,zz+1.05)],.022,'Trim',sides=8)
    for xx in (x+2.8,x+3.3):m.tube([(xx,y+.6,.15),(xx,y+.6,8.8)],.023,'Trim',sides=8)
    for j in range(29):m.tube([(x+2.8,y+.6,.35+j*.29),(x+3.3,y+.6,.35+j*.29)],.018,'Trim',sides=8)
    m.finish()


def station(p):
    a=Assembly('Station_'+str(p['seed']));w,d=p['width'],p['depth'];x0=-w/2;y=-d/2;bw=p['bay_width'];z=p['floor'];top=6.0
    # Side and rear walls enclose the apparatus volume. Front has genuine openings.
    masonry=a.mesh('BayPiers',kind='ApparatusWall',brick_strip=1,weather=True,top=top)
    for j in range(p['bays']+1):
        xx=x0+.4572+j*bw
        masonry.box((xx,y+.19,(top+z)/2),(bw-4.2672,.38,top-z),'Veneer',r=0)
    masonry.box((x0+p['bayblock']/2,y+.19,5.21),(p['bayblock'],.38,1.58),'Veneer',r=0)
    masonry.box((x0+p['bayblock']/2,d/2-.17,3.0),(p['bayblock'],.34,6.0),'Veneer',r=0)
    masonry.box((x0+.17,0,3),(.34,d-.68,6),'Veneer',r=0)
    masonry.box((x0+p['bayblock']-.17,0,3),(.34,d-.68,6),'Siding',(.29,.28,.255),r=0);masonry.finish()
    for j in range(p['bays']):
        xx=x0+.4572+(j+.5)*bw
        overhead(a,'Bay_'+str(j+1),xx,y,z)
        a.socket('Apparatus_'+str(j+1),(xx,y+8,z),'apparatus')
        m=a.mesh('Bay_'+str(j+1)+'_Lintel',kind='BayLintel');m.box((xx,y-.045,4.49),(4.51,.47,.21),'Concrete');m.finish()
        text(a,'BayNumber_'+str(j+1),str(j+1),(xx,y-.04,4.88),.38,(.63,.62,.53))
    roof=a.mesh('ApparatusRoof',kind='RoofPanel');roof.box((x0+p['bayblock']/2,0,5.98),(p['bayblock']+.25,d+.25,.23),'Shingles',r=0);roof.finish()
    for side in (-1,1):
        cornice(a,'StationFascia_'+str(side),(x0+p['bayblock']/2,side*d/2,6.08),p['bayblock'],0 if side<0 else 180,True)
    if p['office']:
        shell(a,'CrewOffice',(x0+p['bayblock'],w/2,y,y+12.192),3.95,z,3.6576,p['stories'],1,True,True)
        text(a,'FireLetters','FIRE - RESCUE',(x0+p['bayblock']+p['office']/2,y-.035,3.42),.31,(.64,.64,.57))
    tower(a,p,x0+2.6,d/2+1.45);interior(a,p,x0,y)
    from services import equipment,drains
    equipment(a,(w/2-2,1,4.4));drains(a,(x0,x0+p['bayblock'],y,d/2),6.0)
    a.socket('PublicWalk',(w/2-5,y-2,.15),'walk');return a
