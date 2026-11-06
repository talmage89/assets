"""LOD atlas charts weighted by delivered texel density, with mip gutters.

The source BVH exists only during layout. It stores original UV density, not
source colors. Every appearance texel still comes from the immutable shader.
"""
import math
import struct

import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def reference(sources, original):
    specs = {}
    sizes = {}
    for material in original.data.get('materials', []):
        pbr = material.get('pbrMetallicRoughness', {})
        info = pbr.get('baseColorTexture') or material.get('normalTexture') or pbr.get('metallicRoughnessTexture')
        if info:
            index = original.data['textures'][info['index']]['source']
            if index not in sizes:
                sizes[index] = struct.unpack_from('>II', original.image(index), 16)
            width, height = sizes[index]
            specs[material.get('name')] = ('LOD_SourceUV' + str(info.get('texCoord', 0)), width * height)
    points = []; faces = []; densities = []; offset = 0
    for ob in sources:
        mesh = ob.data; mesh.calc_loop_triangles()
        matrix = np.array(ob.matrix_world)
        pp = np.array([v.co[:] for v in mesh.vertices]) @ matrix[:3, :3].T + matrix[:3, 3]
        triangles = list(mesh.loop_triangles)
        ff = np.array([t.vertices[:] for t in triangles], np.uint32)
        loops = np.array([t.loops[:] for t in triangles], np.uint32)
        area = np.linalg.norm(np.cross(pp[ff[:, 1]]-pp[ff[:, 0]], pp[ff[:, 2]]-pp[ff[:, 0]]), axis=1)
        density = np.zeros(len(ff))
        for slot, material in enumerate(mesh.materials):
            if not material or material.name not in specs:continue
            uvname, pixels = specs[material.name]
            if uvname not in mesh.uv_layers:continue
            uv = np.array([v.uv[:] for v in mesh.uv_layers[uvname].data])[loops]
            edge = uv[:, 1:] - uv[:, :1]
            uvarea = np.abs(edge[:, 0, 0]*edge[:, 1, 1]-edge[:, 0, 1]*edge[:, 1, 0])
            take = np.array([t.material_index == slot for t in triangles])
            density[take] = pixels*uvarea[take]/np.maximum(area[take], 1e-20)
        points.extend(pp); faces.extend(ff + offset); densities.extend(density); offset += len(pp)
    return BVHTree.FromPolygons([Vector(p) for p in points], faces, all_triangles=True), np.array(densities)


