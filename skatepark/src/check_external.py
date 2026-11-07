"""External geometry and canonical image equality; real same-scene image reuse."""
import sys,json,hashlib
from pathlib import Path
import bpy,numpy as np
from PIL import Image
sys.path[:0]=[str(Path(__file__).resolve().parents[2]),str(Path(__file__).resolve().parent)]
from kit.gltf import GLB

def check(folder):
    records=[];all_images={};bpy.ops.wm.read_factory_settings(use_empty=True)
    for name in ['SkateparkPieces','Park_101','Park_202','Park_303']:
        path=folder/(name+'.gltf');doc=json.loads(path.read_text());embedded=Path('build/embedded')/(name+'.glb');g=GLB(embedded)
        ext=object.__new__(GLB);ext.json=doc;ext.binary=(path.parent/doc['buffers'][0]['uri']).read_bytes();ext.parents={c:i for i,n in enumerate(doc['nodes']) for c in n.get('children',[])}
        # Separate export shares accessors; embedded export can split them by
        # material. Compare the actual indexed corners, independently of packing.
        old_indices={n['name']:i for i,n in enumerate(g.json['nodes'])}
        assert set(old_indices)=={n['name'] for n in doc['nodes']}
        for i,node in enumerate(doc['nodes']):assert np.max(np.abs(ext.world(i)-g.world(old_indices[node['name']])))<2e-6,(name,node['name'],'world frame')
        old_nodes={n['name']:n for n in g.json['nodes'] if 'mesh' in n};visited=set();corners=0;unused_tangent_differences=0
        for node in doc['nodes']:
            if 'mesh' not in node:continue
            old=old_nodes[node['name']];pair=(node['mesh'],old['mesh'])
            if pair in visited:continue
            visited.add(pair)
            left=doc['meshes'][node['mesh']]['primitives'];right=g.json['meshes'][old['mesh']]['primitives']
            assert len(left)==len(right),(name,node['name'],'primitive count')
            for a,b in zip(left,right):
                assert doc['materials'][a['material']]['name']==g.json['materials'][b['material']]['name']
                ia=ext.accessor(a['indices']).ravel();ib=g.accessor(b['indices']).ravel();assert len(ia)==len(ib)
                assert set(a['attributes'])==set(b['attributes']),(name,node['name'],'attributes')
                for semantic,accessor in a['attributes'].items():
                    av=ext.accessor(accessor)[ia];bv=g.accessor(b['attributes'][semantic])[ib]
                    if semantic=='TANGENT' and 'normalTexture' not in doc['materials'][a['material']]:
                        unused_tangent_differences+=int(np.any(av!=bv,axis=1).sum());continue
                    assert np.array_equal(av,bv),(name,node['name'],semantic,float(np.max(np.abs(av-bv))))
                corners+=len(ia)
        embedded_images={hashlib.sha256(g.image(i)).hexdigest() for i in range(len(g.json.get('images',[])))}

        images=[];seen=set();memory=0
        for i,im in enumerate(doc.get('images',[])):
            target=(path.parent/im['uri']).resolve();assert target.is_file() and 'shared/' not in im['uri']
            payload=target.read_bytes();assert hashlib.sha256(payload).hexdigest() in embedded_images,(name,i,'image bytes')
            digest=hashlib.sha256(payload).hexdigest();size=Image.open(target).size
            if digest not in seen:memory+=size[0]*size[1]*4/3/1048576;seen.add(digest)
            images.append(dict(uri=im['uri'],sha256=digest,bytes=len(payload),size=size));all_images[str(target)]=digest
        albedos=[];weights=[]
        for mesh in doc['meshes']:
            for prim in mesh['primitives']:
                mat=doc['materials'][prim['material']]
                if mat['name']!='Skate_Concrete':continue
                attr=prim['attributes'];idx=ext.accessor(prim['indices']).reshape(-1,3)
                uv=ext.accessor(attr['TEXCOORD_0'])[idx].mean(axis=1)
                texture=mat['pbrMetallicRoughness']['baseColorTexture']['index'];image=doc['textures'][texture]['source']
                pixels=np.asarray(Image.open(path.parent/doc['images'][image]['uri']).convert('RGB'),float)/255
                yy=np.clip(((1-(uv[:,1]%1))*pixels.shape[0]).astype(int),0,pixels.shape[0]-1);xx=np.clip(((uv[:,0]%1)*pixels.shape[1]).astype(int),0,pixels.shape[1]-1)
                color=pixels[yy,xx];color=np.where(color<=.04045,color/12.92,((color+.055)/1.055)**2.4)
                if 'COLOR_0' in attr:color*=ext.accessor(attr['COLOR_0'])[idx][...,:3].mean(axis=1)
                color*=np.asarray(mat['pbrMetallicRoughness'].get('baseColorFactor',[1,1,1,1]))[:3]
                vertices=ext.accessor(attr['POSITION'])[idx];area=np.linalg.norm(np.cross(vertices[:,1]-vertices[:,0],vertices[:,2]-vertices[:,0]),axis=1)*.5
                albedos.extend((color@np.array([.2126,.7152,.0722])).tolist());weights.extend(area.tolist())
        albedo={}
        if albedos:
            order=np.argsort(albedos);values=np.array(albedos)[order];cum=np.cumsum(np.array(weights)[order]);cum/=cum[-1]
            albedo={str(p):float(values[np.searchsorted(cum,p/100)]) for p in (5,50,95)}
        assert seen==embedded_images,(name,'image payload set')
        records.append(dict(indexed_corners_compared=corners,unconsumed_tangent_corner_differences=unused_tangent_differences,effective_concrete_linear_Y_area_percentiles=albedo,name=name,unique_mesh_triangles=sum(g.accessor(p['indices']).size//3 for m in doc['meshes'] for p in m['primitives']),gltf_bytes=path.stat().st_size,bin_bytes=len(ext.binary),embedded_build_bytes=embedded.stat().st_size,materials=len(doc['materials']),images=images,compressed_full_mip_MiB=memory))
    # Actual importer cache check: all three parks and repeat 101, in one scene.
    pointers={}
    for seed in (101,202,303,101):
        bpy.ops.import_scene.gltf(filepath=str((folder/f'Park_{seed}.gltf').resolve()))
        for im in bpy.data.images:
            if not im.filepath:continue
            path=str(Path(bpy.path.abspath(im.filepath)).resolve())
            if path not in all_images:continue
            if path in pointers:assert pointers[path]==im.as_pointer(),('Duplicate image allocation',path)
            pointers[path]=im.as_pointer()
    assert len(pointers)==len({str((folder/row['uri']).resolve()) for record in records[1:] for row in record['images']})
    report=dict(passed=True,rows=records,shared_imported_images=len(pointers),rendered_corner_attributes_and_image_payloads_equal=True,albedo_scope='Linear texture/vertex/factor product sampled at triangle centroids, weighted by uninstanced mesh area; not rendered brightness or an illumination measurement')
    old=Path('build/revision-before/preserved.json')
    if old.exists():
        protected=json.loads(old.read_text());root=Path(__file__).resolve().parents[2]
        changed=[p for p,d in protected.items() if not(root/p).exists() or hashlib.sha256((root/p).read_bytes()).hexdigest()!=d]
        assert not changed,changed;report['other_preserved_delivery_files']=len(protected)
    Path('build/external-check.json').write_text(json.dumps(report,indent=2));print('EXTERNAL PASS',len(pointers),'canonical images; geometry and payloads equal')
if __name__=='__main__':check(Path('export/final'))
