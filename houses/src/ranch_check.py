"""Actual ranch-surface audit; analytic checks and serialization are separate."""
import json
import math
from pathlib import Path
import bpy
from mathutils import Vector
from plan import generate,wall_frame,roof_blocks
from check_mesh import surface


def check(source):
 bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));bpy.context.view_layer.update()
 meta=json.loads(source.with_suffix('.json').read_text());p=generate(meta['seed'],meta['spec']);m,g=p['blocks']
 obs=[o for o in bpy.context.scene.objects if o.type=='MESH'];errors=[];total=0;minimum=100
 for ob in obs:
  ob.data.calc_loop_triangles();total+=len(ob.data.loop_triangles)
  if any(t.area<1e-12 for t in ob.data.loop_triangles):errors.append('Degenerate triangle '+ob.name)
  if any(not all(math.isfinite(v) for v in vert.co) for vert in ob.data.vertices):errors.append('Nonfinite '+ob.name)
  minimum=min(minimum,min((ob.matrix_world@v.co).z for v in ob.data.vertices))
 if total!=meta['triangles'] or total>80000:errors.append('Triangle budget/count')
 if minimum<-.001:errors.append(f'Below grade: {minimum}')
 roofs=surface([o for o in obs if o.get('component')=='roof'])
 blocks=([p['roof_envelope']] if p.get('roof_envelope') else roof_blocks(p['blocks']))+[p['porch']];misses=0;maxerr=0;samples=0
 lo=[min(v[k] for b in blocks for v in b.domain()) for k in (0,1)];hi=[max(v[k] for b in blocks for v in b.domain()) for k in (0,1)]
 for iy in range(49):
  y=lo[1]+(iy+.371)/49*(hi[1]-lo[1])
  for ix in range(103):
   x=lo[0]+(ix+.413)/103*(hi[0]-lo[0]);active=[b for b in blocks if b.contains(x,y,b.overhang)]
   if not active:continue
   z=max(b.height(x,y) for b in active);hit=roofs.ray_cast(Vector((x,y,20)),Vector((0,0,-1)),25);samples+=1
   if hit[0] is None:misses+=1
   else:maxerr=max(maxerr,abs(hit[0].z-z))
 if misses or maxerr>3e-5:errors.append(f'Roof holes/error {misses} / {maxerr}')
 walls=surface([o for o in obs if o.get('component')=='wall']);services=surface([o for o in obs if o.get('component')=='services'])
 blocked=[];occluded=[]
 for o in meta['openings']:
  b=next(b for b in p['blocks'] if b.name==o['block']);origin,t,n,l=wall_frame(b,o['face']);normal=Vector((*n,0))
  for du in (-.3,0,.3):
   for zh in (.20,.5,.8):
    point=Vector((origin[0]+t[0]*(o['u']+du*o['w']),origin[1]+t[1]*(o['u']+du*o['w']),o['z']+zh*o['h']))+normal*.4
    if walls.ray_cast(point,-normal,.65)[0] is not None:blocked.append(o['id'])
    if services.ray_cast(point,-normal,.70)[0] is not None:occluded.append(o['id'])
 if blocked:errors.append('Blocked wall opening '+str(set(blocked)))
 if occluded:errors.append('Service crosses opening '+str(set(occluded)))
 frames=surface([o for o in obs if o.get('component') in ('door_frame','carport_structure')]);sockets={}
 for name in ('FrontThreshold','GarageApron'):
  point=bpy.data.objects['Socket_'+name].matrix_world.translation
  sockets[name]=frames.find_nearest(point)[3]
 # Carport apron is a boundary datum beside the real slab, 130 mm beyond it.
 if sockets['FrontThreshold']>.0015:errors.append('Front threshold misses sill')
 if p['spec']['garage']['kind']=='garage' and sockets['GarageApron']>.0015:errors.append('Garage apron misses sill')
 supports=surface([o for o in obs if o.get('component') in ('wall','porch_structure','carport_structure')]);dist=[]
 for d in meta['drains']:
  a,c=map(Vector,(d['centerline'][3],d['centerline'][4]))
  for f in (.2,.5,.8):dist.append(supports.find_nearest(a.lerp(c,f))[3])
 if dist and max(dist)>.16:errors.append(f'Unsupported pipe {max(dist)}')
 # Read landing height from its actual top surface, not the metadata.
 entry=surface([o for o in obs if o.get('component')=='porch_steps']);porch=p['porch']
 hit=entry.ray_cast(Vector((porch.cx,porch.cy,2)),Vector((0,0,-1)),3)[0]
 landing=hit.z if hit else None
 if landing is None or abs(m.floor-landing-.028)>1e-5:errors.append('Entry threshold rise')
 foyer=surface([o for o in obs if o.get('component')=='foyer']);floorhit=foyer.ray_cast(Vector((p['door_x'],m.y0+.65,1.8)),Vector((0,0,-1)),2)[0]
 if floorhit is None or abs(floorhit.z-m.floor)>1e-5:errors.append('Foyer floor')
 patio=surface([o for o in obs if o.get('component')=='rear_landing']);o=next(o for o in meta['openings'] if o['kind']=='patio')
 rear=patio.ray_cast(Vector((m.x0+o['u'],m.y1+.3,2)),Vector((0,0,-1)),3)[0]
 if rear is None or abs(m.floor-rear.z-.028)>1e-5:errors.append('Rear landing rise')
 # Square or paired iron posts must physically bear on the stoop.
 posts=surface([o for o in obs if o.get('component')=='porch_structure']);postgaps=[]
 for x in (porch.x0+.14,porch.x1-.14):
  point=Vector((x,porch.y0+.17,landing-.1));bottom=posts.ray_cast(point,Vector((0,0,1)),.3)[0]
  if bottom is None:errors.append('Missing supported column')
  else:postgaps.append(abs(bottom.z-landing))
 if postgaps and max(postgaps)>1e-5:errors.append('Column floats')
 from ranch_revision_check import check as revision_check
 revision=revision_check(p,meta,obs)
 if errors:raise AssertionError(f"Ranch {meta['seed']}: "+'; '.join(sorted(set(errors))))
 return dict(revision=revision,passed=True,seed=meta['seed'],triangles=total,roof_rays=samples,roof_misses=misses,roof_max_error_m=maxerr,
  opening_rays=len(meta['openings'])*9,blocked_openings=blocked,service_occlusions=occluded,
  minimum_height_measured_m=minimum,socket_to_surface_m=sockets,downspout_support_max_m=max(dist),
  entry_landing_height_measured_m=landing,foyer_floor_height_measured_m=floorhit.z,rear_landing_height_measured_m=rear.z,
  post_landing_gaps_measured_m=postgaps,scope='Actual source surfaces, sampled; no structural engineering or final bake claim')
