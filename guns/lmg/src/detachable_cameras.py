"""Frame every static subset from its actual imported surface vertices."""
import hashlib,json,sys
from pathlib import Path
import bpy,numpy as np
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import weapon_verify as V
from final_shots import SHOTS
from image_masks import projection
records={}
for name in ('box_loaded','box_empty','cartridge','case','link'):
    source=BASE/'export'/(name+'.glb');V.import_glb(source)
    points=np.array([tuple(ob.matrix_world@v.co) for ob in bpy.context.scene.objects if ob.type=='MESH' for v in ob.data.vertices])
    shot=dict(SHOTS[name]);location=np.array(shot['location']);target=np.array(shot['target']);offset=location-target
    if name.startswith('box_'):
        target=(points.min(0)+points.max(0))/2;location=target+offset*1.10
    forward=(target-location)/np.linalg.norm(target-location);width=1000;height=round(width/shot['aspect']);size=np.array([width,height]);margin=size*.05
    step=float(np.linalg.norm(target-location))*.005
    for iteration in range(400):
        shot.update(location=location.tolist(),target=(location+forward).tolist())
        pixels,depth=projection(points,shot,width,height)
        if np.all(depth>0) and np.all(pixels.min(0)>=margin) and np.all(pixels.max(0)<=size-margin):break
        location-=forward*step
    else:raise AssertionError((name,'cannot frame standalone'))
    records[name]=dict(shot=shot,crop=[0,0,width,height],source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),projected_bounds=[*pixels.min(0),*pixels.max(0)],minimum_margin_fraction=.05)
(BASE/'build/detachable-cameras.json').write_text(json.dumps(records,indent=2))
print('MEASURED STANDALONE FRAMES',records,flush=True)
