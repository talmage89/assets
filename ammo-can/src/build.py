"""Original M2A1-style steel ammo can, authored in meters; front latch faces -Y."""
import argparse,math,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import model as G
from kit.materials import surface
from finishes import olive

def main():
 p=argparse.ArgumentParser();p.add_argument('--quality',choices=['high','game'],default='high');p.add_argument('--wear',type=float,default=.35);p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.read_factory_settings(use_empty=True);hi=a.quality=='high'
 root=G.pivot('AmmoCan',(0,0,0));root['static_root']=True
 paint=olive('Olive drab casing with fictional lot stencil',a.wear,stamp=ROOT/'ammo-can/build/markings/lot.png');lidpaint=olive('Olive lid paint',a.wear,'lid');hardware=olive('Rubbed olive hardware',a.wear,'hardware')
 steel=surface('Exposed hinge pin steel','stainless',a.wear,color=(.16,.17,.14),roughness=.48,grime=.25)
 rubber=surface('Retained black lid gasket','rubber',a.wear,grime=.1)
 def add(ob,parent=root):return G.attach(ob,parent,'AmmoCan')
 def pivot(name,pos,axis,limits,parent=root):
  ob=G.pivot(name,pos,axis,limits);bpy.context.view_layer.update();ob.parent=parent;ob.matrix_world=Matrix.Translation(pos);return ob
 lid=pivot('Lid',(0,.1498,.1785),'X',(-110,0))
 handle=pivot('Handle',(-.016,0,.188),'Y',(-90,0),lid)
 latch=pivot('Latch',(0,-.1503,.164),'X',(-105,0),lid)
 def rect(w,d,r,z):return [(x,y,z) for x,y in G.rounded_rectangle(w,d,r,3)]
 # Folded shell includes a thin floor and a small rolled/flared mouth.
 loops=[rect(.1411,.2832,.004,0),rect(.1411,.2832,.004,.002),rect(.1411,.2832,.004,.170),rect(.1435,.2856,.004,.1763),rect(.1419,.2840,.0032,.1763),rect(.1395,.2816,.0032,.170),rect(.1395,.2816,.0032,.0008)]
 body=G.loft('Hollow stamped casing and folded mouth',loops,paint,caps=True)
 bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free();G.smooth(body,38);add(body)
 # Upper side stiffeners have supported overlapping returns, not floating plates.
 for s in (-1,1):
  points=[(-.137,.170),(.137,.170),(.137,.125),(-.025,.125),(-.137,.149)]
  add(G.profile('Pressed upper side reinforcement '+str(s),points,min(s*.07025,s*.07145),max(s*.07025,s*.07145),lidpaint,axis='X',radius=.0003,segments=1))
 # A hemmed lid pan; rear skirt is relieved around the working hinge.
 outer=G.rounded_rectangle(.1548,.2944,.004,3);inner=G.rounded_rectangle(.1524,.2920,.0028,3)
 def skirt(y):return .160+(.1820-.160)*max(0,min(1,(y-.128)/.017))
 panloops=[[(x,y,.1855) for x,y in outer],[(x,y,.183) for x,y in outer],[(x,y,skirt(y)) for x,y in outer],[(x,y,skirt(y)+.0004) for x,y in inner],[(x,y,.1843) for x,y in inner]]
 pan=G.loft('Hemmed cover pan with relieved rear skirt',panloops,lidpaint,caps=True);G.bevel(pan,.00035,1);pan.modifiers[-1].angle_limit=math.radians(40);G.smooth(pan,38);add(pan,lid)
 # Captured gasket retainer: the inner lip enters the body with useful clearance.
 ret=[rect(.149,.289,.004,.1843),rect(.149,.289,.004,.1798),rect(.135,.275,.003,.1798),rect(.135,.275,.003,.174),rect(.1326,.2726,.0024,.174),rect(.1326,.2726,.0024,.1825)]
 add(G.ring_loft('Stamped gasket retainer and inner lip',ret,lidpaint),lid)
 gasketloops=[rect(.1447,.2868,.004,.1763),rect(.1447,.2868,.004,.1798),rect(.1375,.2796,.003,.1798),rect(.1375,.2796,.003,.1763)]
 add(G.ring_loft('Continuous retained rubber gasket',gasketloops,rubber),lid)
 # Body-mounted hinge pin and alternating rolled sleeves.
 add(G.cylinder('Secured rear hinge pin',(-.067,.1498,.1785),(.067,.1498,.1785),.0015,steel,12))
 def sleeve(name,x,length,radius,parent,axis='X',center=(.1498,.1785)):
  cy,cz=center
  return add(G.lathe(name,[(x-length/2,.0018),(x-length/2,radius),(x+length/2,radius),(x+length/2,.0018)],hardware,12,axis=axis,center=(cy,cz),closed=True),parent)
 for s in (-1,1):
  path=[(.1411,.159),(.1411,.169),(.1465,.172),(.1481,.1762)]
  section=path+list(reversed(G.offset_profile(path,.001)))
  add(G.profile('Rear body hinge mounting leaf '+str(s),section,s*.054-.009,s*.054+.009,hardware,axis='X'))
  sleeve('Body rear hinge sleeve '+str(s),s*.054,.018,.003,root)
  path=[(.1435,.1843),(.1465,.1835),(.1472,.1798)]
  section=path+list(reversed(G.offset_profile(path,.0008)))
  add(G.profile('Cover rear hinge leaf '+str(s),section,s*.028-.0115,s*.028+.0115,lidpaint,axis='X'),lid)
  # Open C hooks release from the body-secured pin with the cover opened.
  angles=[math.radians(10+200*k/10) for k in range(11)]
  section=[(.1498+r*math.cos(t),.1785+r*math.sin(t)) for r,aa in [(.003,angles),(.0018,list(reversed(angles)))] for t in aa]
  add(G.profile('Cover rear hinge hook '+str(s),section,s*.028-.0115,s*.028+.0115,hardware,axis='X'),lid)
 # Handle's Y-axis wire stubs run inside two stamped retaining sleeves.
 for y in (-.061,.061):
  add(G.box('Handle mounting foot '+str(y),(-.016,y,.1859),(.020,.022,.0008),hardware,.0003,1),lid)
  # Cylinder authored along Y; annular section is a retained bearing.
  ob=G.lathe('Handle retaining sleeve '+str(y),[(y-.009,.0018),(y-.009,.0025),(y+.009,.0025),(y+.009,.0018)],hardware,12,axis='Y',center=(-.016,.188),closed=True);add(ob,lid)
 pts=[(-.016,-.050,.188),(-.016,-.073,.188),(.009,-.073,.188),(.016,-.066,.188),(.016,.066,.188),(.009,.073,.188),(-.016,.073,.188),(-.016,.050,.188)]
 add(G.tube('Folding carrying handle wire',pts,.0015,hardware,8),handle)
 add(G.box('Folded carrying grip strap',(.016,0,.188),(.011,.109,.002),hardware,.0004,1),handle)
 # Lid-mounted cam hinge and broad stamped lever; the body hasp is its reaction seat.
 add(G.cylinder('Cam latch retained pivot pin',(-.053,-.1503,.164),(.053,-.1503,.164),.0015,steel,12),lid)
 for s in (-1,1):
  add(G.box('Cam latch cover mounting leaf '+str(s),(s*.048,-.1467,.171),(.009,.006,.018),lidpaint,.0004,1),lid)
  sleeve('Cam outer bearing '+str(s),s*.048,.009,.0025,lid,center=(-.1503,.164))
 sleeve('Cam lever hinge sleeve',0,.083,.0025,latch,center=(-.1503,.164))
 outline=[(-.050,.141),(.050,.141),(.050,.066),(.030,.066),(.030,.053),(-.030,.053),(-.030,.066),(-.050,.066)]
 plate=G.profile('Stamped cam latch plate with inspection hole',outline,-.15205,-.15055,hardware,axis='Y',radius=.00035,segments=1)
 G.apply(plate);cutter=G.cylinder('Inspection hole cutter',(0,-.156,.094),(0,-.146,.094),.004,hardware,12);G.boolean(plate,cutter)
 bm=bmesh.new();bm.from_mesh(plate.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-6);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(plate.data);bm.free();G.smooth(plate,35)
 for face in plate.data.polygons:
  if abs(face.normal.y)>.999:face.use_smooth=False
 add(plate,latch)
 add(G.box('Cam hinge folded neck',(0,-.1513,.15165),(.083,.0015,.0213),hardware,0),latch)
 for zz in (.150,.157):add(G.box('Cam stamped horizontal reinforcement '+str(zz),(0,-.1520,zz),(.082,.0014,.002),hardware,.0004,1),latch)
 # A bent, welded hasp reacts against the rear cam surface at the closed position.
 path=[(-.1411,.142),(-.144,.142),(-.15055,.127),(-.15055,.106),(-.144,.100),(-.1411,.100)]
 section=path+list(reversed(G.offset_profile(path,.001)))
 add(G.profile('Body welded hasp reaction seat',section,-.025,.025,hardware,axis='X',radius=0))
 bail=[(-.027,-.1503,.058),(-.027,-.1503,.024),(-.021,-.1503,.018),(.021,-.1503,.018),(.027,-.1503,.024),(.027,-.1503,.058)]
 add(G.tube('Cam pull bail',bail,.0015,hardware,8),latch)
 # Sparse explicit spot-weld crowns read in close-ups and cost little geometry.
 for x in (-.018,.018):
  add(G.cylinder('Hasp projection weld',(x,-.1422,.138),(x,-.1432,.138),.002,hardware,8))
 sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc['asset']='AmmoCan';sc['quality']=a.quality;sc['wear']=a.wear;sc['seed']=51
 bpy.context.view_layer.update();bpy.ops.file.pack_all();Path(a.out).parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
if __name__=='__main__':main()
