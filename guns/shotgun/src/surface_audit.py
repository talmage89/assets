"""Ray-hit texture measurements on actual packed part surfaces, in source meters.

The final verifier independently requires the GLBs' embedded PNG bytes to equal
these canonical images. No photographed pixel enters the generated textures.
"""
import sys,json,math
from pathlib import Path
import bpy,numpy as np
from PIL import Image
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))

def main():
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
 maps={name:np.asarray(Image.open(BASE/'textures'/('T_Hearth12_'+name+'.png'))) for name in ('BaseColor','Normal','ORM')}
 result=dict(units='BaseColor sRGB bytes; Normal/ORM linear bytes; physical UV density at 2048',surfaces={})
 def sample(name,origins,direction):
  ob=bpy.data.objects[name];mesh=ob.data;mesh.calc_loop_triangles();triangles=list(mesh.loop_triangles);uv=mesh.uv_layers['BakeUV']
  tree=BVHTree.FromPolygons([v.co for v in mesh.vertices],[t.vertices for t in triangles],all_triangles=True)
  samples={k:[] for k in maps};density=[]
  for origin in origins:
   hit,normal,index,distance=tree.ray_cast(Vector(origin),Vector(direction))
   if index is None:continue
   triangle=triangles[index];verts=[mesh.vertices[i].co for i in triangle.vertices]
   tex=[Vector((*uv.data[i].uv,0)) for i in triangle.loops];coord=barycentric_transform(hit,*verts,*tex)
   for key,im in maps.items():
    u=min(2047,max(0,int(coord.x*2048)));v=min(2047,max(0,int((1-coord.y)*2048)))
    samples[key].append(im[v,u,:3])
   ua=abs((tex[1]-tex[0]).cross(tex[2]-tex[0]).z)/2;density.append(math.sqrt(ua/triangle.area)*2048)
  assert density,(name,'no actual surface hits')
  return dict(hits=len(density),density_px_m_p5_p50_p95=np.percentile(density,[5,50,95]).round(2).tolist(),
   channels={k:dict(p10_p50_p90=np.percentile(v,[10,50,90],axis=0).round(2).tolist()) for k,v in samples.items()})
 for key,name,ys,zs in [
  ('receiver_blue','Receiver',np.linspace(.080,.130,31),np.linspace(.040,.046,13)),
  ('receiver_crown_contact','Receiver',np.linspace(.080,.130,31),np.linspace(.049,.052,13)),
  ('stock_blank','Stock',np.linspace(-.205,-.130,31),np.linspace(-.028,-.018,13)),
  ('wrist_checkering','Stock',np.linspace(-.032,-.010,31),np.linspace(-.020,-.005,21)),
  ('forend_crest','Forend_Wood',np.arange(.374,.550,.008),np.linspace(.001,.014,13)),
  ('forend_groove','Forend_Wood',np.arange(.375,.550,.008),np.linspace(.001,.014,13)),
  ('fired_hull_wall','Standalone_hull',np.linspace(.030,.050,21),np.linspace(-.004,.004,13)),
  ('fired_hull_soot','Standalone_hull',np.linspace(.068,.069,15),np.linspace(-.004,.004,13))]:
  result['surfaces'][key]=sample(name,[(.04,y,z) for y in ys for z in zs],(-1,0,0))
 # Actual delivered texels at the wear sites the photographic review rejected.
 from build import receiver_shape,GRIP
 origins=[]
 for y in np.linspace(.080,.220,37):
  (_,bottom,_),_=receiver_shape(y*1000+GRIP.y)
  origins.extend((.04,y,(bottom-GRIP.z)*.001+dz) for dz in (.0010,.0014,.0018))
 result['surfaces']['receiver_lower_contact']=sample('Receiver',origins,(-1,0,0))
 for key,name,ys,zs in [
  ('receiver_front_corner','Receiver',np.linspace(.248,.2495,11),np.linspace(.014,.045,17)),
  ('port_rear_lip','Receiver',np.linspace(.1350,.1368,13),np.linspace(.045,.049,11)),
  ('port_front_lip','Receiver',np.linspace(.2375,.2392,13),np.linspace(.045,.049,11)),
  ('cap_rim','Magazine_Cap',np.linspace(.5987,.5998,13),np.linspace(.010,.017,13)),
  ('guard_front','Trigger_Plate',np.linspace(.115,.1175,13),np.linspace(-.010,-.002,15)),
  ('pad_side_molding','Recoil_Pad',np.linspace(-.262,-.248,31),np.linspace(-.090,-.025,41))]:
  result['surfaces'][key]=sample(name,[(.04,y,z) for y in ys for z in zs],(-1,0,0))
 result['surfaces']['muzzle_crown']=sample('Barrel',[(x,.74,.049+z) for x in np.linspace(.0099,.0108,15) for z in np.linspace(-.002,.002,11)],(0,-1,0))
 result['surfaces']['muzzle_underside']=sample('Barrel',[(x,y,-.02) for x in np.linspace(-.0007,.0007,13) for y in np.linspace(.702,.707,19)],(0,0,1))
 result['surfaces']['cap_face_blue']=sample('Magazine_Cap',[(x,.65,.013+z) for x in np.linspace(-.006,.006,17) for z in np.linspace(-.004,.004,13)],(0,-1,0))
 def median(key):return np.asarray(result['surfaces'][key]['channels']['BaseColor']['p10_p50_p90'][1])
 blue=median('receiver_blue');luma=lambda rgb:float(rgb@np.asarray((.2126,.7152,.0722)))
 assert blue[0]<min(blue[1:]),('blue-black must have red lowest',blue)
 contacts=('receiver_lower_contact','receiver_front_corner','port_rear_lip','port_front_lip',
           'cap_rim','guard_front','muzzle_crown','muzzle_underside')
 ratios={key:luma(median(key))/luma(blue) for key in contacts}
 assert min(ratios.values())>1.3,('contact rub disappeared in the shipping map',ratios)
 cap_face_ratio=luma(median('cap_face_blue'))/luma(median('cap_rim'))
 assert cap_face_ratio<.8,('rim wear spread over the cap face',cap_face_ratio)
 result['finish_regression']=dict(passed=True,contact_to_blue_luma_ratios=ratios,minimum_required_ratio=1.3,
  cap_face_to_rim_luma_ratio=cap_face_ratio,cap_face_maximum_ratio=.8,
  scope='actual shipping BaseColor contrast at causal sites; photographic visibility is reviewed separately')
 (BASE/'build/surface-audit.json').write_text(json.dumps(result,indent=2))
 print('HEARTH ACTUAL SURFACE TEXEL AUDIT',flush=True)
if __name__=='__main__':main()
