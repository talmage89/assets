"""Actual on-disk delivery costs; optional README measured-table refresh."""
import argparse,json
from pathlib import Path
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--readme',action='store_true');a=p.parse_args()
blocks=[];rows=[];street=[]
for region in ('midwest','western','northeast','southern'):
 m=json.loads((Path('build/blocks')/region/'block.json').read_text());bs=[]
 for lot,b in zip(m['lots'],m['buildings']):
  path=Path(b['source']);d=json.loads(path.read_text());r=dict(id=b['id'],stories=lot['stories'],corner=lot['corner'],lot_ft=[round(lot['width']/.3048),round(lot['depth']/.3048)],height_m=lot['height'],triangles=b['triangles'],materials=len(d['materials']),gltf_bytes=path.stat().st_size,bin_bytes=path.with_suffix('.bin').stat().st_size)
  rows.append(r);bs.append(r)
 glb=Path('build/blocks')/region/'block.glb'
 blocks.append(dict(region=region,seed=m['seed'],width_m=m['width'],triangles=sum(r['triangles'] for r in bs),geometry_bytes=sum(r['gltf_bytes']+r['bin_bytes'] for r in bs),diagnostic_glb_bytes=glb.stat().st_size))
 path=Path('export')/('DowntownStreet_'+region+'.gltf');meta=json.loads((Path('build/blocks')/region/'street.json').read_text())
 street.append(dict(region=region,triangles=meta['triangles'],geometry_bytes=path.stat().st_size+path.with_suffix('.bin').stat().st_size))
images=[dict(name=p.name,bytes=p.stat().st_size,size=list(Image.open(p).size)) for p in sorted(Path('export/textures').glob('*.png'))]
report=dict(buildings=rows,blocks=blocks,street=street,images=images,building_geometry_bytes=sum(r['geometry_bytes'] for r in blocks),street_geometry_bytes=sum(r['geometry_bytes'] for r in street),shared_image_bytes=sum(r['bytes'] for r in images),compressed_mip_MiB=sum(r['size'][0]*r['size'][1]*4/3 for r in images)/2**20)
report['family_bytes']=sum(report[k] for k in ('building_geometry_bytes','street_geometry_bytes','shared_image_bytes'))
Path('build/summary.json').write_text(json.dumps(report,indent=2)+'\n')
print('DELIVERY',json.dumps({k:v for k,v in report.items() if k not in ('buildings','blocks','street','images')}))
if a.readme:
 lines=['| Block / seed | Frontage m | Building triangles | glTF + bin bytes | Diagnostic GLB bytes |','| --- | ---: | ---: | ---: | ---: |']
 for r in blocks:lines.append(f"| {r['region']} / {r['seed']} | {r['width_m']:.3f} | {r['triangles']:,} | {r['geometry_bytes']:,} | {r['diagnostic_glb_bytes']:,} |")
 lines+=['','| Building | Lot ft | Stories | Front datum m | Triangles | Materials | glTF + bin bytes |','| --- | --- | ---: | ---: | ---: | ---: | ---: |']
 for r in rows:lines.append(f"| {r['id']} | {r['lot_ft'][0]} × {r['lot_ft'][1]} | {r['stories']} | {r['height_m']:.3f} | {r['triangles']:,} | {r['materials']} | {r['gltf_bytes']+r['bin_bytes']:,} |")
 lines+=['','| Street piece | Triangles | glTF + bin bytes |','| --- | ---: | ---: |']
 for r in street:lines.append(f"| {r['region']} | {r['triangles']:,} | {r['geometry_bytes']:,} |")
 lines+=['','Front datums are authored parapet/cornice levels. Covers rise 45 mm above them;','seeded stepped rear parapets rise up to 480 mm farther. These are plan values,','not reported as independent height measurements.','',f"The 28 buildings total **{report['building_geometry_bytes']:,} bytes** of glTF/bin;",f"four street pieces total **{report['street_geometry_bytes']:,} bytes**. Eleven shared",f"images total **{report['shared_image_bytes']:,} bytes**. The deliverable family is",f"**{report['family_bytes']:,} bytes**, excluding diagnostic GLBs and presentation context."]
 path=Path('README.md');s=path.read_text();start=s.index('<!-- METRICS_START -->')+len('<!-- METRICS_START -->');end=s.index('<!-- METRICS_END -->');path.write_text(s[:start]+'\n'+'\n'.join(lines)+'\n'+s[end:])
