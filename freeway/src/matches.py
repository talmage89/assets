"""Feature camera calibration using the kit, with visible residuals/limits.

The real sites are different civil designs. Landmarks align a guide panel, a
pier-cap plane and the central diamond, not the original signs or whole cities.
Photographs and field-neutral corrections are comparison inputs only.
"""
import sys,json
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.photo_match import calibrate,compose

def balance(name,roi):
    im=np.asarray(Image.open('refs/'+name+'.jpg').convert('RGB'),dtype=float)/255
    x0,y0,x1,y1=roi;rgb=np.median(im[y0:y1,x0:x1].reshape(-1,3),axis=0);gains=rgb.mean()/rgb
    out=Path('build/balanced-'+name+'.jpg');Image.fromarray(np.uint8(np.round(np.clip(im*gains,0,1)*255))).save(out,quality=96)
    return str(out),dict(neutral_roi=roi,median_RGB=rgb.tolist(),gains=gains.tolist(),exposure_change=0,scope='Approximate field-neutral white balance; no known gray card or calibrated reflectance')

def cameras():
    highway,hw=balance('freeway-2008',[370,1460,470,1510])
    bridge,br=balance('bridge-2008',[1800,1500,1950,1570])
    diamond,di=balance('diamond-2002',[430,42,455,60])
    definitions={
        'guide_2008':dict(title='Guide panel proportions / 2008 freeway photograph',photo=highway,crop=[0,350,2726,1785],
            location=(2,-190,1.8),target=(-1,-155,7),lens=45,camera_height_m=(1.8,.6),lens_bounds_mm=(24,70),
            landmarks=[dict(world=(x,-155.852,z),pixel=px) for x,z,px in [(-8.5,9.23,(472,566)),(-1.5,9.23,(1153,565)),(-1.5,6.49,(1153,812)),(-8.5,6.49,(472,812))]],
            source='export/Freeway-101.gltf',limitations='Four coplanar panel corners, estimated dimensions and lens; six photographed lanes versus four modeled. Compare sign form and mounted scale, not roadway capacity.'),
        'bearing_2008':dict(title='Bearing-seat and cap plane / FHWA 2008 bridge',photo=bridge,crop=[0,0,2816,2112],
            location=(5,0,4.8),target=(0,-7,5.0),lens=45,lens_bounds_mm=(24,100),
            landmarks=[dict(world=(1,y,z),pixel=px) for y,z,px in [(-9.9,5.5584,(1044,1345)),(-7.,5.5584,(1620,1255)),(-7.,4.4584,(1620,1695)),(-9.9,4.4584,(1044,1730))]],
            source='export/modules/Overpass.gltf',limitations='Cap-plane framing fit only. The photo has a pile bent and SCC beams; this family uses round columns and traditional I girders. No survey dimensions or one-to-one bridge reproduction claimed.'),
        'diamond_2002':dict(title='Diamond plan / USGS 2002 aerial photograph',photo=diamond,crop=[0,0,636,413],
            location=(-90,-40,1100),target=(0,0,0),lens=65,lens_bounds_mm=(24,200),
            landmarks=[dict(world=p,pixel=px) for p,px in [((78,0,7.35),(355,162)),((-78,0,7.35),(318,248)),((0,40,0),(310,195)),((0,-40,0),(357,213)),((0,0,7.35),(335,204))]],
            source='export/Freeway-101.gltf',limitations='Central five-point layout fit. Orthographic USGS photography is approximated with a long pinhole view. The real west approach curves and has a different right of way and terminal spacing.'),
    }
    rows={}
    for name,definition in definitions.items():
        rows[name]=calibrate(definition);rows[name]['source']=definition['source'];rows[name]['limitations']=definition['limitations']
        rows[name]['shot'].update(sun_direction=(.2,.2,-1),sun_energy=5,exposure=-.35)
        print(name,'RMS',round(rows[name]['residual_rms_pixels'],3),'lens',round(rows[name]['shot']['lens'],2))
    Path('build/cameras.json').write_text(json.dumps(rows,indent=2))
    Path('build/reference-balance.json').write_text(json.dumps(dict(guide_2008=hw,bearing_2008=br,diamond_2002=di),indent=2))

if __name__=='__main__':
    if '--compose' in sys.argv:compose('build/cameras.json','renders/matches','renders/matches')
    else:cameras()
