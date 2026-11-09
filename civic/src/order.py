"""A bearing Tuscan entablature and closed pediment, in measured meters.

Fine surface tooling uses the existing limestone normal chart. Geometry pays
only for the order's profiles and the teeth that cast a real street shadow.
"""
from geo import orient,text


def entablature(a,p,top,projection):
    d=p['depth'];front=-d/2-projection;width=9.65
    m=a.mesh('PorticoEntablature',kind='PorticoRoof',weather=True,top=top+.77)
    # Column bearing level is top-.55. The first fascia starts exactly there.
    for z,h,over in [(-.43,.24,0),(-.285,.05,.035),(-.02,.48,.015),(.245,.05,.06)]:
        m.box((0,front+projection/2,z+top),(width+over*2,projection+over*2,h),'Concrete')
    m.finish()
    # Full-depth projecting corona, bed molding and crown, with side returns.
    from parts import cornice
    cornice(a,'EntryCrowningCornice',(0,front,top+.29),width)
    for side in (-1,1):
        cornice(a,'PorticoReturn_'+str(side),(side*width/2,front+projection/2,top+.29),projection,side*90)
    text(a,'CivicInscription',p['name'],(0,front-.061,top-.145),.31)
    if p['order']!='columns':return
    base=top+.90;peak=base+1.68
    m=a.mesh('PorticoPediment',kind='Pediment',weather=True,top=peak)
    m.prism([(-width/2,front+.08,base),(width/2,front+.08,base),(0,front+.08,peak)],(0,1,0),projection-.08,'Concrete',(.43,.414,.365))
    # Raking fasciae and projecting crown. Their square returns close the ends.
    for side in (-1,1):
        start=(side*(width/2+.15),front-.05,base);end=(0,front-.05,peak+.045)
        m.beam(start,end,.17,.36,'Concrete',r=.006)
        start=(side*(width/2+.22),front-.13,base+.12);end=(0,front-.13,peak+.21)
        m.beam(start,end,.11,.46,'Concrete',r=.005)
    m.finish()
    # Vent louver, without a borrowed town seal or invented heraldic brand.
    m=a.mesh('PedimentVent',kind='PedimentVent',trim_strip=5)
    for j in range(7):
        m.box((0,front+.058,base+.44+j*.073),(.43, .045,.025),'Trim',(.31,.30,.263),r=0)
    m.finish()
