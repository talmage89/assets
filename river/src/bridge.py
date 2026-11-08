"""Independent period Type III bridge. Cross-section from FDOT 20130.

No geometry or code is copied from the unmerged freeway branch. Local +X
is span station; cap width and girder pitch can share future kit primitives.
"""
import math
import geometry as G
from plan import FT

# 45 in total, 16 in top, 22 in bottom, 7 in web; 7.5/10/20/7.5 in zones.
SECTION=[(-.26035,0),(.26035,0),(.2794,.01905),(.2794,.1905),
         (.0889,.381),(.0889,.889),(.2032,1.0795),(.2032,1.143),
         (-.2032,1.143),(-.2032,1.0795),(-.0889,.889),(-.0889,.381),
         (-.2794,.1905),(-.2794,.01905)]


def girder(name,length=18.0086,parent=None):
    rt=G.root(name,parent=parent,module='TypeIII_Girder',length_m=length)
    b=G.Batch(name+'__Casting',rt)
    # Small prestress camber remains visible under long raking reflections.
    xs=[-length/2+i*length/12 for i in range(13)]
    rings=[[(x,y,z+.012*(1-(2*x/length)**2)) for y,z in SECTION] for x in xs]
    b.loft(rings);ob=b.finish()
    G.root(name+'__W',(-length/2,0,0),rt,socket_kind='bearing')
    G.root(name+'__E',(length/2,0,0),rt,socket_kind='bearing')
    return rt


def pier(name,width=11.8872,kind='columns',height=2.11,parent=None):
    rt=G.root(name,parent=parent,module='Pier_'+kind)
    b=G.Batch(name+'__Substructure',rt)
    # Datum is waterline. Buried footings stop below exposed bed.
    if kind=='columns':
        for y in (-width*.29,0,width*.29):
            b.cylinder((0,y,(height-.80-1.3)/2),.55,height-.80+1.3,n=24)
            b.box((0,y,-1.42),(1.95,1.95,.36))
    else:
        # Rounded cutwater, aligned with river +Y; not a wall across the flow.
        w=.65;length=width*.83
        sec=[(w,-length/2+.65),(w,length/2-.65)]
        sec += [(w*math.cos(t),length/2-.65+w*math.sin(t)) for t in [i*math.pi/8 for i in range(1,9)]]
        sec += [(-w,-length/2+.65)]
        sec += [(w*math.cos(t),-length/2+.65+w*math.sin(t)) for t in [math.pi+i*math.pi/8 for i in range(1,9)]]
        b.loft([[(x,y,z) for x,y in sec] for z in (-1.4,-.15,.1,1.25,height-.8)])
        b.box((0,0,-1.55),(2.25,length+1,.35))
    # Chamfered cap section, extruded in the transverse direction.
    sec=[(-.86,height-.70),(-.76,height-.80),(.76,height-.80),(.86,height-.70),(.86,height-.08),(.78,height),(-.78,height),(-.86,height-.08)]
    b.loft([[(x,y,z) for x,z in sec] for y in (-width/2+.3,width/2-.3)])
    b.finish();return rt


def abutment(name,width=11.8872,parent=None,seat=2.687,top=4.13):
    rt=G.root(name,parent=parent,module='Abutment',seat_z_m=seat)
    b=G.Batch(name+'__Retaining',rt)
    # Bridge is to local -X; wingwalls contain the approach embankment.
    b.box((.40,0,(seat-.4)/2),(.80,width,seat+.4))
    b.box((.82,0,(seat+top)/2),(.40,width,top-seat))
    b.box((.30,0,-.40),(1.8,width+.6,.35))
    for s in (-1,1):
        b.loft([[(x,y,z) for y,z in ((s*(width/2-.12),-.4),(s*(width/2+.22),-.4),(s*(width/2+.22),top),(s*(width/2-.12),top))] for x,top in ((.8,4.10),(3.2,3.75),(6.3,2.5))])
    b.finish();return rt


def parapet(name,length=6.096,parent=None):
    rt=G.root(name,parent=parent,module='Parapet')
    b=G.Batch(name+'__HemmedConcrete',rt)
    # Curb-mounted 32in concrete parapet, narrow cap with drip projections.
    sec=[(-.20,0),(.20,0),(.20,.10),(.13,.23),(.105,.8128),(-.105,.8128),(-.13,.23),(-.20,.10)]
    b.loft([[(x,y,z) for y,z in sec] for x in (-length/2,length/2)])
    for s in (-1,1):b.box((s*(length/2-.04),0,.81),(.012,.21,.012),'rubber')
    b.finish();return rt


def deck(name,length=6.096,width=11.8872,parent=None):
    rt=G.root(name,parent=parent,module='DeckPanel')
    b=G.Batch(name+'__Slab',rt)
    b.box((0,0,-.19),(length,width,.26))
    # Asphalt crowned at 2%; 5ft walks are integral raised curbs.
    lane=3.3528
    for s in (-1,1):
        vs=[(x,y,.00-.02*abs(y)) for x,y in ((-length/2,0),(length/2,0),(length/2,s*lane),(-length/2,s*lane))]
        b.geom(vs,[(0,1,2,3)],'asphalt')
        b.box((0,s*(lane+.1524/2),-.026),(length,.1524,.19))
        walkwidth=width/2-lane-.1524
        b.box((0,s*(lane+.1524+walkwidth/2),.009144),(length,walkwidth,.1524))
        b.box((0,s*(width/2-.23),-.327),(length,.018,.018),'rubber')
    b.finish();return rt


