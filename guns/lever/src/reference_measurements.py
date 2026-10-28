"""Comparison-only native photo measurements. Never imported by modeling.

The recovered planes depend on estimated cameras and different photographed
guns. Their disagreement is retained, rather than presented as metrology.
"""
import json
import math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
BASE=Path(__file__).resolve().parents[1]
LINES={
 'open_photo':dict(inside_length=((410,489),(393,709)),inside_width=((360,596),(452,604)),
                   bar_side_depth=((349,615),(355,615)),web_depth=((373,400),(391,400))),
 'trigger_quarter':dict(inside_length=((521,409),(753,430)),inside_width=((630,400),(623,442)),
                        bar_side_depth=((627,447),(627,442)),blade_side_depth=((459,373),(468,373))),
}


def recover(data,pixels):
    s=data['shot'];camera=np.asarray(s['location']);forward=np.asarray(s['target'])-camera
    forward/=np.linalg.norm(forward);right=np.cross(forward,[0,0,1]);right/=np.linalg.norm(right)
    up=np.cross(right,forward);a=s['roll'];right,up=right*math.cos(a)+up*math.sin(a),up*math.cos(a)-right*math.sin(a)
    x0,y0,x1,y1=data['crop'];width,height=x1-x0,y1-y0;focal=width*s['lens']/36;points=[]
    for px,py in pixels:
        u,v=px-x0,py-y0
        direction=forward+right*((u-width/2)/focal)+up*((height/2-v)/focal)
        points.append((camera+direction*(-camera[0]/direction[0]))*1000)
    return np.asarray(points)


def main():
    cameras=json.loads((BASE/'build/cameras.json').read_text());report={}
    font=ImageFont.truetype(find_font('Noto Sans','Regular'),17)
    for name,lines in LINES.items():
        data=cameras[name];photo=Image.open(data['photo']).convert('RGB');draw=ImageDraw.Draw(photo);rows={}
        for i,(label,pixels) in enumerate(lines.items()):
            points=recover(data,pixels);length=float(np.linalg.norm(points[1]-points[0]))
            rows[label]=dict(native_pixels=pixels,estimated_plane_points_mm=points.tolist(),estimated_length_mm=length)
            color=('red','lime','cyan','magenta')[i];draw.line((*pixels[0],*pixels[1]),fill=color,width=2)
            draw.text((pixels[0][0]+8,pixels[0][1]),label+' %.1f mm'%length,font=font,fill=color,stroke_width=1,stroke_fill='black')
        if name=='open_photo':
            points=recover(data,[(511,285),(381,394),(393,485)])
            rows['S_curve']=dict(native_pixels=[(511,285),(381,394),(393,485)],
                pivot_belly_throat_mm=points.tolist(),offsets_from_pivot_mm=(points-points[0]).tolist())
        rows['limitation']='Estimated camera-plane lengths, uncertain several millimeters; closed and open photos do not recover the same loop dimensions.'
        report[name]=rows
        out=BASE/'renders/checkpoint';out.mkdir(parents=True,exist_ok=True)
        photo.save(out/(name+'-measurements.jpg'),quality=94,optimize=True)
    report['design_choice']='Open view controls the long loop envelope; closed view constrains section and continuity. The smaller recovered closed loop remains a stated difference, not a claimed exact match.'
    report['transverse_bar_width']='8.2 mm authored class estimate; an oblique photograph cannot independently establish this thickness.'
    report['hammer_checkering']='1.0 mm square pitch, 0.24 mm relief; approximate class detail, not calibrated manufacturer data.'
    native=[(505,189),(580,207)];points=recover(cameras['hammer_photo'],native);forward=points[0]-points[1]
    report['hammer_table']=dict(native_pixels=native,estimated_points_mm=points.tolist(),
        estimated_cocked_angle_degrees=math.degrees(math.atan2(forward[2],forward[1])),
        limitation='Estimated centerline on the same photographic action fit; not recovered manufacturing geometry.')
    (BASE/'build/photo-measurements.json').write_text(json.dumps(report,indent=2))
    print('PHOTO MEASUREMENTS', {n:{k:round(v['estimated_length_mm'],2) for k,v in rows.items() if isinstance(v,dict) and 'estimated_length_mm' in v} for n,rows in report.items() if isinstance(rows,dict)})


if __name__=='__main__':main()
