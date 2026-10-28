"""Actual source/sculpt/imported-GLB triangle cuts, dimensioned in millimeters."""
import json,sys,hashlib,argparse
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import weapon as W,weapon_verify as V
CUTS=[('Grip / lower',2,-.025,'stock'),('Grip / middle',2,0,'stock'),
      ('Grip / upper',2,.025,'stock'),
      ('Tang',1,0,'stock'),('Wrist / forward',1,-.060,'stock'),
      ('Wrist / middle',1,-.095,'stock'),('Wrist / rear',1,-.125,'stock'),
      ('Comb nose / low',1,-.150,'stock'),('Comb nose / high',1,-.175,'stock'),
      ('Cheek',1,-.200,'stock'),('Rear comb',1,-.235,'stock'),
      ('Butt at pad',1,-.282,'stock'),('Forend',1,.32,'stock'),
      ('Barrel float and channel lands',1,.32,'float'),('Scope at turrets',1,.062,'scope')]
def capture(path):
 if path.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(path))
 else:V.import_glb(path)
 arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE');W.pose(arm,None,0);rows=[]
 for title,axis,station,kind in CUTS:
  axes=[i for i in range(3) if i!=axis];segments=[]
  for ob in bpy.context.scene.objects:
   if ob.type!='MESH':continue
   ob.data.calc_loop_triangles()
   for t in ob.data.loop_triangles:
    mat=ob.data.materials[t.material_index]
    if kind=='stock' and 'CP_stock' not in mat.name:continue
    if kind=='float' and not any(k in mat.name for k in ('CP_stock','CP_steel')):continue
    vertices=[ob.matrix_world@ob.data.vertices[i].co for i in t.vertices];hits=[]
    for a,b in zip(vertices,vertices[1:]+vertices[:1]):
     if (a[axis]-station)*(b[axis]-station)<0:hits.append(a+(b-a)*((station-a[axis])/(b[axis]-a[axis])))
    if len(hits)!=2:continue
    if title.startswith('Grip') and any(p.y<-.065 or p.y>.03 for p in hits):continue
    if kind=='scope' and any(p.z<.09 for p in hits):continue
    segments.append([[p[i]*1000 for i in axes] for p in hits])
  assert segments,(path,title)
  points=[p for s in segments for p in s];bounds=[[min(p[i] for p in points),max(p[i] for p in points)] for i in range(2)]
  rows.append(dict(title=title,plane='XYZ'[axis],station_mm=station*1000,axes=['XYZ'[i] for i in axes],
     segments_mm=segments,bounds_mm=bounds,size_mm=[b-a for a,b in bounds]))
 return rows
def main():
 base=Path(__file__).resolve().parents[1]
 p=argparse.ArgumentParser();p.add_argument('--game',default='build/bolt.glb');p.add_argument('--sculpt',default='build/sculpt.blend');p.add_argument('--out',default='renders/checkpoint/sections')
 args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
 out=base/args.out;out.mkdir(parents=True,exist_ok=True)
 paths=[base/args.game,base/args.sculpt];rows=[capture(p) for p in paths]
 data=dict(files=[dict(path=str(p.relative_to(base)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths],game=rows[0],sculpt=rows[1])
 (out/'sections.json').write_text(json.dumps(data,indent=2))
 from PIL import Image,ImageDraw,ImageFont
 from kit.fonts import find_font
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),23);small=ImageFont.truetype(find_font('Noto Sans','Regular'),17)
 sheet=Image.new('RGB',(1800,600*((len(CUTS)+2)//3)),(237,239,236));d=ImageDraw.Draw(sheet)
 for i,(game,dense) in enumerate(zip(*rows)):
  ox=i%3*600;oy=i//3*600;b=game['bounds_mm'];scale=min(460/(b[0][1]-b[0][0]),380/(b[1][1]-b[1][0]));cx=sum(b[0])/2;cy=sum(b[1])/2
  def screen(p):return ox+300+(p[0]-cx)*scale,oy+280-(p[1]-cy)*scale
  d.text((ox+18,oy+10),game['title'],font=font,fill=(22,34,30))
  d.text((ox+18,oy+45),f"{'XYZ'[CUTS[i][1]]} = {CUTS[i][2]*1000:g} mm | actual surfaces",font=small,fill=(40,55,49))
  for r,color,width in [(dense,(20,145,145),3),(game,(139,54,28),1)]:
   for seg in r['segments_mm']:d.line([screen(v) for v in seg],fill=color,width=width)
  label=(f"X: {game['size_mm'][0]:.2f} mm | continues into stock" if i==2 else
       f"{game['axes'][0]} × {game['axes'][1]}: {game['size_mm'][0]:.2f} × {game['size_mm'][1]:.2f} mm")
  d.text((ox+18,oy+510),label,font=font,fill=(22,34,30))
  d.text((ox+18,oy+552),'teal: sculpt | brown: exported GLB',font=small,fill=(40,55,49))
 sheet.save(out/'sections.jpg',quality=92,optimize=True)
 sheet.crop((0,600,1800,2400)).save(out/'wrist-sections.jpg',quality=92,optimize=True)
 sheet.crop((0,2400,1200,3000)).save(out/'forend-sections.jpg',quality=92,optimize=True)
if __name__=='__main__':main()
