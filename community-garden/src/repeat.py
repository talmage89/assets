"""Fresh-scene deterministic rebuild at identical output paths; archive in build/."""
from pathlib import Path
import subprocess,sys,json,hashlib,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];ASSET=HERE.parent


def main():
    target=ASSET/'build/repeat';target.mkdir(parents=True,exist_ok=True)
    # Rebuild in the same relative output frame so deterministic files can
    # be compared as bytes, including URI strings and JSON serialization.
    baseline=target/'baseline'
    if baseline.exists():shutil.rmtree(baseline)
    files=[*sorted((ASSET/'export/final').glob('*.gltf')),*sorted((ASSET/'export/final').glob('*.bin')),
           *sorted((ASSET/'textures/ship').glob('*.png')),*sorted((ASSET/'textures/4k-plants').glob('*.png')),*sorted((ASSET/'textures/source-surfaces').glob('*.png')),
           ASSET/'build/pieces.json',*[ASSET/f'build/garden-{s}.json' for s in (117,229,341)],
           ASSET/'build/context/shed.glb',ASSET/'build/context/shed.json',ASSET/'build/context/chain/tile-report.json',ASSET/'build/surface-layout.json',*[ASSET/f'build/context/costs-{s}.json' for s in (117,229,341)],*sorted((ASSET/'build/context/chain').glob('*.png'))]
    for path in files:
        dst=baseline/path.relative_to(ASSET);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dst)
    commands=[['blender','-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(HERE/'context_build.py')],
              [sys.executable,str(ROOT/'fences/chain-link/src/mesh_tile.py'),'--out','build/context/chain'],
              ['blender','-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(HERE/'build.py'),'--','--out','build/gardens.blend'],
              ['blender','-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(HERE/'repeat_sites.py')]]
    with (target/'repeat.log').open('w') as log:
        for cmd in commands:subprocess.run(cmd,cwd=ASSET,check=True,stdout=log,stderr=subprocess.STDOUT)
    from groundcover import maps
    maps(ROOT,ASSET/'textures/ship')
    rows=[]
    for p in sorted((ASSET/'export/final').glob('*.gltf')):
        q=baseline/'export/final'/p.name;first=json.loads(p.read_text());second=json.loads(q.read_text());assert p.read_bytes()==q.read_bytes(),('glTF bytes differ',p.name)
        assert first==second,('glTF structure/accessors differ',p.name)
        b=p.with_suffix('.bin').read_bytes();c=q.with_suffix('.bin').read_bytes();assert b==c,('Geometry BIN differs',p.name)
        rows.append(dict(file=p.name,geometry_sha256=hashlib.sha256(b).hexdigest(),geometry_bytes=len(b),gltf_byte_identical=True))
    # The new atlas is analytic CPU output, so unlike GPU bakes it is promised
    # byte-identical. Regenerate it, do not compare a copied cache with itself.
    subprocess.run([sys.executable,str(HERE/'atlas.py')],cwd=ASSET,check=True)
    subprocess.run([sys.executable,str(ROOT/'kit/downsample.py'),'--source','textures/4k-plants','--out','textures/ship','--asset','GardenPlants','--size','1024'],cwd=ASSET,check=True)
    images=[]
    for p in (ASSET/'textures/ship').glob('T_GardenPlants_*.png'):
        q=baseline/'textures/ship'/p.name;assert p.read_bytes()==q.read_bytes();images.append(dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    subprocess.run([sys.executable,str(HERE/'surfaces.py')],cwd=ASSET,check=True)
    fields=[]
    for channel in ('BaseColor','ORM','Height'):
        p=ASSET/f'textures/source-surfaces/T_GardenSurfaces_{channel}.png';q=baseline/'textures/source-surfaces'/p.name
        assert p.read_bytes()==q.read_bytes(),('Authored surface field differs',p.name)
        fields.append(dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    # White-balance and fitted camera outputs are deterministic as well.
    if (ASSET/'build/matched-cameras.json').exists():
        photos=[ASSET/'build/matched-cameras.json',*sorted((ASSET/'build/photo-references').glob('*'))]
        before={p:p.read_bytes() for p in photos if p.is_file()}
        with (target/'calibration.log').open('w') as log:
            subprocess.run(['blender','-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(HERE/'match.py'),'--','--calibrate-only'],cwd=ASSET,check=True,stdout=log,stderr=subprocess.STDOUT)
        for path,data in before.items():
            assert path.read_bytes()==data,('Photographic calibration differs',path.name)
    exact=[]
    for path in files:
        original=baseline/path.relative_to(ASSET)
        assert path.read_bytes()==original.read_bytes(),('Deterministic file differs',str(path))
        exact.append(dict(path=str(path.relative_to(ASSET)),bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    result=dict(exact_files=exact,source_fields=fields,passed=True,geometry=rows,analytic_images=images,scope='fresh-scene private shed, garden and full-site glTF/BIN; analytic plant/lawn/chain/source fields and manifests compare byte for byte at identical relative paths; GPU bakes tested separately')
    (ASSET/'build/repeat.json').write_text(json.dumps(result,indent=2));print('REPEAT PASSED',len(rows),'glTF/BIN files and',len(images),'analytic maps')


if __name__=='__main__':main()
