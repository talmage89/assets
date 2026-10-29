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
 ('Guard flat-band section',1,30,['TriggerGuard_Stamping']),
 *[('Rear saddle / '+str(y),1,y,['Sight_RearBlock','Sight_TangentLeaf','Sight_LeafSpring','Barrel']) for y in (195,220,246)],
 ('Gas forging / middle',2,100,['GasBlock_Neck']),
 ('Gas forging / center side',0,0,['GasBlock_Neck','Barrel','GasBlock_TubeSeat']),
 *[('Cover / '+str(y),1,y,['TopCover_Pressed']) for y in (20,100,170)],
 ('Grip lower side lands',2,-30,['PistolGrip_Sculpt'])]
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
def local_lines(lines,window):
 """Clip actual intersection segments; never redraw a measured section."""
 result=[]
 for a,b in lines:
  a=np.array(a);delta=np.array(b)-a;lo,hi=0.,1.
  for k,(minimum,maximum) in enumerate(window):
   if abs(delta[k])<1e-12:
    if not minimum<=a[k]<=maximum:hi=-1;break
   else:
    u,v=sorted(((minimum-a[k])/delta[k],(maximum-a[k])/delta[k]))
    lo=max(lo,u);hi=min(hi,v)
  if lo<=hi:result.append([(a+delta*lo).tolist(),(a+delta*hi).tolist()])
 return result
def round3_contacts():
 from kit import assembly
 objects={o.get('part_name',o.name):o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')}
 pairs=[('Handguard_SlingLoop','Handguard_SlingMount'),('Handguard_SlingLoop','Handguard_Retainer363'),
  ('Handguard_SlingMount','Handguard_Retainer363'),('Handguard_Retainer363','LowerHandguard_Sculpt'),
  ('GasBlock_Neck','Barrel'),('GasBlock_Neck','GasBlock_TubeSeat'),('GasBlock_Neck','Bayonet_Lug'),
  ('Sight_LeafSpring','Sight_RearBlock'),('Sight_LeafSpring','Sight_TangentLeaf')]
 rows=[]
 for a,b in pairs:
  gap,method=assembly.distance(objects[a],objects[b])
  rows.append(dict(parts=[a,b],surface_gap_mm=gap*1000,method=method,passed=gap<=.0002))
 assert all(r['passed'] for r in rows),rows
 return rows
def main():
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/ak.blend'));W.pose(bpy.data.objects['R39Armature'],'Idle',0);rows=[]
 for title,axis,s,names in CUTS:
  low={n:segments(bpy.data.objects[n],axis,s) for n in names}
  high={n:segments(bpy.data.objects['HIGH_'+n],axis,s) for n in names if bpy.data.objects.get('HIGH_'+n)}
  window=((400,458),(70,120)) if title=='Gas forging / center side' else None
  if window:
   low={n:local_lines(lines,window) for n,lines in low.items()}
   high={n:local_lines(lines,window) for n,lines in high.items()}
  points=[p for lines in low.values() for line in lines for p in line];assert points,title
  bounds=[[min(p[k] for p in points),max(p[k] for p in points)] for k in range(2)]
  rows.append(dict(title=title,station_mm=s,axis='XYZ'[axis],axes=['XYZ'[k] for k in range(3) if k!=axis],
   bounds_mm=bounds,dimensions_mm=[b-a for a,b in bounds],clip_window_mm=window,low=low,high=high))
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
 def bounds(name):
  ob=bpy.data.objects[name];q=np.array([tuple(ob.matrix_world@v.co) for v in ob.data.vertices])*1000
  return q.min(axis=0),q.max(axis=0)
 def width(name,axis):
  a,b=bounds(name);return float(b[axis]-a[axis])
 def cutbounds(name,axis,station):
  pts=np.array([p for line in segments(bpy.data.objects[name],axis,station) for p in line])
  return pts.min(axis=0),pts.max(axis=0)
 rear=[]
 for y in (195,220,246):
  a,b=cutbounds('Sight_RearBlock',1,y);c,d=cutbounds('Barrel',1,y)
  rear.append(dict(y_mm=y,top_z_mm=float(b[1]),barrel_top_z_mm=float(d[1]),above_barrel_mm=float(b[1]-d[1])))
 from kit import motion
 from mathutils import Vector
 tree=motion.surface(bpy.data.objects['Sight_FrontHood'])['tree']
 ray=Vector((.02,.552,.126));direction=Vector((-1,0,0))
 outer=tree.ray_cast(ray,direction,.04)[0]
 inner=tree.ray_cast(outer+direction*.00001,direction,.04)[0]
 gauge=(outer-inner).length*1000
 metrics['round3']=dict(rear=rear,leaf_width_mm=width('Sight_TangentLeaf',0),
  notch_width_mm=width('Sight_RearNotch',0),rear_block_width_mm=width('Sight_RearBlock',0),
  hood_depth_mm=width('Sight_FrontHood',1),hood_sheet_mm=gauge,
  hood_sheet_limit='two triangle intersections along X at Z126 / Y552',
  windage_drum_diameter_mm=width('Sight_WindageDrum',2),
  grip_envelope_mm=[width('PistolGrip_Sculpt',k) for k in range(3)])
 metrics['round3']['source_seating']=round3_contacts()
 from kit.weapon_verify import import_glb
 imported=import_glb(BASE/'build/ak.glb');W.pose(imported,'Idle',0)
 metrics['round3']['imported_seating']=round3_contacts()
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
