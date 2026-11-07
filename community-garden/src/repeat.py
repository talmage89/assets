"""Independent clean-scene repeat in an isolated family-local build cache."""
from pathlib import Path
import subprocess,sys,json,hashlib,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];ASSET=HERE.parent


def normalized(path):
    d=json.loads(path.read_text())
    # Working-directory depth changes relative image URIs, not resource identity.
    for row in d.get('images',[]):
        p=path.parent/row['uri'];row['uri']='sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()
    return d


def main():
    target=ASSET/'build/repeat';target.mkdir(parents=True,exist_ok=True)
    for folder in ('build/context','textures/checkpoint'):
        dst=target/folder
        if dst.exists():shutil.rmtree(dst)
        shutil.copytree(ASSET/folder,dst)
    cmd=['blender','-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(HERE/'build.py'),'--','--out','build/gardens.blend']
    with (target/'repeat.log').open('w') as log:subprocess.run(cmd,cwd=target,check=True,stdout=log,stderr=subprocess.STDOUT)
    if all((ASSET/f'export/checkpoint/Site_{s}.gltf').exists() for s in (117,229,341)):
        with (target/'sites.log').open('w') as log:
            subprocess.run(['blender','-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(HERE/'repeat_sites.py')],cwd=target,check=True,stdout=log,stderr=subprocess.STDOUT)
    rows=[]
    for p in sorted((ASSET/'export/checkpoint').glob('*.gltf')):
        q=target/'export/checkpoint'/p.name;first=normalized(p);second=normalized(q)
        assert first==second,('glTF structure/accessors differ',p.name)
        b=p.with_suffix('.bin').read_bytes();c=q.with_suffix('.bin').read_bytes();assert b==c,('Geometry BIN differs',p.name)
        rows.append(dict(file=p.name,geometry_sha256=hashlib.sha256(b).hexdigest(),geometry_bytes=len(b),gltf_equal_after_canonical_image_uri_normalization=True))
    # The new atlas is analytic CPU output, so unlike GPU bakes it is promised
    # byte-identical. Regenerate it, do not compare a copied cache with itself.
    subprocess.run([sys.executable,str(HERE/'atlas.py')],cwd=target,check=True)
    images=[]
    for p in (ASSET/'textures/checkpoint').glob('*.png'):
        q=target/'textures/checkpoint'/p.name;assert p.read_bytes()==q.read_bytes();images.append(dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    result=dict(passed=True,geometry=rows,analytic_images=images,scope='fresh-scene garden/native-neighborhood geometry and analytic CPU textures; native inputs retained, no GPU rebake at form checkpoint')
    (ASSET/'build/repeat.json').write_text(json.dumps(result,indent=2));print('REPEAT PASSED',len(rows),'glTF/BIN files and',len(images),'analytic maps')


if __name__=='__main__':main()
