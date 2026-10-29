"""Measure the actual imported return against the preserved carved section.

This is a visible game-asset fit audit. Distances come from triangle surfaces;
nominal shader/model constants are never reported as measurements.
"""
from pathlib import Path
import json,math,sys
import bpy,numpy as np
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import motion,weapon as W
from sections import segments

def main():
 source=BASE/'build/delivery/imported-parts.blend';bpy.ops.wm.open_mainfile(filepath=str(source))
 W.pose(bpy.data.objects['R39Armature'],'Idle',0)
 names=('Handguard_Retainer363','LowerHandguard_Sculpt');objects={name:bpy.data.objects[name] for name in names}
 trees={name:motion.surface(ob)['tree'] for name,ob in objects.items()};rows=[]
 for i in range(1,24):
  angle=math.pi+math.pi*i/24;c,s=math.cos(angle),math.sin(angle)
  origin=Vector((.080*c,.360,.0843+.080*s));direction=Vector((-c,0,-s))
  cap=trees[names[0]].ray_cast(origin,direction,.1);wood=trees[names[1]].ray_cast(origin,direction,.1)
  if cap[0] is None or wood[0] is None:continue
  inner=trees[names[0]].ray_cast(cap[0]+direction*1e-6,direction,.05)
  assert inner[0] is not None
  overhang=(wood[3]-cap[3])*1000;gauge=(inner[0]-cap[0]).length*1000
  rows.append(dict(angle_degrees=math.degrees(angle),cap_outer_mm=list(cap[0]*1000),wood_outer_mm=list(wood[0]*1000),overhang_mm=overhang,return_gauge_along_ray_mm=gauge))
 assert len(rows)>=19,'Insufficient actual lower-section ray hits'
 overhang=[r['overhang_mm'] for r in rows];gauge=[r['return_gauge_along_ray_mm'] for r in rows]
 result=dict(passed=min(overhang)>-.2 and max(overhang)<2,source='actual imported GLB triangles',station_y_mm=360,sampled_rays=len(rows),overhang_min_median_max_mm=np.percentile(overhang,[0,50,100]).tolist(),gauge_min_median_max_mm=np.percentile(gauge,[0,50,100]).tolist(),rows=rows,scope='Outer cap return versus preserved wood at a real section; no fit inferred from a bounding box or serialization.')
 (BASE/'build/delivery/retainer-fit.json').write_text(json.dumps(result,indent=2));assert result['passed'],result
 from PIL import Image,ImageDraw,ImageFont
 from kit.fonts import find_font
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),20)
 sheet=Image.new('RGB',(1300,1050),'#ebede9');d=ImageDraw.Draw(sheet)
 d.text((25,15),'Actual imported triangles / front handguard cap return at Y360 mm',font=font,fill='black')
 for name,color,width in ((names[0],'#285e80',4),(names[1],'#8b492d',2)):
  for line in segments(objects[name],1,360):d.line([(650+x*17,850-(z-44)*17) for x,z in line],fill=color,width=width)
 d.text((25,925),'Blue: cap sheet. Brown: preserved wood. All visible section intersections retained.',font=font,fill='black')
 d.text((25,958),'Measured radial overhang min / median / max: '+str(np.round(result['overhang_min_median_max_mm'],3).tolist())+' mm',font=font,fill='black')
 d.text((25,991),'Measured return gauge along those rays: '+str(np.round(result['gauge_min_median_max_mm'],3).tolist())+' mm',font=font,fill='black')
 out=BASE/'renders/final/retainer-section.jpg';out.parent.mkdir(parents=True,exist_ok=True);sheet.save(out,quality=94)
 print('RETAINER ACTUAL SECTION',result['sampled_rays'],result['overhang_min_median_max_mm'],flush=True)
if __name__=='__main__':main()
