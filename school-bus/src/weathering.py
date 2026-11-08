"""Bus-specific causal exposure, tire splash, runoff and cabin contact masks.

All fields use authored meter-space attributes, never photographic pixels.
Broad masks survive the shared atlas; small manufacture stays in normals.
"""
from kit.materials import Nodes
import spec as S

def context(mat):
    n=Nodes.__new__(Nodes);n.mat=mat;n.nt=mat.node_tree
    p=n.node('ShaderNodeAttribute',attribute_name='VehicleRest').outputs['Vector']
    return n,p,*n.split(p)

def layer(n,channel,mask,value):
    socket=n.nt.nodes['OUT_'+channel].inputs[0]
    old=socket.links[0].from_socket if socket.is_linked else socket.default_value
    n.feed(socket,n.mix(mask,old,value,channel=='base'))

def relief(n,amount):
    socket=n.nt.nodes['OUT_height'].inputs[0]
    old=socket.links[0].from_socket if socket.is_linked else socket.default_value
    n.feed(socket,n.add(old,amount))

def apply(m,wear):
    n,p,x,y,z=context(m['yellow']);side=n.ramp(n.math('ABSOLUTE',x),.94,1.15)
    breakup=n.noise(n.vec('MULTIPLY',p,(3,1,6)),18,3)
    tide=n.add(.965,n.mul(n.noise(n.vec('MULTIPLY',p,(.1,1,.1)),1.8,2),.105))
    level=n.math('DIVIDE',n.math('SUBTRACT',z,.775),n.math('SUBTRACT',tide,.775))
    lower=n.mul(side,n.ramp(level,1,0),n.ramp(breakup,.42,.66),wear,1.70)
    fans=[]
    for axle in [S.FRONT_AXLE,S.REAR_AXLE]:
        d=n.math('SUBTRACT',y,axle+.18)
        span=n.mul(n.ramp(d,0,.18),n.ramp(d,1.55,.48))
        ceiling=n.add(1.23,n.mul(d,-.20))
        rise=n.ramp(n.math('SUBTRACT',ceiling,z),0,.26)
        fans.append(n.mul(side,span,rise,n.ramp(breakup,.30,.68),wear,1.55))
    splash=n.maximum(lower,*fans)
    layer(n,'base',splash,(.095,.071,.037));layer(n,'rough',splash,.74)
    edge=n.mul(side,n.ramp(z,.835,.767),n.ramp(breakup,.48,.72),wear,1.80)
    layer(n,'base',edge,(.135,.043,.010));layer(n,'rough',edge,.84)
    salt=n.mul(side,n.band(z,.825,.027,.020),n.ramp(breakup,.58,.73),wear,1.10)
    layer(n,'base',salt,(.48,.47,.42));layer(n,'rough',salt,.87)
    leading=n.maximum(n.mul(n.ramp(y,-5.82,-5.94),n.ramp(z,1.34,1.43)),
                      n.mul(n.ramp(y,-5.54,-5.77),n.ramp(n.math('ABSOLUTE',x),.79,.88),n.ramp(z,1.25,1.10)))
    # Wear changes chip coverage, not the opacity of exposed primer.
    chips=n.mul(leading,n.ramp(n.noise(p,75,2),.66-.06*wear,.72-.06*wear))
    layer(n,'base',chips,(.21,.22,.20));layer(n,'rough',chips,.77)
    relief(n,n.mul(chips,-.00025))
    # Streaks start at hatch corners/marker penetrations and follow roof fall.
    roof=n.ramp(z,2.88,3.10);tracks=[]
    for yy in [-1.75,-1.05,3.55,4.25]:
        # Gravity follows the roof's transverse fall, away from hatch corners.
        ax=n.math('ABSOLUTE',x)
        downstream=n.mul(n.ramp(ax,.28,.36),n.ramp(ax,1.19,.82))
        drift=n.mul(n.math('SUBTRACT',breakup,.5),.035)
        distance=n.math('ABSOLUTE',n.math('SUBTRACT',y,n.add(yy,drift)))
        width=n.add(.028,n.mul(n.ramp(ax,.35,1.15),-.018))
        stripes=n.ramp(n.math('DIVIDE',distance,width),1,.25)
        tracks.append(n.mul(downstream,stripes,n.ramp(breakup,.42,.63)))
    # Short marker trails supplement the longer hatch-corner runoff.
    for yy in [-3.72,5.85]:
        stripes=n.maximum(*[n.ramp(n.math('ABSOLUTE',n.math('SUBTRACT',x,xx)),.045,.012) for xx in [-.2,0,.2]])
        fall=n.mul(n.ramp(y,yy-.38,yy-.10),n.ramp(y,yy+.025,yy)) if yy<0 else n.mul(n.ramp(y,yy-.025,yy),n.ramp(y,yy+.38,yy+.10))
        tracks.append(n.mul(fall,stripes))
    runoff=n.mul(roof,n.maximum(*tracks),wear,1.55,n.add(.55,n.mul(breakup,.45)))
    fade=n.mul(roof,wear,.32)
    layer(n,'base',fade,(.82,.49,.058));layer(n,'rough',fade,.48)
    layer(n,'base',runoff,(.22,.14,.049));layer(n,'rough',runoff,.66)
    # Soot sits immediately above/behind the actual left rear tailpipe outlet.
    soot=n.mul(n.ramp(x,-1.04,-1.20),n.ramp(y,5.35,5.65),n.ramp(y,6.14,5.94),
               n.ramp(z,1.03,.77),wear,1.60)
    layer(n,'base',soot,(.017,.016,.013));layer(n,'rough',soot,.86)
    coverage=n.nt.nodes['OUT_paint_coverage'].inputs[0]
    old=coverage.links[0].from_socket
    n.feed(coverage,n.mul(old,*[n.math('SUBTRACT',1,mask) for mask in [splash,edge,salt,chips,fade,runoff,soot]]))
    # Chalky exposed rail crowns; salt/rust remains on low painted steel.
    n,p,x,y,z=context(m['black'])
    rails=n.mul(n.ramp(n.math('ABSOLUTE',x),1.220,1.231),n.ramp(z,1.82,1.77),n.ramp(z,.77,.81))
    grain=n.noise(n.vec('MULTIPLY',p,(1,.3,6)),25,2)
    chalk=n.mul(rails,wear,n.add(.20,n.mul(grain,.55)))
    layer(n,'base',chalk,(.075,.078,.070));layer(n,'rough',chalk,.89)
    bumper=n.mul(n.ramp(n.math('ABSOLUTE',y),5.96,6.04),n.ramp(z,.60,.48),
                 n.ramp(grain,.59,.73),wear,1.50)
    layer(n,'base',bumper,(.100,.033,.009));layer(n,'rough',bumper,.85)
    # Repeated vinyl seam station is the actual seat pitch, not random noise.
    n,p,x,y,z=context(m['vinyl']);xx=n.math('ABSOLUTE',x)
    across=n.math('ABSOLUTE',n.math('SUBTRACT',xx,.657))
    edge=n.band(across,.450,.003,.003)
    top=n.band(z,2.312,.003,.003)
    seam=n.mul(n.maximum(edge,top),n.ramp(z,1.64,1.70))
    relief(n,n.mul(seam,.0010));layer(n,'rough',seam,.68)
    touch=n.mul(n.ramp(z,2.12,2.25),n.ramp(z,2.36,2.32),
                n.ramp(n.noise(n.vec('MULTIPLY',p,(18,.2,8)),4,3),.43,.70),wear,.55)
    layer(n,'base',touch,(.155,.091,.049));layer(n,'rough',touch,.66)
    # Two small tape repairs near a central row, with slightly raised edges.
    repair=n.mul(n.ramp(x,.31,.33),n.ramp(x,.46,.44),n.ramp(y,1.18,1.19),n.ramp(y,1.23,1.21),
                 n.ramp(z,1.94,1.95),n.ramp(z,2.065,2.055))
    repair=n.maximum(repair,n.mul(n.ramp(x,-.48,-.47),n.ramp(x,-.31,-.32),
                     n.ramp(y,-1.49,-1.48),n.ramp(y,-1.43,-1.44),n.ramp(z,2.10,2.11),n.ramp(z,2.21,2.20)))
    layer(n,'base',repair,(.012,.014,.012));layer(n,'rough',repair,.37)
    relief(n,n.mul(repair,.00035))
    # Aisle traffic polishes rubber; fine ribs run lengthwise on the runner,
    # and parallel to the door opening on the stair treads.
    n,p,x,y,z=context(m['floor'])
    aisle=n.mul(n.ramp(n.math('ABSOLUTE',x),.153,.07),n.ramp(z,1.16,1.18),wear)
    layer(n,'base',n.mul(aisle,.35),(.035,.031,.024));layer(n,'rough',aisle,.53)
    stairs=n.mul(n.ramp(y,-3.76,-3.72),n.ramp(y,-2.93,-2.97),n.ramp(x,-.29,-.50),n.ramp(z,1.19,1.15))
    rib=n.ramp(n.math('PINGPONG',x,.0045),.001,.0026)
    runner=n.mul(n.ramp(n.math('ABSOLUTE',x),.155,.151),n.ramp(z,1.18,1.184))
    relief(n,n.mul(n.maximum(stairs,runner),rib,.00085))
    layer(n,'base',n.mul(stairs,rib,.35),(.065,.061,.048))
    # Headliner joints and seam rivets read as metal panels under window light.
    n,p,x,y,z=context(m['ceiling'])
    joints=n.ramp(n.math('PINGPONG',n.add(y,3.38),.632),.004,.001)
    dots=n.ramp(n.add(n.mul(n.math('PINGPONG',x,.05),n.math('PINGPONG',x,.05)),
                      n.mul(n.math('PINGPONG',y,.075),n.math('PINGPONG',y,.075))),.004**2,.002**2)
    relief(n,n.add(n.mul(joints,-.0005),n.mul(dots,.00055)))
    layer(n,'base',n.mul(joints,.18),(.20,.22,.20))
    n,p,x,y,z=context(m['tape'])
    film=n.mul(n.ramp(z,1.043,1.022),n.ramp(n.noise(n.vec('MULTIPLY',p,(1,.3,3)),25,2),.30,.73),wear,.32)
    layer(n,'base',film,(.23,.18,.085));layer(n,'rough',film,.79)
    n,p,x,y,z=context(m['frame'])
    outlet=n.mul(n.ramp(x,-1.10,-1.26),n.ramp(y,5.40,5.63),n.ramp(z,.63,.53),wear,.85)
    layer(n,'base',outlet,(.011,.010,.008));layer(n,'rough',outlet,.91);layer(n,'metal',outlet,0)
    n,p,x,y,z=context(m['wheel']);dust=[]
    for axle in [S.FRONT_AXLE,S.REAR_AXLE]:
        dy=n.math('SUBTRACT',y,axle);dz=n.math('SUBTRACT',z,S.HUB)
        radius=n.math('SQRT',n.add(n.mul(dy,dy),n.mul(dz,dz)))
        dust.append(n.mul(n.ramp(radius,.060,.105),n.ramp(radius,.255,.190)))
    deposit=n.mul(n.maximum(*dust),wear,.65,n.add(.65,n.mul(n.noise(p,90,2),.35)))
    layer(n,'base',deposit,(.033,.027,.019));layer(n,'rough',deposit,.75);layer(n,'metal',deposit,0)
