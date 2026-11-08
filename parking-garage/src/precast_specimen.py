"""Two flat precast bays for the interior photograph, using our stock kit.

The town garage has a ramp at its middle line; the photo has a flat inverted-T
seat. This calibration specimen keeps the actual sections and 11ft spacing.
It is a measured assembly comparator, not a third town garage delivery.
"""
import json,math
from pathlib import Path
import bpy
import geometry as G
import pieces
from plan import garage,TEE,SPAN,FLOOR,DEPTH,STALL
from form import remove_paint
from tee_detail import source
from build import members


def build(layout):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(Path('export/sites/ParkingGarageSite-101.gltf').resolve()));bpy.context.view_layer.update()
    old=bpy.data.objects['Garage_101'];town=bpy.data.objects['TownContext']
    parked=[o for o in town.children if o.name.startswith('Parked ')]
    actor_root=G.root('Comparison parked cars');actors=[]
    for i,x in enumerate((-7.0,-2.7,4.2,8.4)):
        cr=G.clone(parked[(i*41)%len(parked)],'Comparison car '+str(i),(x,12.0,0),180,actor_root)
        actors.append(dict(name=cr.name,triangles=G.triangles(members(cr))))
    for rr in [old,*parked]:
        for ob in reversed(members(rr)):bpy.data.objects.remove(ob,do_unlink=True)
    G.palette(Path('textures/lookdev'));rt=G.root('Garage_101',system='precast',stage='Flat two-bay calibration specimen')
    L=6*TEE;W=2*SPAN;p=garage(101)
    p.update(length=L,width=W,levels=2,tee_count=6,flat_y=-SPAN/2,ramp_y=SPAN/2,ramp_width=SPAN,
        structural_stations=[-L/2,0,L/2],ramp_limits=[-7.5,7.5],joint_y=0,towers=[],stalls=[],pieces=[])
    p['comparison_actors']=actors
    b=G.Mesh('Grade slab comparison',rt);b.box((0,0,-.08),(L,W,.16),'Deck');b.finish()
    for ix,x in enumerate((-L/2,0,L/2)):
        for iy,y in enumerate((-SPAN,0,SPAN)):
            rr=G.root(f'ColumnShaft_{ix}_{iy}',(x,y,0),rt,module_kind='ColumnCorbel');pieces.column(rr)
            for ob in rr.children:
                remove_paint(ob)
                if ob.type=='MESH':
                    for v in ob.data.vertices:
                        if abs(v.co.z-(FLOOR-1.60))<1e-6:v.co.z-=(FLOOR-1.60)*.15
                    ob.data.update()
    for x in (-L/4,L/4):
        for y in (-SPAN,0,SPAN):
            rr=G.root(f'Girder_{x}_{y}',(x,y,FLOOR),rt,module_kind='InvertedT' if y==0 else 'LBeam')
            pieces.beam(rr,edge=y!=0)
            if y<0:rr.rotation_euler.z=math.pi
    for row,cy in enumerate((-SPAN/2,SPAN/2)):
        for i in range(6):
            x=-L/2+(i+.5)*TEE
            rr=G.root(f'Flat_L2_R{row}_T{i}',(x,cy,FLOOR),rt,module_kind='DoubleTee');source(rr)
            if i%2==0:
                for yy in (cy-2.5,cy+2.5):
                    fr=G.root(f'Fixture_{row}_{i}_{yy}',(x,yy,FLOOR-.7024),rt,module_kind='Fixture');pieces.fixture(fr)
                    for ob in fr.children:
                        if ob.type=='MESH':
                            for v in ob.data.vertices:
                                if v.co.z>.30:v.co.z+=.1524
    closure=G.Mesh('Inner closure pour comparison',rt);closure.box((0,0,FLOOR-.025),(L,.08,.05),'Deck');closure.finish()
    marks=G.Mesh('Parking markings comparison',rt)
    for i,x in enumerate((-7.0,-2.7,4.2,8.4)):
        s=dict(x=x,y=12.,z=0,yaw=180,depth=DEPTH,width=STALL,level=0,ramp=False);p['stalls'].append(s)
        for xx in (x-STALL/2,x+STALL/2):marks.quad([(xx-.045,9.25,.006),(xx+.045,9.25,.006),(xx+.045,14.75,.006),(xx-.045,14.75,.006)])
    marks.finish()
    for side in (-1,1):
        for x in (-L/4,L/4):
            rr=G.root(f'Facade_0_{side}_{x}',(x,side*SPAN,0),rt,module_kind='Spandrel');pieces.spandrel(rr,refined=True)
    notice=G.Mesh('Column level and payment notice',rt)
    notice.box((.12,-.386,.80),(.45,.01,.86),'White')
    for z,h,key in ((1.08,.22,'LEVEL 2'),(.78,.10,'PAY BEFORE RETURNING'),(.57,.10,'PAY HERE')):
        notice.quad([(-.09,-.392,z-h/2),(.33,-.392,z-h/2),(.33,-.392,z+h/2),(-.09,-.392,z+h/2)],layout[key],'Graphics')
    notice.finish()
    pts=[]
    for i in range(65):
        a=i*math.tau/64;pts.append([6.3*math.cos(a)+3.5*math.copysign(1,math.cos(a)),4.2*math.sin(a),0])
    p['paths']=[dict(name='Drive_Up_Comparison',points=pts,width=7.3152)];p['pedestrian_paths']=[]
    p['bounds_m']=G.bounds(members(rt));p['garage_triangles']=G.triangles(members(rt))
    Path('build/lookdev/comparison-precast.json').write_text(json.dumps(p,indent=2)+'\n')
    return rt,p
