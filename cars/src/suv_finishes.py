"""Family paint method with X220 rest-space wear and the shared four surfaces.

All textures in this source scene are original marking generators. A later
4096 bake/2048 neutral atlas uses the family's coverage-factor decode.
"""
from pathlib import Path
import bpy
from kit import vehicle_materials as V
from kit.materials import Nodes
import suv_spec as S
from pickup_spec import COLORS as FAMILY_COLORS,PAINT_METAL
COLORS=dict(FAMILY_COLORS,Graphite=(.150,.1540545,.160))

# Authored scene-spawn proportions, not a measured sales statistic.
FLEET_WEIGHTS={'Porcelain':.30,'Carbon':.25,'Graphite':.22,'Aluminum':.16,'Atlantic':.07}


def palette(wear=.65):
 root=Path(__file__).resolve().parents[1]/'build/suv-detail/markings'
 images={k:bpy.data.images.load(str(root/(k+'.png')),check_existing=True) for k in ['badge','model','plate','display','cluster','tire_relief']}
 images['tire_relief'].colorspace_settings.name='Non-Color'
 axles=(S.FRONT_AXLE,S.REAR_AXLE)
 m={'body':V.paint('X220 factory paint',COLORS['Graphite'],wear,axles,front=-S.LENGTH/2,rear=S.LENGTH/2,refined=True,flakes=.55,metallic=PAINT_METAL['Graphite'])}
 for key,col,kind in [('rubber',(.008,.009,.010),'rubber'),('plastic',(.014,.016,.017),'plastic'),('bumper',(.014,.016,.017),'plastic'),('wheel',(.43,.46,.48),'alloy'),('chrome',(.56,.60,.62),'chrome'),('dark_chrome',(.12,.145,.16),'chrome'),('frame',(.009,.011,.012),'plastic'),('caliper',(.12,.13,.13),'steel'),('cloth',(.045,.049,.052),'fabric'),('seat_side',(.020,.024,.026),'plastic'),('interior',(.018,.021,.023),'plastic'),('headliner',(.18,.18,.17),'fabric'),('interior_light',(.085,.093,.098),'plastic')]:
  m[key]=V.manufactured('X220 '+key,col,kind,wear,axles,refined=True,brake_centers=[(sgn*track/2,y,S.HUB_HEIGHT) for sgn in [-1,1] for track,y in [(S.FRONT_TRACK,S.FRONT_AXLE),(S.REAR_TRACK,S.REAR_AXLE)]] if key=='wheel' else ())
 m['brake']=V.brake_rotor('X220 turned rotor')
 m['gloss_black']=V.manufactured('X220 gloss black',(.005,.007,.008),'plastic',wear*.3,(),refined=True)
 bs=m['gloss_black'].node_tree.nodes['SURFACE'];bs.inputs['Coat Weight'].default_value=.8
 # Named output and actual roughness agree; retain all bake channels.
 nt=m['gloss_black'].node_tree
 for socket in [bs.inputs['Roughness'],nt.nodes['OUT_rough'].inputs[0]]:
  for link in list(socket.links):nt.links.remove(link)
  socket.default_value=.15
 m['glass']=V.glazing('X220 windshield',(.32,.40,.41))
 m['side_glass']=V.glazing('X220 front side glass',(.42,.50,.51),axes=(1,2))
 m['privacy']=V.glazing('X220 privacy glass',(.18,.23,.24),True,axes=(1,2))
 m['rear_glass']=V.glazing('X220 backlight',(.21,.26,.27),True)
 m['lens']=V.glazing('X220 clear optical cover',(.97,.98,.99));m['lens'].node_tree.nodes['SURFACE'].inputs['IOR'].default_value=1.49
 n=Nodes('X220 prismatic red reflector');p,x,y,z,nx,ny,nz=V.rest(n,'VehicleRest')
 h=n.mul(n.math('SINE',n.mul(z,3141.59265)),.00006)
 m['reflector_red']=n.finish((.30,.006,.003),.19,.48,h,coat=.8)
 m['red_lens']=V.glazing('X220 red optic',(.52,.025,.018))
 m['drl']=V.lamp('X220 running guide',(.84,.92,1),80)
 m['headlight']=V.lamp('X220 projector emitter',(1,.92,.80),45)
 # The unlit projector sees its dark LED substrate through the lens. Its
 # emission color remains warm white when the lamp control is switched on.
 from suv_weather import graph,replace
 replace(graph(m['headlight']),'base',(.018,.023,.029),'Base Color')
 m['brakelight']=V.lamp('X220 brake guide',(.60,.006,.003),9)
 m['amber']=V.lamp('X220 amber marker',(.62,.12,.003),3)
 m['mirror']=V.manufactured('X220 mirror',(.73,.76,.77),'chrome',0)
 for side,sgn in [('L',-1),('R',1)]:
  mat=V.tire('X220 touring tire '+side,images['tire_relief'],sgn,wear=wear)
  nt=mat.node_tree;tc=next(n for n in nt.nodes if n.type=='TEX_COORD');links=list(tc.outputs['Object'].links)
  scale=nt.nodes.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(.275/S.TIRE_WIDTH,.40135/S.HUB_HEIGHT,.40135/S.HUB_HEIGHT)
  nt.links.new(tc.outputs['Object'],scale.inputs[0])
  for link in links:nt.links.new(scale.outputs[0],link.to_socket)
  m['tire_'+side]=mat
 for key in ['badge','model','plate','display','cluster']:
  n=Nodes('X220 original '+key);tex=n.node('ShaderNodeTexImage');tex.image=images[key]
  mat=n.finish(tex.outputs['Color'],.32 if key=='plate' else .25,0 if key in ['plate','display','cluster'] else .8)
  if key in ['display','cluster']:
   bs=mat.node_tree.nodes['SURFACE'];n.feed(bs.inputs['Emission Color'],tex.outputs['Color']);bs.inputs['Emission Strength'].default_value=.22
  m[key]=mat
 # SUV cladding: upward fading, aft-wheel sediment and loading-sill scuffs.
 n=Nodes('X220 weathered molded cladding');p,x,y,z,nx,ny,nz=V.rest(n,'VehicleRest')
 film=V.daily_road_mask(n,p,y,z,axles,wear*1.8)
 # Wheel wakes load the flanks; the lower rear-facing center is protected by
 # the bumper return. Do not continue the side fan as a pale rear dust blanket.
 shield=n.mul(n.ramp(y,2.02,2.20),n.ramp(ny,.30,.85))
 film=n.mul(film,n.mix(shield,1,.25))
 fade=n.mul(n.ramp(nz,.15,.95),wear,.35)
 base=n.mix(fade,(.012,.014,.015),(.060,.064,.065),True)
 base=n.mix(film,base,(.065,.055,.041),True)
 boot=n.mul(n.ramp(n.math('ABSOLUTE',x),.65,.82),n.ramp(z,.58,.34),n.ramp(y,-.95,-.65),n.ramp(y,1.30,1.1))
 load=n.mul(n.ramp(y,2.03,2.19),n.ramp(z,.45,.55),n.ramp(z,.76,.65),n.ramp(nz,0,.6))
 scuff=n.mul(n.maximum(boot,load),n.ramp(n.noise(n.vec('MULTIPLY',p,(70,8,100)),5,2),.62,.77),wear)
 base=n.mix(scuff,base,(.082,.086,.086),True)
 h=n.add(n.mul(n.math('SUBTRACT',n.noise(p,3500,2),.5),26e-6),n.mul(scuff,-.00008))
 m['cladding']=n.finish(base,n.add(.53,n.mul(film,.18)),0,h)
 from suv_weather import paint,glass,alloy
 paint(m['body'],wear)
 alloy(m['wheel'],wear)
 for key in ['glass','side_glass','privacy','rear_glass']:glass(m[key],wear)
 return m


