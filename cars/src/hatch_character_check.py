"""H120 character measurements on actual game triangles and their parent normals.

Positions are mesh rays/plane cuts; normal angles interpolate authored parent
corner normals (as rendered). No stored design dimension is reported as measured.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
import hatch_spec as S
from hatch_check import mesh_tree,plane_cut,bounds,points
from hatch_fairness import field


def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--diagnostic',action='store_true')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.source).resolve();bpy.ops.wm.open_mainfile(filepath=str(src));bpy.context.view_layer.update()
 obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')=='Hatch']
 skins=[o for o in obs if o.get('part_category') in ['body','doors','glass','pillars','fascia']]
 ray=field(skins);tree=mesh_tree(skins);sections=[]
 for name,y,door in [('mid_front_door',(S.DOOR_FRONT+S.DOOR_SPLIT)/2,'Door F_R'),('b_pillar',S.DOOR_SPLIT+.035,'Door R_R'),('mid_rear_door',(S.DOOR_SPLIT+S.DOOR_REAR)/2,'Door R_R')]:
  def hit(z):
   row=ray((2,y,z),(-1,0,0))
   if row is None:raise ValueError(('Missing section',name,z))
   return row
  def lean(z):
   _,n,_=hit(z);return math.degrees(math.atan2(-n.z,n.x))
  shoulder=max((row[0] for i in range(161) if (row:=ray((2,y,.80+i*.001),(-1,0,0))) is not None),key=lambda p:p.x)
  cut=plane_cut([bpy.data.objects[door]],y)
  lower=min((p for segment in cut for p in segment if p[0]>.5),key=lambda p:p[1])
  # The maximum normal-turn interval locates the soft die crease, independently
  # of its design control. Search the actual low-door interval, excluding sill.
  probes=[(lower[1]+.045+i*.001) for i in range(120)]
  turning=[(abs(lean(z+.040)-lean(z-.040)),z) for z in probes]
  turn,line=max(turning)
  # Locate the shallow inward hollow with actual 50 mm chords through the
  # die-line region. Keep its location and span; do not confuse the outward
  # progressive crown farther up the door with this concave run.
  hollows=[]
  for i in range(75):
   zm=lower[1]+.030+i*.001
   hollows.append((hit(zm)[0].x-(hit(zm-.025)[0].x+hit(zm+.025)[0].x)/2,zm))
  hollow,hollow_z=min(hollows)
  sill=hit(.245)[0]
  sections.append(dict(name=name,y_m=y,shoulder_m=list(shoulder),door_lower_edge_xz_m=lower,
   shoulder_to_lower_edge_inset_m=shoulder.x-lower[0],lower_edge_to_sill_tuck_m=lower[0]-sill.x,
   upper_door_inward_degrees=[-lean(shoulder.z+d) for d in [.025,.040]],
   just_below_shoulder_lean_degrees=lean(shoulder.z-.040),lower_door_lean_degrees=lean(line+.070),
   lower_crease_height_m=line,lower_crease_normal_turn_80mm_degrees=turn,
   hollow_50mm_chord_m=hollow,hollow_center_z_m=hollow_z,segments_xz_m=plane_cut(skins,y)))
 mirrors={o.name:bounds([o]) for o in obs if o.name.startswith('Mirror housing')}
 span=bounds([o for o in obs if o.get('part_category')=='mirrors'])['size'][0]
 crown=[]
 # The cowl moved forward with the unchanged windscreen rake in round two.
 # Keep the aft crown sample on steel, 40 mm ahead of its new shut line.
 for y in [-1.60,-1.30,-1.14]:
  def top(x):return tree.ray_cast(Vector((x,y,3)),Vector((0,0,-1)),3)[0]
  edge=top(.76);candidates=[top(.79+i*.002) for i in range(61)];candidates=[p for p in candidates if p is not None]
  peak=max(candidates,key=lambda p:p.z)
  crown.append(dict(y_m=y,hood_side_edge_m=list(edge),fender_peak_m=list(peak),rise_m=peak.z-edge.z))
 # At a removed mouth, the nearest surviving paint can be a different panel
 # (notably the hood above the grille). Re-evaluate the uncut parent for the
 # measurement direction; the bed and mouth positions remain actual meshes.
 import hatch_body
 parent,_=hatch_body.master(2);parent_ray=field([parent])
 wells={}
 for ob in obs:
  if 'well_mouth_samples' not in ob:continue
  raw=list(ob['well_mouth_samples']);mouth=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];bed=mesh_tree([ob]);samples=[]
  for p0 in mouth[::max(1,len(mouth)//12)]:
   # The evaluated uncut parent defines the original skin normal at this hole.
   n=parent_ray.nearest_normal(p0)
   if n.dot(Vector((p0.x,-1 if p0.y<0 else 1,0)))<0:n.negate()
   hitp,_,_,dist=bed.ray_cast(p0+n*.025,-n,.150)
   if hitp is not None:samples.append(dict(mouth_m=list(p0),bed_m=list(hitp),normal_depth_m=dist-.025))
  # Independent axial rays through the central bed must not find paint in
  # front of it. This proves a cut opening, separately from bed depth.
  raw=list(ob['aperture_samples']);guides=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
  bb=bounds([ob])
  guide_bounds_valid=all(all(bb['min'][k]-.01<=p[k]<=bb['max'][k]+.01 for k in range(3)) for p in guides)
  nu,nv=ob['form_columns'],ob['form_rows'];clearance=[]
  # A three-column cutout has only one interior column. Its last column is
  # the mouth boundary, where hitting the return/painted lip is expected.
  for i in sorted({max(1,min(nu-2,i)) for i in [nu//3,nu//2,2*nu//3]}):
   p0=guides[(nv//2)*nu+i];out=Vector((p0.x,-1 if p0.y<0 else 1,0)).normalized()
   pp,_,_,dd=tree.ray_cast(p0+out*.10,-out,.115)
   clearance.append(dict(bed_guide_m=list(p0),ray_outward=list(out),paint_hit_m=list(pp) if pp is not None else None,paint_hit_distance_m=dd))
  wells[ob.name]=dict(depth_samples=samples,min_depth_m=min((r['normal_depth_m'] for r in samples),default=None),max_depth_m=max((r['normal_depth_m'] for r in samples),default=None),clearance_rays=clearance,world_guides_inside_mesh_bounds=guide_bounds_valid)
 floor=bounds([bpy.data.objects['Form cavity closure']]);half=max(abs(floor['min'][0]),abs(floor['max'][0]))
 tire_inboard=min(abs(p.x) for o in obs if o.name.startswith('Tire_') for p in points(o))
 closure=dict(bounds_m=floor,tire_axial_separation_m=tire_inboard-half,scope='Actual floor/tire extrema; positive X separation proves parked surface clearance and persists through wheel spin. Other motion remains deferred.')
 report=dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),scope='Actual game surfaces; interpolated parent corner-normal angles; finite sampling, not motion or delivery certification',sections=sections,mirrors=mirrors,mirror_span_m=span,fender_crowns=crown,opening_depths=wells,cavity_closure=closure)
 errors=[]
 for r in sections:
  if not all(15<=angle<=25 for angle in r['upper_door_inward_degrees']):errors.append(r['name']+' upper door lean')
  if r['hollow_50mm_chord_m']>-.0005:errors.append(r['name']+' shallow die hollow')
  if not .85<=r['shoulder_m'][2]<=.92:errors.append(r['name']+' shoulder height')
  if not .050<=r['shoulder_to_lower_edge_inset_m']<=.081:errors.append(r['name']+' lower-edge inset')
  if not .040<=r['lower_edge_to_sill_tuck_m']<=.060:errors.append(r['name']+' sill tuck')
  if not 3<=r['just_below_shoulder_lean_degrees']<=5:errors.append(r['name']+' upper lower-door lean')
  if not 12<=r['lower_door_lean_degrees']<=20:errors.append(r['name']+' low-door lean')
  if not 8<=r['lower_crease_normal_turn_80mm_degrees']<=15:errors.append(r['name']+' crease turn')
 for r in crown:
  if not .010<=r['rise_m']<=.030:errors.append('Fender crown at '+str(r['y_m']))
 if not 2.02<=span<=2.06:errors.append('Mirror span')
 if closure['tire_axial_separation_m']<=0:errors.append('Temporary closure reaches the tire envelopes')
 for name,row in wells.items():
  if not row['depth_samples']:errors.append(name+' missing depth coverage')
  if row['min_depth_m'] is not None and row['min_depth_m']<.001:errors.append(name+' insufficient positive recess depth')
  if not row['world_guides_inside_mesh_bounds']:errors.append(name+' guide coordinates are not world-space bed samples')
  if any(p['paint_hit_m'] is not None for p in row['clearance_rays']):errors.append(name+' painted skin remains in front of bed')
 for name,lo,hi in [('Low wide grille opening',.040,.080),('Plate pocket opening',.020,.030)]:
  row=wells[name]
  if row['min_depth_m'] is None or not lo<=row['min_depth_m']<=row['max_depth_m']<=hi:
   errors.append(name+' physical recess outside brief range')
 report.update(passed=not errors,errors=errors);Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ['sections','mirror_span_m','fender_crowns','errors']},indent=2))
 if errors and not a.diagnostic:raise AssertionError(errors)
if __name__=='__main__':main()
