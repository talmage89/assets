"""Build original road-derived equipment libraries and reusable game parts."""
import argparse,sys,json,hashlib,math
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import model as G
from plan import *
import graphics
from geometry import *
import equipment as E
from layout import SITES
from dataclasses import replace

def export(path,objects=None):
 bpy.ops.object.select_all(action='DESELECT')
 if objects is None:objects=list(bpy.context.scene.objects)
 for o in objects:o.select_set(True)
 path.parent.mkdir(parents=True,exist_ok=True)
 bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLB',use_selection=True,export_extras=True,export_apply=True,export_yup=True,export_cameras=False,export_lights=False)
 from deliver import state_factors
 state_factors(path)
 return path.stat().st_size
def bounds(rt):
 pts=[o.matrix_world@v.co for o in rt.children_recursive if o.type=='MESH' for v in o.data.vertices]
 return [[min(p[i] for p in pts) for i in range(3)],[max(p[i] for p in pts) for i in range(3)]] if pts else None
def build(plan,out):
 bpy.ops.wm.read_factory_settings(use_empty=True);palette(Path('build/graphics'))
 site=SITES[plan.seed]
 allrt=root('Signals_'+str(plan.seed),kind='SignalsIntersection')
 parts=[]
 if plan.span:parts.append(E.span('SpanWire',allrt,plan))
 else:
  for turn in site.approaches:
   pt=site.pole(turn)
   if site.diagonal and turn%2==1:
    pt=site.pole((turn-1)%4)
   # Head stations are measured from this pole, so dual arms serve their lanes.
   revised=replace(plan,arm=site.arm(turn),near=plan.near and not(site.diagonal and turn%2),left=plan.left if len(site.positions(turn))>2 or plan.left=='five' else 'permissive')
   mast=E.mast(f'Mast_{turn}',pt,turn*90,revised,allrt)
   if site.diagonal and turn%2==1:
    # Both arm roots share one real steel pole; remove the second support only.
    import bmesh
    fixed=next(o for o in mast.children if o.type=='MESH')
    bm=bmesh.new();bm.from_mesh(fixed.data);layer=bm.faces.layers.int['Construction']
    prefixes=('Round concrete','Base plate','Anchor','Leveling','Plate washer','Jam nut','Nut weather','Tapered shaft','Pole cap','Curved handhole','Handhole screw','Pole identification')
    bmesh.ops.delete(bm,geom=[f for f in bm.faces if COMPONENTS.get(f[layer],'').startswith(prefixes) or (fixed.matrix_local@f.calc_center_median()).z<1.2],context='FACES');bm.to_mesh(fixed.data);bm.free()
   parts.append(mast)
 # Separate pedestrian pole on each end of each crosswalk.
 for turn in site.approaches:
  for side in (-1,1):
   # Local -Y frontage rotated toward opposite curb.
   angle=turn*90+(-90 if side>0 else 90)
   pp=xy(side*(site.face(turn)+1.65),site.core(turn)+1.524+2.30,turn*90,GRADE)
   ped=E.pedestal(f'Pedestal_{turn}_{side}',pp,angle,allrt,walk=turn%2==0,with_head=not(plan.ped_mount=='mast' and side==1));parts.append(ped)
   # Accessible side landing connects to 5 ft walk while leaving main ramp clear.
   pad=root(f'APS_Landing_{turn}_{side}',xy(side*(site.face(turn)+1.65),site.core(turn)+1.524+1.52,turn*90,PAD_TOP-.080),allrt,kind='Landing',yaw=turn*90)
   box('Button clear landing',(0,0,0),(.9144,1.2192,.160),'concrete',pad,.004);join_fixed(pad)
   parts.append(pad)
   parts.append(E.pullbox(f'PullBox_{turn}_{side}',xy(side*(site.face(turn)+2.5),site.core(turn)+4.80,turn*90,.132588),allrt))
 cp=site.cabinet()
 parts.append(E.cabinet('Controller',cp,plan.cabinet*90,allrt))
 service=root('CabinetServiceSlab',cp,allrt,kind='ServiceSlab',yaw=plan.cabinet*90)
 box('Service standing pad',(0,-.75,-.026),(2.6,2.8,.052),'concrete',service,.010);join_fixed(service);parts.append(service)
 for o in bpy.context.scene.objects:
  if not o.get('signal_lens'):continue
  if o.name.startswith('Mast_') and o.get('signal_kind') not in ('hand','walk','countdown'):
   turn=int(o.name.split('_')[1]);mark=o.get('signal_kind');on=mark in (('red','red_arrow') if turn%2==0 else ('green','green_arrow'))
   if mark in ('red_arrow','green_arrow','yellow_arrow') and turn%2:
    kind=o.parent.get('part_kind','');on=(kind=='Head_protected' and mark=='red_arrow') or (kind=='Head_fya' and bool(o.get('flashing_yellow_arrow')))
   o.data.materials.clear();o.data.materials.append(M['lit' if on else 'off']);o['powered']=on
 for part in parts:
  if part.get('part_kind') in ('MastArm','Pedestal','PushButtonPost','Cabinet','SpanSet'):
   sock=root(part.name+'__GroundSocket',(0,0,0),part,kind='socket');sock['socket_kind']='ground_grade'
 from surfaces import lens_uv
 for ob in bpy.context.scene.objects:
  if ob.get('signal_lens'):lens_uv(ob)
 finalize_meshes();bpy.context.view_layer.update()
 for o in bpy.context.scene.objects:
  if o.type=='MESH':o.data.calc_loop_triangles()
 report=dict(plan=plan.data(),site=site.data(),checkpoint=True,parts=[dict(name=o.name,kind=o['part_kind'],triangles=tri(o),bounds=bounds(o)) for o in parts],lenses=[])
 for o in bpy.context.scene.objects:
  if o.get('signal_lens'):report['lenses'].append(dict(name=o.name,kind=o['signal_kind'],powered=bool(o.get('powered')),parent=o.parent.name))
 report['subparts']=[dict(name=o.name,kind=o['part_kind'],triangles=tri(o)) for o in bpy.context.scene.objects if o.type=='EMPTY' and (o.get('part_kind','').startswith('Head_') or o.get('part_kind') in ('PushButton','PedHead','CabinetDoor'))]
 report['equipment_triangles']=sum(len(o.data.loop_triangles) for o in bpy.context.scene.objects if o.type=='MESH')
 report['sha256_recipe']=hashlib.sha256(b''.join(p.read_bytes() for p in sorted(Path('src').glob('*.py')))).hexdigest()
 out.parent.mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()))
 glb=out.with_suffix('.glb');report['glb_bytes']=export(glb);report['glb_sha256']=hashlib.sha256(glb.read_bytes()).hexdigest()
 # Reusable roots are rebased, including pivot-local heads and APS submodules.
 if plan.seed==201:
  chosen=[parts[0],next(o for o in parts if o.get('part_kind')=='Pedestal'),bpy.data.objects['Controller'],bpy.data.objects['Mast_0__Head0'],bpy.data.objects['Mast_0__Head2'],bpy.data.objects['Pedestal_0_1__APS'],bpy.data.objects['Pedestal_0_1__Ped']]
  for ob in chosen:
   parent=ob.parent;matrix=ob.matrix_basis.copy();ob.parent=None;ob.matrix_world=Matrix.Identity(4);bpy.context.view_layer.update()
   export((out.parent/'parts')/(ob['part_kind']+'.glb'),[ob,*ob.children_recursive])
   ob.parent=parent;ob.matrix_basis=matrix
 if plan.seed==202:
  ob=next(o for o in parts if o.get('part_kind')=='PushButtonPost');parent=ob.parent;matrix=ob.matrix_basis.copy();ob.parent=None;ob.matrix_world=Matrix.Identity(4);bpy.context.view_layer.update()
  export((out.parent/'parts/PushButtonPost.glb'),[ob,*ob.children_recursive]);ob.parent=parent;ob.matrix_basis=matrix
 if plan.seed in (202,203):
  ob=bpy.data.objects.get('Mast_0__Head2') or bpy.data.objects['Mast_0__Head1'];parent=ob.parent;matrix=ob.matrix_basis.copy();ob.parent=None;ob.matrix_world=Matrix.Identity(4);bpy.context.view_layer.update()
  export((out.parent/'parts')/(ob['part_kind']+'.glb'),[ob,*ob.children_recursive]);ob.parent=parent;ob.matrix_basis=matrix
 if plan.seed==204:
  ob=parts[0];export((out.parent/'parts/SpanSet.glb'),[ob,*ob.children_recursive])
 out.with_name(out.stem+'-components.json').write_text(json.dumps(COMPONENTS,indent=2))
 out.with_suffix('.json').write_text(json.dumps(report,indent=2));print('BUILT',plan.seed,report['equipment_triangles'],'triangles',report['glb_bytes'],'bytes')
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('build/Signals-201.blend'));p.add_argument('--seeds',default='201,202,203,204');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 graphics.generate('build/graphics')
 for seed in map(int,a.seeds.split(',')):build(PLANS[seed],a.out.parent/f'Signals-{seed}.blend')
if __name__=='__main__':main()
