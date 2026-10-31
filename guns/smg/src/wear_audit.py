"""Measure actual shipped texels mapped to exterior receiver triangles."""
from pathlib import Path
import sys,json,hashlib,numpy as np
import bpy
from PIL import Image,ImageDraw,ImageFilter
sys.path.insert(0,str(Path(__file__).resolve().parent))
from wear_metrics import profile_metrics, reference, BIN_MM
BASE=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
size=2048;ob=bpy.data.objects['Receiver_Shell'];me=ob.data;me.calc_loop_triangles();uv=me.uv_layers['BakeUV']
covered=np.zeros((size,size),bool);positions=np.zeros((size,size,3),np.float32)
for tri in me.loop_triangles:
 world=np.array([tuple(ob.matrix_world@me.vertices[i].co) for i in tri.vertices]);center=world.mean(0)
 if me.polygons[tri.polygon_index].normal.x*center[0]<=.003:continue
 p=np.array([(uv.data[i].uv.x*size,(1-uv.data[i].uv.y)*size) for i in tri.loops])
 lo=np.maximum(0,np.floor(p.min(0)).astype(int));hi=np.minimum(size-1,np.ceil(p.max(0)).astype(int))
 if np.any(hi<lo):continue
 yy,xx=np.mgrid[lo[1]:hi[1]+1,lo[0]:hi[0]+1];q=np.stack((xx+.5,yy+.5),axis=-1)
 a,b,c=p;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
 if abs(den)<1e-12:continue
 wa=((b[1]-c[1])*(q[:,:,0]-c[0])+(c[0]-b[0])*(q[:,:,1]-c[1]))/den
 wb=((c[1]-a[1])*(q[:,:,0]-c[0])+(a[0]-c[0])*(q[:,:,1]-c[1]))/den;wc=1-wa-wb
 valid=(wa>=0)&(wb>=0)&(wc>=0);xyz=wa[:,:,None]*world[0]+wb[:,:,None]*world[1]+wc[:,:,None]*world[2]
 view=covered[lo[1]:hi[1]+1,lo[0]:hi[0]+1];view|=valid
 target=positions[lo[1]:hi[1]+1,lo[0]:hi[0]+1];target[valid]=xyz[valid]
base=np.asarray(Image.open(BASE/'textures/T_Relay9_BaseColor.png')).astype(float)
orm=np.asarray(Image.open(BASE/'textures/T_Relay9_ORM.png')).astype(float)
lum=base[:,:,:3]@np.array((.2126,.7152,.0722))
bright=covered&(lum>110)&(orm[:,:,2]>150)
phosphate=covered&(lum>40)&~bright&(base[:,:,3]<190)
# Opaque specular alpha distinguishes the revised enamel from unchanged
# phosphate/steel independently of its brighter diffuse RGB.
intact=covered&(base[:,:,3]>190)&(orm[:,:,2]<20)
rows={}
for name,mask in [('receiver_exterior',covered),('intact_paint',intact),('bright_steel',bright),('gray_phosphate',phosphate)]:
 if not mask.any():
  rows[name]=dict(texels=0,median_basecolor_rgb_255=None,median_orm_rgb_255=None);continue
 rows[name]=dict(texels=int(mask.sum()),median_basecolor_rgb_255=np.median(base[mask,:3],axis=0).round(2).tolist(),median_orm_rgb_255=np.median(orm[mask,:3],axis=0).round(2).tolist())
 rows[name]['median_specular_factor']=float(np.median(base[mask,3])/255)
accepted=json.loads((BASE/'src/accepted_paint.json').read_text())
for side,expected in accepted['accepted_wear_masks'].items():
 mask=Image.open(BASE/'build/markings'/('receiver_wear_'+side+'.png')).convert('RGB')
 assert hashlib.sha256(mask.tobytes()).hexdigest()==expected, ('Accepted wear changed',side)
