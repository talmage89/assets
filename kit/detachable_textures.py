"""Lossless, nonrotating subsets of an already baked atlas.

All moves are integer source pixels. UV scale is positive and uniform, so
surface sampling, tangent direction and tangent handedness are preserved.
No modeling, unwrapping, baking or image resampling takes place here.
"""
import json
import math
import struct
from pathlib import Path

import numpy as np

from kit import uv
from kit.image_io import read_png, write_png

CHANNELS = ('BaseColor', 'Normal', 'ORM')
PADDING = 2


def _pack(rectangles, size):
    """Deterministic MaxRects, no rotation; None means this layout cannot fit."""
    if sum(w*h for w,h in rectangles) > size*size or any(max(w,h)>size for w,h in rectangles):
        return None
    free = [(0, 0, size, size)]
    placed = {}
    for index, (width, height) in sorted(enumerate(rectangles),
            key=lambda row: (-max(row[1]), -row[1][0]*row[1][1], row[0])):
        candidates = [(min(w-width, h-height), max(w-width, h-height), y, x, i)
                      for i, (x, y, w, h) in enumerate(free)
                      if width <= w and height <= h]
        if not candidates:
            return None
        _, _, y, x, _ = min(candidates)
        placed[index] = (x, y)
        remaining = []
        for fx, fy, fw, fh in free:
            if x >= fx+fw or x+width <= fx or y >= fy+fh or y+height <= fy:
                remaining.append((fx, fy, fw, fh))
                continue
            if x > fx: remaining.append((fx, fy, x-fx, fh))
            if x+width < fx+fw: remaining.append((x+width, fy, fx+fw-x-width, fh))
            if y > fy: remaining.append((fx, fy, fw, y-fy))
            if y+height < fy+fh: remaining.append((fx, y+height, fw, fy+fh-y-height))
        remaining = sorted(set(remaining))
        free = [a for a in remaining if not any(a != b and
                b[0] <= a[0] and b[1] <= a[1] and
                a[0]+a[2] <= b[0]+b[2] and a[1]+a[3] <= b[1]+b[3]
                for b in remaining)]
    return [placed[i] for i in range(len(rectangles))]


def _mask(mesh, layer, loops, origin, shape, source_size):
    """Texel centers on this island, plus the exact bilinear sampling footprint."""
    width, height = shape
    mask = np.zeros((height, width), bool)
    loop_set = set(loops)
    coords = np.array([d.uv[:] for d in layer.data])*source_size-origin
    for tri in mesh.loop_triangles:
        if tri.loops[0] not in loop_set: continue
        points = coords[list(tri.loops)]
        lo = np.maximum(np.floor(points.min(axis=0)-.5).astype(int), 0)
        hi = np.minimum(np.ceil(points.max(axis=0)+.5).astype(int), (width, height))
        if np.any(hi <= lo): continue
        yy, xx = np.mgrid[lo[1]:hi[1], lo[0]:hi[0]]
        p = np.stack((xx+.5, yy+.5), axis=-1)
        a, b, c = points
        cross = lambda v, w: v[..., 0]*w[..., 1]-v[..., 1]*w[..., 0]
        det = cross(b-a, c-a)
        if abs(det) < 1e-15: continue
        s = cross(p-a, c-a)/det; t = cross(b-a, p-a)/det
        inside = (s >= -1e-7) & (t >= -1e-7) & (s+t <= 1+1e-7)
        mask[lo[1]:hi[1], lo[0]:hi[0]] |= inside
        # Very thin triangles can miss every pixel center. Conservative footprint:
        # a texel square participates if it intersects the triangle expanded by
        # half a pixel in each axis (separating-axis test).
        hit = np.ones(xx.shape, bool)
        for u, v in ((a,b), (b,c), (c,a)):
            edge = v-u
            value = cross(edge, p-u)*np.sign(det)
            hit &= value >= -.5*(abs(edge[0])+abs(edge[1]))-1e-7
        mask[lo[1]:hi[1], lo[0]:hi[0]] |= hit
    if not mask.any(): raise ValueError('UV island has no sampleable surface')
    # A point inside a triangle can sample the four neighboring centers.
    expanded = mask.copy()
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            expanded[max(0,dy):height+min(0,dy), max(0,dx):width+min(0,dx)] |= \
                mask[max(0,-dy):height-max(0,dy), max(0,-dx):width-max(0,dx)]
    return expanded


