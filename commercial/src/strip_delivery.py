"""External shared-image strip packages. Never writes the station delivery."""
import argparse,copy,hashlib,json,os
from pathlib import Path
from deliver import read,sha,bundle


def part_materials(doc,meta):
    parents={c:i for i,n in enumerate(doc['nodes']) for c in n.get('children',[])};rows={}
    for i,node in enumerate(doc['nodes']):
        if 'mesh' not in node:continue
        owner=parents.get(i,i);name=doc['nodes'][owner].get('name',node.get('name'))
        if name.startswith('StripBoxwood_'):name='Landscape'
        row=rows.setdefault(name,dict(materials=set(),draw_primitives=0,triangles=0))
        for pr in doc['meshes'][node['mesh']]['primitives']:
            row['materials'].add(doc['materials'][pr['material']]['name']);row['draw_primitives']+=1;row['triangles']+=doc['accessors'][pr['indices']]['count']//3
    return {key:{**row,'materials':sorted(row['materials']),'material_count':len(row['materials'])} for key,row in rows.items()}


def run(seeds,folder=Path('build/strip-look')):
    result=[]
    roots=[Path('textures/ship'),Path('build/strip/signs-look'),Path('../ground/textures/ship'),Path('../shrubs/textures/ship'),Path('../houses/textures/ship')]
    known={sha(p):p for root in roots for p in root.glob('*.png')}
    for seed in seeds:
        source=folder/f'strip-{seed}.glb';doc,binary=read(source);out=Path(f'export/CommercialStrip-{seed}.gltf');out.parent.mkdir(parents=True,exist_ok=True);images=[]
        for im in doc['images']:
            view=doc['bufferViews'][im.pop('bufferView')];start=view.get('byteOffset',0);data=binary[start:start+view['byteLength']];digest=hashlib.sha256(data).hexdigest();chosen=known.get(digest)
            assert chosen is not None,('Unknown export map bytes',im)
            if chosen.parent in roots[:2]:
                dest=out.parent/'textures'/chosen.name;dest.parent.mkdir(parents=True,exist_ok=True)
                if not dest.exists() or dest.read_bytes()!=data:dest.write_bytes(data)
            else:dest=chosen
            im['uri']=os.path.relpath(dest,out.parent);im.pop('mimeType',None);images.append(dict(uri=im['uri'],sha256=digest,bytes=len(data)))
        used=sorted({a['bufferView'] for a in doc['accessors']});payload=bytearray();views=[];remap={}
        for old in used:
            payload.extend(b'\0'*(-len(payload)%4));v=copy.deepcopy(doc['bufferViews'][old]);start=v.get('byteOffset',0);data=binary[start:start+v['byteLength']];v['buffer']=0;v['byteOffset']=len(payload);payload.extend(data);remap[old]=len(views);views.append(v)
        for a in doc['accessors']:a['bufferView']=remap[a['bufferView']]
        meta=json.loads(source.with_suffix('.json').read_text())
        lights=[]
        for row in meta.get('fixture_lights',[]):
            light=dict(name=row['name']+' light',type='point' if row['kind']=='room' else 'spot',intensity=row['candela'],color=[1,.89,.72],range={'room':6.0,'walk':4.5,'lot':15.0}[row['kind']])
            if light['type']=='spot':light['spot']=dict(innerConeAngle=.45,outerConeAngle=1.20)
            x,y,z=row['position'];node=dict(name=light['name'],translation=[x,z,-y],extensions={'KHR_lights_punctual':dict(light=len(lights))})
            if light['type']=='spot':node['rotation']=[-.7071067811865476,0,0,.7071067811865476]
            doc['scenes'][doc.get('scene',0)].setdefault('nodes',[]).append(len(doc['nodes']));doc['nodes'].append(node);lights.append(light)
        if lights:
            doc.setdefault('extensions',{})['KHR_lights_punctual']=dict(lights=lights)
            doc.setdefault('extensionsUsed',[]).append('KHR_lights_punctual')
        doc['bufferViews']=views;doc['buffers']=[dict(uri=out.with_suffix('.bin').name,byteLength=len(payload))]
        out.with_suffix('.bin').write_bytes(payload);out.write_text(json.dumps(doc,separators=(',',':'))+'\n')
        meta=json.loads(source.with_suffix('.json').read_text());meta['delivery_bundle_sha256']=bundle(out);out.with_suffix('.json').write_text(json.dumps(meta,indent=2))
        row=dict(seed=seed,gltf_bytes=out.stat().st_size,bin_bytes=len(payload),glb_bytes=source.stat().st_size,materials=len(doc['materials']),parts=part_materials(doc,meta),images=images,bundle_sha256=bundle(out));result.append(row)
        print('STRIP DELIVERY',seed,row['materials'],'materials',row['gltf_bytes']+len(payload),'geometry bytes')
    (folder/'delivery.json').write_text(json.dumps(dict(rows=result,new_gpu_mib=20/3,scope='Only strip signage/deposit/emission maps are new. Gas manufactured tiles and ground/shrubs/optional house shingles keep canonical original bytes.'),indent=2)+'\n')

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--seeds',default='201,202,203,204');a.add_argument('--source-root',type=Path,default=Path('build/strip-look'));a=a.parse_args();run(map(int,a.seeds.split(',')),a.source_root)
