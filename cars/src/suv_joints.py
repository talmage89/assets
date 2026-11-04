"""Separate manufactured skins at real closure joints without changing the form."""
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
from kit import model as G


def split_y(b,name,sections,axis='Y'):
 ob=bpy.data.objects[name];old=ob.data;old.calc_loop_triangles()
 ps=[ob.matrix_world@v.co for v in old.vertices];triangles=[tuple(t.vertices) for t in old.loop_triangles]
 tree=BVHTree.FromPolygons(ps,triangles,all_triangles=True)
 ns=[tuple(old.corner_normals[li].vector) for t in old.loop_triangles for li in t.loops]
 normal_matrix=ob.matrix_world.to_3x3().inverted().transposed()
 ns=[normal_matrix@Vector(n) for n in ns]
 for label,low,high,parent in sections:
  me=old.copy();me.transform(ob.matrix_world);bm=bmesh.new();bm.from_mesh(me)
  for value,lower in [(low,True),(high,False)]:
   if value is None:continue
   co=Vector();normal=Vector();co['XYZ'.index(axis)]=value;normal['XYZ'.index(axis)]=1
   bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),plane_co=co,plane_no=normal,clear_inner=lower,clear_outer=not lower,dist=1e-7)
  if not bm.faces:bm.free();bpy.data.meshes.remove(me);continue
  # A plane can graze two neighboring dense-chart edges within a few microns.
  # Weld those coincident cut points before capping; otherwise the cap fan
  # contains zero-area slivers despite having a closed boundary.
  bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=5e-6)
  bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=5e-6)
  borders=[e for e in bm.edges if e.is_boundary];caps=bmesh.ops.holes_fill(bm,edges=borders,sides=0)['faces']
  role_layer=bm.faces.layers.int.get('skin_face_role')
  if role_layer is not None:
   for face in caps:face[role_layer]=2
  bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-6)
  bmesh.ops.triangulate(bm,faces=list(bm.faces))
  bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-6)
  bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
  new=bpy.data.objects.new(name+' '+label,me);bpy.context.collection.objects.link(new)
  # Reuse the original corner normal field on retained exterior faces. Newly
  # capped joint ends remain flat and are never smoothed across the reveal.
  custom=[]
  for f in me.polygons:
   for li in f.loop_indices:
    p=me.vertices[me.loops[li].vertex_index].co;hit,_,fi,d=tree.find_nearest(p)
    a,c,e=triangles[fi];n=barycentric_transform(hit,ps[a],ps[c],ps[e],*ns[fi*3:fi*3+3]).normalized()
    custom.append(n if abs(f.normal.dot(n))>.5 and d<.002 else f.normal)
  me.normals_split_custom_set(custom)
  for key in ob.keys():new[key]=ob[key]
  new['joint_split']='Measured original shell clipped at closure plane; new capped ends'
  new['retain_gauge_for_joints']=True
  b.add(new,parent,ob['part_category'])
 bpy.data.objects.remove(ob,do_unlink=True)


def build(b):
 for side in ['L','R']:
  front=bpy.data.objects['Door_F'+side];rear=bpy.data.objects['Door_R'+side]
  gate=bpy.data.objects['Liftgate']
  split_y(b,'Greenhouse_'+side,[('A return',None,-.96225,b.root),('front sash',-.95775,.17775,front),('rear sash',.18225,1.04775,rear),('quarter',1.05225,1.61775,b.root),('gate header',1.62225,None,gate)])
  split_y(b,'Window surround_'+side,[('A return',None,-.96225,b.root),('front sash',-.95775,.17775,front),('rear sash',.18225,1.04775,rear),('quarter',1.05225,None,b.root)])
  split_y(b,'B applique_'+side,[('front door',None,.17775,front),('rear door',.18225,None,rear)])
  split_y(b,'C divider_'+side,[('door',None,1.04775,rear),('quarter',1.05225,None,b.root)])
  split_y(b,'Greenhouse_'+side+' gate header',[('fixed base',None,1.32775,b.root),('moving top',1.33225,None,gate)],axis='Z')
  # The rear door is cut around its wheel; its molded arch segment follows it.
  # A short trailing piece of the front arch similarly belongs to the front door.
  for kind in ['Arch cladding_','Arch flange_']:
   split_y(b,kind+'F'+side,[('fender',None,-.96525,b.root),('door',-.95775,None,front)])
   split_y(b,kind+'R'+side,[('door',None,1.25775,rear),('quarter',1.26225,None,b.root)])
  # The dropped spoiler ends seat over a moving gate header. The joint
  # preserves exterior positions and divides the formerly overlapping solids.
  name='Rear quarter_'+side
  split_y(b,name,[('lower',None,1.31775,b.root),('upper',1.32225,None,b.root)],axis='Z')
  split_y(b,name+' upper',[('forward',None,1.61775,b.root),('aft',1.62225,None,b.root)])
  limits=[('gate return',-.77775,None,gate),('fixed side',None,-.78225,b.root)] if side=='L' else [('gate return',None,.77775,gate),('fixed side',.78225,None,b.root)]
  split_y(b,name+' upper aft',limits,axis='X')
  for ob in bpy.context.scene.objects:
   if ob.name.startswith('Cladding clip ') and side in ob.name.split()[-1]:
    p=sum((ob.matrix_world@v.co for v in ob.data.vertices),Vector())/len(ob.data.vertices)
    parent=front if -.96<p.y<.18 else rear if .18<p.y<1.26 else b.root
    world=ob.matrix_world.copy();ob.parent=parent;ob.matrix_world=world
