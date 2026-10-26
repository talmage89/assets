"""Original stamped and folded 31-gallon galvanized garbage can, in meters."""
import argparse,sys,math
from pathlib import Path
import bpy,bmesh
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import model as G
from finishes import zinc

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--quality',choices=['high','game'],default='high');p.add_argument('--wear',type=float,default=.35)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.read_factory_settings(use_empty=True);hi=a.quality=='high'
 root=G.pivot('MetalTrashCan',(0,0,0));root['static_root']=True
 lid=G.pivot('Lid',(0,0,.714));lid['slide_axis']='Z';lid['range_m']=[0,.6];lid.parent=root
 steel=zinc('Weathered spangled galvanized sheet',a.wear);ls=zinc('Pressed galvanized lid',a.wear,lid=True);grip=zinc('Handled zinc wire',a.wear,handle=True)
 def add(ob,parent=root):return G.attach(ob,parent,'MetalTrashCan')
 N=96 # Four angular samples per flute; stable structural geometry in both sources.
 def ring(z,r,flute=0):
  out=[]
  for i in range(N):
   t=i*math.tau/N;rr=r+flute*(.5+.5*math.cos(24*t))
   # Two local handling impacts, smooth and present on inner/outer sheet.
   def dent(angle,zz,w,h,depth):
    d=math.atan2(math.sin(t-angle),math.cos(t-angle));return depth*math.exp(-((d/w)**2+((z-zz)/h)**2)*2)
   rr-=dent(-.8,.32,.35,.10,.009)+dent(2.5,.15,.22,.055,.006)
   out.append((rr*math.cos(t),rr*math.sin(t),z))
  return out
 # Cross-section travels from underside chime around folded mouth into hollow interior.
 stations=[(.01635,.22795,0),(0,.2286,0),(.008,.2286,0),(.088,.230,0),(.105,.231,.0045),(.615,.247,.005),(.653,.250,0),(.690,.251,0),(.696,.254,0),(.699,.251,0),(.695,.2485,0),(.690,.2485,0),(.615,.24635,.005),(.105,.23035,.0045),(.017,.22535,0)]
 # Fewer inner stations carry the corrugations and keep actual sheet gauge.
 loops=[ring(*s) for s in stations];body=G.loft('Corrugated sheet shell with rolled mouth',loops,steel,caps=False)
 # Close topologically through bottom panel thickness (same radial count).
 n=len(loops);vs=[tuple(v.co) for v in body.data.vertices];fs=[tuple(p.vertices) for p in body.data.polygons]
 ci=len(vs);vs.extend([(0,0,.017),(0,0,.01635)])
 for i in range(N):
  j=(i+1)%N;fs.extend([(ci,(n-1)*N+i,(n-1)*N+j),(ci+1,j,i)])
 bpy.data.objects.remove(body,do_unlink=True)
 # Outer bottom skirts down to ground: underside closes as a conical folded floor.
 body=G.mesh('Corrugated galvanized vessel',vs,fs,steel)
 bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free();G.smooth(body,13);add(body)
 # Horizontal lower stiffening beads are a pressed sheet, integrated visually at the shell.
 # Folded rear longitudinal lock seam.
 seamloops=[]
 for zz,rr,ff in stations[:7]:
  if zz<.02:continue
  yy=rr+ff+.00015
  seamloops.append([(-.0045,yy,zz),(.0045,yy,zz),(.0045,yy+.0012,zz),(-.0045,yy+.0012,zz)])
 add(G.loft('Rear folded lock seam',seamloops,steel))
 # Removable pressed lid, thin closed profile with seating shoulder and hem.
 profile=[(.678,.2605),(.678,.2667),(.681,.2667),(.682,.261),(.6968,.260),(.6968,.254),(.7018,.249),(.718,.214),(.722,.110),(.723,0),(.7222,0),(.7212,.110),(.7172,.214),(.701,.249),(.696,.254),(.696,.2592),(.681,.2602)]
 # A single ring/axis profile is manifold; repeated beads are baked source-only.
 ob=G.lathe('Pressed removable lid with hem',profile,ls,44,closed=True);add(ob,lid)
 # Bent flat bridge, its feet sit on the crown; no unsupported handle.
 path=[(-.063,.722),(-.050,.722),(-.043,.74965),(-.034,.75565),(.034,.75565),(.043,.74965),(.050,.722),(.063,.722)]
 # path is XZ; construct strip, then solidify 0.9 mm downward.
 ob=G.loft('Bent lid bridge handle',[[(x,-.011,z),(x,.011,z)] for x,z in path],ls,caps=False,closed=False)
 m=ob.modifiers.new('Folded handle gauge','SOLIDIFY');m.thickness=.0009;m.offset=-1;add(ob,lid)
 for x in (-.056,.056):add(G.cylinder('Handle spot weld cap',(x,0,.722),(x,0,.723),.003,ls,12 if hi else 8),lid)
 # Side wire carrying loops are separate, pivoted at the retained eyes.
 for s,label in [(-1,'Left'),(1,'Right')]:
  x=s*.2525
  plate=G.box(label+' stamped handle bracket',(x,0,.632),(.002,.103,.043),steel,0)
  # Pressed mounting strap wraps the tapered wall rather than floating at its corners.
  for v in plate.data.vertices:
   y=v.co.y;zz=.632+v.co.z;t=math.asin(y/.252)
   r=.247+(.003*(zz-.615)/.038)+.005*max(0,min(1,(.653-zz)/.038))*(.5+.5*math.cos(24*t))
   v.co.x=s*(math.sqrt(r*r-y*y)-.2525)+v.co.x
  add(plate)
  piv=G.pivot('Handle_'+label,(s*.262,0,.644),'Y',(-95,0) if s>0 else (0,95));piv.parent=root
  # End legs enter retained eyes; the grip bows out 16 mm and hangs below them.
  pts=[(s*.262,-.036,.644),(s*.262,-.049,.644),(s*.274,-.049,.631),(s*.279,-.040,.601),(s*.279,-.028,.591),(s*.279,.028,.591),(s*.279,.040,.601),(s*.274,.049,.631),(s*.262,.049,.644),(s*.262,.036,.644)]
  add(G.tube(label+' folding wire loop',pts,.003,grip,8 if hi else 6),piv)
  for y in (-.044,.044):
   add(G.box(label+' retaining eye folded neck',(s*.250,y,.644),(.009,.008,.008),steel,0))
   # Bent retention eye in XZ plane, with wire passing through its center.
   pts=[(s*(.262+.008*math.cos(t)),y,.644+.007*math.sin(t)) for t in [k*math.tau/8 for k in range(9)]]
   add(G.tube(label+' rolled bracket eye',pts,.0018,steel,4 if not hi else 8))
 sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc['asset']='MetalTrashCan';sc['quality']=a.quality;sc['wear']=a.wear;sc['seed']=114
 Path(a.out).parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
if __name__=='__main__':main()
