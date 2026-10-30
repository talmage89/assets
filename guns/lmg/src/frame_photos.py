"""Keep posed exported whole guns inside their photographic inspection frames.

Landmark fitting supplies the view. Only camera translation changes to retain
all visible surfaces; its resulting fit residual remains in the comparison.
"""
import hashlib,json,math,sys
from pathlib import Path
import bpy,numpy as np
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import weapon as W,weapon_verify as V
from kit.photo_match import project
from delivery import split_imported
from final_shots import PHOTO_POSES
path=BASE/'build/cameras.json';rows=json.loads(path.read_text());proof={}
V.import_glb(BASE/'export/lmg.glb');split_imported(bpy.context.scene,BASE/'build/delivery/finalized.blend')
arm=bpy.data.objects['HarrowArmature']
for name in ('right_photo','left_photo','belt_photo','used_field_photo','used_right_photo','stock_finish_photo','box_finish_photo','handguard_finish_photo'):
    row=rows[name];shot=row['shot'];pose=PHOTO_POSES[name];W.pose(arm,pose['action'],pose['frame'])
    matrices={b.name:b.matrix_basis.copy() for b in arm.pose.bones}
    for bone,(clip,frame) in pose.get('layers',{}).items():W.pose(arm,clip,frame);matrices[bone]=arm.pose.bones[bone].matrix_basis.copy()
    arm.animation_data.action=None
    for bone,matrix in matrices.items():arm.pose.bones[bone].matrix_basis=matrix
    bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();triangles=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or not ob.get('asset_set'):continue
        if pose.get('hide_box') and ob.name.startswith(('Box_','Belt_')):continue
        if pose.get('inspection_parts') and not ob.name.startswith(tuple(pose['inspection_parts'])):continue
        ev=ob.evaluated_get(dg);mesh=ev.to_mesh();mesh.calc_loop_triangles()
        points=np.array([tuple(ev.matrix_world@v.co) for v in mesh.vertices]);faces=np.array([t.vertices[:] for t in mesh.loop_triangles]);q=points[faces]
        valid=np.linalg.norm(np.cross(q[:,1]-q[:,0],q[:,2]-q[:,0]),axis=1)>1e-12
        triangles.append(q[valid].reshape(-1,3));ev.to_mesh_clear()
    xyz=np.concatenate(triangles);w,h=row['crop'][2]-row['crop'][0],row['crop'][3]-row['crop'][1]
    location=np.array(shot['location']);forward=np.array(shot['target'])-location;forward/=np.linalg.norm(forward)
    az=math.atan2(forward[1],forward[0]);el=math.atan2(forward[2],np.linalg.norm(forward[:2]));roll=shot['roll']
    right=np.cross(forward,[0,0,1]);right/=np.linalg.norm(right);up=np.cross(right,forward)
    right,up=right*math.cos(roll)+up*math.sin(roll),up*math.cos(roll)-right*math.sin(roll)
    def projection():return project(np.r_[az,el,location,math.log(shot['lens']),roll],xyz,w,h)[0]
    uv=projection();before=[*uv.min(0),*uv.max(0)];margin=np.array([w,h])*.035
    changed=bool(np.any(uv.min(0)<margin) or np.any(uv.max(0)>np.array([w,h])-margin))
    if changed:
        # Recenter in the image plane, retaining fitted orientation and lens.
        for _ in range(3):
            center=(uv.min(0)+uv.max(0))/2-np.array([w,h])/2
            depth=float(np.median((xyz-location)@forward));scale=depth*36/(w*shot['lens'])
            location+=right*center[0]*scale-up*center[1]*scale;uv=projection()
        initial=location.copy();step=float(np.median((xyz-location)@forward))*.005
        for iteration in range(400):
            if np.all(uv.min(0)>=margin) and np.all(uv.max(0)<=np.array([w,h])-margin):break
            location-=forward*step;uv=projection()
        else:raise AssertionError((name,'could not frame entire gun'))
        shot['location']=location.tolist();shot['target']=(location+forward).tolist()
        row['inspection_margin_note']='Camera translated to retain all visible imported surfaces with >=3.5% frame margin; fitted orientation/lens unchanged.'
        landmarks=project(np.r_[az,el,location,math.log(shot['lens']),roll],np.array(row['landmarks_world_m']),w,h)[0]
        errors=np.linalg.norm(landmarks-np.array(row['measured_pixels']),axis=1)
        row.update(projected_pixels=landmarks.tolist(),residuals_pixels=errors.tolist(),residual_rms_pixels=float(np.sqrt(np.mean(errors**2))))
    proof[name]=dict(changed=changed,projected_bounds_before=before,projected_bounds_after=[*uv.min(0),*uv.max(0)],frame=[w,h],minimum_margin_fraction=.035,triangles=len(xyz)//3,residual_rms_pixels=row['residual_rms_pixels'])
path.write_text(json.dumps(rows,indent=2));(BASE/'build/photo-frame-proof.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256((BASE/'export/lmg.glb').read_bytes()).hexdigest(),shots=proof),indent=2))
print('WHOLE-GUN PHOTO FRAMES',proof,flush=True)