lo,hi=accepted['shipping_specular_factor_bounds']
assert lo<rows['intact_paint']['median_specular_factor']<hi
assert np.max(np.abs(np.array(rows['intact_paint']['median_basecolor_rgb_255'])-accepted['shipping_basecolor_rgb_255']))<=accepted['maximum_median_basecolor_component_delta']
rows['rib_crests']=[]
for z in (.0861,.0891,.1027,.1059):
 mask=bright&(np.abs(positions[:,:,2]-z)<.0015)&(np.abs(positions[:,:,0])>.0185)
 if mask.any():
  zs=positions[:,:,2][mask]*1000
  rows['rib_crests'].append(dict(crest_z_mm=z*1000,bright_texels=int(mask.sum()),actual_sample_center_z_range_mm=[float(zs.min()),float(zs.max())]))
rows['polymer_properties']={}
for name in ('Lower_Mold','Stock_Mold','Handguard_Mold'):
 part=bpy.data.objects[name].data;part.calc_loop_triangles();layer=part.uv_layers['BakeUV']
 im=Image.new('L',(size,size));draw=ImageDraw.Draw(im)
 for tri in part.loop_triangles:
  draw.polygon([(float(layer.data[i].uv.x*size),float((1-layer.data[i].uv.y)*size)) for i in tri.loops],fill=255)
 mask=np.asarray(im.filter(ImageFilter.MinFilter(3)))>0
 assert mask.any(),name
 values=orm[mask]/255
 rows['polymer_properties'][name]=dict(interior_texels=int(mask.sum()),
  median_roughness=float(np.median(values[:,1])),roughness_p5_p95=np.percentile(values[:,1],[5,95]).tolist(),
  median_metallic=float(np.median(values[:,2])),median_basecolor_rgb_255=np.median(base[mask,:3],axis=0).tolist(),
  median_specular_factor=float(np.median(base[mask,3])/255),
  method='UV triangle union, one shipping pixel eroded from island boundaries; actual ORM pixels')
 assert .55<rows['polymer_properties'][name]['median_specular_factor']<.57,name
photo=reference();ribbons=[]
for z in (.0861,.0891,.1027,.1059):
 start=-.0123;span=photo['measured_span_mm'];width=int(round(span/BIN_MM))
 region=covered&(positions[:,:,0]<-.0182)&(np.abs(positions[:,:,2]-z)<photo['ribbon_depth_mm']/2000)&(positions[:,:,1]>=start)&(positions[:,:,1]<start+span/1000)
 idx=np.clip(((positions[:,:,1][region]-start)*1000/BIN_MM).astype(int),0,width-1)
 counts=np.bincount(idx,minlength=width)
 wc=np.bincount(idx,weights=(phosphate|bright)[region],minlength=width)
 bc=np.bincount(idx,weights=bright[region],minlength=width)
 worn=np.arange(100)[:,None] < (wc/np.maximum(counts,1))[None,:]*100
 br=np.arange(100)[:,None] < (bc/np.maximum(counts,1))[None,:]*100
 valid=np.broadcast_to((counts>0)[None,:],worn.shape)
 row=profile_metrics(worn,br,valid)
 row.update(crest_z_mm=z*1000,y_start_mm=start*1000,span_mm=span,
            sampled_texels=int(counts.sum()),gray_share_of_worn=float((wc-bc).sum()/max(wc.sum(),1)),
            bright_share_of_worn=float(bc.sum()/max(wc.sum(),1)))
 ribbons.append(row)
result=dict(passed=True,pattern_acceptance='The passing assertions cover shipped material/specular values. Historical 1-D ribbons below are diagnostic only; use wear-2d-values.json for receiver morphology.',ship_size=size,method='triangle-barycentric UV raster at shipping pixel centers; exterior winding selected, actual BaseColor/ORM classified; no padding or source shader-mask substitution',measurements=rows,reference=photo,shipping_ribbons=ribbons)
(BASE/'build/delivery/wear.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
