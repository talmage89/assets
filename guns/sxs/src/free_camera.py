"""Rigid point/line/rim calibration with free focal length and pose.

Head surfaces and outlines are excluded. The published open image is cropped;
its principal point and the two visible moving-part poses are nuisance variables.
All observations, constraints, residuals and alternate-detent fits are retained.
"""
import copy, math
import numpy as np
from PIL import Image
from kit.photo_match import calibrate, project


def optimize(initial, residual, bound, iterations=800):
    p=np.array(initial,float); damping=.001
    for _ in range(iterations):
        r=residual(p); eye=np.eye(len(p))*1e-6
        jac=np.stack([(residual(p+step)-r)/1e-6 for step in eye],axis=1)
        a=jac.T@jac
        delta=np.linalg.solve(a+damping*np.diag(np.maximum(np.diag(a),1e-9)),-jac.T@r)
        q=bound(p+delta)
        if residual(q)@residual(q)<r@r:
            p=q; damping=max(1e-10,damping*.4)
            if np.linalg.norm(delta)<1e-10: break
        else: damping=min(1e10,damping*5)
    return p


def line_residual(parameters, world, pixels, w, h, offset):
    uv,depth,_=project(parameters,world,w,h); uv+=offset
    line=np.cross(np.r_[uv[0],1],np.r_[uv[1],1]); line/=np.linalg.norm(line[:2])
    return np.c_[pixels,np.ones(len(pixels))]@line


def finish(source,p,points,target,offset,line_errors,scope):
    x,y,x1,y1=source['crop']; w=x1-x; h=y1-y
    uv,depth,direction=project(p[:7],points,w,h); uv+=offset
    assert min(depth)>.021,'Projection must not use the kit near-depth clamp'
    row=calibrate(source)
    row['shot'].update(location=p[2:5].tolist(),target=(p[2:5]+direction).tolist(),
        lens=math.exp(p[5]),roll=float(p[6]),aspect=w/h,
        shift_x=float(-offset[0]/w),shift_y=float(offset[1]/w))
    head_depth=float((np.array([0,.105,.050])-p[2:5])@direction)
    scale=w*math.exp(p[5])/36/head_depth*.001
    errors=np.linalg.norm(uv-target,axis=1); rms=float(np.sqrt(np.mean(errors**2)))
    lrms=float(np.sqrt(np.mean(np.square(line_errors))))
    row.update(projected_pixels=uv.tolist(),measured_pixels=target.tolist(),
        landmarks_world_m=points.tolist(),residuals_pixels=errors.tolist(),
        residual_rms_pixels=rms,camera_fit_rms_pixels=rms,camera_fit_rms_mm=rms/scale,
        rigid_line_residuals_pixels=list(map(float,line_errors)),rigid_line_rms_pixels=lrms,
        rigid_line_rms_mm=lrms/scale,head_depth_m=head_depth,head_pixels_per_mm=scale,
        camera_fit_landmark_count=len(points),camera_fit_passed=max(rms,lrms)/scale<1,
        lens_bounds_mm=[20,2000],lens_status='joint focal/pose fit; no EXIF; sparse class-reference calibration',
        fit_scope=scope,principal_point_crop_pixels=(offset+[w/2,h/2]).tolist())
    return row