def charts(mesh):
    """UV charts separated at meaningful discontinuities of the cage frame."""
    uv=mesh.uv_layers.active.data;normals=np.array([n.vector[:] for n in mesh.corner_normals]);parent=list(range(len(mesh.polygons)));edges={}
    def root(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    cosine=math.cos(math.radians(1))
    for face in mesh.polygons:
        loops=list(face.loop_indices)
        for j,a in enumerate(loops):
            b=loops[(j+1)%len(loops)]
            ends=sorted([(mesh.loops[k].vertex_index,tuple(np.round(uv[k].uv[:],7)),k) for k in (a,b)])
            key=tuple((v,u) for v,u,li in ends);nn=normals[[v[2] for v in ends]]
            for other,normal in edges.get(key,[]):
                if np.all(np.sum(nn*normal,axis=1)>cosine):parent[root(face.index)]=root(other)
            edges.setdefault(key,[]).append((face.index,nn))
    groups={}
    for face in mesh.polygons:groups.setdefault(root(face.index),[]).append(face.index)
    return list(groups.values())


def measures(ob, ids):
    mesh = ob.data; uv = mesh.uv_layers.active.data; matrix = np.array(ob.matrix_world)
    pp = np.array([v.co[:] for v in mesh.vertices]) @ matrix[:3, :3].T + matrix[:3, 3]
    world_area = uv_area = 0.
    for fi in ids:
        face = mesh.polygons[fi]; p = pp[list(face.vertices)]; u = np.array([uv[i].uv[:] for i in face.loop_indices])
        for j in range(1, len(p)-1):
            world_area += np.linalg.norm(np.cross(p[j]-p[0], p[j+1]-p[0]))*.5
            a, b = u[j]-u[0], u[j+1]-u[0]; uv_area += abs(a[0]*b[1]-a[1]*b[0])*.5
    return float(world_area), float(uv_area)


def unwrap(targets, sources, original, size, meters_per_pixel):
    """Preserve relative source sampling importance, then pack all parts once.

    Uniform world-area allocation loses the deliberately denser headlamps,
    labels and paint charts. These weights come from original source UVs and
    image dimensions. A chart's area-weighted source density drives its scale.
    """
    print('LOD LAYOUT START',len(targets),'targets',size,'px',flush=True)
    bpy.context.view_layer.update()
    tree, density = reference(sources, original)
    from kit.lod_transfer import source_hit
    bpy.ops.object.select_all(action='DESELECT')
    for ob in targets:ob.select_set(True)
    bpy.context.view_layer.objects.active = targets[0]
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0, correct_aspect=False, scale_to_bounds=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    groups = []; source_weights = []
    for ob in targets:
        mesh = ob.data; uv = mesh.uv_layers.active.data; matrix = np.array(ob.matrix_world)
        pp = np.array([v.co[:] for v in mesh.vertices]) @ matrix[:3, :3].T + matrix[:3, 3]
        for ids in charts(mesh):
            weight = area_sum = 0.
            for fi in ids:
                p = pp[list(mesh.polygons[fi].vertices)]; area = np.linalg.norm(np.cross(p[1]-p[0], p[2]-p[0]))*.5
                direction=np.cross(p[1]-p[0],p[2]-p[0]);direction/=max(np.linalg.norm(direction),1e-20)
                hit=source_hit(tree,p.mean(axis=0),direction,2*meters_per_pixel)
                value = density[hit[2]] if hit is not None else 0
                # Constant/unmapped surfaces still need a finite chart for
                # their normal/material response, without inventing detail.
                if value <= 0:value = 1/maximum_pixel(meters_per_pixel)**2
                weight += area*value
                area_sum += area
            world_area, old_area = measures(ob, ids)
            if old_area < 1e-20 or world_area < 1e-20:continue
            scale = math.sqrt(weight/old_area)
            loops = [li for fi in ids for li in mesh.polygons[fi].loop_indices]
            center = np.array([uv[li].uv[:] for li in loops]).mean(axis=0)
            for li in loops:uv[li].uv = center + (np.array(uv[li].uv[:])-center)*scale + len(groups)*np.array([1e-4,3e-4])
            groups.append((ob, ids)); source_weights.append(math.sqrt(weight/max(area_sum, 1e-20)))
    print('LOD LAYOUT CHARTS',len(groups),flush=True)
    guard = 4; budget_cap=size/max(16,4*math.sqrt(max(1,len(groups))))
    cap=max(4,min(64,2**int(math.floor(math.log2(max(4,budget_cap)))))); footprint = 1.
    for attempt in range(3):
        print('LOD LAYOUT PACK',attempt,'gutter',guard,flush=True)
        bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.pack_islands(udim_source='ACTIVE_UDIM', rotate=True, scale=True,
                                shape_method='CONCAVE', margin_method='FRACTION', margin=guard/size)
        bpy.ops.object.mode_set(mode='OBJECT')
        footprints = []
        for ob, ids in groups:
            world_area, uv_area = measures(ob, ids)
            footprints.append(size*math.sqrt(uv_area/max(world_area, 1e-20))*meters_per_pixel)
        footprint = max(1., float(np.quantile(footprints, .95))) if footprints else 1.
        needed = max(4, 2**(math.ceil(math.log2(footprint))+1))
        next_guard = min(cap, needed)
        if next_guard <= guard:break
        guard = next_guard
    print('LOD LAYOUT PACKED','gutter',guard,'mip95',round(math.log2(footprint),3),flush=True)
    areas = [measures(ob, ids)[1] for ob, ids in groups]
    return dict(method='source-density-weighted charts', charts=len(groups), uv_area=float(sum(areas)),
                gutter_pixels=guard, estimated_mip_p95=float(math.log2(footprint)),
                gutter_cap_pixels=cap, gutter_capped=needed>cap,
                source_density_min=float(min(source_weights)), source_density_max=float(max(source_weights)))


def maximum_pixel(meters_per_pixel):
    # One texel per switch pixel is sufficient for a constant source field.
    return max(meters_per_pixel, 1e-8)
