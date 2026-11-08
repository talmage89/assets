"""Sparse native grass clumps across the lawns, beyond the slab fringes."""
import math,random


def add(parent,plan,lib):
    from ground_edges import edges
    from terrain import sward_height
    paths=[];old=plan['kind']=='old'
    for row in plan['lots']:
        p=row['home'];r=random.Random(p['occupant_seed']+8603);L,W=p['length'],p['width'];angle=math.radians(row['yaw']);cs,sn=math.cos(angle),math.sin(angle)
        def world(u,v):
            x=row['origin'][0]+cs*u-sn*v;y=row['origin'][1]+sn*u+cs*v
            return (x,y,sward_height(x,y)+.002)
        for j in range(22 if old else 11):
            if j%2 or old and row['number']==1:
                u=r.uniform(L/2+.8,L/2+4.8);v=r.uniform(.78,min(W/2+.45,plan['lot_frontage']/2-1.35))
            else:u=r.uniform(-L/2+.8,L/2-.6);v=-W/2-r.uniform(3.67,3.84)
            theta=r.uniform(0,math.tau);length=r.uniform(.16,.29)
            paths.append([world(u,v),world(u+math.cos(theta)*length,v+math.sin(theta)*length)])
    ob=edges(parent,paths,plan['seed']+9713,lib);ob.name='Sparse unmown lawn clumps';ob['component']='summer_weeds'
    return ob
