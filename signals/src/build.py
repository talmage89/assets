"""Build four original form-checkpoint equipment libraries, and reusable parts."""
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

def export(path,objects=None):
 bpy.ops.object.select_all(action='DESELECT')
 if objects is None:objects=list(bpy.context.scene.objects)
 for o in objects:o.select_set(True)
 path.parent.mkdir(parents=True,exist_ok=True)
 bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLB',use_selection=True,export_extras=True,export_apply=True,export_yup=True,export_cameras=False,export_lights=False)
 return path.stat().st_size
def bounds(rt):
 pts=[o.matrix_world@v.co for o in rt.children_recursive if o.type=='MESH' for v in o.data.vertices]
 return [[min(p[i] for p in pts) for i in range(3)],[max(p[i] for p in pts) for i in range(3)]] if pts else None
def build(plan,out):
 bpy.ops.wm.read_factory_settings(use_empty=True);palette(Path('build/graphics'))
 allrt=root('Signals_'+str(plan.seed),kind='SignalsIntersection')
 parts=[]
 if plan.span:parts.append(E.span('SpanWire',allrt,plan))
 else:
  for turn in range(4):parts.append(E.mast(f'Mast_{turn}',xy(POLE_X,POLE_Y,turn*90,GRADE),turn*90,plan,allrt))
 # Separate pedestrian pole on each end of each crosswalk.
 for turn in range(4):
  for side in (-1,1):
   # Local -Y frontage rotated toward opposite curb.
   angle=turn*90+(-90 if side>0 else 90)
   pp=xy(side*(FACE+1.65),CROSS+2.30,turn*90,GRADE)
   ped=E.pedestal(f'Pedestal_{turn}_{side}',pp,angle,allrt,walk=turn%2==0,with_head=not(plan.ped_mount=='mast' and side==1));parts.append(ped)
   # Accessible side landing connects to 5 ft walk while leaving main ramp clear.
   pad=root(f'APS_Landing_{turn}_{side}',xy(side*(FACE+1.65),CROSS+1.52,turn*90,PAD_TOP-.080),allrt,kind='Landing',yaw=turn*90)
   box('Button clear landing',(0,0,0),(.9144,1.2192,.160),'concrete',pad,.004);join_fixed(pad)
   parts.append(pad)
   parts.append(E.pullbox(f'PullBox_{turn}_{side}',xy(side*(FACE+2.5),CORE+4.80,turn*90,.132588),allrt))
 cp=xy(10.5,15.8,plan.cabinet*90,.171)
 parts.append(E.cabinet('Controller',cp,plan.cabinet*90,allrt))
 service=root('CabinetServiceSlab',cp,allrt,kind='ServiceSlab',yaw=plan.cabinet*90)
 box('Service standing pad',(0,-.75,-.026),(2.6,2.8,.052),'concrete',service,.010);join_fixed(service);parts.append(service)
 for o in bpy.context.scene.objects:
  if not o.get('signal_lens'):continue
  if o.name.startswith('Mast_') and o.get('signal_kind') not in ('hand','walk','countdown'):
   turn=int(o.name.split('_')[1]);mark=o.get('signal_kind');on=mark in (('red','red_arrow') if turn%2==0 else ('green','green_arrow'))
   if mark=='yellow_arrow':on=False
   o.data.materials.clear();o.data.materials.append(M['lit' if on else 'off']);o['powered']=on
 for part in parts:
  if part.get('part_kind') in ('MastArm','Pedestal','PushButtonPost','Cabinet','SpanSet'):
   sock=root(part.name+'__GroundSocket',(0,0,0),part,kind='socket');sock['socket_kind']='ground_grade'
 finalize_meshes();bpy.context.view_layer.update()
 for o in bpy.context.scene.objects:
  if o.type=='MESH':o.data.calc_loop_triangles()
 report=dict(plan=plan.data(),checkpoint=True,parts=[dict(name=o.name,kind=o['part_kind'],triangles=tri(o),bounds=bounds(o)) for o in parts],lenses=[])
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
   export(Path('build/parts')/(ob['part_kind']+'.glb'),[ob,*ob.children_recursive])
   ob.parent=parent;ob.matrix_basis=matrix
 if plan.seed==202:
  ob=next(o for o in parts if o.get('part_kind')=='PushButtonPost');parent=ob.parent;matrix=ob.matrix_basis.copy();ob.parent=None;ob.matrix_world=Matrix.Identity(4);bpy.context.view_layer.update()
  export(Path('build/parts/PushButtonPost.glb'),[ob,*ob.children_recursive]);ob.parent=parent;ob.matrix_basis=matrix
 if plan.seed in (202,203):
  ob=bpy.data.objects['Mast_0__Head2'];parent=ob.parent;matrix=ob.matrix_basis.copy();ob.parent=None;ob.matrix_world=Matrix.Identity(4);bpy.context.view_layer.update()
  export(Path('build/parts')/(ob['part_kind']+'.glb'),[ob,*ob.children_recursive]);ob.parent=parent;ob.matrix_basis=matrix
 if plan.seed==204:
  ob=parts[0];export(Path('build/parts/SpanSet.glb'),[ob,*ob.children_recursive])
 out.with_name(out.stem+'-components.json').write_text(json.dumps(COMPONENTS,indent=2))
 out.with_suffix('.json').write_text(json.dumps(report,indent=2));print('BUILT',plan.seed,report['equipment_triangles'],'triangles',report['glb_bytes'],'bytes')
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('build/Signals-201.blend'));p.add_argument('--seeds',default='201,202,203,204');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 graphics.generate('build/graphics')
 for seed in map(int,a.seeds.split(',')):build(PLANS[seed],a.out.parent/f'Signals-{seed}.blend')
if __name__=='__main__':main()
