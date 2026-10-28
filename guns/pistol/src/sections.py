"""Dimensioned C9 section cuts from actual triangles, including exported GLB.

Dense source and delivery are drawn together. Measurements use mesh-plane
intersections, not constants echoed from the construction script. No reference
image is read here.
"""
import argparse,json,sys,math,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit import weapon,weapon_verify
CUTS=[('grip_lower','Grip / lower', 'Root',2,-.036,(0,1)),
      ('grip_mid','Grip / middle','Root',2,-.020,(0,1)),
      ('grip_upper','Grip / upper','Root',2,-.012,(0,1)),
      ('guard','Guard / bottom bar','Root',1,.044,(0,2)),
      ('dust','Dust cover','Root',1,.095,(0,2)),
      ('slide','Slide','Slide',1,.085,(0,2))]

def capture(path):
 if path.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(path))
 else:weapon_verify.import_glb(path)
 arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE');weapon.pose(arm,None,0)
 rows={}
 for name,title,bone,axis,station,projection in CUTS:
  segments=[]
  for ob in bpy.context.scene.objects:
   if ob.type!='MESH':continue
   if path.suffix=='.blend':
    if ob.get('bone')!=bone:continue
    group=None
   else:
    group=ob.vertex_groups.get(bone)
    if group is None:continue
   ob.data.calc_loop_triangles()
   def owns(i):return group is None or any(g.group==group.index and g.weight>.99 for g in ob.data.vertices[i].groups)
   for tri in ob.data.loop_triangles:
    if not all(owns(i) for i in tri.vertices):continue
    vertices=[ob.matrix_world@ob.data.vertices[i].co for i in tri.vertices]
    hits=[]
    for a,b in zip(vertices,vertices[1:]+vertices[:1]):
     if (a[axis]-station)*(b[axis]-station)<0:
      hits.append(a+(b-a)*(station-a[axis])/(b[axis]-a[axis]))
    if len(hits)==2:
     if name=='guard' and any(p.z>0 for p in hits):continue
     segments.append([[p[i]*1000 for i in projection] for p in hits])
  assert segments,(path,name)
  points=[p for s in segments for p in s]
  bounds=[[min(p[i] for p in points),max(p[i] for p in points)] for i in range(2)]
  rows[name]=dict(title=title,plane_axis='XYZ'[axis],station_mm=station*1000,axes=['XYZ'[i] for i in projection],
    segments_mm=segments,bounds_mm=bounds,size_mm=[b-a for a,b in bounds])
 return rows

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--high',required=True);p.add_argument('--out',required=True)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 source=Path(a.source).resolve();high=Path(a.high).resolve()
 data=dict(source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
           high=str(high),high_sha256=hashlib.sha256(high.read_bytes()).hexdigest(),low=capture(source),high_sections=capture(high))
 (out/'sections.json').write_text(json.dumps(data,indent=2))
 # Pillow is only a plotting canvas for measured geometric segments.
 from PIL import Image,ImageDraw,ImageFont
 from kit.fonts import find_font
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),24);small=ImageFont.truetype(find_font('Noto Sans','Regular'),18)
 sheet=Image.new('RGB',(1800,1440),(239,240,236));d=ImageDraw.Draw(sheet)
 for index,(name,*_) in enumerate(CUTS):
  low=data['low'][name];dense=data['high_sections'][name]
  col=index%3;row=index//3;ox=col*600;oy=row*720
  d.text((ox+22,oy+15),low['title'],font=font,fill=(24,35,31))
  d.text((ox+22,oy+51),f"{low['plane_axis']} = {low['station_mm']:g} mm / actual triangle cuts",font=small,fill=(50,60,56))
  bounds=[[min(low['bounds_mm'][i][0],dense['bounds_mm'][i][0]),max(low['bounds_mm'][i][1],dense['bounds_mm'][i][1])] for i in range(2)]
  scale=min(460/(bounds[0][1]-bounds[0][0]),475/(bounds[1][1]-bounds[1][0]))
  cx=(bounds[0][0]+bounds[0][1])/2;cy=(bounds[1][0]+bounds[1][1])/2
  def screen(v):return (ox+300+(v[0]-cx)*scale,oy+340-(v[1]-cy)*scale)
  for label,cut,color,width in [('high',dense,(28,143,142),4),('low',low,(139,55,26),1)]:
   for segment in cut['segments_mm']:d.line([screen(v) for v in segment],fill=color,width=width)
  x0,x1=low['bounds_mm'][0];y0,y1=low['bounds_mm'][1]
  # Dimension bars use the measured extrema and remain outside the drawing.
  left=ox+55;right=ox+545;top=oy+90;bottom=oy+593
  d.line((screen((x0,cy))[0],bottom,screen((x1,cy))[0],bottom),fill=(45,55,50),width=2)
  for x in (x0,x1):
   sx=screen((x,cy))[0];d.line((sx,bottom-7,sx,bottom+7),fill=(45,55,50),width=2)
  d.text((ox+155,bottom+12),f"{low['axes'][0]}: {x1-x0:.2f} mm",font=font,fill=(30,42,36))
  d.text((ox+22,oy+650),f"{low['axes'][1]}: {y1-y0:.2f} mm | source {dense['size_mm'][0]:.2f} × {dense['size_mm'][1]:.2f}",font=small,fill=(30,42,36))
  d.text((ox+22,oy+685),'teal: sculpt source    brown: game / GLB',font=small,fill=(30,42,36))
 sheet.save(out/'sections.jpg',quality=94,optimize=True)
 print('MEASURED SECTION CUTS',out/'sections.jpg',flush=True)
if __name__=='__main__':main()
