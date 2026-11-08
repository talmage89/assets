"""Serial four-fix review from current and frozen accepted export packages."""
import argparse,json,sys
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
            prior+=R.render(stem,path,meta,views,out,a.width,a.samples)
        (out/'provenance.json').write_text(json.dumps(prior,indent=2))


if __name__=='__main__':main()
