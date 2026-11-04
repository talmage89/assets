"""X220 exterior fittings, entirely original and attached to actual surfaces."""
import math,bpy
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
from kit import model as G
from detail_helpers import box,tube,loop,print_quad,pivot
import suv_spec as S


def tree_for(objects):
 ps=[];fs=[]
 for ob in objects:
  offset=len(ps);ps.extend(ob.matrix_world@v.co for v in ob.data.vertices);ob.data.calc_loop_triangles()
  fs.extend(tuple(offset+i for i in t.vertices) for t in ob.data.loop_triangles)
 return BVHTree.FromPolygons(ps,fs,all_triangles=True)


def fuel_pocket(b,side):
 """Cut the real quarter skin; seat a formed filler cup behind the flap."""
 from mathutils.geometry import barycentric_transform
 from suv_apertures import cut_mesh
 ob=bpy.data.objects['Rear quarter_L'];old=ob.data;old.calc_loop_triangles()
 points=[ob.matrix_world@v.co for v in old.vertices]
 triangles=[tuple(t.vertices) for t in old.loop_triangles]
 normals=[ob.matrix_world.to_3x3().inverted().transposed()@old.corner_normals[i].vector for t in old.loop_triangles for i in t.loops]
 original=BVHTree.FromPolygons(points,triangles,all_triangles=True)
 role=old.attributes['skin_face_role'];outside=[tuple(f.vertices) for f in old.polygons if role.data[f.index].value==0]
 sheet=bpy.data.meshes.new('Quarter filler aperture sheet');sheet.from_pydata([v.co for v in old.vertices],[],outside);sheet.update();sheet.materials.append(b.m['body']);ob.data=sheet
 sheet.calc_loop_triangles();ts=[tuple(t.vertices) for t in sheet.loop_triangles]
 matrix=ob.matrix_world.to_3x3().inverted().transposed()
 surface=dict(tree=BVHTree.FromPolygons(points,ts,all_triangles=True),points=points,triangles=ts,uvs=[Vector((p.y,p.z,0)) for p in points],normals=[matrix@v.normal for v in sheet.vertices])
 y,z=1.56,1.04;outline=G.rounded_rectangle(.161,.161,.025,3 if b.high else 1)
 cutter=[Vector((y+u,z+v,0)) for u,v in outline]
 if sum(a.x*c.y-c.x*a.y for a,c in zip(cutter,cutter[1:]+cutter[:1]))<0:cutter.reverse()
 ob['skin_face_provenance']=False;cut_mesh(ob,[cutter],surface)
 me=ob.data;me.calc_loop_triangles();custom=[]
 for face in me.polygons:
  for li in face.loop_indices:
   p=ob.matrix_world@me.vertices[me.loops[li].vertex_index].co
   options=[hit for hit in original.find_nearest_range(p,.015) if hit[1].dot(matrix@face.normal)>.25]
   hit,_,fi,d=min(options,key=lambda h:h[3]) if options else original.find_nearest(p)
   a,c,e=triangles[fi];n=barycentric_transform(hit,points[a],points[c],points[e],*normals[fi*3:fi*3+3]).normalized()
   custom.append(n if n.dot(face.normal)>.25 else face.normal)
 me.normals_split_custom_set(custom)
 attr=me.attributes.get('skin_face_role') or me.attributes.new('skin_face_role','INT','FACE')
 for face in me.polygons:attr.data[face.index].value=face.material_index;face.material_index=0
 me.materials.clear();me.materials.append(b.m['body'])
 rows=[[side(-1,y+u,z+v,off) for u,v in outline] for off in [-.002,-.055]]
 count=len(outline);verts=rows[0]+rows[1]
 faces=[(i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count)]+[tuple(range(count,count*2))]
 cup=G.mesh('Fuel filler cup',verts,faces,b.m['plastic'])
 sol=cup.modifiers.new('Formed filler cup gauge','SOLIDIFY');sol.thickness=.0015;G.apply(cup)
 # Recalculate the closed manufacturing gauge after the side-chart winding.
 import bmesh
 bm=bmesh.new();bm.from_mesh(cup.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(cup.data);bm.free()
 b.add(cup,category='trim')
 parent=pivot(b,'FuelDoor',side(-1,y-.079,z,-.004),axis='Z',limits=(0,85))
 flap_outline=G.rounded_rectangle(.155,.155,.024,3 if b.high else 1)
 flap=b.add(G.loft('Fuel flap',[[side(-1,y+u,z+v,off) for u,v in flap_outline] for off in [.002,.004]],b.m['body']),parent,'trim')
 bpy.context.view_layer.update();ps=[flap.matrix_world@v.co for v in flap.data.vertices]
 front=min(p.y for p in ps);ends=[p for p in ps if p.y<front+1e-5]
 top=max(ends,key=lambda p:p.z);bottom=min(ends,key=lambda p:p.z)
 from suv_mechanics import rebase
 rebase(parent,(top+bottom)*.5+Vector((-.002,-.004,0)),(top-bottom).normalized())
 parent['hinge_basis']='Actual forward-edge chord, bearing 4 mm forward and 2 mm outboard of its middle'
 cap=G.lathe('Fuel filler cap',[(0,0),(0,.023),(.010,.023),(.010,0)],b.m['plastic'],8 if b.high else 6)
 cap.data.transform(Matrix.Translation(side(-1,y+.015,z-.01,-.044))@Vector((-1,0,0)).to_track_quat('Z','Y').to_matrix().to_4x4());b.add(cap,category='trim')


def build(b):
 skin=tree_for([ob for ob in bpy.context.scene.objects if ob.type=='MESH' and ob.get('part_category') in ['body','doors','pillars','fascia']])
 def side(s,y,z,off=0):
  p,n,_,_=skin.ray_cast(Vector((s*2,y,z)),Vector((-s,0,0)),3)
  if p is None:raise ValueError(('No side support',s,y,z))
  return p+n*off
 def end(x,z,front,off=0):
  p,n,_,_=skin.ray_cast(Vector((x,-3 if front else 3,z)),Vector((0,1 if front else -1,0)),3)
  if p is None:raise ValueError(('No end support',x,z))
  return p+n*off
 # Thin curved lens covers retain the accepted opening. Add optical jewelry
 # inside those real cassettes. DRLs follow their guide instead of a flat box.
 for front in [True,False]:
  for name in sorted(o.name for o in bpy.context.scene.objects if o.name.startswith('Headlamp opening' if front else 'Taillamp opening') and 'cassette' not in o.name):
   ob=bpy.data.objects[name];raw=list(ob['aperture_samples']);pts=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];nu=ob['form_columns'];nv=ob['form_rows'];parent=ob.parent
   middle=sum(pts,Vector())/len(pts);normal=Vector((middle.x*.8,-1 if front else 1,0)).normalized()
   path=[pts[(nv-1)*nu+i] for i in range(1,nu-1,2)]+[pts[j*nu+nu-2] for j in range(nv-2,-1,-1)]+[pts[i] for i in range(nu-3,0,-2)]
   # The generated outer lens is at -6 mm; emitters sit another 8 mm inboard.
   path=[p.lerp(middle,.08)-normal*.012 for p in path]
   tube(b,('Running guide ' if front else 'Rear guide ')+name,path,.005 if front else .006,b.m['drl' if front else 'brakelight'],'lamps',parent,sides=4)
   if front:
    for i,frac in enumerate([.24,.58]):
     center=pts[(nv//2)*nu+round(frac*(nu-1))]-normal*.020
     r=.030 if i==0 else .027
     reflect=G.lathe('Reflector '+name+str(i),[(-.016,r*.65),(0,r),( .005,r*.92),(.005,r*.79),(-.014,r*.50)],b.m['chrome'],20 if b.high else 16,axis='Z',closed=True)
     xf=Matrix.Translation(center)@normal.to_track_quat('Z','Y').to_matrix().to_4x4();reflect.data.transform(xf);b.add(reflect,parent,'lamps')
     lens=G.lathe('Projector '+name+str(i),[(0,0),(0,r*.78),(.005,r*.62),(.008,0)],b.m['lens'],20 if b.high else 16,axis='Z');lens.data.transform(xf);b.add(lens,parent,'lamps')
     emitter=G.lathe('LED source '+name+str(i),[(-.004,0),(-.004,r*.45),(-.001,r*.45),(-.001,0)],b.m['headlight'],12,axis='Z');emitter.data.transform(xf);b.add(emitter,parent,'lamps')
    p=pts[nu-3].lerp(pts[(nv-1)*nu+nu-3],.5)-normal*.010
    box(b,'Amber side optic '+name,p,(.018,.025,.038),b.m['amber'],'lamps',parent,.003)
 # More numerous thin recessed grille ribs and a central original medallion.
 for name in ['Upper grille opening','Lower intake opening']:
  blank=bpy.data.objects[name];nu=blank['form_columns'];raw=list(blank['aperture_samples']);pts=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
  for ob in list(bpy.context.scene.objects):
   if ob.name.startswith(name+' blade'):bpy.data.objects.remove(ob,do_unlink=True)
  for j in range(1,6):
   t=j/6*4;lo=int(t);f=t-lo;row=[pts[lo*nu+i].lerp(pts[min(lo+1,4)*nu+i],f) for i in range(1,nu-1,2)]
   rows=[[p+Vector((0,dy,dz)) for dy,dz in [(-.008,-.003),(.004,-.003),(.004,.003),(-.008,.003)]] for p in row]
   b.add(G.loft(name+' recessed rib '+str(j),rows,b.m['dark_chrome']),category='trim')
  for i in range(2,nu-1,2):
   p=pts[i];q=pts[4*nu+i];tube(b,name+' back web '+str(i),[p+Vector((0,.005,0)),q+Vector((0,.005,0))],.003,b.m['plastic'],'trim',sides=4)
 # Badge lands are deliberately fictional, without a real emblem silhouette.
 p=end(0,1.13,False,.012)
 print_quad(b,'Rear ALDER badge',[(p.x+.034,p.y+.002,p.z-.012),(p.x-.034,p.y+.002,p.z-.012),(p.x-.034,p.y+.002,p.z+.012),(p.x+.034,p.y+.002,p.z+.012)],b.m['badge'],'trim',bpy.data.objects['Liftgate'])
 box(b,'Front badge land',(0,-2.26,.83),(.11,.016,.034),b.m['dark_chrome'],'trim',radius=.01)
 print_quad(b,'Front ALDER badge',[(-.048,-2.269,.819),(.048,-2.269,.819),(.048,-2.269,.841),(-.048,-2.269,.841)],b.m['badge'])
 for s,side_name in [(-1,'L'),(1,'R')]:
  for end_name,y in [('F',-.05),('R',1.025)]:
   parent=bpy.data.objects['Door_'+end_name+side_name];z=1.09+.022*y;p=side(s,y,z,.006)
   outline=G.rounded_rectangle(.17,.044,.012,3 if b.high else 1)
   rings=[[side(s,y+u,z+v,off) for u,v in outline] for off in [.0005,.0035]]
   b.add(G.loft('Handle escutcheon '+end_name+side_name,rings,b.m['gloss_black']),parent,'trim')
   path=[side(s,y+d,z,off) for d,off in [(-.073,.009),(-.053,.024),(.05,.025),(.073,.010)]]
   tube(b,'Pull handle '+end_name+side_name,path,.009,b.m['body'],'trim',parent,sides=6)
  # Belt brightwork and a molded black edge on each window, attached to its pane.
  for window in ['Front','Rear','Quarter']:
   ob=bpy.data.objects[window+' side glazing_'+side_name];raw=list(ob['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];nu=ob['form_columns'];nv=ob['form_rows']
   # Guide metadata predates the six-mm seating inset; re-seat the border too.
   ps=[p-Vector((s*.005,0,0)) for p in ps];middle=sum(ps,Vector())/len(ps)
   from suv_apertures import boundary_indices
   indices=boundary_indices(nu,nv);border=[ps[i] for i in indices[::2]]
   rings=[[p+(p-middle).normalized()*d+Vector((s*.004,0,0)) for p in border] for d in [0,.007]]
   trim=G.loft('Window seal '+window+side_name,rings,b.m['gloss_black'],caps=False);sol=trim.modifiers.new('Molded seal gauge','SOLIDIFY');sol.thickness=.003;b.add(trim,ob.parent,'trim')
   tube(b,'Window belt '+window+side_name,[ps[i]+Vector((s*.007,0,-.005)) for i in range(0,nu,3)],.003,b.m['dark_chrome'],'trim',ob.parent,sides=4)
  # Rail tips already have molded feet: accent the closing cap joint.
  for i,y in enumerate([.055,1.50]):box(b,'Rail end cap '+side_name+str(i),(s*.620,y,1.66),(.025,.027,.012),b.m['plastic'],'trim',radius=.004)
  # Push fasteners live on the concealed liner flange, not the painted face.
  # Their drive relief is a high-source/bake detail at this size.
 fuel_pocket(b,side)
 # Actual plate size; blank fictional brand only, no plausible registration.
 blank=bpy.data.objects['Plate pocket opening'];raw=list(blank['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];c=sum(ps,Vector())/len(ps)
 normal=Vector(blank['bed_plane_normal']);right=Vector((1,0,0));up=right.cross(normal).normalized();c+=normal*.004
 backing=G.box('Rear plate',(0,0,0),(.305,.002,.1524),b.m['plate'],.001 if b.high else 0,1)
 backing.matrix_world=Matrix(((right.x,normal.x,up.x,c.x),(right.y,normal.y,up.y,c.y),(right.z,normal.z,up.z,c.z),(0,0,0,1)))
 b.add(backing,bpy.data.objects['Liftgate'],'trim')
 print_quad(b,'Rear plate face',[c+normal*.0012+right*x+up*z for x,z in [(.15,-.074),(-.15,-.074),(-.15,.074),(.15,.074)]],b.m['plate'],'trim',bpy.data.objects['Liftgate'])
 p=end(.45,.82,False,.003);right=Vector((1,0,0));up=Vector((0,0,1))
 print_quad(b,'X220 AWD model badge',[p+right*x+up*z for x,z in [(.055,-.014),(-.055,-.014),(-.055,.014),(.055,.014)]],b.m['model'],'trim',bpy.data.objects['Liftgate'])
 # Wipers are parked against their actual glass surfaces, with substantial arms.
 wind=tree_for([bpy.data.objects['Windshield']]);rear=tree_for([bpy.data.objects['Backlight']]);hood=tree_for([bpy.data.objects['Hood outer']])
 for i,(a,c) in enumerate([(-.64,-.12),(.04,.55)]):
  points=[]
  for j in range(5):
   x=a+(c-a)*j/4;p,n,_,_=wind.ray_cast(Vector((x,-1.03,2)),Vector((0,0,-1)),2)
   if p is None:p,n,_,_=wind.find_nearest(Vector((x,-.98,1.16)))
   points.append(p+n*.009)
  base=points[-1]+Vector((.03,.045,.006));tube(b,'Front wiper blade '+str(i),points,.004,b.m['rubber'],'trim',sides=4)
  tube(b,'Front wiper arm '+str(i),[base,points[2]+Vector((0,0,.014))],.005,b.m['frame'],'trim',sides=4)
  p,n,_,_=hood.ray_cast(Vector((a,-1.10,2)),Vector((0,0,-1)),2)
  box(b,'Washer nozzle '+str(i),p+n*.004,(.015,.023,.009),b.m['plastic'],'trim',radius=.003)
 pts=[]
 for x in [-.35,-.18,0,.18]:
  p,n,_,_=rear.find_nearest(Vector((x,2.14,1.31)));pts.append(p+n*.012)
 tube(b,'Rear wiper blade',pts,.004,b.m['rubber'],'trim',bpy.data.objects['Liftgate'],sides=4)
 tube(b,'Rear wiper arm',[(.22,2.16,1.29),pts[2]+Vector((0,.009,.01))],.006,b.m['plastic'],'trim',bpy.data.objects['Liftgate'],sides=4)
 # Low shark fin, lofted with a compound rounded nose.
 rows=[]
 for z,sc,y in [(1.663,1,1.22),(1.69,.75,1.23),(1.735,.15,1.275)]:rows.append([(u*sc,y+v*sc,z) for u,v in G.rounded_rectangle(.065,.15,.022,3)])
 b.add(G.smooth(G.loft('Shark fin antenna',rows,b.m['body'])),category='trim')
