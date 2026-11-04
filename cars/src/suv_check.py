"""Independent measurements of actual X220 triangles, rays and normal fields.

No constants are returned as measurements. Mechanical sweeps, final materials,
UVs, baking and export are deliberately outside this source form checkpoint.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
import suv_spec as S
from suv_measure import points,bounds,mesh_tree,plane_cut
from suv_fairness import field

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.source).resolve();bpy.ops.wm.open_mainfile(filepath=str(src));bpy.context.view_layer.update()
 obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')==S.ASSET_SET]
 skins=[o for o in obs if o.get('part_category') in ['body','doors','glass','pillars','fascia']]
 ray=field(skins);tree=mesh_tree(skins);alltree=mesh_tree(obs)
 opening_skin_tree=mesh_tree(skins+[o for o in obs if o.get('part_category')=='cladding' and 'bumper' in o.name])
 def hit(y,z):
  row=ray((2,y,z),(-1,0,0))
  if row is None:raise ValueError(('Missing side',y,z))
  return row
 def lean(y,z):
  _,n,_=hit(y,z);return math.degrees(math.atan2(-n.z,n.x))
 glass_ray=field([o for o in skins if 'side glazing' in o.name])
 sections=[]
 for name,y in [('mid_front_door',(S.DOOR_FRONT+S.DOOR_SPLIT)/2),('b_pillar',S.DOOR_SPLIT+.035),('mid_rear_door',(S.DOOR_SPLIT+S.DOOR_REAR)/2)]:
  shoulder=max((hit(y,.97+i*.001)[0] for i in range(150)),key=lambda p:p.x)
  turns=[(abs(lean(y,z+.04)-lean(y,z-.04)),z) for z in [.46+i*.001 for i in range(180)]];turn,line=max(turns)
  hollow,hz=min((hit(y,z)[0].x-(hit(y,z-.025)[0].x+hit(y,z+.025)[0].x)/2,z) for z in [.51+i*.001 for i in range(110)])
  frame_lo,frame_hi=1.25,1.51;fl,fh=hit(y,frame_lo),hit(y,frame_hi)
  valid=[z for z in [1.15+i*.001 for i in range(500)] if glass_ray((2,y,z),(-1,0,0)) is not None]
  if not valid:raise ValueError(('No actual side pane at section',name))
  bottom,top=min(valid),max(valid);lo=bottom+.20*(top-bottom);hi=bottom+.80*(top-bottom)
  xl,xh=glass_ray((2,y,lo),(-1,0,0))[0].x,glass_ray((2,y,hi),(-1,0,0))[0].x
  sections.append(dict(name=name,y_m=y,segments_xz_m=plane_cut(skins,y),shoulder_m=list(shoulder),
   upper_inward_degrees=[-lean(y,shoulder.z+d) for d in [.030,.055]],just_below_degrees=lean(y,shoulder.z-.04),
   low_door_degrees=lean(y,line+.070),crease_height_m=line,crease_normal_turn_80mm_degrees=turn,
   hollow_50mm_chord_m=hollow,hollow_center_z_m=hz,tumblehome_degrees=math.degrees(math.atan2(xl-xh,hi-lo)),tumblehome_samples_m=[[xl,lo],[xh,hi]],
   glass_span_z_m=[bottom,top],glass_angle_method='Central 60 percent of the actual ray-hit side-pane height, excluding its rounded border',
   fixed_height_chord_debug=dict(degrees=math.degrees(math.atan2(fl[0].x-fh[0].x,frame_hi-frame_lo)),sample_parts=[fl[2],fh[2]],z_m=[frame_lo,frame_hi],scope='All-skin rays at legacy fixed heights; this can cross onto windshield/roof and is not a glass angle')))
 parts={};categories={};parents={}
 for o in obs:
  o.data.calc_loop_triangles();n=len(o.data.loop_triangles);parts[o.name]=n;k=o['part_category'];categories[k]=categories.get(k,0)+n;parents[o.parent.name]=parents.get(o.parent.name,0)+n
 bb=bounds([o for o in obs if o.get('part_category')!='mirrors']);wheel={n:list(bpy.data.objects['Wheel_'+n].matrix_world.translation) for n in ['FL','FR','RL','RR']}
 arches=[]
 for code in wheel:
  tb=bounds([bpy.data.objects['Tire_'+code]]);ab=bounds([bpy.data.objects['Arch flange_'+code]])
  arches.append(dict(wheel=code,tire_bounds_m=tb,arch_bounds_m=ab,crown_gap_m=ab['max'][2]-tb['max'][2]))
 hood=points(bpy.data.objects['Hood outer']);roof=points(bpy.data.objects['Roof'])
 hoodfront=min((p for p in hood if abs(p.x)<.03),key=lambda p:p.y)
 # Windshield centerline points; near-border means actual physical boundary.
 wind=points(bpy.data.objects['Windshield']);center=[p for p in wind if abs(p.x)<.03];lo=min(center,key=lambda p:p.z);hi=max(center,key=lambda p:p.z)
 rake=math.degrees(math.atan2(hi.y-lo.y,hi.z-lo.z))
 back=bpy.data.objects['Backlight'];bps=points(back);low=min(p.z for p in bps);high=max(p.z for p in bps)
 widths={k:2*max(abs(p.x) for p in bps if abs(p.z-z)<.018) for k,z in [('base',low),('top',high)]}
 bc=[p for p in bps if abs(p.x)<.03];bl=min(bc,key=lambda p:p.z);bt=max(bc,key=lambda p:p.z)
 backrake=math.degrees(math.atan2(abs(bl.y-bt.y),bt.z-bl.z))
 belt_points=[q for o in skins if o.get('part_category')!='glass' for q in points(o) if q.y>1.5 and abs(q.z-low)<.018]
 rear_belt_width=2*max(abs(q.x) for q in belt_points)
 mirror={o.name:bounds([o]) for o in obs if o.name.startswith('Mirror housing')}
 lamps={}
 for ob in obs:
  if not ob.name.startswith(('Headlamp opening','Taillamp opening')) or 'aperture_samples' not in ob:continue
  raw=list(ob['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];nu,nv=ob['form_columns'],ob['form_rows'];row=ps[(nv//2)*nu:(nv//2+1)*nu]
  lamps[ob.name]=dict(centerline_length_m=sum((b-a).length for a,b in zip(row,row[1:])),maximum_height_m=max((ps[(nv-1)*nu+i]-ps[i]).length for i in range(nu)),fore_aft_return_m=max(p.y for p in row)-min(p.y for p in row))
  clear=[]
  for i in [nu//3,nu//2,2*nu//3]:
   q=row[i];n=ray.nearest_normal(q)
   if n.dot(Vector((q.x,-1 if q.y<0 else 1,0)))<0:n=-n
   ph,_,_,_=opening_skin_tree.ray_cast(q+n*.030,-n,.033);clear.append(ph is None)
  lamps[ob.name]['paint_clearance_rays']=clear
 wells={}
 for ob in obs:
  if 'well_mouth_samples' not in ob:continue
  raw=list(ob['well_mouth_samples']);mouth=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];bed=mesh_tree([ob]);samples=[]
  for q in mouth[::max(1,len(mouth)//12)]:
   n=ray.nearest_normal(q);n=n if n.dot(Vector((q.x,-1 if q.y<0 else 1,0)))>0 else -n
   ph,_,_,dist=bed.ray_cast(q+n*.025,-n,.16)
   if ph is not None:samples.append(dict(mouth_m=list(q),bed_m=list(ph),depth_m=dist-.025))
  raw=list(ob['aperture_samples']);guides=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];nu,nv=ob['form_columns'],ob['form_rows'];clear=[]
  for i in [nu//3,nu//2,2*nu//3]:
   q=guides[(nv//2)*nu+i];n=bed.find_nearest(q)[1];n=n if n.dot(Vector((q.x,-1 if q.y<0 else 1,0)))>0 else -n;ph,_,_,_=opening_skin_tree.ray_cast(q+n*.12,-n,.125);clear.append(ph is None)
  wells[ob.name]=dict(min_depth_m=min((r['depth_m'] for r in samples),default=None),max_depth_m=max((r['depth_m'] for r in samples),default=None),samples=samples,paint_clearance_rays=clear)
 cases={}
 for ob in obs:
  if 'case_loop_vertices' not in ob:continue
  n=ob['case_loop_vertices'];ps=points(ob);depths=[(ps[n+i]-ps[i]).length for i in range(n)]
  cases[ob.name]=dict(minimum_wall_depth_m=min(depths),maximum_wall_depth_m=max(depths),scope='Actual paired mouth/back vertex groups of the closed molded cassette')
 # Ground-tangent slope for the actual outer surfaces beyond each tire patch.
 approaches={}
 for front in [True,False]:
  wheel_code='FR' if front else 'RR';axle=wheel[wheel_code][1];hub_z=wheel[wheel_code][2]
  tire_box=bounds([bpy.data.objects['Tire_'+wheel_code]])
  rolling_radius=(tire_box['max'][2]-tire_box['min'][2])/2;rows=[]
  for o in obs:
   if o.get('part_category') in ['tires','wheels','mirrors','rails']:continue
   for q in points(o):
    dy=(axle-q.y) if front else (q.y-axle)
    if dy>rolling_radius+.001 and q.z>.015:
     lo_a,hi_a=0.,math.radians(89)
     for _ in range(44):
      aa=(lo_a+hi_a)/2
      tangent_height=dy*math.tan(aa)+hub_z-rolling_radius/math.cos(aa)
      if tangent_height>q.z:hi_a=aa
      else:lo_a=aa
     rows.append((math.degrees((lo_a+hi_a)/2),list(q),o.name))
  angle,q,name=min(rows);approaches['approach' if front else 'departure']=dict(degrees=angle,limiting_point_m=q,part=name,tire_extent_radius_m=rolling_radius,hub_z_m=hub_z,ground_contact_angle_degrees=math.degrees(math.atan2(q[2],abs(q[1]-axle))),method='Minimum supporting plane tangent to a mean circle fitted from actual tire extents/hub, tested against actual outer-form vertices. Original ground-contact estimate retained separately; suspension/loading not simulated')
 swells={}
 for name,y in [('front',S.FRONT_AXLE),('rear',S.REAR_AXLE)]:
  z=.90;swells[name]=dict(fender_m=list(hit(y,z)[0]),door_m=list(hit(0,z)[0]),swell_m=hit(y,z)[0].x-hit(0,z)[0].x)
 crowns=[]
 hood_object=bpy.data.objects['Hood outer'];hood_tree=mesh_tree([hood_object]);fender_tree=mesh_tree([bpy.data.objects['Front fender_R']])
 for y in [-1.60,-1.40,-1.25]:
  cuts=plane_cut([hood_object],y);edge_x=max(p[0] for segment in cuts for p in segment)
  edge=hood_tree.ray_cast(Vector((edge_x-.001,y,3)),Vector((0,0,-1)),3)[0]
  tops=[fender_tree.ray_cast(Vector((edge_x+i*.002,y,3)),Vector((0,0,-1)),3)[0] for i in range(110)];tops=[p for p in tops if p is not None]
  peak=max(tops,key=lambda p:p.z);crowns.append(dict(y_m=y,hood_boundary_x_m=edge_x,hood_edge_m=list(edge),fender_peak_m=list(peak),rise_m=peak.z-edge.z,scope='Actual hood plane-cut boundary, sampled 1 mm inboard to avoid its gauge rim; actual adjacent fender maximum'))
 # Separate molding dimensions are measured on actual mesh surfaces.
 moldings={}
 for o in obs:
  if not o.name.startswith('Lower door cladding'):continue
  bbm=bounds([o]);yc=(bbm['min'][1]+bbm['max'][1])/2;sgn=-1 if bbm['max'][0]<0 else 1;ct=mesh_tree([o]);probes=[]
  for z in [.32,.36,.41]:
   pc=ct.ray_cast(Vector((sgn*2,yc,z)),Vector((-sgn,0,0)),3)[0]
   pp=tree.ray_cast(Vector((sgn*2,yc,z)),Vector((-sgn,0,0)),3)[0]
   if pc is not None and pp is not None:probes.append(dict(z_m=z,proud_x_m=sgn*(pc.x-pp.x)))
  moldings[o.name]=dict(bounds_m=bbm,proud_samples=probes)
 arch_molding={}
 for code in wheel:
  co=bpy.data.objects['Arch cladding_'+code];fl=bpy.data.objects['Arch flange_'+code];cb=bounds([co]);fb=bounds([fl]);axle=wheel[code][1];sgn=-1 if wheel[code][0]<0 else 1;ct=mesh_tree([co]);probes=[]
  for dz in [.010,.025,.045]:
   z=fb['max'][2]+dz;pc=ct.ray_cast(Vector((sgn*2,axle,z)),Vector((-sgn,0,0)),3)[0];pp=tree.ray_cast(Vector((sgn*2,axle,z)),Vector((-sgn,0,0)),3)[0]
   if pc is not None and pp is not None:probes.append(dict(z_m=z,proud_x_m=sgn*(pc.x-pp.x)))
  arch_molding[code]=dict(crown_band_width_m=cb['max'][2]-fb['max'][2],proud_samples=probes)
 plate_ob=bpy.data.objects['Plate pocket opening'];raw=list(plate_ob['well_mouth_samples']);mouth=[raw[i:i+3] for i in range(0,len(raw),3)]
 plate=dict(mouth_x_extent_m=max(p[0] for p in mouth)-min(p[0] for p in mouth),mouth_z_extent_m=max(p[2] for p in mouth)-min(p[2] for p in mouth))
 plan={}
 for front in [True,False]:
  z=.710 if front else .750;ps=[]
  for x in [.65,.70,.75]:
   q=tree.ray_cast(Vector((x,-4 if front else 4,z)),Vector((0,1 if front else -1,0)),5)[0]
   if q is not None:ps.append(q)
  if len(ps)==3:
   aa,bbp,cc=ps;area=(bbp-aa).cross(cc-aa).length/2;radius=(bbp-aa).length*(cc-bbp).length*(aa-cc).length/(4*area)
   plan['front' if front else 'rear']=dict(local_plan_radius_m=radius,actual_samples_m=[list(p) for p in ps],scope='Finite three-point circle on source skin, not constant radius')
 seams={}
 for side in ['L','R']:
  front=bpy.data.objects['Door F_'+side];rear=bpy.data.objects['Door R_'+side];rt=mesh_tree([rear]);pf=points(front);edge=max(p.y for p in pf)
  distances=[rt.find_nearest(p)[3] for p in pf if p.y>edge-.012 and .65<p.z<1.00]
  seams[side]=dict(samples=len(distances),minimum_m=min(distances),maximum_m=max(distances))
 report=dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),stage='source form only',quality=bpy.context.scene['quality'],surface_cage=json.loads(bpy.data.objects[S.NAME]['surface_cage']),
  bounds_m=bb,full_bounds_m=bounds(obs),triangles=sum(parts.values()),triangles_per_category=categories,triangles_per_mesh=parts,triangles_per_parent=parents,
  wheel_centers_m=wheel,wheelbase_m=wheel['RR'][1]-wheel['FR'][1],tracks_m={e:wheel[e+'R'][0]-wheel[e+'L'][0] for e in ['F','R']},
  overhangs_m=dict(front=wheel['FR'][1]-bb['min'][1],rear=bb['max'][1]-wheel['RR'][1]),sections=sections,
  hood_leading_center_m=list(hoodfront),roof_peak_m=list(max(roof,key=lambda p:p.z)),windshield_rake_degrees=rake,windshield_endpoints_m=[list(lo),list(hi)],
  backlight=dict(widths_m=widths,height_m=bt.z-bl.z,rake_degrees=backrake,endpoints_m=[list(bl),list(bt)],body_belt_width_m=rear_belt_width,d_pillar_belt_width_m=(rear_belt_width-widths['base'])/2,scope='Actual glass end-band widths/centerline height and painted rear body width in the same 18 mm base-height band; rear projection estimate'),
  arches=arches,mirrors=mirror,mirror_span_m=bounds([o for o in obs if o.get('part_category')=='mirrors'])['size'][0],lamps=lamps,openings=wells,angles=approaches,fender_swell=swells,fender_crowns=crowns,
  door_seams=seams,lower_door_moldings=moldings,arch_moldings=arch_molding,plate_pocket=plate,corner_plan=plan,
  hood_rise_degrees=math.degrees(math.atan2(lo.z-hoodfront.z,lo.y-hoodfront.y)),
  optical_cassettes=cases,materials=sorted({m.name for o in obs for m in o.data.materials if m}),image_textures=len([im for im in bpy.data.images if im.users and im.source=='FILE']),
  deferred=['interior','underbody / actual running ground clearance','mechanical hinge/steering sweeps','UV/bake/delivery GLB','paint and causal wear'])
 from suv_round2_measure import measure as round2_measure
 report['round2']=round2_measure(obs)
 errors=[]
 for sec in sections:
  if not all(12<=v<=20 for v in sec['upper_inward_degrees']):errors.append(sec['name']+' upper door')
  if not 3<=sec['just_below_degrees']<=5:errors.append(sec['name']+' lower initial lean')
  if not 10<=sec['low_door_degrees']<=18:errors.append(sec['name']+' lower progressive lean')
  if not 8<=sec['crease_normal_turn_80mm_degrees']<=15:errors.append(sec['name']+' crease turn')
  if not 15<=sec['tumblehome_degrees']<=22:errors.append(sec['name']+' tumblehome')
 if report['quality']=='game' and report['triangles']>60000:errors.append('Source allocation exceeds 60k')
 if abs(report['wheelbase_m']-S.WHEELBASE)>1e-5:errors.append('Wheelbase')
 if any(not .040<=r['crown_gap_m']<=.070 for r in arches):errors.append('Arch crown clearance')
 if not 55<=rake<=60:errors.append('Windshield rake')
 if not 20<=backrake<=35:errors.append('Backlight rake')
 if not .250<=bt.z-bl.z<=.360:errors.append('Backlight height outside the reference-photo construction range')
 if any(not all(v for v in r['paint_clearance_rays']) for r in wells.values()):errors.append('Paint remains over a recess')
 if any(not all(r['paint_clearance_rays']) for r in lamps.values()):errors.append('Paint remains over an optical aperture')
 report.update(passed=not errors,errors=errors);Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(report,indent=2))
 print(json.dumps({k:report[k] for k in ['triangles','bounds_m','overhangs_m','windshield_rake_degrees','backlight','errors']},indent=2))
 if errors:raise AssertionError(errors)
if __name__=='__main__':main()
