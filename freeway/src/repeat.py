"""Independent seeded construction repeat in an isolated local build folder."""
import sys,subprocess,json,hashlib,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ASSET=HERE.parent

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    target=Path('build/repeat');target.mkdir(parents=True,exist_ok=True)
    # Reuse read-only native caches; the test exercises construction/export,
    # not a second GPU manufacture bake; all inputs are immutable for this check.
    (target/'build').mkdir(exist_ok=True);(target/'textures').mkdir(exist_ok=True)
    for link,source in [(target/'build/context',ASSET/'build/context'),(target/'textures/checkpoint',ASSET/'textures/checkpoint'),(target/'textures/ship',ASSET/'textures/ship'),(target/'textures/context',ASSET/'textures/context')]:
        if not link.exists():link.symlink_to(source,target_is_directory=True)
    cmd=[os.environ.get('BLENDER_BINARY','blender'),'-t','2','-b','--factory-startup','--python-exit-code','1','--python',str(HERE/'build.py'),'--','--out','build/Freeway.blend']
    with (target/'build.log').open('w') as log:subprocess.run(cmd,cwd=target,stdout=log,stderr=subprocess.STDOUT,check=True)
    # Re-run the original CPU field recipes in a separate directory, then
    # compare the generated PNG bytes independently of geometry construction.
    field_target=target/'fields';(field_target/'textures').mkdir(parents=True,exist_ok=True);(field_target/'build').mkdir(exist_ok=True)
    link=field_target/'textures/checkpoint'
    if not link.exists():link.symlink_to(ASSET/'textures/checkpoint',target_is_directory=True)
    with (target/'fields.log').open('w') as log:subprocess.run([sys.executable,str(HERE/'textures.py'),'--size','4096'],cwd=field_target,stdout=log,stderr=subprocess.STDOUT,check=True)
    fields=[]
    for original in sorted(Path('textures/source').glob('*.png')):
        copy=field_target/original;same=sha(original)==sha(copy);assert same,original
        fields.append(dict(file=str(original),bytes=original.stat().st_size,sha256=sha(original),identical=same))
    rows=[]
    for original in sorted(Path('export').rglob('*.bin')):
        if 'staging' in original.parts:continue
        copy=target/original
        assert copy.exists(),str(copy)
        same=sha(original)==sha(copy);rows.append(dict(file=str(original),bytes=original.stat().st_size,identical=same,sha256=sha(original)))
    assert all(r['identical'] for r in rows),[r['file'] for r in rows if not r['identical']]
    Path('build/repeat.json').write_text(json.dumps(dict(scope='Exact geometry/accessor buffer bytes across clean scene construction; native source caches reused, CPU fields exact, no GPU rebake',files=rows,fields=fields,all_identical=True),indent=2))
    print('REPEAT PASSED:',len(rows),'geometry buffers byte-identical')
if __name__=='__main__':main()
