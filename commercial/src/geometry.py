"""Family construction vocabulary. Parts are authored, never image-derived.

Reusable commercial components live in this family until another family needs
these semantics. Low-level mesh, loft, tube and transform operations use kit.
"""
import math
import bpy
from mathutils import Vector, Matrix
from kit import model as G
from kit.fonts import find_font

M={}


def material(name,color,rough=.65,metal=0,transmission=0,emission=0):
 m=bpy.data.materials.get(name)
 if m:return m
 m=bpy.data.materials.new(name);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
 p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 p.inputs['Transmission Weight'].default_value=transmission
 p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=emission
 return m


def palette(brand,wall_color):
 global M
 M.clear();M.update({k:material('Form_'+k,col,r,met,tr,em) for k,col,r,met,tr,em in (
 ('Concrete',(.34,.35,.35),.90,0,0,0),('Asphalt',(.055,.059,.063),.94,0,0,0),
 ('Wall',wall_color,.85,0,0,0),('Roof',(.12,.13,.135),.94,0,0,0),
 ('Metal',(.30,.32,.33),.34,.82,0,0),('Trim',(.035,.043,.047),.32,.55,0,0),
 ('White',(.67,.67,.64),.58,0,0,0),('Black',(.009,.012,.014),.64,0,0,0),
 ('Rubber',(.012,.014,.015),.8,0,0,0),('Glass',(.78,.84,.86),.025,0,1,0),
 ('Inside',(.027,.030,.032),.9,0,0,0),('Primary',brand['primary'],.42,.10,0,0),
 ('Accent',brand['accent'],.43,.05,0,0),('Logo',brand['accent'],.45,0,0,.35),('Light',brand['light'],.48,0,0,.25),
 ('LED',(.88,.40,.075),.45,0,0,1.5),('Lamp',(.65,.72,.75),.4,0,0,.5),
 ('Yellow',(.70,.44,.025),.64,0,0,0),('Red',(.52,.018,.015),.65,0,0,0),
 ('Blue',(.015,.095,.42),.65,0,0,0),('Orange',(.76,.17,.015),.65,0,0,0),
 ('Green',(.10,.17,.065),.92,0,0,0),('Soil',(.065,.048,.031),.96,0,0,0))})
 return M


def root(name,loc=(0,0,0),yaw=0,kind=None,parent=None):
 o=G.pivot(name,loc);o.rotation_euler.z=math.radians(yaw)
 o['module_kind']=kind or name;o['static_root']=True
 if parent:o.parent=parent
 return o


def own(ob,parent,solid=True):
 ob.parent=parent;ob['asset_set']=parent.get('module_kind','Commercial')
 ob['module_root']=parent.name
 if solid:ob['solid']=True
 return ob


def box(name,p,size,mat,parent,r=.002,seg=1):
 return own(G.box(name,p,size,M.get(mat,mat),r,seg),parent)


def mesh(name,verts,faces,mat,parent,solid=True):return own(G.mesh(name,verts,faces,M.get(mat,mat)),parent,solid)


def tube(name,pts,r,mat,parent,sides=10):return own(G.smooth(G.tube(name,pts,r,M.get(mat,mat),sides=sides)),parent)


def cylinder(name,a,b,r,mat,parent,n=16):return own(G.smooth(G.cylinder(name,a,b,r,M.get(mat,mat),n)),parent)


def panel(name,x,y,z,w,h,mat,parent,thick=.012):return box(name,(x,y,z),(w,thick,h),mat,parent,.004)


def frame(name,x,y,z,w,h,mat,parent,bar=.045,depth=.10):
 for side in (-1,1):box(name+' jamb',(x+side*(w-bar)/2,y,z),(bar,depth,h),mat,parent,.002)
 for side in (-1,1):box(name+' rail',(x,y,z+side*(h-bar)/2),(w-2*bar,depth,bar),mat,parent,.002)


