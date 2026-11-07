"""Within-photo linear ratios, with no attempt to recover camera exposure."""
import json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
Y=np.array([.2126,.7152,.0722])
def linear(a):return np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
def measure():
    path=Path('refs/20070329_Burnham_Park_Skatepark.JPG');im=Image.open(path).convert('RGB');a=linear(np.asarray(im,float)/255)
    rois=dict(neutral=(1600,1150,1650,1180),concrete=(1600,1150,1650,1180),lawn_dark=(850,1860,1000,1940),lawn_dry=(1400,2080,1550,2150))
    x0,y0,x1,y1=rois['neutral'];n=np.median(a[y0:y1,x0:x1],axis=(0,1));gains=n.mean()/n;a*=gains
    vals={k:float(np.median(a[y0:y1,x0:x1]@Y)) for k,(x0,y0,x1,y1) in rois.items()}
    ratios={k:vals['concrete']/vals[k] for k in ('lawn_dark','lawn_dry')}
    lawn=linear(np.asarray(Image.open('../ground/textures/ship/T_Lawn_BaseColor.png').convert('RGB'),float)/255)
    lawn_Y=float(np.median(lawn@Y))
    d=ImageDraw.Draw(im)
    for k,r in rois.items():d.rectangle(r,outline=(240,25,25),width=6);d.text((r[0],r[1]-30),k,fill=(255,0,0),stroke_width=1)
    out=Path('renders/ratios');out.mkdir(parents=True,exist_ok=True);im.save(out/'photo-rois.jpg',quality=95)
    report=dict(photo=str(path),neutral_description='Unpainted sunlit concrete assumed neutral, no gray card; linear RGB gains preserve mean luminance',rois=rois,linear_white_balance=gains.tolist(),linear_Y=vals,concrete_to_lawn_ratios=ratios,limits='Different grass moisture/dormancy and the unknown camera response bound the range. Ratios cancel a common exposure, not tone curves or unequal illumination. These are calibration constraints, not measured reflectances.')
    report.update(fixed_Ground_lawn_linear_Y=lawn_Y,target_concrete_linear_Y_from_fixed_lawn=[min(ratios.values())*lawn_Y,max(ratios.values())*lawn_Y])
    pool=Image.open('refs/memorial.jpg').convert('RGB');pixels=linear(np.asarray(pool,float)/255)
    pool_rois=dict(coping=(20,780,90,810),tile_a=(40,850,100,867),tile_b=(280,880,330,897),wall=(200,950,260,1030),nose=(50,830,100,838))
    x0,y0,x1,y1=pool_rois['coping'];neutral=np.median(pixels[y0:y1,x0:x1],axis=(0,1));balance=neutral.mean()/neutral;pixels*=balance
    colors={k:np.median(pixels[y0:y1,x0:x1],axis=(0,1)).tolist() for k,(x0,y0,x1,y1) in pool_rois.items()}
    values={k:float(np.median(pixels[y0:y1,x0:x1]@Y)) for k,(x0,y0,x1,y1) in pool_rois.items()}
    report['memorial']=dict(neutral='Unpainted coping top, assumed neutral',rois=pool_rois,linear_white_balance=balance.tolist(),linear_RGB=colors,linear_Y=values,ratios_to_coping={k:values[k]/values['coping'] for k in values if k!='coping'},limits='Wall, tile and coping have different surface normals and illumination; ratios describe this photographed view, not albedo ratios.')
    d=ImageDraw.Draw(pool)
    for k,r in pool_rois.items():d.rectangle(r,outline=(240,25,25),width=5);d.text((r[0],r[1]-22),k,fill=(255,0,0),stroke_width=1)
    pool.save(out/'memorial-rois.jpg',quality=95)
    Path('build/albedo-ratios.json').write_text(json.dumps(report,indent=2));return report
if __name__=='__main__':print(json.dumps(measure(),indent=2))
