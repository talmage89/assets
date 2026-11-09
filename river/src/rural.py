"""Agricultural edge: rows, fencerows, driveways, ditches and native poles."""
import math
import random
import geometry as G
import context as C
from channel import surface_z


def add(p,parent,lots):
    # Keep the native lawn's fine stubble normal, with dry harvest color.
    # Material assignment on actual terrain cannot intersect its own ground.
    G.M['hay']=G.M['grass'].copy();G.M['hay'].name='River_harvest_stubble'
    ma=G.M['hay'];ma['tiling_vertex_tint']=True
    vc=ma.node_tree.nodes.new('ShaderNodeVertexColor');vc.layer_name='Tint'
    ma.node_tree.links.new(vc.outputs['Color'],ma.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
    rng=random.Random(p.seed+501);b=G.Batch('FarmRoadsideAndYards',parent,'context')
    import bpy
    soil=bpy.context.scene.objects['BedBanksFloodplain']
    soil.data.materials.append(ma);material_index=len(soil.data.materials)-1
    tint=soil.data.color_attributes['Tint']
    # Recover each original quad from its fixed LL-to-UR diagonal. Classifying
    # its two triangles separately cuts long green teeth into a field edge.
    cells={}
    for face in soil.data.polygons:
        vertices=[soil.data.vertices[i] for i in face.vertices]
        lo=min(v.co.y for v in vertices);hi=max(v.co.y for v in vertices)
        ll=min((v for v in vertices if v.co.y==lo),key=lambda v:v.co.x)
        ur=max((v for v in vertices if v.co.y==hi),key=lambda v:v.co.x)
        cells.setdefault((ll.index,ur.index),[]).append(face)
    for faces in cells.values():
        corners=sorted({i for face in faces for i in face.vertices})
        x=sum(soil.data.vertices[i].co.x for i in corners)/len(corners)
        y=sum(soil.data.vertices[i].co.y for i in corners)/len(corners)
        edge=max(abs(p.center(y))+p.halfwidth(y)+23,45)
        # Continue the crop to the terrain's actual outer boundary.
        if not (49<abs(y)<160 and edge<abs(x)):continue
        row=math.floor((abs(y)-48)/4);value=.97+.035*math.sin(row*2.39)
        for face in faces:
            face.material_index=material_index
            for li in face.loop_indices:tint.data[li].color=(.20*value,.165*value,.078*value,1)
    for side in (-1,1):
        for end in (-1,1):
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
        steps=max(2,math.ceil(abs(end-road)))
        for j in range(steps):
            a=road+(end-road)*j/steps;c=road+(end-road)*(j+1)/steps
            pts=[(xx,yy,surface_z(p,xx,yy)+.025) for xx,yy in ((x-1.65,a),(x+1.65,a),(x+1.65,c),(x-1.65,c))]
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
