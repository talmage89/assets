"""Measured delivered triangles/bytes, with shared maps counted once."""
import json
from PIL import Image
from pathlib import Path

def run():
 delivery=json.loads(Path('build/delivery.json').read_text());audit=json.loads(Path('build/delivery-check.json').read_text());checks=json.loads(Path('build/checks.json').read_text())
 raw={r['file']:r for r in audit['files']};rows=[]
 for r in delivery['rows']:
  a=raw[r['file']];document=json.loads(Path(r['file']).read_text());paths=[Path(r['file']).parent/im['uri'] for im in document.get('images',[])];used_mib=sum(Image.open(p).width*Image.open(p).height*4/3 for p in set(paths))/1048576
  rows.append(dict(file=r['file'],triangles=a['triangles'],materials=a['material_count'],json_bytes=r['json_bytes'],geometry_bytes=r['geometry_bytes'],unique_asset_bytes=r['json_bytes']+r['geometry_bytes'],geometry_buffer_mib=r['geometry_bytes']/1048576,referenced_shared_images=[p.name for p in paths],referenced_compressed_mips_mib=used_mib,geometry_plus_referenced_compressed_mib=used_mib+r['geometry_bytes']/1048576))
 parts=[r for r in rows if '/parts/' in r['file']];assemblies=[r for r in rows if '/parts/' not in r['file']]
 budgets=[]
 for s in checks['seeds']:
  b=s['budget'];masts=[r for r in b if r['kind']=='MastArm'];heads=[r for r in b if r['kind'].startswith('Head_')]
  group=[masts[i]['triangles']+masts[i+1]['triangles'] for i in (0,2)] if s['seed']==202 else [r['triangles'] for r in masts]
  budgets.append(dict(seed=s['seed'],complete_support_triangles=group,head_triangles=sorted(set(r['triangles'] for r in heads)),equipment_triangles=s['equipment_triangles'],parts=b))
 out=dict(parts=parts,intersections=assemblies,supports=budgets,maps=delivery['maps'],shared_map_bytes=delivery['shared_map_bytes'],all_geometry_and_json_bytes=sum(r['unique_asset_bytes'] for r in rows),all_delivery_bytes=sum(r['unique_asset_bytes'] for r in rows)+delivery['shared_map_bytes'],gpu_block_compressed_full_mips_mib=17.5,gpu_rgba8_full_mips_mib=70,scope='External glTF accessor index counts and actual file stat bytes. Scene context and arterial ground excluded. Shared images counted once; parts duplicate some assembly geometry by design. GPU figures are format estimates, not measured allocation.')
 Path('build/budget-report.json').write_text(json.dumps(out,indent=2))
 lines=['# Signals measured delivery','','Shared maps: '+str(out['shared_map_bytes'])+' bytes; 17.5 MiB compressed complete mips (70 MiB RGBA8).','','| Delivery | Triangles | Materials | glTF bytes | Geometry bytes |','| --- | ---: | ---: | ---: | ---: |']
 for r in rows:lines.append('| '+Path(r['file']).stem+' | '+str(r['triangles'])+' | '+str(r['materials'])+' | '+str(r['json_bytes'])+' | '+str(r['geometry_bytes'])+' |')
 lines+=['','| Delivery | Shared images, MiB | Geometry buffer, MiB | First use total, MiB |','| --- | ---: | ---: | ---: |']
 for r in rows:lines.append('| '+Path(r['file']).stem+' | '+f"{r['referenced_compressed_mips_mib']:.3f}"+' | '+f"{r['geometry_buffer_mib']:.3f}"+' | '+f"{r['geometry_plus_referenced_compressed_mib']:.3f}"+' |')
 lines+=['','Shared images are allocated once across loaded family parts; subsequent parts add only their geometry. Estimates assume 8-bpp image compression/full mips and no engine bookkeeping.','','Combined unique geometry/JSON: '+str(out['all_geometry_and_json_bytes'])+' bytes. Entire family including one map copy: '+str(out['all_delivery_bytes'])+' bytes.','',''+out['scope']]
 Path('build/budget-report.md').write_text('\n'.join(lines)+'\n');print('BUDGET',out['all_delivery_bytes'],'bytes, five shared maps;',len(rows),'deliveries')
if __name__=='__main__':run()
