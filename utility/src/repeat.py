"""Clean geometry repeat, deterministic fields and an independent GPU rebake."""
import argparse,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main(blender):
    out=Path('build/repeat');shutil.rmtree(out,ignore_errors=True);out.mkdir(parents=True)
    fields={p.name:sha(p) for p in Path('build/fields').glob('*.png')}
    config=json.loads(Path('build/fields/fields.json').read_text());bake=json.loads(Path('build/bake.json').read_text())
    field_stage=out/'fields-stage';field_stage.mkdir()
    with (out/'fields.log').open('w') as log:subprocess.run(['python3',str(HERE/'textures.py'),'source','--size',str(config['size']),'--wear',str(config['wear'])],cwd=field_stage,stdout=log,stderr=subprocess.STDOUT,check=True)
    assert fields=={p.name:sha(p) for p in (field_stage/'build/fields').glob('*.png')},'Original field repeat differs'
    with (out/'geometry.log').open('w') as log:subprocess.run([blender,'-b','-t','4','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--out',str(out/'utility.blend')],stdout=log,stderr=subprocess.STDOUT,check=True)
    rows=[]
    for stem in ('utility','street-101','street-102','street-103','street-104'):
        a=Path('build')/(stem+'.glb');b=out/(stem+'.glb');assert a.read_bytes()==b.read_bytes(),(stem,'geometry/material/texture package differs')
        rows.append(dict(source=str(a),bytes=a.stat().st_size,sha256=sha(a),byte_identical=True))
    # The independent bake reads the exact same original fields but writes only
    # beneath this fresh repeat directory. It cannot replace a delivery map.
    stage=out/'bake-stage';(stage/'build').mkdir(parents=True)
    (stage/'build/fields').symlink_to((field_stage/'build/fields').resolve(),target_is_directory=True)
    with (out/'bake.log').open('w') as log:
        subprocess.run([str(ROOT/'kit/with_gpu.sh'),blender,'-b','-t','4','--factory-startup','--python-exit-code','1','--python',str(HERE/'textures.py'),'--','bake','--size',str(config['size']),'--samples',str(bake['samples'])],cwd=stage,stdout=log,stderr=subprocess.STDOUT,check=True)
        subprocess.run(['python3',str(ROOT/'kit/downsample.py'),'--source',str(stage/'textures/bake'),'--out',str(stage/'textures/ship'),'--asset','Utility','--size','2048'],stdout=log,stderr=subprocess.STDOUT,check=True)
    import numpy as np
    sys.path.insert(0,str(ROOT));from kit.image_io import read_png
    textures={}
    for channel in ('BaseColor','Normal','ORM'):
        a=Path('textures/ship')/f'T_Utility_{channel}.png';b=stage/'textures/ship'/a.name
        delta=(read_png(a)-read_png(b))*255;maximum=float(abs(delta).max());rmse=float(np.sqrt(np.mean(delta*delta)))
        assert maximum<=2.0001 and rmse<=.02,(channel,maximum,rmse)
        textures[channel]=dict(maximum_delta_255=maximum,rmse_255=rmse,byte_identical=a.read_bytes()==b.read_bytes())
    report=dict(geometry=rows,original_field_pngs=len(fields),fields_byte_identical=True,independent_rebake=textures,texture_tolerance=dict(maximum_255=2,rmse_255=.02))
    Path('build/repeat-check.json').write_text(json.dumps(report,indent=2));print('UTILITY REPEAT PASS',sum(r['bytes'] for r in rows),'package bytes;',textures)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--blender',default=os.environ.get('BLENDER','blender'));main(p.parse_args().blender)
