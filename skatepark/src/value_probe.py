"""Sunlit exported concrete, compared with balanced, outlined photo patches.

Exposed image values only: no inversion of camera exposure into reflectance.
Actual triangle hits and sun/camera rays certify the render patch surfaces.
"""
import argparse,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]

def median(im,mask):
    a=np.asarray(im,dtype=float)/255;y=a@np.array([.2126,.7152,.0722]);return float(np.median(y[mask]))

def main():
    import bpy
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    from render import render
    p=argparse.ArgumentParser();p.add_argument('--samples',type=int,default=32);p.add_argument('--out',type=Path,default=Path('renders/values'));a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True)
    shot=dict(location=(13,-8.5,2.2),target=(14.2,-6,0),lens=45,aspect=1.5,sky_saturation=.35)
    render(101,'export/lookdev',a.out,1200,a.samples,custom={'concrete_value':shot},with_context=False)
    scene=bpy.context.scene;deps=bpy.context.evaluated_depsgraph_get();im=Image.open(a.out/'concrete_value.png').convert('RGB');annotated=im.copy();draw=ImageDraw.Draw(annotated);rows=[]
    tosun=Vector((.7,-.35,.55)).normalized()
    for x,y in [(13.6,-6),(14.2,-6),(14.8,-6)]:
        points=[];checks=[]
        for dx,dy in [(-.13,-.13),(.13,-.13),(.13,.13),(-.13,.13),(0,0)]:
            hit,pos,normal,face,ob,_=scene.ray_cast(deps,Vector((x+dx,y+dy,8)),Vector((0,0,-1)))
            assert hit and abs(pos.z)<2e-5 and normal.z>.99,(pos,ob)
            assert 'Concrete' in ob.data.materials[ob.data.polygons[face].material_index].name,ob.name
            assert not scene.ray_cast(deps,pos+normal*.002,tosun,distance=100)[0],('Sun occlusion',list(pos))
            direction=pos-scene.camera.location;distance=direction.length
            visible=scene.ray_cast(deps,scene.camera.location,direction.normalized(),distance=distance-.003)[0]
            assert not visible,('Camera occlusion',list(pos))
            q=world_to_camera_view(scene,scene.camera,pos);points.append((q.x*im.width,(1-q.y)*im.height));checks.append(list(pos))
        polygon=points[:4];mask=Image.new('1',im.size);ImageDraw.Draw(mask).polygon(polygon,fill=1);mask=np.asarray(mask,dtype=bool)
        draw.line(polygon+[polygon[0]],fill=(250,70,30),width=3)
        rows.append(dict(actual_surface_corners_m=checks,render_polygon_pixels=polygon,display_Y_median=median(im,mask),sun_and_camera_rays_clear=True))
    annotated.save(a.out/'render-sunlit-patches.jpg',quality=95)
    photo=Image.open('refs/venice.jpg').convert('RGB');rgb=np.asarray(photo,dtype=float)/255;lin=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
    neutral=(2100,1445,2140,1470);x0,y0,x1,y1=neutral;n=np.median(lin[y0:y1,x0:x1],axis=(0,1));gains=n.mean()/n
    balanced=np.clip(lin*gains,0,1);rgb=np.where(balanced<=.0031308,balanced*12.92,1.055*balanced**(1/2.4)-.055);photo=Image.fromarray(np.rint(rgb*255).astype('uint8'));d=ImageDraw.Draw(photo)
    photo_rows=[]
    for rect in [(2070,1450,2140,1490),(2840,1400,2920,1430),(3340,1330,3410,1360)]:
        mask=Image.new('1',photo.size);ImageDraw.Draw(mask).rectangle(rect,fill=1);value=median(photo,np.asarray(mask,dtype=bool));photo_rows.append(dict(native_rectangle=rect,display_Y_median=value));d.rectangle(rect,outline=(250,70,30),width=6)
    photo.save(a.out/'photo-sunlit-patches.jpg',quality=95)
    result=dict(render=rows,photo=photo_rows,photo_neutral=neutral,neutral_description='Sunlit unpainted light-gray concrete coping/deck, assumed neutral; no gray card',linear_white_balance_gains=gains.tolist(),scope='Exposed sRGB image Y, not measured real-world reflectance. Camera exposure, unknown photo processing and neutral assumption bound the comparison.')
    (a.out/'concrete-value.json').write_text(json.dumps(result,indent=2));print('CONCRETE VALUE',json.dumps(result))

if __name__=='__main__':main()
