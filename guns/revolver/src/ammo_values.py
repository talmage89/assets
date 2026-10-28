"""Original exterior ammunition: photo values beside actual projected GLB patches."""
import json,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import weapon_verify as V
from kit.fonts import find_font
from final_shots import SHOTS
V.import_glb(BASE/'export/cartridge.glb');ob=next(o for o in bpy.context.scene.objects if o.type=='MESH')
ob.data.calc_loop_triangles();tree=BVHTree.FromPolygons([ob.matrix_world@v.co for v in ob.data.vertices],[t.vertices[:] for t in ob.data.loop_triangles],all_triangles=True)
photo=Image.open(BASE/'build/references/softpoint.png').convert('RGB');font=ImageFont.truetype(find_font('Noto Sans','Regular'),19)
rows={};panels=[]
def stats(im,poly):
 mask=Image.new('L',im.size,0);ImageDraw.Draw(mask).polygon(poly,fill=255)
 rgb=np.asarray(im)[np.asarray(mask)>0].astype(float);m=np.median(rgb,axis=0)
 return dict(pixels=len(rgb),rgb_median=m.tolist(),rgb_ratio_G1=(m/max(1,m[1])).tolist(),luma_median=float(np.median(rgb@np.array([.2126,.7152,.0722]))))
for name,y,dy,dz,rect in [('brass',.016,.0018,.0007,(57,110,91,248)),('copper',.035,.0007,.0006,(61,54,105,73)),('lead',.0396,.00025,.00025,(66,25,104,40)),('primer',0,.00025,.00025,(354,78,366,89))]:
 shot=SHOTS['cartridge_head' if name=='primer' else 'cartridge'];im=Image.open(BASE/'renders/final/ammo/cartridge'/('cartridge_head.png' if name=='primer' else 'cartridge.png')).convert('RGB')
 data=bpy.data.cameras.new('Ammo value '+name);cam=bpy.data.objects.new(data.name,data);bpy.context.scene.collection.objects.link(cam)
 cam.location=shot['location'];cam.rotation_euler=(Vector(shot['target'])-cam.location).to_track_quat('-Z','Y').to_euler();data.sensor_fit='HORIZONTAL';data.sensor_width=36;data.lens=shot['lens']
 sc=bpy.context.scene;sc.camera=cam;sc.render.resolution_x=im.width;sc.render.resolution_y=im.height;sc.render.resolution_percentage=100;bpy.context.view_layer.update()
 points=[];poly=[]
 for a,b in [(-1,-1),(1,-1),(1,1),(-1,1)]:
  origin=(.0007+a*dy,-.01,b*dz) if name=='primer' else (.030,y+a*dy,b*dz)
  direction=(0,1,0) if name=='primer' else (-1,0,0)
  hit=tree.ray_cast(Vector(origin),Vector(direction),.06);assert hit[0] is not None,name
  points.append(list(hit[0]));uv=world_to_camera_view(sc,cam,hit[0]);poly.append((uv.x*im.width,(1-uv.y)*im.height))
 x0,y0,x1,y1=rect;pp=[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
 rows[name]=dict(photo_native_patch=rect,actual_surface_points_m=points,render_polygon=poly,photo=stats(photo,pp),render=stats(im,poly))
 patch=photo.crop(rect);bounds=(int(min(x for x,y in poly))-3,int(min(y for x,y in poly))-3,int(max(x for x,y in poly))+4,int(max(y for x,y in poly))+4)
 panel=Image.new('RGB',(900,210),(232,233,229));d=ImageDraw.Draw(panel)
 for i,p in enumerate((patch,im.crop(bounds))):
  p.thumbnail((360,150));p=p.resize((max(1,round(p.width*min(350/p.width,150/p.height))),max(1,round(p.height*min(350/p.width,150/p.height)))));panel.paste(p,(i*450,40))
 d.text((8,5),name+' / balanced photo',font=font,fill=(20,30,25));d.text((458,5),'actual exported surface patch',font=font,fill=(20,30,25))
 r=rows[name];d.text((8,180),f'median view luma {r["photo"]["luma_median"]:.2f} / {r["render"]["luma_median"]:.2f}; different reflected light',font=font,fill=(20,30,25));panels.append(panel)
out=BASE/'renders/final/ammo';canvas=Image.new('RGB',(900,len(panels)*210),(232,233,229))
for i,im in enumerate(panels):canvas.paste(im,(0,i*210))
canvas.save(out/'value-patches.jpg',quality=92,optimize=True)
(out/'values.json').write_text(json.dumps(dict(neutral=json.loads((BASE/'build/references/whitebalance.json').read_text())['softpoint'],patches=rows,note='Independent white-balanced photo and ray-hit GLB patches; view values, not recovered albedo. The old low-resolution source limits the primer and lead estimates.'),indent=2))
print('AMMUNITION VALUES',[(n,r['photo']['luma_median'],r['render']['luma_median']) for n,r in rows.items()])
