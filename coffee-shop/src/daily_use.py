"""Original small signs of customers, at real scale and within furniture bays."""
import math
from mathutils import Vector
from geometry import Batch,root


def laptop(b):
    """325 x 227 x 29 mm closed envelope, 13.3-inch 16:10 display, circa 2006.

    An original generic business notebook; no manufacturer's marks or UI.
    Open lid is 95 degrees from the deck. Keys are 14mm, on 18mm pitch.
    """
    b.rounded((.025,-.07,.0145),(.325,.227,.029),.006,'steel',3)
    b.rounded((.025,-.054,.030),(.285,.126,.002),.002,'black',1)
    for j in range(6):
        for k in range(14):
            if j==0 and 3<=k<=9:continue
            b.box((-.092+k*.018,-.102+j*.017,.0325),(.014,.013,.003),'rubber')
            from geometry import LAYOUT
            a,bb,c,d=LAYOUT['keyboard'];ua=a+(c-a)*k/14;ub=a+(c-a)*(k+1)/14;v0=d-(d-bb)*(j+1)/6;v1=d-(d-bb)*j/6
            b.uv[-5]=[(ua,v0),(ub,v0),(ub,v1),(ua,v1)];b.roles[-5]='keyboard'
    b.box((.025,-.102,.0325),(.114,.013,.003),'rubber')
    b.rounded((.025,-.157,.0305),(.067,.035,.0015),.003,'black',2)
    b.box((.025,-.180,.031),(.067,.005,.001),'steel')
    # Hinge barrels on the same axis as the lid, rather than floating sticks.
    for x in (-.103,.153):b.tube([(x-.018,.037,.034),(x+.018,.037,.034)],.006,'black',8)
    up=Vector((0,math.sin(math.radians(5)),math.cos(math.radians(5))))
    normal=Vector((0,-up.z,up.y));origin=Vector((.025,.037,.034))
    def pt(x,y,t=0):return origin+Vector((x,0,0))+up*y+normal*t
    vs=[pt(x,y,t) for x,y,t in ((-.1625,0,-.004),(.1625,0,-.004),(.1625,.217,-.004),(-.1625,.217,-.004),(-.1625,0,.004),(.1625,0,.004),(.1625,.217,.004),(-.1625,.217,.004))]
    b.geom(vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'black')
    b.print([pt(-.1435,.021,.0042),pt(.1435,.021,.0042),pt(.1435,.200,.0042),pt(-.1435,.200,.0042)],'screen')
    for x in (-.1377,.1877):
        b.box((x,-.073,.011),(.001,.027,.006),'black')


def napkin(b,x,y,z):
    # A folded sheet with one lifted corner, not a thick cardboard block.
    b.geom([(x-.047,y-.040,z),(x+.046,y-.042,z),(x+.050,y+.037,z+.001),(x-.043,y+.043,z+.003)],[(0,1,2,3)],'white')
    b.geom([(x-.043,y+.043,z+.003),(x+.005,y+.034,z+.002),(x-.038,y+.015,z+.004)],[(0,1,2)],'cream')


def bag(parent,pos):
    r=root('Customer canvas satchel',pos,parent);b=Batch('Satchel folded body',r)
    rings=[]
    for z,w,d in ((.012,.14,.075),(.12,.16,.085),(.29,.145,.040),(.34,.14,.035)):
        rings.append([(-w,-d,z),(w,-d+.008,z+.008),(w,d,z),(-w,d,z-.004)])
    b.loft(rings,'ochre');b.box((0,-.042,.267),(.27,.004,.105),'ochre')
    b.tube([(-.12,.013,.31),(-.15,.018,.41),(.12,.024,.43),(.13,.018,.31)],.008,'black',6)
    for x in (-.07,.07):b.box((x,-.047,.245),(.014,.009,.05),'black')
    low=min(v[2] for v in b.v);b.v=[(x,y,z-low) for x,y,z in b.v]
    b.finish();return r


