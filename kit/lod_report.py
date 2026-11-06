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
from kit.lod import configuration,tool_digests
from kit.lod_io import Document,digest,residency
from kit.fonts import find_font


def table(manifest):
    lines=['| Level | Triangles / target | Materials / draw calls | Geometry bytes | PNG bytes | Total load bytes | GPU unique textures + mesh, MiB | Switch height / distance |',
           '| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |']
    for row in manifest['levels']+[a for r in manifest['levels'] for a in r.get('alternatives',[])]:
        target='—' if row['level']==0 else f'{row["target_triangles"]:,}'
        switch='near' if row['level']==0 else f'{row["screen_height"]:.1%} / {row["distance_m"]:.2f} m'
        png=sum(i['bytes'] for i in row['images'])
        textures=sum(i['compressed_mip_bytes'] for i in {i['sha256']:i for i in row['images']}.values())
        label=f'LOD{row["level"]}'+(' camera-facing' if row.get('alternative') else '')
        lines.append(f'| {label} | {row["triangles"]:,} / {target} | {row["materials"]} / {row["draw_calls"]} | {row["geometry_bytes"]:,} | {png:,} | {row["package_bytes"]:,} | {textures/2**20:.3f} + {row["mesh_gpu_bytes"]/2**20:.4f} | {switch} |')
    return '\n'.join(lines)


def resident_text(m):
    r=m['resident'];unit=2**20
    result=('Whole-chain resident GPU estimate: **'+f"{r['total_gpu_bytes']/unit:.3f} MiB"+'**, versus LOD0 alone **'+f"{r['lod0_total_gpu_bytes']/unit:.3f} MiB"+
      '**. Unique textures '+f"{r['texture_gpu_bytes']/unit:.3f} MiB = {r['lod0_texture_gpu_bytes']/unit:.3f} MiB original + {r['proxy_texture_gpu_bytes']/unit:.3f} MiB proxy/impostor"+
      '; all meshes '+f"{r['mesh_gpu_bytes']/unit:.4f} MiB"+
      '. Increase over LOD0 '+f"{(r['total_gpu_bytes']-r['lod0_total_gpu_bytes'])/unit:.3f} MiB = {r['proxy_texture_gpu_bytes']/unit:.3f} MiB far maps + {r['additional_mesh_gpu_bytes']/unit:.4f} MiB additional mesh buffers"+
      '. Intermediate new images: '+str(len(r['unexpected_intermediate_images']))+
      '. Bind intermediate primitives to the canonical LOD0 material resources; the manifest records full image hashes and source image indices. '+
      'Identical embedded/external PNG bytes require this resource binding to share GPU allocations, including duplicate original image entries. GPU columns deduplicate complete image hashes within each row; PNG/dependency bytes retain physical payload copies. Optional camera-facing impostor is a separate alternative; engine overhead is excluded.')
    for index,row in enumerate(m['levels']):
        for alternative in row.get('alternatives',[]):
            choice=list(m['levels']);choice[index]=alternative
            cost=residency(choice)
            result+=(' Replacing the fixed far level with '+alternative['alternative']+' gives **'+
                     f"{cost['total_gpu_bytes']/unit:.3f} MiB"+'** for that complete alternative chain ('+
                     f"{cost['proxy_texture_gpu_bytes']/unit:.3f} MiB"+' new far maps).')
    return result


