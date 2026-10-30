"""Independent control exports: only textures may change, never the binding."""
import hashlib,json,sys,io
import bpy
from PIL import Image
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit.gltf import GLB
from kit.detachable_verify import samplers
from lookdev import SITES
from look_review import SITES as PARTS
from kit.detachable_textures import _mask
from kit.detachable_clusters import _expand

def texture_arrays(g):
    m=g.json['materials'][0];p=m['pbrMetallicRoughness']
    refs={'BaseColor':p['baseColorTexture'],'Normal':m['normalTexture'],'ORM':p['metallicRoughnessTexture']}
    return {name:np.asarray(Image.open(io.BytesIO(g.image(g.json['textures'][ref['index']]['source'])))).astype(np.int16) for name,ref in refs.items()}

def main():
    bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
    masks={site:np.zeros((2048,2048),bool) for site in SITES}
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH':continue
        relevant=[site for site in SITES if ob.name.startswith(PARTS[site])]
        if not relevant:continue
        mesh=ob.data;mesh.calc_loop_triangles()
        coverage=_mask(mesh,mesh.uv_layers['BakeUV'],range(len(mesh.loops)),np.array([0,0]),(2048,2048),2048)
        for site in relevant:masks[site]|=np.flipud(coverage)
    masks={site:_expand(mask,12) for site,mask in masks.items()}
    selected=tuple(sys.argv[sys.argv.index('--sites')+1].split(',')) if '--sites' in sys.argv else SITES
    assert set(selected)<=set(SITES)
    canonical=GLB(BASE/'export/lmg.glb');records={};canonical_images=texture_arrays(canonical)
    for site in selected:
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
        assert g.json['materials']==canonical.json['materials'],(site,'material settings')
        image_audit={}
        for channel,pixels in texture_arrays(g).items():
            delta=np.max(abs(pixels-canonical_images[channel]),axis=2)
            outside=delta[~masks[site]]
            # <=3 quantized levels accommodates subpixel bake noise; all
            # larger changes must stay on the named parts and their guards.
            assert int(outside.max())<=3,(site,channel,'unrelated texture changes',int(outside.max()))
            image_audit[channel]=dict(changed_pixels_over_3=int((delta>3).sum()),maximum_change_outside_part_guard=int(outside.max()))
        assert any(r['changed_pixels_over_3'] for r in image_audit.values()),(site,'no use-layer difference')
        ledger=json.loads((BASE/'build/controls'/site/'high.json').read_text())
        assert ledger['omitted_site']==site and ledger['wear']==1
        report=json.loads((BASE/'build/controls'/site/'baked/bake-report.json').read_text())
        assert report['size']==4096 and report['samples']>=32
        for channel in ('BaseColor','BaseColorAlpha','Roughness','Metallic','AO','MaterialAO','Normal'):
            assert report[channel]['alpha_missed_interior_texels']==0,(site,channel)
        records[site]=dict(passed=True,geometry_and_animation_arrays_identical=True,attributes_checked=checked,
                           texture_changes_confined_to_named_parts=image_audit,clips=19,bake_size=4096,bake_samples=report['samples'],sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    output='control-verification.json' if selected==SITES else 'control-verification-partial.json'
    (BASE/'build'/output).write_text(json.dumps(dict(passed=True,controls=records),indent=2))
    print(str(len(selected))+' WEAR CONTROLS: identical geometry, UVs, normals, weights, nodes, bind frames, clips and samplers',flush=True)
if __name__=='__main__':main()
