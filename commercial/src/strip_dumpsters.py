"""Three welded service-container constructions, supported on rear pads."""
import random
from geometry import *
from strip_graphics import quad
from age import decal


def add(p,ink,layout):
    rng=random.Random(p['seed']+1908);b=p['building'];rows=[]
    for i,m in enumerate(p['modules'][1::3]):
        if m['wing']:continue
        kind=(p['seed']+i)%3;w,d,h=((1.8,1.35,1.15),(2.45,1.60,1.45),(1.65,1.15,1.0))[kind]
        x=m['origin'][0]+m['width']*.31;y=b['rear']+1.40
        rt=root('RearDumpster_'+str(i),(x,y,0),180,kind='ServiceContainer');rt['reusable_module']=True
        box('Dumpster concrete pad',(0,0,.06),(w+.44,d+.45,.12),'Concrete',rt,.012)
        for side in (-1,1):box('Dumpster welded skid',(side*w*.33,0,.18),(.10,d-.16,.12),'Trim',rt,0)
        loops=[]
        for zz,ww,dd in ((.24,w-.14,d-.14),(h,w,d),(h,w-.012,d-.012),(.25,w-.16,d-.16)):
            loops.append([(-ww/2,-dd/2,zz),(ww/2,-dd/2,zz),(ww/2,dd/2,zz),(-ww/2,dd/2,zz)])
        ob=own(G.ring_loft('Tapered welded dumpster skin',loops,M['Primary']),rt);ob['container_color']=kind
        for xx in (-w/2,w/2):
            box('Container side lift pocket',(xx,0,.66),(.12,.65,.14),'Primary',rt,.008)['container_color']=kind
        for xx in (-w*.34,w*.34):box('Pressed front stiffener',(xx,-d/2-.008,(h+.28)/2),(.045,.028,h-.28),'Primary',rt,0)['container_color']=kind
        # Two split injection-molded lids, or one compact steel lid.
        for j in range(1 if kind==2 else 2):
            lw=w if kind==2 else w/2-.016;xx=0 if kind==2 else (-.25 if j==0 else .25)*w
            lid=root(f'RearDumpster_{i}_Lid_{j}',(xx,d/2,h+.022),parent=rt);lid['static_root']=False;lid['pivot_axis']='X';lid['range_degrees']=(-95,0)
            box('Container hinged lid',(0,-d/2,.019),(lw,d+.04,.038),'Black',lid,.016,1)
            for rib in (-.28,0,.28):box('Molded lid stiffening rib',(rib*lw,-d/2,.053),(.035,d*.77,.03),'Black',lid,.008)
            cylinder('Lid hinge pin',(-lw/2,0,0),(lw/2,0,0),.018,'Metal',lid,8)
        quad('Container service label','Waste','sign',0,-d/2-.026,.73,w*.40,.24,rt,ink,layout)
        decal('Container wet hem corrosion',(0,-d/2-.027,.32),w-.12,.16,'Rust',rt,vertical=True)
        decal('Container lid runoff',(w*.12,-d/2-.029,h-.24),w*.36,.39,'Grime',rt,vertical=True)
        rows.append(dict(name=rt.name,type=('small split lid','wide ribbed','compact steel lid')[kind],pad=(w+.44,d+.45),position=(x,y)))
    p['rear_containers']=rows
