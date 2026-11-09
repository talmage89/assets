"""Block-scale context with native buildings at individually drawn lot widths."""
import math,random
from pathlib import Path
import geometry as G
from library import instance,car


def pad(name,rect,role='asphalt',z=-.01):
    from siteworks import slab
    return slab(name,rect,z,role,None)


def house(i,x,y,yaw,width=24):
    # Fronts and driveways face the adjoining street. Variants change native
    # plan and exterior, rather than repeating a single ranch on bare ground.
    files=('HearthfieldCape-34','HearthfieldRanch-11','Hearthfield-2','HearthfieldRanch-14','HearthfieldCape-32','Hearthfield-6')
    rt=instance(G.ROOT/f'houses/export/{files[i%6]}.gltf',f'Neighbor lot {i:02}',(x,y,0),yaw,actor='town')
    angle=math.radians(yaw);cs,sn=math.cos(angle),math.sin(angle)
    def world(u,v,z=0):return (x+cs*u-sn*v,y+sn*u+cs*v,z)
    # Native front datums vary; measure the envelope before placing the walk.
    import bpy
    from mathutils import Vector
    bpy.context.view_layer.update();inv=rt.matrix_world.inverted()
    pts=[inv@o.matrix_world@v.co for o in rt.children_recursive if o.type=='MESH' for v in o.data.vertices]
    front=min(q.y for q in pts);back=max(q.y for q in pts)
    m=G.Mesh('Neighbor drive walk and fence '+str(i),actor_kind='town')
    drive_x=-width*.29 if i%2 else width*.29
    front_street=-14.4 if yaw in (0,180) else -12.0
    a=world(drive_x-1.65,front_street,-.012);b=world(drive_x+1.65,front_street,-.012)
    c=world(drive_x+1.65,front+.2,-.012);d=world(drive_x-1.65,front+.2,-.012)
    m.geom([a,b,c,d],[(0,1,2,3)],'concrete')
    lawn=G.Mesh('Individual neighbor lawn '+str(i),actor_kind='town')
    for u in range(math.floor(-width/2),math.ceil(width/2),2):
        for v in range(math.floor(front_street),math.ceil(back+4),2):
            ua=max(-width/2,u);ub=min(width/2,u+2);va=max(front_street,v);vb=min(back+4,v+2)
            if ub<=ua or vb<=va:continue
            midu=(ua+ub)/2;midv=(va+vb)/2
            if min(q.x for q in pts)<midu<max(q.x for q in pts) and front<midv<back:continue
            if abs(midu-drive_x)<2 and front_street<midv<front+.3:continue
            lawn.geom([world(ua,va,-.016),world(ub,va,-.016),world(ub,vb,-.016),world(ua,vb,-.016)],[(0,1,2,3)],'lawn')
    lawn.finish()
    # Native privacy sections only along alternating rear lot boundaries.
    if i%2==0:
        for j in range(4):
            instance(G.ROOT/'fences/export/WoodPrivacy.glb',f'Neighbor privacy {i}_{j}',world(width/2-.2,front+4+j*1.8288),yaw,kind='Section_A' if j%2 else 'Section_B',actor='town')
    m.finish()
    if i%4==1:car(140+i,world(drive_x,front-3.1,.004),yaw)
    tree=world((-1 if i%2 else 1)*width*.30,front-4.5)
    instance(G.ROOT/('trees/export/PinOak.glb' if i%3==0 else 'trees/export/RedMaple.glb'),f'Yard tree {i}',tree,i*47,.66,actor='vegetation')


def rear_street(cx,cy,horizontal,count):
    path=G.ROOT/'ground/export/Ground.glb'
    for i in range(count):
        station=(i+.5)*6.096;point=(cx+station,cy,-.16764) if horizontal else (cx,cy+station,-.16764)
        instance(path,'Subdivision local road',point,90 if horizontal else 0,kind='Road_Straight_A',actor='site')
    # Sidewalks and verge reuse Ground maps; grid turf variation is authored
    # separately. Narrow sidewalks close the block rather than a distant field.
    if horizontal:
        for s in (-1,1):
            pad('Subdivision sidewalk',(cx,cx+count*6.096,cy+s*6.1-.76,cy+s*6.1+.76),'concrete',-.002)
    else:
        for s in (-1,1):pad('Subdivision sidewalk',(cx+s*6.1-.76,cx+s*6.1+.76,cy,cy+count*6.096),'concrete',-.002)


def build(p):
    modern=p['style']=='aframe'
    if modern:
        rear_street(-30,51,True,19);rear_street(82,-47,False,17);rear_street(44,-10,False,10)
        rows=[(x,69,0,24) for x in (-15,9,34,59,83)]
        rows += [(100,y,-90,24) for y in (-24,0,24,49,73)]
        rows += [(x,-65,180,25) for x in (-15,10,35,60,85)]
        rows += [(-48,y,90,24) for y in (-22,2,26,51)]
        rows += [(61,3,-90,24),(61,28,-90,24)]
    else:
        for i,(x,y) in enumerate(((26.6,-21),(36.8,-22),(48.2,-21),(-2,51),(8.5,51),(19,51))):
            instance(Path(f'build/hosts/town-{i}.glb'),f'Distinct town building {i}',(x,y,0),actor='town')
        pad('Shared rear alley',(-22,55,44.3,50.4),'asphalt',.002)
        pad('Alley side connection',(53,58,-23,50.4),'asphalt',.002)
        rows=[(-45,y,90,23) for y in (-10,14,38)]+[(x,-49,180,24) for x in (-13,11,38)]+[(-17,65,0,23)]
    for i,row in enumerate(rows):house(i,*row)
