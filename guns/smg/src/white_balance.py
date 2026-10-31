"""Reference-only neutral adaptation; native patch coordinates remain auditable."""
from pathlib import Path
import json,numpy as np
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[1]
NEUTRALS={
 'studio-original.jpg':((1300,970,1480,1080),'actual neutral gray table, lower right away from the gun shadow; original upload',0),
 'left.jpg':((596,224,605,237),'white safe-selector S legend, brightest paint pixels; edited image, auxiliary',85),
 'right.jpg':((1300,100,1500,350),'unclipped pale gray studio backdrop; auxiliary',0),
 'navy2.jpg':((2270,535,2330,565),'white selector legend on upper gun; brightest paint pixels, estimated neutral',85),
 'trigger-ref.jpg':((2280,882,2340,922),'white selector safe legend; brightest paint pixels, estimated neutral',85),
 'daylight.jpg':((1700,950,1800,1100),'gray painted ship bulkhead in daylight, estimated neutral',0),
}
PATCHES={
 'navy2.jpg':{'paint':[(1780,1260),(2020,1260),(2020,1290),(1780,1290)],'polymer':[(2440,440),(2530,440),(2530,500),(2440,500)],'polymer_stock':[(2600,1420),(2780,1440),(2780,1500),(2600,1480)],'worn_phosphate':[(1840,280),(1950,280),(1950,335),(1840,335)]},
 'trigger-ref.jpg':{'paint':[(1710,604),(1980,604),(1980,625),(1710,625)],'polymer':[(2440,970),(2500,970),(2560,1070),(2500,1070)]},
 'daylight.jpg':{'paint':[(1210,1775),(1250,1730),(1270,1745),(1230,1790)],'magazine':[(1250,2125),(1280,2125),(1290,2180),(1260,2180)]},
 'left.jpg':{'paint':[(450,143),(530,143),(530,156),(450,156)],'polymer':[(640,185),(690,185),(690,230),(640,230)],'magazine':[(805,330),(825,330),(845,400),(825,400)]},
 'right.jpg':{'paint':[(810,440),(1040,430),(1040,450),(810,460)],'polymer':[(440,480),(650,480),(650,535),(440,535)],'magazine':[(750,780),(770,785),(738,885),(717,880)]},
}
def linear(a):return np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
def srgb(a):return np.where(a<=.0031308,12.92*a,1.055*np.maximum(a,0)**(1/2.4)-.055)
def stats(im,poly):
 mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(poly,fill=255)
 a=np.asarray(im.convert('RGB'),dtype=float)[np.asarray(mask)>0];rgb=np.median(a,axis=0);lum=a@np.array((.2126,.7152,.0722))
 return dict(pixels=len(a),median_rgb_255=rgb.tolist(),median_luma_255=round(float(np.median(lum)),2),rgb_ratios_g1=(rgb/max(rgb[1],1)).round(4).tolist(),luma_p20_p80=np.percentile(lum,[20,80]).round(2).tolist())
def build():
 out=BASE/'build/white-balanced';out.mkdir(parents=True,exist_ok=True);rows={};measurements={}
 for name,(rect,note,percentile) in NEUTRALS.items():
  im=Image.open(BASE/'refs'/name).convert('RGB');a=np.asarray(im,dtype=float)/255
  x0,y0,x1,y1=rect;pixels=linear(a[y0:y1,x0:x1]).reshape(-1,3)
  if percentile: pixels=pixels[pixels@np.array((.2126,.7152,.0722))>=np.percentile(pixels@np.array((.2126,.7152,.0722)),percentile)]
  sample=np.median(pixels,axis=0);neutral=sample@np.array((.2126,.7152,.0722));gain=neutral/np.maximum(sample,1e-6)
  corrected=Image.fromarray(np.round(np.clip(srgb(linear(a)*gain),0,1)*255).astype('uint8'));dest=out/(Path(name).stem+'.png');corrected.save(dest)
  marked=corrected.copy();d=ImageDraw.Draw(marked);d.rectangle(rect,outline='red',width=4)
  for key,poly in PATCHES.get(name,{}).items():d.line(poly+[poly[0]],fill='yellow',width=3)
  marked.thumbnail((1500,1200));marked.save(out/(Path(name).stem+'-patches.jpg'),quality=90)
  rows[name]=dict(output=str(dest),neutral_rectangle_native=rect,neutral_description=note,neutral_srgb_255=np.round(srgb(sample)*255,2).tolist(),linear_rgb_gains=gain.round(6).tolist())
  measurements[name]={k:stats(corrected,poly) for k,poly in PATCHES.get(name,{}).items()}
 (out/'corrections.json').write_text(json.dumps(rows,indent=2));(out/'measurements.json').write_text(json.dumps(measurements,indent=2));return rows
if __name__=='__main__':print(json.dumps(build(),indent=2))
