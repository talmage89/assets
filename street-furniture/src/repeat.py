"""Repeat both new deliveries with the accepted shared baked maps retained.

This is a byte determinism check of procedural geometry, UV packing, graphics
and stock glTF serialization. The full 4096 GPU bake is proven by the separate
clean build; this target does not claim bit-identical stochastic rebakes.
"""
import hashlib,json,subprocess,sys,os
from pathlib import Path
FAMILY=Path(__file__).resolve().parents[1];SIGNS=FAMILY.parent/'street-signs'
def snapshot():
    return {str(p.relative_to(FAMILY.parent)):dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for folder in (FAMILY/'export',SIGNS/'export/set') for p in sorted(folder.rglob('*')) if p.suffix in ('.gltf','.bin','.png')}
def main():
    before=snapshot();assert before
    generated=[*list((FAMILY/'export').rglob('*')),*list((SIGNS/'export/set').rglob('*')),*list((SIGNS/'build/set').glob('*'))]
    generated += [FAMILY/'build'/n for n in ('T_StreetFurniture_Checkpoint.png','T_StreetFurniture_GraphicsSource.png','graphics.json','game.blend','game.json','finalized.blend','uv.json','delivery.blend','manifest.json')]
    times={p:(p.stat().st_atime_ns,p.stat().st_mtime_ns) for p in generated if p.is_file()}
    cmds=[(FAMILY,[sys.executable,'src/graphics.py']),
      (FAMILY,['blender','-b','-t','4','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--out','build/game.blend']),
      (FAMILY,['blender','-b','-t','4','--factory-startup','--python-exit-code','1','--python','src/finalize.py','--','--source','build/game.blend','--out','build/finalized.blend','--config','src/bake_config.py','--report','build/uv.json','--size','2048','--margin','.001','--target-density','650']),
      (FAMILY,['blender','-b','-t','4','--factory-startup','--python-exit-code','1','--python','src/deliver.py','--']),
      (SIGNS,[sys.executable,'src/set_graphics.py','build/set']),
      (SIGNS,['blender','-b','-t','4','--factory-startup','--python-exit-code','1','--python','src/set_build.py','--','--out','build/set/Signs.blend'])]
    with (FAMILY/'build/repeat.log').open('w') as log:
        for cwd,cmd in cmds:subprocess.run(cmd,cwd=cwd,stdout=log,stderr=subprocess.STDOUT,check=True)
    after=snapshot();changed=[p for p in set(before)|set(after) if before.get(p)!=after.get(p)];report=dict(passed=not changed,files=len(after),bytes=sum(x['bytes'] for x in after.values()),changed=changed,scope=__doc__)
    (FAMILY/'build/repeat.json').write_text(json.dumps(report,indent=2));assert not changed,changed
    # Identical exported geometry/UV/graphics leaves the accepted bake and
    # render dependencies valid. Preserve their build timestamps so a later
    # `make check` does not start another unchanged GPU bake and render cycle.
    for path,(atime,mtime) in times.items():os.utime(path,ns=(atime,mtime))
    print('REPEAT PASSED',report['files'],'files /',report['bytes'],'bytes')
if __name__=='__main__':main()
