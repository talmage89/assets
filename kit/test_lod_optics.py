"""Fresh-Blender transmission partition; exact fields, source optics, no maps."""
import copy
import json
import sys
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from kit.lod_io import Document
from kit.lod_optics import split_transmission


class TransmissionPartition(unittest.TestCase):
    def test_real_bake_and_five_fresh_imports(self):
        import bpy
        from kit.test_lod_factory import fixture
        from kit.lod_atlas import bake
        from kit.lod_factory import apply
        from kit.lod_io import digest
        out = ROOT/'build/lod-optics-bake-test'
        out.mkdir(parents=True,exist_ok=True)
        source,target,colors,metals = fixture(out)
        before = Document(source).dependencies()
        path = out/'proxy.gltf'
        report = bake(target,source,path,128,proxy=True,projection_m=.02,
                      supersample=2,factory_paint=True,separate_transmission=True)
        target.save(path)
        doc = Document(path)
        self.assertEqual(Document(source).dependencies(),before)
        self.assertEqual(doc.stats()['materials'],2)
        self.assertEqual(doc.stats()['draw_calls'],2)
        self.assertEqual(doc.stats()['triangles'],48)
        self.assertEqual(len(doc.data['images']),8)
        for preset in colors:
            bpy.ops.wm.read_factory_settings(use_empty=True)
            bpy.ops.import_scene.gltf(filepath=str(path),import_pack_images=False)
            paint = apply(preset,lights=False)
            self.assertAlmostEqual(paint.node_tree.nodes['Factory metallic'].inputs[1].default_value,metals[preset])
            glass = bpy.data.materials['LOD_Glass']
            self.assertIsNone(glass.node_tree.nodes.get('Factory delta'))
            for lights in (False,True):
                apply(preset,lights=lights)
                for m in [paint,glass]:
                    bs = next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
                    self.assertAlmostEqual(bs.inputs['Emission Strength'].default_value,
                                           m['lamp_strength'] if lights else 0)
        (out/'proof.json').write_text(json.dumps(dict(passed=True,source_dependencies=before,
            proxy_sha256=digest(path),partition=report['separate_transmission'],
            presets=list(colors),lights=[False,True],stats=doc.stats()),indent=2)+'\n')

    def test_materials_and_exact_corner_fields(self):
        out = Path(__file__).resolve().parents[1]/'build/lod-optics-test'
        out.mkdir(parents=True, exist_ok=True)
        coverage = np.zeros((8,8,3), np.uint8)
        coverage[:,:,0] = 255
        coverage[:,:4,1:] = 153
        transmission = np.zeros_like(coverage)
        transmission[:,4:,:] = 255
        for name, pixels in [('coverage',coverage),('transmission',transmission)]:
            Image.fromarray(pixels).save(out/(name+'.png'))
        proxy = dict(name='Proxy',occlusionTexture=dict(index=0),
                     pbrMetallicRoughness=dict(baseColorFactor=[1,1,1,1]),
                     extensions={'KHR_materials_transmission':dict(transmissionFactor=1,transmissionTexture=dict(index=1)),
                                 'KHR_materials_clearcoat':dict(clearcoatFactor=1)},
                     extras=dict(paint_decode='reference_plus_coverage_delta',
                                 lod_factory_coverage='occlusion G paint / B clean metallic',lamp_strength=8))
        data = dict(asset=dict(version='2.0'),scene=0,scenes=[dict(nodes=[0])],
                    nodes=[dict(name='Proxy',mesh=0)],
                    meshes=[dict(primitives=[dict(attributes={},indices=0,material=0)])],
                    materials=[proxy],images=[dict(uri='coverage.png'),dict(uri='transmission.png')],
                    textures=[dict(source=0),dict(source=1)],accessors=[],bufferViews=[],buffers=[])
        stub = out/'stub.gltf'
        stub.write_text(json.dumps(data))
        doc = Document(stub)
        attrs = dict(POSITION=np.array([[0,0,0],[1,0,0],[0,1,0],[2,0,0],[3,0,0],[2,1,0],
                                       [4,0,0],[5,0,0],[4,1,0]],np.float32),
                     NORMAL=np.tile([0,0,1],(9,1)).astype(np.float32),
                     TEXCOORD_0=np.array([[.05,.2],[.3,.2],[.05,.8],[.7,.2],[.95,.2],[.7,.8],
                                          [.4,.2],[.95,.2],[.7,.8]],np.float32),
                     COLOR_0=np.arange(36,dtype=np.float32).reshape(9,4)/36)
        doc.replace(doc.data['meshes'][0]['primitives'][0],attrs,np.arange(9,dtype=np.uint32).reshape(3,3))
        source = Document(stub)
        source.data['materials'] = [dict(doubleSided=True,extensions={
            'KHR_materials_transmission':dict(transmissionFactor=1),
            'KHR_materials_ior':dict(ior=1.52)})]
        before = copy.deepcopy(doc.data['materials'][0])
        images = copy.deepcopy(doc.data['images'])
        result = split_transmission(doc,source)
        self.assertEqual(result['glass_triangles'],1)
        self.assertEqual(result['mixed_or_opaque_triangles'],2)
        self.assertEqual(result['extra_maps'],0)
        self.assertEqual(doc.data['images'],images)
        self.assertEqual(doc.data['materials'][0],before)
        glass = doc.data['materials'][1]
        self.assertTrue(glass['doubleSided'])
        self.assertEqual(glass['extensions']['KHR_materials_ior']['ior'],1.52)
        self.assertNotIn('paint_decode',glass['extras'])
        self.assertEqual(glass['extras']['lamp_strength'],8)
        self.assertNotIn('KHR_materials_clearcoat',glass['extensions'])
        for i,p in enumerate(doc.data['meshes'][0]['primitives']):
            a,f = doc.arrays(p)
            self.assertEqual(p['material'],i)
            for key in attrs:
                wanted = [0,1,2,6,7,8] if i == 0 else [3,4,5]
                np.testing.assert_array_equal(a[key][f].reshape(-1,attrs[key].shape[1]),attrs[key][wanted])


if __name__ == '__main__':
    unittest.main(argv=['test_lod_optics'])