def _dilate(values, valid):
    """Extend only this island's sampling footprint, never other atlas surfaces."""
    # Stable nearest-in-Chebyshev-distance propagation; every map uses identical
    # ownership. Padding copies normals verbatim (no filtering/renormalization).
    values = values.copy(); valid = valid.copy()
    height, width = valid.shape
    while not valid.all():
        old = valid.copy()
        for dy, dx in ((-1,0),(0,-1),(0,1),(1,0),(-1,-1),(-1,1),(1,-1),(1,1)):
            ys = slice(max(0,dy), height+min(0,dy)); xs = slice(max(0,dx), width+min(0,dx))
            sy = slice(max(0,-dy), height-max(0,dy)); sx = slice(max(0,-dx), width-max(0,dx))
            fill = ~valid[ys,xs] & old[sy,sx]
            values[ys,xs][fill] = values[sy,sx][fill]
            valid[ys,xs][fill] = True
        if np.array_equal(old, valid): raise ValueError('Empty island padding seed')
    return values


def extract(objects, folder, asset, output, size, *, layer='UVMap'):
    """Replace copied meshes' atlas UVs/material images with their own map set.

    ``size`` is exactly 512 or 1024. Fail rather than reduce source texel
    density; callers should request the smallest fitting size. ``objects``
    must be disposable export copies, never the main assembly's source data.
    Returns measured density, layout, padding and map paths for auditing.
    """
    if type(size) is not int or size not in (512,1024):
        raise ValueError('texture_size must be 512 or 1024')
    arrays = {c: read_png(Path(folder)/f'T_{asset}_{c}.png')[::-1] for c in CHANNELS}
    source_size = arrays['BaseColor'].shape[0]
    if any(a.shape[:2] != (source_size,source_size) for a in arrays.values()):
        raise ValueError('Detachable extraction requires matching square maps')
    islands = []; densities = []; areas = []
    for ob in objects:
        mesh = ob.data; mesh.calc_loop_triangles(); data = mesh.uv_layers[layer]
        for group in uv.islands(ob, layer):
            loops = sorted(group)
            points = np.array([data.data[i].uv[:] for i in loops])*source_size
            if points.min() < -1e-3 or points.max() > source_size+1e-3:
                raise ValueError('Detachable UVs must be inside the canonical atlas')
            lo = np.floor(points.min(axis=0)-1).astype(int)
            hi = np.ceil(points.max(axis=0)+1).astype(int)
            islands.append(dict(ob=ob, loops=loops, lo=lo, shape=hi-lo))
        for tri in mesh.loop_triangles:
            p = [ob.matrix_world@mesh.vertices[i].co for i in tri.vertices]
            surface = (p[1]-p[0]).cross(p[2]-p[0]).length*.5
            texels = abs(uv.signed_area([tuple(data.data[i].uv) for i in tri.loops]))*source_size**2
            if surface > 1e-15 and texels > 1e-15:
                densities.append(math.sqrt(texels/surface)); areas.append(surface)
    if not islands: raise ValueError('Detachable contains no UV islands')
    rectangles = [tuple(map(int,i['shape']+2*PADDING)) for i in islands]
    target_size = size
    positions = _pack(rectangles, target_size)
    if positions is None:
        raise ValueError(f'Detachable cannot fit {size} at original density with {PADDING}px padding')
    result = {c:np.zeros((target_size,target_size,a.shape[2]),np.float32) for c,a in arrays.items()}
    records = []
    # Calculate footprints before changing any UVs.
    masks = [_mask(i['ob'].data, i['ob'].data.uv_layers[layer], i['loops'],
                   i['lo'], i['shape'], source_size) for i in islands]
    for island, (x,y), mask in zip(islands, positions, masks):
        width,height = map(int,island['shape']); ox,oy = map(int,island['lo'])
        for channel, source in arrays.items():
            # Match the canonical atlas's repeat sampling on its outer border.
            patch = source[np.arange(oy,oy+height)%source_size][:,np.arange(ox,ox+width)%source_size]
            valid = np.pad(mask, PADDING)
            patch = np.pad(patch, ((PADDING,PADDING),(PADDING,PADDING),(0,0)))
            result[channel][y:y+height+2*PADDING,x:x+width+2*PADDING] = _dilate(patch, valid)
        data = island['ob'].data.uv_layers[layer].data
        offset = np.array((x+PADDING,y+PADDING))-island['lo']
        for i in island['loops']:
            data[i].uv = (np.array(data[i].uv)*source_size+offset)/target_size
        records.append(dict(object=island['ob'].name,loops=island['loops'],
                            source_origin=island['lo'].tolist(),shape=island['shape'].tolist(),
                            destination_origin=[x+PADDING,y+PADDING],padding=PADDING))
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    paths = {}
    for channel,array in result.items():
        path = output/f'T_{asset}_{output.name}_{channel}.png'; write_png(path,array[::-1]);paths[channel]=str(path)
    # Copy materials as well as mesh data. Preserve factors, extensions, alpha
    # masks/data and all links; change only the three image datablocks.
    import bpy
    materials = {}; replacements = {}
    for ob in objects:
        for index, material in enumerate(ob.data.materials):
            if material not in materials:
                copy = material.copy(); materials[material] = copy
                for node in copy.node_tree.nodes:
                    if node.type != 'TEX_IMAGE' or node.image is None: continue
                    channel = next((c for c in CHANNELS if Path(node.image.filepath).stem == f'T_{asset}_{c}'),None)
                    if channel is None: raise ValueError('Detachable uses an image outside its canonical atlas')
                    if channel not in replacements:
                        image = bpy.data.images.load(paths[channel],check_existing=False)
                        image.colorspace_settings.name = 'sRGB' if channel == 'BaseColor' else 'Non-Color'
                        replacements[channel] = image
                    node.image = replacements[channel]
            ob.data.materials[index] = materials[material]
    order = np.argsort(densities); cum = np.cumsum(np.array(areas)[order]); total = cum[-1]
    percentiles = {str(p):float(np.array(densities)[order][np.searchsorted(cum,total*p/100)]) for p in (5,50,95)}
    new_densities = []
    for ob in objects:
        mesh = ob.data; data = mesh.uv_layers[layer]
        for tri in mesh.loop_triangles:
            points = [ob.matrix_world@mesh.vertices[i].co for i in tri.vertices]
            surface = (points[1]-points[0]).cross(points[2]-points[0]).length*.5
            texels = abs(uv.signed_area([tuple(data.data[i].uv) for i in tri.loops]))*target_size**2
            if surface > 1e-15 and texels > 1e-15:
                new_densities.append(math.sqrt(texels/surface))
    ratios = np.array(new_densities)/densities
    if np.min(ratios) < .999: raise ValueError('Texture extraction reduced density')
    new_order = np.argsort(new_densities); new_cum = np.cumsum(np.array(areas)[new_order])
    new_percentiles = {str(p):float(np.array(new_densities)[new_order][np.searchsorted(new_cum,total*p/100)]) for p in (5,50,95)}
    report = dict(source_size=source_size,size=target_size,requested_size=size,
                  source_density_px_m=percentiles,density_px_m=new_percentiles,
                  density_ratio_min=float(ratios.min()),density_ratio_max=float(ratios.max()),
                  padding_px=PADDING,islands=records,maps=paths,
                  sampling='LINEAR, no mipmaps; 2px guards; do not override sampler')
    (output/'layout.json').write_text(json.dumps(report,indent=2))
    return report


def set_sampler(path):
    """Declare base-level bilinear filtering; glTF has no max-LOD sampler field.

    No finite gutter can isolate multiple islands at the 1x1 mip tail. Engines
    must honor this sampler (or explicitly clamp LOD when generating mipmaps).
    Mesh/accessor/image/BIN bytes are untouched.
    """
    path = Path(path); raw = path.read_bytes(); chunks = []; offset = 12
    while offset < len(raw):
        length,kind = struct.unpack_from('<II',raw,offset)
        payload = raw[offset+8:offset+8+length]; offset += 8+length
        if kind == 0x4e4f534a:
            document = json.loads(payload)
            for sampler in document.get('samplers',[]):
                sampler.update(minFilter=9729,magFilter=9729,wrapS=33071,wrapT=33071)
            payload = json.dumps(document,separators=(',',':')).encode()
            payload += b' '*(-len(payload)%4)
        chunks.append(struct.pack('<II',len(payload),kind)+payload)
    payload = b''.join(chunks)
    path.write_bytes(struct.pack('<III',0x46546c67,2,12+len(payload))+payload)
