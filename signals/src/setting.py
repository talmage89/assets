"""Presentation from existing local library exports; never included in signal GLBs."""
import math,hashlib,json
from pathlib import Path
import bpy
from geometry import root,box,M
from kit.tiling import world_uv
from plan import *
ROOT=Path(__file__).resolve().parents[2]
def load(path):
 before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
 added=set(bpy.context.scene.objects)-before
 return {o.name:o for o in added if o.parent not in added},added
def clone(source,name,loc,yaw=0):
 obs=[source,*source.children_recursive];cop={}
 for o in obs:
  cp=o.copy();bpy.context.collection.objects.link(cp);cop[o]=cp
 for o,cp in cop.items():
  cp.parent=cop.get(o.parent);cp.matrix_basis=o.matrix_basis.copy();cp.name=name+'__'+o.name
 r=cop[source];r.location=loc;r.rotation_mode='XYZ';r.rotation_euler=(0,0,math.radians(yaw));return r
def ground(seed=201):
 from layout import SITES
 from ground.src.junction import build
 return build(SITES[seed].data(),ROOT)
def context(seed):
 from layout import SITES
 import random
 site=SITES[seed];rng=random.Random(seed);provenance=[];libraries={}
 def library(relative):
  if relative in libraries:return libraries[relative]
  path=ROOT/relative;lib,old=load(path);base=root('LibraryContext_'+path.stem)
  for ob in lib.values():ob.parent=base
  provenance.append(dict(source=relative,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
  libraries[relative]=(base,old|{base});return libraries[relative]
 houses=['houses/export/HearthfieldRanch-11.gltf','houses/export/HearthfieldCape-31.gltf','houses/export/HearthfieldSplit-51.gltf']
 for turn in site.approaches:
  angle=turn*90
  for side in (-1,1):
   for i in range(8):
    y=site.core(turn)+22+i*29+rng.uniform(-2,2);x=side*(site.face(turn)+15+rng.uniform(-1,2))
    pos=xy(x,y,angle,.15)
    # Reserve the complete commercial parcel plus house eaves/setback.
    if site.commercial and abs(pos[0]-(site.hx+31))<35 and abs(pos[1]-(site.hy+33))<35:continue
    rel=houses[(i+turn+side+seed)%3];base,_=library(rel)
    clone(base,f'House{turn}_{side}_{i}',pos,angle+(-90 if side>0 else 90))
   for i in range(11):
    y=site.core(turn)+30+i*22
    rel='trees/export/PinOak.glb' if (i+seed)%2 else 'trees/export/RedMaple.glb';base,_=library(rel)
    clone(base,f'StreetTree{turn}_{side}_{i}',xy(side*(site.face(turn)+7.3),y,angle,.15),rng.randrange(360))
   base,_=library('street-light/export/StreetLight.glb')
   for i in range(6):clone(base,f'StreetLamp{turn}_{side}_{i}',xy(side*(site.face(turn)+1.25),site.core(turn)+15+i*32,angle,.15),angle+(90 if side>0 else -90))
 if len(site.approaches)==3:
  base,_=library('houses/export/HearthfieldCape-31.gltf');clone(base,'ClosedT_House',(-site.hx-18,0,.15),90)
  base,_=library('trees/export/RedMaple.glb')
  for yy in (-18,18):clone(base,'ClosedT_Tree'+str(yy),(-site.hx-11,yy,.15),yy*7)
 if site.commercial:
  base,_=library('commercial/export/CommercialGas-101.gltf')
  # The station occupies the NE commercial parcel, behind both public walks.
  clone(base,'CornerGasStation',(site.hx+31,site.hy+33,.15),0)
 # Each delivered body appears at stop bars and in cross traffic. Local +X
 # is the northbound lane. No foreground vehicle in the driver's lane.
 cars=['cars/export/AlderC150.glb','cars/export/AlderX220.glb','cars/export/AlderH120.glb']
 for j,turn in enumerate(site.approaches):
  base,_=library(cars[j%3]);center=site.half(turn)-1.6764
  car=clone(base,f'WaitingVehicle{j}',xy(-center,site.stop(turn)+2.8,turn*90,.012),turn*90)
  # Alternate perpendicular lane is kept out of the driver's foreground.
  if turn==2:
   car.location=xy(-LANE/2,site.stop(turn)+3,turn*90,.012) if site.ns>=4 else xy(-LANE/2,site.stop(turn)+38,turn*90,.012)
  # Imported meshes carry the delivered paint-coverage decode. Vary only
  # the factory tint through that retained metadata, preserving dirt.
  for ob in car.children_recursive:
   if ob.type!='MESH':continue
   for idx,mat in enumerate(ob.data.materials):
    if not mat or mat.get('paint_decode')!='reference_plus_coverage_delta':continue
    ob.data=ob.data.copy();ma=mat.copy();ob.data.materials[idx]=ma
    tree=ma.node_tree;p=next(n for n in tree.nodes if n.type=='BSDF_PRINCIPLED');tex=next(n for n in tree.nodes if n.type=='TEX_IMAGE' and 'BaseColor' in n.image.name)
    target=[(.45,.46,.42),(.18,.025,.018),(.012,.046,.080),(.26,.26,.25)][j%4];ref=list(mat['paint_reference_color'])
    delta=tree.nodes.new('ShaderNodeVectorMath');delta.operation='SCALE';delta.inputs[0].default_value=tuple(a-b for a,b in zip(target,ref));tree.links.new(tex.outputs['Alpha'],delta.inputs['Scale'])
    add=tree.nodes.new('ShaderNodeVectorMath');add.operation='ADD';tree.links.new(tex.outputs['Color'],add.inputs[0]);tree.links.new(delta.outputs[0],add.inputs[1]);tree.links.new(add.outputs[0],p.inputs['Base Color'])
 base,_=library('cars/export/AlderH120.glb');clone(base,'CrossingVehicle',(0,-LANE/2,.012),90)
 for base,obs in libraries.values():
  for ob in obs:bpy.data.objects.remove(ob,do_unlink=True)
 return provenance

def audit_ground(seed=201):
 from layout import SITES
 from mathutils import Vector
 site=SITES[seed];bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();rows=[]
 for turn in site.approaches:
  for x in (-site.half(turn)-3,-site.half(turn)-1,0,site.half(turn)+1,site.half(turn)+3):
   p=xy(x,site.core(turn)+9,turn*90,50);ok,hit,n,idx,ob,_=bpy.context.scene.ray_cast(dg,Vector(p),Vector((0,0,-1)))
   assert ok,('Ground hole',turn,x);assert -.01<hit.z<.22,(ob.name,hit.z)
   rows.append(dict(turn=turn,x=x,mesh=ob.name,height_m=hit.z))
 Path(f'build/ground-placement-{seed}.json').write_text(json.dumps(dict(passed=True,samples=rows),indent=2));return rows
