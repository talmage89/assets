"""Original parcel arrangements informed by the published plans in REFERENCE.

All construction is in the building's local frame. Campus rotation places its
entry on a different compass frontage without changing a classroom dimension.
Routes are open one-way polylines: never closed stadium rings on the lawn.
"""
def configure(p):
    ex,ey=p['entry'];kind=p['type']
    if kind=='finger':
        p.update(parcel='mid-block',site_yaw=0,lot=(210.,184.),
          parking=(-86,-58,-30,1),blacktop=(-12,44,30.20,69),
          playground=(44,65.336,36,51.24),field=(56,55),
          portables=[(-70,41,0)],
          bus_route=[(-58,-89.7),(-58,-60),(-53,-43),(-40,-35),(-5,-35),(9,-39),(48,-49),(59,-62),(59,-89.7)],
          parent_route=[(-91,-89.7),(-91,-44),(-74,-34),(-56,-28),(-49,-15),(-49,10),(-61,17),(-88,17),(-98,5),(-98,-89.7)],
          bus_curb=((-40,-31.3424),(-5,-31.3424)),
          parent_curb=((-45.3424,-8),(-45.3424,16)),
          streets=[dict(axis='X',at=-89.7,lo=-240,hi=240)],
          trees=[(-50,-52),(-24,-62),(12,-65),(46,-56),(-82,61),(-59,70),(84,16),(82,43)],
          shrubs=[(-39,-24),(-36,-24),(-33,-24),(-11,-25.3),(-8,-25.3),(5,-25.3)],
          hero=((-89,-44,1.68),(ex+3,ey+.5,2.1)))
    elif kind=='courtyard':
        p.update(parcel='corner / two frontages',site_yaw=90,lot=(210.,184.),
          parking=(51,86,-17,7),blacktop=(-15,43,33.70,72),
          playground=(-60,-38.664,40,55.24),field=(55,55),
          portables=[(-73,14,0)],
          bus_route=[(-70,-89.7),(-70,-65),(-58,-48),(-28,-46),(0,-35.8),(32,-35.8),(46,-50),(49,-67),(58,-79),(88,-79),(108,-79)],
          parent_route=[(108,-4),(86,-4),(55,-4),(52,-20),(62,-36),(72,-54),(98,-60),(108,-60)],
          bus_curb=((3,-32.1424),(28,-32.1424)),
          parent_curb=((55,-.3424),(83,-.3424)),
          streets=[dict(axis='X',at=-89.7,lo=-240,hi=240),dict(axis='Y',at=108,lo=-230,hi=230)],
          trees=[(-47,-33),(-42,-58),(-20,-58),(9,-60),(58,22),(-54,72),(79,64),(80,31)],
          shrubs=[(-27,-29),(-24,-29),(-21,-29),(-5,-29),(-2,-29),(9,-10)],
          hero=((100,-60,1.68),(4,-26,2.4)))
    else:
        p.update(parcel='backing onto a city park',site_yaw=180,lot=(210.,184.),
          parking=(-83,-49,-31,-12.7),blacktop=(-11.8184,62,28.8632,65),
          playground=(51,72.336,9,24.24),field=(-46,48),portables=[],
          bus_route=[(76,-89.7),(76,-61),(61,-43),(36,-38),(13,-36.8),(-8,-29.5),(-36,-29.5),(-44,-46),(-37,-64),(-37,-89.7)],
          parent_route=[(-75,-89.7),(-53,-54),(-49,-26),(-55,-9),(-80,-9),(-90,-27),(-90,-89.7)],
          bus_curb=((-27,-25.8424),(-10,-25.8424)),
          parent_curb=((-78,-5.3424),(-56,-5.3424)),
          streets=[dict(axis='X',at=-89.7,lo=-240,hi=240)],
          trees=[(-26,-60),(-10,-52),(35,-57),(48,-54),(-77,15),(-68,69),(7,75),(87,58)],
          shrubs=[(-34,-22.7),(-31,-22.7),(-28,-22.7),(-7,-22.6),(-4,-22.6),(3,-22.6)],
          hero=((-54,-49,1.68),(-3,-21,2.1)))
    p['bus_bays']=1 if kind=='compact' else 2
    p['parking_aprons']=[(-81,-61,-40,-27)] if kind=='finger' else [(-94,-80,-26,-17)] if kind=='compact' else []
    if kind in ('finger','courtyard'):p['bus_route'].reverse()
    p['stage']='look-dev checkpoint / reused baked PBR / no final docs'
    return p
