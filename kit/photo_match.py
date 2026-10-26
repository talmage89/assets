"""Calibrate pinhole cameras from measured 3D landmarks and reference pixels.

Uses NumPy only, never modifies a mesh. Original photographs are read only by
this review tool, never by Blender materials or texture generation. Lens is an
estimate when EXIF/calibration data are absent. Camera residuals remain visible.
"""
import argparse,json,math,runpy,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
FONT='/usr/share/fonts/noto/NotoSans-Regular.ttf'


def project(parameters,points,width,height):
    az,el,cx,cy,cz,loglens,roll=parameters
    forward=np.array([math.cos(el)*math.cos(az),math.cos(el)*math.sin(az),math.sin(el)])
    right=np.cross(forward,[0,0,1]);right/=np.linalg.norm(right)
    up=np.cross(right,forward)
    right,up=right*math.cos(roll)+up*math.sin(roll),up*math.cos(roll)-right*math.sin(roll)
    relative=points-np.array([cx,cy,cz])
    depth=relative@forward
    focal=width*math.exp(loglens)/36
    safe=np.maximum(depth,.02)
    uv=np.stack([width/2+focal*(relative@right)/safe,height/2-focal*(relative@up)/safe],axis=1)
    return uv,depth,forward


def calibrate(match):
    width,height=match['crop'][2]-match['crop'][0],match['crop'][3]-match['crop'][1]
    points=np.array([row['world'] for row in match['landmarks']],float)
    target=np.array([row['pixel'] for row in match['landmarks']],float)-np.array(match['crop'][:2])
    weights=np.sqrt(np.array([row.get('weight',1) for row in match['landmarks']]))
    camera=np.array(match['location'],float);direction=np.array(match['target'])-camera
    az=math.atan2(direction[1],direction[0]);el=math.atan2(direction[2],np.linalg.norm(direction[:2]))
    initial=np.array([az,el,*camera,math.log(match['lens']),0.0]);parameters=initial.copy()
    def residual(p):
        uv,depth,_=project(p,points,width,height)
        errors=((uv-target)*weights[:,None]/width).ravel()
        # Small lens prior keeps a noisy short baseline from inventing a telephoto lens.
        return np.r_[errors,(p[5]-initial[5])*.012,p[6]*.02,np.minimum(depth-.02,0)*10]
    damping=.001;cost=np.inf
    for iteration in range(160):
        r=residual(parameters);cost=float(r@r)
        columns=[]
        for k in range(7):
            step=1e-5 if k in (0,1,5) else 1e-5*max(1,abs(parameters[k]))
            candidate=parameters.copy();candidate[k]+=step
            columns.append((residual(candidate)-r)/step)
        jac=np.stack(columns,axis=1)
        matrix=jac.T@jac
        delta=np.linalg.solve(matrix+damping*np.diag(np.maximum(np.diag(matrix),1e-5)), -jac.T@r)
        candidate=parameters+delta
        candidate[1]=np.clip(candidate[1],-1.54,1.30)
        candidate[5]=np.clip(candidate[5],math.log(18),math.log(180))
        candidate[6]=np.clip(candidate[6],-.35,.35)
        cr=residual(candidate);new_cost=float(cr@cr)
        if new_cost<cost:
            parameters=candidate;damping=max(1e-9,damping*.4)
            if np.linalg.norm(delta)<1e-7:break
        else:damping=min(1e8,damping*5)
    uv,depth,forward=project(parameters,points,width,height)
    errors=np.linalg.norm(uv-target,axis=1)
    if np.any(depth<=0):raise ValueError('Camera fitted behind a landmark')
    location=parameters[2:5].tolist();look=(parameters[2:5]+forward).tolist()
    shot=dict(location=location,target=look,lens=math.exp(parameters[5]),aspect=width/height,
              roll=float(parameters[6]),studio_yaw=match.get('studio_yaw',0),lid=match.get('lid',0),hide=match.get('hide',[]),isolate=match.get('isolate',[]),
              hide_sets=match.get('hide_sets',[]),hide_assemblies=match.get('hide_assemblies',[]),exposure=match.get('exposure',-.8),background=match.get('background','light'))
    return dict(shot=shot,crop=match['crop'],photo=match['photo'],title=match['title'],
                lens_status='estimated from measured landmarks; original EXIF unavailable',
                residual_rms_pixels=float(np.sqrt(np.mean(errors**2))),residuals_pixels=errors.tolist(),
                landmarks_world_m=points.tolist(),projected_pixels=uv.tolist(),measured_pixels=target.tolist())


