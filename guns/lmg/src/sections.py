"""Actual triangle intersections; dimensioned sections, not restated constants."""
import json,sys
from pathlib import Path
import bpy,numpy as np
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import weapon as W,weapon_verify as V
BASE=Path(__file__).resolve().parents[1]
CUTS=[('Receiver at tray',1,160,['Receiver_Sheet']),('Receiver at trigger',1,46,['Receiver_Sheet']),
 ('Handguard rear',1,280,['Handguard_Sculpt']),('Handguard front',1,440,['Handguard_Sculpt']),
 ('Stock rear',1,-275,['Stock_Sculpt']),('Stock neck',1,-115,['Stock_Sculpt']),
 ('Grip low',2,-49,['PistolGrip_Sculpt']),('Grip middle',2,-9,['PistolGrip_Sculpt']),('Grip web',2,30,['PistolGrip_Sculpt']),
 ('Box midheight',2,-43,['Box_Shell']),('Cover middle',1,80,['FeedCover_Shell']),('Guard band',1,35,['TriggerGuard_Band'])]
def segments(ob,axis,station):
 dg=bpy.context.evaluated_depsgraph_get();ev=ob.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles()
 p=np.array([tuple(ev.matrix_world@v.co) for v in me.vertices])*1000
 t=p[np.array([t.vertices for t in me.loop_triangles])];d=t[:,:,axis]-station
 keep=(d.min(axis=1)<0)&(d.max(axis=1)>0);t=t[keep];d=d[keep];out=[[] for _ in t]
 for a,b in ((0,1),(1,2),(2,0)):
  k=d[:,a]*d[:,b]<0;ii=np.where(k)[0];u=-d[k,a]/(d[k,b]-d[k,a]);hits=t[k,a]+(t[k,b]-t[k,a])*u[:,None]
  for i,h in zip(ii,hits):out[i].append(h)
 ev.to_mesh_clear();axes=[i for i in range(3) if i!=axis]
 return [[[float(p[k]) for k in axes] for p in line] for line in out if len(line)==2]
def main():
 arm=V.import_glb(BASE/'build/lmg.glb');W.pose(arm,'Idle',0);rows=[]
 for title,axis,station,names in CUTS:
  lines=[]
  for name in names:
   obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith(name)]
   for o in obs:lines+=segments(o,axis,station)
  assert lines,title
  pts=np.array([p for l in lines for p in l]);a,b=pts.min(axis=0),pts.max(axis=0)
  rows.append(dict(title=title,axis='XYZ'[axis],station_mm=station,segments_mm=lines,bounds_mm=[a.tolist(),b.tolist()],dimensions_mm=(b-a).tolist()))
 (BASE/'build/sections.json').write_text(json.dumps(rows,indent=2))
 from PIL import Image,ImageDraw,ImageFont
 from kit.fonts import find_font
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),23);small=ImageFont.truetype(find_font('Noto Sans','Regular'),18)
 im=Image.new('RGB',(1800,600*math_ceil(len(rows)/3)),(235,237,233));d=ImageDraw.Draw(im)
 for i,r in enumerate(rows):
  ox=i%3*600;oy=i//3*600;a,b=np.array(r['bounds_mm']);size=b-a;scale=min(470/max(size[0],1),410/max(size[1],1));c=(a+b)/2
  def xy(p):return (ox+300+(p[0]-c[0])*scale,oy+300-(p[1]-c[1])*scale)
  d.text((ox+18,oy+12),r['title'],font=font,fill=(25,38,30));d.text((ox+18,oy+47),f"{r['axis']} = {r['station_mm']:g} mm | imported GLB triangles",font=small,fill=(52,65,54))
  for line in r['segments_mm']:d.line([xy(p) for p in line],fill=(28,113,105),width=2)
  d.text((ox+18,oy+540),f"Section {size[0]:.2f} × {size[1]:.2f} mm",font=font,fill=(25,38,30))
 out=BASE/'renders/checkpoint';out.mkdir(parents=True,exist_ok=True);im.save(out/'sections.jpg',quality=92)
def math_ceil(v):return int(__import__('math').ceil(v))
if __name__=='__main__':main()
