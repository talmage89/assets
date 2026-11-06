"""True exported tubes and the optional .85 px ribbon at 30/60/120 metres.

Photographs have no surveyed wire distances. Their labelled near/middle/far
sky-line samples are native photographic contrasts, not invented range data.
They are shown beside all three exact model distances, with this limitation.
No reference pixels are used by Blender or the texture generator.
"""
import argparse,json,hashlib,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import numpy as np
from kit.image_io import srgb_to_linear,linear_to_srgb

# Native image coordinates. Small search bands accommodate a curved line and
# unknown lens distortion; annotations expose the actual profile locations.
PHOTO_LINES={
 'residential-a':dict(neutral=(20,95,55,120),lines=[
   dict(zone='near',a=(80,79),b=(140,128)),
   dict(zone='middle',a=(120,111),b=(160,144)),
   dict(zone='far',a=(282,148),b=(289,165))]),
 'residential-b':dict(neutral=(2150,330,2220,380),lines=[
   dict(zone='near',a=(100,445),b=(250,412)),
   dict(zone='middle',a=(400,376),b=(550,338)),
   dict(zone='far',a=(700,300),b=(850,261)),
   dict(zone='jacket',a=(900,506),b=(1000,490))]),
 'hardware':dict(neutral=None,lines=[
   dict(zone='jacket',a=(80,743),b=(180,715))])}


def render(width,samples):
    import bpy
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    from render import setup
    from ribbon import inspection
    from deliver import bundle
    from span import catenary
    bpy.ops.wm.read_factory_settings(use_empty=True);source=Path('export/UtilityStreet-101.gltf')
    bpy.ops.import_scene.gltf(filepath=str(source.resolve()));meta=json.loads(source.with_suffix('.json').read_text())
    for ob in list(bpy.context.scene.objects):
        if ob.type=='MESH' and not ob.name.startswith('Conductors_'):bpy.data.objects.remove(ob,do_unlink=True)
    cam=setup(max(128,samples),wire_control=True);sc=bpy.context.scene;sc.compositing_node_group=None;sc.cycles.use_adaptive_sampling=False
    sc.view_layers[0].cycles.denoising_store_passes=False;sc.view_layers[0].use_pass_object_index=False
    sc.render.resolution_x=width;sc.render.resolution_y=width//2;sc.render.resolution_percentage=100
    cam.data.lens=50
    first=meta['plan']['poles'][0]['location'];second=meta['plan']['poles'][1]['location'];middle=(first[1]+second[1])/2
    probes=[s for s in meta['spans'] if s['name'] in ('Span_0_Primary_A','Span_0_Telephone','Span_0_CATV')]
    folder=Path('renders/wires');folder.mkdir(parents=True,exist_ok=True);rows=[]
    for distance in (30,60,120):
        cam.location=(first[0]+distance,middle,1.85);target=Vector((first[0],middle,7.2))
        cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update()
        project=lambda p: world_to_camera_view(sc,cam,Vector(p))
        projected=[]
        for s in probes:
            curve=catenary(s['start'],s['end'],s['sag_m'])['point'];pts=[]
            for f in np.linspace(.38,.62,61):
                uv=project(curve(float(f)));pts.append((uv.x*width,(1-uv.y)*sc.render.resolution_y))
            projected.append(dict(name=s['name'],material=s['material'],diameter_m=s['diameter_m'],points_px=pts))
        wire_objects=[o for o in sc.objects if o.name.startswith('Conductors_')]
        for mode in ('tube','ribbon','sky'):
            temporary=None
            if mode=='ribbon':temporary=inspection(meta,cam,width,sc.render.resolution_y)
            for ob in wire_objects:ob.visible_camera=(mode=='tube')
            path=folder/f'{distance}-{mode}.png';sc.render.filepath=str(path.resolve());bpy.ops.render.render(write_still=True)
            if temporary:bpy.data.objects.remove(temporary,do_unlink=True)
        rows.append(dict(distance_m=distance,camera=list(cam.location),lens_mm=50,width_px=width,probes=projected))
    (folder/'provenance.json').write_text(json.dumps(dict(source=str(source),bundle_sha256=bundle(source),samples=max(128,samples),
        engine='Cycles GPU, no denoise, adaptive sampling off',scope='Exported actual conductors; same sky and display transform for tubes, optional ribbons and empty-sky control; exact horizontal range to span centre',rows=rows),indent=2))


