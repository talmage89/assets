"""Compose an LOD checkpoint and opt-in README tables from checked manifests.

python3 kit/lod_report.py <asset>/src/lod.json ... [--write-readmes] [--docs]
Full-size per-level evidence stays beside each asset; the sheet is an index.
"""
import argparse
import json
import sys
from pathlib import Path

from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from kit.lod import configuration
from kit.lod_io import Document,digest
from kit.fonts import find_font


def table(manifest):
    lines=['| Level | Triangles / target | Materials | Geometry bytes | PNG bytes | Total load bytes | GPU textures + mesh, MiB | Switch height / distance |',
           '| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |']
    for row in manifest['levels']:
        target='—' if row['level']==0 else f'{row["target_triangles"]:,}'
        switch='near' if row['level']==0 else f'{row["screen_height"]:.1%} / {row["distance_m"]:.2f} m'
        png=sum(i['bytes'] for i in row['images'])
        lines.append(f'| LOD{row["level"]} | {row["triangles"]:,} / {target} | {row["materials"]} | {row["geometry_bytes"]:,} | {png:,} | {row["package_bytes"]:,} | {row["texture_gpu_bytes"]/2**20:.3f} + {row["mesh_gpu_bytes"]/2**20:.4f} | {switch} |')
    return '\n'.join(lines)


