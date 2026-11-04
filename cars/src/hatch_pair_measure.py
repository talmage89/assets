"""White-balanced, display-value photo patches. Images never enter Blender."""
import argparse,json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw

REFS={
 'used_front':dict(neutral=(120,12,220,42),neutral_name='white exterior siding between the two windows, above vegetation',
   patches={'upper front door':(806,350,824,368),'front road film':(807,465,825,481),'rear door':(1010,332,1028,350),'rear road film':(1005,455,1023,469),'front glass':(853,159,871,177),'windshield':(590,165,608,183),'tire sidewall':(584,425,596,437)}),
 'used_rear':dict(neutral=(210,65,216,125),neutral_name='gray painted garage-door mullion, left of the roof',
   patches={'upper front door':(270,310,288,328),'front road film':(277,423,295,439),'rear door':(469,327,487,345),'rear road film':(477,452,495,466),'front glass':(323,158,341,176),'backlight':(918,154,936,172),'tire sidewall':(548,414,560,426)}),
}
LUMA=np.array([.2126,.7152,.0722])
def linear(v):return np.where(v<=.04045,v/12.92,((v+.055)/1.055)**2.4)
def display(v):return np.where(v<=.0031308,v*12.92,1.055*np.maximum(v,0)**(1/2.4)-.055)
def summary(a):
    flat=a.reshape(-1,3);median=np.median(flat,axis=0)
    return dict(rgb_median_255=median.tolist(),luma_median_255=float(np.median(flat@LUMA)),luma_p10_p90_255=np.percentile(flat@LUMA,[10,90]).tolist(),pixels=len(flat))


def measure(folder):
    folder=Path(folder);meta=json.loads((folder/'shots.json').read_text());reports={}
    root=Path(__file__).resolve().parents[1]
    for name,spec in REFS.items():
        original=Image.open(root/('refs/hatch-used-'+name.split('_')[1]+'.jpg')).convert('RGB')
        reference=original.resize((1200,round(original.height*1200/original.width)),Image.Resampling.LANCZOS)
        ref=np.asarray(reference,dtype=float)/255;lin=linear(ref)
        x0,y0,x1,y1=spec['neutral'];neutral=np.median(lin[y0:y1,x0:x1],axis=(0,1));gains=neutral.mean()/neutral
        balanced=np.clip(display(lin*gains),0,1)*255
        rendered_image=Image.open(folder/(name+'.png')).convert('RGBA')
        background=Image.new('RGBA',rendered_image.size,(235,237,238,255))
        render=np.asarray(Image.alpha_composite(background,rendered_image).convert('RGB'),dtype=float)
        shot=meta[name];points=shot['appearance_points'];rows=[]
        left=Image.fromarray(render.astype('uint8'));right=Image.fromarray(balanced.astype('uint8'));ld=ImageDraw.Draw(left);rd=ImageDraw.Draw(right)
        for label,rect in spec['patches'].items():
            xx0,yy0,xx1,yy1=rect;phot=summary(balanced[yy0:yy1,xx0:xx1]);cx,cy=points[label]['render_pixel'];radius=max(3,round(render.shape[1]/200))
            rx,ry=round(cx),round(cy);rrect=(rx-radius,ry-radius,rx+radius+1,ry+radius+1)
            rendered=summary(render[rrect[1]:rrect[3],rrect[0]:rrect[2]])
            ld.rectangle(rrect,outline=(255,180,30),width=2);ld.text((rx+8,ry),label,fill=(255,160,20))
            rd.rectangle(rect,outline=(255,180,30),width=2);rd.text((xx1+4,yy0),label,fill=(220,80,0))
            rows.append(dict(label=label,reference_rect_1200=list(rect),render_rect=rrect,world_patch_m=points[label]['world_m'],reference=phot,render=rendered,
                display_luma_delta_255=rendered['luma_median_255']-phot['luma_median_255']))
        rd.rectangle(spec['neutral'],outline=(20,160,230),width=2)
        canvas=Image.new('RGB',(2400,round(max(left.height,right.height)*1200/max(left.width,right.width))+50),(230,232,234))
        # Preserve each full framing in its own panel; annotation is diagnostic.
        for k,im in enumerate([left,right]):
            im=im.resize((1200,round(im.height*1200/im.width)),Image.Resampling.LANCZOS);canvas.paste(im,(1200*k,35))
        ImageDraw.Draw(canvas).text((14,12),name+' / rendered patches and white-balanced reference; displayed values, not recovered albedo',fill=(15,25,30))
        canvas.save(folder/(name+'-measured.jpg'),quality=92,optimize=True)
        reports[name]=dict(source_sha256=shot['source_sha256'],neutral=spec['neutral_name'],neutral_rect_1200=list(spec['neutral']),linear_rgb_gains=gains.tolist(),
            neutral_rgb_before_255=(np.median(ref[y0:y1,x0:x1],axis=(0,1))*255).tolist(),patches=rows,
            qualification='Class surfaces and photo pose differ. Camera RMS, patch ranges and neutral assumption remain separate from albedo and roughness; no gray card or calibrated radiometry.')
    (folder/'pair-values.json').write_text(json.dumps(reports,indent=2));return reports

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--renders',required=True);a=p.parse_args();r=measure(a.renders)
    for name,row in r.items():print(name,'WB',row['linear_rgb_gains'],[(p['label'],round(p['display_luma_delta_255'],2)) for p in row['patches']])
