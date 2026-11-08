"""Compare two independent source builds, excluding Blender file timestamps."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,numpy as np

def state(path):
    bpy.ops.wm.open_mainfile(filepath=str(path.resolve()))
    rows={}
    for ob in sorted(bpy.context.scene.objects,key=lambda o:o.name):
        if not (ob.get('asset_set')=='SchoolBus' or ob.get('bake_only')):continue
        h=hashlib.sha256();normal_values=np.empty((0,3),dtype=np.float32)
        h.update(np.asarray(ob.matrix_world,dtype='<f4').tobytes())
        properties={k:ob[k] for k in ['asset_set','part_category','variant_id','pivot_axis','range_degrees','socket_kind'] if k in ob}
        h.update(json.dumps(properties,sort_keys=True,default=list).encode())
        if ob.type=='MESH':
            h.update(np.asarray([v.co for v in ob.data.vertices],dtype='<f4').tobytes())
            # BMesh may rotate a face's first loop or reorder faces. Compare
            # the same oriented corners and their corresponding normals,
            # rather than mistaking storage permutations for new form.
            normals=ob.data.corner_normals;faces=[]
            for p in ob.data.polygons:
                corners=[(ob.data.loops[i].vertex_index,*normals[i].vector) for i in p.loop_indices]
                start=min(range(len(corners)),key=lambda i:corners[i][0])
                faces.append((p.material_index,tuple(corners[start:]+corners[:start])))
            faces.sort(key=lambda row:(row[0],tuple(c[0] for c in row[1])))
            h.update(repr([(mat,tuple(c[0] for c in corners)) for mat,corners in faces]).encode())
            normal_values=np.asarray([c[1:] for _,corners in faces for c in corners],dtype=np.float32)
            h.update(json.dumps([m.name if m else None for m in ob.data.materials]).encode())
        rows[ob.name]=dict(geometry=h.hexdigest(),normals=normal_values)
    return rows

def main():
    p=argparse.ArgumentParser();p.add_argument('--first',required=True)
    p.add_argument('--second',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    first=state(Path(a.first));second=state(Path(a.second))
    changed=[k for k in sorted(first.keys()|second.keys()) if k not in first or k not in second or first[k]['geometry']!=second[k]['geometry']]
    deltas={}
    for k in first.keys()&second.keys():
        x,y=first[k]['normals'],second[k]['normals']
        deltas[k]=float(np.max(np.abs(x-y))) if x.shape==y.shape and x.size else 0 if x.shape==y.shape else float('inf')
        if deltas[k]>1e-6:changed.append(k)
    changed=sorted(set(changed))
    result=dict(passed=not changed,objects=len(first),changed=changed,
        measured_maximum_normal_component_difference=max(deltas.values()),normal_component_tolerance=1e-6,
        scope='Independent seed-101 builds: exact vertices, canonical oriented topology/material bindings, transforms and metadata; measured smooth-normal float rounding within 1e-6, not file timestamp equality')
    Path(a.out).write_text(json.dumps(result,indent=2));print('BUS_DETERMINISM',result,flush=True)
    if changed:raise SystemExit(1)

if __name__=='__main__':main()
