"""Rigid pivots and telescoping supports, evaluated from actual attachment frames."""
import math,bpy,bmesh
from mathutils import Vector,Matrix
from kit import model as G
from detail_helpers import box,tube


def rebase(pivot,position,axis=None):
 children={o:o.matrix_world.copy() for o in pivot.children};pivot.location=position
 if axis is not None:pivot.rotation_euler=axis.to_track_quat('Z','Y').to_euler()
 bpy.context.view_layer.update()
 for o,m in children.items():o.matrix_world=m


def split_roof(b):
 """Hidden roof/gate header joint under the molded spoiler's front seat."""
 ob=bpy.data.objects['Roof'];mesh=ob.data;role=mesh.attributes.get('skin_face_role')
 ps=[ob.matrix_world@v.co for v in mesh.vertices];fs=[tuple(f.vertices) for f in mesh.polygons if role.data[f.index].value==0]
 from suv_body import skin_gauge
 for aft in [False,True]:
  me=bpy.data.meshes.new('Roof hinge seam');me.from_pydata(ps,[],fs);me.update();bm=bmesh.new();bm.from_mesh(me)
  bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),plane_co=(0,1.62+(.00225 if aft else -.00225),0),plane_no=(0,1,0),clear_inner=aft,clear_outer=not aft,dist=1e-7)
  bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
  new=bpy.data.objects.new('Gate upper header' if aft else 'Roof fixed',me);bpy.context.collection.objects.link(new);me.materials.append(b.m['body']);skin_gauge(new,.0009);b.add(new,bpy.data.objects['Liftgate'] if aft else b.root,'body')
  a=new.data.attributes.get('skin_face_role') or new.data.attributes.new('skin_face_role','INT','FACE')
  for f in new.data.polygons:a.data[f.index].value=f.material_index;f.material_index=0
  new.data.materials.clear();new.data.materials.append(b.m['body'])
 bpy.data.objects.remove(ob,do_unlink=True)


def support(b,name,fixed,moving,pivot,barrel,rod):
 bpy.context.view_layer.update();local=pivot.matrix_world.inverted()@Vector(moving)
 for kind,length,profile,mat in [('barrel',barrel,[(0,.006),(0,.010),(barrel,.010),(barrel,.006)],b.m['frame']),('rod',rod,[(0,0),(0,.0045),(rod,.0045),(rod,0)],b.m['chrome'])]:
  ob=G.lathe(name+' '+kind,profile,mat,8 if not b.high else 12,axis='Z',closed=kind=='barrel');b.add(ob,category='mechanisms')
  ob['support_fixed']=list(fixed);ob['support_moving_local']=list(local);ob['support_pivot']=pivot.name;ob['support_kind']=kind;ob['support_length_m']=length
  ob['allow_boundary']=False
 for label,pos in [('body',fixed),('gate',moving)]:box(b,name+' '+label+' ball seat',pos,(.025,.020,.025),b.m['frame'],'mechanisms',pivot if label=='gate' else b.root,.006)


def update_supports():
 bpy.context.view_layer.update()
 for ob in bpy.context.scene.objects:
  if 'support_pivot' not in ob:continue
  pivot=bpy.data.objects[ob['support_pivot']];a=Vector(ob['support_fixed']);c=pivot.matrix_world@Vector(ob['support_moving_local']);d=c-a
  if ob['support_kind']=='rod':a=c;d=-d
  ob.matrix_world=Matrix.Translation(a)@d.to_track_quat('Z','Y').to_matrix().to_4x4()
 bpy.context.view_layer.update()


