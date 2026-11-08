"""Soft alpha weather from joints, drains, water level and maintenance.

All masks live in the accepted 512 bank-card sheet. Broad color evidence
belongs in texture, not pointed geometry. Native concrete maps stay identical.
"""
import math
import random
import geometry as G


def chart(k):
    x=256+k%2*128;y=k//2*128
    return [(x/512+.002,1-(y+128)/512+.002),((x+128)/512-.002,1-(y+128)/512+.002),
            ((x+128)/512-.002,1-y/512-.002),(x/512+.002,1-y/512-.002)]


def wet_chart():
    # Runoff originates at the top; algae originates at the water. Reversing
    # this chart makes the wet band fade upward instead of ending in blocks.
    return [(u,1.75-v) for u,v in chart(0)]


def add(p,parent):
    rng=random.Random(940+p.seed);b=G.Batch('TextureDrivenBridgeAge',parent,'bridge')
    bottom=p.deck_z-.32-1.143;seat=bottom-.30;outer=p.deck_width/2-.95
    def vertical(x,y,z,w,h,k=0,color=(1,1,1,1)):
        b.geom([(x-w/2,y,z-h),(x+w/2,y,z-h),(x+w/2,y,z),(x-w/2,y,z)],[(0,1,2,3)],'maintenance',color,uv=chart(k))
    for j in (0,p.spans):
        x=-p.length/2+j*p.span+(.4 if j==0 else -.4)
        for side in (-1,1):
            vertical(x,side*(outer+.306),seat+.22,.43,.019,0,(.95,.31,.075,1))
            vertical(x,side*(outer+.266),seat+.30,.36,.016,0,(.78,.29,.09,1))
    for i in range(p.spans):
        a=-p.length/2+i*p.span
        for side in (-1,1):
            for x in (a+p.span*.28,a+p.span*.73):
                # Scupper splash fans on the exposed web and lower flange.
                vertical(x,side*(outer+.090),bottom+.85,rng.uniform(.8,1.9),.48,0,(.67,.66,.59,1))
                vertical(x+.13,side*(outer+.280),bottom+.177,1.5,.15,0)
                vertical(x,side*(p.deck_width/2+.002),p.deck_z-.13,1.3,.18,0)
            # Plow/spray dirt at the parapet toe, with broken intervals.
            for j in range(5):
                x=a+(j+.25+rng.random()*.5)*p.span/5
                w=rng.uniform(1.1,3.1)
                pts=[]
                for xx,h in ((x-w/2,.002),(x+w/2,.002),(x+w/2,.15),(x-w/2,.15)):
                    y=side*(p.deck_width/2-max(0,h-.0762)+.002)
                    pts.append((xx,y,p.deck_z+.085344+h))
                b.geom(pts,[(0,1,2,3)],'maintenance',(.60,.57,.51,1),uv=chart(0))
            for j in range(2):
                x=a+rng.uniform(1,p.span-1)
                vertical(x,side*(outer+.090),bottom+.82,rng.uniform(.35,.85),.40,2)
    for j in range(1,p.spans):
        x=-p.length/2+j*p.span
        for side in (-1,1):
            yy=side*(p.deck_width/2-.3+.002)
            for k in range(3):
                vertical(x+rng.uniform(-.55,.55),yy,seat-.045,rng.uniform(.34,.70),rng.uniform(.55,.98),k%2)
            vertical(x+.3,yy,seat-.42,.8,.45,2)
            # Irregular mismatched gray paint over old tags.
            if j%2:
                vertical(x-.2,yy,seat-.12,1.35,.58,3,(.86,.87,.84,1))
        for side in (-1,1):
            for dx in (-.4,.4):
                # Oxide originates at the steel/elastomer bearing interface.
                vertical(x+dx,side*(outer+.306),seat+.22,.43,.019,0,(.95,.31,.075,1))
                vertical(x+dx,side*(outer+.266),seat+.30,.36,.016,0,(.78,.29,.09,1))
        # Stained actual columns: mapped patches around each circumference.
        if p.pier=='columns':
            for cy in (-p.deck_width*.29,0,p.deck_width*.29):
                for k in range(32):
                    t=k*math.tau/32;c=(k+1)*math.tau/32
                    lo=-.03;hi=lambda a:.35+.035*math.sin(a*3+cy)+.025*math.sin(a*7)
                    vs=[(x+.602*math.cos(a),cy+.602*math.sin(a),z) for a,z in ((t,lo),(c,lo),(c,hi(c)),(t,hi(t)))]
                    uv=wet_chart();u0=.502+.246*k/32;u1=.502+.246*(k+1)/32
                    uv=[(u0,uv[0][1]),(u1,uv[1][1]),(u1,uv[2][1]),(u0,uv[3][1])]
                    b.geom(vs,[(0,1,2,3)],'maintenance',(.40,.58,.22,1),uv=uv)
                for k in range(5):
                    # Joint runoff on the front quadrant of the cylinder.
                    t=(22+k)*math.tau/32;c=t+math.tau/32
                    top=seat-1.10;low=top-rng.uniform(.60,1.20)
                    vs=[(x+.602*math.cos(a),cy+.602*math.sin(a),z) for a,z in ((t,low),(c,low),(c,top),(t,top))]
                    b.geom(vs,[(0,1,2,3)],'maintenance',(.75,.72,.61,1),uv=chart(0))
        else:
            # The cutwater follows flow, so copy/clip the actual stem facets
            # for its wetting marks instead of assuming an axis-aligned box.
            import bpy
            stem=next(o for o in parent.children_recursive if o.type=='MESH' and o.name==f'Pier_{j}__Substructure')
            bpy.context.view_layer.update();seen=set()
            for face in stem.data.polygons:
                if abs(face.normal.z)>.15:continue
                points=[stem.matrix_world@stem.data.vertices[k].co for k in face.vertices]
                if min(v.z for v in points)>.45 or max(v.z for v in points)<-.05:continue
                # Use authored horizontal face endpoints to retain its flow
                # alignment, with independent high-water top variation.
                xy=list(dict.fromkeys((round(v.x,6),round(v.y,6)) for v in points))
                if len(xy)!=2:continue
                key=(tuple(sorted(xy)),round(min(v.z for v in points),5),round(max(v.z for v in points),5))
                if key in seen:continue
                seen.add(key)
                lo=max(-.05,min(v.z for v in points));hi=min(rng.uniform(.24,.43),max(v.z for v in points))
                if hi<=lo:continue
                normal=stem.matrix_world.to_3x3()@face.normal
                vs=[(xx+normal.x*.002,yy+normal.y*.002,z) for (xx,yy),z in ((xy[0],lo),(xy[1],lo),(xy[1],hi),(xy[0],hi))]
                b.geom(vs,[(0,1,2,3)],'maintenance',(.40,.58,.22,1),uv=wet_chart())
        # Cup-like mud nests at protected girder/cap junctions, no floating
        # balls: flattened backs intersect their supporting soffits.
        for k in range(6):
            cy=rng.uniform(-outer,outer);xx=x+rng.choice((-.55,.55));z=p.deck_z-.32+.002
            rings=[[(xx+rx*math.cos(t),cy+ry*math.sin(t),zz) for t in [q*math.tau/8 for q in range(8)]]
                   for rx,ry,zz in ((.06,.04,z-.16),(.14,.09,z-.06),(.13,.085,z))]
            b.loft(rings,'bank',(.85,.77,.62,1),caps=False)
    b.finish()
    walls=G.Batch('FloodwallWeepAge',parent,'site')
    for side in (-1,1):
        if p.kind!='downtown':break
        for j in range(150):
            a=-150+j*2;c=a+2;hi=rng.uniform(.17,.36)
            pts=[]
            for yy,z in ((a,p.water_z(a)-.03),(c,p.water_z(c)-.03),(c,p.water_z(c)+hi),(a,p.water_z(a)+hi)):
                pts.append((p.center(yy)+side*(p.halfwidth(yy)+.998),yy,z))
            u0=.502+.246*(j%4)/4;u1=u0+.246/4
            walls.geom(pts,[(0,1,2,3)],'maintenance',(.40,.58,.22,1),uv=[(u0,.998),(u1,.998),(u1,.752),(u0,.752)])
        for y in (-33,59):
            pts=[(p.center(yy)+side*(p.halfwidth(yy)+.997),yy,z)
                 for yy,z in ((y-.8,-.02),(y+.8,-.02),(y+.8,.62),(y-.8,.62))]
            walls.geom(pts,[(0,1,2,3)],'maintenance',(.55,.61,.35,1),uv=chart(0))
        for j in range(30):
            y=-143+j*9.7+rng.uniform(-2,2)
            x=p.center(y)+side*(p.halfwidth(y)+4.198)
            # Each stain starts at a physical weep hole. Pattern intervals
            # vary with repaired wall bays; no perfectly even row of drips.
            walls.tube([(x,y,1.8),(x-side*.04,y,1.8)],.045,'rubber',8)
            h=rng.uniform(.7,1.2);w=rng.uniform(.4,.85)
            pts=[(p.center(yy)+side*(p.halfwidth(yy)+4.197),yy,z) for yy,z in ((y-w/2,1.8-h),(y+w/2,1.8-h),(y+w/2,1.8),(y-w/2,1.8))]
            walls.geom(pts,[(0,1,2,3)],'maintenance',(.67,.73,.52,1),uv=chart(0))
    if walls.v:walls.finish()
