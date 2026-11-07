"""Exact deterministic outputs; independent GPU rebake under the kit tolerance."""
import sys,json,hashlib,shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.compare_textures import compare


def deterministic(root):
    files=[p for p in (root/'export/final').glob('*') if p.suffix in ('.gltf','.bin') or p.name.endswith('.frames.json')]
    files += [p for p in (root/'build/procedural').iterdir() if p.suffix in ('.png','.json') or p.name=='.stamp']
    files += list((root/'build/flat-trim-source').glob('*.png'))
    files += [p for p in (root/'build/context').iterdir() if p.suffix in ('.glb','.json')]
    files += [root/'textures/ship/.stamp',root/'build/source-geometry.json']
    result={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    for path in (root/'export/final').glob('*.gltf'):
        for row in json.loads(path.read_text()).get('images',[]):
            if row['uri'].startswith('../../textures/ship/'):continue
            target=path.parent/row['uri'];result['shared:'+row['uri']]=hashlib.sha256(target.read_bytes()).hexdigest()
    return result


def preserve():
    files=[p for folder in ('export/final','build/embedded','textures/ship') for p in Path(folder).rglob('*') if p.is_file()]
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}


path=Path('build/repeat-before.json')
if sys.argv[1]=='snapshot':
    Path('build/repeat-check.json').write_text(json.dumps(dict(passed=False,status='incomplete')))
    path.write_text(json.dumps(dict(exact=deterministic(Path('.')),original=preserve()),indent=2))
    folder=Path('build/repeat');shutil.rmtree(folder,ignore_errors=True);(folder/'build').mkdir(parents=True)
    (folder/'build/context').mkdir()
    for name in ('ground','trees','fences'):
        shared=Path('build')/name;target=(Path('..')/name).resolve()
        if shared.exists():assert shared.is_symlink() and shared.resolve()==target,shared
        else:shared.symlink_to(target,target_is_directory=True)
    (folder/'textures').mkdir()
else:
    before=json.loads(path.read_text());after=deterministic(Path('build/repeat'))
    different=[p for p in set(before['exact'])|set(after) if before['exact'].get(p)!=after.get(p)]
    texture=compare('textures/ship','build/repeat/textures/ship',max_delta=2,rmse_limit=.02)
    # The kit comparator checks RGB. Alpha is also procedural coverage and must
    # remain byte-identical rather than inherit the RGB tolerance.
    import numpy as np
    from PIL import Image
    alpha=[]
    for p in sorted(Path('textures/ship').glob('T_*.png')):
        a=Image.open(p);b=Image.open(Path('build/repeat/textures/ship')/p.name)
        if 'A' in a.getbands():
            equal=np.array_equal(np.asarray(a.getchannel('A')),np.asarray(b.getchannel('A')))
            alpha.append(dict(file=p.name,byte_identical=equal));assert equal,alpha[-1]
    Path('build/texture-repeat-check.json').write_text(json.dumps(texture,indent=2))
    preserved=preserve()==before['original']
    report=dict(passed=not different and preserved and texture['passed'],exact_files=len(after),different=different,exact_sha256=after,
                original_exports_unchanged=preserved,coverage_alpha=alpha,gpu_textures=texture,
                scope='Factory-startup geometry rebuilt from regenerated procedural fields and independent GPU bake. glTF, BIN, frame receipts, source PNGs, bake-input PNGs, source geometry receipts, empty stamps, layout and referenced canonical shared maps compare byte for byte. GPU maps use kit RGB limits; embedded GLBs and image-hash/size receipts depend on those maps and are validated by the normal export audit, not falsely promised byte-identical. Own context geometry is rebuilt too. Ground/tree/fence canonical deliveries remain read-only inputs; .blend containers, stochastic renders and image-dependent hash/size reports are not falsely promised byte-identical.')
    Path('build/repeat-check.json').write_text(json.dumps(report,indent=2));assert report['passed'],report
    print('REPEAT PASS',len(after),'exact files; GPU textures max delta',max(r['max_byte_delta'] for r in texture['textures']),'max byte RMSE',max(r['rmse_bytes'] for r in texture['textures']))