def build(b):
 for side,s in [('L',-1),('R',1)]:
  for end,y in [('F',-1.035),('R',.150)]:
   pivot=bpy.data.objects['Door_'+end+side];axis=Vector((s*.10,0,1)).normalized();hinge_x=.84 if end=='F' else .82;rebase(pivot,(s*hinge_x,y,.78),axis)
   pivot['hinge_axis_vehicle']=list(axis)
   pivot['range_degrees']=[0,60] if s<0 else [-60,0]
   for z in ([.73,1.04] if end=='F' else [.63,1.01]):
    prefix='Door hinge '+end+side+str(z)
    center=Vector((s*hinge_x+axis.x/axis.z*(z-.78),y,z))
    xf=Matrix.Translation(center)@axis.to_track_quat('Z','Y').to_matrix().to_4x4()
    pin=G.lathe(prefix+' pin',[(-.027,0),(-.027,.006),(.022,.006),(.022,0)],b.m['frame'],12 if b.high else 6)
    pin.data.transform(xf);b.add(pin,category='mechanisms')
    sleeve=G.lathe(prefix+' sleeve',[(-.016,.007),(-.016,.011),(.016,.011),(.016,.007)],b.m['frame'],12 if b.high else 6,closed=True)
    sleeve.data.transform(xf);b.add(sleeve,pivot,'mechanisms')
    bracket=[(center.x,y-.0015),(center.x-s*.055,y-.0015),(center.x-s*.055,y+.0015)]
    b.add(G.profile(prefix+' fixed bracket',bracket,z-.030,z-.018,b.m['frame'],axis='Z'),category='mechanisms')
    seam=-.960 if end=='F' else .180
    arm=[(center.x-s*.004,y+.007),(s*.715,y+.007),(s*.715,seam+.085),(s*.815,seam+.085),(s*.815,seam+.075),(s*.725,seam+.075),(s*.725,y+.017),(center.x-s*.004,y+.017)]
    b.add(G.profile(prefix+' door leaf',arm,z-.005,z+.005,b.m['frame'],axis='Z'),pivot,'mechanisms')
 hood=bpy.data.objects['Hood'];rebase(hood,(0,-1.07,1.12));hood['range_degrees']=[-65,0]
 gate=bpy.data.objects['Liftgate'];rebase(gate,(0,1.62,1.67));gate['range_degrees']=[0,75]
 split_roof(b)
 # The plate bed and return must follow the gate, including its dark recess.
 for name in ['Plate pocket opening','Plate pocket opening molded return']:
  ob=bpy.data.objects[name];world=ob.matrix_world.copy();ob.parent=gate;ob.matrix_world=world
 for s in [-1,1]:
  for name,y,z,parent in [('Hood',-1.13,1.08,hood),('Liftgate',1.66,1.61,gate)]:
   plate=box(b,name+' hinge '+str(s),(s*.48,y,z),(.06,.045,.025),b.m['frame'],'mechanisms',parent,0)
   if name=='Hood':
    from suv_exterior import tree_for
    tree=tree_for([bpy.data.objects['Hood outer']]);bpy.context.view_layer.update();inverse=plate.matrix_world.inverted()
    for vertex in plate.data.vertices:
     point=plate.matrix_world@vertex.co
     if point.z<=z:continue
     hit=tree.ray_cast(Vector((point.x,point.y,.6)),Vector((0,0,1)),1)[0]
     if hit is None:raise ValueError('Hood hinge plate misses its inner skin')
     point.z=hit.z+.0005;vertex.co=inverse@point
    plate.data.update()
  support(b,'Hood strut '+str(s),(s*.59,-1.18,.85),(s*.59,-1.65,1.04),hood,.46,.44)
  from suv_exterior import tree_for
  fender=bpy.data.objects['Front fender_'+('L' if s<0 else 'R')];tree=tree_for([fender])
  hit=tree.ray_cast(Vector((s*2,-1.18,.85)),Vector((-s,0,0)),2)[0]
  if hit is None:raise ValueError('Hood strut return misses the fender')
  x=hit.x+s*.0005
  outline=[(s*.58,-1.19),(x,-1.19),(x,-1.13)]
  b.add(G.profile('Hood strut body return '+str(s),outline,.847,.853,b.m['frame'],axis='Z',radius=.0015 if b.high else 0,segments=2),category='mechanisms')
  support(b,'Gate strut '+str(s),(s*.68,1.55,1.19),(s*.68,1.98,1.49),gate,.50,.44)
  box(b,'Gate strut body return '+str(s),(s*.775,1.55,1.19),(.21,.025,.025),b.m['frame'],'mechanisms',radius=0)
 update_supports()
