"""Placed causal marks from Ground's existing shared decal sheet."""
import math,random
import bpy
from geo import ROOT
RECTS=dict(paint=(0,.75,.5,1),oil=(.5,.5,.75,.75),stain=(.75,.5,1,.75),
    sediment=(.5,.25,1,.5),scuff=(.125,0,.25,.125),crack=(.5,0,.625,.25),joint=(.625,0,.75,.25))


def decal(a,name,p,size,kind,seed=0,yaw=0,vertical=False):
    from kit.tiling import material
    ma=bpy.data.materials.get('CivicGround_Decals')
    if not ma:
        ma=material('GroundTrim',ROOT/'ground/textures/ship',tint=True);ma.name='CivicGround_Decals'
        bs=ma.node_tree.nodes.get('Principled BSDF');tx=next(n for n in ma.node_tree.nodes if n.type=='TEX_IMAGE' and n.image.name.startswith('T_GroundTrim_BaseColor'))
        ma.node_tree.links.new(tx.outputs['Alpha'],bs.inputs['Alpha']);ma.surface_render_method='DITHERED';ma.use_backface_culling=False
    x,y,z=p;w,h=size;r=math.radians(yaw);c,s=math.cos(r),math.sin(r)
    coords=[]
    for u,v in ((-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)):
        coords.append((x+u*c-v*s,y+u*s+v*c,z) if not vertical else (x+u,y,z+v))
    me=bpy.data.meshes.new(name);me.from_pydata(coords,[],[(0,1,2),(0,2,3)]);me.update()
    ob=bpy.data.objects.new(a.root.name+'__'+name,me);bpy.context.collection.objects.link(ob);ob.parent=a.root;me.materials.append(ma)
    ob['module_kind']='Placed'+kind;ob['cause']=name;ob['placement_seed']=seed
    uv=me.uv_layers.new(name='UVMap');l,f,r,k=RECTS[kind];g=.001
    corners=[(l+g,f+g),(r-g,f+g),(r-g,k-g),(l+g,k-g)]
    for loop in me.loops:uv.data[loop.index].uv=corners[loop.vertex_index]
    tint=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT');me.color_attributes.active_color=tint
    rng=random.Random(seed);factor=rng.uniform(.60,.95)
    for row in tint.data:row.color=(factor,factor,factor,1)
    return ob


def apron_wear(a,sp):
    p=sp['building'];x,y,_=sp['building_at'];w,d=p['width'],p['depth'];rng=random.Random(sp['seed'])
    for j in range(p['bays']):
        xx=x-w/2+.4572+(j+.5)*p['bay_width'];front=y-d/2
        for side in (-1,1):
            for k in range(7):
                yy=front-1.3-k*2.6;zz=.1524*(yy+32)/(front+32)+.003
                decal(a,f'Bay{j+1}_WheelLane_{side}_{k}',(xx+side*.94+rng.uniform(-.07,.07),yy,zz),(.24+rng.uniform(0,.09),1.8+rng.uniform(0,.7)),'scuff',j*100+k,rng.uniform(-3,3))
        for k in range(4):
            yy=front-2.3-k*3.8;zz=.1524*(yy+32)/(front+32)+.003
            decal(a,f'Bay{j+1}_OilStanding_{k}',(xx+rng.uniform(-.28,.28),yy,zz),(1.0,1.3+rng.random()),'oil',j*31+k)
    # Drain belongs at the low street end, perpendicular to the apparatus exits.
    m=a.mesh('ApronTrenchDrain',kind='TrenchDrain',trim_strip=2)
    for j in range(round(p['bayblock']/.15)):
        xx=x-w/2+j*.15
        m.box((xx,-31,.011),(.105,.30,.025),'Trim',(.045,.049,.042),r=0)
    for yy in (-31.18,-30.82):m.box((x-w/2+p['bayblock']/2,yy,.013),(p['bayblock'],.025,.03),'Trim',(.18,.19,.17),r=0)
    m.finish()