def solve(source,*,opened_view=False):
    if opened_view: return solve_open(source)
    source=copy.deepcopy(source);x,y,x1,y1=source['crop'];w=x1-x;h=y1-y
    ow,oh=Image.open(source['photo']).size;offset=np.array([ow/2-x-w/2,oh/2-y-h/2])
    points=np.array([r['world'] for r in source['landmarks']]);target=np.array([r['pixel'] for r in source['landmarks']])-[x,y]
    lines=[(np.array(r['world']),np.array(r['pixels'])-[x,y]) for r in source['rigid_lines']]
    direction=np.array(source['target'])-source['location'];direction/=np.linalg.norm(direction)
    initial=np.r_[math.atan2(direction[1],direction[0]),math.asin(direction[2]),source['location'],math.log(150),0.]
    def residual(q):
        uv,depth,d=project(q,points,w,h);uv+=offset
        return np.r_[((uv-target)/w).ravel(),*[line_residual(q,lw,lp,w,h,offset)/w for lw,lp in lines],
                     np.minimum(depth-.021,0)*100,min(0,d@direction-.5)*10]
    def bound(q):
        q[1]=np.clip(q[1],-1.55,1.55);q[5]=np.clip(q[5],math.log(20),math.log(2000));return q
    trials=[]
    for lens in (30,60,120,240,500):
        p=initial.copy();center=points.mean(0);p[2:5]=center+(p[2:5]-center)*lens/150;p[5]=math.log(lens)
        p=optimize(p,residual,bound);trials.append((float(residual(p)@residual(p)),p))
    _,p=min(trials,key=lambda r:r[0]);le=np.concatenate([line_residual(p,lw,lp,w,h,offset) for lw,lp in lines])
    row=finish(source,p,points,target,offset,le,'Four rigid surface points plus rib centerline; no head outline or surface used')
    row.update(landmark_names=[r['name'] for r in source['landmarks']],
        principal_point_policy='original image center retained through comparison crop',
        rigid_lines=source['rigid_lines'],parameters=p.tolist())
    return row


