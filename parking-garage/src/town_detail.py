"""Street foregrounds and closed blocks; canonical Ground turf with tints.

School's ground_finish supplies the .62/.68/.58 maintained-turf tint idiom.
No turf, paving, car, tree or host texture is changed or regenerated.
"""
import math,random,numpy as np
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from mathutils import Quaternion
from mathutils.bvhtree import BVHTree
from kit import tiling
import geometry as G
from plan import TEE


def fit_queue(car):
    """Fit four native wheel patches to the actual apron triangles."""
    bpy.context.view_layer.update();inv=car.matrix_world.inverted();points=[]
    for ob in car.children_recursive:
        if ob.type=='MESH':points.extend(inv@ob.matrix_world@v.co for v in ob.data.vertices)
    low=min(v.z for v in points);groups={}
    for v in points:
        if v.z<low+.003:groups.setdefault((v.x>0,v.y>0),[]).append(v)
    assert len(groups)==4,('Native wheel patch groups',len(groups))
    contacts=[Vector((sum(v.x for v in vs)/len(vs),sum(v.y for v in vs)/len(vs),min(v.z for v in vs))) for vs in groups.values()]
    apron=next(o for o in bpy.context.scene.objects if o.name.startswith('Private entry and accessible street walk'))
    apron.data.calc_loop_triangles();vs=[apron.matrix_world@v.co for v in apron.data.vertices]
    faces=[tuple(t.vertices) for t in apron.data.loop_triangles if (apron.matrix_world.to_3x3()@t.normal).z>.7]
    surface=BVHTree.FromPolygons(vs,faces,all_triangles=True)
    def sample(point):
        hit=surface.ray_cast(point+Vector((0,0,1)),Vector((0,0,-1)),2)
        assert hit[0] is not None,point
        return hit[0].z
    world=[car.matrix_world@v for v in contacts];heights=[sample(v) for v in world]
    a,b,c=np.linalg.lstsq([[v.x,v.y,1] for v in world],heights,rcond=None)[0]
    before=max(abs(v.z-z) for v,z in zip(world,heights));yaw=car.rotation_euler.z
    car.rotation_mode='QUATERNION';car.rotation_quaternion=Vector((0,0,1)).rotation_difference(Vector((-a,-b,1)).normalized())@Quaternion((0,0,1),yaw)
    car.location.z=float(a*car.location.x+b*car.location.y+c-low);bpy.context.view_layer.update()
    errors=[abs((car.matrix_world@v).z-sample(car.matrix_world@v)) for v in contacts]
    assert max(errors)<.001,errors
    return dict(samples=4,before_max_gap_m=before,after_max_abs_gap_m=max(errors),method='Native low tire patches / actual apron BVH / fitted rigid support plane')


