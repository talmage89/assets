"""Optional second proxy material for transmission, sharing the same atlas."""
import copy

import numpy as np

from kit.detachable_verify import _image, sample


def split_transmission(doc, original):
    """Partition existing faces; never change coverage, UVs or vertex fields.

    Mixed paint/glass faces keep the coverage decoder. A second material can
    take only faces whose entire padded UV rectangle has no paint derivative.
    This conservative test can retain boundary glass on the first material.
    It does not reconstruct an interior removed by the proxy envelope.
    """
    if len(doc.data['materials']) != 1 or doc.stats()['draw_calls'] != 1:
        raise ValueError('Transmission partition requires a single proxy material/draw')
    native = [m for m in original.data['materials'] if
              m.get('extensions', {}).get('KHR_materials_transmission', {}).get('transmissionFactor', 0) > 0]
    if not native:
        raise ValueError('Transmission partition requires source glass')
    sides = {bool(m.get('doubleSided', False)) for m in native}
    iors = {m.get('extensions', {}).get('KHR_materials_ior', {}).get('ior', 1.5) for m in native}
    if len(sides) != 1 or len(iors) != 1:
        raise ValueError('Second proxy material requires one source glass culling/IOR policy')
    solid = doc.data['materials'][0]
    texture = solid['extensions']['KHR_materials_transmission']['transmissionTexture']['index']
    def pixels(index):
        return _image(doc.image(doc.data['textures'][index]['source']))
    transmission = pixels(texture)
    coverage = pixels(solid['occlusionTexture']['index']) if solid.get('extras', {}).get('lod_factory_coverage') else None
    glass = copy.deepcopy(solid)
    glass['name'] = 'LOD_Glass'
    glass['doubleSided'] = next(iter(sides))
    glass['extras'] = {'lod_transmission_partition': True}
    if solid.get('extras', {}).get('lamp_strength'):
        glass['extras']['lamp_strength'] = solid['extras']['lamp_strength']
    if not any(m.get('extensions', {}).get('KHR_materials_clearcoat', {}).get('clearcoatFactor', 0) > 0 for m in native):
        glass['extensions'].pop('KHR_materials_clearcoat', None)
    glass['extensions']['KHR_materials_ior'] = {'ior': next(iter(iors))}
    threshold = .5 * min(m['extensions']['KHR_materials_transmission']['transmissionFactor'] for m in native)
    probes = np.array([[1,0,0], [0,1,0], [0,0,1], [.5,.5,0], [.5,0,.5], [0,.5,.5], [1/3]*3])
    changed = retained = 0
    for mesh in doc.data['meshes']:
        result = []
        for primitive in mesh['primitives']:
            attrs, faces = doc.arrays(primitive)
            uv = attrs['TEXCOORD_0'][faces]
            values = sample(transmission, (probes @ uv).reshape(-1, 2))[:, 0].reshape(-1, len(probes))
            selected = np.median(values, axis=1) >= threshold
            if coverage is not None:
                height, width = coverage.shape[:2]
                for i in np.flatnonzero(selected):
                    lo = np.maximum(0, np.floor(uv[i].min(axis=0)*[width,height]-1).astype(int))
                    hi = np.minimum([width,height], np.ceil(uv[i].max(axis=0)*[width,height]+1).astype(int))
                    patch = coverage[lo[1]:hi[1], lo[0]:hi[0], 1:3]
                    if patch.size == 0 or patch.max() > .5/255:
                        selected[i] = False
            for material, take in [(0, ~selected), (1, selected)]:
                if not take.any():
                    continue
                part = copy.deepcopy(primitive)
                part['material'] = material
                used, remap = np.unique(faces[take], return_inverse=True)
                doc.replace(part, {k:v[used] for k,v in attrs.items()}, remap.reshape(-1,3).astype(np.uint32))
                result.append(part)
            changed += int(selected.sum())
            retained += int((~selected).sum())
        mesh['primitives'] = result
    if not changed or not retained:
        raise ValueError('Transmission partition needs both glass and opaque faces')
    doc.data['materials'].append(glass)
    if 'KHR_materials_ior' not in doc.data.setdefault('extensionsUsed', []):
        doc.data['extensionsUsed'].append('KHR_materials_ior')
    stats = doc.stats()
    return dict(glass_triangles=changed, mixed_or_opaque_triangles=retained,
                extra_maps=0, materials=stats['materials'], color_pass_draws=stats['draw_calls'],
                limitation='Geometry and baked interior coverage are unchanged')
