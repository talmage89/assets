"""UV measurements with actual triangle intersection tests, not bounding-box guesses."""
import math
from collections import defaultdict
import numpy as np


def signed_area(poly):
    return sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1]))*.5


def intersection_area(a,b):
    """Sutherland-Hodgman clipping of two counterclockwise UV triangles."""
    output=[tuple(p) for p in a]
    if signed_area(list(b))<0:b=list(reversed(b))
    for p,q in zip(b,list(b[1:])+[b[0]]):
        if not output:return 0.0
        source=output;output=[]
        def side(v):return (q[0]-p[0])*(v[1]-p[1])-(q[1]-p[1])*(v[0]-p[0])
        previous=source[-1];sp=side(previous)
        for current in source:
            sc=side(current)
            if (sc>=-1e-13)!=(sp>=-1e-13):
                t=sp/(sp-sc)
                output.append((previous[0]+t*(current[0]-previous[0]),previous[1]+t*(current[1]-previous[1])))
            if sc>=-1e-13:output.append(current)
            previous=current;sp=sc
    return abs(signed_area(output)) if len(output)>2 else 0.0


def report(objects,size=2048,layer='BakeUV'):
    triangles=[];areas=[];densities=[];island_rows=[];degenerate=0;outside=0
    for ob in objects:
        me=ob.data;me.calc_loop_triangles()
        uv=me.uv_layers.get(layer) or me.uv_layers.active
        if uv is None:raise ValueError(f'{ob.name}: no UV layer')
        # Island connectivity requires equal UVs at shared geometric edges.
        adjacency=defaultdict(list);parent=list(range(len(me.polygons)))
        def find(i):
            while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
            return i
        def union(a,b):parent[find(a)]=find(b)
        for face in me.polygons:
            loops=list(face.loop_indices)
            for x,y in zip(loops,loops[1:]+loops[:1]):
                a=(me.loops[x].vertex_index,*[round(v,7) for v in uv.data[x].uv])
                b=(me.loops[y].vertex_index,*[round(v,7) for v in uv.data[y].uv])
                adjacency[tuple(sorted((a,b)))].append(face.index)
        for faces in adjacency.values():
            for face in faces[1:]:union(faces[0],face)
        islands=defaultdict(lambda:[0.0,0.0])
        for tri in me.loop_triangles:
            coords=[tuple(uv.data[i].uv) for i in tri.loops]
            ua=abs(signed_area(coords));points=[ob.matrix_world@me.vertices[i].co for i in tri.vertices]
            wa=(points[1]-points[0]).cross(points[2]-points[0]).length*.5
            if ua<1e-14 or wa<1e-12:degenerate+=1;continue
            outside+=any(v<0 or v>1 for p in coords for v in p)
            triangles.append(coords);areas.append(ua)
            densities.append(math.sqrt(ua/wa)*size)
            key=find(tri.polygon_index);islands[key][0]+=ua;islands[key][1]+=wa
        for key,(ua,wa) in islands.items():
            island_rows.append(dict(object=ob.name,island=key,uv_area=ua,surface_m2=wa,density_px_m=math.sqrt(ua/wa)*size))
    # Spatial buckets only select candidates. Every positive overlap is polygon-clipped.
    grid=defaultdict(list);pairs=set();overlaps=[];overlap_area=0
    cells=96
    for index,tri in enumerate(triangles):
        lo=np.floor(np.min(tri,axis=0)*cells).astype(int);hi=np.floor(np.max(tri,axis=0)*cells).astype(int)
        for x in range(max(0,lo[0]),min(cells-1,hi[0])+1):
            for y in range(max(0,lo[1]),min(cells-1,hi[1])+1):
                for other in grid[x,y]:pairs.add((other,index))
                grid[x,y].append(index)
    for a,b in sorted(pairs):
        ta,tb=triangles[a],triangles[b]
        if max(p[0] for p in ta)<=min(p[0] for p in tb)+1e-12 or max(p[0] for p in tb)<=min(p[0] for p in ta)+1e-12:continue
        if max(p[1] for p in ta)<=min(p[1] for p in tb)+1e-12 or max(p[1] for p in tb)<=min(p[1] for p in ta)+1e-12:continue
        area=intersection_area(ta,tb)
        if area>1e-10:
            overlaps.append([a,b,area]);overlap_area+=area
    coverage=sum(areas)
    # Area-weighted density percentiles avoid tiny screw caps dominating the summary.
    ordered=sorted(zip(densities,areas));total=sum(areas);accum=0;percentiles={}
    for density,area in ordered:
        accum+=area
        for percentile in (5,50,95):
            if percentile not in percentiles and accum>=total*percentile/100:percentiles[percentile]=density
    return dict(texture_size=size,triangles=len(triangles),islands=len(island_rows),coverage=coverage,
                outside_triangles=outside,degenerate_uv_triangles=degenerate,
                overlap_pairs=len(overlaps),overlap_area=overlap_area,overlap_fraction=overlap_area/max(coverage,1e-12),
                density_px_m={str(k):v for k,v in percentiles.items()},island_measurements=island_rows,
                overlap_examples=overlaps[:20])


def islands(ob,layer='BakeUV'):
    """Return face-loop groups joined across equal geometric and UV edges."""
    me=ob.data;uv=me.uv_layers[layer];parent=list(range(len(me.polygons)));edges={}
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for face in me.polygons:
        loops=list(face.loop_indices)
        for x,y in zip(loops,loops[1:]+loops[:1]):
            a=(me.loops[x].vertex_index,*[round(v,7) for v in uv.data[x].uv])
            b=(me.loops[y].vertex_index,*[round(v,7) for v in uv.data[y].uv])
            key=tuple(sorted((a,b)))
            if key in edges:parent[find(face.index)]=find(edges[key])
            else:edges[key]=face.index
    result=defaultdict(set)
    for face in me.polygons:result[find(face.index)].update(face.loop_indices)
    return result.values()
