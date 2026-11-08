"""Varied native rear elevations meet a service alley along the river.

Unique downtown generator seeds, no repeated block in the 300m core. Retained
canonical buildings close the distant view. Every native rear door, escape,
porch and stepped roof remains in the instance.
"""
import json
import math
import random
from pathlib import Path
import geometry as G
import context as C


def add(p,rt):
    rng=random.Random(p.seed+377);lots=[];base=Path('build/town')
    rows=json.loads((base/'manifest.json').read_text())
    paving=G.Batch('MainStreetAndServiceAlleys',rt,'context')
    furniture=G.Batch('RearAlleyServiceEquipment',rt,'context')
    rt['main_street_front_m']=90.
    rt['unique_building_seeds']=[r['seed'] for r in rows]
    for index,(side,direction) in enumerate(((-1,-1),(-1,1),(1,-1),(1,1))):
        block=json.loads((base/rows[index]['block']).read_text());cursor=15.5
        for i,lot in enumerate(block['lots']):
            width=lot['width'];depth=lot['depth'];y=direction*(cursor+width/2);cursor+=width+.12
            # Rear additions can project 4m. Their toes, not the front
            # facades, meet the working service lane 4.6m above the shore.
            edge=p.center(y)+side*p.halfwidth(y)
            x=edge+side*(11.5+depth/2)
            src=base/Path(rows[index]['block']).parent/(lot['id']+'.gltf')
            C.instance(src,f'MainStreetBack_{side}_{direction}_{i}',(x,y,3.70+p.water_z(y)),rt,-90 if side<0 else 90)
            lots.append((x-depth/2-4,x+depth/2+4,y-width/2,y+width/2))
            if i%3!=1:
                dx=edge+side*rng.uniform(8.0,9.2);dz=3.775+p.water_z(y)
                # 2yd dumpster: formed sides, sloping polymer lids, feet.
                furniture.box((dx,y,dz+.52),(1.5,1.03,1.0),'steel',(.24,.32,.22,1))
                furniture.box((dx,y,dz+1.04),(1.58,1.10,.08),'rubber')
                for yy in (-.38,.38):
                    furniture.box((dx,y+yy,dz+.03),(1.25,.10,.06),'steel')
            # Loading apron to the lane, front sidewalk and a varying
            # street line behind each native lot, all seated on the terrace.
            for x0,x1,role in ((edge+side*7,edge+side*11.5,'asphalt'),
                              (x+side*depth/2,x+side*(depth/2+2),'concrete'),
                              (x+side*(depth/2+2),x+side*(depth/2+11),'asphalt')):
                for a in range(math.floor(y-width/2),math.ceil(y+width/2),2):
                    c=min(y+width/2,a+2);z=lambda v:3.775+p.water_z(v)
                    pts=[(x0,a,z(a)),(x1,a,z(a)),(x1,c,z(c)),(x0,c,z(c))]
                    paving.geom(pts,[(0,1,2,3)],role,up=True)
                    C.paving_skirts(paving,pts,[(3,0),(1,2)] if side>0 else [(0,3),(2,1)],role)
        # A continuous curving lane follows the actual river terrace.
        for j in range(150):
            if direction>0:continue
            a=-150+j*2;c=a+2
            if abs(a)<15:continue
            coords=[]
            for yy,off in ((a,4.6),(a,7.0),(c,7.0),(c,4.6)):
                xx=p.center(yy)+side*(p.halfwidth(yy)+off)
                coords.append((xx,yy,3.775+p.water_z(yy)))
            paving.geom(coords,[(0,1,2,3)],'asphalt',up=True)
            C.paving_skirts(paving,coords,[(3,0),(1,2)] if side>0 else [(0,3),(2,1)],'asphalt')
    # A small back-of-block surface parking lot, connected to the alley.
    for side in (-1,1):
        y=-128;x=p.center(y)+side*(p.halfwidth(y)+19)
        z=3.775+p.water_z(y)
        paving.geom([(x+dx,y+dy,z-p.water_z(y)+p.water_z(y+dy)) for dx,dy in ((-10,-11),(10,-11),(10,11),(-10,11))],[(0,1,2,3)],'asphalt',up=True)
        for j in range(7):
            yy=y-9+j*2.7
            paving.geom([(x+dx,yy+dy,3.78+p.water_z(yy)) for dx,dy in ((-9,0),(-4,0),(-4,.09),(-9,.09))],[(0,1,2,3)],'paint_white',up=True)
    paving.finish();furniture.finish()
    return lots
