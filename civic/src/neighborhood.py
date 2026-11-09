"""Arterial parcels: native houses, actual drives, yard boundaries and shops."""
import math,random
from mathutils import Vector
from geo import ROOT,LOCAL
from library import place


def build(a,sp):
    from sites import ground
    rng=random.Random(1482);house=LOCAL/'build/context/house.glb';cape=LOCAL/'build/context/house-cape.glb'
    fence=ROOT/'fences/chain-link/export/ChainLink.glb'
    def fence_run(aa,bb):
        start,end=Vector((*aa,0)),Vector((*bb,0));delta=end-start;n=math.ceil(delta.length/3.048)
        for j in range(n):
            mid=start+delta*(j+.5)/n
            rt=place(fence,'ResidentialYardFence',tuple(mid),math.degrees(math.atan2(delta.y,delta.x)),'Chain_Section',a.root);rt.scale.x=delta.length/n/3.048
            place(fence,'ResidentialFencePost',tuple(start+delta*j/n),select='Chain_Line',parent=a.root)
        place(fence,'ResidentialFenceEnd',tuple(end),select='Chain_Terminal',parent=a.root)
    # 70–76ft lots with independently placed houses and real street connections.
    for rear in (False,True):
        for j in range(-4,5):
            x=j*22.4+rng.uniform(-.5,.5);yy=52+rng.uniform(0,1.4) if rear else -64+rng.uniform(-1,1)
            yaw=0 if rear else 180;front=yy-6.5 if rear else yy+6.5
            place(cape if j%3==1 else house,('Rear' if rear else 'Across')+'House_'+str(j),(x,yy,-.01),yaw,parent=a.root)
            verge=44.4 if rear else -50.8
            aa,bb=sorted((front,verge));dx=x+8.0*(1 if rear else -1)
            ground(a,'ResidentialDrive',(dx-1.65,dx+1.65,aa-.35,bb+.35),'Concrete',.006)
            # The drive crosses the verge sidewalk without an ornamental curb.
            if rear:ground(a,'RearDriveDrop',(dx-1.7,dx+1.7,42.5,44.6),'Concrete',.005)
            else:ground(a,'AcrossDriveDrop',(dx-1.7,dx+1.7,-51.0,-48.4),'Concrete',.005)
            walkx=x-1.7
            ground(a,'ResidentialEntryWalk',(walkx-.52,walkx+.52,aa,bb),'Concrete',.012)
            back=yy+(8.7 if rear else -8.7)
            if j%3!=0:fence_run((x-10.7,back),(x+10.7,back))
            # Trees grow in individual yards, with gaps for the drive and crown.
            tx=x-rng.uniform(5,8);ty=yy+(-10 if rear else 10)
            place(ROOT/'trees/export'/('PinOak.glb' if j%3==0 else 'RedMaple.glb'),'ResidentialYardTree',(tx,ty,-.025),j*73,parent=a.root)
    # A cross street directly behind the parcel explains the rear addresses.
    ground(a,'RearLocalStreet',(-165,165,35.8,42.0),'Asphalt',-.028)
    ground(a,'RearNorthWalk',(-165,165,42.2,44.2),'Concrete',.145)
    # The station is part of an arterial block, framed by existing Main Street
    # shops beyond the west cross street and houses immediately east of it.
    shops=LOCAL/'textures/shared/downtown/build/blocks/midwest/block.glb'
    place(shops,'WestArterialShops',(-62,-3,0),90,parent=a.root)
    place(shops,'AdjacentArterialOffice',(-35,-1,0),0,'Midwest_411_02',a.root)
    ground(a,'NeighborOfficeParking',(-42,-27,-32,-12),'Asphalt',-.003)
    ground(a,'NeighborOfficeEntry',(-36,-34,-13,-9),'Concrete',.145)
    for j in range(3):
        yy=-14+j*22.5;xx=65+rng.uniform(0,1.1)
        place(cape if j==1 else house,'EastNeighborHouse_'+str(j),(xx,yy,-.01),-90,parent=a.root)
        ground(a,'EastNeighborDrive',(52.4,xx-4.9,yy+6.2,yy+9.5),'Concrete',.006)
        fence_run((xx+9.2,yy-10.4),(xx+9.2,yy+10.4))
        place(ROOT/'trees/export/RedMaple.glb','EastYardTree',(xx-7.4,yy-5.4,-.025),j*81,parent=a.root)
