"""Street foregrounds and closed blocks; canonical Ground turf with tints.

School's ground_finish supplies the .62/.68/.58 maintained-turf tint idiom.
No turf, paving, car, tree or host texture is changed or regenerated.
"""
import math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from kit import tiling
import geometry as G
from plan import TEE


def refine(rt,p,layout):
    L,W=p['length'],p['width'];municipal=p['system']=='precast'
    G.palette(Path('textures/lookdev'))
    sy=W/2+12.2 if municipal else 48.8;rw=12.192
    walk_x=-(L/2+14.2)-rw/2-1.6
    # Actual World-XY turf projection, rather than each lawn box's ambiguous
    # normal-sorted axes. Color stations break the felt green at mowing scale.
    lawn=tiling.material('Lawn',G.ROOT/'ground/textures/ship',tint=True);lawn.name='Garage town maintained turf'
    for ob in rt.children_recursive:
        if ob.type!='MESH' or not any(m and m.name.split('.')[0]=='Lawn' for m in ob.data.materials):continue
        ob.data=ob.data.copy();bm=bmesh.new();bm.from_mesh(ob.data)
        ids={i for i,m in enumerate(ob.data.materials) if m and m.name.split('.')[0]=='Lawn'}
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
    # Native main-street rows close the right-hand vanishing street and rear
    # cross streets at different setbacks; no billboard backdrop is used.
    block=next(o for o in rt.children if o.name.startswith('Native Main Street row'))
    for i,(pos,yaw) in enumerate([((134,0,0),90),((-135,0,0),-90),((65,112,0),0),((-60,110,0),0)]):
        G.clone(block,'Closing town block '+str(i),pos,yaw,rt)
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
    return [dict(socket='Entry queue',category='entry queue',kind=car.name,triangles=G.triangles([queued,*queued.children_recursive]),position=list(pos),yaw=180)]
