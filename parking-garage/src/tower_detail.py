"""Panelized 1980s/90s cores; viewable flights, shaft cap and entry fittings.

Harmon (2012) informs exposed flights/landings; Ratto (2008) informs the
glazed stair beside an opaque panelled lift shaft. Original architecture.
"""
import math
from geometry import Mesh,root
from plan import FLOOR


def add(r,levels,H):
    b=Mesh(r.name+'__Envelope details',r)
    # Glazed street return with half-level transoms, clear low-iron panes.
    for lev in range(levels):
        z=lev*FLOOR
        for half in range(2):
            lo=z+half*FLOOR/2+.09;hi=min(H-.04,z+(half+1)*FLOOR/2-.04)
            if hi<=lo:continue
            for a,c in ((-2.40,-.65),(-.60,1.02)):
                b.box((-2.713,(a+c)/2,(lo+hi)/2),(.012,c-a,hi-lo),'Glass')
            b.box((-2.75,-.69,z+half*FLOOR/2+.025),(.10,3.78,.13),'Steel')
        for yy in (-2.43,-.625,1.06):b.box((-2.75,yy,z+min(3,H-z)/2),(.10,.05,min(3,H-z)),'Steel')
        # The half landing's exposed edge and its guard remain legible behind
        # the glass. Vertical pickets belong to the landing, not the curtain.
        if lev<levels-1:
            zmid=z+FLOOR/2
            b.beam((-2.50,-2.45,zmid+1.07),(.10,-2.45,zmid+1.07),.038,.038)
            for j in range(23):
                xx=-2.5+j*2.6/22
                b.beam((xx,-2.45,zmid+.02),(xx,-2.45,zmid+1.07),.016,.016)
        # Precast panels set off the lift shaft; joints stop at the concrete
        # arrises. Shallow cover panels give real returns and shadow reveals.
        for a,c in ((.38,1.45),(1.48,2.59)):
            b.box(((a+c)/2,-2.724,z+min(FLOOR,H-z)/2),(c-a,.045,min(FLOOR,H-z)-.026))
        for a,c in ((-2.57,-.89),(.89,2.57)):
            b.box((2.814,(a+c)/2,z+min(FLOOR,H-z)/2),(.028,c-a,min(FLOOR,H-z)-.025))
        b.box((2.714,0,z+min(FLOOR,H-z)/2),(.012,1.68,min(FLOOR,H-z)-.10),'Glass')
        b.box((2.77,0,z+.005),(.10,1.78,.12),'Steel')
        for yy in (-.85,.85):b.box((2.77,yy,z+1.5),(.10,.065,3.0),'Steel')
        # Landing call panel and a conventional recessed door surround.
        b.box((2.20,2.902,z+1.10),(.12,.025,.25),'Steel')
        for zz in (1.06,1.15):b.box((2.20,2.9185,z+zz),(.035,.008,.035),'White')
        for xx in (.51,2.09):b.box((xx,2.825,z+1.1),(.065,.035,2.2),'Steel')
        # Formed sheet pockets conceal the full landing/inner-panel travel.
        # Their inner side is an open mouth; a return there would block the
        # sliding leaf. Closed 2mm skins give the solid-motion sampler real
        # thickness; concrete closes the rear of each assembled pocket.
        for lo,hi,outer in ((-.20,.55,-.20),(2.05,2.80,2.80)):
            y0,y1=2.701,2.88;bottom,top=z+.006,z+2.17
            b.box(((lo+hi)/2,y1-.001,(bottom+top)/2),(hi-lo,.002,top-bottom),'Stainless')
            b.box((outer+(.001 if outer==lo else -.001),(y0+y1)/2,(bottom+top)/2),(.002,y1-y0,top-bottom),'Stainless')
            for zz in (bottom+.001,top-.001):b.box(((lo+hi)/2,(y0+y1)/2,zz),(hi-lo,y1-y0,.002),'Stainless')
    # Elevator overrun and separate machine-room hood, vent and folded coping.
    b.box((1.48,0,H+.51),(2.42,5.37,.84))
    b.box((1.48,0,H+.98),(2.60,5.55,.10),'Steel')
    for j in range(7):b.box((1.48,-2.696,H+.27+j*.065),(1.48,.04,.026),'Steel')
    for xx in (-2.84,2.84):b.box((xx,0,H+.21),(.08,5.66,.08),'Steel')
    for yy in (-2.79,2.79):b.box((0,yy,H+.21),(5.76,.08,.08),'Steel')
    b.box((-2.75,-.69,H-.005),(.10,3.78,.07),'Steel')
    # Street-door canopy, folded drip, brackets and wall lanterns. No props in
    # the swing volume or on the upper stair/lift route.
    b.box((-3.25,1.83,2.45),(1.3,1.7,.11),'Steel')
    b.box((-3.87,1.83,2.40),(.045,1.7,.12),'Steel')
    for yy in (1.10,2.53):b.beam((-2.83,yy,2.0),(-3.68,yy,2.4),.035,.035)
    b.box((-2.84,2.54,1.72),(.10,.12,.30),'Steel')
    b.box((-2.898,2.54,1.72),(.018,.085,.22),'Light')
    for xx,wall in ((.40,.35),(2.53,2.60)):
        b.beam((xx,1.435,.05),(xx,1.435,H+.4),.055,.07)
        for lev in range(levels):b.box(((xx+wall)/2,1.435,lev*FLOOR+1), (abs(xx-wall),.10,.045),'Steel')
    # Fixed ground-level car enclosure visible through the shaft inspection
    # glazing; no moving cab or simulated lift mechanics are claimed.
    b.box((1.43,1.435,2.31),(1.9,2.6,.12),'White')
    b.box((1.43,1.435,-.07),(1.9,2.6,.14),'Steel')
    b.box((1.43,1.435,.002),(1.78,2.45,.004),'Seal')
    b.box((1.43,.165,1.125),(1.9,.06,2.25),'Stainless')
    for xx in (.48,2.38):b.box((xx,1.4125,1.125),(.06,2.555,2.25),'Stainless')
    for xx in (.43,2.48):
        for zz in (.35,2.0):b.box((xx,1.435,zz),(.10,.14,.10),'Steel')
    b.box((1.43,1.435,2.246),(.25,.65,.008),'Light')
    for lev in range(levels):
        b.box((.105,1.9,lev*FLOOR+2.65),(.09,.70,.18),'Steel')
        b.box((.055,1.9,lev*FLOOR+2.65),(.012,.62,.13),'Light')
    b.finish()
    root(r.name+'__StairDaylight',(-2.10,-.7,H/2),r,socket_kind='daylight_core')
    for lev in range(levels):
        root(r.name+f'__StairFixture_{lev}',(.025,1.9,lev*FLOOR+2.55),r,socket_kind='light_emitter',emitter_down_watts=35,emitter_up_watts=0)
    root(r.name+'__CabinLamp',(1.43,1.435,2.235),r,socket_kind='light_emitter',emitter_down_watts=14,emitter_up_watts=0,emitter_size_x=.25,emitter_size_y=.65,downlight_offset=.002)
    root(r.name+'__CabinFloor',(1.43,1.435,.004),r,socket_kind='fixed_cabin_floor')
