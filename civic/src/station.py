"""Period apparatus hall, tracked sectional doors and a shallow service bay."""
import math
from geo import Assembly,orient,text
from buildings import shell
from parts import cornice


def overhead(a,name,x,y,z,w=4.2672,h=4.2672):
    # Door and tracks sit behind the masonry's inner return, so a rising
    # section can pass the actual lintel rather than crossing through it.
    y+=.38
    nominal_width=w;w-=.014;count=8;ph=h/count
    for j in range(count):
        pivot=name+'_Section_'+str(j)
        rt=a.pivot(pivot,(x,y+.24,z+j*ph+.018),axis='X',limits=(-90,0))
        rt['overhead_door']=name;rt['section_index']=j;rt['panel_pitch_m']=ph
        rt['door_width_m']=nominal_width;rt['door_height_m']=h;rt['track_radius_m']=.42
        rt['open_translation_m']=(0,.42+j*ph,h+.52-j*ph);rt['open_rotation_x_degrees']=-90
        m=a.mesh(pivot+'_Mesh',part=pivot,kind='OverheadDoorSection',trim_strip=5)
        color=(.43,.055,.028) if j>0 else (.30,.043,.025)
        if j in (4,5):
            m.box((0,y+.07,z+j*ph+ph/2),(w-.08,.015,ph-.11),'Glass',r=0)
            for k in range(6):
                xx=-w/2+.022+k*(w-.044)/5
                m.box((xx,y+.07,z+j*ph+ph/2),(.044,.055,ph-.012),'Trim',color,r=0)
            for zz in (j*ph+.024,(j+1)*ph-.024):m.box((0,y+.07,z+zz),(w,.065,.048),'Trim',color,r=0)
        elif j<2:
            # Gauged steel panel, with shallow localized impact dents in the
            # bottom two sections. The edge/roller envelope remains unchanged.
            nx=8;ny=2;vs=[]
            for back in (False,True):
                for row in range(ny+1):
                    for col in range(nx+1):
                        u=col/nx;v=row/ny
                        dent=.018*math.sin(u*math.pi)**4*math.exp(-((u-.32-.13*j)/.14)**2)*math.sin(v*math.pi)**2
                        vs.append(((u-.5)*w,y+.105 if back else y+.035+dent,z+j*ph+.006+v*(ph-.012)))
            fs=[];offset=(nx+1)*(ny+1)
            for row in range(ny):
                for col in range(nx):
                    k=row*(nx+1)+col;face=(k,k+1,k+nx+2,k+nx+1);fs.extend([face,tuple(i+offset for i in reversed(face))])
            border=list(range(nx+1))+[row*(nx+1)+nx for row in range(1,ny+1)]+[ny*(nx+1)+col for col in range(nx-1,-1,-1)]+[row*(nx+1) for row in range(ny-1,0,-1)]
            fs += [(aa,bb,bb+offset,aa+offset) for aa,bb in zip(border,border[1:]+border[:1])]
            m.geom(vs,fs,'Trim',color)
        else:m.box((0,y+.07,z+j*ph+ph/2),(w,.07,ph-.012),'Trim',color,r=.006)
        # Skin relief belongs to normal charts; hinges/rollers change silhouette.
        for xx in (-w/2+.055,w/2-.055):
            m.tube([(xx-.04,y+.20,z+j*ph+.04),(xx+.04,y+.20,z+j*ph+.04)],.027,'Trim',(.42,.43,.40),sides=8)
            m.box((xx,y+.17,z+j*ph+.08),(.06,.14,.12),'Trim',(.40,.42,.39),r=0)
            m.tube([(xx-.04,y+.24,z+j*ph+.018),(xx+.04,y+.24,z+j*ph+.018)],.012,'Trim',(.38,.40,.38),sides=6)
        m.v=[(vx+x,vy,vz) for vx,vy,vz in m.v];ob=m.finish()
        tint=ob.data.color_attributes['Tint']
        for loop in ob.data.loops:
            q=ob.data.vertices[loop.vertex_index].co;fac=.84+.14*math.sin((q.x+x)*.66+j*.43)**2
            c=tint.data[loop.index].color;tint.data[loop.index].color=(*(c[i]*fac+(.038,.019,.014)[i]*(1-fac) for i in range(3)),1)
    track=a.mesh(name+'_Tracks',kind='BayDoorTrack',trim_strip=2)
    for xx in (x-w/2-.07,x+w/2+.07):
        pts=[(xx,y+.22,z),(xx,y+.22,z+h+.10)]
        pts += [(xx,y+.64-.42*math.cos(t),z+h+.10+.42*math.sin(t)) for t in [i*math.pi/16 for i in range(1,9)]]
        pts += [(xx,y+5.1,z+h+.52)]
        track.tube(pts,.034,'Trim',(.43,.45,.43),sides=8)
    for yy in (1.1,3.9):
        track.box((x,y+yy,z+h+.67),(w+.32,.09,.09),'Trim',(.36,.38,.36),r=0)
        for xx in (x-w/2-.07,x+w/2+.07):track.beam((xx,y+yy,z+h+.67),(xx,y+yy,z+h+1.1),.035,role='Trim',r=0)
    ob=track.finish();ob['kinematic_guide']=True


