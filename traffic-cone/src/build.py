"""Original hollow 28-inch slim PVC cone, black weighted base, two foil collars."""
import sys,math
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import model as G,materials as M
from kit.prop import Build,arguments

def finish(wear,base=False):
    n=M.Nodes('Road-scuffed black PVC base' if base else 'Orange PVC and two reflective collars');c=M.common(n);p=c['position'];x,y,z=n.split(p)
    grain=n.noise(p,1800,2)
    bands=n.maximum(n.mul(n.ramp(z,.30455,.3048),n.ramp(z,.40665,.4064)),n.mul(n.ramp(z,.45695,.4572),n.ramp(z,.60985,.6096)))
    orange=(.65,.065,.002);white=(.70,.72,.67)
    col=(.009,.011,.010) if base else n.mix(bands,orange,white,True)
    rough=.78 if base else n.mix(bands,.33,.28)
    edge=n.maximum(n.ramp(n.math('ABSOLUTE',x),.147,.172),n.ramp(n.math('ABSOLUTE',y),.147,.172)) if base else n.ramp(z,.22,.035)
    drag=n.mul(wear,edge,n.ramp(n.noise(n.vec('MULTIPLY',p,(3,25,1)),110,3),.57,.72))
    col=n.mix(drag,col,(.09,.079,.054) if base else (.22,.13,.059),True);rough=n.mix(drag,rough,.82)
    dirt=n.mul(wear,n.ramp(z,.16,.02),n.ramp(n.noise(p,130,3),.25,.72),.25)
    col=n.mix(dirt,col,(.045,.034,.020),True)
    if not base:
        hand=n.mul(wear,n.ramp(z,.657,.69),n.ramp(n.noise(p,95,3),.53,.70),.25)
        col=n.mix(hand,col,(.19,.10,.035),True)
    height=n.add(n.mul(n.math('SUBTRACT',grain,.5),15e-6 if base else 3e-6),n.mul(drag,-20e-6))
    if not base:
        seam=n.mul(bands,n.band(x,0,.0005,.001),n.ramp(y,0,.01))
        rims=n.maximum(0,*[n.band(z,v,.0015,.001) for v in [.3048,.4064,.4572,.6096]])
        scuff=n.mul(wear,rims,n.ramp(n.noise(p,310,3),.55,.70),.6)
        col=n.mix(scuff,col,(.23,.19,.12),True);rough=n.mix(scuff,rough,.72)
        angle=n.math('ARCTAN2',y,x)
        grip=n.mul(n.ramp(z,.659,.671),n.math('POWER',n.math('MAXIMUM',0,n.math('COSINE',n.mul(angle,8))),8))
        height=n.add(height,n.mul(bands,.00012),n.mul(seam,.00018),n.mul(grip,.00012))
    return n.finish(col,rough,0,height)

def main():
    a=arguments();b=Build('TrafficCone',a.quality,a.wear);orange=finish(a.wear);black=finish(a.wear,True)
    # Top and bottom open: 2.54 mm-class wall; the grip neck has a real central opening.
    outer=[(.0254,.108),(.034,.108),(.045,.09525),(.050,.094),(.6604,.0254),(.667,.0254),(.682,.0135),(.695,.0135),(.6985,.01905),(.7112,.01905)]
    inner=[(.7112,.009525),(.695,.009525),(.6604,.02286),(.05,.09146),(.0254,.104)]
    b.add(G.lathe('Hollow orange cone and grip',outer+inner,orange,96 if b.high else 20,closed=True))
    # Equal-angle rings keep the stacking bore circular. Reusing rounded-square
    # corner parameters here would turn the bore into a rounded diamond.
    count=96 if b.high else 24;poly=[]
    for i in range(count):
        t=i*math.tau/count;lo=.15;hi=.26
        for _ in range(28):
            radius=(lo+hi)/2;qx=abs(radius*math.cos(t))-(.1778-.016);qy=abs(radius*math.sin(t))-(.1778-.016)
            sdf=math.hypot(max(qx,0),max(qy,0))+min(max(qx,qy),0)-.016
            if sdf>0:hi=radius
            else:lo=radius
        poly.append((lo*math.cos(t),lo*math.sin(t)))
    vs=[]
    for z in [0,.0254]:
        for inside in [False,True]:
            for i,(x,y) in enumerate(poly):
                t=i*math.tau/count;vs.append((.091*math.cos(t),.091*math.sin(t),z) if inside else (x,y,z))
    fs=[]
    for i in range(count):
        j=(i+1)%count;fs += [(i,j,j+2*count,i+2*count),(i+count,i+3*count,j+3*count,j+count),(i,i+count,j+count,j),(i+2*count,j+2*count,j+3*count,i+3*count)]
    ob=G.mesh('Weighted black base with stacking bore',vs,fs,black)
    if b.high:G.bevel(ob,.0007,2)
    b.add(ob);b.save(a.out,a.quality)
if __name__=='__main__':main()
