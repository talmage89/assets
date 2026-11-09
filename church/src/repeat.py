"""Deterministic own geometry/maps; native library files remain immutable."""
import hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ASSET=HERE.parent


def main():
    stage=ASSET/'build/repeat';shutil.rmtree(stage,ignore_errors=True);(stage/'build').mkdir(parents=True)
    log=ASSET/'build/repeat.log'
    with log.open('w') as out:
        subprocess.run([sys.executable,str(HERE/'textures.py')],cwd=stage,stdout=out,stderr=subprocess.STDOUT,check=True)
        subprocess.run([sys.executable,str(HERE/'dependencies.py')],cwd=stage,stdout=out,stderr=subprocess.STDOUT,check=True)
        subprocess.run(['blender','-b','-t','4','--factory-startup','--python-exit-code','1','--python',str(HERE/'build.py')],cwd=stage,stdout=out,stderr=subprocess.STDOUT,check=True)
        # Photographic preparation/calibration is deterministic too. References
        # stay local; this link does not copy them into another delivery.
        (stage/'refs').symlink_to(ASSET/'refs',target_is_directory=True)
        subprocess.run([sys.executable,str(HERE/'matches.py')],cwd=stage,stdout=out,stderr=subprocess.STDOUT,check=True)
    compared=[];errors=[]
    def uri(value,source,target):
        resolved=(source.parent/value).resolve()
        if resolved.is_relative_to(stage):resolved=ASSET/resolved.relative_to(stage)
        return Path(os.path.relpath(resolved,target.parent)).as_posix()
    # Relocate only relative image URIs into the original package frame. This
    # removes the independent directory's path depth, not content differences.
    replacements={}
    for path in sorted((stage/'export').rglob('*.gltf')):
        target=ASSET/path.relative_to(stage);d=json.loads(path.read_text())
        for row in d.get('images',[]):
            old=row['uri'];row['uri']=uri(old,path,target);replacements[old]=row['uri']
        path.write_text(json.dumps(d,separators=(',',':'))+'\n')
    def relocated(value):
        if isinstance(value,dict):return {k:relocated(v) for k,v in value.items()}
        if isinstance(value,list):return [relocated(v) for v in value]
        return replacements.get(value,value) if isinstance(value,str) else value
    files=[*sorted((stage/'export').rglob('*.*')),*sorted((stage/'textures/ship').glob('*.png'))]
    files += [stage/'build'/s for s in ('plan-101.json','plan-202.json','metrics.json','letters.json','dependencies.json','matched-cameras.json','photo-balance.json')]
    for path in files:
        accepted=ASSET/path.relative_to(stage)
        if path.suffix=='.json':
            candidate=json.dumps(relocated(json.loads(path.read_text())),sort_keys=True,separators=(',',':')).encode()
            baseline=json.dumps(json.loads(accepted.read_text()),sort_keys=True,separators=(',',':')).encode()
        else:candidate=path.read_bytes();baseline=accepted.read_bytes()
        same=candidate==baseline
        compared.append(dict(file=str(path.relative_to(stage)),bytes=path.stat().st_size,exact=same))
        if not same:errors.append(str(accepted))
    receipt=dict(passed=not errors,scope='All church, site, range and module glTF/BIN/metadata, plans, metrics, calibration and analytic maps; glTF image URIs relocated to canonical directory, JSON keys canonicalized. Native actors are immutable original inputs. Blend containers and Cycles sampling excluded.',files=compared,errors=errors)
    (ASSET/'build/repeat.json').write_text(json.dumps(receipt,indent=2))
    assert not errors,errors
    print('PASS',len(compared),'deterministic geometry/map payloads,',sum(r['bytes'] for r in compared),'bytes')


if __name__=='__main__':main()
