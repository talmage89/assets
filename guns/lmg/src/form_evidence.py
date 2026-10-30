"""Measured exterior form and decorative interleaving from the imported GLB."""
import json,sys,math
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import weapon as W,weapon_verify as V,assembly
from check import bounds
from sections import segments
BASE=Path(__file__).resolve().parents[1]

def points(ob):
 ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
 p=np.array([tuple(ev.matrix_world@v.co) for v in me.vertices])*1000;ev.to_mesh_clear();return p

def circle(p):
 q=np.unique(np.round(p,5),axis=0)
 a=np.c_[2*q,np.ones(len(q))];v=np.linalg.lstsq(a,(q*q).sum(axis=1),rcond=None)[0]
 c=v[:2];r=np.sqrt(max(0,v[2]+c@c));return c,r

def main():
 arm=V.import_glb(BASE/'build/lmg.glb');W.pose(arm,'Idle',0)
 def ob(name):return next(o for o in bpy.context.scene.objects if o.name==name)
 result={'scope':'Exterior visual fit. Decorative links and ready witnesses do not certify a working mechanism.'}
 result['stock_sections_mm']={}
 for station in (-305,-275,-220,-180,-122.2243655948854,-115,-90.12188772331137,-60):
  lines=segments(ob('Stock_Sculpt'),1,station);p=np.array([p for l in lines for p in l]);lo,hi=p.min(axis=0),p.max(axis=0)
  result['stock_sections_mm'][str(station)]=dict(width=hi[0]-lo[0],bottom=lo[1],comb=hi[1],height=hi[1]-lo[1],toe_drop_below_bore=105-lo[1])
 a,b=bounds(ob('Buttpad'));result['butt_height_mm']=(b[2]-a[2])*1000
 barrel_lo,barrel_hi=bounds(ob('Barrel_Exterior'));bore=(barrel_lo[2]+barrel_hi[2])*500
 result['butt_bounds_mm']=[(a*1000).tolist(),(b*1000).tolist()];result['toe_drop_below_bore_mm']=bore-a[2]*1000
 result['receiver_rivets_mm']={}
 for side in (-1,1):
  names=sorted(o.name for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('Receiver_Rivet_'+str(side)+'_'))
  result['receiver_rivets_mm'][str(side)]={name:((sum(bounds(ob(name)))*500).tolist()) for name in names}
 result['wall_gauges_mm']={}
 for name,y,z in [('Receiver_Sheet',40,110),('FeedCover_Shell',80,132),('Handguard_Sculpt',280,60),('Box_Shell',164,-50)]:
  _,_,tree=assembly.surface(ob(name));p0=Vector((0,y*.001,z*.001));direction=Vector((1,0,0))
  first=tree.ray_cast(p0,direction,.1);second=tree.ray_cast(first[0]+direction*.000001,direction,.1)
  assert first[0] is not None and second[0] is not None,name
  result['wall_gauges_mm'][name]=(second[0]-first[0]).length*1000
 result['handguard_sections_mm']={}
 for station in (280,440):
  p=np.array([p for l in segments(ob('Handguard_Sculpt'),1,station) for p in l]);lo,hi=p.min(axis=0),p.max(axis=0)
  q=p[(p[:,0]>hi[0]-2.7)&(p[:,1]<lo[1]+5)]
  _,radius=circle(q)
  result['handguard_sections_mm'][str(station)]=dict(width=hi[0]-lo[0],height=hi[1]-lo[1],bottom=lo[1],top=hi[1],outside_corner_circle_fit_radius=radius)
 p=points(ob('RearSight_Aperture'));r=np.hypot(p[:,0],p[:,2]-176)
 result['rear_sight_mm']=dict(aperture_outer_diameter=2*r.max(),aperture_hole=2*r.min(),ears={})
 for side in (-1,1):
  a,b=bounds(ob('RearSight_Ear_'+str(side)));result['rear_sight_mm']['ears'][str(side)]=dict(thickness=(b[0]-a[0])*1000,height=(b[2]-a[2])*1000)
  p=points(ob('RearSight_Dial_'+str(side)));cy,cz=((-30,159) if side==-1 else (-5,170));result['rear_sight_mm']['knob_diameter']=2*np.hypot(p[:,1]-cy,p[:,2]-cz).max()
 # Actual finite plate thickness at broad lands, not the assigned gauge value.
 a,b=bounds(ob('FeedTray_Pan'));result['tray_thickness_mm']=(b[2]-a[2])*1000
 result['bipod_mm']={}
 for clip,frame,key in [('BipodDeploy',54,'retracted'),('BipodDeploy',84,'extended')]:
  W.pose(arm,clip,frame)
  for side in ('L','R'):
   hinge=arm.pose.bones['Bipod'+side].matrix.translation*1000
   foot=points(ob('Bipod_Foot_'+side));distance=np.linalg.norm(foot-np.array(hinge),axis=1)
   centered=foot-foot.mean(axis=0);_,_,axes=np.linalg.svd(centered,full_matrices=False)
   spans=np.ptp(centered@axes.T,axis=0);tilt=math.degrees(math.acos(min(1,abs(axes[-1,2]))))
   result['bipod_mm'].setdefault(side,{})[key]=dict(pad_principal_spans_mm=spans.tolist(),pad_plane_tilt_from_horizontal_degrees=tilt,hinge_to_farthest_pad_point=distance.max(),hinge_to_pad_centroid=np.linalg.norm(foot.mean(axis=0)-np.array(hinge)),foot_width=(foot[:,0].max()-foot[:,0].min()))
 W.pose(arm,'Idle',0)
 a,b=bounds(ob('Bipod_Yoke'));result['bipod_yoke_dimensions_mm']=((b-a)*1000).tolist()
 q=np.array([p for line in segments(ob('Bipod_Channel_L'),1,400) for p in line])
 result['bipod_leg_section_mm']=(q.max(axis=0)-q.min(axis=0)).tolist()
 # Fit centers to actual inner cuff vertices. The three axial bands are
 # recovered from their mesh Y levels, and fitted independently of bone heads.
 links=[];rounds=[]
 for i in range(16):
  p=points(ob(f'Belt_Link_{i:02d}'));bands=[]
  for level in (153.,160.,168.):
   q=p[np.abs(p[:,1]-level)<.001][:,[0,2]];c,r=circle(q)
   q=q[np.linalg.norm(q-c,axis=1)<5.4];c,r=circle(q);bands.append(dict(center=c.tolist(),inner_radius=r))
  links.append(bands)
  p=points(ob(f'Belt_Round_{i:02d}'));q=p[np.abs(p[:,1]-148)<.001][:,[0,2]];c,r=circle(q);rounds.append(c)
 levels=sorted(set(np.round(points(ob('Belt_Link_00'))[:,1],3)))
 base=points(ob('Belt_Round_00'))[:,1].min()
 bands=[float(v-base) for v in levels if any(abs(v-t)<.001 for t in (153,157,160,165,168,172))]
 gaps=[bands[2]-bands[1],bands[4]-bands[3]]
 p=points(ob('Belt_Round_16'));q=p[np.abs(p[:,1]-148)<.001][:,[0,2]];c,r=circle(q);rounds.append(c)
 rows=[]
 for i in range(16):
  previous=links[i]
  rows.append(dict(link=i,next_link=i+1 if i<15 else None,next_round=i+1,
   double_loop_to_own_round_error_mm=max(np.linalg.norm(np.array(previous[k]['center'])-rounds[i]) for k in (0,2)),
   single_loop_to_next_round_error_mm=np.linalg.norm(np.array(previous[1]['center'])-rounds[i+1]),
   single_between_next_double_axial_gaps_mm=gaps if i<15 else None,
   inner_radius_mm=previous[1]['inner_radius']))
 assert max(r['single_loop_to_next_round_error_mm'] for r in rows)<.01
 assert max(r['double_loop_to_own_round_error_mm'] for r in rows)<.01
 # Recover and verify the axial ordering from actual vertex levels too.
 ylevels=sorted(set(np.round(points(ob('Belt_Link_00'))[:,1],3)))
 actual=[float(v) for v in ylevels if any(abs(v-t)<.001 for t in (153,157,160,165,168,172))]
 assert actual==[153,157,160,165,168,172],actual
 result['link_interleaving']=dict(axial_band_endpoints_mm=actual,rows=rows,verified_visible_neighbor_pairs=len(rows)-1,verified_single_cuff_rounds=len(rows),maximum_single_center_error_mm=max(r['single_loop_to_next_round_error_mm'] for r in rows),limitation='Decorative cuffs only; no retention-force or feed-function claim. Axial gaps are measured between recovered mesh band endpoints.')
 # Draw real mesh intersections through two consecutive links and their rounds.
 from PIL import Image,ImageDraw,ImageFont
 from kit.fonts import find_font
 im=Image.new('RGB',(1600,900),(237,239,234));d=ImageDraw.Draw(im);font=ImageFont.truetype(find_font('Noto Sans','Regular'),24)
 objects=[('Belt_Round_00',(122,99,56)),('Belt_Round_01',(122,99,56)),('Belt_Link_00',(20,105,115)),('Belt_Link_01',(173,67,45))]
 def xy(p):return (250+(p[1]-145)*18,350-p[0]*18)
 for name,color in objects:
  for line in segments(ob(name),2,124.15):d.line([xy(p) for p in line],fill=color,width=3)
 d.text((30,20),'Z = 124.15 mm | actual imported triangle sections | two consecutive links',font=font,fill=(25,40,35))
 d.text((30,68),'Teal link 00: two cuffs on round 00; single cuff centered on round 01',font=font,fill=(20,105,115))
 d.text((30,110),'Rust link 01: its double cuffs straddle link 00 single cuff around round 01',font=font,fill=(173,67,45))
 d.text((30,820),'Axial bands: 8–12 / 15–20 / 23–27 mm from decorative case base; gaps 3 / 3 mm.',font=font,fill=(25,40,35))
 im.save(BASE/'renders/checkpoint/link-interleaving-section.jpg',quality=94)
 tri=json.loads((BASE/'build/triangles.json').read_text());from collections import Counter
 group=Counter()
 for name,count in tri['parts'].items():group[name.split('_')[0]]+=count
 result['triangles_by_group']=dict(group);result['triangles']=tri['triangles']
 (BASE/'build/form-round2.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
