"""Dimensioned triangle-plane cuts of the source and imported game meshes."""
import sys,argparse,json,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit import weapon as W,weapon_verify as V
CUTS=[('Lower grip',2,-.050,(0,1),('Grip_RubberMold',)),
 ('Middle grip',2,-.027,(0,1),('Grip_RubberMold',)),
 ('Upper grip',2,.005,(0,1),('Grip_RubberMold',)),
 ('Cylinder / chambers and flutes',1,.066,(0,2),('Cylinder_Fluted',)),
 ('Frame / window',1,.060,(0,2),('Frame_Forging','Cylinder_Fluted','CylinderStop')),
 ('Frame / rear shoulder',1,.034,(0,2),('Frame_Forging',)),
 ('Underlug / shroud',1,.118,(0,2),('Barrel','Extractor_Rod')),
 ('Grip / longitudinal saddle',0,0,(1,2),('Grip_RubberMold',))]
def capture(path):
 if path.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(path))
 else:V.import_glb(path)
 arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE');W.pose(arm,'Idle',0)
 rows=[];dg=bpy.context.evaluated_depsgraph_get()
 for title,axis,station,projection,names in CUTS:
  parts={}
  for ob in bpy.context.scene.objects:
   if ob.type!='MESH' or ob.get('part_name',ob.name) not in names:continue
   ev=ob.evaluated_get(dg);mesh=ev.to_mesh();mesh.calc_loop_triangles();segments=[]
   for tri in mesh.loop_triangles:
    vs=[ev.matrix_world@mesh.vertices[i].co for i in tri.vertices];hits=[]
    for a,b in zip(vs,vs[1:]+vs[:1]):
     if (a[axis]-station)*(b[axis]-station)<0:
      hits.append(a+(b-a)*(station-a[axis])/(b[axis]-a[axis]))
    if len(hits)==2:segments.append([[p[k]*1000 for k in projection] for p in hits])
   ev.to_mesh_clear()
   if segments:parts[ob.get('part_name',ob.name)]=segments
  assert parts,title
  pts=[p for ss in parts.values() for s in ss for p in s];bounds=[[min(p[k] for p in pts),max(p[k] for p in pts)] for k in (0,1)]
  rows.append(dict(title=title,plane='XYZ'[axis],station_mm=station*1000,parts=parts,
   axes=['XYZ'[i] for i in projection],bounds_mm=bounds,size_mm=[b-a for a,b in bounds]))
 return rows
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--high',required=True);p.add_argument('--out',required=True)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 source=Path(a.source).resolve();high=Path(a.high).resolve()
 result=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),high_sha256=hashlib.sha256(high.read_bytes()).hexdigest(),game=capture(source),dense=capture(high))
 (out/'sections.json').write_text(json.dumps(result,indent=2))
 from PIL import Image,ImageDraw,ImageFont
 from kit.fonts import find_font
 im=Image.new('RGB',(1800,3*620+65),(239,240,235));d=ImageDraw.Draw(im)
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),22);small=ImageFont.truetype(find_font('Noto Sans','Regular'),17)
 d.text((20,15),'Meridian Six / actual triangle sections / mm',font=font,fill=(24,35,30))
 for i,(game,dense) in enumerate(zip(result['game'],result['dense'])):
  ox=i%3*600;oy=65+i//3*620;b=game['bounds_mm'];cx=sum(b[0])/2;cy=sum(b[1])/2
  scale=min(490/(b[0][1]-b[0][0]),420/(b[1][1]-b[1][0]))
  def xy(v):return (ox+300+(v[0]-cx)*scale,oy+300-(v[1]-cy)*scale)
  d.text((ox+18,oy+10),game['title'],font=font,fill=(24,35,30))
  d.text((ox+18,oy+46),f"{game['plane']} {game['station_mm']:g} / {game['size_mm'][0]:.2f} x {game['size_mm'][1]:.2f}",font=small,fill=(34,48,42))
  for row,color,width in [(dense,(28,141,143),4),(game,(135,55,25),1)]:
   for segs in row['parts'].values():
    for seg in segs:d.line([xy(v) for v in seg],fill=color,width=width)
  x0,x1=b[0];y=oy+535
  d.line((xy((x0,cy))[0],y,xy((x1,cy))[0],y),fill=(25,35,30),width=2)
  for x in (x0,x1):d.line((xy((x,cy))[0],y-6,xy((x,cy))[0],y+6),fill=(25,35,30),width=2)
  d.text((ox+18,oy+558),f"{game['axes'][0]} {x1-x0:.2f} mm; {game['axes'][1]} {b[1][1]-b[1][0]:.2f} mm",font=small,fill=(24,35,30))
  d.text((ox+18,oy+590),'teal dense source / brown imported GLB',font=small,fill=(24,35,30))
 im.save(out/'sections.jpg',quality=92,optimize=True)
 print('SECTIONS',out/'sections.jpg')
if __name__=='__main__':main()