def solve_open(source):
    source=copy.deepcopy(source);x,y,x1,y1=source['crop'];w=x1-x;h=y1-y;ow,oh=Image.open(source['photo']).size
    ring=np.array(source['rim_pixels']);n=len(ring)
    target=np.r_[ring,np.array([r['pixel'] for r in source['landmarks']])]-[x,y]
    hinge=np.array([0,.170,.019]);rib=np.array(source['rigid_lines'][0]['world']);breech=np.array(source['rigid_lines'][1]['world'])
    line_pixels=[np.array(r['pixels'])-[x,y] for r in source['rigid_lines']]
    def geometry(q,safety):
        a=q[-2];c=math.cos(a);s=math.sin(a);rot=np.array([[1,0,0],[0,c,-s],[0,s,c]])
        rim=np.c_[-.0126+.01335*np.cos(q[9:9+n]),np.full(n,.115),.044+.01335*np.sin(q[9:9+n])]
        rim=(rim-hinge)@rot.T+hinge
        a=q[-1];c=math.cos(a);s=math.sin(a)
        tail=(.0006*c+.073471*s,.094+.0006*s-.073471*c,.029812)
        return np.r_[rim,np.array([tail,(0,safety,.025567),(-.02595,.115,.0302)])],rot
    def bound(q):
        q[1]=np.clip(q[1],-1.55,-.05);q[5]=np.clip(q[5],math.log(20),math.log(2000))
        q[-2]=np.clip(q[-2],math.radians(-42),math.radians(-5.7));q[-1]=np.clip(q[-1],0,math.radians(25))
        q[9:9+n]=np.clip(q[9:9+n],.8,5.5)
        q[7]=np.clip(q[7],(-ow-x-w/2)/w,(2*ow-x-w/2)/w)
        q[8]=np.clip(q[8],(-oh-y-h/2)/w,(2*oh-y-h/2)/w)
        return q
    trials=[]
    # Initial view is a prior calibration, not a fixed solution. Diverse focal
    # starts and both actual safety detents are reoptimized from observations.
    for detent,safety in [('safe',.002),('fire',.007)]:
        def residual(q):
            points,rot=geometry(q,safety);offset=q[7:9]*w
            rear=rot@(np.array([0,.115,.044])-hinge)+hinge
            hemisphere=float((q[2:5]-rear)@(rot@np.array([0,1,0])))
            uv,depth,_=project(q[:7],points,w,h);uv+=offset
            lr=np.r_[line_residual(q[:7],(rib-hinge)@rot.T+hinge,line_pixels[0],w,h,offset),
                     line_residual(q[:7],breech,line_pixels[1],w,h,offset)]
            return np.r_[((uv-target)/w).ravel(),lr/w,np.minimum(depth-.021,0)*100,
                         min(0,q[4]-.06)*100,min(0,hemisphere-.001)*100,np.minimum(np.diff(q[9:9+n]),0)]
        for azimuth,elevation,focal in [(-.6,-.5,80),(-1.,-.5,120),(-.2,-.4,150),(-1.4,-.3,80),(-1.4,-.8,150),(-.7,-.9,80)]:
            location=np.array(source['location']);direction=np.array(source['target'])-location;direction/=np.linalg.norm(direction)
            offset=np.array([ow/2-x-w/2,oh/2-y-h/2])/w
            p=np.r_[math.atan2(direction[1],direction[0]),math.asin(direction[2]),location,math.log(150),0.,offset,
                    np.linspace(1.8,4.2,n),math.radians(-30),math.radians(20)]
            center=np.array([0,.105,.05]);p[2:5]=center+(p[2:5]-center)*focal/150;p[5]=math.log(focal)
            direction=np.array([math.cos(elevation)*math.cos(azimuth),math.cos(elevation)*math.sin(azimuth),math.sin(elevation)])
            p[:2]=[azimuth,elevation];p[2:5]=center-direction*(focal/150*.7)
            p=optimize(p,residual,bound,1200)
            points,rot=geometry(p,safety);offset=p[7:9]*w
            le=np.r_[line_residual(p[:7],(rib-hinge)@rot.T+hinge,line_pixels[0],w,h,offset),line_residual(p[:7],breech,line_pixels[1],w,h,offset)]
            score=float(residual(p)[:len(target)*2+4]@residual(p)[:len(target)*2+4])
            row=finish(source,p,points,target,offset,le,'Seven points on rigid turned barrel rim, lever tail, safety pad, breech corner; rigid rib and breech lines; no head outline used')
            row.update(parameters=p.tolist(),safety_detent=detent,objective=score,
                       principal_point_policy='published cropped frame; principal point fitted within one full original frame beyond image; no EXIF',
                       nuisance_parameters='barrel and lever angle, rim polar coordinates, principal point',
                       landmark_names=[f'near barrel rim {i+1}' for i in range(n)]+[r['name'] for r in source['landmarks']],
                       rigid_lines=[dict(world=((rib-hinge)@rot.T+hinge).tolist(),pixels=source['rigid_lines'][0]['pixels']),source['rigid_lines'][1]])
            row['barrel_front_hemisphere_m']=float((p[2:5]-(rot@(np.array([0,.115,.044])-hinge)+hinge))@(rot@np.array([0,1,0])))
            row['camera_fit_passed'] &= row['barrel_front_hemisphere_m']>.00099
            print('OPEN TRIAL',detent,focal,row['camera_fit_rms_pixels'],row['camera_fit_rms_mm'],row['barrel_front_hemisphere_m'],flush=True)
            row['view_constraint']='explicit muzzle-side prior: camera at least 1 mm ahead of the posed barrel rear plane; all projected depths >21 mm'
            row['correspondence_validated']=False
            row['acceptance_blocker']='Visible rim/control registration remains uncertain; a numerically small opposite-side fit was rejected after viewing its render'
            row['shot'].update(solved_barrel_angle=math.degrees(p[-2]),solved_lever_angle=math.degrees(p[-1]),solved_safety_shift_mm=-5 if detent=='safe' else 0)
            trials.append(row)
    row=min(trials,key=lambda r:r['objective'])
    row['alternate_fits']=[dict(lens_mm=r['shot']['lens'],safety_detent=r['safety_detent'],point_rms_mm=r['camera_fit_rms_mm'],line_rms_mm=r['rigid_line_rms_mm'],objective=r['objective']) for r in trials]
    return row
