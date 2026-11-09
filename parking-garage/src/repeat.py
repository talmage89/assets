"""Isolated rebuild of form geometry and original graphic bytes.

There is no GPU bake at this checkpoint, so no texture-tolerance claim is made.
Native image resources remain immutable canonical inputs.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

HERE=Path(__file__).resolve().parent;ASSET=HERE.parent;ROOT=ASSET.parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    stage=ASSET/'build/repeat-repo'
    if stage.exists():shutil.rmtree(stage)
    folder=stage/'parking-garage';folder.mkdir(parents=True);shutil.copytree(HERE,folder/'src')
    for family in ('kit','ground','street-light','cars','trees'):(stage/family).symlink_to(ROOT/family,target_is_directory=True)
    (folder/'build').mkdir();(folder/'build/context').symlink_to(ASSET/'build/context-repeat',target_is_directory=True)
    env=dict(os.environ,TMPDIR=str(ASSET/'build/tmp'));Path(env['TMPDIR']).mkdir(parents=True,exist_ok=True)
    with (ASSET/'build/repeat.log').open('w') as log:
        subprocess.run([str(folder/'src/blender.sh'),'-b','--factory-startup','--python-exit-code','1','--python','src/repeat_worker.py'],cwd=folder,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
    wanted=[p for p in (ASSET/'export').rglob('*') if p.is_file() and p.suffix in ('.gltf','.bin') and not any(k in ('form','lookdev','final') for k in p.relative_to(ASSET/'export').parts)]
    wanted += list((ASSET/'textures/checkpoint').rglob('*.png'))
    wanted += [ASSET/'build'/n for n in ('manifest.json','modules.json','garage-101.json','garage-202.json','actors-101.json','actors-202.json','sites.json')]
    rows=[];mixed=[]
    for p in wanted:
        q=folder/p.relative_to(ASSET);assert q.exists(),q
        embedded='sites' in p.relative_to(ASSET).parts or p.name in ('actors-101.json','actors-202.json','sites.json')
        identical=p.read_bytes()==q.read_bytes()
        rows.append(dict(path=str(p.relative_to(ASSET)),bytes=p.stat().st_size,sha256=sha(p),repeated_sha256=sha(q),identical=identical,embedded=embedded))
        if embedded and p.suffix=='.gltf':mixed.append([str(p),str(q)])
        if embedded and p.suffix=='.json' and not identical:
            compare_manifest(json.loads(p.read_text()),json.loads(q.read_text()))
    pairs=ASSET/'build/embedded-repeat-pairs.json';pairs.write_text(json.dumps(mixed)+'\n')
    subprocess.run(['blender','-t','2','-b','--factory-startup','--python-exit-code','1','--python','src/embedded_repeat.py','--',
        '--pairs',str(pairs),'--out','build/embedded-repeat.json'],cwd=ASSET,stdout=subprocess.DEVNULL,check=True)
    report=dict(files=rows,passed=all(r['identical'] or r['embedded'] for r in rows),scope='Garage/module/graphics bytes exact; independently rebuilt car caches embedded in sites, exact noncar payloads plus 0.1% car triangles / 1mm bidirectional samples. GPU bake separate.')
    (ASSET/'build/repeat.json').write_text(json.dumps(report,indent=2)+'\n')
    assert report['passed'],[r['path'] for r in rows if not r['identical']]
    print('REPEAT PASS',len(rows),'files',sum(r['bytes'] for r in rows),'bytes',flush=True)


def compare_manifest(a,b,key=''):
    """Only resource totals inherited from cars may vary; plan stays exact."""
    counts={'triangles','context_triangles','actor_triangles','garage_car_triangles','surface_car_triangles','street_car_triangles',
            'unique_mesh_triangles','expanded_scene_triangles','gltf_bytes','bin_bytes','glb_bytes'}
    if isinstance(a,dict):
        assert a.keys()==b.keys(),key
        for k in a:compare_manifest(a[k],b[k],k)
    elif isinstance(a,list):
        assert len(a)==len(b),key
        for x,y in zip(a,b):compare_manifest(x,y,key)
    elif key in counts and isinstance(a,(int,float)):
        assert abs(a-b)<=max(abs(a),1)*.001,(key,a,b)
    else:assert a==b,(key,a,b)


if __name__=='__main__':main()
