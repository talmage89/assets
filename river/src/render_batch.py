"""One GPU-lock acquisition; serial fresh Blender workers and verified resume.

Each worker renders at most three views. SIGTERM is retried at most twice;
other failures stop immediately. No child survives the orchestrator.
"""
import argparse
import json
import os
import shlex
import signal
import subprocess
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
from package import bundle,presentation_recipe,sha,camera_signature
from plan import Plan
from views import views


def interrupted(signum,frame):raise KeyboardInterrupt


def execute(command,locked=False):
    child=subprocess.Popen(command,start_new_session=True,pass_fds=(9,) if locked else ())
    try:return child.wait()
    except BaseException:
        try:os.killpg(child.pid,signal.SIGTERM)
        except ProcessLookupError:pass
        try:child.wait(timeout=15)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid,signal.SIGKILL);child.wait()
        raise


def run(args):
    out=args.out;recipe=presentation_recipe();cache={}
    def current(path,source,camera=None,engine='CYCLES',before=False,fields=None):
        if not path.is_file() or not path.with_suffix('.json').is_file():return False
        try:meta=json.loads(path.with_suffix('.json').read_text())
        except (OSError,ValueError):return False
        if meta.get('image_sha256')!=sha(path) or meta.get('width')!=args.width or meta.get('samples')!=args.samples:return False
        if camera is not None:
            actual=meta.get('camera',{})
            if before:actual=camera_signature(actual);camera=camera_signature(camera)
            if actual!=json.loads(json.dumps(camera)):return False
        if before:return meta.get('accepted_revision')=='4f09582'
        if source not in cache:cache[source]=bundle(source)
        return (meta.get('recipe_sha256')==recipe and meta.get('bundle_sha256')==cache[source]
                and meta.get('engine')==engine and meta.get('source_fields_sha256',{})==(fields or {}))
    jobs=[]
    for seed in (101,202):
        source=Path(f'export/RiverCrossing-{seed}.gltf')
        plan=Plan(**json.loads(Path(f'build/RiverCrossing-{seed}.json').read_text())['plan']);definitions=views(seed,plan)
        order=list(dict.fromkeys(['hero','abutment','riffle','bar',*definitions]))
        names=[n for n in order if n in definitions and not current(out/str(seed)/(n+'.png'),source,definitions[n])]
        for i in range(0,len(names),3):jobs.append(['--seeds',str(seed),'--shots',*names[i:i+3]])
        if not current(out/str(seed)/'eevee.png',source,definitions['hero'],'BLENDER_EEVEE'):
            jobs.append(['--seeds',str(seed),'--shots','_none','--eevee'])
        names=[n for n,camera in definitions.items() if not current(Path(f'renders/fixes/before/{seed}/{n}.png'),None,camera,before=True)]
        for i in range(0,len(names),3):jobs.append(['--seeds',str(seed),'--shots',*names[i:i+3],'--auxiliary-only','--with-baseline'])
    if not current(out/'modules.png',Path('export/RiverModules.gltf')):jobs.append(['--auxiliary-only','--modules'])
    calibration=json.loads(Path('build/photo-calibration.json').read_text())
    fields={p.name:sha(p) for p in Path('build/bank-fields/source').glob('*.png')}
    for name,row in calibration.items():
        source=Path(f'export/RiverCrossing-{row["seed"]}.gltf')
        if not current(Path(f'renders/checkpoint-matches/{name}.png'),source,row['shot']):
            jobs.append(['--auxiliary-only','--matches','--match-names',name])
        if not current(Path(f'renders/source-matches/{name}.png'),source,row['shot'],fields=fields):
            jobs.append(['--auxiliary-only','--matches','--match-names',name,'--source-fields',
                         '--match-out','renders/source-matches'])
    # Resolve both crossings' remaining appearance risks first. Baselines
    # reuse the original light and can wait until the new views are judged.
    def priority(job):
        if '--with-baseline' in job:return 4
        if '--auxiliary-only' in job:return 3
        if '--eevee' in job:return 2
        return 0 if 'hero' in job else 1
    jobs.sort(key=priority)
    if not jobs:
        print('RENDER_BATCH_CURRENT');(out/'.stamp').touch();return
    if args.plan:
        print(json.dumps(jobs,indent=2));return
    if args.verify_only:raise RuntimeError(('Incomplete or stale render workers',jobs))
    if not args.locked:
        command=[str(REPO/'kit/with_gpu.sh'),sys.executable,str(HERE/'render_batch.py'),
            '--locked','--out',str(out),'--width',str(args.width),'--samples',str(args.samples)]
        code=execute(command)
        if code:raise subprocess.CalledProcessError(code,command)
        return
    blender=shlex.split(os.environ.get('BLENDER','blender -t 1'))
    for i,job in enumerate(jobs):
        command=blender+['-b','--factory-startup','--python-exit-code','1','--python','src/render.py','--',
            '--out',str(out),'--width',str(args.width),'--samples',str(args.samples),*job]
        print('RENDER_WORKER',i+1,len(jobs),' '.join(job),flush=True)
        for attempt in range(3):
            code=execute(command,locked=True)
            if code==0:break
            if code not in (-15,143) or attempt==2:raise subprocess.CalledProcessError(code,command)
            print('RENDER_WORKER_SIGTERM_RETRY',attempt+1,flush=True)
    # Re-evaluate actual image, source, recipe and camera receipts before the
    # stamp. This also detects an input edit during the batch.
    if presentation_recipe()!=recipe:raise RuntimeError('Render recipe changed during the batch')
    args.verify_only=True;run(args)
    print('RENDER_BATCH_COMPLETE',len(jobs),flush=True)


if __name__=='__main__':
    signal.signal(signal.SIGTERM,interrupted)
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('renders/checkpoint'))
    ap.add_argument('--width',type=int,default=1280);ap.add_argument('--samples',type=int,default=32)
    ap.add_argument('--locked',action='store_true');ap.add_argument('--verify-only',action='store_true')
    ap.add_argument('--plan',action='store_true');ap.add_argument('--kit-worker',action='store_true')
    # kit.checkpoint_rules appends the ordinary Blender command after '--'.
    # This dispatcher supplies its own bounded Blender commands instead.
    argv=sys.argv[1:]
    if '--kit-worker' in argv:argv=argv[:argv.index('--')]
    run(ap.parse_args(argv))
