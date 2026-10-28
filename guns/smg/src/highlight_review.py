"""Auditable reflected-light profiles; photos stay outside all asset generation.

Display-luma peaks and widths above each intact paint median constrain the
response, not a BRDF inversion. Unknown source size, editing, reflection angle
and perspective limit any inference of physical roughness from photographs.
"""
from pathlib import Path
import argparse, json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit.fonts import find_font
from finish_review import camera
from kit.photo_match import project

PHOTO_PROFILES={
    'navy2':dict(rect=(1350,1327,1500,1382),ppm=1090/230),
    'right':dict(rect=(830,424,1030,458),ppm=410/230),
}
LUMA=np.array((.2126,.7152,.0722))

def profile_metrics(values,coordinate,baseline):
    values=np.asarray(values);coordinate=np.asarray(coordinate)
    # Peak from a three-sample box, suppressing single-pixel grain/glints.
    peak_profile=np.convolve(np.pad(values,(1,1),mode='edge'),np.ones(3)/3,mode='valid')
    i=int(peak_profile.argmax());peak=float(peak_profile[i]);half=baseline+(peak-baseline)/2
    a=b=i
    while a>0 and peak_profile[a-1]>=half:a-=1
    while b<len(values)-1 and peak_profile[b+1]>=half:b+=1
    def cross(i,j):
        if i==j or peak_profile[i]==peak_profile[j]:return float(coordinate[i])
        return float(coordinate[i]+(half-peak_profile[i])/(peak_profile[j]-peak_profile[i])*(coordinate[j]-coordinate[i]))
    lo=cross(a,max(0,a-1));hi=cross(b,min(len(values)-1,b+1))
    return dict(paint_median_luma_255=float(baseline),highlight_peak_luma_255=peak,
                peak_over_median=peak/baseline,half_excess_luma_255=half,
                width_half_excess=float(abs(hi-lo)),width_interval=[lo,hi],
                width_boundary_censored=a==0 or b==len(values)-1,
                coordinates=coordinate.tolist(),luma=values.tolist())

