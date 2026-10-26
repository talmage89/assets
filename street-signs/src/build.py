"""Original residential sign assembly and parked, shared-atlas name templates."""
import sys,math
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import model as G,materials as M
from kit.prop import Build,arguments

def main():
    a=arguments();b=Build('StreetSigns',a.quality,a.wear);metal=b.metal();mark=Path(__file__).resolve().parents[1]/'build/markings'
    # Hollow 2-inch galvanized tube, 2 mm wall. Perforations are baked small detail.
    n=M.Nodes('Perforated galvanized tube');c=M.common(n);p=c['position'];x,y,z=n.split(p)
    phase=n.mul(n.math('SUBTRACT',n.math('FRACT',n.math('DIVIDE',z,.0254)),.5),.0254)
    face=n.math('MINIMUM',n.math('ABSOLUTE',x),n.math('ABSOLUTE',y))
    holes=n.ramp(n.add(n.mul(phase,phase),n.mul(face,face)),.0045**2,.0035**2)
    grain=n.noise(p,2300,2);base=n.mix(holes,(.34,.37,.38),(.009,.011,.010),True)
    zinc=n.finish(base,n.mix(holes,.58,.83),n.mix(holes,1,0),n.add(n.mul(grain,2e-6),n.mul(holes,-.0014)))
    for label,outer,inner,height in [('Square perforated galvanized post',.0254,.0234,3.0),('Breakaway anchor sleeve',.028575,.026575,.0762)]:
        vs=[]
        for z0 in [0,height]:
            for r in [outer,inner]:vs.extend([(sx*r,sy*r,z0) for sx,sy in [(-1,-1),(1,-1),(1,1),(-1,1)]])
        fs=[]
        for i in range(4):
            j=(i+1)%4;fs.extend([(i,j,j+8,i+8),(i+4,i+12,j+12,j+4),(i,i+4,j+4,j),(i+8,j+8,j+12,i+12)])
        b.add(G.mesh(label,vs,fs,zinc))
    b.add(G.cylinder('Anchor through pin',(-.030,0,.0381),(.030,0,.0381),.0038,metal,24 if b.high else 6))
    for sign in [-1,1]:b.bolt('Anchor retaining nut',(sign*.028575,0,.0381),(sign,0,0),metal,.006)
    stop=M.print_material('R1-1 reflective face',mark/'stop.png',base=M.surface('Sign sheeting substrate','plastic',a.wear,color=(.5,.05,.04),roughness=.30),rough=.30)
    aa=.381;bb=aa*(math.sqrt(2)-1);pts=[(-aa,-bb),(-bb,-aa),(bb,-aa),(aa,-bb),(aa,bb),(bb,aa),(-bb,aa),(-aa,bb)]
    b.plate('Stop plate',pts,.002,metal,front=stop,center=(0,-.0284,2.5146))
    for z0 in [2.2946,2.7346]:
        b.add(G.box('Stop back mounting spacer',(0,-.0269,z0),(.035,.003,.040),metal,.0003 if b.high else 0))
        b.bolt('Stop mounting carriage bolt',(0,-.0294,z0),(0,-1,0),metal,.006)
    for i in range(4):
        for j,z0 in enumerate([3.0713,3.3339]):
            name=M.print_material(f'Name {i}-{j}',mark/f'name-{i}-{j}.png',base=M.surface(f'Green sheeting {i}-{j}','plastic',a.wear,color=(.015,.15,.04),roughness=.30),rough=.30)
            ob=b.plate(f'Street blade {i}-{j}',G.rounded_rectangle(.762,.2286,.014,3),.002,metal,front=name,back=name,center=(i*1.6,0,z0),rotation=j*math.pi/2)
            ob['variant_id']=i;ob['bake_offset']=(i*1.6,0,0);ob['bake_only']=i!=0
    saddle=G.box('Post cap blade saddle',(0,0,3.003),(.066,.050,.066),metal,.001 if b.high else 0)
    G.boolean(saddle,G.box('Lower blade slot',(0,0,3.04),(.08,.0022,.15),metal,0));b.add(saddle)
    cross=G.box('Cross bracket saddle',(0,0,3.207),(.060,.060,.075),metal,.001 if b.high else 0)
    G.boolean(cross,G.box('Cross lower slot',(0,0,3.163),(.08,.0022,.047),metal,0))
    G.boolean(cross,G.box('Cross upper slot',(0,0,3.25),(.0022,.08,.061),metal,0));b.add(cross)
    for z0 in [2.985,3.010]:b.bolt('Lower saddle screw',(0,-.025,z0),(0,-1,0),metal,.004)
    for z0 in [3.185,3.230]:b.bolt('Cross saddle screw',(0,-.030,z0),(0,-1,0),metal,.004)
    for z0 in [3.195,3.235]:b.bolt('Upper blade screw',(.030,0,z0),(1,0,0),metal,.004)
    b.save(a.out,a.quality)
if __name__=='__main__':main()
