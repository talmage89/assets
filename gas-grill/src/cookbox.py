"""Cast drain-through firebox, combustion hardware, grates and grease management."""
import math
from kit import model as G


def build_firebox(b):
    # The path goes down the outside, through the grease throat, and back up the
    # inside. No closed bottom hides the real drain. Cast wall gauge is 4–7 mm.
    stations=[(.897,.654,.530,.045,.012),(.881,.655,.530,.045,.012),
              (.749,.606,.474,.058,.012),(.699,.525,.387,.065,-.002),
              (.671,.102,.118,.018,-.024),(.678,.094,.110,.016,-.024),
              (.713,.515,.377,.063,-.002),(.758,.595,.463,.055,.012),
              (.889,.640,.515,.043,.012),(.897,.640,.515,.043,.012)]
    loops=[]
    for z,w,d,r,y in stations:
        loops.append([(x,v+y,z) for x,v in G.rounded_rectangle(w,d,r,9 if b.high else 3)])
    vessel=G.ring_loft('Cast firebox with sloped grease throat',loops,b.mat('casting'))
    # Large cast side walls stay planar; only the curved corner strips are smooth.
    G.smooth(vessel,35)
    vessel.data.materials.append(b.mat('bowl'))
    count=len(loops[0])
    for poly in vessel.data.polygons:
        if poly.index//count in range(4,9):poly.material_index=1
    G.bevel(vessel,.0007,b.edges);b.add(vessel)
    # Continuous overlapping lid seat, with a front grease-stained lip.
    b.box('Firebox stained front rim',(0,-.249,.895),(.638,.016,.014),'lip',.002)
    b.box('Rear exhaust seat',(0,.271,.894),(.638,.015,.013),'casting',.002)
    for x in (-.321,.321):
        b.box('Cast grate shelf',(x,.014,.870),(.015,.448,.013),'casting',.002)
        for y in (-.164,.158):
            b.box('Cast mounting boss',(x,y,.756),(.017,.034,.036),'casting',.004)
            b.fastener('Cookbox mounting bolt',(x+math.copysign(.010,x),y,.757),(math.copysign(1,x),0,0))
        for y in (-.16,.025,.19):
            # Tapered cast strengthening ribs blend into the wall at their ends.
            section=[(y-.006,.750),(y+.006,.750),(y+.004,.854),(y-.004,.854)]
            b.profile('Tapered exterior casting rib',section,x-.004,x+.004,'casting',radius=.002)
    # Front heat/manifold shield, hidden behind fascia but visible through gaps.
    shield=G.sheet('Control manifold heat shield',[(-.250,.852),(-.242,.751),(-.218,.731)],.606,.0012,b.mat('powder'))
    b.add(shield)
    for x in (-.283,.283):b.fastener('Heat shield screw',(x,-.264,.755),kind='cross',radius=.0035)
    build_burners(b)
    build_heat_tents(b)
    build_grates(b)
    build_warming_rack(b)
    build_grease_system(b)


