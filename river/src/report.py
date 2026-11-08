"""Measured delivery tables, unique image allocation and portable receipts."""
import hashlib
import json
from pathlib import Path
from PIL import Image


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
            gltf_bytes=row['gltf_bytes'],bin_bytes=row['bin_bytes'],material_states=row['materials'],placed_draws=draws))
    costs=dict(crossings=rows,unique_images=list(images.values()),image_count=len(images),
               texture_mib_bc8_mips=sum(i['mib_bc8_mips'] for i in images.values()))
    Path('build/costs.json').write_text(json.dumps(costs,indent=2)+'\n')
    lines=['| Piece | Triangles |','| --- | ---: |']
    lines += [f'| {m["name"]} | {m["triangles"]:,} |' for m in manifest['modules']]
    lines += ['','Flat panels intentionally stay below 300 triangles; no subdivisions are added for a minimum.','',
              '| Seed | Bridge | Bed / banks | Water | Site | Vegetation | Cars | Town / people | Total |',
              '| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
    for r in rows:
        c=r['categories'];lines.append('| '+str(r['seed'])+' | '+' | '.join(f'{c.get(k,0):,}' for k in ('bridge','reach','water','site','vegetation','cars','context'))+f' | {r["total"]:,} |')
    lines+=['','| Seed | glTF + BIN bytes | Material states / unbatched placed draws |','| --- | ---: | ---: |']
    for r in rows:lines.append(f'| {r["seed"]} | {r["gltf_bytes"]+r["bin_bytes"]:,} | {r["material_states"]} / {r["placed_draws"]} |')
    lines+=['',f'Both crossings share {len(images)} unique image payloads, estimated **{costs["texture_mib_bc8_mips"]:.2f} MiB** at 8bpp with full mips. PNG dependency bytes and uncompressed residency differ. These totals include native context; the new river-only allocation is listed above.','']
    path=Path('README.md');s=path.read_text();a='<!-- measured-costs:start -->';b='<!-- measured-costs:end -->'
    path.write_text(s[:s.index(a)+len(a)]+'\n'+'\n'.join(lines)+s[s.index(b):])
    print('MEASURED_COSTS',[(r['seed'],r['total']) for r in rows],len(images),costs['texture_mib_bc8_mips'])


if __name__=='__main__':main()
