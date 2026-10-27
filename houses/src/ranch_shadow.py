"""Measure the hero's eave band in rendered pixels and on imported surfaces."""
import json
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
from PIL import Image,ImageDraw
from bpy_extras.object_utils import world_to_camera_view


def measure(path,meta,camera,direction):
 sc=bpy.context.scene;bpy.context.view_layer.update();im=Image.open(path).convert('RGB');rgb=np.asarray(im)/255.;weights=np.array((.2126,.7152,.0722));m,g=meta['blocks'];front=m['y0']-.0725
 def project(p):
  q=world_to_camera_view(sc,camera,Vector(p));return (q.x*im.width,(1-q.y)*im.height)
 def patch(points):
  polygon=[project(p) for p in points];mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(polygon,fill=255);a=rgb[np.asarray(mask)>0]
  linear=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
  return dict(encoded_y=float(np.mean(a@weights)),linear_y=float(np.mean(linear@weights)),pixels=len(a),polygon_pixels=polygon)
 centers=[g['x0']+g['x1']*0+1.8,g['x0']+2.8,g['x0']+3.8]
 # Select actual front-facing masonry triangles in this clear wall pier.
 heights=[]
 for ob in sc.objects:
  if ob.type!='MESH' or not ob.get('asset_set'):continue
  for poly in ob.data.polygons:
   if not ob.data.materials[poly.material_index].name.startswith('RanchBrick'):continue
   n=ob.matrix_world.to_3x3()@poly.normal
   if n.y>-.9:continue
   pts=[ob.matrix_world@ob.data.vertices[i].co for i in poly.vertices]
   if all(abs(p.y-front)<.002 for p in pts) and centers[0]-.5<sum(p.x for p in pts)/len(pts)<centers[-1]+.5:heights.extend(p.z for p in pts)
 top=max(heights);profiles=[];bands=[];band_patches=[]
 for x in centers:
  zs=np.arange(1.75,top-.03,.01)
  def at(z):return patch([(x-.35,front,z-.02),(x+.35,front,z-.02),(x+.35,front,z+.02),(x-.35,front,z+.02)])
  ys=np.array([at(z)['encoded_y'] for z in zs]);low=float(np.median(ys[zs<2.08]));high=float(np.median(ys[zs>top-.32]));threshold=(low+high)/2
  candidates=[i for i in range(len(zs)-1) if ys[i]>=threshold and ys[i+1]<threshold]
  assert candidates,(x,low,high)
  i=max(candidates,key=lambda j:ys[j]-ys[j+1]);bottom=float(zs[i]+(threshold-ys[i])/(ys[i+1]-ys[i])*.01)
  pixels=abs(project((x,front,bottom))[1]-project((x,front,top))[1]);bands.append(top-bottom)
  band_patches.append(patch([(x-.35,front,bottom+.12),(x+.35,front,bottom+.12),(x+.35,front,top-.08),(x-.35,front,top-.08)]))
  profiles.append(dict(x_m=x,z_m=list(map(float,zs)),encoded_y=list(map(float,ys)),threshold_y=threshold,bottom_z_m=bottom,height_m=top-bottom,height_pixels=pixels))
 side=patch([(g['x1']+.0725,g['y0']+.85,1.20),(g['x1']+.0725,g['y0']+1.55,1.20),(g['x1']+.0725,g['y0']+1.55,1.80),(g['x1']+.0725,g['y0']+.85,1.80)])
 # Project each delivered vertex along the sun ray onto presentation grade.
 shadows=[];ray=Vector(direction)
 for ob in sc.objects:
  if ob.type!='MESH' or not ob.get('asset_set'):continue
  for v in ob.data.vertices:
   p=ob.matrix_world@v.co
   if p.z>0:
    q=p+ray*(-p.z/ray.z);shadows.append(project(q))
 bounds=[min(p[0] for p in shadows),min(p[1] for p in shadows),max(p[0] for p in shadows),max(p[1] for p in shadows)]
 result=dict(scope='Threshold crossings in rendered front-wall profiles; masonry top from imported triangles; Y-prime encoded Rec.709, not albedo',masonry_top_z_m=top,median_band_height_m=float(np.median(bands)),median_band_height_pixels=float(np.median([p['height_pixels'] for p in profiles])),band_patches=band_patches,band_encoded_y=float(np.mean([p['encoded_y'] for p in band_patches])),shaded_side=side,profiles=profiles,ground_shadow_projected_bounds_pixels=bounds,ground_shadow_in_frame=all((bounds[0]>=0,bounds[1]>=0,bounds[2]<im.width,bounds[3]<im.height)))
 path.with_name('eave-band.json').write_text(json.dumps(result,indent=2))
 from kit.fonts import find_font
 from PIL import ImageFont
 annotated=im.copy();draw=ImageDraw.Draw(annotated);font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),20)
 for p in band_patches:draw.polygon(p['polygon_pixels'],outline=(245,198,45),width=2)
 draw.polygon(side['polygon_pixels'],outline=(80,205,245),width=2)
 label=f"Eave band: {result['median_band_height_m']:.3f} m / {result['median_band_height_pixels']:.1f} px; Y' {result['band_encoded_y']:.3f}; shaded side {side['encoded_y']:.3f}"
 draw.rectangle((12,12,im.width-12,46),fill=(18,24,22));draw.text((22,17),label,font=font,fill=(245,245,235))
 annotated.save(path.with_name('hero-band-measurement.jpg'),quality=92,optimize=True)
 print('EAVE_BAND',result['median_band_height_m'],result['median_band_height_pixels'],result['band_encoded_y'],side['encoded_y'],result['ground_shadow_in_frame'],flush=True)
 return result