def build_burners(b):
    # Three fore-aft tubes and the rear crossover match the exploded E-310 layout.
    for i,x in enumerate((-.205,0,.205),1):
        profile=[(-.252,0),(-.252,.012),(-.228,.012),(-.221,.009),
                 (.219,.009),(.231,.007),(.231,0)]
        if b.high:profile=[(-.252,.012),(-.228,.012),(-.221,.009),(.219,.009),(.231,.007),(.231,0),(.2302,0),(.2302,.0062),(.2187,.0082),(-.221,.0082),(-.227,.0112),(-.252,.0112)]
        burner=G.lathe(f'Burner {i} stainless tube',profile,b.mat('burner'),32 if b.high else 12,axis='Y',center=(x,.770),closed=b.high)
        if b.high:
            # Both walls have a row of flame ports. Geometry provides real apertures
            # in source; the game version will receive their normal-map impression.
            for k in range(36):
                y=-.209+k*.0118
                cut=G.cylinder('Burner port cutter',(x-.015,y,.772),(x+.015,y,.772),.00085,None,8)
                G.boolean(burner,cut)
        b.add(burner)
        b.box('Burner rear mounting tab',(x,.237,.766),(.029,.032,.002),'stainless',.0007)
        b.fastener('Burner retaining screw',(x,.246,.769),(0,0,1),radius=.003,kind='cross',washer=False)
        # Mesh-backed venturi air intake and a separate brass control valve.
        b.lathe('Venturi air shutter',[(-.266,.010),(-.266,.013),(-.242,.013),(-.242,.010)],
                'stainless',24 if b.high else 12,axis='Y',center=(x,.770),closed=True)
        b.cylinder('Gas valve brass body',(x,-.261,.789),(x,-.230,.789),.009,'brass',16 if b.high else 8)
        b.cylinder('Gas metering nozzle',(x,-.230,.777),(x,-.216,.777),.0035,'brass',12 if b.high else 6)
        if b.high:
            for k in range(9):
                y=-.262+k*.002
                b.cylinder('Venturi mesh strut',(x-.011,y,.777),(x+.011,y,.777),.0003,'stainless',6)
    b.cylinder('Rear crossover burner',(-.212,.218,.767),(.212,.218,.767),.0055,'burner',24 if b.high else 10)
    if b.high:
        for k in range(37):
            x=-.198+k*.011
            b.cylinder('Crossover port aperture',(x,.212,.769),(x,.2117,.769),.0007,'void',6)
    b.cylinder('Gas manifold pipe',(-.245,-.277,.748),(.260,-.277,.748),.0065,'stainless',20 if b.high else 8)
    for x in (-.205,0,.205):
        b.cylinder('Manifold valve tee',(x,-.277,.748),(x,-.277,.774),.006,'brass',16 if b.high else 8)
    # Ceramic electrode, mounting clip, visible steel tip and silicone lead.
    b.box('Igniter retaining bracket',(-.221,-.180,.779),(.018,.015,.002),'stainless',.0005)
    b.cylinder('Igniter ceramic insulator',(-.228,-.193,.778),(-.228,-.162,.778),.0032,'paint',20 if b.high else 8)
    b.tube('Igniter spark electrode',[(-.228,-.162,.778),(-.228,-.151,.778),(-.219,-.150,.776)],.00075,'stainless',8 if b.high else 5)
    b.tube('Ignition insulated cable',[(-.228,-.193,.778),(-.245,-.237,.748),(-.270,-.253,.734),(-.285,-.249,.826)],.0017,'rubber',8 if b.high else 5)


def build_heat_tents(b):
    # Five dull inverted-V channels; every other bar covers one of three burners.
    # Cross-section is closed steel gauge, flat shading on broad folded faces.
    for i,x in enumerate((-.205,-.1025,0,.1025,.205),1):
        section=[(x-.041,.812),(x,.841),(x+.041,.812),
                 (x+.0405,.8108),(x,.8395),(x-.0405,.8108)]
        bar=G.profile(f'Heat tent {i}',section,-.190,.223,b.mat('tent'),axis='Y')
        G.bevel(bar,.00035,2 if b.high else 1)
        for p in bar.data.polygons:p.use_smooth=False
        if b.high:
            # End locating notches are real cuts, not melted-looking bevels.
            for y in (-.191,.223):
                cutter=G.box('Heat tent end notch',(x,y,.814),(.019,.012,.011),None,0)
                G.boolean(bar,cutter)
        b.add(bar);bar['export_part']='HeatTents'
    # Integral cast ledges meet the bowl wall and support the channel FEET.
    # Small tabs under each ridge would float in the V's empty interior.
    for y in (-.2145,.2425):
        b.box('Cast heat channel support ledge',(0,y,.809),(.580,.055,.004),'casting',.001)


def build_grates(b):
    before=set(b.root.children)
    # Two framed castings separated by a 4 mm expansion gap; trapezoidal/rounded
    # bars have broad cooking faces and narrower undersides, not wooden boards.
    for sign in (-1,1):
        left,right=(-.304,-.002) if sign<0 else (.002,.304)
        center=(left+right)/2
        for j in range(19):
            x=left+.010+j*(right-left-.020)/18
            section=[(x-.0034,.874),(x+.0034,.874),(x+.0053,.884),
                     (x+.0044,.887),(x-.0044,.887),(x-.0053,.884)]
            b.profile('Cooking grate porcelain bar',section,-.207,.239,'grate',axis='Y',radius=.00065)
        # Underneath cross ribs merge the load into the perimeter cast frame.
        for y in (-.202,.015,.234):
            b.box('Grate underside cross rib',(center,y,.874),(.298,.009,.009),'grate',.0012)
        for x in (left+.0025,right-.0025):
            b.box('Grate cast side frame',(x,.016,.880),(.005,.446,.014),'grate',.0012)
        for y in (-.206,.238):b.box('Grate cast end frame',(center,y,.880),(.302,.007,.014),'grate',.0013)
        for x in (left+.018,right-.018):
            for y in (-.192,.224):b.box('Grate support nib',(x,y,.866),(.014,.019,.009),'grate',.001)

    for ob in set(b.root.children)-before:ob['export_part']='CookGrates'