def interior(a,p,x0,y0):
    from services import gear
    w=p['bayblock'];d=p['depth'];z=p['floor']
    m=a.mesh('ApparatusInterior',kind='BayInterior',trim_strip=2)
    # A connected floor slab with 1m chart stations: the old single 18m face
    # stretched a limestone normal strip until it resembled brushed wood.
    ny=math.ceil(d-.4);vs=[]
    for j in range(ny+1):
        for xx in (x0+.25,x0+w-.25):vs.append((xx,y0+.2+(d-.4)*j/ny,z))
    fs=[(j*2,j*2+1,j*2+3,j*2+2) for j in range(ny)];offset=len(vs)
    vs += [(x0+.25,y0+.2,z-.16),(x0+w-.25,y0+.2,z-.16),(x0+w-.25,y0+d-.2,z-.16),(x0+.25,y0+d-.2,z-.16)]
    fs += [(offset+3,offset+2,offset+1,offset),(0,offset,offset+1,1),(2*ny+1,offset+2,offset+3,2*ny)]
    fs += [tuple(range(0,2*ny+1,2))+(offset+3,offset),
        (1,offset+1,offset+2)+tuple(range(2*ny+1,1,-2))]
    m.geom(vs,fs,'Concrete',(.29,.285,.255))
    for yy in (y0+3,y0+8,y0+13,y0+17):
        m.box((x0+w/2,yy,5.55),(w-.5,.16,.28),'Trim',(.18,.20,.18))
        for xx in (x0+.45,x0+w-.45):m.box((xx,yy,2.9),(.14,.14,5.5),'Trim',(.18,.20,.18))
    for j in range(p['bays']):
        x=x0+.4572+(j+.5)*p['bay_width']
        # Exhaust duct is supported by a rail; flexible drop hangs in a slack bend.
        m.tube([(x+1.35,y0+1.8,5.6),(x+1.35,y0+15.8,5.6)],.075,'Trim',(.43,.45,.42),sides=10)
        pts=[(x+1.35,y0+7,5.55),(x+1.35,y0+7,4.7),(x+1.45,y0+7.02,3.6),(x+1.7,y0+7.2,2.1),(x+1.85,y0+7.65,.85)]
        m.tube(pts,.075,'Trim',(.66,.35,.018),sides=12)
        m.box((x+1.85,y0+7.65,.76),(.23,.23,.25),'Trim',(.025,.028,.025))
        for k in range(3):gear(a,'Gear_'+str(j)+'_'+str(k),(x-1+k*.75,y0+d-1.1,z))
    m.finish()
    from aging import patch
    for j in range(p['bays']):
        xx=x0+.4572+(j+.5)*p['bay_width']
        for side in (-1,1):
            patch(a,f'InteriorWheelLane_{j}_{side}',(xx+side*.94-.15,y0+1,z+.002),(1,0,0),(0,1,0),.30,d-2,(.035,.037,.029),
                lambda s,t,j=j:.28*math.sin(s*math.pi)**2*math.sin(t*math.pi)**.35*(.7+.3*math.sin(t*19+j)**2),nx=4,ny=36)
        patch(a,f'InteriorEngineTrail_{j}',(xx-.30,y0+1.7,z+.003),(1,0,0),(0,1,0),.60,d-3.4,(.027,.029,.022),
            lambda s,t,j=j:.38*math.sin(s*math.pi)**4*math.sin(t*math.pi)**.35*(.3+.6*math.exp(-((t-.35-.12*j)/.14)**2)),nx=4,ny=28)
    import bpy
    ma=bpy.data.materials.get('CivicBayDiffusers')
    if not ma:
        ma=bpy.data.materials.new('CivicBayDiffusers');ma.use_nodes=True;ma['switch_kind']='interior_lights';ma['tiling_vertex_tint']=False
        bs=ma.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.78,.77,.69,1);bs.inputs['Emission Color'].default_value=(1,.89,.70,1);bs.inputs['Emission Strength'].default_value=8
    for j in range(p['bays']):
        for k in range(3):
            xx=x0+.4572+(j+.5)*p['bay_width'];yy=y0+3.2+k*5.2
            lamp=a.mesh(f'BayLight_{j}_{k}',kind='InteriorLight');lamp.box((xx,yy,5.47),(1.6,.25,.08),'Glass')
            ob=lamp.finish();ob.data.materials.clear();ob.data.materials.append(ma)
            for face in ob.data.polygons:face.material_index=0
            socket=a.socket(f'BayLight_{j}_{k}',(xx,yy,5.40),'interior_light');socket['power_w']=240


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
    if p['office']:
        masonry.box((x0+p['bayblock']-.17,0,3),(.34,d-.68,6),'Siding',(.29,.28,.255),r=0)
    else:
        # A compact station still has a pedestrian exit when the wing is omitted.
        center=-4.5;half=.565
        for aa,bb in ((y+.34,center-half),(center+half,d/2-.34)):
            masonry.box((w/2-.17,(aa+bb)/2,3),(.34,bb-aa,6),'Siding',(.29,.28,.255),r=0)
        masonry.box((w/2-.17,center,(6+z+2.75)/2),(.34,2*half,6-z-2.75),'Siding',(.29,.28,.255),r=0)
        masonry.box((w/2-.17,center,z/2),(.34,2*half,z),'Concrete',r=0)
        from parts import front_door
        front_door(a,'Side_Door',(w/2,center,z),.915,2.70,90)
    masonry.finish()
    for j in range(p['bays']):
        xx=x0+.4572+(j+.5)*bw
        overhead(a,'Bay_'+str(j+1),xx,y,z)
        a.socket('Apparatus_'+str(j+1),(xx,y+8,z),'apparatus')
        m=a.mesh('Bay_'+str(j+1)+'_Lintel',kind='BayLintel');m.box((xx,y-.045,z+4.2672+.105),(4.51,.47,.21),'Concrete');m.finish()
        text(a,'BayNumber_'+str(j+1),str(j+1),(xx,y-.04,4.88),.38,(.63,.62,.53))
    roof=a.mesh('ApparatusRoof',kind='RoofPanel');roof.box((x0+p['bayblock']/2,0,5.98),(p['bayblock']+.25,d+.25,.23),'Shingles',r=0);roof.finish()
    text(a,'StationFrieze','FIRE STATION 3',(x0+p['bayblock']/2,y-.035,5.53),.42,(.65,.64,.57))
    for side in (-1,1):
        cornice(a,'StationFascia_'+str(side),(x0+p['bayblock']/2,side*d/2,6.08),p['bayblock'],0 if side<0 else 180,True)
    if p['office']:
        office_top=z+p['stories']*3.7976
        shell(a,'CrewOffice',(x0+p['bayblock'],w/2,y,y+12.192),office_top,z,3.6576,p['stories'],1,True,True)
        text(a,'FireLetters','FIRE - RESCUE',(x0+p['bayblock']+p['office']/2,y-.035,3.42),.31,(.64,.64,.57))
    if p['roof']=='hip':
        from buildings import hip
        hip(a,'StationHipRoof',(x0,x0+p['bayblock'],y,d/2),6.25,2.0)
    tower(a,p,x0+2.6,d/2+1.45);interior(a,p,x0,y)
    from services import equipment,drains
    if p['office']:equipment(a,(w/2-2,1,office_top+.27))
    drains(a,(x0,x0+p['bayblock'],y,d/2),6.0)
    a.socket('PublicWalk',(w/2-5,y-2,.15),'walk');return a
