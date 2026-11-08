"""Independent 4096 source regeneration / locked GPU rebake / shipping compare."""
import hashlib,json,os,subprocess
from pathlib import Path


def run(args):subprocess.run(args,check=True)


def main():
    root=Path('build/texture-repeat');root.mkdir(parents=True,exist_ok=True)
    python=os.environ.get('PYTHON','python3');blender=os.environ.get('BLENDER','blender')
    run([python,'src/textures.py','--out',str(root/'source')])
    source=[]
    for p in sorted(Path('textures/source').glob('*')):
        if not p.is_file() or p.name.startswith('.'):continue
        q=root/'source'/p.name;assert p.read_bytes()==q.read_bytes(),('Source field changed',p)
        source.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    run(['../kit/with_gpu.sh',blender,'-b','-t','2','--factory-startup','--python-exit-code','1','--python','../kit/flat_bake.py','--',
         '--source',str(root/'source'),'--out',str(root/'4k'),'--name','Manufactured','--coverage','4.8768','--height-distance','.012','--size','4096','--samples','8'])
    run([python,'../kit/downsample.py','--source',str(root/'4k'),'--out',str(root/'ship'),'--asset','Manufactured','--size','2048'])
    run([python,'../kit/compare_textures.py','--reference','textures/ship','--candidate',str(root/'ship'),'--out','build/texture-repeat-check.json'])
    Path('build/texture-source-repeat.json').write_text(json.dumps(dict(passed=True,files=source),indent=2))


if __name__=='__main__':main()
