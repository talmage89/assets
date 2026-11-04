"""Dimensioned source evidence and photo comparisons. Writes no docs assets."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.fonts import find_font
import hatch_spec as S
ASSET=Path(__file__).resolve().parents[1]
FONT=find_font('Noto Sans','Regular')
def font(size):return ImageFont.truetype(FONT,size)
def rgb(path):
    im=Image.open(path).convert('RGBA');bg=Image.new('RGBA',im.size,(229,231,232,255));bg.alpha_composite(im);return bg.convert('RGB')
def save(im,path):im.save(path,quality=93,optimize=True)

# Pixels were picked while viewing the 1200-wide reference previews. Photos
# are read only by this comparison program, never by any modeling/bake script.
PROFILE_PICKS={
 'corolla':dict(hubs=[(246,566),(974,566)],wheelbase=2.640,
  top=[('hood lead',60,443),('hood middle',180,400),('cowl',335,373),('windshield',430,318),('roof front',550,274),('roof peak',700,255),('roof aft',900,259),('spoiler',1008,274),('backlight',1053,323),('tail',1120,369)],
  ends=[('nose upper',33,485,True),('nose bumper',30,530,True),('chin',31,577,True),('tail upper',1145,449,False),('tail bumper',1171,502,False),('tail lower',1159,563,False)]),
 'hyundai':dict(hubs=[(241,566),(976,565)],wheelbase=2.650,
  top=[('hood lead',60,440),('hood middle',180,400),('cowl',330,375),('windshield',430,318),('roof front',550,266),('roof peak',700,249),('roof aft',940,257),('spoiler',1060,274),('backlight',1104,319),('tail',1141,355)],
  ends=[('nose upper',29,477,True),('nose bumper',29,531,True),('chin',36,582,True),('tail upper',1161,449,False),('tail bumper',1170,499,False),('tail lower',1153,555,False)])}

def side_overlay(out,shots):
    records={};source=Image.open(out/'side.png').convert('RGBA')
    sf=np.array(shots['side']['points']['front_axle']);sr=np.array(shots['side']['points']['rear_axle'])
    for make,picks in PROFILE_PICKS.items():
        photo=Image.open(ASSET/('refs/hatch-'+make+'-side.jpg')).convert('RGBA')
        factor=photo.width/1200;pf,pr=[np.array(q)*factor for q in picks['hubs']]
        v,w=sr-sf,pr-pf;angle=math.atan2(w[1],w[0])-math.atan2(v[1],v[0]);scale=np.linalg.norm(w)/np.linalg.norm(v)
        matrix=scale*np.array([[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]])
        offset=pf-matrix@sf;inverse=np.linalg.inv(matrix);translation=-inverse@offset
        warped=source.transform(photo.size,Image.Transform.AFFINE,(*inverse[0],translation[0],*inverse[1],translation[1]),Image.Resampling.BICUBIC)
        mask=np.array(warped.getchannel('A'))>200;ppm=np.linalg.norm(w)/picks['wheelbase'];measure=[]
        for label,x,y in picks['top']:
            xx,yy=round(x*factor),round(y*factor);ys=np.nonzero(np.any(mask[:,xx-1:xx+2],axis=1))[0]
            if len(ys):measure.append(dict(feature=label,signed_deviation_m=(yy-int(ys[0]))/ppm,photo_pixel=[xx,yy],render_pixel=[xx,int(ys[0])],axis='height'))
        for label,x,y,front in picks['ends']:
            xx,yy=round(x*factor),round(y*factor);xs=np.nonzero(np.any(mask[yy-1:yy+2,:],axis=0))[0]
            if len(xs):
                rx=int(xs[0] if front else xs[-1]);measure.append(dict(feature=label,signed_deviation_m=(xx-rx if front else rx-xx)/ppm,photo_pixel=[xx,yy],render_pixel=[rx,yy],axis='outward'))
        tint=Image.new('RGBA',photo.size,(20,112,205,0));tint.putalpha(warped.getchannel('A').point(lambda v:round(v*.38)));photo.alpha_composite(tint)
        im=photo.convert('RGB');d=ImageDraw.Draw(im)
        d.text((25,25),'H120 / '+make.upper()+' / wheelbase-registered profile',font=font(29),fill=(25,55,75))
        d.text((25,70),'Axles only set scale and level. Near-profile photograph retains perspective; no outline fit.',font=font(22),fill=(25,55,75))
        for row in measure:
            q,r=row['photo_pixel'],row['render_pixel'];d.line((*q,*r),fill=(210,60,25),width=3);d.ellipse((q[0]-4,q[1]-4,q[0]+4,q[1]+4),fill=(210,60,25))
        save(im,out/('side-overlay-'+make+'.jpg'))
        records[make]=dict(method='Wheelbase similarity transform; held-out silhouette picks, no fitted outline',reference='refs/hatch-'+make+'-side.jpg',wheelbase_m=picks['wheelbase'],pixels_per_m=ppm,rotation_degrees=math.degrees(angle),pick_uncertainty_m=4*factor/ppm,measurements=measure,worst_absolute_deviation_m=max(abs(r['signed_deviation_m']) for r in measure),caveat='Stock side photo has finite perspective. OEM brochure elevations are also raster perspective illustrations; numerical dimensions take precedence. Raw errors are retained, not corrected to pass.')
    (out/'side-overlays.json').write_text(json.dumps(records,indent=2))

def sections(out,report,photo_angle):
    for record in report['sections']:
        if record['name']=='centerline':continue
        im=Image.new('RGB',(1000,850),(240,241,239));d=ImageDraw.Draw(im);scale=365
        def project(p):return (500+p[0]*scale,745-p[1]*scale)
        for z in [0,.25,.5,.75,1,1.25,1.5]:
            a=project([-1.1,z]);b=project([1.1,z]);d.line((*a,*b),fill=(215,219,217));d.text((30,a[1]-12),f'{z:.2f} m',font=font(16),fill=(80,90,85))
        d.line((500,160,500,745),fill=(185,193,188),width=1)
        for a,b in record['segments_xz_m']:d.line((*project(a),*project(b)),fill=(35,64,81),width=2)
        d.text((30,20),record['name'].replace('_',' ').upper()+f" / y = {record['y_m']:.3f} m",font=font(28),fill=(30,43,50))
        d.text((30,65),'Actual triangle-plane intersections, including sheet gauge and glass.',font=font(19),fill=(55,70,75))
        if 'tumblehome_degrees' in record:
            low,high=record['tumblehome_samples_m'];d.line((*project(low),*project(high)),fill=(210,65,25),width=4)
            for angle in [20,25]:
                top=[low[0]-(high[1]-low[1])*math.tan(math.radians(angle)),high[1]]
                d.line((*project(low),*project(top)),fill=(45,145,90),width=2)
            d.text((30,105),f"Mesh {record['tumblehome_degrees']:.2f} deg / brief range 20-25 deg",font=font(21),fill=(120,60,35))
            d.text((30,135),'Green: requested 20-25 deg range. Orange: measured evaluated section.',font=font(18),fill=(55,70,75))
        else:
            caption=('Door section: progressive lower crown, die hollow and recessed sill.' if record['name'].startswith('mid_') else
                     'The axle station cuts the fenders; full-height side glass exists at the B-pillar.')
            d.text((30,105),caption,font=font(18),fill=(55,70,75))
        save(im,out/('section-'+record['name']+'.jpg'))

def centerline(out,report):
    record=next(r for r in report['sections'] if r['name']=='centerline')
    im=Image.new('RGB',(1700,750),(240,241,239));d=ImageDraw.Draw(im);scale=305
    def project(p):return (850+p[0]*scale,640-p[1]*scale)
    for z in [0,.25,.5,.75,1,1.25,1.5]:
        a,b=project([-2.55,z]),project([2.55,z]);d.line((*a,*b),fill=(215,219,217));d.text((15,a[1]-12),f'{z:.2f} m',font=font(16),fill=(70,85,80))
    for a,b in record['segments_yz_m']:d.line((*project(a),*project(b)),fill=(35,64,81),width=2)
    f,r=report['end_measurements']['front'],report['end_measurements']['rear']
    d.text((30,20),'CENTERLINE +1 MM / ACTUAL TRIANGLE CUT / FRONT LEFT',font=font(28),fill=(30,43,50))
    d.text((70,690),f"Windshield {report['a_pillar_rake_from_vertical_degrees']:.2f} deg / backlight {r['backlight_rake_from_vertical_degrees']:.2f} deg from vertical / hood rise {f['hood_rise_degrees']:.1f} deg",font=font(23),fill=(35,64,81))
    save(im,out/'section-centerline.jpg')


def rear_references(out,report):
    records={}
    # Horizontal widths projected in each rear photograph. Perspective and
    # different surface depths limit these to class estimates, +/-30 mm.
    definitions={
      'corolla':dict(width=1.790,body=(234,962),top=(376,829,257),base=(350,851,345),pillar=(300,350,345)),
      'hyundai':dict(width=1.795,body=(232,968),top=(365,836,255),base=(316,884,336),pillar=(280,316,336))}
    for make,row in definitions.items():
        im=Image.open(ASSET/('refs/hatch-'+make+'-back.jpg')).convert('RGB');d=ImageDraw.Draw(im);factor=im.width/1200
        ppm=(row['body'][1]-row['body'][0])/row['width'];measure={}
        for key,color in [('top',(25,120,180)),('base',(25,120,180)),('pillar',(200,65,25))]:
            x1,x2,y=row[key];d.line((x1*factor,y*factor,x2*factor,y*factor),fill=color,width=5);measure[key+'_width_m']=(x2-x1)/ppm
        d.text((25,25),make.upper()+' / projected rear glazing widths / +/-30 mm',font=font(28),fill=(30,50,65))
        d.text((25,70),'Neutral: white studio background, unit RGB gains. No photographic texel enters the model.',font=font(21),fill=(30,50,65))
        save(im,out/('rear-reference-'+make+'.jpg'));records[make]=dict(measure,picks_preview_pixels=row,uncertainty_m=.030)
        left=rgb(out/'rear.png');right=im;left.thumbnail((1100,820));right.thumbnail((1100,820))
        pair=Image.new('RGB',(2240,920),(229,231,232));pair.paste(left,((1100-left.width)//2,80));pair.paste(right,(1120+(1100-right.width)//2,80));dd=ImageDraw.Draw(pair)
        dd.text((20,20),'H120 ORTHOGRAPHIC REAR / '+make.upper()+' PHOTO / unregistered form comparison',font=font(26),fill=(25,45,60));save(pair,out/('rear-comparison-'+make+'.jpg'))
    records['H120']=report['end_measurements']['rear'];(out/'rear-reference-measurements.json').write_text(json.dumps(records,indent=2))

def dimensioned(out,shots,report):
    for name in ['side','front','rear','top']:
        im=rgb(out/(name+'.png'));d=ImageDraw.Draw(im);points=shots[name]['points'];w,h=im.size
        def line(a,b,y,text):
            x1,x2=sorted((points[a][0],points[b][0]));d.line((x1,y,x2,y),fill=(25,83,113),width=2)
            for x in [x1,x2]:d.line((x,y-7,x,y+7),fill=(25,83,113),width=2)
            box=d.textbbox((0,0),text,font=font(18));d.text(((x1+x2-box[2])/2,y-27),text,font=font(18),fill=(25,83,113))
        d.text((22,18),'ALDER H120 / '+name.upper()+' / SOURCE FORM',font=font(25),fill=(30,45,55))
        d.text((22,53),'Targets below; independent surface measurements are in form-check.json.',font=font(17),fill=(60,75,85))
        if name in ['side','top']:line('front','rear',h-28,'4360 mm length / Toyota 4370, Hyundai 4340 mm')
        if name=='side':
            line('front_axle','rear_axle',h-78,'2650 mm wheelbase / Toyota 2640, Hyundai 2650 mm')
            d.text((w-290,h//2),f"Roof {report['bounds_m']['size'][2]*1000:.1f} mm",font=font(19),fill=(25,83,113))
            d.text((25,h-115),f"Measured overhangs {report['overhangs_m']['front']*1000:.0f} / {report['overhangs_m']['rear']*1000:.0f} mm (front / rear)",font=font(18),fill=(25,83,113))
        if name=='top':
            f,r=report['end_measurements']['front'],report['end_measurements']['rear']
            d.text((25,h-80),f"Actual bumper-height sweep at x=800 mm: front {f['plan_sweep_at_800mm_m']*1000:.0f} / rear {r['plan_sweep_at_800mm_m']*1000:.0f} mm",font=font(18),fill=(25,83,113))
        if name in ['front','rear']:line('left','right',h-28,'1795 mm body / Toyota 1790, Hyundai 1795 mm')
        save(im,out/(name+'-dimensions.jpg'))

def main():
    p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--report',required=True);p.add_argument('--cameras',required=True);a=p.parse_args()
    out=Path(a.renders);shots=json.loads((out/'shots.json').read_text());report=json.loads(Path(a.report).read_text());cameras=json.loads(Path(a.cameras).read_text())
    if any(s['source_sha256']!=report['source_sha256'] for s in shots.values()):raise ValueError('Mixed source revisions')
    tone={}
    for name,shot in shots.items():
        path=out/(name+'.png');im=Image.open(path).convert('RGBA');arr=np.array(im);valid=arr[...,3]>250;cols=arr[...,:3][valid];luma=cols@np.array([.2126,.7152,.0722])
        tone[name]=dict(display_luma_p1_p50_p99=np.percentile(luma,[1,50,99]).tolist(),channel_255_fraction=float(np.mean(cols.max(axis=1)==255)),deep_shadow_below_25=float(np.mean(luma<25)))
        save(rgb(path),out/(name+'.jpg'))
    (out/'tonal-range.json').write_text(json.dumps(dict(scope='Opaque foreground only; neutral source clay, no factory-paint albedo claim',views=tone),indent=2))
    sections(out,report,22.5);centerline(out,report);dimensioned(out,shots,report);side_overlay(out,shots);rear_references(out,report)
    from hatch_profiles import profiles
    profiles(out,cameras)
    from kit.photo_match import compose
    clay={name+'_clay':dict(data,title=data['title'].replace('clay with stripes','neutral clay')) for name,data in cameras.items()}
    calibration=out/'clay-cameras.json';calibration.write_text(json.dumps(clay,indent=2));compose(calibration,out,out)
    front,rear=[rgb(out/(name+'-dimensions.jpg')) for name in ['front','rear']]
    pair=Image.new('RGB',(front.width+rear.width,max(front.height,rear.height)),(229,231,232));pair.paste(front,(0,0));pair.paste(rear,(front.width,0));save(pair,out/'front-rear.jpg')
    names=['front_three_quarter.jpg','rear_three_quarter.jpg','side-dimensions.jpg','front-dimensions.jpg','rear-dimensions.jpg','front-rear.jpg','top-dimensions.jpg','side_raking.jpg','side-overlay-corolla.jpg','side-overlay-hyundai.jpg',
       'stripes_horizontal.jpg','stripes_vertical.jpg','stripes_rear_horizontal.jpg','stripes_rear_vertical.jpg',
       'stripes_side_horizontal.jpg','stripes_side_vertical.jpg','stripes_hood_driver.jpg','curvature-body.jpg','curvature-hood-roof.jpg',
       'section-front_axle.jpg','section-b_pillar.jpg','section-rear_axle.jpg','section-mid_front_door.jpg','section-mid_rear_door.jpg','section-centerline.jpg','rear-reference-corolla.jpg','rear-reference-hyundai.jpg','rear-comparison-corolla.jpg','rear-comparison-hyundai.jpg']
    names += [name+'-pair.jpg' for name in cameras]
    names += [name+'_clay-pair.jpg' for name in cameras]
    names += [name+'-calibration.jpg' for name in cameras]
    names += ['side-perspective-'+make+'.jpg' for make in ['corolla','hyundai']]
    names += ['side-methods-'+make+'.jpg' for make in ['corolla','hyundai']]
    names += ['side-rounds-'+make+'.jpg' for make in ['corolla','hyundai']]
    tw,th=800,530;canvas=Image.new('RGB',(3*tw,math.ceil(len(names)/3)*th),(229,231,232));d=ImageDraw.Draw(canvas)
    for i,name in enumerate(names):
        im=Image.open(out/name).convert('RGB');im.thumbnail((tw-20,th-55),Image.Resampling.LANCZOS);x=(i%3)*tw;y=(i//3)*th
        canvas.paste(im,(x+(tw-im.width)//2,y+45+(th-55-im.height)//2));d.text((x+15,y+10),name,font=font(20),fill=(35,50,55))
    save(canvas,out/'contact.jpg')
    print('HATCH FORM REVIEW',out/'contact.jpg',len(names),'views; measured sections, tone, overlay and photo estimate')
if __name__=='__main__':main()