def rounded_slab(name,p,w,d,h,r,mat,parent):
 points=G.rounded_rectangle(w,d,r,5)
 loops=[[(x+p[0],y+p[1],p[2]+z) for x,y in points] for z in (0,h)]
 return own(G.loft(name,loops,M[mat]),parent)


def beam(name,a,b,w,d,mat,parent):
 a,b=Vector(a),Vector(b);o=box(name,(a+b)/2,(w,d,(b-a).length),mat,parent,.002)
 o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o


def mark(name,p,height,brand,parent):
 x,y,z=p;h=height
 if brand['mark']=='three_piers':
  for i,fac in enumerate((.68,1,.81)):
   box(name+' pier',(x+(i-1)*h*.29,y,z-h*.5+h*fac*.5),(h*.15,.026,h*fac),'Logo',parent,.002)
 else:
  for side in (-1,1):
   xx=x+side*h*.25;zz=z+side*h*.14
   box(name+' bracket stem',(xx,y,zz),(h*.12,.026,h*.75),'Logo',parent,.002)
   for s in (-1,1):box(name+' bracket cap',(xx-side*h*.075,y,zz+s*h*.315),(h*.27,.026,h*.12),'Logo',parent,.002)


def brand_sign(name,p,w,h,brand,parent):
 x,y,z=p;panel(name+' backing',x,y,z,w,h,'Primary',parent,.055)
 mark(name+' mark',(x-w*.38,y-.04,z),h*.65,brand,parent)
 text(name+' name',brand['name'],(x+w*.065,y-.030,z),min(h*.43,w/(len(brand['name'])*.80)), 'Light',parent)


def hinge(name,p,parent,limits=(0,100)):
 o=root(name,p,parent=parent);o['static_root']=False;o['pivot_axis']='Z';o['range_degrees']=limits
 return o


def socket(name,p,parent,kind='attachment',yaw=0):
 o=root(name,p,yaw,parent=parent);o['socket_kind']=kind;del o['static_root'];return o


def finalize():
 # Keep source construction, but apply physical bevels, convert temporary text,
 # triangulate, and join static geometry per module/moving pivot for runtime use.
 import bmesh
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
 copies=[]
 for ob in list(bpy.context.scene.objects):
  if ob.type!='MESH':continue
  data=bpy.data.meshes.new_from_object(ob.evaluated_get(dg),depsgraph=dg,preserve_all_data_layers=True)
  if data.uv_layers:data.uv_layers[0].name='UVMap'
  bm=bmesh.new();bm.from_mesh(data)
  bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
  bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-8)
  bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='FIXED',ngon_method='EAR_CLIP')
  bm.to_mesh(data);bm.free()
  copies.append((ob,data))
 for ob,data in copies:
  ob.data=data;ob.modifiers.clear()
  if not ob.data.uv_layers:
   uv=ob.data.uv_layers.new(name='UVMap')
   for poly in ob.data.polygons:
    axes=sorted(range(3),key=lambda k:abs(poly.normal[k]))[:2]
    for li in poly.loop_indices:
     v=ob.data.vertices[ob.data.loops[li].vertex_index].co
     uv.data[li].uv=(v[axes[0]],v[axes[1]])
 # Rebase fixed construction to each reusable module; only physical leaves and
 # detachable nozzles retain their own meshes. Helper coordinate frames survive
 # where a pivot/socket still uses them, without extra static draw objects.
 bpy.context.view_layer.update()
 for ob in [o for o in bpy.context.scene.objects if o.type=='MESH']:
  owner=ob.parent
  while owner and not (owner.get('reusable_module') or owner.get('pivot_axis') or owner.get('detachable')):owner=owner.parent
  if owner and ob.parent!=owner:
   xf=owner.matrix_world.inverted()@ob.matrix_world;ob.data.transform(xf)
   ob.parent=owner;ob.matrix_parent_inverse=Matrix.Identity(4);ob.matrix_basis=Matrix.Identity(4)
 # Static joins retain the module pivot and moving leaves remain separate.
 parents={o.parent for o in bpy.context.scene.objects if o.type=='MESH'}
 for parent in sorted(parents,key=lambda p:p.name if p else ''):
  obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent==parent]
  if not obs:continue
  bpy.ops.object.select_all(action='DESELECT')
  for o in obs:o.select_set(True)
  bpy.context.view_layer.objects.active=obs[0]
  if len(obs)>1:bpy.ops.object.join()
  o=bpy.context.object;o.name=parent.name+'__Mesh' if parent else 'CommercialMesh'
  # Consolidated surface vertices remain in each owning module's local frame.
  xf=o.matrix_basis.copy();o.data.transform(xf);o.matrix_basis=Matrix.Identity(4)
 return [o for o in bpy.context.scene.objects if o.type=='MESH']


