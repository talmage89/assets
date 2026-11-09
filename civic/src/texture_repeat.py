"""Fresh private manufacture fields and GPU rebakes; canonical maps stay intact."""
import hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];LOCAL=ROOT/'civic'
SETS={'downtown':{'Masonry':2048,'MineralRoof':1024,'Finish':2048},
      'commercial':{'CMU':1024}}


def run(command,cwd,log):
    with log.open('w') as f:subprocess.run(list(map(str,command)),cwd=cwd,stdout=f,stderr=subprocess.STDOUT,check=True)


def main():
    stage=LOCAL/'build/texture-repeat'
    if '--bake-worker' in sys.argv:
        for family in SETS:
            folder=stage/family;args=['--roles','CMU'] if family=='commercial' else []
            run([os.environ.get('BLENDER','blender'),'-b','-t','4','--factory-startup','--python-exit-code','1',
                 '--python',ROOT/family/'src/textures.py','--','bake','--size','4096','--samples','1',*args],folder,stage/(family+'-bake.log'))
        return
    shutil.rmtree(stage,ignore_errors=True);stage.mkdir(parents=True)
    sources=[]
    for family in SETS:
        folder=stage/family;folder.mkdir();args=['--roles','CMU'] if family=='commercial' else []
        run([sys.executable,ROOT/family/'src/textures.py','source','--size','4096',*args],folder,stage/(family+'-source.log'))
        for p in sorted((folder/'build/procedural').glob('T_*.png')):
            canonical=LOCAL/'textures/shared'/family/'build/procedural'/p.name
            same=p.read_bytes()==canonical.read_bytes();assert same,p
            sources.append(dict(file=str(p.relative_to(stage)),exact=same,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    # Parent owns the lease until both serial Blender children have joined.
    subprocess.run([ROOT/'kit/with_gpu.sh',sys.executable,Path(__file__).resolve(),'--bake-worker'],check=True)
    maps=[]
    for family,roles in SETS.items():
        folder=stage/family
        for role,size in roles.items():
            asset=family.title()+role
            run([sys.executable,ROOT/'kit/downsample.py','--source','textures/bake','--out','textures/ship','--asset',asset,'--size',size],folder,stage/(asset+'-ship.log'))
            for p in sorted((folder/'textures/ship').glob('T_'+asset+'_*.png')):
                reference=LOCAL/'textures/shared'/family/'textures/ship'/p.name
                a=np.asarray(Image.open(reference).convert('RGBA'),dtype=np.int16)
                b=np.asarray(Image.open(p).convert('RGBA'),dtype=np.int16);assert a.shape==b.shape,p
                delta=np.abs(a-b);maximum=int(delta.max());mean=float(delta.mean()/255)
                passed=maximum<=1 and mean<=1e-5
                maps.append(dict(file=p.name,max_byte_delta=maximum,mean_normalized_error=mean,passed=passed));assert passed,maps[-1]
    import importlib.util
    spec=importlib.util.spec_from_file_location('_repeat_july',ROOT/'community-garden/src/groundcover.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.maps(ROOT,stage/'lawn')
    for p in sorted((stage/'lawn').glob('*.png')):
        same=p.read_bytes()==(LOCAL/'textures/lawn/ship'/p.name).read_bytes();assert same,p
        maps.append(dict(file=p.name,exact=same,passed=True))
    result=dict(passed=True,source_fields=sources,maps=maps,max_byte_delta_limit=1,mean_normalized_error_limit=1e-5,
        scope='Fresh 4096 manufacture and serial GPU rebake of the four civic-owned shared sets; July maps exact. Other native images remain read-only and hash-audited by make check.')
    (LOCAL/'build/texture-repeat.json').write_text(json.dumps(result,indent=2)+'\n')
    print('CIVIC TEXTURE REPEAT PASS',len(sources),'exact fields;',len(maps),'maps')


if __name__=='__main__':main()
