"""Serial four-fix review from current and frozen accepted export packages."""
import argparse,hashlib,json,shutil,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
import render as R


def main():
    args=sys.argv[sys.argv.index('--')+1:]
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('renders/finish-pass1'))
    p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=32);p.add_argument('--before',action='store_true');a=p.parse_args(args)
    rows=[]
    for stem in ('Park-101','Park-202'):
        path=Path('export')/(stem+'.gltf');meta=json.loads(path.with_suffix('.json').read_text())
        views={k:v for k,v in R.shot_views(stem,meta).items() if k in (('hero','row') if stem=='Park-101' else ('hero',))}
        rows+=R.render(stem,path,meta,views,a.out,a.width,a.samples)
    name='street-2007';c=json.loads(Path('build/cameras.json').read_text())[name];v=dict(c['shot'])
    v.update(fixed_camera=True,review_landmarks=c['landmarks_world_m'],review_subject_nodes=c['subject_nodes'],
             light=dict(sun_energy=5,sky_strength=.12,sky_saturation=.35,angle_degrees=.65,direction=(.5,.5,-1),exposure=.10))
    rows+=R.render('Park-101',Path('export/Park-101.gltf'),json.loads(Path('export/Park-101.json').read_text()),{name:v},a.out,a.width,a.samples)
    (a.out/'provenance.json').write_text(json.dumps(rows,indent=2))
    if a.before:
        prior=[];out=Path('renders/finish-before')
        for stem in ('Park-101','Park-202'):
            path=Path('build/round4-before/export')/(stem+'.gltf');meta=json.loads(path.with_suffix('.json').read_text())
            views={r['shot']:dict(r['camera'],light=r['light'],fixed_camera=True,fixed_matrix=r['camera_matrix_world']) for r in rows if r['stem']==stem}
            # Reuse byte-verified historical frames only with identical
            # optics and all eight light controls; never enlarge a panel.
            historical=Path('renders/age-pass3');old_rows=json.loads((historical/'provenance.json').read_text()) if (historical/'provenance.json').exists() else []
            packed=Path('build/round4-before/build/embedded')/(stem+'.glb')
            digest=hashlib.sha256(packed.read_bytes()).hexdigest() if packed.is_file() else None
            for shot in list(views):
                old=next((r for r in old_rows if r['stem']==stem and r['shot']==shot),None)
                current=next(r for r in rows if r['stem']==stem and r['shot']==shot)
                frame=historical/stem/(shot+'.png')
                if not old or old['sha256']!=digest or not frame.exists() or old['camera_parameters']!=current['camera_parameters']:continue
                delta=max(abs(x-y) for p,q in zip(old['camera_matrix_world'],current['camera_matrix_world']) for x,y in zip(p,q))
                keys=('direction','sun_energy','sky_strength','exposure','angle_degrees','sky_saturation','camera_sky_strength','camera_sky_saturation')
                if delta>1e-6 or any(old['light'][k]!=current['light'][k] for k in keys):continue
                target=out/stem/(shot+'.png');target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(frame,target)
                prior.append(dict(old,reused_verified_frame=str(frame)));del views[shot]
            if views:prior+=R.render(stem,path,meta,views,out,a.width,a.samples)
        (out/'provenance.json').write_text(json.dumps(prior,indent=2))


if __name__=='__main__':main()
