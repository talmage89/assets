"""Auditable photographic rear-glass estimates, never modeling input.

Chassis-calibrated camera rays intersect an approximate backlight plane. These
are class estimates with perspective/curved-glass uncertainty, not OEM CAD.
"""
import json,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw


def rear_glass(out,cameras,font,save):
    root=Path(__file__).resolve().parents[1];report={}
    picks={
      'camry_rear':dict(top=[(299,225),(635,227)],base=[(113,320),(513,308)],hip=(591,344)),
      'accord_rear':dict(top=[(325,222),(685,210)],base=[(189,299),(510,297)],hip=(597,324))}
    for name,pp in picks.items():
        data=cameras[name];s=data['shot'];cam=np.array(s['location']);fw=np.array(s['target'])-cam;fw/=np.linalg.norm(fw)
        right=np.cross(fw,[0,0,1]);right/=np.linalg.norm(right);up=np.cross(right,fw);a=s['roll']
        right,up=right*np.cos(a)+up*np.sin(a),up*np.cos(a)-right*np.sin(a)
        crop=data['crop'];w=crop[2]-crop[0];h=crop[3]-crop[1];f=w*s['lens']/36
        def ray(xy):
            q=np.array(xy)*1.75-np.array(crop[:2]);return fw+(q[0]-w/2)/f*right-(q[1]-h/2)/f*up
        def glass(xy,intercept=1.67):
            r=ray(xy);return cam+r*(intercept-cam[2]-.30*cam[1])/(r[2]+.30*r[1])
        top=[glass(p) for p in pp['top']];base=[glass(p) for p in pp['base']]
        y=np.mean([p[1] for p in base]);r=ray(pp['hip']);hip=cam+r*(y-cam[1])/r[1]
        widths={key:abs(pts[1][0]-pts[0][0]) for key,pts in [('top',top),('base',base)]}
        pillar=abs(hip[0]-base[1][0])
        report[name]=dict(photo='refs/sedan-'+name.replace('_','-')+'.jpg',preview_picks=pp,
          backprojected_top_m=[p.tolist() for p in top],backprojected_base_m=[p.tolist() for p in base],
          hip_at_base_y_m=hip.tolist(),top_width_m=widths['top'],base_width_m=widths['base'],near_c_pillar_transverse_width_m=pillar,
          width_uncertainty_m=.080,pillar_uncertainty_m=.060,
          method='Chassis camera rays intersect z + 0.30 y = 1.67 m; hip intersects the mean base Y plane. Glass is curved, picks +/-4 preview px, plane height/rake are estimates.',
          white_balance='Neutral white studio backdrop, unit RGB gains; no paint color measurement')
        im=Image.open(root/data['photo'].split('/')[-2]/Path(data['photo']).name).convert('RGB');d=ImageDraw.Draw(im)
        for key,color in [('top',(220,65,25)),('base',(20,130,210))]:
            ps=[tuple(v*1.75 for v in p) for p in pp[key]];d.line((*ps[0],*ps[1]),fill=color,width=5)
            for x,y in ps:d.ellipse((x-7,y-7,x+7,y+7),outline=color,width=4)
        ps=[tuple(v*1.75 for v in p) for p in [pp['base'][1],pp['hip']]];d.line((*ps[0],*ps[1]),fill=(25,170,70),width=5)
        d.text((32,30),name.replace('_',' ').upper()+' / REAR GLASS CLASS ESTIMATE',font=font(28),fill=(35,50,65))
        d.text((32,75),f"Top {widths['top']*1000:.0f}, base {widths['base']*1000:.0f} mm (+/-80); near sail {pillar*1000:.0f} mm (+/-60)",font=font(24),fill=(35,50,65))
        d.text((32,115),'Calibrated rays + estimated glass plane; transverse widths, not surface distances or OEM dimensions.',font=font(21),fill=(35,50,65))
        save(im,out/(name+'-glass-measure.jpg'))
    (out/'rear-glass-photo.json').write_text(json.dumps(report,indent=2))
    return report