def assign(b):
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH':continue
  name=ob.name;cat=ob.get('part_category');key='body'
  if cat in ['liners','closure']:key='rubber'
  elif cat=='cladding':key='wheel' if 'skid' in name else 'cladding'
  elif cat=='glass':key='side_glass' if 'Front side' in name else 'privacy' if 'side glazing' in name else 'rear_glass' if 'Backlight' in name else 'glass'
  elif cat=='openings':
   key='reflector_red' if name.startswith('Reflector') and 'return' not in name else 'reflector_red' if name.startswith('Taillamp') and 'optical cassette' in name else 'lens' if name.startswith('Headlamp opening') and 'cassette' not in name else 'red_lens' if name.startswith('Taillamp opening') and 'cassette' not in name else 'dark_chrome' if any(q in name for q in ['surround','garnish','blade']) else 'plastic'
  elif cat=='mirrors':key='mirror' if 'pane' in name else 'plastic' if 'sail' in name else 'body'
  elif cat=='rails':key='dark_chrome' if 'Roof rail' in name else 'plastic'
  elif cat=='pillars' and ('applique' in name or 'divider' in name):key='gloss_black'
  elif cat=='tires':key='tire_L' if name.endswith('L') else 'tire_R'
  elif cat=='wheels':key='wheel'
  elif name=='Spoiler brake lamp':key='brakelight'
  ob.data.materials.clear();ob.data.materials.append(b.m[key])
  for f in ob.data.polygons:f.material_index=0
  if name.startswith('Taillamp') and 'cassette' in name:
   ob.data.materials.append(b.m['chrome']);ps=[ob.matrix_world@v.co for v in ob.data.vertices];low=min(p.z for p in ps);high=max(p.z for p in ps)
   for face in ob.data.polygons:
    p=ob.matrix_world@face.center
    if .39<abs(p.x)<.60 and p.z<low+.50*(high-low):face.material_index=1
  if name.startswith('Taillamp') and 'cassette' not in name:
   ob.data.materials.append(b.m['lens']);ps=[ob.matrix_world@v.co for v in ob.data.vertices];low=min(p.z for p in ps);high=max(p.z for p in ps)
   for face in ob.data.polygons:
    p=ob.matrix_world@face.center
    if .43<abs(p.x)<.60 and p.z<low+.50*(high-low):face.material_index=1
 bpy.context.view_layer.update()
 for ob in bpy.context.scene.objects:
  if ob.type=='MESH':
   attr=ob.data.attributes.get('VehicleRest') or ob.data.attributes.new('VehicleRest','FLOAT_VECTOR','POINT')
   attr.data.foreach_set('vector',[q for v in ob.data.vertices for q in ob.matrix_world@v.co])
