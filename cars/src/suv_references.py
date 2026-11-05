"""Sparse manual measurements of manufacturer plans and stock photographs.

This review-only module never supplies geometry to the modeler. Reference
images are viewed/annotated, never projected, traced or baked into the asset.
Coordinates are recorded in the stated page/image coordinate systems. Plan
scales use the published envelope independently in each page direction; these
are rescue-sheet illustrations, not dimensioned engineering plans.
"""
import argparse,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),14)

PLANS={
 'rav4':dict(file='suv-rav4-plan.pdf',length_mm=4595,width_mm=1855,
   page_envelope=[125,409,1091,805],center_y=607,
   front_center=[125,607],rear_center=[1091,607],
   front_corner=[182,436],rear_corner=[1038,436]),
 'crv':dict(file='suv-crv-plan.pdf',length_mm=4625,width_mm=1855,
   page_envelope=[129.5,272,1161,690],center_y=481,
   front_center=[129.5,481],rear_center=[1161,481],
   front_corner=[187,301],rear_corner=[1117,301]),
}
# Picks on a 1200 x 900 review resize. The image scale is the body width at
# the fascia, not mirror span. Perspective and depth allow about +/-30 mm.
PHOTOS={
 'rav4_front':dict(file='suv-rav4-face.jpg',width_px=[238,940],
   hood_y=425,ground_y=766,chin_y=701,black_top_y=553,
   painted_corner_bottom_y=646,lamp_outer_y=[397,458]),
 'crv_front':dict(file='suv-crv-face.jpg',width_px=[234,969],
   hood_y=445,ground_y=768,chin_y=720,black_top_y=600,
   painted_corner_bottom_y=621,lamp_outer_y=[409,475]),
 'rav4_rear':dict(file='suv-rav4-back.jpg',width_px=[236,965],
   black_top_y=490,lip_top_y=560,chin_y=650,lamp_outer_y=[295,365]),
 'crv_rear':dict(file='suv-crv-back.jpg',width_px=[233,966],
   black_top_y=563,lip_top_y=580,chin_y=672,lamp_outer_y=[291,369]),
}

def measure():
 result={'plan':{},'photos':{},'caveat':'Sparse manual picks; +/-20 mm plan and +/-30 mm photo estimates. No model calibration uses these pixels. Plan corners are at about 800 mm from the centerline. Honda RW rescue drawing predates the facelift; it is scaled to the cited US 4625 mm envelope. Allow for the small trim difference.'}
 for make,r in PLANS.items():
  x0,y0,x1,y1=r['page_envelope'];sx=r['length_mm']/(x1-x0);sy=r['width_mm']/(y1-y0)
  result['plan'][make]=dict(front_setback_mm=(r['front_corner'][0]-r['front_center'][0])*sx,
   rear_setback_mm=(r['rear_center'][0]-r['rear_corner'][0])*sx,
   corner_halfwidth_mm=(r['center_y']-r['front_corner'][1])*sy,picks=r)
 for name,r in PHOTOS.items():
  scale=1855/(r['width_px'][1]-r['width_px'][0]);values=dict(black_height_mm=(r['chin_y']-r['black_top_y'])*scale,
   outer_lamp_height_mm=(r['lamp_outer_y'][1]-r['lamp_outer_y'][0])*scale,picks=r)
  if 'ground_y' in r:values.update(black_share_hood_to_ground=(r['chin_y']-r['black_top_y'])/(r['ground_y']-r['hood_y']),painted_corner_black_height_mm=(r['chin_y']-r['painted_corner_bottom_y'])*scale)
  else:values['lower_lip_below_upper_crease_mm']=(r['chin_y']-r['lip_top_y'])*scale
  result['photos'][name]=values
 return result

def main():
 p=argparse.ArgumentParser();p.add_argument('--refs',default='refs');p.add_argument('--out',required=True);p.add_argument('--plan-pages',default='../build');a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 report=measure();(out/'reference-measurements.json').write_text(json.dumps(report,indent=2))
 for name,r in PHOTOS.items():
  im=Image.open(Path(a.refs)/r['file']).convert('RGB').resize((1200,900));draw=ImageDraw.Draw(im)
  for k,y in r.items():
   if not k.endswith('_y') or not isinstance(y,(float,int)):continue
   draw.line([(r['width_px'][0],y),(r['width_px'][1],y)],fill=(20,100,210),width=2);draw.text((r['width_px'][1]+5,y-8),k,fill=(10,50,130),font=FONT)
  x=r['width_px'][1]-65;ya,yb=r['lamp_outer_y'];draw.line([(x,ya),(x,yb)],fill=(220,65,20),width=3)
  draw.rectangle((0,0,1200,50),fill='white');draw.text((16,12),name+' | neutral: white studio background, unit RGB gains; sparse dimension picks only',fill='black',font=FONT)
  im.save(out/(name+'-measurements.jpg'),quality=88)
 for name,r in PLANS.items():
  im=Image.open(Path(a.plan_pages)/('suv-'+name+'-plan.png')).convert('RGB');draw=ImageDraw.Draw(im)
  for kind in ['front','rear']:
   a0=r[kind+'_center'];c=r[kind+'_corner'];draw.line([tuple(a0),(a0[0],c[1]),tuple(c)],fill=(225,65,20),width=3)
   for x,y in [a0,c]:draw.ellipse((x-4,y-4,x+4,y+4),fill=(20,90,220))
  im.thumbnail((1600,1600));im.save(out/(name+'-plan-measurements.jpg'),quality=88)
 print(json.dumps({k:{m:{q:round(v,1) if isinstance(v,float) else v for q,v in r.items() if q!='picks'} for m,r in d.items()} for k,d in report.items() if k!='caveat'},indent=2))
if __name__=='__main__':main()
