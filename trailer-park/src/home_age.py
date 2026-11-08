"""Sparse roof-fastener runoff, feathered into the actual wall finish.

Meter-scale corner colors survive the shared bake without per-home textures.
Stain strips sit 0.8mm above the skin, stop at openings, and follow gravity.
"""
import math,random
from mathutils import Vector


def runoff(a,p):
    from homes import openings
    from surfaces import age
    if p['era']=='1996':return
    L,W,E,F=p['length'],p['width'],p['eave'],p['floor'];r=random.Random(p['seed']+741)
    severity={'kept':.25,'patched':1,'faded':.76}[p['upkeep']]
    m=a.mesh('FastenerRunoff',component='weather_stains')
    for face in ('front','back','left','right'):
        along=face in ('front','back');sign=-1 if face in ('front','left') else 1
        length=L if along else W;holes=openings(p,face)
        normal=Vector((0,sign,0) if along else (sign,0,0))
        def xf(u,z):return (u,sign*(W/2+.0008),z) if along else (sign*(L/2+.0008),u,z)
        count=math.ceil(length/.9144);used=[]
        for j in range(1,count):
            if r.random()>.35+.60*severity:continue
            u=-length/2+j*length/count;drop=r.uniform(.65,1.75)*(.65+severity)
            # A hood diverts runoff to its ends; do not truncate every
            # seam above the awnings and hide the entire age treatment.
            for h in holes:
                if abs(u-h['u'])<h['w']/2+.14:u=h['u']+(1 if u>=h['u'] else -1)*(h['w']/2+.17)
            if abs(u)>length/2-.14 or any(abs(u-v)<.43 for v in used):continue
            used.append(u)
            bottom=max(F+.78,E-drop)
            for h in holes:
                if abs(u-h['u'])<h['w']/2+.08:bottom=max(bottom,h['z']+h['h']+.075)
            if bottom>E-.06:continue
            width=r.uniform(.035,.115)*(.6+severity);levels=[bottom+(E-bottom)*v for v in (0,.16,.42,.72,1)]
            vs=[];colors=[]
            for k,z in enumerate(levels):
                strength=(k/4)**.4*severity*r.uniform(.66,.98)
                drift=.008*math.sin(k*1.7+j);spread=width*(.35+.65*(k/4))
                for t in (-1,0,1):
                    q=xf(u+drift+spread*t,z);base=Vector(age(q,normal,p['color'],'Siding','wall',p,p['seed']))
                    c=base.lerp(Vector((.16,.050,.012)),strength if t==0 else 0)
                    vs.append(q);colors.append((*c,1))
            fs=[(k*3+t,k*3+t+1,(k+1)*3+t+1,(k+1)*3+t) for k in range(4) for t in range(2)]
            if (along and sign>0) or (not along and sign<0):fs=[tuple(reversed(f)) for f in fs]
            m.geom(vs,fs,'Siding');m.col[-len(colors):]=colors
    if m.v:
        ob=m.finish()
        # These are open skins. A closed-volume normal pass is ambiguous.
        for poly in ob.data.polygons:
            c=poly.center;n=poly.normal
            if n.x*c.x+n.y*c.y<0:poly.flip()
        ob.data.update()
