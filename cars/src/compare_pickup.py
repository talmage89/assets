"""Exact pickup source arrays and re-exported GLB accessors, independently.

The source comparison requires a fresh invocation of the default build path.
GLB comparison re-exports the accepted finalized source/maps, isolating export
compatibility from nondeterministic GPU bake bytes. No previous binary is an
input to the car generator or exporter.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.gltf import GLB

def capture(path):
    bpy.ops.wm.open_mainfile(filepath=str(path.resolve()));bpy.context.view_layer.update();result={}
    for ob in bpy.context.scene.objects:
        row=dict(matrix=np.array(ob.matrix_world),type=ob.type,parent=ob.parent.name if ob.parent else None)
        if ob.type=='MESH':
            row.update(vertices=np.array([tuple(v.co) for v in ob.data.vertices]),polygons=[tuple(f.vertices) for f in ob.data.polygons],
              normals=np.array([tuple(n.vector) for n in ob.data.corner_normals]),materials=[m.name for m in ob.data.materials])
        result[ob.name]=row
    return result
def main():
    p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',required=True);p.add_argument('--old-glb',required=True);p.add_argument('--new-glb',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);before=capture(Path(a.before));after=capture(Path(a.after));changes=[]
    if before.keys()!=after.keys():changes.append('Source object set')
    for name,row in before.items():
        if name not in after:continue
        for key,value in row.items():
            other=after[name][key];same=np.array_equal(value,other) if isinstance(value,np.ndarray) else value==other
            if not same:changes.append(name+' / '+key)
    old,new=GLB(Path(a.old_glb)),GLB(Path(a.new_glb));array_changes=[];accessors=0
    if len(old.json['meshes'])!=len(new.json['meshes']):array_changes.append('Mesh count')
    for mi,(left,right) in enumerate(zip(old.json['meshes'],new.json['meshes'])):
        for pi,(lp,rp) in enumerate(zip(left['primitives'],right['primitives'])):
            la={'indices':lp['indices'],**lp['attributes']};ra={'indices':rp['indices'],**rp['attributes']}
            if la.keys()!=ra.keys():array_changes.append(f'{mi}/{pi} attributes')
            for key,index in la.items():
                accessors+=1
                if not np.array_equal(old.accessor(index),new.accessor(ra[key])):array_changes.append(f'{mi}/{pi}/{key}')
    images_equal=len(old.json['images'])==len(new.json['images']) and all(old.image(i)==new.image(i) for i in range(len(old.json['images'])))
    graph_equal=all(old.json.get(k)==new.json.get(k) for k in ['nodes','scenes','materials','textures','samplers'])
    json_changes=[k for k in sorted(set(old.json)|set(new.json)) if old.json.get(k)!=new.json.get(k)]
    def without_generator(document):
        result=dict(document);result['asset']={k:v for k,v in document['asset'].items() if k!='generator'};return result
    metadata_only=without_generator(old.json)==without_generator(new.json)
    payload_equal=old.binary==new.binary
    report=dict(passed=not changes and not array_changes and images_equal and graph_equal and payload_equal and metadata_only,source_objects=len(before),
       source_meshes=sum(r['type']=='MESH' for r in before.values()),source_changes=changes,
       glb_accessors_compared=accessors,glb_array_changes=array_changes,embedded_maps_identical=images_equal,delivery_graph_identical=graph_equal,
       old_bytes=Path(a.old_glb).stat().st_size,new_bytes=Path(a.new_glb).stat().st_size,
       old_sha256=hashlib.sha256(Path(a.old_glb).read_bytes()).hexdigest(),new_sha256=hashlib.sha256(Path(a.new_glb).read_bytes()).hexdigest(),
       complete_glb_identical=Path(a.old_glb).read_bytes()==Path(a.new_glb).read_bytes(),
       binary_payload_identical=payload_equal,json_fields_changed=json_changes,
       json_identical_except_exporter_version=metadata_only,
       exporter_versions=[old.json['asset'].get('generator'),new.json['asset'].get('generator')],
       scope='Fresh default pickup source generation; re-export of unchanged accepted finalized source/maps. No GPU rebake.')
    Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
    if not report['passed']:raise AssertionError('Pickup preservation failed')
if __name__=='__main__':main()
