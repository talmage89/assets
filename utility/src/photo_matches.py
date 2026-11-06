"""Type comparisons: measured photo pixels, estimated original street cameras.

Photographic poles are not surveyed. 40-ft poles / typical level grade set the
working scale; absolute camera distance and lens remain estimates. No private
home plan or image is traced into any asset.
"""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]


def meta(seed):return json.loads(Path(f'build/street-{seed}.json').read_text())


# Cloud neutrals are approximate daylight assumptions, not calibrated cards.
# The shaded porcelain candidate was rejected; it is not a reliable neutral. These inspection copies never enter the material pipeline.
def balance_photos():
    from PIL import Image
    import numpy as np
    from kit.image_io import srgb_to_linear,linear_to_srgb
    out=Path('build/reference-balance');out.mkdir(parents=True,exist_ok=True);rows={}
    for name,roi in {'residential-a':(20,95,55,120),'residential-b':(2150,330,2220,380),'hardware':None}.items():
        src=Path('refs')/(name+'.jpg');rgb=np.asarray(Image.open(src).convert('RGB'),dtype=np.float32)/255
        linear=srgb_to_linear(rgb)
        if roi:
            x0,y0,x1,y1=roi;med=np.median(linear[y0:y1,x0:x1].reshape(-1,3),axis=0);gains=float(np.mean(med))/med
        else:gains=np.ones(3)
        encoded=np.clip(linear_to_srgb(linear*gains),0,1)
        Image.fromarray(np.uint8(encoded*255+.5)).save(out/src.name,quality=97)
        rows[name]=dict(original=str(src),roi=roi,assumed_neutral='none accepted; original WB retained, geometry/contrast only' if name=='hardware' else 'achromatic cloud; approximate daylight white point, no gray card',linear_gains=gains.tolist())
    (out/'balance.json').write_text(json.dumps(rows,indent=2))


a=meta(104);b=meta(101)
def pole(m,i,key):return m['sockets']['P'+str(i)][key]
def base(m,i):return m['plan']['poles'][i]['location']
def anchor(world,pixel,weight=1):return dict(world=world,pixel=pixel,weight=weight)
MATCHES=dict(
 nc_street=dict(seed=104,title='Residential NC / vertical three-phase construction, 2009',photo='refs/residential-a.jpg',crop=(0,0,1074,484),
   location=(8,-6,1.85),target=(-3,85,5.5),lens=35,lens_bounds_mm=(25,65),camera_height_m=(1.85,.10),
   landmarks=[anchor(base(a,1),(281,280),2),anchor(pole(a,1,'Primary_A'),(272,127),2),
      anchor(pole(a,1,'Primary_B'),(267,140)),anchor(pole(a,1,'Primary_C'),(280,155)),
      anchor(pole(a,1,'Neutral'),(280,179)),anchor(base(a,2),(300,264)),
      anchor(pole(a,2,'Primary_A'),(294,171)),anchor(pole(a,3,'Primary_A'),(307,198))]),
 md_top={'seed': 101, 'title': 'Transformer pole top / Maryland / shaft and crossarm fit', 'photo': 'refs/residential-b.jpg', 'crop': [880, 180, 1280, 640], 'location': [-17, 29, 1.85], 'target': [-5.05, 42, 9.4], 'lens': 100, 'lens_bounds_mm': [35, 280], 'camera_height_m': [1.85, 0.2], 'landmarks': [{'world': [-6.025360107421875, 43.15403747558594, 10.170839309692383], 'pixel': [979, 226], 'weight': 2}, {'world': [-4.074640274047852, 43.15403747558594, 10.170839309692383], 'pixel': [1111, 309], 'weight': 2}, {'world': [-5.05, 42.94903390385878, 10.530840000000001], 'pixel': [1060, 250], 'weight': 2}, {'world': [-5.05, 42.94903390385878, 9.93084], 'pixel': [1060, 288], 'weight': 2}]},
 comm_space=dict(seed=101,title='Communications / full shaft and arm camera fit',photo='refs/hardware.jpg',crop=(0,0,749,1640),
   location=(-11,70,1.85),target=(-5.05,84,6.5),lens=85,lens_bounds_mm=(18,220),camera_height_m=(1.85,.15),
   landmarks=[anchor(base(b,2),(386,1530)),
      anchor([base(b,2)[0],base(b,2)[1],base(b,2)[2]+b['plan']['poles'][2]['height']],(344,219)),
      anchor(pole(b,2,'Primary_B'),(212,238)),anchor(pole(b,2,'Primary_C'),(452,291))]),

)


