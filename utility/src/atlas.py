"""Physical, guarded reusable charts in the single Utility atlas.

Rects use a 2048 design grid, bottom-up. Reuse of manufactured stock/wood
charts is intentional and audited separately from unique-island overlaps.
"""
RECTS = {
 'PoleA': (0,0,512,2048), 'PoleB': (512,0,1024,2048),
 'Crossarm':(1024,1536,2048,2048), 'Tank':(1024,768,1664,1536),
 'Guard':(1664,768,1856,1536), 'Molding':(1856,768,2048,1536),
 'Steel':(1024,384,1536,768), 'Porcelain':(1536,384,1792,768),
 'Polymer':(1792,384,2048,768), 'Endgrain':(1024,0,1280,256),
 'Cable':(1280,0,1536,256), 'Vine':(1536,0,1792,256),
 'Recess':(1792,0,2048,256), 'Tag':(1024,256,1280,384),
 'Brand':(1280,256,1664,384), 'Rating':(1664,256,2048,384),
}
PHYSICAL = dict(PoleA=(.87,12),PoleB=(.87,12),Crossarm=(3.048,.121),
 Tank=(1.60,.86),Guard=(.164,2.44),Molding=(.038,2.6),
 Steel=(.5,.375),Porcelain=(.20,.3),Polymer=(.20,.3),
 Endgrain=(.30,.30),Cable=(.22,.22),Vine=(.08,.08),Recess=(.1,.1),
 Tag=(.065,.22),Brand=(.12,.15),Rating=(.18,.15))
GUARD = 8


def rect(role):
    a,b,c,d=RECTS[role]
    return tuple(x/2048 for x in (a+GUARD,b+GUARD,c-GUARD,d-GUARD))


def point(role,u,v):
    a,b,c,d=rect(role)
    return (a+(c-a)*u,b+(d-b)*v)
