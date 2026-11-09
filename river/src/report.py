"""Measured delivery tables, unique image allocation and portable receipts."""
import hashlib
import json
from pathlib import Path
from PIL import Image


def piece_census(doc):
    groups={}
    for node in doc['nodes']:
        if 'mesh' not in node or node.get('extras',{}).get('river_category')!='bridge':continue
        name=node['name'];key=name.split('_')[0]
        if name.startswith('Span_'):key='Span '+name.split('__')[1]
        n=sum(doc['accessors'][p['indices']]['count']//3 for p in doc['meshes'][node['mesh']]['primitives'])
        groups.setdefault(key,[]).append(n)
    return {key:dict(count=len(v),maximum=max(v),total=sum(v)) for key,v in sorted(groups.items())}


def main():
    manifest=json.loads(Path('build/manifest.json').read_text());rows=[];images={}
    for row in manifest['crossings']:
        seed=row['plan']['seed'];p=Path(f'export/RiverCrossing-{seed}.gltf');d=json.loads(p.read_text())
        draws=sum(len(d['meshes'][n['mesh']]['primitives']) for n in d['nodes'] if 'mesh' in n)
        for im in d.get('images',[]):
            path=(p.parent/im['uri']).resolve();digest=hashlib.sha256(path.read_bytes()).hexdigest()
            w,h=Image.open(path).size
            images[digest]=dict(uri=im['uri'],size=[w,h],bytes=path.stat().st_size,mib_bc8_mips=w*h*4/3/1048576)
        counts=row['triangles'];rows.append(dict(seed=seed,categories=counts,total=sum(counts.values()),
            gltf_bytes=row['gltf_bytes'],bin_bytes=row['bin_bytes'],material_states=row['materials'],placed_draws=draws,
            bridge_piece_census=piece_census(d)))
    costs=dict(crossings=rows,unique_images=list(images.values()),image_count=len(images),
               texture_mib_bc8_mips=sum(i['mib_bc8_mips'] for i in images.values()))
    Path('build/costs.json').write_text(json.dumps(costs,indent=2)+'\n')
    lines=['| Piece | Triangles |','| --- | ---: |']
    lines += [f'| {m["name"]} | {m["triangles"]:,} |' for m in manifest['modules']]
    lines += ['','Flat panels intentionally stay below 300 triangles; no subdivisions are added for a minimum.','',
              '| Assembled mesh type | Downtown count × max triangles | Edge count × max triangles |',
              '| --- | ---: | ---: |']
    groups=sorted(set().union(*(r['bridge_piece_census'] for r in rows)))
    for key in groups:
        cells=[]
        for r in rows:
            c=r['bridge_piece_census'].get(key)
            cells.append(f'{c["count"]} × {c["maximum"]:,}' if c else '—')
        lines.append('| '+key+' | '+' | '.join(cells)+' |')
    lines += ['',
              '| Seed | Bridge | Bed / banks | Water | Site | Vegetation | Cars | Town / people | Total |',
              '| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
    for r in rows:
        c=r['categories'];lines.append('| '+str(r['seed'])+' | '+' | '.join(f'{c.get(k,0):,}' for k in ('bridge','reach','water','site','vegetation','cars','context'))+f' | {r["total"]:,} |')
    lines+=['','| Seed | glTF + BIN bytes | Material states / unbatched placed draws |','| --- | ---: | ---: |']
    for r in rows:lines.append(f'| {r["seed"]} | {r["gltf_bytes"]+r["bin_bytes"]:,} | {r["material_states"]} / {r["placed_draws"]} |')
    resources=json.loads(Path('build/resources.json').read_text())
    lines += ['', '| Seed | Scene + river-owned PNG bytes | All referenced PNG bytes | Scene + standalone copies of all PNGs |',
              '| --- | ---: | ---: | ---: |']
    for seed in (101,202):
        r=resources[f'RiverCrossing-{seed}']
        assert r['scene_and_river_images_bytes']<120000000
        lines.append(f'| {seed} | {r["scene_and_river_images_bytes"]:,} | {r["external_png_bytes"]:,} | {r["standalone_copy_bytes"]:,} |')
    lines += ['', 'The original 367 MB measurement counted glTF + BIN. Both scenes also remain below 120 MB including their river-owned PNGs. Canonical library PNGs remain external, shared and byte-identical. Copying every shared dependency into a standalone folder costs the larger total above.']
    lines += ['', 'Shared full-mip image residency per crossing, including native context: '
              + ' / '.join(f'{seed}: **{resources[f"RiverCrossing-{seed}"]["shared_image_mib"]:.2f} MiB**'
                           for seed in (101,202)) + '. The two totals overlap and are not additive.']
    lines += ['','| Seed / category | Placed triangles | Unique triangles | Geometry bytes | Shared image MiB |',
              '| --- | ---: | ---: | ---: | ---: |']
    for seed in (101,202):
        for category,r in resources[f'RiverCrossing-{seed}']['categories'].items():
            lines.append(f'| {seed} / {category} | {r["placed_triangles"]:,} | {r["unique_triangles"]:,} | {r["geometry_buffer_bytes"]:,} | {r["shared_image_mib"]:.2f} |')
    lines += ['', 'Geometry bytes and image allocations are deduplicated within each row; shared rows are not additive.',
              '', '| Module | glTF + BIN bytes | Shared image MiB |','| --- | ---: | ---: |']
    for module in manifest['modules']:
        r=resources[module['name']]
        lines.append(f'| {module["name"]} | {r["gltf_bytes"]+r["bin_bytes"]:,} | {r["shared_image_mib"]:.2f} |')
    lines+=['',f'Both crossings share {len(images)} unique image payloads, estimated **{costs["texture_mib_bc8_mips"]:.2f} MiB** at 8bpp with full mips. PNG dependency bytes and uncompressed residency differ. These totals include native context; the new river-only allocation is listed above.','']
    path=Path('README.md');s=path.read_text();a='<!-- measured-costs:start -->';b='<!-- measured-costs:end -->'
    path.write_text(s[:s.index(a)+len(a)]+'\n'+'\n'.join(lines)+s[s.index(b):])
    print('MEASURED_COSTS',[(r['seed'],r['total']) for r in rows],len(images),costs['texture_mib_bc8_mips'])


if __name__=='__main__':main()