def build_warming_rack(b):
    before=set(b.root.children)
    # Narrower 2.8 mm wires at 16 mm pitch; return legs rest in cast sockets.
    for x in (-.273,.273):
        points=[(x,.221,.881),(x,.226,.930),(x,.215,.968),(x,.195,.974)]
        b.tube('Warming rack support leg',points,.003,'stainless',10 if b.high else 6)
        b.box('Rack cast receiving socket',(x,.238,.882),(.021,.020,.018),'casting',.003)
    for y in (.094,.215):b.cylinder('Warming rack perimeter',(-.2785,y,.974),(.2785,y,.974),.0028,'stainless',16 if b.high else 6)
    for j in range(7):
        y=.094+j*.02017
        b.cylinder('Warming rack transverse wire',(-.275,y,.974),(.275,y,.974),.0014,'stainless',12 if b.high else 6)
    for x in (-.273,0,.273):
        b.cylinder('Warming rack underside tie',(x,.094,.972),(x,.215,.972),.0018,'stainless',12 if b.high else 6)
        if b.high:
            for j in range(7):
                y=.094+j*.02017
                b.cylinder('Rack resistance weld',(x,y,.972),(x,y,.9735),.0017,'stainless',8)

    for ob in set(b.root.children)-before:ob['export_part']='WarmingRack'


def build_grease_system(b):
    # Drain throat drops into a broad shallow stamped sliding tray and a foil cup.
    for x in (-.143,.143):
        b.profile('Grease tray runner',[(x-.010,.680),(x+.004,.680),(x+.004,.650),(x-.010,.650),
                                      (x-.010,.652),(x+.002,.652),(x+.002,.678),(x-.010,.678)],
                  -.195,.212,'stainless',axis='Y',radius=.0006)
    before=set(b.root.children)
    loops=[]
    for z,w,d,r in [(.647,.260,.330,.019),(.653,.286,.361,.021),(.667,.298,.373,.024),(.668,.297,.372,.024)]:
        loops.append([(u,v-.009,z) for u,v in G.rounded_rectangle(w,d,r,6 if b.high else 2)])
    tray=G.loft('Removable stamped grease tray',loops,b.mat('tray'))
    G.bevel(tray,.0007,b.edges);b.add(tray)
    b.box('Grease tray front fold',(0,-.196,.662),(.297,.003,.018),'tray',.001)
    for x in (-.073,.073):b.box('Grease tray handle standoff',(x,-.204,.658),(.012,.016,.012),'powder',.002)
    b.cylinder('Grease tray pull handle',(-.076,-.214,.658),(.076,-.214,.658),.004,'stainless',16 if b.high else 8)
    # Small foil catch cup beneath outlet; the upper open surface contains residue.
    loops=[]
    for z,w,d in [(.610,.155,.104),(.629,.184,.130),(.630,.187,.133),(.631,.179,.125),(.614,.151,.100)]:
        loops.append([(u,v-.030,z) for u,v in G.rounded_rectangle(w,d,.018,6 if b.high else 2)])
    cup=G.loft('Foil grease catch cup rolled rim',loops,b.mat('tray'))
    G.smooth(cup);b.add(cup)
    b.box('Catch cup grease residue',(0,-.030,.615),(.145,.094,.001),'soot',.004)
    if b.high:
        for k in range(7):
            x=-.062+k*.020
            b.tube('Foil cup emboss rib',[(x,-.078,.615),(x,-.083,.620),(x,-.087,.628)],.00035,'stainless',6)

    # The drawer and its catch cup slide along the runners as one removable part.
    drawer=G.pivot('GreaseTray',(0,-.009,.647));drawer.parent=b.root
    drawer['slide_axis']='Y';drawer['range_m']=[-.20,0]
    for ob in set(b.root.children)-before-{drawer}:
        if ob.type=='MESH':G.attach(ob,drawer)
