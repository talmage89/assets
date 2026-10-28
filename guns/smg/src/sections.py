"""Dimensioned triangle-plane sections, comparing dense molds with game meshes."""
import hashlib,json,sys
from pathlib import Path
import bpy,numpy as np
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit import weapon as W
BASE=Path(__file__).resolve().parents[1]
CUTS=[*[(f'Grip / Z {z:g}',2,z,['Lower_Mold']) for z in (-40,-10,22)],
 *[(f'Stock / Y {y:g}',1,y,['Stock_Mold']) for y in (-245,-170,-105)],
 *[(f'Handguard / Y {y:g}',1,y,['Handguard_Mold']) for y in (200,255,310)],
 *[(f'Receiver + well / Y {y:g}',1,y,['Receiver_Shell','MagazineWell_Shell']) for y in (136,145,155)],
 *[(f'Guard / Y {y:g}',1,y,['Lower_Mold']) for y in (55,70,85)]]

def segments(ob,axis,station):
 m=ob.data;m.calc_loop_triangles()
 points=np.array([tuple(ob.matrix_world@v.co) for v in m.vertices],float)*1000
 tri=points[np.array([t.vertices for t in m.loop_triangles])]
 signed=tri[:,:,axis]-station;mask=(signed.min(axis=1)<0)&(signed.max(axis=1)>0);tri=tri[mask];signed=signed[mask]
 found=[[] for _ in tri]
 for a,b in ((0,1),(1,2),(2,0)):
  mask=signed[:,a]*signed[:,b]<0;idx=np.where(mask)[0]
  t=-signed[mask,a]/(signed[mask,b]-signed[mask,a]);hits=tri[mask,a]+(tri[mask,b]-tri[mask,a])*t[:,None]
  for i,v in zip(idx,hits):found[i].append(v)
 axes=[i for i in range(3) if i!=axis]
 return [[[float(v[i]) for i in axes] for v in pair] for pair in found if len(pair)==2]

def main():
 source=BASE/'build/smg.blend';bpy.ops.wm.open_mainfile(filepath=str(source));W.pose(bpy.data.objects['SMGArmature'],'Idle',0)
 rows=[]
 for title,axis,station,names in CUTS:
  low={n:segments(bpy.data.objects[n],axis,station) for n in names}
  dense={n:segments(bpy.data.objects['HIGH_'+n],axis,station) for n in names if bpy.data.objects.get('HIGH_'+n)}
  if title.startswith('Grip'):
   low={n:[s for s in segs if max(p[1] for p in s)<60] for n,segs in low.items()}
   dense={n:[s for s in segs if max(p[1] for p in s)<60] for n,segs in dense.items()}
  if title.startswith('Guard'):
   low={n:[s for s in segs if max(p[1] for p in s)<20] for n,segs in low.items()}
   dense={n:[s for s in segs if max(p[1] for p in s)<20] for n,segs in dense.items()}
  flat=[v for segs in low.values() for seg in segs for v in seg];assert flat,title
  bounds=[[min(v[i] for v in flat),max(v[i] for v in flat)] for i in range(2)]
  rows.append(dict(title=title,axis='XYZ'[axis],station_mm=station,axes=['XYZ'[i] for i in range(3) if i!=axis],
   low=low,dense=dense,bounds_mm=bounds,dimensions_mm=[hi-lo for lo,hi in bounds]))
 centers=[]
 for z in (-52,25):
  segs=segments(bpy.data.objects['Lower_Mold'],2,z)
  ys=[p[1] for line in segs if max(p[1] for p in line)<60 for p in line]
  centers.append(dict(z_mm=z,y_mm=(min(ys)+max(ys))/2))
 import math
 angle=math.degrees(math.atan2(77,centers[1]['y_mm']-centers[0]['y_mm']))
 data=dict(grip_axis=dict(method='midpoint of actual front/back section extents at heel and web',stations=centers,angle_to_bore_degrees=angle),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),method='actual triangle intersections, not authored station extrema',cuts=rows)
 (BASE/'build/sections.json').write_text(json.dumps(data,indent=2))
 from PIL import Image,ImageDraw,ImageFont
 from kit.fonts import find_font
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),21);small=ImageFont.truetype(find_font('Noto Sans','Regular'),17)
 sheet=Image.new('RGB',(1800,2035),(239,240,236));d=ImageDraw.Draw(sheet)
 d.text((22,12),'Relay 9 / actual game + dense sculpt sections / dimensions in mm',font=font,fill=(25,40,34))
 for i,row in enumerate(rows):
  x=i%3*600;y=55+i//3*395;bounds=row['bounds_mm'];dims=row['dimensions_mm']
  d.text((x+18,y+8),row['title'],font=font,fill=(25,40,34))
  d.text((x+18,y+40),f"{row['axes'][0]} {dims[0]:.2f} × {row['axes'][1]} {dims[1]:.2f} mm",font=small,fill=(40,55,48))
  scale=min(480/max(dims[0],1),245/max(dims[1],1));cx=sum(bounds[0])/2;cy=sum(bounds[1])/2
  def screen(v):return (x+300+(v[0]-cx)*scale,y+205-(v[1]-cy)*scale)
  for layer,color,width in [('dense',(32,151,146),4),('low',(130,59,36),1)]:
   for segs in row[layer].values():
    for segment in segs:d.line([screen(p) for p in segment],fill=color,width=width)
  a,b=screen((bounds[0][0],cy)),screen((bounds[0][1],cy));d.line((a[0],y+340,b[0],y+340),fill=(40,55,48),width=2)
  for p in (a,b):d.line((p[0],y+334,p[0],y+346),fill=(40,55,48),width=2)
  d.text((x+18,y+360),'teal: dense mold | brown: game; cut on actual surfaces',font=small,fill=(40,55,48))
 out=BASE/'renders/checkpoint';out.mkdir(parents=True,exist_ok=True);sheet.save(out/'sections.jpg',quality=94,optimize=True)
 print('SECTION CUTS',len(rows),flush=True)
if __name__=='__main__':main()
