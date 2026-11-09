"""Opt-in fixed UV domains for shared-map reductions, including trim sheets.

Chart boundaries are identified by geometric edge incidence and exact UV/material
corner records, independently of normal splits. Pinning their endpoints retains
the complete domain, including concave boundaries and holes. Interior collapses
must retain UV orientation and area after FLOAT serialization. No UV is clamped.
"""
from contextlib import contextmanager
from contextvars import ContextVar
from collections import Counter, defaultdict
import numpy as np

_ENABLED = ContextVar('lod_preserve_uv_regions', default=False)


@contextmanager
def policy(enabled=False):
    if type(enabled) is not bool:
        raise ValueError('preserve_uv_regions must be a boolean')
    token = _ENABLED.set(enabled)
    try:
        yield
    finally:
        _ENABLED.reset(token)


def enabled():
    return _ENABLED.get()


def determinant(uv):
    edges = np.asarray(uv, dtype=np.float32).astype(float)[..., 1:, :] - np.asarray(uv, dtype=np.float32).astype(float)[..., :1, :]
    return edges[..., 0, 0]*edges[..., 1, 1] - edges[..., 0, 1]*edges[..., 1, 0]


def boundaries(attrs, faces, geo=None):
    """Count oriented domain edges; normal-only splits do not split a chart."""
    if geo is None:
        _, geo = np.unique(attrs['POSITION'], axis=0, return_inverse=True)
    keys = sorted(k for k in attrs if k.startswith('TEXCOORD_'))
    groups = defaultdict(list)
    for face in faces:
        material = tuple(attrs['_LOD_MATERIAL'][face[0]]) if '_LOD_MATERIAL' in attrs else ()
        # A continuous but folded UV sheet has a domain edge at its fold too.
        # Opposite signs cannot be treated as one injective chart: their signed
        # areas cancel and an interior fold could otherwise grow out of domain.
        orientation=tuple(int(np.sign(determinant(attrs[k][face]))) for k in keys)
        for a, b in zip(face, np.roll(face, -1)):
            ga, gb = int(geo[a]), int(geo[b])
            if ga > gb:
                a, b = b, a
                ga, gb = gb, ga
            signature = (material, orientation, *(tuple(attrs[k][a])+tuple(attrs[k][b]) for k in keys))
            groups[ga, gb].append(signature)
    return {edge: values for edge, values in groups.items()
            if len(values) != 2 or values[0] != values[1]}


def pins(attrs, faces, geo):
    edges = boundaries(attrs, faces, geo)
    fixed = {v for edge in edges for v in edge}
    # Inherited constant/flat UVs are legitimate (LED swatches, unprinted metal).
    # Retain those complete triangles instead of trading one degeneration for
    # another elsewhere in the same material/layer's aggregate count.
    for key in attrs:
        if key.startswith('TEXCOORD_'):
            flat = np.abs(determinant(attrs[key][faces])) <= 1e-12
            fixed.update(map(int, geo[faces[flat]].ravel()))
    return fixed


def valid_face(old, new):
    for key in old:
        if not key.startswith('TEXCOORD_'):
            continue
        before, after = float(determinant(old[key])), float(determinant(new[key]))
        if abs(before) <= 1e-12:
            if not np.array_equal(np.float32(old[key]), np.float32(new[key])):
                return False
        elif abs(after) <= 1e-12 or before*after <= 0:
            return False
    if 'TANGENT' in new:
        tangent = np.float32(new['TANGENT']).astype(float)
        normal = np.float32(new['NORMAL']).astype(float)
        if np.any(np.linalg.norm(tangent[:, :3], axis=1) < .9998):
            return False
        if np.any(np.abs(np.einsum('ij,ij->i', tangent[:, :3], normal)) > 1e-3):
            return False
    return True


def audit(source, faces, candidate, triangles, *, allow_removed=False):
    """Independent per-component boundary multiset check on stored arrays."""
    def records(attrs, ff):
        _, geo = np.unique(attrs['POSITION'], axis=0, return_inverse=True)
        positions = {int(g): tuple(p) for g, p in zip(geo, attrs['POSITION'])}
        return Counter((positions[a], positions[b], signature)
                       for (a, b), signatures in boundaries(attrs, ff, geo).items()
                       for signature in signatures)
    before, after = records(source, faces), records(candidate, triangles)
    missing, added=sum((before-after).values()),sum((after-before).values())
    return dict(passed=added == 0 and (allow_removed or missing == 0),
                source_boundary_records=sum(before.values()),
                removed_boundary_records=missing, new_boundary_records=added,
                changed_boundary_records=missing+added)