def sample(image,x,y):
    h,w=image.shape[:2];x=np.clip(x,0,w-1.001);y=np.clip(y,0,h-1.001)
    xi=np.floor(x).astype(int);yi=np.floor(y).astype(int);fx=x-xi;fy=y-yi
    return image[yi,xi]*(1-fx)*(1-fy)+image[yi,xi+1]*fx*(1-fy)+image[yi+1,xi]*(1-fx)*fy+image[yi+1,xi+1]*fx*fy


def profiles(image,points,sky=None,search=2):
    Y=image@np.array([.2126,.7152,.0722]);linear=srgb_to_linear(image)@np.array([.2126,.7152,.0722])
    points=np.asarray(points);direction=points[-1]-points[0];direction/=np.linalg.norm(direction);normal=np.array([-direction[1],direction[0]])
    offsets=np.linspace(-search,search,81);xy=points[:,None,:]+offsets[None,:,None]*normal
    values=sample(Y,xy[:,:,0],xy[:,:,1]);radiance=sample(linear,xy[:,:,0],xy[:,:,1]);which=values.argmin(axis=1)
    if sky is None:
        band=np.array([-9,-7,7,9]);control=points[:,None,:]+band[None,:,None]*normal
        bg=np.median(sample(Y,control[:,:,0],control[:,:,1]),axis=1)
        bg_linear=np.median(sample(linear,control[:,:,0],control[:,:,1]),axis=1)
    else:
        bg=sample(sky@np.array([.2126,.7152,.0722]),points[:,0],points[:,1])
        bg_linear=sample(srgb_to_linear(sky)@np.array([.2126,.7152,.0722]),points[:,0],points[:,1])
    line=values[np.arange(len(points)),which];line_linear=radiance[np.arange(len(points)),which]
    contrast=(bg-line)/np.maximum(.01,bg);integrated=np.trapezoid(np.maximum(0,(bg[:,None]-values)/np.maximum(.01,bg[:,None])),offsets,axis=1)
    return dict(encoded_Yprime_sky_median=float(np.median(bg)),encoded_Yprime_line_median=float(np.median(line)),
        encoded_Weber_contrast_median=float(np.median(contrast)),encoded_Weber_contrast_p10=float(np.quantile(contrast,.1)),
        linear_Weber_contrast_median=float(np.median((bg_linear-line_linear)/np.maximum(.001,bg_linear))),
        integrated_encoded_deficit_pixels_median=float(np.median(integrated)),profile_count=len(points),normal_search_radius_px=search)


