"""Concrete-balanced facade value readings; illumination is not albedo.

Hero samples project authored surface stations through the saved camera.
Photo boxes are independent, inspected bare cement/column/opening regions.
"""
import argparse,json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.image_io import srgb_to_linear


def project(point,r):
    w,x,y,z=r['rotation_quaternion']
    R=np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
    local=R.T@(np.array(point)-r['camera']);f=r['width']*r['lens_mm']/r['sensor_width_mm']
    return r['width']/2+local[0]/-local[2]*f,r['height']/2-local[1]/-local[2]*f


def stats(im,box):
    a=np.asarray(im.crop(box).convert('RGB'),dtype=float)/255;linear=srgb_to_linear(a)
    return dict(roi=box,median_srgb=np.median(a.reshape(-1,3),axis=0).tolist(),median_linear_Y=float(np.median(linear@np.array([.2126,.7152,.0722]))))


def main():
    p=argparse.ArgumentParser();p.add_argument('--pass-name',default='final');a=p.parse_args();folder=Path('renders')/a.pass_name
    frames=json.loads((folder/'views.json').read_text());result={};work=Path('build/facade-values');work.mkdir(parents=True,exist_ok=True)
    # Harmon balance is on its bare concrete, preserving the accepted pair.
    photo=Image.open('build/lookdev/matches/harmon-balanced.jpg').convert('RGB')
    photo_boxes=dict(spandrel=[2350,1180,2380,1195],column=[2348,1250,2358,1270],opening=[2390,1248,2410,1263])
    result['reference']={key:stats(photo,box) for key,box in photo_boxes.items()}
    annotated=photo.copy();d=ImageDraw.Draw(annotated)
    for name,box in photo_boxes.items():d.rectangle(box,outline='red',width=3);d.text((box[0],box[1]-18),name,fill='red')
    annotated.save(work/'photo-rois.jpg',quality=95)
    for seed in (101,202):
        r=next(r for r in frames if r['seed']==seed and r['name']=='hero');im=Image.open(r['output']).convert('RGB');annotated=im.copy();d=ImageDraw.Draw(annotated)
        plan=json.loads(Path(f'build/lookdev/garage-{seed}.json').read_text());stations=plan['structural_stations'];x=(stations[2]+stations[3])/2;y=-plan['width']/2;level=plan['floor_to_floor']*(2 if seed==101 else 1)
        points=dict(spandrel=[x,y-(.131 if seed==101 else .091),level+(.48 if seed==101 else .20)],column=[stations[2],y-.382,level-1.05],opening=[x,y+.25,level+1.7])
        points['column_side']=[stations[2]-.382,y-.12,level-1.05]
        values={}
        for name,point in points.items():
            u,v=project(point,r);half=1 if name=='column_side' else max(2,round(r['width']/320));box=[round(u-half),round(v-half),round(u+half),round(v+half)]
            values[name]=stats(im,box);values[name]['world_station_m']=point
            d.rectangle(box,outline='red',width=1);d.text((box[0],box[1]-15),name,fill='red')
        result[str(seed)]=values;annotated.save(work/f'{seed}-rois.jpg',quality=95)
    result['basis']=json.loads(Path('build/lookdev/matches/balance.json').read_text())['harmon']
    result['limitation']='Display-linear readings under different lights; not albedo recovery. Column is the visible front shaft, not presumed shaded without inspecting its ROI.'
    (work/(a.pass_name+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
