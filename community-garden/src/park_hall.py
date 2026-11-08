"""Original small municipal timber recreation hall, presentation context only.

13 x 8.5 m footprint, raised concrete footing, framed window/door reveals,
board siding and standing-seam roof. No asset or photographic geometry input.
"""
import geometry as Q


def build(parent,x,y):
    rt=Q.root('Meadow park community hall','presentation building',parent);rt.location=(x,y,0)
    Q.box('Hall concrete foundation',(0,0,.14),(13.12,8.62,.28),rt,'Block',.012)
    # Continuous gauged walls, partitioned around actual window and door
    # openings. No wall or sill remains hidden across a moving doorway.
    windows=[(-4.55,2.05),(-1.90,1.30),(1.90,1.30),(4.55,2.05)]
    for side in (-1,1):
        yy=side*4.25
        intervals=[(-6.5,-.91),(.91,6.5)] if side<0 else [(-6.5,6.5)]
        for lo,hi in intervals:Q.box('Hall wall sill',((lo+hi)/2,yy,.65),(hi-lo,.15,.77),rt,'OldWood')
        Q.box('Hall window head band',(0,yy,2.9425),(13,.15,.715),rt,'OldWood')
        openings=sorted([(xx-ww/2,xx+ww/2) for xx,ww in windows]+([(-.91,.91)] if side<0 else []))
        end=-6.5
        for lo,hi in [*openings,(6.5,6.5)]:
            if lo>end:Q.box('Hall framed wall pier',((end+lo)/2,yy,1.81),(lo-end,.15,1.55),rt,'OldWood')
            end=hi
        if side<0:Q.box('Hall solid door header',(0,yy,2.5575),(1.82,.15,.055),rt,'OldWood')
        for xx,ww in windows:
            Q.box('Hall recessed glazing',(xx,yy-side*.075,1.81),(ww,.024,1.48),rt,'Glass')
            for dx in (-ww/2,ww/2):Q.box('Hall window jamb return',(xx+dx,yy,1.81),(.075,.21,1.62),rt,'White')
            for zz in (1.035,2.585):Q.box('Hall window frame cap',(xx,yy,zz),(ww+.12,.21,.075),rt,'White')
            Q.box('Hall window mullion',(xx,yy+side*.03,1.81),(.044,.06,1.48),rt,'White')
            Q.box('Hall window transom',(xx,yy+side*.03,2.12),(ww,.06,.044),rt,'White')
    for side in (-1,1):
        xx=side*6.5
        Q.box('Hall end wall',(xx,0,1.78),(.15,8.5,3.02),rt,'OldWood')
        Q.mesh('Hall gable wall',[(xx,-4.25,3.3),(xx,4.25,3.3),(xx,0,5.0)],[(0,1,2)],rt,'OldWood')
        for j in range(58):
            yy=-4.22+j*.147
            Q.box('Hall vertical end siding batten',(xx+side*.084,yy,1.8),(.018,.032,2.98),rt,'Wood')
    # Front entry vestibule projects from the long facade, reached from lawn.
    Q.box('Hall threshold',(0,-4.35,.28),(1.75,.30,.024),rt,'Zinc')
    for side in (-1,1):
        leaf=Q.root('HallDoorLeft' if side<0 else 'HallDoorRight','pivot',rt)
        leaf.location=(side*.82,-4.46,.30);leaf['pivot_axis']='Z';leaf['range_degrees']=[-90,0] if side<0 else [0,90]
        Q.box('Hall door leaf',(-side*.405,0,1.07),(.81,.052,2.14),leaf,'Green')
        Q.box('Hall door vision glass',(-side*.405,-.034,1.445),(.55,.018,.74),leaf,'Glass')
        Q.cyl('Hall pull handle',(-side*.70,-.08,.855),(-side*.70,-.08,1.135),.010,leaf,'Zinc',8)
        for zz in (.855,1.135):Q.cyl('Hall pull standoff',(-side*.70,-.026,zz),(-side*.70,-.08,zz),.008,leaf,'Zinc',6)
        Q.join(leaf)
    for xx in (-.91,.91):Q.box('Hall entry surround',(xx,-4.47,1.36),(.12,.20,2.30),rt,'White')
    Q.box('Hall entry lintel',(0,-4.47,2.53),(1.94,.20,.14),rt,'White')
    Q.box('Hall entry canopy',(0,-4.95,2.69),(2.65,1.45,.12),rt,'Roof')
    Q.box('Hall entry landing',(0,-5.1,.16),(3.0,1.7,.15),rt,'Block')
    Q.box('Hall lower entrance step',(0,-6.02,.06),(3.0,.30,.12),rt,'Block')
    for side in (-1,1):
        Q.mesh('Hall standing seam roof', [(-6.85,0,5.05),(6.85,0,5.05),(6.85,side*4.65,3.19),(-6.85,side*4.65,3.19)],[(0,1,2,3)],rt,'Roof',upward=True)
        for j in range(33):
            xx=-6.78+j*.424
            Q.beam('Hall raised roof seam',(xx,0,5.055),(xx,side*4.65,3.195),.018,rt,'Roof',.025)
        Q.box('Hall eaves fascia',(0,side*4.65,3.15),(13.7,.038,.18),rt,'White')
    Q.box('Hall civic sign',(0,-4.37,3.02),(4.6,.065,.43),rt,'Green')
    Q.text(rt,'MEADOW PARK  /  COMMUNITY HALL',(0,-4.412,2.96),.16,'White')
    Q.join(rt)
    rt['dimensions_m']=[13,8.5,5.05];rt['scope']='original representative municipal hall, not surveyed replica'
    return rt
