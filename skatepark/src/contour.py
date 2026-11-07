"""Original bowl plan curves, shared by model and photographic measurement."""
import math

def _paths():
    c1=(-3.4,0);c2=(3.4,0);r1,r2,rw=4.1,4.8,.9
    x=((r1+rw)**2-(r2+rw)**2)/13.6;y=math.sqrt((r1+rw)**2-(x+3.4)**2);cw=(x,y)
    a1=math.atan2(y,x+3.4);a2=math.atan2(y,x-3.4)
    low=math.atan2(-math.sqrt(1-((r1-r2)/6.8)**2),(r1-r2)/6.8)%math.tau
    def arc(c,r,a,b):return ('arc',c,r,a,b,abs(b-a)*r)
    p1=(c1[0]+r1*math.cos(low),r1*math.sin(low));p2=(c2[0]+r2*math.cos(low),r2*math.sin(low))
    return ([arc(c2,r2,0,a2),arc(cw,rw,a2-math.pi,a1-math.pi),arc(c1,r1,a1,math.pi)],
            [arc(c1,r1,math.pi,low),('line',p1,p2,0,0,math.dist(p1,p2)),arc(c2,r2,low,math.tau)])
PATHS=_paths()

def rim_xy(t,shape='kidney'):
    t=t%math.tau
    if shape=='clover':
        r=6.1+1.6*math.cos(3*t);return r*math.cos(t),r*math.sin(t)
    path=PATHS[0] if t<=math.pi else PATHS[1];u=t/math.pi if t<=math.pi else (t-math.pi)/math.pi
    s=u*sum(p[-1] for p in path)
    for i,(kind,c,r,a,b,L) in enumerate(path):
        if s<=L or i==len(path)-1:
            f=min(1,max(0,s/L))
            if kind=='line':return c[0]+(r[0]-c[0])*f,c[1]+(r[1]-c[1])*f
            return c[0]+r*math.cos(a+(b-a)*f),c[1]+r*math.sin(a+(b-a)*f)
        s-=L

def normal_xy(t,shape='kidney'):
    a=rim_xy(t-.00001,shape);b=rim_xy(t+.00001,shape);dx=b[0]-a[0];dy=b[1]-a[1];L=math.hypot(dx,dy)
    return dy/L,-dx/L
