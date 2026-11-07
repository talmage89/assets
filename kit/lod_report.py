"""Compose an LOD checkpoint and opt-in README tables from checked manifests.

python3 kit/lod_report.py <asset>/src/lod.json ... [--write-readmes] [--docs]
Full-size per-level evidence stays beside each asset; the sheet is an index.
"""
import argparse
import json
import os
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


def family_residency(chains):
    """Union canonical images and full original containers across module kinds.

    Each entry is (immutable source key, manifest). A repeated source contributes
    its original mesh allocation once; every additional kind/level contributes
    its own buffers. Optional far alternatives are not resident together.
    """
    images={};original_images={};sources={};additional=0;unexpected=set()
    for key,m in chains:
        zero=m['levels'][0];size=zero['mesh_gpu_bytes']
        if key in sources and sources[key]!=size:raise ValueError('Inconsistent full source-container allocation')
        sources[key]=size
        original={i['sha256'] for i in zero['images']}
        for image in zero['images']:original_images[image['sha256']]=image['compressed_mip_bytes']
        for row in m['levels']:
            if row['level']:additional+=row['mesh_gpu_bytes']
            for image in row['images']:
                h=image['sha256'];value=image['compressed_mip_bytes']
                if h in images and images[h]!=value:raise ValueError('Inconsistent canonical image allocation')
                images[h]=value
                if row['level'] and not (row.get('proxy') or row.get('impostor')) and h not in original:unexpected.add(h)
    original_mesh=sum(sources.values());textures=sum(images.values());original_textures=sum(original_images.values())
    return dict(original_containers=len(sources),original_texture_gpu_bytes=original_textures,
                additional_texture_gpu_bytes=sum(v for k,v in images.items() if k not in original_images),
                original_mesh_gpu_bytes=original_mesh,additional_mesh_gpu_bytes=additional,
                texture_gpu_bytes=textures,mesh_gpu_bytes=original_mesh+additional,
                lod0_total_gpu_bytes=original_textures+original_mesh,total_gpu_bytes=textures+original_mesh+additional,
                unexpected_intermediate_images=sorted(unexpected),passed=not unexpected)


def checkpoint_markers(cfg):
    label='LOD checkpoint'+(' '+cfg['readme_key'] if cfg.get('readme_key') else '')
    return '<!-- '+label+': begin -->','<!-- '+label+': end -->'


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


