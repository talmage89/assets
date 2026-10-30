"""Adjacent geometric face-normal angles on the dense source, in degrees.

Uses actual triangulated source faces, never transferred shading normals or
generator derivatives. Records each maximum's endpoints and both face centers
so a bad edge cannot disappear inside a percentile. Deliberate manufactured
edges are reported separately. This does not replace reflection inspection.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy, bmesh
import numpy as np
from mathutils.bvhtree import BVHTree
from mathutils import Vector

def measure(source):
    bpy.ops.wm.open_mainfile(filepath=str(source))
    ob = bpy.data.objects['HIGH_Action_Body']
    bm = bmesh.new(); bm.from_mesh(ob.data)
    topology=dict(nonmanifold_edges=sum(not e.is_manifold for e in bm.edges),
        zero_area_faces=sum(f.calc_area()<1e-17 for f in bm.faces),volume_m3=bm.calc_volume(signed=True))
    bmesh.ops.triangulate(bm, faces=list(bm.faces)); bm.normal_update()
    groups = {name: [] for name in ('right fence/head', 'left fence/head', 'center fill',
        'right rear return', 'left rear return', 'recess lip', 'breech arris', 'rear wood seam', 'recess floor edge', 'bushing counterbore', 'spindle seat')}
    def angle(a,b): return math.degrees(math.acos(max(-1,min(1,a.dot(b)))))
    for e in bm.edges:
        if len(e.link_faces) != 2: continue
        a,b = e.link_faces
        if min(a.calc_area(),b.calc_area()) < 1e-17: continue
        p = (e.verts[0].co+e.verts[1].co)*500
        centers = [f.calc_center_median()*1000 for f in (a,b)]
        x,y,z = p; name = None
        if 69 < y < 115.05 and z > 40:
            if y > 114.65: name = 'breech arris'
            elif y>113.8 and z<48 and abs(abs(x)-12.6)<3.8: name='bushing counterbore'
            elif any(any(v.co.z<.030 and v.co.y<.081 for v in f.verts) for f in (a,b)): name='rear wood seam'
            elif abs(x)<4.6 and 89.4<y<98.6 and z<48.05: name='spindle seat'
            elif abs(x)<10.5 and 86<y<100.5 and abs(z-(48+.4*min(0,y-94)))<.035: name='recess floor edge'
            elif abs(x)<10 and 86<y<101 and z>48+.4*min(0,y-94)+.035: name='recess lip'
            elif abs(x)<7.5 and 100.5<y<114.65: name='center fill'
            elif 101<y<114.65: name=('right' if x>0 else 'left')+' fence/head'
            elif 85<y<=101: name=('right' if x>0 else 'left')+' rear return'
        if name:
            groups[name].append(dict(angle_degrees=angle(a.normal,b.normal), edge_length_mm=e.calc_length()*1000,
                edge_mm=[[float(v*1000) for v in q.co] for q in e.verts],face_centers_mm=[list(c) for c in centers]))
    # Read the actual upper source triangles along both bore axes. The
    # front edge break is deliberately outside this Y95.5–114.8 interval.
    tree=BVHTree.FromBMesh(bm);crown_profiles=[]
    for side in (-1,1):
        ys=np.arange(95.5,114.801,.1)
        zs=np.array([tree.ray_cast(Vector((side*(12.6+1.7*(115-y)/660.4)*.001,y*.001,.08)),Vector((0,0,-1)),.08)[0].z*1000 for y in ys])
        slopes=np.diff(zs)/np.diff(ys)
        crown_profiles.append(dict(side=side,stations_y_mm=ys.tolist(),height_mm=zs.tolist(),minimum_forward_slope=float(slopes.min()),maximum_height_y_mm=float(ys[zs.argmax()]),rear_to_front_monotone=bool(slopes.min()>0)))
    bm.free(); report = {}
    for name, rows in groups.items():
        rows.sort(key=lambda r:r['angle_degrees'],reverse=True)
        report[name] = dict(edges=len(rows), maximum=rows[0] if rows else None,
            largest=rows[:10])
    smooth=('right fence/head','left fence/head','center fill','right rear return','left rear return','recess lip')
    passed=all(report[name]['maximum'] and report[name]['maximum']['angle_degrees']<12 for name in smooth)
    passed=passed and all(r['rear_to_front_monotone'] for r in crown_profiles) and not topology['nonmanifold_edges'] and not topology['zero_area_faces'] and topology['volume_m3']>0
    return dict(passed=passed,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),dense_topology=topology,
        crown_profiles=crown_profiles,smooth_region_limit_degrees=12,limit_scope='source tessellation audit, not a photographic fairness certificate',
        method='geometric normals of adjacent triangulated dense-source faces; sharp edges separately classified by measured location',
        intended_edges=['standing-breech front arris, 0.18 mm edge break', 'external rear wood joint',
            'recess floor/wall below the radiused upper lip', 'firing-pin bushing counterbore steps', 'lower spindle seat'], regions=report)

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve()
    result=measure(source);Path(a.out).write_text(json.dumps(result,indent=2))
    for name,row in result['regions'].items():
        print(name,row['edges'],row['maximum']['angle_degrees'] if row['maximum'] else None)
    assert result['passed'],result

if __name__=='__main__':main()
