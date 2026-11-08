"""Agricultural edge: rows, fencerows, driveways, ditches and native poles."""
import math
import random
import geometry as G
import context as C
from channel import surface_z


def add(p,parent,lots):
    if 'hay' not in G.M:
        from materials import plain
        G.M['hay']=plain('River_hay',(.24,.205,.09),.97)
    ma=G.M['hay'];ma['tiling_vertex_tint']=True
    vc=ma.node_tree.nodes.new('ShaderNodeVertexColor');vc.layer_name='Tint'
    ma.node_tree.links.new(vc.outputs['Color'],ma.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
    rng=random.Random(p.seed+501);b=G.Batch('FarmRoadsideAndYards',parent,'context')
    # Dry late-summer hay swaths follow the fields, not an axis-aligned turf
    # checker. Streamable field ribbons use the existing bank/lawn images.
    for side in (-1,1):
        for end in (-1,1):
            for j in range(36):
                y=end*(49+j*3.1);c=y+end*3.11
                edge=max(abs(p.center(y))+p.halfwidth(y)+23,45)
                for x0,x1 in ((edge,85),(85,135),(135,170)):
                    if x1<=x0:continue
                    value=rng.uniform(.92,1.04);col=(.24*value,.205*value,.09*value,1)
                    pts=[(side*x,yy,surface_z(p,side*x,yy)+.012) for x,yy in ((x0,y),(x1,y),(x1,c),(x0,c))]
                    b.geom(pts,[(0,1,2,3)],'hay',col,up=True)
            # Post-and-wire field boundary with uneven, supported volunteers.
            for j in range(32):
                x=side*(40+j*4);y=end*44;z=surface_z(p,x,y)
                b.box((x,y,z+.52),(.11,.10,1.12),'wood')
                if j:
                    for h in (.45,.85):
                        b.tube([(x-side*4,y,surface_z(p,x-side*4,y)+h),(x-side*2,y,z+h-.025),(x,y,z+h)],.0025,'steel',4)
                if j%3==1:
                    C.instance(C.REPO/'school/build/context/shrub.glb',f'Field hedge {side} {end} {j}',(x,y,z-.02),parent,rng.uniform(0,360),rng.uniform(.8,1.5),category='vegetation')
    # Broad shallow roadside swales and their gravel shoulders. Terrain owns
    # the ditch section; these ribbons carry the exposed gravel at the road.
    for side in (-1,1):
        for x in range(-145,145,3):
            if abs(x)<p.length/2+8:continue
            pts=[(xx,yy,surface_z(p,xx,yy)+.018) for xx,yy in ((x,side*5.1),(x+3,side*5.1),(x+3,side*6.6),(x,side*6.6))]
            b.geom(pts,[(0,1,2,3)],'bank',(.9,.86,.72,1),up=True)
    for i,(x0,x1,y0,y1) in enumerate(lots):
        x=(x0+x1)/2;y=(y0+y1)/2;s=1 if y>0 else -1
        road=s*5.0;end=y-s*7
        # Driveway grade to the actual porch/yard elevation.
        pts=[(xx,yy,surface_z(p,xx,yy)+.04) for xx,yy in ((x-1.65,road),(x+1.65,road),(x+1.65,end),(x-1.65,end))]
        b.geom(pts,[(0,1,2,3)],'bank',(.92,.89,.80,1),up=True)
        mx=x-2.4;my=s*6.8;z=surface_z(p,mx,my)
        # Small original rural box uses the native mailbox's arch vocabulary.
        b.box((mx,my,z+.53),(.089,.089,1.06),'wood')
        section=[(-.10,0),(-.10,.12)]+[(.10*math.cos(t),.12+.10*math.sin(t)) for t in [math.pi-j*math.pi/8 for j in range(9)]]+[(.10,0)]
        b.loft([[(mx+a,my+yy,z+1.04+h) for a,h in section] for yy in (-.22,.22)],'steel')
        b.box((mx+.106,my,z+1.20),(.008,.12,.028),'rust')
    # The original utility cache includes several module examples. Select one
    # actual tangent pole and retain conductor sockets and native hardware.
    for side in (-1,1):
        poles=[]
        for x in range(46,230,38):
            xx=side*x;y=9.6;z=surface_z(p,xx,y)
            pole=C.instance(C.REPO/'school/build/context/utility.glb',f'County pole {side} {x}',(xx,y,z),parent,90,select='Tangent')
            poles.append(pole)
        import bpy
        bpy.context.view_layer.update()
        for a,c in zip(poles,poles[1:]):
            for key in ('Primary_B','Primary_C','Primary_A','Neutral','Telephone'):
                start=next(o.matrix_world.translation.copy() for o in a.children_recursive if o.name.endswith('__Socket_'+key))
                end=next(o.matrix_world.translation.copy() for o in c.children_recursive if o.name.endswith('__Socket_'+key))
                pts=[]
                for j in range(17):
                    t=j/16;point=start*(1-t)+end*t;point.z-=.55*4*t*(1-t);pts.append(point)
                b.tube(pts,.009 if key=='Telephone' else .005,'steel',5)
    b.finish()
