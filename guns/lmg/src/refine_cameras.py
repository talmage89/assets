"""Keep the entire loose sight inside its inspection pair, with honest residuals."""
import json,sys,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.photo_match import project
BASE=Path(__file__).resolve().parents[1]
p=BASE/'build/cameras.json';data=json.loads(p.read_text())
r=data['sight_detail_photo'];s=r['shot'];location=np.array(s['location']);direction=np.array(s['target'])-location;direction/=np.linalg.norm(direction)
# A loose-part photograph and an assembled original housing differ. Its rim
# extremities must still remain visible; the residual is recomputed, not hidden.
center=np.array((0,-.018,.164));delta=(location-center)*.16
location+=delta;s['location']=location.tolist();s['target']=(location+direction).tolist()
w,h=r['crop'][2]-r['crop'][0],r['crop'][3]-r['crop'][1]
az=math.atan2(direction[1],direction[0]);el=math.atan2(direction[2],np.linalg.norm(direction[:2]))
uv,_,_=project(np.r_[az,el,location,math.log(s['lens']),s['roll']],np.array(r['landmarks_world_m']),w,h)
errors=np.linalg.norm(uv-np.array(r['measured_pixels']),axis=1)
r['projected_pixels']=uv.tolist();r['residuals_pixels']=errors.tolist();r['residual_rms_pixels']=float(np.sqrt(np.mean(errors**2)))
r['title']='Rear sight / complete rim and aperture'
r['inspection_margin_note']='Camera moved 16% farther from loose housing to retain the complete rim; resulting photographic residual is reported.'
p.write_text(json.dumps(data,indent=2))
print('SIGHT PAIR full-rim margin, measured RMS',r['residual_rms_pixels'])
