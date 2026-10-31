"""Dimensioned source evidence and photo comparisons. Writes no docs assets."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.fonts import find_font
import sedan_spec as S
ASSET=Path(__file__).resolve().parents[1]
FONT=find_font('Noto Sans','Regular')
def font(size):return ImageFont.truetype(FONT,size)
def rgb(path):
    im=Image.open(path).convert('RGBA');bg=Image.new('RGBA',im.size,(229,231,232,255));bg.alpha_composite(im);return bg.convert('RGB')
def save(im,path):im.save(path,quality=93,optimize=True)

def side_overlay(out,shots):
    source=Image.open(out/'side.png').convert('RGBA');photo=Image.open(ASSET/'refs/sedan-camry-side.jpg').convert('RGBA')
    data=shots['side'];sf=np.array(data['points']['front_axle']);sr=np.array(data['points']['rear_axle'])
    pf=np.array([238,541])*1.75;pr=np.array([924,540])*1.75
    v=sr-sf;w=pr-pf;theta=math.atan2(w[1],w[0])-math.atan2(v[1],v[0]);scale=np.linalg.norm(w)/np.linalg.norm(v)
    matrix=scale*np.array([[math.cos(theta),-math.sin(theta)],[math.sin(theta),math.cos(theta)]])
    offset=pf-matrix@sf;inverse=np.linalg.inv(matrix);translation=-inverse@offset
    warped=source.transform(photo.size,Image.Transform.AFFINE,(*inverse[0],translation[0],*inverse[1],translation[1]),Image.Resampling.BICUBIC)
    tint=Image.new('RGBA',photo.size,(20,112,205,0));tint.putalpha(warped.getchannel('A').point(lambda v:round(v*.45)));photo.alpha_composite(tint)
    im=photo.convert('RGB');d=ImageDraw.Draw(im)
    d.text((35,35),'S240 / 45% rendered silhouette over Camry SE profile',font=font(29),fill=(25,55,75))
    d.text((35,82),'Wheel centers alone set scale/level. Camry 2824.48 mm wheelbase; model 2830 mm (+0.20%).',font=font(22),fill=(25,55,75))
    for x,y in [pf,pr]:d.ellipse((x-7,y-7,x+7,y+7),outline=(20,80,180),width=3)
    save(im,out/'side-overlay.jpg')
    ppm=np.linalg.norm(w)/2.82448;mask=np.array(warped.getchannel('A'))>200;measure=[]
    for label,x,y in [('hood lead',70,440),('hood mid',170,409),('cowl',330,385),('roof front',550,286),('roof peak',670,273),('roof aft',800,284),('deck',1090,349)]:
        xx,yy=round(x*1.75),round(y*1.75);ys=np.nonzero(np.any(mask[:,xx-1:xx+2],axis=1))[0]
        if len(ys):measure.append(dict(feature=label,render_minus_photo_height_m=(yy-int(ys[0]))/ppm,photo_pixel=[xx,yy],pick_uncertainty_m=4*1.75/ppm))
    record=dict(method='Two inspected wheel centers only; similarity transform, no outline fit',reference='refs/sedan-camry-side.jpg',wheelbase_reference_m=2.82448,
       original_pixels_per_m=ppm,rotation_degrees=math.degrees(theta),scale=scale,offset_pixels=offset.tolist(),silhouette_differences=measure,
       caveat='Corrected front/rear overhangs; OEM metric front reference 975 mm. Reference is near-profile with residual perspective; outline picks +/-4 preview pixels.')
    (out/'side-overlay.json').write_text(json.dumps(record,indent=2))

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
            d.text((30,105),f"Mesh {record['tumblehome_degrees']:.2f} deg / class photo estimate {photo_angle:.2f} deg (+/-4.5)",font=font(21),fill=(120,60,35))
            d.text((30,135),'Green: requested 20-25 deg range. Orange: measured evaluated section.',font=font(18),fill=(55,70,75))
        else:
            d.text((30,105),'The axle station cuts hood/deck; full-height side glass exists at the B-pillar.',font=font(18),fill=(55,70,75))
        save(im,out/('section-'+record['name']+'.jpg'))

def centerline(out,report):
    record=next(r for r in report['sections'] if r['name']=='centerline')
    im=Image.new('RGB',(1700,750),(240,241,239));d=ImageDraw.Draw(im);scale=305
    def project(p):return (850+p[0]*scale,640-p[1]*scale)
    for z in [0,.25,.5,.75,1,1.25,1.5]:
        a,b=project([-2.55,z]),project([2.55,z]);d.line((*a,*b),fill=(215,219,217));d.text((15,a[1]-12),f'{z:.2f} m',font=font(16),fill=(70,85,80))
    for a,b in record['segments_yz_m']:d.line((*project(a),*project(b)),fill=(35,64,81),width=2)
    f,r=report['end_measurements']['front'],report['end_measurements']['rear']
    marks=[('Bumper',f['bumper_leading_m']),('Hood edge',f['hood_edge_m']),('Chin',f['chin_m']),('Cowl',f['cowl_m']),
           ('Deck lip',r['deck_trailing_edge_m']),('Rear bumper',r['bumper_rearmost_m']),('Diffuser',r['diffuser_m'])]
    for i,(name,p) in enumerate(marks):
        xy=project([p[1],p[2]]);d.ellipse((xy[0]-4,xy[1]-4,xy[0]+4,xy[1]+4),fill=(205,70,30))
        text=f'{name}: y {p[1]*1000:.0f}, z {p[2]*1000:.0f} mm'
        xx=75 if i<4 else 1130;yy=90+(i if i<4 else i-4)*38
        d.line((*xy,xx,yy+12),fill=(175,155,130),width=1);d.text((xx,yy),text,font=font(18),fill=(110,60,35))
    d.text((30,20),'CENTERLINE / ACTUAL MESH CUT / FRONT LEFT',font=font(28),fill=(30,43,50))
    d.text((70,690),f"Front face {f['upper_face_degrees_from_vertical']:.1f} deg / hood rise {f['hood_rise_degrees']:.1f} deg / rear lean {r['upper_panel_degrees_from_vertical']:.1f} deg / deck {r['deck_length_m']*1000:.0f} mm",font=font(23),fill=(35,64,81))
    save(im,out/'section-centerline.jpg')


def photo_section(out,cameras):
    data=cameras['accord_front'];shot=data['shot'];cam=np.array(shot['location']);fw=np.array(shot['target'])-cam;fw/=np.linalg.norm(fw)
    right=np.cross(fw,[0,0,1]);right/=np.linalg.norm(right);up=np.cross(right,fw);roll=shot['roll']
    right,up=right*np.cos(roll)+up*np.sin(roll),up*np.cos(roll)-right*np.sin(roll)
    def unproject(xy,y=S.DOOR_SPLIT):
        uv=np.array(xy)*1.75-np.array(data['crop'][:2]);w=data['crop'][2]-data['crop'][0];h=data['crop'][3]-data['crop'][1];f=w*shot['lens']/36
        ray=fw+(uv[0]-w/2)/f*right-(uv[1]-h/2)/f*up
        return cam+ray*(y-cam[1])/ray[1]
    picks=[(905,207),(948,322)];upper,lower=[unproject(p) for p in picks]
    angle=math.degrees(math.atan2(abs(lower[0]-upper[0]),upper[2]-lower[2]))
    im=Image.open(ASSET/'refs/sedan-accord-front.jpg').convert('RGB');d=ImageDraw.Draw(im);xy=[tuple(1.75*v for v in p) for p in picks]
    d.line((*xy[0],*xy[1]),fill=(230,65,15),width=5)
    for x,y in xy:d.ellipse((x-8,y-8,x+8,y+8),outline=(230,65,15),width=4)
    d.text((35,35),f'B-PILLAR SECTION ESTIMATE / {angle:.2f} deg from vertical, +/-4.5 deg',font=font(29),fill=(40,50,55))
    d.text((35,80),f'Calibrated rays intersect y={S.DOOR_SPLIT:.2f} m. Assumes locally upright B-pillar; picks +/-4 preview pixels.',font=font(22),fill=(40,50,55))
    d.text((35,117),'White balance: neutral white backdrop (unit RGB gains). This is an estimate, not an OEM section drawing.',font=font(21),fill=(40,50,55))
    save(im,out/'photo-tumblehome.jpg')
    row=dict(estimate_degrees=angle,uncertainty_degrees=4.5,photo_pixels_original=xy,backprojected_points_m=[upper.tolist(),lower.tolist()],
        method='Kit camera rays intersect original-design B-pillar plane at y=0.20 m; photographic class estimate only',
        assumptions=['B-pillar locally upright in Y; up to 40 mm unmeasured rake','+/-4 preview pixel picks','chassis camera registration; different styling'],white_balance_neutral='white studio backdrop, unit gains')
    (out/'photo-tumblehome.json').write_text(json.dumps(row,indent=2));return angle

def dimensioned(out,shots,report):
    for name in ['side','front','top']:
        im=rgb(out/(name+'.png'));d=ImageDraw.Draw(im);points=shots[name]['points'];w,h=im.size
        def line(a,b,y,text):
            x1,x2=sorted((points[a][0],points[b][0]));d.line((x1,y,x2,y),fill=(25,83,113),width=2)
            for x in [x1,x2]:d.line((x,y-7,x,y+7),fill=(25,83,113),width=2)
            box=d.textbbox((0,0),text,font=font(18));d.text(((x1+x2-box[2])/2,y-27),text,font=font(18),fill=(25,83,113))
        d.text((22,18),'ALDER S240 / '+name.upper()+' / SOURCE FORM',font=font(25),fill=(30,45,55))
        d.text((22,53),'Targets below; independent surface measurements are in form-check.json.',font=font(17),fill=(60,75,85))
        if name in ['side','top']:line('front','rear',h-28,'4900 mm length / class 4882-4895 mm')
        if name=='side':
            line('front_axle','rear_axle',h-78,'2830 mm wheelbase / Honda 2830, Toyota 2824.48 mm')
            d.text((w-290,h//2),f"Roof {report['bounds_m']['size'][2]*1000:.1f} mm",font=font(19),fill=(25,83,113))
            d.text((25,h-115),f"Measured overhangs {report['overhangs_m']['front']*1000:.0f} / {report['overhangs_m']['rear']*1000:.0f} mm (front / rear)",font=font(18),fill=(25,83,113))
        if name=='top':
            f,r=report['end_measurements']['front'],report['end_measurements']['rear']
            d.text((25,h-80),f"Actual bumper-height sweep at x=850 mm: front {f['plan_sweep_at_850mm_m']*1000:.0f} / rear {r['plan_sweep_at_850mm_m']*1000:.0f} mm",font=font(18),fill=(25,83,113))
        if name=='front':line('left','right',h-28,'1850 mm body / class 1839-1862 mm')
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
    angle=photo_section(out,cameras);sections(out,report,angle);centerline(out,report);dimensioned(out,shots,report);side_overlay(out,shots)
    from kit.photo_match import compose
    clay={name+'_clay':dict(data,title=data['title'].replace('clay with stripes','neutral clay')) for name,data in cameras.items()}
    calibration=out/'clay-cameras.json';calibration.write_text(json.dumps(clay,indent=2));compose(calibration,out,out)
    names=['front_three_quarter.jpg','rear_three_quarter.jpg','side-dimensions.jpg','front-dimensions.jpg','top-dimensions.jpg','side-overlay.jpg',
       'stripes_horizontal.jpg','stripes_vertical.jpg','stripes_rear_horizontal.jpg','stripes_rear_vertical.jpg',
       'stripes_side_horizontal.jpg','stripes_side_vertical.jpg','stripes_hood_driver.jpg','curvature-body.jpg','curvature-hood-deck.jpg',
       'section-front_axle.jpg','section-b_pillar.jpg','section-rear_axle.jpg','section-centerline.jpg','photo-tumblehome.jpg']
    names += [name+'-pair.jpg' for name in cameras]
    names += [name+'_clay-pair.jpg' for name in cameras]
    names += [name+'-calibration.jpg' for name in cameras]
    tw,th=800,530;canvas=Image.new('RGB',(3*tw,math.ceil(len(names)/3)*th),(229,231,232));d=ImageDraw.Draw(canvas)
    for i,name in enumerate(names):
        im=Image.open(out/name).convert('RGB');im.thumbnail((tw-20,th-55),Image.Resampling.LANCZOS);x=(i%3)*tw;y=(i//3)*th
        canvas.paste(im,(x+(tw-im.width)//2,y+45+(th-55-im.height)//2));d.text((x+15,y+10),name,font=font(20),fill=(35,50,55))
    save(canvas,out/'contact.jpg')
    print('SEDAN FORM REVIEW',out/'contact.jpg',len(names),'views; measured sections, tone, overlay and photo estimate')
if __name__=='__main__':main()