def build(response_dir=None):
    refs=json.loads((BASE/'build/white-balanced/measurements.json').read_text())
    wb=json.loads((BASE/'build/white-balanced/corrections.json').read_text())
    result=dict(method='Spatial median across fixed intact-crown strips; peak after three-sample box; full width at half of peak excess over that crown profile median. Flat-land reference medians retained separately. Display luma 0–255.',
                limitations='Approximate photographic scale and uncontrolled source dimensions, reflection angle, perspective and editing; observed appearance, not recovered BRDF.',photos={},render={})
    out=BASE/'renders/final/pairs';out.mkdir(exist_ok=True,parents=True)
    regions={}
    for name,spec in PHOTO_PROFILES.items():
        im=Image.open(BASE/'build/white-balanced'/(name+'.png')).convert('RGB')
        x0,y0,x1,y1=spec['rect'];lum=np.asarray(im,dtype=float)@LUMA
        values=np.median(lum[y0:y1,x0:x1],axis=1)
        row=profile_metrics(values,np.arange(y0,y1),float(np.median(values)))
        row['flat_paint_median_luma_255']=refs[name+'.jpg']['paint']['median_luma_255']
        row['peak_over_flat_paint_median']=row['highlight_peak_luma_255']/row['flat_paint_median_luma_255']
        row.update(rectangle_native=list(spec['rect']),width_unit='native px',approximate_width_mm=row['width_half_excess']/spec['ppm'],pixels_per_mm=spec['ppm'],neutral=wb[name+'.jpg'])
        result['photos'][name]=row
        regions[name]=im.crop((x0-15,y0-15,x1+15,y1+15))
        marked=im.crop((x0-20,y0-30,x1+20,y1+30));d=ImageDraw.Draw(marked)
        for y in row['width_interval']:d.line((0,y-y0+30,marked.width,y-y0+30),fill='orange',width=1)
        marked.resize((marked.width*3,marked.height*3),Image.Resampling.NEAREST).save(out/(name+'-highlight-region.png'))
    response=Path(response_dir) if response_dir else BASE/'renders/final/finish-response'
    if (response/'shots.json').exists():
        meta=json.loads((response/'shots.json').read_text())['paint_response']
        im=Image.open(response/'paint_response.png').convert('RGB');a=np.asarray(im,dtype=float)@LUMA
        theta=np.linspace(.18,np.pi-.18,180)
        stations=[]
        for y in np.linspace(.025,.065,25):
            stations.append(np.stack((.0167*np.cos(theta),np.full_like(theta,y),.1105+.0205*np.sin(theta)),axis=1))
        points=np.array(stations);xy=project(camera(meta),points.reshape(-1,3),im.width,im.height)[0].reshape(25,-1,2)
        x=xy[:,:,0];y=xy[:,:,1];ix=np.floor(x).astype(int);iy=np.floor(y).astype(int);fx=x-ix;fy=y-iy
        v=a[iy,ix]*(1-fx)*(1-fy)+a[iy,ix+1]*fx*(1-fy)+a[iy+1,ix]*(1-fx)*fy+a[iy+1,ix+1]*fx*fy
        values=np.median(v,axis=0)
        center=xy[12];dist=np.r_[0,np.cumsum(np.linalg.norm(np.diff(center,axis=0),axis=1))]
        baseline=float(np.median(values))
        row=profile_metrics(values,dist,baseline)
        row.update(width_unit='native px along projected crown',profile_world_points_m=points[12].tolist(),profile_pixels=center.tolist(),
                   source='export/smg.glb',lighting='Identical final_shots studio configuration, exposure -0.15; supplemental camera only')
        # Top view uses the actual 33.4-mm outer crown width as its scale.
        span=project(camera(meta),np.array([(-.0167,.045,.1105),(.0167,.045,.1105)]),im.width,im.height)[0]
        ppm=float(np.linalg.norm(span[1]-span[0])/33.4)
        row.update(pixels_per_mm=ppm,approximate_width_mm=row['width_half_excess']/ppm)
        # The new upper-land wear enters this historical probe. The old
        # width target was withdrawn; retain the raw curve without calling
        # phosphate peaks an intact-paint highlight or a changed BRDF.
        keys=('paint_median_luma_255','highlight_peak_luma_255','peak_over_median',
              'half_excess_luma_255','width_half_excess','width_interval',
              'width_boundary_censored','approximate_width_mm')
        row['mixed_profile_metrics']={k:row[k] for k in keys}
        for k in keys:row[k]=None
        row.update(valid_intact_paint_profile=False,
            diagnostic_status='Historical fixed probe now crosses receiver wear; raw mixed curve only. The 4–6-mm highlight target is withdrawn.')
        result['render']['paint_response']=row
        lo=np.floor(xy.min(axis=(0,1))).astype(int)-8;hi=np.ceil(xy.max(axis=(0,1))).astype(int)+8
        regions['paint_response']=im.crop(tuple(map(int,(*lo,*hi))))
        d=ImageDraw.Draw(im)
        for station in xy[::6]:d.line([tuple(p) for p in station],fill='orange',width=1)
        im.save(response/'paint_response-loci.jpg',quality=95)
    audit=json.loads((BASE/'build/delivery/wear.json').read_text())['measurements']
    result['shipping_surface_properties']=dict(paint_roughness=audit['intact_paint']['median_orm_rgb_255'][1]/255,
        paint_basecolor_srgb_255=audit['intact_paint']['median_basecolor_rgb_255'],
        paint_specular_factor=audit['intact_paint']['median_specular_factor'],
        polymer=audit['polymer_properties'],phosphate_roughness=audit['gray_phosphate']['median_orm_rgb_255'][1]/255,
        phosphate_metallic=audit['gray_phosphate']['median_orm_rgb_255'][2]/255)
    # Same fixed profile convention on both photographs and the exported GLB.
    entries=[*result['photos'].items(),*result['render'].items()]
    panel=Image.new('RGB',(700*len(entries),690),(228,229,225));d=ImageDraw.Draw(panel)
    font=ImageFont.truetype(find_font('Noto Sans','Regular'),17)
    for i,(name,row) in enumerate(entries):
        x=i*700;mixed=not row.get('valid_intact_paint_profile',True)
        measured=row['mixed_profile_metrics'] if mixed else row
        d.text((x+16,12),name+(' / mixed paint and wear' if mixed else ' / intact paint'),font=font,fill=(20,30,25))
        crop=ImageOps.contain(regions[name],(660,190),Image.Resampling.LANCZOS)
        panel.paste(crop,(x+(700-crop.width)//2,50+(190-crop.height)//2))
        coord=np.array(row['coordinates']);v=np.array(row['luma'])
        p=np.stack((x+30+(coord-coord.min())/max(np.ptp(coord),1)*640,405-v/255*145),axis=1)
        d.line([tuple(a) for a in p],fill=(35,75,100),width=2)
        for value,color in [(measured['paint_median_luma_255'],(150,90,50)),(measured['half_excess_luma_255'],(70,100,70))]:
            y=405-value/255*145;d.line((x+30,y,x+670,y),fill=color,width=1)
        if mixed:
            text=['Historical probe crosses the new rubbed strip.',
                  'Intact-paint peak / width: unavailable from this probe.',
                  'Raw mixed-surface curve retained for transparency.',
                  '4–6-mm target withdrawn; lighting and paint BRDF unchanged.']
        else:text=[f"Crown median {row['paint_median_luma_255']:.2f}; peak {row['highlight_peak_luma_255']:.2f} / 255",
              f"Peak / median {row['peak_over_median']:.2f}; half-excess width {row['approximate_width_mm']:.2f} mm",
              'Blue: measured profile. Brown: crown median. Green: half-excess.',
              'Estimated photo scale; different lighting is not a recovered BRDF.']
        if 'flat_paint_median_luma_255' in row:text.append(f"Flat-land median {row['flat_paint_median_luma_255']:.2f}; peak / land {row['peak_over_flat_paint_median']:.2f}")
        if row.get('width_boundary_censored'):text.append('WIDTH CENSORED: highlight reaches measured window boundary.')
        for j,line in enumerate(text):d.text((x+16,430+j*30),line,font=font,fill=(20,30,25))
    props=result['shipping_surface_properties'];poly=props['polymer']
    d.text((16,625),f"Actual shipped roughness medians: paint {props['paint_roughness']:.3f}; lower / stock {poly['Lower_Mold']['median_roughness']:.3f}; handled handguard {poly['Handguard_Mold']['median_roughness']:.3f} (p5 {poly['Handguard_Mold']['roughness_p5_p95'][0]:.3f}).",font=font,fill=(20,30,25))
    d.text((16,655),f"Paint BC {props['paint_basecolor_srgb_255']}; specular factor {props['paint_specular_factor']:.3f}. Phosphate roughness {props['phosphate_roughness']:.3f} / metallic {props['phosphate_metallic']:.3f}. Camera / source differences limit width comparison.",font=font,fill=(20,30,25))
    panel.save(out/'paint-highlight-pair.jpg',quality=94)
    (out/'highlight-values.json').write_text(json.dumps(result,indent=2))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--response');a=p.parse_args();rows=build(a.response)
    print(json.dumps({group:{k:{f:v for f,v in row.items() if f in ('paint_median_luma_255','highlight_peak_luma_255','peak_over_median','width_half_excess','approximate_width_mm','width_boundary_censored','valid_intact_paint_profile','diagnostic_status')} for k,row in rows[group].items()} for group in ('photos','render')},indent=2))