def block(cfg,m):
    lines=['<!-- LOD checkpoint: begin -->','#'*cfg.get('readme_level',2)+' Additional LODs','',
      '`make lod` builds additional glTF/BIN files under `export/lod/`; `make check-lod` independently checks them. '
      'The existing delivery is immutable LOD0. Default `make` and `make check` retain their original build graph.','',
      table(m),'',
      'Distances are to the bound center at a 60° vertical FOV / 1080p. GPU figures estimate 8-bpp block-compressed '
      'textures with full mips plus raw accessor mesh bytes, before engine overhead. PNG storage is separate. '
      'Each row is a cold load; URI/content caching can share images across levels. Targets are aspirations: '
      'the achieved counts retain geometry when reduction fails seam, silhouette, shading or topology checks.','',
      'Load the original and additional files as alternatives and explicitly configure Godot visibility ranges, '
      'Unity LODGroup renderers, or corresponding Unreal mesh/component LODs. A filename does not create an engine controller. '
      'Keep matching pivots in the same pose during switching. '
      '[Engine sources, thresholds, texture policy and limitations](../kit/LOD.md).','',
      'All ordinary moving geometry, sockets, skins and their frames stay separate and retain their delivered data. '
      'No pilot merges moving parts into its body. '
      'Embedded original PNGs are extracted once for the additional near levels; the original GLB keeps its embedded copy. '
      'A distant texture set saves residency only when larger maps are unloaded or streamed.','',
      'Native-pixel comparison strips, amplified differences and close views of every level: `renders/lod/`. '
      'The local `contact.jpg` indexes them; `metrics.json` records original/adjacent comparisons from three azimuths. '
      'Raw checks and immutable-input hashes: `export/lod/check.json` and `manifest.json`. '
      'Rejected component reductions: `build/lod/<source stem>/simplification.json`. '
      '[Two critique passes and the six-pilot sheet](../kit/LOD_REVIEW.md).']
    from collections import Counter
    image_sizes=[]
    for row in m['levels']:
        sizes=Counter(tuple(i['size']) for i in row['images'])
        image_sizes.append(f'LOD{row["level"]}: '+', '.join(f'{n} × {w}×{h}' for (w,h),n in sorted(sizes.items())))
    lines+=['','Shipped PNG dimensions: '+'; '.join(image_sizes)+'.']
    if cfg.get('include_nodes'):
        lines+=['','This pilot selects `Canopy` (including islands) and `Dispenser_1` from the original station. '
          'LOD0 triangle counts describe those modules, while its bytes/materials/maps describe the full unchanged station container. '
          'The new levels carry only selected geometry and its four materials, in the original station coordinates. '
          'Their canonical external maps remain shared. Separate dispenser close-ups accompany each level.']
    elif cfg['kind'].startswith('colonial'):
        lines+=['','The canonical tiling sets/trim remain shared at all levels; no parallel low-resolution building maps are added. '
          'Use engine mip streaming for texture residency. Only seed 27 is piloted.']
    elif cfg.get('foliage_shader'):
        lines+=['','LOD0 retains all leaf cards, bent normals and `_WIND`. Two ordinary near-level reduction trials failed the preservation gates '
          'and retained every triangle; those redundant levels are omitted from the accepted chain. '
          'The final 2-triangle billboard has a 32-sector 2048×1024 prelit RGBA atlas rendered from this tree. '
          'It needs a cylindrical camera-facing controller: rotate around glTF +Y; choose '
          '`round(azimuth / 11.25) mod 32`, where azimuth is the asset-to-camera angle in the local glTF X/Z plane; '
          'then select that tile of the 8×4 atlas. '
          'The stock glTF fallback shows sector zero. `kit/lod_impostor.py:pose` is the reference controller. '
          'Wind is frozen and lighting is baked at that level; overhead views, changing sun and continuous angular blending remain limitations.']
    lines+=['','<!-- LOD checkpoint: end -->','']
    return '\n'.join(lines)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('configs',nargs='+')
    p.add_argument('--write-readmes',action='store_true');p.add_argument('--docs',action='store_true')
    args=p.parse_args();rows=[];text=['# LOD pilot checkpoint',''];cells=[]
    font=ImageFont.truetype(find_font('Noto Sans'),17)
    for config in args.configs:
        cfg,root,source,out=configuration(config);m=json.loads((out/'manifest.json').read_text())
        checks=json.loads((out/'check.json').read_text());renders=root/cfg.get('renders','renders/lod')
        metrics=json.loads((renders/'metrics.json').read_text());normals=json.loads((out/'normals-vs-lod0.json').read_text())
        if checks.get('manifest_sha256')!=digest(out/'manifest.json') or not checks['passed'] or not metrics['passed'] or not normals['passed'] or normals['manifest_sha256']!=digest(out/'manifest.json') or normals.get('auditor_sha256')!=digest(ROOT/'kit/lod_normals.py') or metrics.get('renderer_sha256')!=digest(ROOT/'kit/lod_render.py') or Document(source).dependencies()!=m['baseline']:
            raise RuntimeError('Checkpoint is not current/passing: '+str(config))
        text+=['## '+cfg['kind'],'',table(m),'']
        dependencies={}
        for row in m['levels']:
            doc=Document(out/row['path'])
            for rel in doc.dependencies():
                path=(doc.path.parent/rel).resolve();dependencies[path]=path.stat().st_size
        distinct_bytes=sum(dependencies.values())
        text+=[f'Distinct payload dependencies for the whole chain: **{distinct_bytes:,} bytes**, excluding optional audit JSONs.','']
        rows.append(dict(asset=root.name,levels=m['levels'],distinct_payload_bytes=distinct_bytes,
                         maximum_image_mean=max(r['reference']['mean'] for r in metrics['comparisons'])))
        if args.write_readmes:
            readme=root/'README.md';old=readme.read_text();start='<!-- LOD checkpoint: begin -->';end='<!-- LOD checkpoint: end -->'
            addition=block(cfg,m)
            if start in old:
                a,b=old.split(start,1);_,c=b.split(end,1);new=a+addition.rstrip()+c
            elif cfg.get('readme_before') and cfg['readme_before'] in old:
                i=old.index(cfg['readme_before']);new=old[:i].rstrip()+'\n\n'+addition+old[i:]
            else:new=old.rstrip()+'\n\n'+addition
            readme.write_text(new)
        cell=Image.new('RGB',(800,610),(31,33,35));d=ImageDraw.Draw(cell)
        d.text((16,12),cfg['kind'],font=font,fill='white')
        for j,row in enumerate(m['levels']):
            s=f'LOD{row["level"]}: {row["triangles"]:,} tris, {row["package_bytes"]:,} B, texture {row["texture_gpu_bytes"]/2**20:.2f} MiB'
            d.text((16,42+j*23),s,font=font,fill=(210,215,220))
        # Near/far native comparisons retain aspect and are labeled as an index.
        first=m['levels'][1];last=m['levels'][-1]
        for j,row in enumerate([first,last]):
            if j and first['level']==last['level']:
                for k,li in enumerate([0,last['level']]):
                    close=Image.open(renders/f'close-LOD{li}.png').convert('RGBA')
                    background=Image.new('RGBA',close.size,(46,46,46,255));background.alpha_composite(close)
                    preview=background.convert('RGB');preview.thumbnail((340,210));cell.paste(preview,(30+k*380,375))
                continue
            strip=Image.open(renders/f'LOD{row["level"]}-55-strip.jpg').convert('RGB');strip.thumbnail((770,210))
            cell.paste(strip,(15,155+j*220))
        cells.append(cell)
    sheet=Image.new('RGB',(1600,610*((len(cells)+1)//2)),(25,27,29))
    for i,cell in enumerate(cells):sheet.paste(cell,(i%2*800,i//2*610))
    dest=ROOT/'build/lod-pilots';dest.mkdir(parents=True,exist_ok=True)
    sheet.save(dest/'contact.jpg',quality=92)
    (dest/'report.md').write_text('\n'.join(text));(dest/'report.json').write_text(json.dumps(rows,indent=2)+'\n')
    if args.docs:
        docs=ROOT/'kit/docs';docs.mkdir(exist_ok=True)
        for quality in range(88,39,-4):
            sheet.save(docs/'lod-pilots.jpg',quality=quality,optimize=True)
            if (docs/'lod-pilots.jpg').stat().st_size<=200000:break
        else:raise RuntimeError('Contact cannot meet docs byte budget')
    print(dest/'report.md');print(dest/'contact.jpg')


if __name__=='__main__':main()