def crop_pair(calibration,folder,out):
    """A native review crop of the verified full portrait; no camera refit."""
    from PIL import Image,ImageDraw
    from kit.photo_match import project
    import numpy as np,math
    data=json.loads(Path(calibration).read_text());row=data['comm_space'];folder=Path(folder)
    path=folder/'comm_space.png';im=Image.open(path);assert im.size==(749,1640),im.size
    im.save(folder/'comm_space-full.png');box=(90,500,660,870);im.crop(box).save(path)
    row['full_frame_control_fit']=dict(crop=row['crop'],rms_px=row['residual_rms_pixels'],note='Four controls on full shaft and upper arm, not local arbitrary shaft stations')
    sh=row['shot'];d=np.array(sh['target'])-np.array(sh['location']);pars=[math.atan2(d[1],d[0]),math.atan2(d[2],np.linalg.norm(d[:2])),*sh['location'],math.log(sh['lens']),sh['roll']]
    point=[base(b,2)[0],base(b,2)[1],pole(b,2,'TelephoneStrand')[2]]
    uv=project(pars,np.array([point]),749,1640)[0][0];observed=np.array([356,676])
    audit=Image.open(row['photo']).convert('RGB');draw=ImageDraw.Draw(audit)
    for observed_control,predicted_control in zip(row['measured_pixels'],row['projected_pixels']):
        x,y=observed_control;draw.ellipse((x-4,y-4,x+4,y+4),outline='lime',width=2)
        x,y=predicted_control;draw.line((x-4,y,x+4,y),fill='red',width=2);draw.line((x,y-4,x,y+4),fill='red',width=2)
    x,y=observed;draw.ellipse((x-4,y-4,x+4,y+4),outline='orange',width=2);draw.line((*observed,*uv),fill='red',width=2)
    audit.save(folder/'comm_space-full-calibration.jpg',quality=96)
    audit.crop(box).save(folder/'comm_space-heldout-calibration.jpg',quality=96)
    row['held_out_communication_height']=dict(world=point,observed_photo_px=observed.tolist(),projected_photo_px=uv.tolist(),error_px=float(np.linalg.norm(uv-observed)),note='Shaft centre at telephone strand height; photo assumed class-4 40-ft pole, not a survey')
    row['crop']=box
    for k in ('projected_pixels','measured_pixels'):row[k]=(np.array(row[k])-np.array(box[:2])).tolist()
    row['title']+=' / native crop'
    receipt=folder/'provenance.json';r=json.loads(receipt.read_text());r['comm_space']['post_crop']=dict(native_full_pixels=list(im.size),crop=box,full_render='comm_space-full.png');receipt.write_text(json.dumps(r,indent=2))
    Path(out).write_text(json.dumps(data,indent=2));print('FULL-CAMERA COMMUNICATIONS',row['full_frame_control_fit'],'HELD OUT',row['held_out_communication_height'])


if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--crop':crop_pair(*sys.argv[2:])
    else:
        from kit.photo_match import solve
        balance_photos()
        out=sys.argv[1] if len(sys.argv)>1 else 'build/matched-cameras.json'
        solve(__file__,out);results=json.loads(Path(out).read_text())
        for name,row in results.items():
            row['seed']=MATCHES[name]['seed']
            lighting=dict(nc_street=dict(sun_direction=(-.8,.2,-.8),sun_energy=3.6,sky_strength=.15,exposure=-.2),
                          md_top=dict(sun_direction=(-.4,-.6,-1),sun_energy=1.1,sky_strength=.17,sky_saturation=.3,sun_angle=7,aerosol=1.4,exposure=-.15),
                          comm_space=dict(sun_direction=(.8,-.4,-1),sun_energy=3.5,sky_strength=.15,exposure=-.2,width_px=749))
            row['shot'].update(lighting[name])
        Path(out).write_text(json.dumps(results,indent=2))