def bowl(parent,x,y,z):
    r=root('Door dog water bowl',(x,y,z),parent);b=Batch('Dog bowl spun stainless',r)
    b.lathe([(.0,.12),(.012,.125),(.070,.105),(.075,.098),(.015,.090),(.015,.001)],'steel',24)
    b.cylinder((0,0,.044),.096,.002,'ink',24);b.finish();return r


def bicycle(parent,x,y,z):
    """Original 700c commuter, leaning on the rack; actual 35mm tires."""
    r=root('Locked commuter bicycle',(x,y,z),parent);b=Batch('Commuter frame and running gear',r)
    # Bicycle lies in X/Z; all wheel axles are local Y.
    def wheel(cx):
        for rad,wire,role in ((.337,.0175,'rubber'),(.308,.009,'steel')):
            pts=[(cx+rad*math.cos(k*math.tau/36),0,.355+rad*math.sin(k*math.tau/36)) for k in range(37)]
            b.tube(pts,wire,role,6)
        b.tube([(cx,-.045,.355),(cx,.045,.355)],.018,'black',10)
        for k in range(16):
            a=k*math.tau/16;b.tube([(cx,.018*(-1 if k%2 else 1),.355),(cx+.301*math.cos(a),0,.355+.301*math.sin(a))],.0013,'steel',4)
    for cx in (-.53,.53):wheel(cx)
    bb=(-.07,0,.29);seat=(-.25,0,.84);head=(.36,0,.89);low=(.41,0,.71)
    for a,c in ((bb,seat),(seat,head),(head,low),(low,bb),(bb,(-.53,0,.355)),(seat,(-.53,0,.355)),(low,(.53,0,.355))):b.tube([a,c],.014,'forest',8)
    b.tube([seat,(-.25,0,.94)],.011,'steel',8);b.rounded((-.27,0,.955),(.25,.15,.040),.012,'black',3)
    b.tube([head,(.34,0,1.01),(.34,-.24,1.02),(.25,-.30,1.03)],.011,'steel',8)
    b.tube([(.34,0,1.01),(.34,.24,1.02),(.25,.30,1.03)],.011,'steel',8)
    for s in (-1,1):
        b.tube([(-.07,0,.29),(-.07+s*.13,s*.075,.29)],.010,'steel',6)
        b.box((-.07+s*.13,s*.10,.29),(.08,.065,.022),'black')
    b.tube([(-.13,-.037,.30),(-.53,-.037,.37),(-.50,-.037,.32),(-.13,-.037,.25),(-.13,-.037,.30)],.003,'black',5)
    # A slack brake cable, plus a closed 14mm U-bow around frame and rack.
    b.tube([(.26,-.26,1.02),(.35,-.09,.95),(.38,-.05,.77),(.44,-.06,.64)],.0024,'black',5)
    # The bow lies in an oblique plane: the leaned bicycle and vertical rack
    # have different heights at the two enclosed sections. check_use.py checks
    # both sections and actual triangle clearance after glTF re-import.
    lock_center=Vector((-.215,.0242,.73));lock_radius=.065
    lock_axis=Vector((0,-.3542,-.07)).normalized()
    bow=[lock_center+Vector((-lock_radius,0,0))]
    for k in range(9):
        theta=math.pi-k*math.pi/8
        bow.append(lock_center+Vector((lock_radius*math.cos(theta),0,0))+lock_axis*(.295+lock_radius*math.sin(theta)))
    bow.append(lock_center+Vector((lock_radius,0,0)))
    b.tube(bow,.007,'black',5)
    b.tube([bow[0],bow[-1]],.010,'black',7)
    ob=b.finish();r.rotation_euler.x=math.radians(7)
    low=min((r.rotation_euler.to_matrix()@v.co).z for v in ob.data.vertices)
    r.location.z-=low;return r
