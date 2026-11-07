"""Render serial fresh Blender chunks while inheriting one GPU lease.

Long-lived Cycles scenes with this town's many native materials have stalled
after repeated views. Fresh processes bound their lifetime and memory. The
outer kit/with_gpu.sh owns FD 9 for the complete set; children inherit it.
"""
import argparse,hashlib,json,os,shlex,subprocess,sys
from pathlib import Path
from external import bundle

SCENES={101:['terminal','hero','above','alignment','barrier','guardrail_end',
             'sign_structure','south_sign','pier_girders','gore',
             'terminal_controls','rail_repair'],
        202:['hero','above','alignment','sound_wall','cable_median']}

def fresh(path,source,args):
    try:
        data=json.loads(path.with_suffix('.json').read_text())
        return (not args.source_fields and path.is_file()
                and data['frame_sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
                and data['recipe_sha256']==hashlib.sha256(Path('src/render.py').read_bytes()).hexdigest()
                and data['bundle_sha256']==bundle(source)
                and all(r['bundle_sha256']==bundle(r['source']) for r in data.get('context',[]))
                and data['width']==args.width and data['samples']==args.samples
                and data['engine']==args.engine)
    except (OSError,KeyError,ValueError):return False

def main():
    p=argparse.ArgumentParser();p.add_argument('--blender',default='blender -t 2')
    p.add_argument('--python',default='src/render.py');p.add_argument('render_args',nargs=argparse.REMAINDER)
    a=p.parse_args();raw=a.render_args
    if raw and raw[0]=='--':raw=raw[1:]
    q=argparse.ArgumentParser();q.add_argument('--source',default='export/Freeway-101.gltf')
    q.add_argument('--out',required=True);q.add_argument('--width',type=int,default=1400)
    q.add_argument('--samples',type=int,default=32);q.add_argument('--engine',default='CYCLES')
    q.add_argument('--seeds',type=int,nargs='+',default=[101,202]);q.add_argument('--shots',nargs='+')
    q.add_argument('--camera-file');q.add_argument('--source-fields',action='store_true');r=q.parse_args(raw)
    shared=['--out',r.out,'--width',str(r.width),'--samples',str(r.samples),'--engine',r.engine]
    jobs=[]
    if r.camera_file:
        for name,row in json.loads(Path(r.camera_file).read_text()).items():
            if r.shots and name not in r.shots:continue
            if fresh(Path(r.out)/(name+'.png'),row.get('source',r.source),r):continue
            jobs.append(shared+['--camera-file',r.camera_file,'--shots',name]+(['--source-fields'] if r.source_fields else []))
    else:
        for seed in r.seeds:
            names=[n for n in SCENES[seed] if (not r.shots or n in r.shots)
                   and not fresh(Path(r.out)/str(seed)/(n+'.png'),f'export/Freeway-{seed}.gltf',r)]
            for i in range(0,len(names),3):jobs.append(shared+['--seeds',str(seed),'--shots']+names[i:i+3])
    try:os.fstat(9);fds=(9,)
    except OSError:fds=()
    for i,job in enumerate(jobs):
        print(f'SERIAL RENDER CHUNK {i+1}/{len(jobs)}: {job}',flush=True)
        subprocess.run(shlex.split(a.blender)+['-b','--factory-startup','--python-exit-code','1','--python',a.python,'--']+job,check=True,pass_fds=fds)
    print('SERIAL RENDER SET COMPLETE',len(jobs),flush=True)
if __name__=='__main__':main()
