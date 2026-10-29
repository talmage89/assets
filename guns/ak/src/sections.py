"""Dimensioned actual-triangle section evidence; no authoring constants reported as measurements."""
import json,sys
from pathlib import Path
import bpy,numpy as np
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import weapon as W
BASE=Path(__file__).resolve().parents[1]
CUTS=[('Receiver at magazine well',1,143,['Receiver_Sheet']),
 ('Receiver at selector',1,5,['Receiver_Sheet']),
 *[(name+' / '+str(y),1,y,[name+'_Sculpt']) for name,ys in [('LowerHandguard',(245,330)),('UpperHandguard',(265,325)),('Stock',(-220,-95))] for y in ys],
 ('Pistol grip',2,-5,['PistolGrip_Sculpt']),
 ('Magazine',2,-35,['Magazine_Sheet']),
 ('Front sight / collar',1,552,['Sight_FrontTower','Barrel']),
 ('Front sight / drum',2,117,['Sight_FrontTower','Sight_WindageDrum','Sight_FrontHood','Sight_FrontPost']),
 ('Guard flat-band section',1,30,['TriggerGuard_Stamping'])]
def segments(o,axis,station):
 o.data.calc_loop_triangles();p=np.array([tuple(o.matrix_world@v.co) for v in o.data.vertices])*1000
 t=p[np.array([t.vertices for t in o.data.loop_triangles])];d=t[:,:,axis]-station
 keep=(d.min(axis=1)<0)&(d.max(axis=1)>0);t=t[keep];d=d[keep];out=[[] for _ in t]
 for a,b in ((0,1),(1,2),(2,0)):
  keep=d[:,a]*d[:,b]<0;idx=np.where(keep)[0];u=-d[keep,a]/(d[keep,b]-d[keep,a])
  hits=t[keep,a]+(t[keep,b]-t[keep,a])*u[:,None]
  for i,v in zip(idx,hits):out[i].append(v)
 axes=[i for i in range(3) if i!=axis]
 return [[[float(p[k]) for k in axes] for p in line] for line in out if len(line)==2]
def main():
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/ak.blend'));W.pose(bpy.data.objects['R39Armature'],'Idle',0);rows=[]
 for title,axis,s,names in CUTS:
  low={n:segments(bpy.data.objects[n],axis,s) for n in names}
  high={n:segments(bpy.data.objects['HIGH_'+n],axis,s) for n in names if bpy.data.objects.get('HIGH_'+n)}
  points=[p for lines in low.values() for line in lines for p in line];assert points,title
  bounds=[[min(p[k] for p in points),max(p[k] for p in points)] for k in range(2)]
  rows.append(dict(title=title,station_mm=s,axis='XYZ'[axis],axes=['XYZ'[k] for k in range(3) if k!=axis],
   bounds_mm=bounds,dimensions_mm=[b-a for a,b in bounds],low=low,high=high))
 (BASE/'build/sections.json').write_text(json.dumps(rows,indent=2))
 # These are measurements on the evaluated game triangles, not a restatement
 # of the generator's control points. Cross-section centers describe the bow.
 trigger=bpy.data.objects['Trigger_Shoe']
 p=np.array([tuple(trigger.matrix_world@v.co) for v in trigger.data.vertices])*1000
 lo=p.min(axis=0);hi=p.max(axis=0);centerline=[]
 for z in np.linspace(lo[2]+1,hi[2]-1,18):
  hits=[v for line in segments(trigger,2,float(z)) for v in line]
  if hits:centerline.append([float((min(v[1] for v in hits)+max(v[1] for v in hits))/2),float(z)])
 first,last=np.array(centerline[0]),np.array(centerline[-1]);direction=last-first
 bow=max(abs(direction[0]*(v[1]-first[1])-direction[1]*(v[0]-first[0]))/np.linalg.norm(direction) for v in centerline)
 tip=p[p[:,2]<lo[2]+.5].mean(axis=0)
 guard=next(r for r in rows if r['title']=='Guard flat-band section')
 metrics=dict(trigger=dict(envelope_mm=(hi-lo).tolist(),low_tip_mm=tip.tolist(),
  section_centerline_yz_mm=centerline,maximum_chord_bow_mm=float(bow),
  limit='section-center bow, not a circular radius or mechanical dimension'),
  guard=dict(section_xz_mm=guard['dimensions_mm'],station_y_mm=30))
 (BASE/'build/form-measurements.json').write_text(json.dumps(metrics,indent=2))
 from PIL import Image,ImageDraw,ImageFont
 from kit.fonts import find_font
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),20);small=ImageFont.truetype(find_font('Noto Sans','Regular'),16)
 sheet=Image.new('RGB',(1500,55+455*((len(rows)+2)//3)),(238,238,234));d=ImageDraw.Draw(sheet)
 d.text((20,12),'Rill 39 / actual game and dense-source section intersections / mm',font=font,fill=(25,35,30))
 for i,r in enumerate(rows):
  x=i%3*500;y=55+i//3*455;b=r['bounds_mm'];ds=r['dimensions_mm'];cx=sum(b[0])/2;cy=sum(b[1])/2
  scale=min(410/max(ds[0],1),290/max(ds[1],1))
  def project(p):return (x+250+(p[0]-cx)*scale,y+225-(p[1]-cy)*scale)
  d.text((x+12,y+5),r['title'],font=font,fill=(25,35,30))
  d.text((x+12,y+35),f"{r['axis']} {r['station_mm']:g} | {r['axes'][0]} {ds[0]:.2f} × {r['axes'][1]} {ds[1]:.2f}",font=small,fill=(25,35,30))
  for layer,color,width in [('high',(20,145,140),4),('low',(138,58,32),1)]:
   for lines in r[layer].values():
    for line in lines:d.line([project(p) for p in line],fill=color,width=width)
  d.text((x+12,y+402),'brown: game | teal: retained dense sculpt',font=small,fill=(40,50,45))
 out=BASE/'renders/checkpoint';out.mkdir(parents=True,exist_ok=True);sheet.save(out/'sections.jpg',quality=93)
 print('SECTIONS',len(rows))
if __name__=='__main__':main()
