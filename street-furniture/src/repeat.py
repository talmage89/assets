"""Rebuild both new exports and compare every external delivery byte.

Existing STOP/blades and other families are never build targets here.
"""
import hashlib,json,subprocess,sys
from pathlib import Path
FAMILY=Path(__file__).resolve().parents[1];SIGNS=FAMILY.parent/'street-signs'

def snapshot():
    paths=[p for folder in (FAMILY/'export',SIGNS/'export/set') for p in folder.rglob('*') if p.suffix in ('.gltf','.bin','.png')]
    return {str(p.relative_to(FAMILY.parent)):dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted(paths)}

def main():
    before=snapshot();assert before,'Build the checkpoint first'
    log=FAMILY/'build/repeat.log'
    with log.open('w') as output:
        for cwd,cmd in [(FAMILY,[sys.executable,'src/graphics.py']),
           (FAMILY,['blender','-b','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--out','build/StreetFurniture.blend']),
           (SIGNS,[sys.executable,'src/set_graphics.py','build/set']),
           (SIGNS,['blender','-b','--factory-startup','--python-exit-code','1','--python','src/set_build.py','--','--out','build/set/Signs.blend'])]:
            subprocess.run(cmd,cwd=cwd,stdout=output,stderr=subprocess.STDOUT,check=True)
    after=snapshot();changed=[k for k in set(before)|set(after) if before.get(k)!=after.get(k)]
    report=dict(passed=not changed,files=len(after),bytes=sum(v['bytes'] for v in after.values()),changed=changed,scope=__doc__)
    (FAMILY/'build/repeat.json').write_text(json.dumps(report,indent=2));assert not changed,changed
    print('REPEAT PASSED',report['files'],'files /',report['bytes'],'byte-identical bytes')
if __name__=='__main__':main()