def block(cfg,m,status=None):
    if cfg.get('foliage_shader'):
        assembly_text=('Intermediate levels reduce branches and retain fewer, enlarged source leaf cards. '
                       'Their source UVs, bent normals and Wind fields remain; the last impostor freezes wind and lighting.')
    else:
        assembly_text=('Near levels consolidate static parts by material and simplify moving parts while retaining names, '
          'pivots, sockets and animation data. Both intermediate levels preserve original charts, attributes and LOD0 materials. ')
        if any(row.get('proxy') for row in m['levels']):
            assembly_text+=('The final proxy merges all moving geometry in its rest pose: its retained transform names are '
              'placement/socket metadata, and cannot animate that shell. Keep an animatable level while an interaction pose differs from rest. ')
        assembly_text+=('Only the proxy receives new charts baked from the immutable delivered maps and shaders. '
                        'LOD1/2 allocate no additional images.')
    lines=['<!-- LOD checkpoint: begin -->','#'*cfg.get('readme_level',2)+' Additional LODs','',
      '`make lod` builds additional core glTF/BIN files and a manifest under `export/lod/`; '
      '`make check-lod` checks them. The existing delivery is immutable LOD0. '
      'Default `make` and `make check` retain their original build graph.','',table(m),'',resident_text(m),'',
      'Distances are to the bound center at 60° vertical FOV / 1080p. GPU figures estimate 8-bpp block-compressed '
      'textures with full mips plus raw accessor mesh bytes, before engine overhead. Per-level map bytes describe dependencies, including reused originals. The whole-chain estimate deduplicates canonical image resources. '
      'Targets and achieved counts are reported separately; a count alone does not establish visual acceptance.','',
      'Load these files as alternatives and configure Godot visibility ranges, Unity LODGroup renderers, '
      'or Unreal mesh/component LODs. Keep matching near pivots in the same pose during switching. '
      '[Engine sources, pixel thresholds and texture policy](../kit/LOD.md).','',
      assembly_text,'',
      'Native-pixel LOD0/adjacent strips, amplified differences, close views and measured image status: '
      '`renders/lod/` (`contact.jpg`, `metrics.json`). Raw checks: `export/lod/check.json` and '
      '`normals-vs-lod0.json`; per-level construction/pruning decisions: '
      '`build/lod/<source stem>/simplification.json` and manifest assembly receipts. '
      '[Critique, target misses and known failures](../kit/LOD_REVIEW.md).']
    if status:lines[6:6]=['',status,'']
    from collections import Counter
    image_sizes=[]
    for row in m['levels']+[a for r in m['levels'] for a in r.get('alternatives',[])]:
        sizes=Counter(tuple(i['size']) for i in row['images'])
        label=f'LOD{row["level"]}'+(' camera-facing' if row.get('alternative') else '')
        image_sizes.append(label+': '+', '.join(f'{n} × {w}×{h}' for (w,h),n in sorted(sizes.items())))
    lines+=['','Shipped PNG dimensions: '+'; '.join(image_sizes)+'.']
    for row in m['levels'][1:]:
        assembly=row.get('assembly') or {}
        if assembly.get('separate_nodes'):
            lines+=['',f'LOD{row["level"]} separate moving meshes: '+', '.join('`'+n+'`' for n in assembly['separate_nodes'])+'.']
    if cfg.get('include_nodes'):
        lines+=['','This pilot selects `Canopy` (including islands) and `Dispenser_1`. LOD0 triangles, '
          'materials and draws describe those modules; its load bytes, maps and mesh allocation describe the complete '
          'unchanged station container. Extraction savings are separate from reduction. '
          'Dispenser close-ups accompany each level.']
    if cfg.get('foliage_shader'):
        lines+=['','LOD1/2 retain fewer, enlarged source leaf cards, their original UVs, bent normals and Wind fields; '
          'wood simplifies separately. LOD3 is four fixed crossed planes / eight triangles, one material and '
          'one draw, fitted jointly to 32 renders of this tree. It works without an engine controller. '
          'The separate camera-facing alternative has two triangles and a 32-sector atlas. '
          '`kit/lod_impostor.py:pose` is its reference controller. Both impostors freeze lighting and wind; '
          'overhead views, changing sun and continuous angular blending remain limitations.']
    lines+=['','<!-- LOD checkpoint: end -->','']
    return '\n'.join(lines)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('configs',nargs='+')
    p.add_argument('--write-readmes',action='store_true');p.add_argument('--docs',action='store_true')
    p.add_argument('--allow-failed',action='store_true',help='Report current failed evidence explicitly; never waive checks')
    args=p.parse_args();rows=[];text=['# LOD pilot checkpoint',''];cells=[]
    font=ImageFont.truetype(find_font('Noto Sans'),17)
    for config in args.configs:
        cfg,root,source,out=configuration(config);m=json.loads((out/'manifest.json').read_text())
        checks=json.loads((out/'check.json').read_text());renders=root/cfg.get('renders','renders/lod')
        metrics=json.loads((renders/'metrics.json').read_text());normals=json.loads((out/'normals-vs-lod0.json').read_text())
        if m.get('config_sha256')!=digest(config) or m.get('tools')!=tool_digests() or metrics.get('manifest_sha256')!=digest(out/'manifest.json') or checks.get('manifest_sha256')!=digest(out/'manifest.json') or (not args.allow_failed and not (checks['passed'] and metrics['passed'] and normals['passed'])) or normals['manifest_sha256']!=digest(out/'manifest.json') or normals.get('auditor_sha256')!=digest(ROOT/'kit/lod_normals.py') or metrics.get('renderer_sha256')!=digest(ROOT/'kit/lod_render.py') or Document(source).dependencies()!=m['baseline']:
            raise RuntimeError('Checkpoint is not current/passing: '+str(config))
        status=f'Chain check: {checks["passed"]}; image check: {metrics["passed"]}; normal check: {normals["passed"]}.'
        text+=['## '+cfg['kind'],'',status,'',table(m),'',resident_text(m),'']
        failures=[r for r in metrics['comparisons'] if not r['passed']]
        if failures:
            text+=['Failed views (reference and preceding level use the same limits):','',
                   '| View | Exceeded limits | Native comparison |',
                   '| --- | --- | --- |']
            for r in failures:
                label=f'LOD{r["level"]}'+('-camera-facing' if r.get('alternative') else '')
                exceeded=[]
                for comparison in ('reference','adjacent'):
                    for metric,limit in r['limits'].items():
                        value=r[comparison][metric]
                        if value>limit:exceeded.append(f'{comparison} {metric} {value:.4f} > {limit:.4f}')
                relative=(renders/f'{label}-{r["azimuth"]}-strip.jpg').relative_to(ROOT)
                text.append(f'| {label} / {r["azimuth"]}° | '+ '; '.join(exceeded)+f' | [strip](../../{relative}) |')
            text+=['']
        text += [f'Construction views and all differences: `{root.name}/{cfg.get("renders","renders/lod")}/`. Renderer: {metrics["renderer"]}.','']
        dependencies={}
        for row in m['levels']+[a for r in m['levels'] for a in r.get('alternatives',[])]:
            doc=Document(out/row['path'])
            for rel in doc.dependencies():
                path=(doc.path.parent/rel).resolve();dependencies[path]=path.stat().st_size
        distinct_bytes=sum(dependencies.values())
        text+=[f'Distinct payload dependencies for the delivery, including optional alternatives: **{distinct_bytes:,} bytes**, excluding audit JSONs.','']
        rows.append(dict(asset=root.name,resident=m['resident'],levels=m['levels'],chain_passed=checks['passed'],images_passed=metrics['passed'],normals_passed=normals['passed'],distinct_payload_bytes=distinct_bytes,
                         maximum_image_mean=max(r[k]['mean'] for r in metrics['comparisons'] for k in ['reference','adjacent'])))
        if args.write_readmes:
            readme=root/'README.md';old=readme.read_text();start='<!-- LOD checkpoint: begin -->';end='<!-- LOD checkpoint: end -->'
            addition=block(cfg,m,status)
            if start in old:
                a,b=old.split(start,1);_,c=b.split(end,1);new=a+addition.rstrip()+c
            elif cfg.get('readme_before') and cfg['readme_before'] in old:
                i=old.index(cfg['readme_before']);new=old[:i].rstrip()+'\n\n'+addition+old[i:]
            else:new=old.rstrip()+'\n\n'+addition
            readme.write_text(new)
        cell=Image.new('RGB',(800,610),(31,33,35));d=ImageDraw.Draw(cell)
        target_miss=any(row.get('target_met') is False for row in m['levels'])
        label=' — PASS'+('; target miss' if target_miss else '') if checks['passed'] and metrics['passed'] and normals['passed'] else ' — FAILED CHECKPOINT'
        d.text((16,12),cfg['kind']+label,font=font,fill='white')
        for j,row in enumerate(m['levels']):
            textures=sum(i['compressed_mip_bytes'] for i in {i['sha256']:i for i in row['images']}.values())
            s=f'LOD{row["level"]}: {row["triangles"]:,} tris, {row["package_bytes"]:,} B, unique maps {textures/2**20:.2f} MiB'
            d.text((16,42+j*23),s,font=font,fill=(210,215,220))
        resident=m['resident']
        d.text((16,134),f'Resident LOD0 -> chain: {resident["lod0_total_gpu_bytes"]/2**20:.2f} -> {resident["total_gpu_bytes"]/2**20:.2f} MiB; new intermediate images: {len(resident["unexpected_intermediate_images"])}',font=font,fill=(210,215,220))
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
            sheet.save(docs/'lod-reduced-pilots.jpg',quality=quality,optimize=True)
            if (docs/'lod-reduced-pilots.jpg').stat().st_size<=200000:break
        else:raise RuntimeError('Contact cannot meet docs byte budget')
    print(dest/'report.md');print(dest/'contact.jpg')


if __name__=='__main__':main()
