"""Full-face export audit for optical cassettes and both fascia moldings.

The source supplies part names only. Positions, oriented triangles and exact
corner normals come from a fresh GLB import, including hidden laminate faces.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from sedan_surface_proof import delivery_parts
from sedan_surface_check import intersects
MIN_AREA=1e-10
MIN_ALTITUDE=1e-6


def measure(ob):
    me=ob.data;me.calc_loop_triangles();exact=me.attributes.get('DeliveryNormal')
    seen=set();edges={};areas=[];altitudes=[];dots=[];corner_dots=[];duplicates=[];flipped=[];optical=[]
    roles=me.attributes.get('sheet_role')
    for tri in me.loop_triangles:
        ps=[ob.matrix_world@me.vertices[i].co for i in tri.vertices]
        cross=(ps[1]-ps[0]).cross(ps[2]-ps[0]);area=cross.length/2
        longest=max((ps[(i+1)%3]-ps[i]).length for i in range(3))
        ns=[exact.data[i].vector if exact else me.corner_normals[i].vector for i in tri.loops]
        dot=cross.normalized().dot(sum(ns,Vector()).normalized())
        if ob.name.startswith('Headlamp opening') and (roles.data[tri.polygon_index].value==0 if roles else tri.polygon_index<ob['lens_outer_faces']):optical.append(dot)
        corner_dots.extend(cross.normalized().dot(n) for n in ns)
        areas.append(area);altitudes.append(2*area/max(longest,1e-15));dots.append(dot)
        keys=[tuple(round(c,7) for c in p) for p in ps];key=tuple(sorted(keys))
        if key in seen:duplicates.append(tri.index)
        seen.add(key)
        if dot<=0:flipped.append(tri.index)
        for a,c in zip(keys,keys[1:]+keys[:1]):edges.setdefault(tuple(sorted((a,c))),[]).append(1 if a<c else -1)
    inconsistent=[edge for edge,uses in edges.items() if len(uses)==2 and sum(uses)!=0]
    row=dict(triangles=len(areas),duplicate_faces=len(duplicates),flipped_normal_faces=len(flipped),
        inconsistent_shared_edge_winding=len(inconsistent),flipped_corner_normals=sum(d<=0 for d in corner_dots),near_zero_area_faces=sum(a<MIN_AREA or h<MIN_ALTITUDE for a,h in zip(areas,altitudes)),
        minimum_face_area_m2=min(areas),minimum_face_altitude_m=min(altitudes),minimum_winding_to_corner_normal_dot=min(dots),minimum_individual_corner_dot=min(corner_dots),
        duplicate_examples=duplicates[:8],flipped_examples=flipped[:8])
    row['passed']=not any(row[k] for k in ['duplicate_faces','flipped_normal_faces','flipped_corner_normals','inconsistent_shared_edge_winding','near_zero_area_faces'])
    if optical:
        row['maximum_outer_optical_chord_normal_error_degrees']=math.degrees(math.acos(max(-1,min(1,min(optical)))))
        row['passed'] &= row['maximum_outer_optical_chord_normal_error_degrees']<=3.1
    return row


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--glb',required=True);p.add_argument('--out',required=True);p.add_argument('--diagnose',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);obs,correspondence=delivery_parts(Path(a.source).resolve(),Path(a.glb).resolve())
    selected=[o for o in obs if o.get('part_category') in ['lamps','fascia'] or any(t in o.name for t in ['Headlamp','Taillamp','DRL pocket','grille','Lower intake','slot intake'])]
    rows={o.name:measure(o) for o in selected};failed=[n for n,r in rows.items() if not r['passed']]
    seen={};global_duplicates=[]
    for ob in selected:
        ob.data.calc_loop_triangles()
        for tri in ob.data.loop_triangles:
            key=tuple(sorted(tuple(round(v,7) for v in ob.matrix_world@ob.data.vertices[i].co) for i in tri.vertices))
            if key in seen and seen[key]!=ob.name:global_duplicates.append([seen[key],ob.name,tri.index])
            seen[key]=ob.name
    if global_duplicates:failed.append('Coincident duplicate faces across parts')
    from mathutils.bvhtree import BVHTree
    crossings={}
    for cover in [o for o in obs if o.name.startswith('Headlamp opening')]:
        roles=cover.data.attributes['sheet_role'];cover.data.calc_loop_triangles()
        ps=[v.co.copy() for v in cover.data.vertices]
        fs=[tuple(t.vertices) for t in cover.data.loop_triangles if roles.data[t.polygon_index].value==0]
        tree=BVHTree.FromPolygons(ps,fs,all_triangles=True);parts={}
        for ob in obs:
            if ob==cover or not (('Headlamp' in ob.name and not ob.name.startswith('Headlamp')) or ob.name in ['Front molded fascia','Hood outer','Front fender_L','Front fender_R'] or ob.name.startswith(('S240 inner aperture liner Hood outer','S240 inner aperture liner moving hem Hood outer','S240 inner aperture liner Front molded fascia'))):continue
            ob.data.calc_loop_triangles();qs=[v.co.copy() for v in ob.data.vertices];ts=[tuple(t.vertices) for t in ob.data.loop_triangles]
            other=BVHTree.FromPolygons(qs,ts,all_triangles=True)
            count=sum(intersects([ps[i] for i in fs[a]],[qs[i] for i in ts[b]]) for a,b in tree.overlap(other))
            parts[ob.name]=count
        crossings[cover.name]=dict(triangle_crossings=sum(parts.values()),parts=parts)
        if sum(parts.values()):failed.append(cover.name+' cassette/backing intersections')
    report=dict(passed=not failed,failed_parts=failed,parts=rows,delivery_correspondence=correspondence,
        glb_sha256=hashlib.sha256(Path(a.glb).read_bytes()).hexdigest(),
        lens_intersections=crossings,global_duplicate_faces=len(global_duplicates),global_duplicate_examples=global_duplicates[:8],
        scope=__doc__.strip(),thresholds=dict(face_area_m2=MIN_AREA,shortest_altitude_m=MIN_ALTITUDE,duplicate_position_rounding_m=1e-7))
    Path(a.out).write_text(json.dumps(report,indent=2));print('S240_FRONT_MESH',len(rows),'parts; failures:',failed)
    if failed and not a.diagnose:raise SystemExit(1)
if __name__=='__main__':main()