def refine(rt,p,layout):
    L,W=p['length'],p['width'];municipal=p['system']=='precast'
    G.palette(Path('textures/lookdev'))
    sy=W/2+12.2 if municipal else 48.8;rw=12.192
    walk_x=-(L/2+14.2)-rw/2-1.6
    # Actual World-XY turf projection, rather than each lawn box's ambiguous
    # normal-sorted axes. Color stations break the felt green at mowing scale.
    lawn=tiling.material('Lawn',G.ROOT/'ground/textures/ship',tint=True);lawn.name='Garage town maintained turf'
    G.M['TurfFringe']=lawn;fringe=G.Mesh('Mown verge boundary blades',rt);rng=random.Random(p['seed']+958)
    for ob in rt.children_recursive:
        if ob.type!='MESH' or not any(m and m.name.split('.')[0]=='Lawn' for m in ob.data.materials):continue
        ob.data=ob.data.copy();bm=bmesh.new();bm.from_mesh(ob.data)
        ids={i for i,m in enumerate(ob.data.materials) if m and m.name.split('.')[0]=='Lawn'}
        # A few centimetres of mown blades soften the actual paving boundary.
        # Reuse Lawn itself, no alpha atlas or second turf texture set.
        border={}
        for f in ob.data.polygons:
            if f.material_index not in ids or f.normal.z<.7:continue
            seq=list(f.vertices)
            for a,c in zip(seq,seq[1:]+seq[:1]):border.setdefault(tuple(sorted((a,c))),[]).append((a,c))
        for uses in border.values():
            if len(uses)!=1:continue
            a,c=[ob.matrix_world@ob.data.vertices[i].co for i in uses[0]];delta=c-a
            if delta.xy.length<.2:continue
            inside=Vector((-delta.y,delta.x,0)).normalized()
            for j in range(min(70,int(delta.length/.65))):
                base=a.lerp(c,(j+.35)/max(1,int(delta.length/.65)))+inside*.045
                for k in range(5):
                    foot=base+inside*rng.uniform(0,.045);foot.z+=.002
                    tip=foot+Vector((rng.uniform(-.02,.02),rng.uniform(-.02,.02),rng.uniform(.025,.055)))
                    side=Vector((math.cos(k*1.7),math.sin(k*1.7),0))*rng.uniform(.002,.004)
                    fringe.geom([foot-side,foot+side,tip],[(0,1,2)],'TurfFringe')
        turf=[f for f in bm.faces if f.material_index in ids and f.normal.z>.7]
        edges=list({e for f in turf for e in f.edges})
        bmesh.ops.subdivide_edges(bm,edges=edges,cuts=5,use_grid_fill=True)
        bm.to_mesh(ob.data);bm.free();ob.data.update()
        for i in ids:ob.data.materials[i]=lawn
        uv=ob.data.uv_layers.active;attr=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER');ob.data.color_attributes.active_color=attr
        for f in ob.data.polygons:
            for li in f.loop_indices:
                q=ob.matrix_world@ob.data.vertices[ob.data.loops[li].vertex_index].co
                attr.data[li].color=(1,1,1,1)
                if f.material_index in ids:
                    var=.88+.10*math.sin(q.x*.27+math.sin(q.y*.15))+.06*math.sin(q.y*.64)
                    attr.data[li].color=(.62*var,.68*var,.58*var,1)
                    if abs(f.normal.z)>.6:uv.data[li].uv=(q.x/3.048,q.y/3.048)
    grass=fringe.finish()
    if grass:
        attr=grass.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER');grass.data.color_attributes.active_color=attr
        for row in attr.data:row.color=(.62,.68,.58,1)
    # Native main-street rows close the right-hand vanishing street and rear
    # cross streets at different setbacks; no billboard backdrop is used.
    block=next(o for o in rt.children if o.name.startswith('Native Main Street row'))
    for i,(pos,yaw) in enumerate([((134,0,0),90),((-135,0,0),-90),((65,78 if municipal else 112,0),0),((-60,110,0),0)]):
        G.clone(block,'Closing town block '+str(i),pos,yaw,rt)
    if municipal:G.clone(block,'Northeast closing frontage',(146,88,0),90,rt)
    b=G.Mesh('Street markings and meter hardware',rt)
    for sign in (-1,1):
        yy=sign*sy
        for x in range(-115,116,7):
            b.quad([(x-1.4,yy-.065,-.017),(x+1.4,yy-.065,-.017),(x+1.4,yy+.065,-.017),(x-1.4,yy+.065,-.017)],None,'Yellow')
    # Parking meters, poles and planted street trees frame the view from the
    # opposite sidewalk; clear the entry's queue reservation and public walk.
    for i,x in enumerate(range(-45,46,9)):
        yy=-sy-rw/2-.65
        b.tube([(x,yy,0),(x,yy,1.18)],.026,'Steel')
        b.box((x,yy,1.29),(.19,.14,.24),'Steel');b.box((x,yy-.073,1.32),(.13,.007,.07),'Seal')
        b.box((x+.055,yy-.078,1.22),(.045,.012,.013),'Steel')
    sx=walk_x+.9;yy=-W/2+5
    b.tube([(sx,yy,0),(sx,yy,2.8)],.03,'Steel');b.box((sx,yy,2.52),(.45,.035,.58),'Steel')
    b.quad([(sx-.21,yy-.020,2.25),(sx+.21,yy-.020,2.25),(sx+.21,yy-.020,2.79),(sx-.21,yy-.020,2.79)],layout['2 HOUR PARKING'],'Graphics')
    b.finish()
    near=G.Mesh('Near crossing parking meters',rt)
    near.box((walk_x,0,-.08),(3.2,2*(sy-rw/2),.16),'GroundConcrete')
    for yy in (-W/2-2,-W/2+5):
        xx=walk_x+.9
        near.tube([(xx,yy,0),(xx,yy,1.17)],.026,'Steel')
        near.box((xx,yy,1.29),(.20,.15,.25),'Steel');near.box((xx-.103,yy,1.32),(.006,.105,.08),'Seal')
    near.finish()
    tree=next(o for o in rt.children if o.name.startswith('Library RedMaple'))
    for i,xx in enumerate((-L/2-2,-L/2+12,12,L/2+9)):
        # Trees are planted outside the 1.83m walk, on the far curb's verge.
        G.clone(tree,'Opposite street tree '+str(i),(xx,-sy-rw/2-3.65,0),i*57,rt)
    # A smaller native street tree at the crossing is visible in the hero.
    # Its narrow soil well leaves the long side walk clear beside it.
    tree_x=walk_x-1.1
    t=G.clone(tree,'Crossing street tree',(tree_x,-W/2-4.7,0),37,rt);t.scale=(.50,.50,.50)
    G.M['Soil']=G.material('Tree well soil',(.065,.047,.024),.98)
    soil=G.Mesh('Crossing tree well',rt);soil.box((tree_x,-W/2-4.7,.001),(.70,.85,.006),'Soil');soil.finish()
    # The entry queue is a separate actor, shared native mesh, not garage
    # geometry. Place at the actual apron before the clearance gantry.
    car=next(o for o in rt.children if o.name.startswith('Street parked '))
    ex=L/2-p['end_length']/2
    pos=(ex-1.65,-W/2-3.3,0)
    queued=G.clone(car,'Entry queue vehicle',pos,180,rt)
    support=fit_queue(queued)
    return [dict(socket='Entry queue',category='entry queue',kind=car.name,triangles=G.triangles([queued,*queued.children_recursive]),position=list(queued.location),quaternion=list(queued.rotation_quaternion),wheel_support=support,yaw=180)]
