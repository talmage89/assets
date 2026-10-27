"""Two ranches and a colonial, with immutable own-family landscape exports.

All house and context geometry is imported for presentation only. No export,
join, or edit of their mesh/texture data occurs here.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from render import setup
from street import imported
from delivery_io import bundle_hash
from kit.tiling import world_uv


def move(objects,location,yaw=0):
 for ob in objects:
  if ob.parent not in objects:
   ob.location+=Vector(location);ob.rotation_mode='XYZ';ob.rotation_euler.z+=math.radians(yaw)


def main(a):
 bpy.ops.wm.read_factory_settings(use_empty=True);houses=[];house_groups=[]
 for file,location in [('HearthfieldRanch-12.gltf',(0,6,0)),('Hearthfield-27.gltf',(24,8,0)),('HearthfieldRanch-15.gltf',(48,5,0))]:
  source=Path('export')/file;objects=imported(source);move(objects,location)
  houses.append(dict(source=str(source),bundle_sha256=bundle_hash(source),location=location));house_groups.append(objects)
 context=json.loads(Path('build/ranch/delivery/context.json').read_text())
 for row in context:assert hashlib.sha256(Path(row['source']).read_bytes()).hexdigest()==row['sha256']
 ground=imported(Path(context[0]['source']));library={o.name:o for o in ground if o.parent is None};placed=[]
 def place(kind,name,loc,yaw=0,scale=(1,1,1)):
  root=library[kind];copies={}
  for ob in [root]+list(root.children_recursive):
   cp=ob.copy();bpy.context.collection.objects.link(cp);copies[ob]=cp
  for ob,cp in copies.items():cp.parent=copies.get(ob.parent);cp.matrix_basis=ob.matrix_basis.copy();cp.name=name+'__'+ob.name
  rt=copies[root];rt.location=loc;rt.rotation_mode='XYZ';rt.rotation_euler=(0,0,math.radians(yaw));rt.scale=scale;placed.extend(copies.values());return rt
 # Native ground cross-section: flow line at -10 m, road crown farther
 # south, curb, planting strip and sidewalk on the house side.
 grade=-.16764;curb_y=-10.;walk_y=curb_y+.1524+1.8288
 for i in range(-8,26):place('Road_Straight_A',f'Road_{i}',(i*6.096,curb_y-.4572-3.6576,grade),90)
 for i in range(-16,52):place('Curb_Straight',f'Curb_{i}',(i*3.048,curb_y,grade),90)
 walks=[]
 for i in range(-32,104):
  rt=place('Sidewalk_A',f'Sidewalk_{i}',(i*1.524,walk_y,grade),90);walks.extend([rt,*rt.children_recursive])
 def lawn_rect(x0,x1,y0,y1,label):
  nx=math.ceil((x1-x0)/6.096);ny=math.ceil((y1-y0)/6.096);dx=(x1-x0)/nx;dy=(y1-y0)/ny
  for ix in range(nx):
   for iy in range(ny):
    sx=dx/6.096;angle=math.atan(.004/sx);base=.16264
    rt=place('Lawn_Field',f'{label}_{ix}_{iy}',(x0+ix*dx-math.sin(angle)*base,y0+(iy+.5)*dy,-math.cos(angle)*base),scale=(sx,dy/6.096,1));rt.rotation_euler.y=angle
 lawn_rect(-40,150,curb_y+.1524,walk_y,'PlantingStrip')
 lawn_rect(-40,150,walk_y+1.524,24,'Lawns')
 south_curb=curb_y-2*(.4572+3.6576);south_walk=south_curb-.1524-1.8288
 for i in range(-16,52):place('Curb_Straight',f'SouthCurb_{i}',(i*3.048,south_curb,grade),-90)
 for i in range(-32,104):
  rt=place('Sidewalk_A',f'SouthWalk_{i}',(i*1.524,south_walk,grade),-90);walks.extend([rt,*rt.children_recursive])
 lawn_rect(-40,150,south_walk,south_curb-.1524,'SouthStrip')
 lawn_rect(-40,150,-45,south_walk-1.524,'SouthLawns')
 # Delivered pours under the colonial pickup; instances only.
 meta=json.loads(Path('export/Hearthfield-27.json').read_text());apron=meta['sockets']['GarageApron'];end=apron[1]+8
 count=4;pitch=(end-curb_y)/count
 for i in range(count):
  y=curb_y+i*pitch;z=apron[2]-.16764-.004*(end-y)+.005
  place('Driveway_Slab',f'Drive_{i}',(apron[0]+24,y,z),90,(pitch/3.048,2,1))
 for ob in ground:bpy.data.objects.remove(ob,do_unlink=True)
 # Foundation shrubs retain the two delivered species at native scale.
 for x,y,choice in [(-6,1.,'box'),(-4.8,1.,'box'),(-2.5,1.,'hyd'),(5,1.,'box'),(6.2,1.,'box'),(42,1.,'hyd'),(44,1.,'box'),(51,1.,'box'),(53,1.,'hyd'),(19,1.5,'box'),(20.3,1.5,'hyd')]:
  shrubs=imported(Path(context[3]['source']))
  # Family roots carry original species names; unused species are removed.
  roots=[o for o in shrubs if o.parent not in shrubs]
  for rt in roots:
   descendants={rt,*rt.children_recursive};keep=('boxwood' in rt.name.lower()) if choice=='box' else ('hydrangea' in rt.name.lower())
   if not keep:
    for o in descendants:bpy.data.objects.remove(o,do_unlink=True)
   else:move(descendants,(x,y,0))
 tree=imported(Path(context[1]['source']));move(tree,(42,1,0))
 tree2=imported(Path(context[4]['source']));move(tree2,(12,11,0),25)
 pickup=imported(Path(context[2]['source']));move(pickup,(30,-1,.075),180)
 camera=setup('CYCLES',a.samples);bpy.data.objects.remove(bpy.data.objects['Presentation grade, excluded from asset'],do_unlink=True)
 lawn=next(m for o in placed if o.type=='MESH' for m in o.data.materials if m.name=='Lawn')
 bpy.ops.mesh.primitive_plane_add(size=2000,location=(0,0,-.25));far=bpy.context.object;far.name='Distant presentation lawn';far.data.materials.append(lawn);world_uv(far,3.048)
 tint=far.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
 for c in tint.data:c.color=(.95,.95,.95,1)
 # This view is context presentation; no socket-contact claim is made.
 camera.location=(-30,-21,1.68);target=Vector((18,6,3.2));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.lens=24
 sc=bpy.context.scene;sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/1.8);sc.render.resolution_percentage=100
 from check_mesh import surface
 walk=surface([o for o in walks if o.type=='MESH']);hit=walk.ray_cast(Vector((camera.location.x,camera.location.y,2)),Vector((0,0,-1)),3)[0];assert hit is not None
 camera.location.z=hit.z+1.68
 camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
 from bpy_extras.object_utils import world_to_camera_view
 bpy.context.view_layer.update()
 for row,objects in zip(houses,house_groups):
  projections=[world_to_camera_view(sc,camera,o.matrix_world@v.co) for o in objects if o.type=='MESH' for v in o.data.vertices]
  row['projected_frame_width']=max(p.x for p in projections)-min(p.x for p in projections)
 bpy.data.objects['Afternoon sun'].rotation_euler=Vector((.35,.9,-.65)).to_track_quat('-Z','Y').to_euler()
 out=Path('renders/ranch/street');out.mkdir(parents=True,exist_ok=True);sc.render.filepath=str((out/'street.png').resolve());bpy.ops.render.render(write_still=True)
 for row in houses:assert bundle_hash(Path(row['source']))==row['bundle_sha256']
 for row in context:assert hashlib.sha256(Path(row['source']).read_bytes()).hexdigest()==row['sha256']
 (out/'provenance.json').write_text(json.dumps(dict(houses=houses,context=context,camera_height_m=camera.location.z,eye_height_above_sidewalk_m=camera.location.z-hit.z,sidewalk_surface_z_m=hit.z,engine='CYCLES',render_only=True),indent=2))


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=1800);p.add_argument('--samples',type=int,default=48);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);main(a)
