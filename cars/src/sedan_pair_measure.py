"""White balance and held-out display measurements for used-class photo pairs.

Photographs enter only this review script. They never enter modeling, baking,
materials or the lighting graph. Values are appearance comparisons, not albedo.
"""
import argparse,json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageOps,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.photo_match import project
from kit.fonts import find_font

def linear(rgb):return np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
def srgb(rgb):return np.where(rgb<=.0031308,rgb*12.92,1.055*np.maximum(rgb,0)**(1/2.4)-.055)
def balance(calibration,out):
    data=json.loads(Path(calibration).read_text());folder=Path(out).parent/'balanced-references';folder.mkdir(parents=True,exist_ok=True)
    for name,row in data.items():
        im=ImageOps.exif_transpose(Image.open(row['photo'])).convert('RGB');arr=np.asarray(im)/255.
        if 'front' in name:box=[1030,15,1100,35];neutral='assumed neutral off-white exterior plaster at upper right'
        else:box=[1095,103,1110,112];neutral='assumed neutral white paint on the background car upper trunk; stained curb rejected'
        factor=im.width/1200;box=[round(v*factor) for v in box];x0,y0,x1,y1=box
        median=np.median(linear(arr[y0:y1,x0:x1]).reshape(-1,3),axis=0);target=median@np.array([.2126,.7152,.0722]);gain=target/np.maximum(median,1e-5)
        result=np.clip(srgb(np.clip(linear(arr)*gain,0,1)),0,1)
        photo=(folder/(name+'.png')).resolve();Image.fromarray(np.uint8(np.round(result*255))).save(photo)
        row['unbalanced_photo']=row['photo'];row['photo']=str(photo)
        row['reference_white_balance']=dict(neutral=neutral,patch_original_pixels=box,median_linear_rgb=median.tolist(),linear_channel_gains=gain.tolist(),limitation='Assumed neutral, not a photographed gray card; reflected surroundings remain colored')
    Path(out).write_text(json.dumps(data,indent=2))

def measure(calibration,renders,out):
    data=json.loads(Path(calibration).read_text());result={}
    for name,row in data.items():
        photo=Image.open(row['photo']).convert('RGB').crop(row['crop']);render=Image.open(Path(renders)/(name+'.png')).convert('RGB')
        shot=row['shot'];cam=np.array(shot['location']);fw=np.array(shot['target'])-cam;fw/=np.linalg.norm(fw)
        parameters=[math.atan2(fw[1],fw[0]),math.asin(fw[2]),*cam,math.log(shot['lens']),shot.get('roll',0)]
        metadata=json.loads((Path(renders)/'shots.json').read_text())[name]
        patches=metadata['appearance_points']
        records={}
        for label,point in patches.items():
            p=point['world_m']
            uv=project(np.array(parameters),np.array([p]),photo.width,photo.height)[0][0];radius=photo.width*.0065
            samples={}
            for key,im in [('reference',photo),('render',render)]:
                f=im.width/photo.width;x,y=point['render_pixel'] if key=='render' else uv;r=radius*f
                if key=='reference':x,y=uv
                box=[round(x-r),round(y-r),round(x+r),round(y+r)]
                values=np.asarray(im.crop(box))/255.;median=np.median(values.reshape(-1,3),axis=0)
                samples[key]=dict(display_rgb=(median*255).tolist(),display_luma=float(median@np.array([.2126,.7152,.0722])*255),rectangle_pixels=box)
            records[label]=dict(world_m=p,**samples,render_minus_reference_luma=samples['render']['display_luma']-samples['reference']['display_luma'])
        # Audit the patch locations on both images; source photos remain
        # confined to ignored review products and never reach the asset graph.
        panel_width=render.width;panel_height=render.height
        annotated=Image.new('RGB',(panel_width*2,panel_height+90),(238,239,236))
        for column,(key,im) in enumerate([('render',render),('reference',photo)]):
            annotated.paste(im.resize(render.size,Image.Resampling.LANCZOS),(column*panel_width,0))
        draw=ImageDraw.Draw(annotated);font=ImageFont.truetype(find_font('Noto Sans','Regular'),14)
        for index,(label,record) in enumerate(records.items(),1):
            for column,key in enumerate(['render','reference']):
                f=panel_width/(render.width if key=='render' else photo.width)
                x0,y0,x1,y1=[q*f for q in record[key]['rectangle_pixels']];offset=column*panel_width
                draw.rectangle((offset+x0,y0,offset+x1,y1),outline=(240,100,20) if key=='render' else (20,180,225),width=2)
                draw.text((offset+x0,y0-17),str(index),fill=(240,100,20) if key=='render' else (20,180,225),font=font)
            text=f"{index} {label}: render {record['render']['display_luma']:.1f} / photo {record['reference']['display_luma']:.1f}"
            draw.text((12+(index-1)%3*panel_width*2/3,panel_height+10+(index-1)//3*24),text,fill=(30,40,45),font=font)
        annotated.save(Path(renders)/(name+'-patches.jpg'),quality=93,optimize=True)
        result[name]=dict(reference_white_balance=row.get('reference_white_balance'),render_white_balance='scene linear D65 display; unit gains',scope='Ray-measured original paint surface patches; calibrated photo rays approximate class correspondence, including lighting/reflection/shape differences; not material albedo',patches=records)
    Path(out).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['balance','measure']);p.add_argument('--calibration',required=True);p.add_argument('--out',required=True);p.add_argument('--renders');a=p.parse_args()
    if a.mode=='balance':balance(a.calibration,a.out)
    else:measure(a.calibration,a.renders,a.out)
