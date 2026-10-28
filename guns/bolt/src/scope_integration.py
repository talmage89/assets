"""Presentation-only render target on the delivered ocular glass primitive.

No delivery geometry, UV, material slots, rig, or atlas is modified. The runtime
shader selects the ocular half of Glass by optical-axis position. It samples a
scene-linear objective-camera render and composites the original split-post
pattern as crisp shader lines. The original internal reticle remains geometry
in the GLB; the opaque render target occludes it in this integration.
"""
import math,json
from pathlib import Path
import bpy
from mathutils import Vector
MAGNIFICATION=8
OCULAR_RADIUS=.0188
EYE_TO_OCULAR=.0919
DISTANCE=100.0

def fov(m):return math.degrees(2*math.atan(OCULAR_RADIUS/(EYE_TO_OCULAR*m)))

def integrate(scene,shot):
 eye=scene.objects['Socket_Eye'].matrix_world.copy();objective=scene.objects['Socket_OpticObjective'].matrix_world.copy()
 dest=Path(scene.render.filepath).parent;dest.mkdir(parents=True,exist_ok=True)
 # prepare_shot supplies the destination before the primary render begins.
 out=dest/'aimed-range.exr';preview=dest/'aimed-range.png'
 secondary=bpy.data.scenes.new('Procedural 100m daylight range')
 secondary.render.engine='CYCLES';secondary.cycles.device='GPU';secondary.cycles.samples=32;secondary.cycles.use_denoising=True
 secondary.render.resolution_x=1024;secondary.render.resolution_y=1024;secondary.render.resolution_percentage=100
 secondary.view_settings.view_transform='AgX';secondary.view_settings.look='AgX - Medium High Contrast';secondary.view_settings.exposure=-.15
 secondary.render.image_settings.file_format='OPEN_EXR';secondary.render.image_settings.color_mode='RGBA';secondary.render.image_settings.color_depth='32';secondary.render.filepath=str(out)
 world=bpy.data.worlds.new('Procedural daylight');world.use_nodes=True;secondary.world=world
 nt=world.node_tree;sky=nt.nodes.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(35);sky.sun_rotation=math.radians(120)
 nt.links.new(sky.outputs[0],nt.nodes['Background'].inputs['Color']);nt.nodes['Background'].inputs['Strength'].default_value=.25
 def material(name,color):
  m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.85;return m
 def mesh(name,verts,faces,mat):
  data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update();data.materials.append(mat)
  ob=bpy.data.objects.new(name,data);secondary.collection.objects.link(ob);return ob
 origin=objective.translation;forward=(objective.to_3x3()@Vector((0,1,0))).normalized();up=(eye.to_3x3()@Vector((0,0,1))).normalized();right=forward.cross(up).normalized()
 ground_z=origin.z-1.6
 ground=material('Range ground',(.095,.115,.060))
 mesh('Ground',[(-250,-40,ground_z),(250,-40,ground_z),(250,350,ground_z),(-250,350,ground_z)],[(0,1,2,3)],ground)
 # Original 1.8 m human silhouette: flat target, not an imported model.
 outline=[(-.10,0),(-.23,0),(-.16,.77),(-.36,.53),(-.43,.61),(-.28,1.34),(-.12,1.43),(-.13,1.64),(-.08,1.78),(0,1.8),(.08,1.78),(.13,1.64),(.12,1.43),(.28,1.34),(.43,.61),(.36,.53),(.16,.77),(.23,0),(.10,0),(0,.70)]
 base=origin+forward*DISTANCE;base.z=ground_z
 mesh('1.8m silhouette at 100m',[tuple(base+right*x+up*z) for x,z in outline],[tuple(range(len(outline)))],material('Target charcoal',(.018,.018,.018)))
 # Pale backer and lane posts make the rendered magnification legible.
 card=material('Target backer',(.62,.59,.49));back=base+forward*.03
 mesh('Target backer',[tuple(back+right*x+up*z) for x,z in [(-.8,-.01),(.8,-.01),(.8,2.05),(-.8,2.05)]],[(0,1,2,3)],card)
 for distance in (25,50,75,100,125):
  for side in (-1,1):
   p=origin+forward*distance+right*(side*2.2);p.z=ground_z
   mesh('Distance stake',[tuple(p+right*x+up*z) for x,z in [(-.045,0),(.045,0),(.045,.75),(-.045,.75)]],[(0,1,2,3)],card)
 cd=bpy.data.cameras.new('Objective camera');cam=bpy.data.objects.new('Socket_OpticObjective camera',cd);secondary.collection.objects.link(cam)
 cam.location=origin;cam.rotation_euler=forward.to_track_quat('-Z','Y').to_euler();cd.type='PERSP';cd.sensor_fit='HORIZONTAL';cd.sensor_width=36;cd.lens=36/(2*math.tan(math.radians(fov(MAGNIFICATION))/2));cd.clip_start=.01;cd.clip_end=500;secondary.camera=cam
 # Nesting render operators inside render_pre is unsupported. Defer the main
 # render hook until this objective image has been generated in prepare_shot.
 bpy.ops.render.render(scene=secondary.name,write_still=True)
 secondary.render.image_settings.file_format='PNG';secondary.render.image_settings.color_depth='8';bpy.data.images['Render Result'].save_render(str(preview),scene=secondary)
 image=bpy.data.images.load(str(out),check_existing=True)
 meshes=[o for o in scene.objects if o.type=='MESH' and any(m and 'Glass' in m.name for m in o.data.materials)]
 assert len(meshes)==1,[(o.name,[m.name for m in o.data.materials]) for o in meshes]
 ob=meshes[0];slot=next(i for i,m in enumerate(ob.data.materials) if m and 'Glass' in m.name);old=ob.data.materials[slot]
 mat=old.copy();mat.name='Ocular render target demonstration';ob.data.materials[slot]=mat;nt=mat.node_tree;nodes=nt.nodes;links=nt.links
 def node(kind):return nodes.new(kind)
 def mathnode(op,a,b):
  n=node('ShaderNodeMath');n.operation=op
  for value,socket in ((a,n.inputs[0]),(b,n.inputs[1])):
   if isinstance(value,(float,int)):socket.default_value=value
   else:links.new(value,socket)
  return n.outputs[0]
 pos=node('ShaderNodeNewGeometry').outputs['Position'];offset=node('ShaderNodeVectorMath');offset.operation='SUBTRACT';links.new(pos,offset.inputs[0]);offset.inputs[1].default_value=eye.translation
 coords=[]
 for axis in ((1,0,0),(0,1,0),(0,0,1)):
  n=node('ShaderNodeVectorMath');n.operation='DOT_PRODUCT';links.new(offset.outputs[0],n.inputs[0]);n.inputs[1].default_value=eye.to_3x3()@Vector(axis);coords.append(n.outputs['Value'])
 x,y,z=coords;uv=node('ShaderNodeCombineXYZ')
 links.new(mathnode('ADD',mathnode('DIVIDE',x,.0376),.5),uv.inputs['X']);links.new(mathnode('ADD',mathnode('DIVIDE',z,.0376),.5),uv.inputs['Y'])
 tex=node('ShaderNodeTexImage');tex.image=image;tex.extension='EXTEND';tex.interpolation='Linear';links.new(uv.outputs[0],tex.inputs['Vector'])
 # Same original split-post pattern, composed on the ocular render target.
 ax=mathnode('ABSOLUTE',x,0);az=mathnode('ABSOLUTE',z,0)
 vertical=mathnode('LESS_THAN',ax,.00011)
 horizontal=mathnode('MULTIPLY',mathnode('LESS_THAN',az,.00011),mathnode('GREATER_THAN',ax,.0009))
 lines=mathnode('MAXIMUM',vertical,horizontal)
 for height in (-.008,-.004,.004,.008):
  stripe=mathnode('MULTIPLY',mathnode('LESS_THAN',mathnode('ABSOLUTE',mathnode('SUBTRACT',z,height),0),.00009),mathnode('LESS_THAN',ax,.0009));lines=mathnode('MAXIMUM',lines,stripe)
 color=node('ShaderNodeMixRGB');color.blend_type='MIX';links.new(lines,color.inputs[0]);links.new(tex.outputs['Color'],color.inputs[1]);color.inputs[2].default_value=(.00001,.00001,.00001,1)
 emission=node('ShaderNodeEmission');links.new(color.outputs[0],emission.inputs[0]);emission.inputs['Strength'].default_value=1
 output=next(n for n in nodes if n.type=='OUTPUT_MATERIAL');original=output.inputs['Surface'].links[0].from_socket
 mix=node('ShaderNodeMixShader');links.new(mathnode('LESS_THAN',y,.15),mix.inputs[0]);links.new(original,mix.inputs[1]);links.new(emission.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],output.inputs['Surface'])
 report=dict(magnification=MAGNIFICATION,objective_horizontal_fov_degrees=fov(MAGNIFICATION),horizontal_fov_by_magnification={str(m):fov(m) for m in range(4,17)},fov_definition='2 atan(ocular_radius / (eye_to_ocular_distance * magnification))',aperture_angular_diameter_degrees=fov(1),objective_camera_position_m=list(origin),eye_camera_position_m=list(eye.translation),target_distance_from_objective_m=DISTANCE,target_height_m=1.8,ocular_radius_m=OCULAR_RADIUS,ocular_center_distance_from_eye_m=EYE_TO_OCULAR,mesh=ob.name,material_slot=slot,delivered_material=old.name,ocular_selection='dot(world_position - Socket_Eye.position, Socket_Eye.forward) < 0.15 m',reticle='procedural texture/shader composite on ocular; original internal GLB geometry is occluded',render_target=str(out),preview=str(preview))
 (dest/'scope-integration.json').write_text(json.dumps(report,indent=2));shot['scope_integration']=report
 scene['scope_material_mesh']=ob.name;scene['scope_material_slot']=slot;scene['scope_original_material']=old.name

def restore(scene):
 if scene.get('scope_material_mesh'):
  scene.objects[scene['scope_material_mesh']].data.materials[scene['scope_material_slot']]=bpy.data.materials[scene['scope_original_material']]
  del scene['scope_material_mesh']
