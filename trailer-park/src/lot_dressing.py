"""Resident-owned service clutter, placed from the occupant seed."""
import math,random


def add(a,p,seed):
    L,W=p['length'],p['width'];r=random.Random(seed+803)
    m=a.mesh('ResidentStorage',component='resident_storage')
    x=L*.30;y=-W/2-.42
    # Stored replacement panels and an actual leaning tool behind the stairs.
    if p['era']!='1996' or seed%4==0:
        for j in range(2+seed%3):
            xx=x+j*.19
            m.beam((xx,y-.24,.004),(xx-.22,-W/2-.01,1.03),.16,.018,'Trim',(.55,.54,.47),r=0)
        for j in range(2):
            xx=x-.4-j*.16
            m.beam((xx,y-.45,.04),(xx-.16,-W/2-.01,1.25),.027,.027,'Veneer',(.30,.22,.12),r=0)
            m.box((xx,y-.45,.075),(.20,.045,.15),'Trim',(.13,.14,.12))
        m.box((x+.75,y-.20,.18),(.50,.36,.30),'Trim',(.045,.05,.041),r=.015)
        m.box((x+.75,y-.20,.35),(.54,.39,.065),'Trim',(.08,.085,.067),r=.008)
        m.tube([(x+1.16,y-.2,.003),(x+1.16,y-.2,.29)],.13,'Trim',(.27,.29,.25),12)
    # A low, sagging fabric cover over stored tools; gravity-shaped folds.
    # It is tied around a supported heap, not stretched between remote pins.
    if (seed%4==0 or p.get('corner_apron')) and p['era']!='1996':
        cx=x-1.1;cy=y-.22;vs=[]
        m.box((cx,cy,.24),(.85,.54,.48),'Veneer',(.12,.11,.08))
        # Grid stations follow the actual box edges, so triangles outside
        # its footprint drape down without cutting through its corners.
        us=[-1,-.82,-.68,-.425/.73,-.35,-.17,0,.17,.35,.425/.73,.68,.82,1]
        vv=[-1,-.8,-.27/.57,-.25,0,.25,.27/.57,.8,1]
        for v in vv:
            for u in us:
                edge=max(abs(u*.73)-.425,abs(v*.57)-.27,0)
                z=max(.028,.483-1.4*edge)
                z+=.015*math.sin(u*19+v*4)**2
                vs.append((cx+u*.73,cy+v*.57,z))
        fs=[(j*13+i,j*13+i+1,(j+1)*13+i+1,(j+1)*13+i) for j in range(8) for i in range(12)]
        m.geom(vs,fs,'Trim',(.115,.13,.075))
    # A hose hangs from its wall hook in a slack gravity loop.
    if seed%3==1:
        cx=-L*.30;cy=W/2+.07
        m.box((cx,cy,.73),(.18,.10,.055),'Trim',(.12,.14,.10))
        for k in range(3):
            points=[(cx+(.22+k*.015)*math.sin(t),cy+.035*k,.44+.29*math.cos(t)) for t in [j*math.tau/24 for j in range(25)]]
            m.tube(points,.010,'Trim',(.045,.09,.036),6)
    m.finish()
