"""Eye-height views, structural inspections and complete reach views."""
from plan import generate


def views(seed,plan=None):
    p=plan or generate(seed);rural=p.kind=='edge';y=-59 if rural else -64
    x=p.center(y)-p.halfwidth(y)-(7 if rural else 2.6)
    hero_z=p.bed(x,y)+.035+1.65 if rural else 2.30
    ux=p.water_edges(-7)[0]-.8;uz=p.bed(ux,-7)+1.65
    by=p.bar_y-8;inner=-p.outside;bx=p.water_edges(by)[0 if inner<0 else 1]+inner*.50;bz=p.bed(bx,by)+1.65
    ry=p.riffle_y-13;rx=p.water_edges(ry)[0]-.35;rz=p.bed(rx,ry)+1.65
    # The widened bend moves this bank. Clear the accepted town terrace too,
    # so one camera gives useful before/after images of both channel shapes.
    if not rural:rz=max(rz,4.8)
    bearing_y=-p.deck_width/2-2.2;bearing_x=p.water_edges(bearing_y)[0]-1.4
    bearing_target_x=-p.length/2+.40 if rural else -p.length/2+p.span
    rural_abutment_x=p.water_edges(-13)[0]-2.0
    abutment_x=p.water_edges(-7.6)[0]-1.2;abutment_z=p.bed(abutment_x,-7.6)+1.65
    return dict(
        hero=dict(location=(x,y,hero_z),target=(2,0,2.25),lens=40),
        above=dict(location=(-110,-140,142),target=(0,10,0),lens=35),
        under=dict(location=(ux,-7,uz),target=(0,1,3.4),lens=26,exposure=.3),
        bearings=dict(location=(bearing_x,bearing_y,p.bed(bearing_x,bearing_y)+2.0),target=(bearing_target_x,-p.deck_width/2+.95,p.deck_z-.32-1.143-.10),lens=110,exposure=1.4),
        pier=dict(location=(-7,-13,1.65),target=(0 if rural else -p.span/2,-2.7,1.1),lens=48),
        abutment=dict(location=(rural_abutment_x,-13,p.bed(rural_abutment_x,-13)+1.65) if rural else (abutment_x,-7.6,abutment_z),target=(-p.length/2-.4,-4.0,2.1),lens=34,exposure=.9),
        driver=dict(location=(-p.length/2-24,-1.6764,p.deck_z+1.15),target=(16,-1.6764,p.deck_z+1.14),lens=40),
        riffle=dict(location=(rx,ry,rz),target=(p.center(p.riffle_y),p.riffle_y,.0),lens=42),
        bar=dict(location=(bx,by,bz),target=(p.center(p.bar_y)+inner*p.width*.27,p.bar_y,.0),lens=42),
        scale=dict(location=(-p.length/2-12,-10,p.deck_z+1.65),target=(-p.length/2-3,0,p.deck_z+.8),lens=40))
