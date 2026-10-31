"""Positive rounding cases and negative regressions for the accepted-bake gate."""
import copy
import io
from pathlib import Path
import sys
import unittest

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bake_identity as B
from reviewed_rebaseline import reviewed_record


class TextureIdentityTests(unittest.TestCase):
    def setUp(self):
        self.image = np.random.default_rng(39).integers(10, 245, (64, 64, 4), dtype=np.uint8)
        self.reference = B.texture_record(self.image)

    def check_edits(self, edits):
        changed = self.image.copy()
        for y, x, channel, delta in edits:
            changed[y, x, channel] = int(changed[y, x, channel]) + delta
        before = changed.copy()
        result = B.compare_texture(changed, self.reference)
        np.testing.assert_array_equal(changed, before)
        self.assertEqual(result['changed_texels'], len({(y, x) for y, x, _, _ in edits}))
        return result

    def test_exact_decoded_pixels(self):
        self.assertEqual(self.check_edits([])['maximum_per_channel'], [0, 0, 0, 0])

    def test_each_channel_including_specular_alpha(self):
        result = self.check_edits([(0, 10 + c, c, 1) for c in range(4)])
        self.assertEqual(result['maximum_per_channel'], [1, 1, 1, 1])

    def test_two_equal_sign_errors_per_block(self):
        for delta in (-1, 1):
            with self.subTest(delta=delta):
                self.check_edits([(0, 0, 0, delta), (15, 63, 0, delta)])

    def test_opposite_sign_errors_per_block(self):
        for delta in (-1, 1):
            with self.subTest(delta=delta):
                self.check_edits([(0, 0, 0, delta), (15, 63, 0, -delta)])

    def test_multiple_channels_one_texel(self):
        self.check_edits([(0, 0, c, 1) for c in range(4)])

    def test_two_levels_are_rejected_in_every_channel(self):
        for c in range(4):
            for delta in (-2, 2):
                with self.subTest(channel=c, delta=delta):
                    with self.assertRaises(AssertionError):
                        self.check_edits([(0, 0, c, delta)])

    def test_unrecoverable_changes_fail_closed(self):
        with self.assertRaises(AssertionError):
            self.check_edits([(0, i, 0, 1) for i in range(3)])

    def test_final_sha_catches_modular_checksum_collision(self):
        # Third finite difference has zero sum and first/second moments.
        changed = self.image.copy()
        for x, delta in enumerate((1, -3, 3, -1)):
            changed[0, x, 0] = int(changed[0, x, 0]) + delta
        np.testing.assert_array_equal(B.moments(changed), B.moments(self.image))
        with self.assertRaisesRegex(AssertionError, 'Decoded bake'):
            B.compare_texture(changed, self.reference)

    def test_changed_texel_limit(self):
        image = np.full((512, 512, 3), 100, np.uint8)
        reference = B.texture_record(image)
        for i in range(129):
            image.reshape(-1, 3)[i * B.BLOCK, 0] += 1
        with self.assertRaisesRegex(AssertionError, 'Too many'):
            B.compare_texture(image, reference)

    def test_dimension_or_alpha_loss(self):
        for image in (self.image[:, :, :3], self.image.reshape(128, 32, 4)):
            with self.assertRaisesRegex(AssertionError, 'shape'):
                B.compare_texture(image, self.reference)

    def test_png_compression_has_no_effect(self):
        images = []
        for level in (0, 9):
            stream = io.BytesIO()
            Image.fromarray(self.image).save(stream, format='PNG', compress_level=level)
            images.append(stream.getvalue())
            self.assertEqual(B.compare_texture(B.decode(stream.getvalue()), self.reference)['changed_texels'], 0)
        self.assertNotEqual(images[0], images[1])

    def test_record_rejects_nonaccepted_glb(self):
        with self.assertRaisesRegex(AssertionError, 'historical GLB'):
            B.record(Path(__file__), '0' * 64)


class ExportIdentityTests(unittest.TestCase):
    def setUp(self):
        self.doc = dict(buffers=[dict(byteLength=20)],
                        bufferViews=[dict(buffer=0, byteOffset=0, byteLength=4),
                                     dict(buffer=0, byteOffset=4, byteLength=16)],
                        images=[dict(name='Map', bufferView=1, mimeType='image/png')],
                        nodes=[dict(name='Root', translation=[0, 0, 0])],
                        accessors=[dict(bufferView=0, count=1, type='SCALAR', componentType=5126)],
                        materials=[dict(name='Atlas', alphaMode='OPAQUE')],
                        samplers=[dict(minFilter=9987)], animations=[dict(name='Idle')])
        self.binary = b'abcd' + b'image data......'
        self.reference = B.export_signature(self.doc, self.binary)

    def test_allocation_only_changes_are_ignored(self):
        doc = copy.deepcopy(self.doc)
        doc['bufferViews'][1].update(byteOffset=8, byteLength=20)
        doc['buffers'][0]['byteLength'] = 28
        self.assertEqual(B.export_signature(doc, b'abcdPAD!' + b'x' * 20), self.reference)

    def test_nonimage_data_is_exact(self):
        self.assertNotEqual(B.export_signature(self.doc, b'Abcd' + self.binary[4:]), self.reference)

    def test_json_semantics_are_exact(self):
        changes = [('nodes', 'translation', [0, .01, 0]), ('accessors', 'count', 2),
                   ('materials', 'alphaMode', 'BLEND'), ('samplers', 'minFilter', 9729),
                   ('animations', 'name', 'Other')]
        for collection, key, value in changes:
            with self.subTest(collection=collection):
                doc = copy.deepcopy(self.doc)
                doc[collection][0][key] = value
                self.assertNotEqual(B.export_signature(doc, self.binary), self.reference)


class ReviewedChangeTests(unittest.TestCase):
    def setUp(self):
        self.old=dict(accepted_glb_sha256='old',export={'exact':'geometry'},
            block_samples=B.BLOCK,prime=B.PRIME,maximum_component_difference=1,
            maximum_changed_texels_per_map=B.MAX_CHANGED_TEXELS,
            maps={'map':dict(decoded_sha256='decoded',png_sha256='png')})
        self.new=copy.deepcopy(self.old);self.new['accepted_glb_sha256']='new'

    def test_reviewed_change_keeps_old_identity(self):
        row=reviewed_record(self.old,self.new,'manifest','Reviewed paint correction')
        self.assertEqual(row['historical_handoff_sha256'],'old')
        self.assertEqual(row['reviewed_changes'][0]['previous_glb_sha256'],'old')
        self.assertEqual(row['reviewed_changes'][0]['reviewed_glb_sha256'],'new')

    def test_geometry_cannot_be_rebaselined(self):
        self.new['export']['exact']='changed'
        with self.assertRaisesRegex(AssertionError,'Geometry'):
            reviewed_record(self.old,self.new,'manifest','paint')

    def test_tolerance_cannot_be_rebaselined(self):
        for key in ('block_samples','prime','maximum_component_difference','maximum_changed_texels_per_map'):
            with self.subTest(key=key):
                new=copy.deepcopy(self.new);new[key]+=1
                with self.assertRaisesRegex(AssertionError,'tolerance'):
                    reviewed_record(self.old,new,'manifest','paint')


if __name__ == '__main__':
    unittest.main()
