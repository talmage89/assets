"""Folded stainless fascia, rigid shaft controls and original silkscreen."""
import math
from kit import model as G
from mathutils import Matrix


def build_controls(b):
    panel=G.pivot('Control_panel',(0,0,0));panel.parent=b.root
    b.box('Fascia stainless stamping',(0,0,0),(.636,.0014,.133),'stainless',.0005,panel)
    for x in (-.318,.318):
        b.box('Fascia side return',(x,.016,0),(.0014,.032,.133),'stainless',.0006,panel)
        b.box('Fascia black edge seal',(x+.001,0,0),(.003,.005,.130),'rubber',.001,panel)
    for z in (-.067,.067):
        b.box('Fascia hem fold',(0,.008,z),(.636,.016,.0014),'stainless',.0005,panel)
        b.box('Fascia hem return',(0,.016,z-.002),(.630,.0014,.005),'stainless',.0004,panel)
    print_plane=G.plane_uv('Fascia original silkscreen',[(-.317,-.0009,-.066),(.317,-.0009,-.066),
                           (.317,-.0009,.066),(-.317,-.0009,.066)],b.mat('panel_print'))
    b.add(print_plane,panel)
    for i,x in enumerate((-.205,0,.205),1):
        b.lathe('Control fixed bezel',[(.001,.025),(-.001,.031),(-.004,.032),(-.007,.030),(-.007,.025)],
                'stainless',64 if b.high else 12,axis='Y',center=(x,0),closed=True,parent=panel)
        if b.high:b.lathe('Control bezel gasket',[(-.006,.025),(-.006,.028),(-.008,.028),(-.008,.025)],
                'rubber',48 if b.high else 16,axis='Y',center=(x,0),closed=True,parent=panel)
        knob=G.pivot(f'Knob_{i}',(0,0,0),'Y',[0,270]);knob.parent=panel
        shape=[(0,0),(0,.022),(-.003,.025),(-.010,.027),(-.020,.0265),(-.026,.024),(-.028,.021),(-.028,0)]
        b.lathe('Molded control knob',shape,'plastic',64 if b.high else 16,axis='Y',parent=knob)
        # Small mold seam, center recess and ergonomic tapered thumb paddle.
        if b.high:b.lathe('Knob front molded ring',[(-.028,.017),(-.028,.020),(-.029,.020),(-.029,.017)],
                'plastic',64 if b.high else 24,axis='Y',closed=True,parent=knob)
        outline=[(-.006,-.016),(.006,-.016),(.008,.006),(.004,.022),(-.004,.022),(-.008,.006)]
        b.profile('Knob raised thumb paddle',outline,-.035,-.027,'plastic',axis='Y',radius=.002,parent=knob)
        b.box('Knob red index',(0,-.036,.021),(.003,.001,.009),'red',.0005,knob)
        if b.high:
            for j in range(12):
                angle=math.pi+j*math.pi/11
                x0=.026*math.cos(angle);z0=.026*math.sin(angle)
                b.cylinder('Knob grip mold flute',(x0,-.021,z0),(x0,-.009,z0),.0006,'plastic',8,knob)
        for child in knob.children:child.data.transform(Matrix.Diagonal((1.12,1.04,1.12,1)))
        knob.location=(x,-.006,0)
    b.cylinder('Igniter bezel',(-.285,-.002,.027),(-.285,-.009,.027),.009,'stainless',40 if b.high else 16,panel)
    b.cylinder('Igniter rubber boot',(-.285,-.009,.027),(-.285,-.017,.027),.0067,'rubber',32 if b.high else 12,panel)
    b.cylinder('Igniter push cap',(-.285,-.017,.027),(-.285,-.020,.027),.0057,'plastic',24 if b.high else 12,panel)
    for x in (-.302,.302):
        for z in (-.051,.051):b.fastener('Fascia Phillips screw',(x,-.0009,z),radius=.0035,kind='cross',parent=panel,washer=False)
    panel.location=(0,-.277,.795);panel.rotation_euler.x=math.radians(-12)
    return panel
