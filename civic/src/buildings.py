"""Program assemblies made from independent wall, trim, roof and entry units."""
import math
from geo import Assembly,orient,text
from parts import wall_bay,window,cornice,column,front_door,steps


def shell(a,name,rect,height,floor=.15,pitch=4.18,stories=1,brick=0,doors=True,modern=False,entry_face='Front'):
    l,r,f,k=rect;w=r-l;d=k-f
    for face,p,yaw,length in [('Front',((l+r)/2,f,floor),0,w),('Rear',((l+r)/2,k,floor),180,w),('East',(r,(f+k)/2,floor),90,d),('West',(l,(f+k)/2,floor),-90,d)]:
        n=max(1,round(length/pitch));bw=length/n
        for story in range(stories):
            for j in range(n):
                u=-length/2+(j+.5)*bw;rad=math.radians(yaw)
                at=(p[0]+u*math.cos(rad),p[1]+u*math.sin(rad),floor+story*(height-floor)/stories)
                hh=(height-floor)/stories
                if doors and face==entry_face and j==n//2 and story==0:
                    m=a.mesh(name+'_EntryMasonry',kind='DoorWallBay',brick_strip=brick,weather=True,top=height)
                    dw=2.10;dh=2.75;half=(bw-dw)/2
                    for s in (-1,1):m.box((s*(dw+half)/2,.17,hh/2),(half,.34,hh),'Veneer',r=0)
                    m.box((0,.17,(hh+dh)/2),(dw,.34,hh-dh),'Veneer',r=0)
                    orient(m,at,yaw);m.finish()
                    front_door(a,name+'_DoorL',(at[0]-.5025*math.cos(rad),at[1]-.5025*math.sin(rad),floor),.915,2.70,yaw)
                    front_door(a,name+'_DoorR',(at[0]+.5025*math.cos(rad),at[1]+.5025*math.sin(rad),floor),.915,2.70,yaw)
                else:wall_bay(a,f'{name}_{face}_{story}_{j}',at,bw,hh,.70 if modern else .76,1.65 if modern else 1.3716,1.7 if modern else min(2.4384,hh-1.02),yaw,brick,modern)
        run=a.mesh(name+'_'+face+'_WaterTable',kind='WaterTable',weather=True)
        run.box((0,.16,floor/2),(length,.40,floor),'Concrete')
        if doors and face==entry_face:
            entry_u=-length/2+(n//2+.5)*length/n
            for aa,bb in ((-length/2,entry_u-1.08),(entry_u+1.08,length/2)):
                run.box(((aa+bb)/2,.11,floor+.045),(bb-aa,.51,.09),'Concrete')
        else:run.box((0,.11,floor+.045),(length,.51,.09),'Concrete')
        orient(run,(p[0],p[1],0),yaw);run.finish()
        sections=max(1,math.ceil(length/4.18))
        for j in range(sections):
            u=-length/2+(j+.5)*length/sections
            cornice(a,f'{name}_{face}_Cornice_{j}',(p[0]+u*math.cos(math.radians(yaw)),p[1]+u*math.sin(math.radians(yaw)),height),length/sections,yaw,modern)
    roof=a.mesh(name+'_Roof',kind='RoofPanel')
    roof.box(((l+r)/2,(f+k)/2,height+.16),(w-.34,d-.34,.22),'Shingles',r=0);roof.finish()


def hip(a,name,rect,z,height=2.2,cupola=False):
    l,r,f,k=rect;cx=(l+r)/2;cy=(f+k)/2;w,d=r-l,k-f
    v=[(l-.4,f-.4,z),(r+.4,f-.4,z),(r+.4,k+.4,z),(l-.4,k+.4,z)]
    if abs(w-d)<1e-6:
        v.append((cx,cy,z+height));faces=[(0,1,4),(1,2,4),(2,3,4),(3,0,4)]
    elif w>d:
        ridge=(w-d)*.35;v.extend([(cx-ridge,cy,z+height),(cx+ridge,cy,z+height)])
        faces=[(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4)]
    else:
        ridge=(d-w)*.35;v.extend([(cx,cy-ridge,z+height),(cx,cy+ridge,z+height)])
        faces=[(0,1,4),(1,2,5,4),(2,3,5),(3,0,4,5)]
    m=a.mesh(name,kind='HipRoof')
    for face in faces:m.prism([v[i] for i in face],(0,0,-1),.12,'Shingles')
    m.finish()
    if cupola:
        m=a.mesh('Cupola',kind='Cupola',trim_strip=5)
        base=z+height-.1
        for zz,ww,hh in [(base,2.7,.28),(base+1.1,2.2,1.9),(base+2.10,2.8,.25)]:m.box((cx,cy,zz),(ww,ww,hh),'Concrete')
        for s in (-1,1):
            for yy in (-1,1):m.box((cx+s*1.02,cy+yy*1.02,base+1.08),(.18,.18,2.0),'Trim',(.68,.67,.60))
        m.finish();hip(a,'CupolaCopperCap',(cx-1.5,cx+1.5,cy-1.5,cy+1.5),base+2.25,1.2)


def hall(p):
    a=Assembly(p['program'].title()+'_'+str(p['seed']));w,d=p['width'],p['depth'];floor=p['floor'];top=floor+p['stories']*p['story_pitch']
    shell(a,'Main',(-w/2,w/2,-d/2,d/2),top,floor,p['bay_width'],p['stories'],p['brick'])
    for side in (-1,1):
        q=a.mesh('CornerQuoins_'+str(side),kind='QuoinPier')
        for j in range(round((top-floor)/.42)):
            q.box((side*(w/2-.24),-d/2-.07,floor+.20+j*.42),(.68 if j%2 else .50,.15,.40),'Concrete',r=.002)
        q.finish()
    if p['order']!='plain':
        ch=top-floor-.55;diam=ch/8.4
        projection=3.1 if p['order']=='columns' else .50
        for j,x in enumerate((-3.9,-1.3,1.3,3.9)):
            column(a,'EntryOrder_'+str(j),(x,-d/2-(2.7 if p['order']=='columns' else .12),floor),ch,diam,p['order']=='pilasters')
        m=a.mesh('PorticoEntablature',kind='PorticoRoof')
        m.box((0,-d/2-projection/2,top-.18),(9.2,projection,.90),'Concrete')
        m.box((0,-d/2-projection/2,top+.34),(9.65,projection+.20,.18),'Concrete');m.finish()
        cornice(a,'EntryCrowningCornice',(0,-d/2-projection,top+.15),9.65)
        text(a,'CivicInscription',p['name'],(0,-d/2-projection-.016,top-.40),.335)
        deck=a.mesh('PorticoLanding',kind='EntryLanding');deck.box((0,-d/2-projection/2,floor/2),(9.3,projection+.70,floor),'Concrete');deck.finish()
    else:text(a,'CivicInscription',p['name'],(0,-d/2-.025,top-.60),.30,(.66,.64,.55))
    if floor>.20:steps(a,(0,-d/2-(3.45 if p['order']=='columns' else .85),0),8.6,count=round(floor/.1524))
    if p['roof'] in ('hip','cupola'):hip(a,'MainHipRoof',(-w/2,w/2,-d/2,d/2),top+.45,2.5,p['roof']=='cupola')
    else:
        m=a.mesh('Parapet',kind='Parapet',brick_strip=p['brick'])
        for yy in (-d/2+.16,d/2-.16):m.box((0,yy,top+.70),(w,.32,.65),'Veneer',r=0);m.box((0,yy,top+1.04),(w+.10,.45,.11),'Concrete')
        for xx in (-w/2+.16,w/2-.16):m.box((xx,0,top+.70),(.32,d-.64,.65),'Veneer',r=0);m.box((xx,0,top+1.04),(.45,d-.50,.11),'Concrete')
        m.finish()
    if p['wings']:
        shell(a,'Police',(-w/2,-w/2+14.6304,d/2-.34,d/2+11.85),4.42,.1524,3.6576,1,1,True,True,'Rear')
        label=text(a,'PoliceLetters','BRIAR GLEN POLICE' if p['program']=='hall' else 'PUBLIC ANNEX',(-w/2+7.315,d/2+11.88,3.83),.23,(.64,.64,.57));label.rotation_euler.z=math.pi
        # 1994 entrance to an internal lift; at grade, beside original stairs.
        x=w/2+1.1;y=1.2
        shell(a,'AccessibleVestibule',(w/2-.34,w/2+3.05,-.2,3.7),3.4,.1524,3.39,1,1,True,True)
        text(a,'AccessLetters','PUBLIC ENTRY',(x,-.23,2.94),.17,(.64,.65,.59))
    stone=a.mesh('Cornerstone',kind='Cornerstone');stone.box((-w/2+.6,-d/2-.025,.48),(1.05,.06,.47),'Concrete');stone.finish()
    text(a,'CornerstoneDate',str(p['year']),(-w/2+.6,-d/2-.065,.37),.16)
    from services import equipment,drains
    equipment(a,(w/2-3,d/2-3,top+.29));drains(a,(-w/2,w/2,-d/2,d/2),top)
    a.socket('PublicWalk',(0,-d/2-5.5,0),'walk');return a
