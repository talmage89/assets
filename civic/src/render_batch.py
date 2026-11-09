"""One lease, fresh serial Blender workers, validated resumable captures."""
import argparse,hashlib,json,os,signal,subprocess,sys
from pathlib import Path
SHOTS={'101':'hero,above,entry,cornice,police,scale,flag,hero-fixed,front,side,back,top',
       '202':'hero,above,bays,interior,tower,scale,scupper,hero-fixed,front,side,back,top'}
ACTIVE=None


def stop(signum,frame):
    # Unwind Popen.wait's internal lock before joining a terminated child.
    raise SystemExit(128+signum)


def current(path,width,samples):
    if not path.exists() or not path.with_suffix('.json').exists():return False
    d=json.loads(path.with_suffix('.json').read_text())
    if d.get('width')!=width or d.get('samples')!=samples:return False
    for key,file in [('render_recipe_sha256','render.py'),('sheet_recipe_sha256','sheets.py')]:
        if key in d and d[key]!=hashlib.sha256(Path('src',file).read_bytes()).hexdigest():return False
    sources=d.get('sources',[dict(path=d.get('source'),sha256=d.get('source_sha256'))])
    for row in sources:
        p=Path(row['path']);p=p if p.exists() else Path('..')/p
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:return False
    if 'context_recipe_sha256' in d:
        recipe=hashlib.sha256(b''.join(Path('src',n).read_bytes() for n in ('town.py','neighborhood.py','actors.py','library.py','sites.py','geo.py','turf.py'))).hexdigest()
        if recipe!=d['context_recipe_sha256']:return False
    return True


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='renders/final');p.add_argument('--width',type=int,default=1400);p.add_argument('--samples',type=int,default=40);p.add_argument('--matches',action='store_true');a=p.parse_args()
    signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
    common=[os.environ.get('BLENDER','blender'),'-b','-t','4','--factory-startup','--python-exit-code','1','--python','src/render.py','--','--out',a.out,'--width',str(a.width),'--samples',str(a.samples)]
    jobs=[]
    if a.matches:
        for name in json.loads(Path('build/matched-cameras.json').read_text()):jobs.append(([Path(a.out)/(name+'.png')],['--matches','--shots',name]))
    else:
        for seed,names in SHOTS.items():
            for name in names.split(','):jobs.append(([Path(a.out)/seed/(name+'.png')],['--seeds',seed,'--shots',name]))
        jobs.append(([Path('renders/eevee/202/hero.png')],['--seeds','202','--shots','hero','--engine','BLENDER_EEVEE','--out','renders/eevee']))
        jobs.append(([Path(a.out)/(name+'.png') for name in ('modules','range','scale')],['--sheets-only']))
    global ACTIVE
    for paths,args in jobs:
        if all(current(path,a.width,a.samples) for path in paths):print('REUSE verified',paths,flush=True);continue
        print('CAPTURE',paths,flush=True);ACTIVE=subprocess.Popen(common+args)
        try:code=ACTIVE.wait()
        except BaseException:
            ACTIVE.terminate()
            try:ACTIVE.wait(timeout=25)
            except subprocess.TimeoutExpired:ACTIVE.kill();ACTIVE.wait()
            ACTIVE=None;raise
        ACTIVE=None
        if code:raise subprocess.CalledProcessError(code,common+args)


if __name__=='__main__':main()
