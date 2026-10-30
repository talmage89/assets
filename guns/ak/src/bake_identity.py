"""Compare every decoded shipping texel with the accepted bake, without storing it.

GPU rounding can move a few 8-bit samples by one. Three modular checksums per
1024 samples locate up to two such changes in each channel block. Correcting
an IN-MEMORY comparison copy must reproduce the accepted full-image SHA-256.
Thus checksum collisions or unlocated differences fail closed. Neither PNGs
nor the GLB are ever rewritten. These checksums cannot reconstruct a texture
without an already near-identical bake; they are validation metadata.
"""
import argparse
import base64
import copy
import hashlib
import io
import json
from pathlib import Path
import struct
import zlib

import numpy as np
from PIL import Image

BASE = Path(__file__).resolve().parents[1]
BLOCK = 1024
PRIME = 65521
MAX_CHANGED_TEXELS = 128  # per map, including unused atlas pixels


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_glb(path):
    data = Path(path).read_bytes()
    assert struct.unpack_from('<III', data) == (0x46546C67, 2, len(data))
    offset = 12
    chunks = {}
    while offset < len(data):
        size, kind = struct.unpack_from('<II', data, offset)
        assert kind not in chunks and offset + 8 + size <= len(data)
        chunks[kind] = data[offset + 8:offset + 8 + size]
        offset += 8 + size
    assert offset == len(data)
    return json.loads(chunks[0x4E4F534A]), chunks[0x004E4942]


def view_bytes(g, binary, index):
    view = g['bufferViews'][index]
    start = view.get('byteOffset', 0)
    result = binary[start:start + view['byteLength']]
    assert len(result) == view['byteLength']
    return result


def export_signature(g, binary):
    """Exact content and JSON semantics; ignore only physical buffer allocation."""
    images = {im['bufferView'] for im in g['images']}
    layout = copy.deepcopy(g)
    for i, view in enumerate(layout['bufferViews']):
        view.pop('byteOffset', None)
        if i in images:
            del view['byteLength']
    for buffer in layout['buffers']:
        del buffer['byteLength']
    return dict(
        json_sha256=sha(json.dumps(layout, sort_keys=True, separators=(',', ':')).encode()),
        non_image_sha256=sha(b''.join(view_bytes(g, binary, i)
                                    for i in range(len(g['bufferViews'])) if i not in images)))


def decode(data):
    with Image.open(io.BytesIO(data)) as im:
        assert im.format == 'PNG' and im.mode in ('RGB', 'RGBA'), 'Expected 8-bit RGB(A) PNG'
        # Check bit depth explicitly: Pillow otherwise reduces 16-bit RGB to 8-bit.
        assert data[24] == 8, 'Expected 8-bit shipping map'
        return np.asarray(im).copy()


def moments(array):
    assert array.dtype == np.uint8 and array.ndim == 3
    assert array.shape[0] * array.shape[1] % BLOCK == 0
    rows = np.moveaxis(array, -1, 0).reshape(-1, BLOCK).astype(np.int64)
    x = np.arange(1, BLOCK + 1, dtype=np.int64)
    return np.stack([rows.sum(1), (rows * x).sum(1),
                     (rows * (x * x % PRIME)).sum(1)], axis=1) % PRIME


def texture_record(array):
    return dict(shape=list(array.shape), decoded_sha256=sha(array.tobytes()),
                moments_zlib_base64=base64.b64encode(zlib.compress(
                    moments(array).astype('<u2').tobytes(), 9)).decode('ascii'))


