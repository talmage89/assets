"""Formed-steel open cart: actual gauge, bent wheel legs and folded shelf hardware."""
import math
from kit import model as G


def build_cart(b):
    # 2 mm steel C sections, 62 mm broad visible front face. Open back returns.
    w,d,g=.062,.049,.002
    section=[(-w/2,-d/2),(w/2,-d/2),(w/2,d/2),(w/2-g,d/2),
             (w/2-g,-d/2+g),(-w/2+g,-d/2+g),(-w/2+g,d/2),(-w/2,d/2)]
    for sign in (-1,1):
        x=sign*.296
        for y in (-.222,.222):
            sec=section if y<0 else [(u,-v) for u,v in section]
            if sign>0:
                stations=[(.357,y,.088),(.352,y,.132),(.311,y,.200),(x,y,.260),(x,y,.779)]
            else:stations=[(x,y,.017),(x,y,.779)]
            leg=G.hollow_section('Formed cart leg',stations,sec,b.mat('powder'))
            G.bevel(leg,.00065,b.edges);b.add(leg)
            for z in (.315,.373,.717,.760):
                b.fastener('Leg carriage bolt',(x,y-.025 if y<0 else y+.025,z),
                           (0,-1,0) if y<0 else (0,1,0),kind='cross')
            if sign<0:
                # Push-on foot follows the section, with a thin splayed contact flange.
                loops=[]
                for z,fw,fd in [(0,.080,.071),(.003,.080,.071),(.009,.068,.058),(.026,.063,.050)]:
                    loops.append([(x+u,y+v,z) for u,v in G.rounded_rectangle(fw,fd,.007,4 if b.high else 2)])
                shoe=G.loft('Fixed foot molded shoe',loops,b.mat('plastic'))
                G.smooth(shoe);b.add(shoe)
                if b.high:
                    for k in range(3):b.box('Foot grip rib',(x-.025+k*.025,y-.030,.009),(.002,.001,.012),'plastic',.0004)
    # Perimeter tray rails and two side cross braces, all thin-wall formed channels.
    for y in (-.222,.222):
        pts=[(-.026,-.034),(.026,-.034),(.026,.034),(.024,.034),(.024,-.032),(-.026,-.032)]
        # A horizontal folded rail, 2 mm gauge, broad face toward the observer.
        b.profile('Lower frame cross channel',[(u+y,v+.342) for u,v in pts],-.294,.294,'powder',axis='X',radius=.0006)
        b.weld('Rail end stitch',[(-.265,y-.025,.311),(-.242,y-.025,.311)])
    for x in (-.296,.296):
        b.box('Side lower stretcher',(x,0,.341),(.032,.425,.029),'powder',.0012)
        # Broad side brace at mid-height, with angled folded return.
        outline=[(-.200,.573),(.200,.573),(.200,.520),(-.200,.520)]
        b.profile('Side frame brace',outline,x-.001,x+.001,'powder',radius=.001)
        b.box('Side brace lower return',(x+.009,0,.520),(.018,.40,.002),'powder',.0005)
        for y in (-.181,.181):b.fastener('Side brace bolt',(x+.003,y,.548),(1,0,0))
    # Rear formed strengthening panel with two ventilation slots.
    back=b.box('Rear cart brace panel',(0,.224,.447),(.530,.002,.096),'powder',.001)
    if b.high:
        for x in (-.16,0,.16):
            cut=G.profile('Rear brace slot cutter',G.rounded_rectangle(.09,.009,.004,4),.21,.24,None,axis='Y')
            cut.location=(x,0,.451);G.boolean(back,cut)
    b.box('Rear brace folded return',(0,.216,.398),(.530,.018,.002),'powder',.0006)
    # Stamped bottom shelf: shallow pressing, hemmed edges and pressed channels.
    loops=[]
    for z,width,depth in [(.347,.536,.396),(.350,.554,.412),(.352,.554,.412)]:
        loops.append([(u,v,z) for u,v in G.rounded_rectangle(width,depth,.010,4 if b.high else 2)])
    tray=G.loft('Pressed lower shelf tray',loops,b.mat('shelf'))
    G.bevel(tray,.0006,b.edges);b.add(tray)
    for y in (-.208,.208):b.box('Bottom shelf hem',(0,y,.358),(.554,.005,.014),'shelf',.001)
    for x in (-.166,-.055,.055,.166):
        pts=[(x-.008,.351),(x-.005,.356),(x+.005,.356),(x+.008,.351)]
        b.profile('Stamped shelf reinforcing channel',pts,-.196,.196,'shelf',axis='Y',radius=.0007)
    # Real axle and recessed black hub caps; plastic spokes connect hub and outer rim.
    b.cylinder('Solid wheel axle',(.357,-.288,.09),(.357,.288,.09),.0065,'stainless',16)
    for y in (-.253,.253):
        pivot=G.pivot('Wheel_Front' if y<0 else 'Wheel_Back',(0,0,0),'Y',[0,360]);pivot.parent=b.root
        n=96 if b.high else 32
        profile=[(-.025,.066),(-.025,.074),(-.020,.085),(-.013,.090),(.012,.090),(.021,.083),(.025,.072),(.025,.066)]
        if b.high:profile[3:5]=[(-.013,.090),(-.009,.090),(-.008,.0886),(-.006,.0886),(-.005,.090),(.004,.090),(.005,.0886),(.007,.0886),(.008,.090),(.012,.090)]
        tire=G.lathe('Rubber wheel tire',profile,b.mat('tire'),n,axis='Y',closed=True)
        # Tread blocks/molded channels alter the silhouette only in high detail.
        if b.high:
            for v in tire.data.vertices:
                r=math.hypot(v.co.x,v.co.z)
                if r>.084:
                    theta=math.atan2(v.co.z,v.co.x)
                    v.co*=1-.004*(.5+.5*math.cos(theta*48))
        b.add(tire,pivot)
        b.lathe('Wheel outer molded rim',[(-.021,.061),(-.021,.071),(-.015,.074),(.017,.074),(.021,.069),(.021,.061)],
                'plastic',48 if b.high else 24,axis='Y',closed=True,parent=pivot)
        b.lathe('Wheel hub', [(-.024,0),(-.024,.017),(.024,.017),(.026,.014),(.026,0)],'plastic',32 if b.high else 16,axis='Y',parent=pivot)
        for j in range(6):
            angle=j*math.tau/6
            spoke=G.box('Wheel structural spoke',(.040*math.cos(angle),0,.040*math.sin(angle)),(.056,.018,.010),b.mat('plastic'),.0015 if b.high else 0,b.edges)
            spoke.rotation_euler.y=-angle;b.add(spoke,pivot)
            if b.high:
                rib=G.box('Wheel spoke stiffening rib',(.040*math.cos(angle),.012,.040*math.sin(angle)),(.048,.003,.003),b.mat('plastic'),.0007,2)
                rib.rotation_euler.y=-angle;b.add(rib,pivot)
        side=-1 if y<0 else 1
        b.lathe('Wheel snap-in hub cap',[(side*.025,0),(side*.025,.014),(side*.027,.014),(side*.030,.012),(side*.030,0)],
                'plastic',32 if b.high else 16,axis='Y',parent=pivot)
        if b.high:b.lathe('Tire mold split line',[(-.001,.0892),(-.001,.0898),(.001,.0898),(.001,.0892)],'tire',n,axis='Y',closed=True,parent=pivot)
        pivot.location=(.357,y,.09)
        b.box('Axle steel mounting ear',(.350,y,.112),(.042,.026,.046),'powder',.003)
        b.fastener('Axle bracket bolt',(.339,y-.015,.125),(0,-1,0),radius=.004)


