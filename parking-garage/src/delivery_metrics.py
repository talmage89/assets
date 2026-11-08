"""Measured payload and shared-image costs, separated from placed actors."""
import json
from pathlib import Path
from PIL import Image


def resource(path,triangles):
    path=Path(path);doc=json.loads(path.read_text());maps={}
    for row in doc.get('images',[]):
        p=(path.parent/row['uri']).resolve();w,h=Image.open(p).size
        maps[str(p)]=dict(bytes=p.stat().st_size,mib=w*h*4/3/2**20)
    return dict(triangles=triangles,gltf_bytes=path.stat().st_size,bin_bytes=path.with_suffix('.bin').stat().st_size,
        geometry_bytes=path.stat().st_size+path.with_suffix('.bin').stat().st_size,materials=len(doc.get('materials',[])),images=len(maps),
        referenced_png_bytes=sum(v['bytes'] for v in maps.values()),texture_mib=sum(v['mib'] for v in maps.values()))


def main():
    modules={name:resource(Path('export/lookdev/modules')/(name+'.gltf'),row['triangles']) for name,row in json.loads(Path('build/lookdev/modules.json').read_text()).items()}
    garages={str(seed):resource(f'export/lookdev/ParkingGarageLook-{seed}.gltf',json.loads(Path(f'build/lookdev/look-{seed}.json').read_text())['garage_triangles']) for seed in (101,202)}
    report=dict(modules=modules,garages=garages,memory_basis='8bpp per map with full 4/3 mip chain. Shared image references are charged once per package; they are not incremental per module instance.')
    Path('build/delivery-metrics.json').write_text(json.dumps(report,indent=2)+'\n')
    lines=['| Module | Triangles | glTF + BIN bytes | Materials | Referenced image MiB |','| --- | ---: | ---: | ---: | ---: |']
    for name,row in modules.items():lines.append(f"| {name} | {row['triangles']:,} | {row['geometry_bytes']:,} | {row['materials']} | {row['texture_mib']:.2f} |")
    Path('build/delivery-metrics.md').write_text('\n'.join(lines)+'\n')
    print('DELIVERY METRICS',garages,flush=True)


if __name__=='__main__':main()