def solve(config,out):
    definitions=runpy.run_path(config)['MATCHES']
    results={name:calibrate(value) for name,value in definitions.items()}
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    Path(out).write_text(json.dumps(results,indent=2))
    for name,result in results.items():print(name,'lens %.1f mm, RMS %.2f px'%(result['shot']['lens'],result['residual_rms_pixels']))


def compose(calibration,renders,out):
    results=json.loads(Path(calibration).read_text());out=Path(out);out.mkdir(parents=True,exist_ok=True)
    for name,data in results.items():
        photo=Image.open(data['photo']).convert('RGBA').crop(data['crop'])
        render=Image.open(Path(renders)/(name+'.png')).convert('RGBA')
        width=1100;height=round(width*photo.height/photo.width)
        def panel(im):
            im=im.resize((width,height),Image.Resampling.LANCZOS)
            bg=Image.new('RGBA',im.size,(238,239,236,255));bg.alpha_composite(im)
            return bg.convert('RGB')
        pair=Image.new('RGB',(width*2,height+126),(238,239,236));draw=ImageDraw.Draw(pair)
        pair.paste(panel(render),(0,70));pair.paste(panel(photo),(width,70))
        font=ImageFont.truetype(FONT,23);small=ImageFont.truetype(FONT,18)
        draw.text((18,12),data['title']+' / original asset',font=font,fill=(22,38,29))
        draw.text((width+18,12),'Reference photograph / same calibrated framing',font=font,fill=(22,38,29))
        text='Estimated %.1f mm lens • measured-landmark RMS %.1f px • source pixels are comparison only'%(data['shot']['lens'],data['residual_rms_pixels'])
        draw.text((18,height+84),text,font=small,fill=(49,64,52))
        pair.save(out/(name+'-pair.jpg'),quality=94,optimize=True)
        # Separate diagnostic overlay shows fitting error without hiding the pair.
        overlay=panel(photo);d=ImageDraw.Draw(overlay)
        source_w=data['crop'][2]-data['crop'][0];factor=width/source_w
        for measured,predicted in zip(data['measured_pixels'],data['projected_pixels']):
            p=tuple(v*factor for v in measured);q=tuple(v*factor for v in predicted)
            d.ellipse((p[0]-5,p[1]-5,p[0]+5,p[1]+5),outline='lime',width=2)
            d.line((*p,*q),fill='red',width=2)
        overlay.save(out/(name+'-calibration.jpg'),quality=92,optimize=True)
        print('PAIR',out/(name+'-pair.jpg'))


def verify(calibration):
    """Independent Blender projection check: handedness, roll and horizontal FOV."""
    import bpy
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    sc=bpy.context.scene
    camera=bpy.data.objects.new('Calibration verification',bpy.data.cameras.new('Calibration verification'))
    sc.collection.objects.link(camera)
    camera.data.sensor_fit='HORIZONTAL';camera.data.sensor_width=36
    for name,data in json.loads(Path(calibration).read_text()).items():
        shot=data['shot'];width=data['crop'][2]-data['crop'][0];height=data['crop'][3]-data['crop'][1]
        sc.render.resolution_x=width;sc.render.resolution_y=height
        camera.location=shot['location']
        camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler()
        camera.rotation_euler.rotate_axis('Z',shot['roll']);camera.data.lens=shot['lens']
        bpy.context.view_layer.update()
        errors=[]
        for point,expected in zip(data['landmarks_world_m'],data['projected_pixels']):
            uv=world_to_camera_view(sc,camera,Vector(point))
            pixel=(uv.x*width,(1-uv.y)*height)
            errors.append(math.dist(pixel,expected))
        maximum=max(errors)
        if maximum>.05:raise AssertionError(f'{name}: Blender/calibrator disagreement {maximum:.3f} px')
        print(f'CAMERA VERIFIED {name}: maximum projection disagreement {maximum:.5f} px')
    bpy.data.objects.remove(camera,do_unlink=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();sub=parser.add_subparsers(dest='mode',required=True)
    a=sub.add_parser('solve');a.add_argument('--config',required=True);a.add_argument('--out',required=True)
    a=sub.add_parser('compose');a.add_argument('--calibration',required=True);a.add_argument('--renders',required=True);a.add_argument('--out',required=True)
    a=sub.add_parser('verify');a.add_argument('--calibration',required=True)
    arguments=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None
    args=parser.parse_args(arguments)
    if args.mode=='solve':solve(args.config,args.out)
    elif args.mode=='compose':compose(args.calibration,args.renders,args.out)
    else:verify(args.calibration)