def measure():
    from PIL import Image,ImageDraw,ImageFont
    from kit.fonts import find_font
    from kit.contact import contact
    folder=Path('renders/wires');meta=json.loads((folder/'provenance.json').read_text());rows=[]
    font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),18)
    for row in meta['rows']:
        distance=row['distance_m'];sky=np.asarray(Image.open(folder/f'{distance}-sky.png').convert('RGB'),float)/255
        for mode in ('tube','ribbon'):
            path=folder/f'{distance}-{mode}.png';im=Image.open(path).convert('RGB');rgb=np.asarray(im,float)/255;probes=[];draw=ImageDraw.Draw(im)
            for p in row['probes']:
                result=profiles(rgb,p['points_px'],sky);probes.append(dict(name=p['name'],diameter_m=p['diameter_m'],**result))
                point=p['points_px'][len(p['points_px'])//2];draw.text((point[0]+10,point[1]+10),p['name'].removeprefix('Span_0_')+' '+f'{result["encoded_Weber_contrast_median"]:.1%}',font=font,fill=(255,100,30))
            im.save(folder/f'{distance}-{mode}-profiles.jpg',quality=95);rows.append(dict(distance_m=distance,representation=mode,probes=probes))
    photos={};crop_paths=[]
    for name,spec in PHOTO_LINES.items():
        im=Image.open('refs/'+name+'.jpg').convert('RGB');rgb=np.asarray(im,float)/255;linear=srgb_to_linear(rgb)
        if spec['neutral']:
            x0,y0,x1,y1=spec['neutral'];neutral=np.median(linear[y0:y1,x0:x1].reshape(-1,3),axis=0);gains=float(np.mean(neutral))/neutral
        else:gains=np.ones(3)
        balanced=np.clip(linear_to_srgb(linear*gains),0,1);annotation=Image.fromarray(np.uint8(balanced*255+.5));draw=ImageDraw.Draw(annotation);values=[]
        for line in spec['lines']:
            a=np.array(line['a']);b=np.array(line['b']);pts=a+(b-a)*np.linspace(.05,.95,81)[:,None]
            result=profiles(balanced,pts,search=3);values.append(dict(**line,**result))
            draw.line([tuple(a),tuple(b)],fill=(255,70,30),width=1);draw.text(tuple(a+np.array((4,10))),line['zone']+' '+f'{result["encoded_Weber_contrast_median"]:.1%}',font=font,fill=(255,70,30))
        annotation.save(folder/(name+'-profiles.jpg'),quality=96)
        photos[name]=dict(neutral_assumption=('none accepted; original WB, geometry/contrast only' if name=='hardware' else 'achromatic cloud, approximate daylight white point; no gray card'),neutral_roi=spec['neutral'],linear_gains=gains.tolist(),lines=values,range_status='No surveyed distance. Native near/middle/far image zones only; not a literal 30/60/120 m survey.')
        # Retain native pixels around the sky lines; comparison crops never
        # become an atlas, a decal, a background or a committed docs image.
        for line in spec['lines']:
            a=np.array(line['a']);b=np.array(line['b']);cx,cy=(a+b)/2
            box=(max(0,int(cx-180)),max(0,int(cy-55)),min(im.width,int(cx+180)),min(im.height,int(cy+55)))
            crop=Image.fromarray(np.uint8(balanced*255+.5)).crop(box);p=folder/(name+'-'+line['zone']+'.jpg');crop.save(p,quality=96);crop_paths.append(p)
    output=dict(model=rows,photographs=photos,measurement='Displayed Rec.709 Y-prime Weber contrast (sky-line)/sky, with linear-light contrast and integrated deficit also reported. Median of transverse profiles; annotations expose selections.',
        range_limit='Model distances are exact horizontal ranges. These public photos have no surveyed line depths: native sky-line contrasts bracket the comparison, and are not presented as measured distances.')
    (folder/'contrast.json').write_text(json.dumps(output,indent=2))
    paths=[folder/f'{d}-{m}-profiles.jpg' for d in (30,60,120) for m in ('tube','ribbon')]
    from kit.contact import review_sheet
    review_sheet([paths[i:i+2] for i in range(0,len(paths),2)],folder/'distance-contact.jpg',width=2400,title='Exact model ranges / exported tubes and optional compensated ribbons')
    review_sheet([crop_paths[i:i+3] for i in range(0,len(crop_paths),3)],folder/'photo-contrast.jpg',width=2400,title='Native photographic sky-line profiles / unsurveyed near-middle-far zones')
    review_sheet([[folder/f'{d}-tube-profiles.jpg',folder/f'{d}-ribbon-profiles.jpg',folder/f'residential-a-{zone}.jpg',folder/f'residential-b-{zone}.jpg'] for d,zone in zip((30,60,120),('near','middle','far'))],folder/'photo-distance-pairs.jpg',width=3200,title='Exact model 30 / 60 / 120 m beside native photo zones / photo depths unknown')
    print('WIRE CONTRAST',[(r['distance_m'],r['representation'],[(p['name'],round(p['encoded_Weber_contrast_median'],3)) for p in r['probes']]) for r in rows])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=('render','measure'));p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=64)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    render(a.width,a.samples) if a.stage=='render' else measure()