def compare_texture(array, reference):
    """Prove <=1/255 per component, <=128 changed texels, and exact remainder."""
    assert list(array.shape) == reference['shape'], 'Shipping texture shape changed'
    expected = np.frombuffer(zlib.decompress(base64.b64decode(
        reference['moments_zlib_base64'], validate=True)), '<u2').reshape(-1, 3).astype(np.int64)
    observed = moments(array)
    assert expected.shape == observed.shape
    delta = (expected - observed) % PRIME
    corrected = np.moveaxis(array, -1, 0).copy().reshape(-1, BLOCK)
    for row in np.flatnonzero(np.any(delta, axis=1)):
        a, b, c = map(int, delta[row])
        sign = a if a < PRIME // 2 else a - PRIME
        if abs(sign) == 1:
            x = b * sign % PRIME
            assert 1 <= x <= BLOCK and sign * x * x % PRIME == c, 'Bake exceeds rounding bound'
            edits = [(x, sign)]
        elif abs(sign) == 2:
            s = sign // 2
            total = b * s % PRIME
            edits = None
            for x in range(1, BLOCK + 1):
                y = (total - x) % PRIME
                if x < y <= BLOCK and s * (x * x + y * y) % PRIME == c:
                    edits = [(x, s), (y, s)]
                    break
            assert edits is not None, 'Bake exceeds rounding bound'
        elif sign == 0 and b:
            total = c * pow(b, -1, PRIME) % PRIME
            x = (total + b) * pow(2, -1, PRIME) % PRIME
            y = (total - b) * pow(2, -1, PRIME) % PRIME
            assert 1 <= x <= BLOCK and 1 <= y <= BLOCK and x != y, 'Bake exceeds rounding bound'
            edits = [(x, 1), (y, -1)]
        else:
            raise AssertionError('Bake exceeds sparse rounding bound')
        for x, d in edits:
            value = int(corrected[row, x - 1]) + d
            assert 0 <= value <= 255, 'Bake exceeds rounding bound'
            corrected[row, x - 1] = value
    accepted = np.moveaxis(corrected.reshape(array.shape[-1], *array.shape[:2]), 0, -1)
    assert sha(accepted.tobytes()) == reference['decoded_sha256'], 'Decoded bake differs beyond rounding bound'
    diff = np.abs(array.astype(np.int16) - accepted.astype(np.int16))
    count = int(np.any(diff, axis=2).sum())
    assert count <= MAX_CHANGED_TEXELS, 'Too many changed bake texels'
    return dict(maximum_per_channel=diff.max(axis=(0, 1)).tolist(), changed_texels=count,
                changed_per_channel=np.count_nonzero(diff, axis=(0, 1)).tolist(),
                decoded_sha256=sha(array.tobytes()), accepted_decoded_sha256=reference['decoded_sha256'])


def record(path, accepted_sha256):
    assert sha(Path(path).read_bytes()) == accepted_sha256, 'Not the accepted historical GLB'
    g, binary = read_glb(path)
    maps = {}
    for im in g['images']:
        data = view_bytes(g, binary, im['bufferView'])
        array = decode(data)
        assert array.shape == (2048, 2048, 4 if im['name'].endswith('BaseColor') else 3)
        maps[im['name']] = dict(texture_record(array), png_sha256=sha(data))
    assert set(maps) == {'T_Rill39_' + c for c in ('BaseColor', 'Normal', 'ORM')}
    return dict(accepted_glb_sha256=accepted_sha256, block_samples=BLOCK, prime=PRIME,
                maximum_component_difference=1, maximum_changed_texels_per_map=MAX_CHANGED_TEXELS,
                export=export_signature(g, binary), maps=maps)


def verify(path, reference):
    assert reference['block_samples'] == BLOCK and reference['prime'] == PRIME
    assert reference['maximum_component_difference'] == 1
    assert reference['maximum_changed_texels_per_map'] == MAX_CHANGED_TEXELS
    g, binary = read_glb(path)
    assert export_signature(g, binary) == reference['export'], 'Accepted GLB data or JSON semantics changed'
    images = {im['name']: im for im in g['images']}
    assert len(images) == len(g['images']) and images.keys() == reference['maps'].keys()
    return {name: compare_texture(decode(view_bytes(g, binary, im['bufferView'])), reference['maps'][name])
            for name, im in images.items()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record-from', required=True, type=Path)
    args = parser.parse_args()
    destination = BASE / 'src/accepted_bake.json'
    assert not destination.exists(), 'Never replace an accepted baseline'
    source = json.loads((BASE / 'src/accepted_detachable_geometry.json').read_text())
    result = record(args.record_from, source['main_sha256'])
    destination.write_text(json.dumps(result, indent=2) + '\n')