def build_shelves(b):
    for sign in (-1,1):
        x=sign*.4944
        # Steel top pressing; the 31 mm deep folded apron makes thickness readable.
        b.box('Brushed stainless work surface',(x,.018,.865),(.320,.493,.0014),'stainless_used',.0005)
        for y in (-.229,.265):
            # Two folded bends and a 6 mm inward hem, instead of an infinitely thin edge.
            b.box('Shelf folded apron',(x,y,.850),(.324,.0015,.030),'stainless_used',.00065)
            b.box('Shelf return hem',(x,y+(.003 if y<0 else -.003),.835),(.324,.007,.0015),'stainless_used',.0005)
        for xx in (sign*.335,sign*.654):
            b.box('Shelf inner end wall',(xx,.018,.851),(.0015,.493,.028),'stainless_used',.0006)
        # Molded end cap wraps the outer apron with a continuous 52-inch envelope.
        cap_points=[(-.235,.836),(.272,.836),(.272,.862),(.253,.879),(-.215,.879),(-.235,.864)]
        cap=b.profile('Shelf molded wrap endcap',cap_points,
                      sign*.650-.010,sign*.650+.010,'plastic',radius=.004)
        # Tubular hook rail under the outer edge, attached to two molded lugs.
        b.cylinder('Tool hook support rail',(sign*.645,-.192,.827),(sign*.645,.226,.827),.004,'plastic',16 if b.high else 8)
        for y in (-.19,.22):b.box('Hook rail mounting lug',(sign*.646,y,.833),(.018,.014,.026),'plastic',.003)
        for k in range(3):
            y=-.130+k*.116
            points=G.bezier((sign*.645,y,.828),(sign*.653,y,.808),(sign*.649,y,.791),(sign*.634,y,.795),10 if b.high else 5)
            b.tube('Molded tool hook',points,.003,'plastic',10 if b.high else 6)
        # Folded steel angle brackets with actual holes and an inner lip.
        for y in (-.172,.192):
            outline=[(sign*.321,.852),(sign*.505,.852),(sign*.505,.833),(sign*.336,.785),(sign*.321,.785)]
            bracket=G.profile('Shelf folded support bracket',outline,y-.001,y+.001,b.mat('powder'),axis='Y')
            if b.high:
                cut=G.profile('Bracket lightening cutout',[(sign*.350,.838),(sign*.458,.838),(sign*.350,.810)],y-.008,y+.008,None,axis='Y')
                G.boolean(bracket,cut)
            G.bevel(bracket,.0008,b.edges);b.add(bracket)
            b.box('Shelf bracket top flange',(sign*.413,y-.007,.851),(.180,.016,.002),'powder',.0005)
            b.fastener('Shelf bracket screw',(sign*.338,y-.002,.824),(0,-1,0),kind='cross',radius=.004)
        for y in (-.207,.239):b.fastener('Shelf endcap screw',(sign*.6545,y,.850),(sign,0,0),radius=.003,kind='cross',washer=False)
