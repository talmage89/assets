"""Photo-only roof estimates and separately reported camera/design residuals.

Meter estimates assume the proof box's stated story height/depth. A single
uncalibrated photograph is not a building survey. Occlusion and weak baselines
are recorded rather than replaced by authored constants called measurements.
"""
import json,math,runpy,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.photo_match import project
from plan import generate


def parameters(shot):
    d=np.array(shot['target'])-np.array(shot['location']);d/=np.linalg.norm(d)
    return np.array((math.atan2(d[1],d[0]),math.atan2(d[2],np.linalg.norm(d[:2])),*shot['location'],math.log(shot['lens']),shot['roll']))


def ray(data,pixel):
    shot=data['shot'];c=np.array(shot['location']);forward=np.array(shot['target'])-c;forward/=np.linalg.norm(forward)
    right=np.cross(forward,(0,0,1));right/=np.linalg.norm(right);up=np.cross(right,forward);roll=shot['roll']
    right,up=right*math.cos(roll)+up*math.sin(roll),up*math.cos(roll)-right*math.sin(roll)
    x0,y0,x1,y1=data['crop'];w=x1-x0;h=y1-y0;f=w*shot['lens']/36
    return c,forward+right*((pixel[0]-x0-w/2)/f)+up*((h/2-pixel[1]+y0)/f)


def plane_point(data,pixel,axis,position):
    c,d=ray(data,pixel);t=(position-c[axis])/d[axis]
    if t<=0:raise ValueError('Photographic measurement behind camera')
    return c+t*d


def audit():
    config=runpy.run_path('src/split_photo_matches.py');matches=config['MATCHES'];cal=json.loads(Path('build/split/cameras-look.json').read_text());rows={}
    for name,data in cal.items():
        definition=matches[name];w=data['crop'][2]-data['crop'][0];h=data['crop'][3]-data['crop'][1]
        held=definition.get('held_out',[]);predicted=project(parameters(data['shot']),np.array([s['world'] for s in held]),w,h)[0] if held else []
        records=[]
        for s,uv in zip(held,predicted):
            measured=np.array(s['pixel'])-data['crop'][:2];records.append(dict(label=s['label'],measured_native=s['pixel'],projected_native=(uv+data['crop'][:2]).tolist(),error_pixels=float(np.linalg.norm(uv-measured))))
        seed=config['PAIR_SEEDS'][name];plan=generate(seed,house_type='split');b=plan['blocks'][1] if name.startswith('side_') else plan['blocks'][0]
        record=dict(seed=seed,structural_camera_rms_native=data['residual_rms_pixels'],native_crop_width=w,normalized_1100_camera_rms=data['residual_rms_pixels']*1100/w,estimated_lens_mm=data['shot']['lens'],camera_height_m=data['shot']['location'][2],held_out=records,held_out_rms_native=float(np.sqrt(np.mean([r['error_pixels']**2 for r in records]))) if records else None,scope='Corresponding upper wall corners calibrate pose; mismatched roofs/entries/parking remain held out and visible. Camera error is not whole-house similarity.')
        ridge={'side_pa':(618.5,209.5),'side_oh':(312,83)}.get(name)
        if ridge:
            # Gable-front photograph measures its ridge in the front gable
            # plane. Parallel ridges use the stated half-depth station.
            station=b.y0-b.rake if b.ridge_axis=='Y' else b.cy
            q=plane_point(data,ridge,1,station);run=b.width/2 if b.ridge_axis=='Y' else b.depth/2
            pitch=(q[2]-b.eave)/run*12
            record['roof_estimate']=dict(ridge_pixel=ridge,ray_intersection_m=q.tolist(),assumed_ridge_y_m=station,assumed_run_m=run,pitch_per_12=pitch,scope='Photo ray plus stated story/box-depth scale, not an independent meter survey; roof skin versus fascia uncertainty is included below.')
        else:record['roof_estimate']=dict(pitch_per_12=None,reason='The main roof is occluded or uses an added front-facing gable unlike the proof box. This view does not recover the main roof pitch from a fascia line.')
        if name=='foyer_pa':
            a,c,q=[plane_point(data,p,1,b.y0-b.rake) for p in ((383,83),(619,91),(503,27))]
            slopes=[float((q[2]-k[2])/abs(q[0]-k[0])*12) for k in (a,c)]
            record['roof_estimate']['visible_added_gable']=dict(pitch_per_12_sides=slopes,mean_per_12=sum(slopes)/2,scope='Added cross-gable only; left bearing partly leaf-obscured. Main roof remains unrecoverable. Different left/right estimates expose perspective/landmark uncertainty.')
        # Visible soffit bands are recorded in native pixels. Physical depth
        # is only bounded because fascia thickness and camera pitch covary.
        bands={'side_pa':((615,247),(615,250)),'side_oh':((440,146),(432,151)),'foyer_pa':((560,95),(560,99)),'foyer_oh':((720,151),(720,159))}
        a,c=bands[name];record['eave_observation']=dict(outer_underedge_pixel=a,wall_junction_pixel=c,visible_band_pixels=math.dist(a,c),depth_identifiability='Weak single-view estimate; fascia thickness, wall cantilever and rake/eave direction are separate. Do not call the band itself meter depth.')
        if name=='side_oh':
            left=plane_point(data,(188,142),1,b.y0-b.rake);right=plane_point(data,(449,148),1,b.y0-b.rake)
            depth=(b.x0-left[0]+right[0]-b.x1)/2
            record['eave_observation'].update(depth_estimate_m=float(depth),depth_estimate_in=float(depth/.0254),estimated_uncertainty_in=4.,method='Two roof-skin endpoints unprojected onto the front gable plane; average extension beyond wall corners. Rake depth is assumed; this estimates bearing-eave width.')
        else:
            record['eave_observation'].update(depth_estimate_m=None,reason='No clear transverse gable endpoint baseline. Fascia/soffit thickness and cantilever confound depth at this near-frontal angle; a meter depth is not claimed.',authored_depth_in=b.overhang/.0254)
        rows[name]=record
    out=dict(rows=rows,scope='Native pixel measurements, assumed-scale pitch estimates and explicit unresolved design residuals. No source photograph is used by a material generator.')
    Path('build/split/photo-audit.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:dict(camera=round(v['structural_camera_rms_native'],3),held_out=round(v['held_out_rms_native'],2) if v['held_out_rms_native'] else None,pitch=v['roof_estimate']['pitch_per_12']) for k,v in rows.items()},indent=2))


if __name__=='__main__':audit()
