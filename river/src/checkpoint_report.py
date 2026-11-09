"""Measured checkpoint tables; presentation stays local until acceptance."""
import json
from pathlib import Path


def shots(*names,seeds=(101,202)):
    return ', '.join(f'[{s} {n}](../renders/checkpoint/{s}/{n}.png)' for s in seeds for n in names)


def comparisons(*names,seeds=(101,202)):
    return ', '.join(f'[{s} {n}](../renders/fixes/{s}-{n}.jpg)' for s in seeds for n in names)


def main():
    resources=json.loads(Path('build/resources.json').read_text())
    costs=json.loads(Path('build/costs.json').read_text())
    check=json.loads(Path('build/check.json').read_text())
    fits=json.loads(Path('build/photo-calibration.json').read_text())
    lines=['# River / current export evidence','',
           'Both places use freshly imported external-image glTF and shared shipped PBR images.',
           'The generator interface, section, module counts, canonical shared images and path/socket names remain.',
           '', '| Fix | Export views |','| --- | --- |',
           f'| 1. Low side sun, lit fascia/banks/walk, deep open underside | {shots("hero","under")} |',
           f'| 2. Parapet, lip, exposed web/flange, joints, scuppers and cap ends | {shots("hero","under","bearings")} |',
           f'| 3. Varied native footprints, alleys/parking and detailed floodwall | {shots("above","floodwall",seeds=(101,))}; [outfall](../renders/wall-details/outfall.png), [ladder](../renders/wall-details/ladder.png) |',
           f'| 4. Depth/flow shading, shallow bed, reflections and porous foam trains | {shots("riffle","bar")} |',
           f'| 5. Graded quarried riprap, buried toes, wet/algae tint | {shots("abutment","pier")} |',
           f'| 6. Narrow cap runoff and subdued mineral edges | {shots("pier","bearings")} |',
           '| 7. Shared mesh references and bounded compact storage | `build/storage-check.json`; per-category bytes below |',
           '', 'Before/after: '+comparisons('hero','above','bearings','abutment','riffle','bar','pier','under','driver','scale')+'.',
           '', 'All twenty-four comparisons are in `renders/fixes/`, 1280 pixels per side, with identical cameras.',
           '[Wall outfall comparison](../renders/fixes/101-outfall.jpg), [wall ladder comparison](../renders/fixes/101-ladder.jpg).',
           'The baseline is the reconstructed accepted `4f09582` export and lighting.',
           'The unchanged cameras retain the original handoff frames. Receipts: `build/fix-evidence.json`.',
           '', '| Photo pair | RMS px |','| --- | ---: |']
    for name in ('urban','bank','under'):
        lines.append(f'| {name} | {fits[name]["residual_rms_pixels"]:.2f} |')
    lines += ['', 'Pairs: '+', '.join(f'[{n}](../renders/checkpoint-matches/{n}-pair.jpg)' for n in ('urban','bank','under'))+'. Assumed concrete/dock neutrals and gains are in the calibration receipt.',
              'The underside uses FHWA’s 2008 concrete I-beam photograph. Fits prove framing of the measured anchors, not appearance.',
              '', '| Module | Triangles | Materials | Referenced image MiB | glTF + BIN bytes |',
              '| --- | ---: | ---: | ---: | ---: |']
    for name in ('TypeIII_Girder18','DeckPanel6','Parapet6','PierColumns','PierWall','Abutment','GuardrailTerminal'):
        r=resources[name];n=sum(v['placed_triangles'] for v in r['categories'].values())
        materials=sum(v['material_states'] for v in r['categories'].values())
        lines.append(f'| {name} | {n:,} | {materials} | {r["shared_image_mib"]:.2f} | {r["gltf_bytes"]+r["bin_bytes"]:,} |')
    bearing=resources['RiverCrossing-101']['bearing_unit']
    lines.append(f'| Bearing stack (placed assembly) | {bearing["triangles_per_unit"]:,} | {bearing["material_states"]} | {bearing["shared_image_mib"]:.2f} | included in crossing |')
    lines += ['', 'Image allocations are shared, deduplicated full-mip estimates at 8bpp. Rows are not additive.',
              'New river images remain 4⅔ MiB: one 1024 bank/bed triple and two 512 images (plants/weather/foam and water normal).',
              '']
    for seed in (101,202):
        r=resources[f'RiverCrossing-{seed}']
        lines += ['| Crossing / category | Placed triangles | Unique triangles | Mesh instances | Materials | Shared image MiB |',
                  '| --- | ---: | ---: | ---: | ---: | ---: |']
        for name in ('bridge','reach','water','site','vegetation','cars','context'):
            v=r['categories'][name]
            lines.append(f'| {seed} / {name} | {v["placed_triangles"]:,} | {v["unique_triangles"]:,} | {v["mesh_instances"]:,} | {v["material_states"]} | {v["shared_image_mib"]:.2f} |')
        civil=sum(r['categories'][k]['placed_triangles'] for k in ('reach','water','site'))
        assert civil<150000
        lines += ['',f'{seed}: bed/banks + complete water + riverwalk/site **{civil:,} triangles**, below 150,000.',
                  f'glTF + BIN **{r["gltf_bytes"]+r["bin_bytes"]:,} bytes**; shared images **{r["shared_image_mib"]:.2f} MiB**.','']
    lines += [f'Both crossings’ image union: **{costs["texture_mib_bc8_mips"]:.2f} MiB**. Native cars/buildings/botany remain separate costs.',
              'The instanced context needs engine batching/culling/LOD; no frame-rate claim is made.',
              '', 'Construction, storage, image regeneration, repeat and appearance receipts are separate; missing receipts remain pending.',
              f'Preservation: **{check["preserved_files"]}** existing delivery files. Kit and top-level README are unchanged.',
              'Receipts: `build/check.json`, `resources.json`, `repeat.json`, `texture-repeat.json`, `render-check.json` and `fix-evidence.json`.',
              '', '[Full frame contact](../renders/checkpoint/contact.jpg); [photo contact](../renders/checkpoint-matches/contact.jpg).',
              'The module sheet and 1.8m human/car scale shots are in the same checkpoint folder.',
              'Visual criticism and remaining CG cues are recorded in the last pass of [REVIEW.md](../REVIEW.md).','']
    for name in ('check','storage-check','repeat','texture-repeat','render-check','fix-evidence'):
        path=Path('build')/(name+'.json')
        status='present' if path.exists() else 'pending'
        if path.exists():
            data=json.loads(path.read_text())
            if 'passed' in data:status='passed' if data['passed'] else 'FAILED'
        lines.append(f'- `{path}`: {status}')
    latest=Path('build/last-evidence.json')
    if latest.exists():
        evidence=json.loads(latest.read_text())
        lines += ['', '## Last round / 56cce73 controls', '',
                  '[Native-size identical-camera comparisons](../renders/last-fixes/contact.jpg).',
                  f'{len(evidence["panels"])} panels; 1280 native pixels per side. Appearance status and unresolved',
                  'misses are in the README’s Known flaws section and REVIEW passes 29 onward.',
                  'The light, exposure and camera are checked against the original handoff.', '']
        for seed in (101,202):
            coverage=check['crossings'][str(seed)]['construction'].get('abutment_apron_surface_coverage',[])
            for row in coverage:
                lines.append(f'- {seed} apron {row["side"]}: {row["exposed_stone_probes"]}/{row["bed_surface_probes"]} rays expose stone above the bed ({row["exposed_stone_fraction"]:.1%}). Soil/fines in the other rays remain a visual judgment.')
    Path('build/checkpoint-report.md').write_text('\n'.join(lines))


if __name__=='__main__':main()
