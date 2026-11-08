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
        def xf(u,z):return (u,sign*(W/2+.0015),z) if along else (sign*(L/2+.0015),u,z)
        count=math.ceil(length/.9144);sources=[]
        for j in range(1,count):
            if r.random()>.12+.17*severity:continue
            u=-length/2+j*length/count
            if any(abs(u-h['u'])<h['w']/2+.15 for h in holes):continue
            sources.append((u,E-.025,r.uniform(.17,.75),r.uniform(.028,.075),r.uniform(.42,.88)))
        # A broad end window excludes the inner roof stations. Its outer
        # hood/drip-rail fasteners still weather the exposed wall corners.
        if not along and severity>.5:
            h=holes[0];side=-1 if p['seed']%2 else 1
            sources.append((side*(h['w']/2+.19),E-.018,r.uniform(.34,.68),.065,.86))
        for h in holes:
            if h['kind']!='window':continue
            for side in (-1,1):
                if r.random()>.35+.3*severity:continue
                # Corroded sill ends and awning screws bleed independently.
                u=h['u']+side*(h['w']/2+.07)
                sources.append((u,h['z']-.045,r.uniform(.16,.48),r.uniform(.028,.065),r.uniform(.40,.78)))
                if p['era']=='1972' and r.random()<.45:
                    sources.append((u+side*.07,min(E-.03,h['z']+h['h']+.16),r.uniform(.12,.35),.025,.48))
        for j,(u,top,drop,width,opacity) in enumerate(sources):
            bottom=max(F+.08,top-drop)
            if bottom>=top:continue
            levels=[top-(top-bottom)*v for v in (0,.12,.35,.67,1)]
            vs=[];colors=[]
            for k,z in enumerate(levels):
                t=k/4;strength=(1-t)**1.45*severity*opacity
                drift=.004*math.sin(k*1.7+j);spread=width*(1-.85*t)
                for t in (-1,0,1):
                    q=xf(u+drift+spread*t,z)
                    color=p['accent'] if p['era']=='1972' and z<F+.71 else p['color']
                    base=Vector(age(q,normal,color,'Siding','wall',p,p['seed']))
                    c=base.lerp(Vector((.12,.041,.011)),strength if t==0 else 0)
                    vs.append(q);colors.append((*c,1))
            fs=[(k*3+t,k*3+t+1,(k+1)*3+t+1,(k+1)*3+t) for k in range(4) for t in range(2)]
            if (along and sign>0) or (not along and sign<0):fs=[tuple(reversed(f)) for f in fs]
            m.geom(vs,fs,'Siding');m.col[-len(colors):]=colors
            if top>E-.06:
                # A real source head sits in the drip rail above its stain.
                m.box(xf(u,top+.012),(.012,.012,.012),'Trim',(.12,.07,.035))
    if m.v:
        ob=m.finish()
        # These are open skins. A closed-volume normal pass is ambiguous.
        for poly in ob.data.polygons:
            c=poly.center;n=poly.normal
            if n.x*c.x+n.y*c.y<0:poly.flip()
        ob.data.update()
