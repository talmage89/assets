"""Display-image color/value populations, never a reflectance calibration."""
import colorsys
from pathlib import Path
import numpy as np
from PIL import Image
from reference_measurements import MEASUREMENTS


def measure(image,crop=None):
    im=Image.open(image).convert('RGBA')
    if crop:im=im.crop(crop)
    a=np.asarray(im)/255
    green=(a[:,:,1]>a[:,:,0]*1.10)&(a[:,:,1]>a[:,:,2]*1.08)&(a[:,:,3]>.5)
    rgb=a[:,:,:3][green];lum=rgb@np.array([.2126,.7152,.0722])
    p=np.percentile(lum,[5,20,50,80,95]);row=dict(selected_green_pixels=len(rgb),display_luminance_p5_p50_p95=p[[0,2,4]].tolist())
    for name,mask in [('brightest_20_percent',lum>=p[3]),('darkest_20_percent',lum<=p[1])]:
        mean=rgb[mask].mean(axis=0);h,s,v=colorsys.rgb_to_hsv(*mean)
        row[name]=dict(mean_display_rgb=mean.tolist(),hue_degrees=h*360,saturation=s,median_display_luminance=float(np.median(lum[mask])))
    row['scope']='Selected green display pixels; population comparison across different lighting and individuals, not calibrated albedo or equal illumination'
    return row


def comparisons(renders):
    root=Path(__file__).resolve().parents[1]
    return {name:dict(model=measure(Path(renders)/('match_'+name+'.png')),
                      photo=measure(root/'refs'/ref['photo'],ref['crown']),
                      use='color and form' if name=='psu' else 'form only; shifted scanned slide') for name,ref in MEASUREMENTS.items()}