def led_digits(name,string,p,height,parent):
 """Original seven-segment price display, flush luminous bars; no font asset."""
 glyphs={'0':'abcedf','1':'bc','2':'abged','3':'abgcd','4':'fgbc','5':'afgcd','6':'afgecd','7':'abc','8':'abcdefg','9':'abfgcd'}
 x,y,z=p;w=height*.46;gap=height*.12;total=sum(w*.33 if c=='.' else w+gap for c in string)-gap
 cursor=x-total/2
 bars={'a':(w/2,height/2,w*.74,height*.085),'g':(w/2,0,w*.74,height*.085),'d':(w/2,-height/2,w*.74,height*.085),
       'f':(w*.075,height*.25,w*.085,height*.39),'b':(w*.925,height*.25,w*.085,height*.39),
       'e':(w*.075,-height*.25,w*.085,height*.39),'c':(w*.925,-height*.25,w*.085,height*.39)}
 for char in string:
  if char=='.':
   mesh(name+' decimal',[(cursor,y,z-height*.51),(cursor+w*.12,y,z-height*.51),(cursor+w*.12,y,z-height*.41),(cursor,y,z-height*.41)],[(0,1,2,3)],'LED',parent,False);cursor+=w*.33;continue
  for bar in glyphs[char]:
   xx,zz,bw,bh=bars[bar];mesh(name+' segment',[(cursor+xx-bw/2,y,z+zz-bh/2),(cursor+xx+bw/2,y,z+zz-bh/2),(cursor+xx+bw/2,y,z+zz+bh/2),(cursor+xx-bw/2,y,z+zz+bh/2)],[(0,1,2,3)],'LED',parent,False)
  cursor+=w+gap


def wheelchair_sign(parent,x,y,z,size):
 # Official ISA topology, analytically drawn. Unlike a decorative blank blue panel,
 # the symbol remains readable independently of its text.
 rr=size*.30
 pts=[(x+rr*math.cos(math.radians(25+i*310/18)),y,z-size*.13+rr*math.sin(math.radians(25+i*310/18))) for i in range(19)]
 tube('ISA wheel',pts,size*.025,'White',parent,6)
 tube('ISA body',[(x-size*.04,y,z+size*.29),(x-size*.04,y,z-size*.02),(x+size*.28,y,z-size*.02),(x+size*.37,y,z-size*.30)],size*.028,'White',parent,6)
 cylinder('ISA head',(x-size*.04,y+.002,z+size*.42),(x-size*.04,y-.002,z+size*.42),size*.068,'White',parent,12)

# Form-only raster type. Every glyph comes from installed open fonts and our
# strings. A shared sheet replaces thousands of tiny contour triangles. This
# is a diagnostic sheet, not the future manufactured/weathered delivery atlas.
PRINTS={};PRINT_OBS=[];PRINT_CANVAS=None;PRINT_CURSOR=[4,4,0]


