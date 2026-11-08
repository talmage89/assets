"""Eye-height views, structural inspections and complete reach views."""
from plan import generate


def views(seed,plan=None):
    p=plan or generate(seed);rural=p.kind=='edge';y=-59 if rural else -64
    x=p.center(y)-p.halfwidth(y)-(7 if rural else 2.6)
    hero_z=p.bed(x,y)+.035+1.65 if rural else 2.30
    ux=p.water_edges(-7)[0]-.8;uz=p.bed(ux,-7)+1.65
    by=p.bar_y-8;inner=-p.outside;bx=p.water_edges(by)[0 if inner<0 else 1]+inner*.50;bz=p.bed(bx,by)+1.65
    ry=p.riffle_y-13;rx=p.water_edges(ry)[0]-.35;rz=p.bed(rx,ry)+1.65
    return dict(
        hero=dict(location=(x,y,hero_z),target=(2,0,2.25),lens=40),
        above=dict(location=(-110,-140,142),target=(0,10,0),lens=35),
        under=dict(location=(ux,-7,uz),target=(0,1,3.4),lens=26,exposure=.3),
        bearings=dict(location=(-p.length/2+2.4,-p.deck_width/2-2.1,2.55),target=(-p.length/2+.40,-p.deck_width/2+.95,2.88),lens=52,exposure=.5),
        pier=dict(location=(-7,-13,1.65),target=(0 if rural else -p.span/2,-2.7,1.1),lens=48),
        abutment=dict(location=(-p.length/2+8,-13,2.35),target=(-p.length/2-.9,-4.4,2.35),lens=34,exposure=.1),
        driver=dict(location=(-p.length/2-24,-1.6764,p.deck_z+1.15),target=(16,-1.6764,p.deck_z+1.14),lens=40),
        riffle=dict(location=(rx,ry,rz),target=(p.center(p.riffle_y),p.riffle_y,.0),lens=42),
        bar=dict(location=(bx,by,bz),target=(p.center(p.bar_y)+inner*p.width*.27,p.bar_y,.0),lens=42),
        scale=dict(location=(-p.length/2-12,-10,p.deck_z+1.65),target=(-p.length/2-3,0,p.deck_z+.8),lens=40))
