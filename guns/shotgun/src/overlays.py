"""Compare exported silhouettes with manually observed photographic landmarks.

Only this review compositor reads photos. No reference contour is extracted or
used by geometry. Distances are local camera-plane estimates, not metrology.
"""
import json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps,ImageFilter,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.fonts import find_font
POINTS={
 'right':[("comb heel",(60,141)),("comb aft",(180,128)),("comb middle",(280,117)),
  ("comb front",(350,111)),("comb nose",(406,110)),("wrist top",(442,95)),
  ("grip cap aft",(367,212)),("grip cap front",(391,218)),("wrist underside",(419,163)),
  ("belly",(311,203)),("wood toe",(76,300))],
 'left':[("comb aft",(2930,817)),("comb middle",(2800,815)),("comb front",(2660,813)),
  ("comb nose",(2600,822)),("wrist top",(2500,803)),
  ("grip cap",(2610,985)),("belly",(2690,950))]}
def basis(row):
 s=row['shot'];c=np.array(s['location']);f=np.array(s['target'])-c;f/=np.linalg.norm(f)
 r=np.cross(f,[0,0,1]);r/=np.linalg.norm(r);u=np.cross(r,f);a=s['roll']
 r,u=r*math.cos(a)+u*math.sin(a),u*math.cos(a)-r*math.sin(a)
 w=row['crop'][2]-row['crop'][0];h=row['crop'][3]-row['crop'][1];focal=w*s['lens']/36
 def unproject(q):
  v=f+(q[0]-w/2)/focal*r-(q[1]-h/2)/focal*u
  return c-c[0]/v[0]*v
 return unproject
def main():
 data=json.loads((BASE/'build/cameras.json').read_text());out=BASE/'renders/checkpoint/pairs';report={}
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),20)
 for side in ('right','left'):
  row=data[side+'_photo'];photo=ImageOps.exif_transpose(Image.open(row['photo'])).convert('RGBA').crop(row['crop'])
  alpha=Image.open(BASE/'renders/checkpoint/stock-masks'/('stock_'+side+'.png')).getchannel('A').resize(photo.size,Image.Resampling.LANCZOS)
  mask=alpha.point(lambda x:255 if x>128 else 0);edge=np.asarray(mask).astype(int)-np.asarray(mask.filter(ImageFilter.MinFilter(3))).astype(int)
  ys,xs=np.where(edge>0);edges=np.c_[xs,ys];assert len(edges)>100
  tint=Image.new('RGBA',photo.size,(0,210,240,0));tint.putalpha(mask.point(lambda x:round(x*.10)));photo.alpha_composite(tint)
  stroke=Image.new('RGBA',photo.size,(0,210,240,0));stroke.putalpha(Image.fromarray(np.uint8(edge)));photo.alpha_composite(stroke)
  canvas=Image.new('RGB',(photo.width,photo.height+88),(235,237,232));canvas.paste(photo.convert('RGB'),(0,65));d=ImageDraw.Draw(canvas)
  d.text((12,7),'Cyan: exported wood silhouette / photo beneath / '+side,font=font,fill=(20,40,35))
  d.text((12,31),'Observed points: magenta / distances are local camera-plane estimates',font=font,fill=(20,40,35))
  unproject=basis(row);rows=[]
  for label,p in POINTS[side]:
   p=np.array(p,float)-row['crop'][:2];idx=np.argmin(np.sum((edges-p)**2,axis=1));q=edges[idx];pixels=float(np.linalg.norm(q-p))
   millimeters=float(np.linalg.norm(unproject(q)-unproject(p))*1000)
   a=tuple(p+[0,65]);b=tuple(q+[0,65]);d.line((*a,*b),fill=(240,30,150),width=2)
   d.ellipse((a[0]-3,a[1]-3,a[0]+3,a[1]+3),outline=(240,30,150),width=2)
   rows.append(dict(region=label,observed_pixel=p.tolist(),nearest_export_contour_pixel=q.tolist(),distance_pixels=pixels,estimated_distance_mm=millimeters))
  canvas.save(out/('stock_'+side+'-overlay.jpg'),quality=94,optimize=True)
  report[side]=dict(scope='manually observed photo points to exported wood contour; estimated lens and X=0 camera-plane scale',camera_rms_pixels=row['residual_rms_pixels'],points=rows)
  if side=='right':
   # Independently observed inside edges and bow wall in the utility photo.
   # These are approximate camera-plane distances, not source mesh dimensions.
   measures=[]
   for label,a,b in [('guard opening at middle height',(510,152),(580,152)),
                     ('guard opening height',(550,138),(550,168)),
                     ('guard lower bow wall',(540,170),(540,176))]:
    a=np.array(a,float)-row['crop'][:2];b=np.array(b,float)-row['crop'][:2]
    measures.append(dict(region=label,observed_pixels=[a.tolist(),b.tolist()],
                         estimated_distance_mm=float(np.linalg.norm(unproject(a)-unproject(b))*1000)))
   report[side]['guard_photo_measures']=measures
 (BASE/'build/stock-profile.json').write_text(json.dumps(report,indent=2))
 print('STOCK OVERLAYS',[(s,round(max(p['estimated_distance_mm'] for p in r['points']),2)) for s,r in report.items()])
if __name__=='__main__':main()
