"""Eye-height views, structural inspections and complete reach views."""
from plan import generate


def views(seed):
    p=generate(seed);rural=p.kind=='edge';x=-26 if rural else -24;y=-59 if rural else -64
    hero_z=p.bed(x,y)+1.65 if rural else 2.30
    ux=p.water_edges(-7)[0]-.8;uz=p.bed(ux,-7)+1.65
    return dict(
        hero=dict(location=(x,y,hero_z),target=(2,0,2.25),lens=40),
        above=dict(location=(-110,-140,142),target=(0,10,0),lens=35),
        under=dict(location=(ux,-7,uz),target=(0,1,3.4),lens=26),
        pier=dict(location=(-7,-13,1.65),target=(0 if rural else -p.span/2,-2.7,1.1),lens=48),
        abutment=dict(location=(-p.length/2+9,-14,2.45),target=(-p.length/2,-1,2.4),lens=42),
        driver=dict(location=(-p.length/2-17,-1.6764,p.deck_z+1.15),target=(16,-1.6764,p.deck_z+1.14),lens=40),
        riffle=dict(location=(p.center(p.riffle_y)-p.width*.49,p.riffle_y-13,1.5),target=(p.center(p.riffle_y),p.riffle_y,.0),lens=42),
        bar=dict(location=(p.center(p.bar_y)-p.width*.56,p.bar_y-8,1.4),target=(p.center(p.bar_y)-p.width*.27,p.bar_y,.0),lens=42),
        scale=dict(location=(-p.length/2-12,-10,p.deck_z+1.65),target=(-p.length/2-3,0,p.deck_z+.8),lens=40))