def guardrail(name,length=7.62,parent=None):
    rt=G.root(name,parent=parent,module='GuardrailTerminal')
    b=G.Batch(name+'__SheetAndPosts',rt)
    # Original 12ga bent W section; local X length, offset Y from traffic.
    sec=[(0,.48),(.067,.51),(.083,.56),(.016,.635),(.083,.71),(.067,.76),(0,.7874)]
    sec+= [(y+.00266,z) for y,z in reversed(sec)]
    b.loft([[(x,y,z) for y,z in sec] for x in (-length/2,length/2)],'steel')
    for i in range(5):
        x=-length/2+i*length/4
        for y in (.22,.36): b.box((x,y,.34),(.1524,.009,.76),'steel')
        b.box((x,.29,.34),(.006,.14,.76),'steel')
        b.box((x,.145,.63),(.1524,.2032,.3556),'wood')
        b.tube([(x,-.01,.635),(x,.36,.635)],.008,'steel',6)
    b.box((-length/2,.04,.635),(.35,.24,.40),'steel')
    b.box((-length/2-.18,.04,.635),(.008,.26,.38),'yellow')
    b.beam((-length/2,.29,.08),(-length/2+2.1,.29,.08),.06,role='steel')
    b.finish();return rt


def assemble(p,parent):
    rt=G.root('Bridge',parent=parent,bridge_plan=p.data());n=5
    ys=[-p.deck_width*.34+i*p.deck_width*.68/(n-1) for i in range(n)]
    soffit=p.deck_z-.32;bottom=soffit-1.143;seat=bottom-.30
    for i in range(p.spans):
        a=-p.length/2+i*p.span;c=a+p.span
        for j,y in enumerate(ys):
            ob=girder(f'Girder_{i}_{j}',p.span-.28,rt);ob.location=((a+c)/2,y,bottom)
        d=G.Batch(f'Span_{i}__DiaphragmsHaunches',rt)
        for x in (a+.48,(a+c)/2,c-.48):
            for ya,yb in zip(ys,ys[1:]):d.box((x,(ya+yb)/2,bottom+.69),(.22,yb-ya-.178,.75))
        for y in ys:d.box(((a+c)/2,y,soffit+.02),(p.span-.28,.41,.04))
        d.finish()
        for k in range(3):
            panel=deck(f'Deck_{i}_{k}',(p.span-.04)/3,p.deck_width,rt)
            panel.location=(a+.02+(k+.5)*(p.span-.04)/3,0,p.deck_z)
        for side in (-1,1):
            for j in range(3):
                ob=parapet(f'Parapet_{i}_{side}_{j}',p.span/3-.016,rt)
                ob.location=(a+(j+.5)*p.span/3,side*(p.deck_width/2-.24),p.deck_z+.085344)
        # Each 8m scupper drains through a real gutter gap into a downpipe.
        drain=G.Batch(f'Span_{i}__DrainConduit',rt)
        for side in (-1,1):
            for x in (a+p.span*.28,a+p.span*.73):
                y=side*3.51
                drain.box((x,y,p.deck_z-.16),(.36,.22,.16),'steel')
                drain.tube([(x,y,p.deck_z-.21),(x,y,p.deck_z-.67),(x,side*(p.deck_width/2+.12),p.deck_z-.74),(x,side*(p.deck_width/2+.12),p.deck_z-1.28)],.055,'steel',8)
            y=side*(p.deck_width*.31)
            drain.tube([(a+.15,y,soffit-.23),(c-.15,y,soffit-.23)],.048,'steel',8)
            for x in (a+2,a+7,c-2):
                drain.tube([(x,y-.12,soffit),(x,y-.12,soffit-.30),(x,y+.12,soffit-.30),(x,y+.12,soffit)],.008,'steel',6)
        drain.finish()
    for i in range(p.spans+1):
        x=-p.length/2+i*p.span
        if i in (0,p.spans):
            ob=abutment('Abutment_'+str(i),p.deck_width,rt,seat,soffit)
            ob.location.x=x;ob.rotation_euler.z=math.pi if i==0 else 0
        else:
            ob=pier('Pier_'+str(i),p.deck_width,p.pier,seat,rt);ob.location.x=x
        b=G.Batch('BearingStation_'+str(i),rt)
        for y in ys:
            offsets=(.40,-.40) if 0<i<p.spans else ((.40,) if i==0 else (-.40,))
            for dx in offsets:
                b.box((x+dx,y,seat+.10),(.56,.70,.20))
                b.box((x+dx,y,seat+.24),(.48,.60,.08),'rubber')
                b.box((x+dx,y,seat+.29),(.50,.62,.02),'steel')
        b.box((x,0,p.deck_z-.04),(.035,6.72,.04),'rubber')
        for dx in (-.033,.033):b.box((x+dx,0,p.deck_z-.039),(.025,6.72,.008),'steel')
        b.finish()
    for s in (-1,1):
        b=G.Batch('ApproachSlab_'+str(s),rt)
        b.box((s*(p.length/2+2),0,p.deck_z-.18),(4,p.deck_width,.28));b.finish()
        for side in (-1,1):
            ob=guardrail(f'ApproachRail_{s}_{side}',parent=rt)
            ob.location=(s*(p.length/2+4),side*(p.deck_width/2-.20),p.deck_z)
            ob.scale.y=side
    for y in (-1.6764,1.6764):
        pts=[(-120+i*4,y,p.deck_z-.02*abs(y)+.008) for i in range(61)]
        if y>0:pts.reverse()
        G.path('Lane_'+str(y),pts,rt,'drive',speed_m_s=11.176)
    for y in (-4.2672,4.2672):G.path('Sidewalk_'+str(y),[(x,y,p.deck_z+.085344) for x in (-120,120)],rt,'walk')
    return rt
