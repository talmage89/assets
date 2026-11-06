"""Actual external buffer/image byte costs, distinct from texture GPU estimates."""
import json
from pathlib import Path


def main():
    delivery=json.loads(Path('build/delivery.json').read_text());rows=[]
    for row in delivery['rows']:
        doc=json.loads(Path(row['delivery']).read_text());parts={}
        for node in doc['nodes']:
            if 'mesh' not in node:continue
            mesh=doc['meshes'][node['mesh']];views=set();vertices=0;triangles=0
            for p in mesh['primitives']:
                vertices+=doc['accessors'][p['attributes']['POSITION']]['count'];triangles+=doc['accessors'][p['indices']]['count']//3
                for ai in [p['indices'],*p['attributes'].values()]:views.add(doc['accessors'][ai]['bufferView'])
            payload=sum(doc['bufferViews'][i]['byteLength'] for i in views)
            parts[node['name']]=dict(triangles=triangles,split_vertices=vertices,attribute_index_bytes=payload,geometry_mib=round(payload/2**20,6),materials=sorted({doc['materials'][p['material']]['name'] for p in mesh['primitives']}),draws=len(mesh['primitives']))
        rows.append(dict(delivery=row['delivery'],triangles=row['triangles'],gltf_bytes=row['gltf_bytes'],bin_bytes=row['bin_bytes'],geometry_mib=round(row['bin_bytes']/2**20,6),file_bytes_without_shared_images=row['gltf_bytes']+row['bin_bytes'],parts=parts))
    maps=delivery['shared_images'];result=dict(rows=rows,shared_images=maps,shared_png_bytes=sum(m['bytes'] for m in maps),shared_compressed_mipmapped_texture_mib=16,shared_uncompressed_rgb_mipmapped_texture_mib=48,scope='Geometry memory is serialized vertex/index payload; an engine may repack attributes/indices. Three 2048 maps at 8 bpp with mips allocate 16 MiB once per loaded family; scalar wire surfaces allocate no maps. PNG disk bytes are separate.')
    Path('build/costs.json').write_text(json.dumps(result,indent=2));print('MEASURED COSTS',[(r['delivery'],r['triangles'],r['file_bytes_without_shared_images']) for r in rows],'; maps',result['shared_png_bytes'],'bytes; shared compressed mips 16 MiB')

if __name__=='__main__':main()