def block(cfg,m,status=None,kit_prefix="../kit"):
    start,end=checkpoint_markers(cfg)
    renders=cfg.get("renders","renders/lod")
    output=cfg.get("output","export/lod")
    if cfg.get('foliage_shader'):
        assembly_text=('Intermediate levels reduce branches and retain fewer, enlarged source leaf cards. '
                       'Their source UVs, bent normals and Wind fields remain; the last impostor freezes wind and lighting.')
    else:
        assembly_text=('Near levels consolidate static parts by material and simplify moving parts while retaining names, '
          'pivots, sockets and animation data. Intermediate levels preserve original charts, attributes and LOD0 materials. ')
        if any(row.get('proxy') for row in m['levels']):
            assembly_text+=('The final proxy merges all moving geometry in its rest pose: its retained transform names are '
              'placement/socket metadata, and cannot animate that shell. Keep an animatable level while an interaction pose differs from rest. ')
        assembly_text+=('Only the proxy receives new charts baked from the immutable delivered maps and shaders. '
                        'Intermediate levels allocate no additional images.')
    lines=[start,'#'*cfg.get('readme_level',2)+' '+cfg.get('readme_title','Additional LODs'),'',
      f'`make lod` builds additional core glTF/BIN files and a manifest under `{output}/`; '
      '`make check-lod` checks them. The existing delivery is immutable LOD0. '
      'Default `make` and `make check` retain their original build graph.','',table(m),'',resident_text(m),'',
      'Distances are to the bound center at 60° vertical FOV / 1080p. GPU figures estimate 8-bpp block-compressed '
      'textures with full mips plus raw accessor mesh bytes, before engine overhead. Per-level map bytes describe dependencies, including reused originals. The whole-chain estimate deduplicates canonical image resources. '
      'Targets and achieved counts are reported separately; a count alone does not establish visual acceptance.','',
      'Load these files as alternatives and configure Godot visibility ranges, Unity LODGroup renderers, '
      'or Unreal mesh/component LODs. Keep matching near pivots in the same pose during switching. '
      f'[Engine sources, pixel thresholds and texture policy]({kit_prefix}/LOD.md).','',
      assembly_text,'',
      'Native-pixel LOD0/adjacent strips, amplified differences, close views and measured image status: '
      f'`{renders}/` (`contact.jpg`, `metrics.json`). Raw checks: `{output}/check.json` and '
      f'`{output}/normals-vs-lod0.json`; per-level construction/pruning decisions: '
      '`build/lod/<source stem>/simplification.json` and manifest assembly receipts. '
      f'[Critique, target misses and known failures]({kit_prefix}/LOD_REVIEW.md).']
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
        for part in assembly.get('retained_source_geometry',[]):
            lines+=['',f'LOD{row["level"]} retains original geometry for `{part["node"]}`: '
                    f'{part["source_triangles"]:,} triangles instead of {part["reduced_triangles"]:,} reduced triangles '
                    '(measured grazing-layer exception; original frame, materials and maps).']
    if cfg.get('include_nodes'):
        lines+=['','Selected placement roots: '+', '.join('`'+n+'`' for n in cfg['include_nodes'])+'. LOD0 triangles, '
          'materials and draws describe those modules; its load bytes, maps and mesh allocation describe the complete '
          'unchanged original container. Extraction savings are separate from reduction. '
          'Retain child transforms when replacing a selected root placement.']
    if cfg.get('foliage_shader'):
        lines+=['','LOD1/2 retain fewer, enlarged source leaf cards, their original UVs, bent normals and Wind fields; '
          'wood simplifies separately. LOD3 is four fixed crossed planes / eight triangles, one material and '
          'one draw, fitted jointly to 32 renders of this tree. It works without an engine controller. '
          'The separate camera-facing alternative has two triangles and a 32-sector atlas. '
          '`kit/lod_impostor.py:pose` is its reference controller. Both impostors freeze lighting and wind; '
          'overhead views, changing sun and continuous angular blending remain limitations.']
    lines+=['',end,'']
    return '\n'.join(lines)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('configs',nargs='+')
    p.add_argument('--write-readmes',action='store_true');p.add_argument('--docs',action='store_true')
    p.add_argument('--allow-failed',action='store_true',help='Report current failed evidence explicitly; never waive checks')
    p.add_argument('--out',default='build/lod-pilots',help='Report directory relative to the repository')
    p.add_argument('--family-root',help='Union all configs under this repository-relative family root')
    args=p.parse_args();rows=[];text=['# LOD checkpoint',''];cells=[];families={}
    dest=(ROOT/args.out).resolve()
    family_root=(ROOT/args.family_root).resolve() if args.family_root else None
    font=ImageFont.truetype(find_font('Noto Sans'),17)
    for config in args.configs:
        cfg,root,source,out=configuration(config);m=json.loads((out/'manifest.json').read_text())
        checks=json.loads((out/'check.json').read_text());renders=root/cfg.get('renders','renders/lod')
        metrics=json.loads((renders/'metrics.json').read_text());normals=json.loads((out/'normals-vs-lod0.json').read_text())
        if m.get('config_sha256')!=digest(config) or m.get('tools')!=tool_digests() or metrics.get('manifest_sha256')!=digest(out/'manifest.json') or checks.get('manifest_sha256')!=digest(out/'manifest.json') or (not args.allow_failed and not (checks['passed'] and metrics['passed'] and normals['passed'])) or normals['manifest_sha256']!=digest(out/'manifest.json') or normals.get('auditor_sha256')!=digest(ROOT/'kit/lod_normals.py') or metrics.get('renderer_sha256')!=digest(ROOT/'kit/lod_render.py') or Document(source).dependencies()!=m['baseline']:
            raise RuntimeError('Checkpoint is not current/passing: '+str(config))
        status=f'Chain check: {checks["passed"]}; image check: {metrics["passed"]}; normal check: {normals["passed"]}.'
        text+=['## '+cfg['kind'],'',status,'',table(m),'',resident_text(m),'']
        if checks.get('errors'):
            text+=['Raw check errors:','']+['- '+error for error in checks['errors']]+['']
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
                relative=Path(os.path.relpath(renders/f'{label}-{r["azimuth"]}-strip.jpg',dest)).as_posix()
                text.append(f'| {label} / {r["azimuth"]}° | '+ '; '.join(exceeded)+f' | [strip]({relative}) |')
            text+=['']
        text += [f'Construction views and all differences: `{root.name}/{cfg.get("renders","renders/lod")}/`. Renderer: {metrics["renderer"]}.','']
        dependencies={}
        for row in m['levels']+[a for r in m['levels'] for a in r.get('alternatives',[])]:
            doc=Document(out/row['path'])
            for rel in doc.dependencies():
                path=(doc.path.parent/rel).resolve();dependencies[path]=path.stat().st_size
        distinct_bytes=sum(dependencies.values())
        text+=[f'Distinct payload dependencies for the delivery, including optional alternatives: **{distinct_bytes:,} bytes**, excluding audit JSONs.','']
        if family_root and not root.is_relative_to(family_root):raise ValueError('Config is outside --family-root')
        families.setdefault(family_root or root,[]).append(((str(source.resolve()),digest(source)),m))
        rows.append(dict(asset=root.name,kind=cfg['kind'],config=str(Path(config)),resident=m['resident'],levels=m['levels'],chain_passed=checks['passed'],chain_errors=checks.get('errors',[]),images_passed=metrics['passed'],normals_passed=normals['passed'],distinct_payload_bytes=distinct_bytes,
                         maximum_image_mean=max(r[k]['mean'] for r in metrics['comparisons'] for k in ['reference','adjacent'])))
        if args.write_readmes:
            readme=root/'README.md';old=readme.read_text();start,end=checkpoint_markers(cfg)
            addition=block(cfg,m,status,kit_prefix=Path(os.path.relpath(ROOT/"kit",root)).as_posix())
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
    family_costs={str(root.relative_to(ROOT)):family_residency(chains) for root,chains in families.items()}
    for root,chains in families.items():
        if len(chains)<2:continue
        cost=family_costs[str(root.relative_to(ROOT))]
        text+=['## '+root.name+' shared-resource union','',
            '| Allocation | MiB |','| --- | ---: |']
        for label,key in [('Original maps once','original_texture_gpu_bytes'),('Additional maps','additional_texture_gpu_bytes'),
                          ('Original containers once','original_mesh_gpu_bytes'),('Every additional mesh','additional_mesh_gpu_bytes'),
                          ('Whole family','total_gpu_bytes')]:
            text.append(f'| {label} | {cost[key]/2**20:.4f} |')
        text+=['','Canonical image hashes are deduplicated across kinds; each full immutable original container is counted once. Additional geometry for every kind/level remains resident. These estimates exclude engine overhead.','']
    sheet=Image.new('RGB',(1600,610*((len(cells)+1)//2)),(25,27,29))
    for i,cell in enumerate(cells):sheet.paste(cell,(i%2*800,i//2*610))
    dest.mkdir(parents=True,exist_ok=True)
    sheet.save(dest/'contact.jpg',quality=92)
    (dest/'report.md').write_text('\n'.join(text));(dest/'report.json').write_text(json.dumps(rows,indent=2)+'\n')
    (dest/'families.json').write_text(json.dumps(family_costs,indent=2)+'\n')
    if args.docs:
        docs=ROOT/'kit/docs';docs.mkdir(exist_ok=True)
        for quality in range(88,39,-4):
            sheet.save(docs/'lod-reduced-pilots.jpg',quality=quality,optimize=True)
            if (docs/'lod-reduced-pilots.jpg').stat().st_size<=200000:break
        else:raise RuntimeError('Contact cannot meet docs byte budget')
    print(dest/'report.md');print(dest/'contact.jpg')


if __name__=='__main__':main()
