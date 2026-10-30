"""Independent control exports: only textures may change, never the binding."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit.gltf import GLB
from kit.detachable_verify import samplers
from lookdev import SITES

def main():
    canonical=GLB(BASE/'export/lmg.glb');records={}
    for site in SITES:
        path=BASE/'build/controls'/site/'export/lmg.glb';g=GLB(path)
        assert g.json['nodes']==canonical.json['nodes'],site
        assert len(g.json['meshes'])==len(canonical.json['meshes'])
        checked=0
        for a,b in zip(g.json['meshes'],canonical.json['meshes']):
            assert len(a['primitives'])==len(b['primitives'])
            for p,q in zip(a['primitives'],b['primitives']):
                assert p['attributes'].keys()==q['attributes'].keys()
                for key in p['attributes']:
                    assert np.array_equal(g.accessor(p['attributes'][key]),canonical.accessor(q['attributes'][key])),(site,key)
                    checked+=1
                assert np.array_equal(g.accessor(p['indices']),canonical.accessor(q['indices']))
        for a,b in zip(g.json['skins'],canonical.json['skins']):
            assert a['joints']==b['joints']
            assert np.array_equal(g.accessor(a['inverseBindMatrices']),canonical.accessor(b['inverseBindMatrices']))
        assert len(g.json['animations'])==len(canonical.json['animations'])==19
        for a,b in zip(g.json['animations'],canonical.json['animations']):
            assert a['name']==b['name'] and a['channels']==b['channels']
            for p,q in zip(a['samplers'],b['samplers']):
                assert p.get('interpolation')==q.get('interpolation')
                for key in ('input','output'):assert np.array_equal(g.accessor(p[key]),canonical.accessor(q[key])),(site,a['name'],key)
        assert samplers(g)==samplers(canonical)
        ledger=json.loads((BASE/'build/controls'/site/'high.json').read_text())
        assert ledger['omitted_site']==site and ledger['wear']==1
        report=json.loads((BASE/'build/controls'/site/'baked/bake-report.json').read_text())
        assert report['size']==4096 and report['samples']>=32
        for channel in ('BaseColor','BaseColorAlpha','Roughness','Metallic','AO','MaterialAO','Normal'):
            assert report[channel]['alpha_missed_interior_texels']==0,(site,channel)
        records[site]=dict(passed=True,geometry_and_animation_arrays_identical=True,attributes_checked=checked,
                           clips=19,bake_size=4096,bake_samples=report['samples'],sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    (BASE/'build/control-verification.json').write_text(json.dumps(dict(passed=True,controls=records),indent=2))
    print('NINE WEAR CONTROLS: identical geometry, UVs, normals, weights, nodes, bind frames, clips and samplers',flush=True)
if __name__=='__main__':main()