def text(name,string,p,size,mat,parent,align='CENTER',yaw=0):
 from PIL import Image,ImageDraw,ImageFont
 global PRINT_CANVAS
 if PRINT_CANVAS is None:PRINT_CANVAS=Image.new('RGBA',(2048,2048),(255,255,255,0))
 key=(string,mat)
 if key not in PRINTS:
  font=ImageFont.truetype(str(find_font('DejaVu Sans','Bold' if size>.16 else 'Book')),48)
  bb=ImageDraw.Draw(PRINT_CANVAS).multiline_textbbox((0,0),string,font=font,align='center',spacing=3)
  iw,ih=bb[2]-bb[0]+8,bb[3]-bb[1]+8
  x,y,row=PRINT_CURSOR
  if x+iw+4>2048:x=4;y+=row+4;row=0
  if y+ih+4>2048:raise RuntimeError('Form lettering sheet is full')
  col=M[mat].node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value[:3]
  def srgb(v):return 12.92*v if v<=.0031308 else 1.055*v**(1/2.4)-.055
  color=tuple(round(srgb(c)*255) for c in col)+(255,)
  ImageDraw.Draw(PRINT_CANVAS).multiline_text((x+4-bb[0],y+4-bb[1]),string,font=font,fill=color,spacing=3,align='center')
  PRINTS[key]=(x,y,iw,ih);PRINT_CURSOR[:]=[x+iw+4,y,max(row,ih)]
 x,y,iw,ih=PRINTS[key];w=iw/48*size;h=ih/48*size
 px,py,pz=p
 if align=='LEFT':px+=w/2
 verts=[(px-w/2,py,pz-h/2),(px+w/2,py,pz-h/2),(px+w/2,py,pz+h/2),(px-w/2,py,pz+h/2)]
 ob=own(G.plane_uv(name,verts,M['White']),parent,False)
 ob.rotation_euler.z=math.radians(yaw);ob['graphic']=True
 uv=ob.data.uv_layers.active;uv.name='UVMap'
 coords=[(x/2048,1-(y+ih)/2048),((x+iw)/2048,1-(y+ih)/2048),((x+iw)/2048,1-y/2048),(x/2048,1-y/2048)]
 for poly in ob.data.polygons:
  for li in poly.loop_indices:uv.data[li].uv=coords[ob.data.loops[li].vertex_index]
 ob['graphic_emission']=M[mat].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value
 PRINT_OBS.append(ob);return ob


def finish_prints(path):
 global PRINT_CANVAS
 if PRINT_CANVAS is None:return
 PRINT_CANVAS.save(path)
 im=bpy.data.images.load(str(path.resolve()),check_existing=True)
 ma=bpy.data.materials.new('FormLettering');ma.use_nodes=True
 ns,ls=ma.node_tree.nodes,ma.node_tree.links;pp=ns.get('Principled BSDF');node=ns.new('ShaderNodeTexImage');node.image=im
 ls.new(node.outputs['Color'],pp.inputs['Base Color']);ls.new(node.outputs['Alpha'],pp.inputs['Alpha'])
 pp.inputs['Roughness'].default_value=.56
 ma.surface_render_method='DITHERED';ma.use_transparency_overlap=False
 emit=ma.copy();emit.name='FormLetteringIlluminated'
 ep=emit.node_tree.nodes.get('Principled BSDF');en=next(n for n in emit.node_tree.nodes if n.type=='TEX_IMAGE')
 emit.node_tree.links.new(en.outputs['Color'],ep.inputs['Emission Color']);ep.inputs['Emission Strength'].default_value=.35
 for ob in PRINT_OBS:
  ob.data.materials.clear();ob.data.materials.append(emit if ob.get('graphic_emission',0)>.1 else ma)


def reset_prints():
 global PRINT_CANVAS
 PRINTS.clear();PRINT_OBS.clear();PRINT_CANVAS=None;PRINT_CURSOR[:]=[4,4,0]
