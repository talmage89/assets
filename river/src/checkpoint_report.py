"""Measured checkpoint tables; presentation stays local until acceptance."""
import json
from pathlib import Path


def main():
    resources=json.loads(Path('build/resources.json').read_text())
    costs=json.loads(Path('build/costs.json').read_text())
    check=json.loads(Path('build/check.json').read_text())
    fits=json.loads(Path('build/photo-calibration.json').read_text())
    lines=['# River revision checkpoint','',
           'Both places use freshly imported external-image glTF. No docs images or README gallery are added.',
           'The generator interface, section, module counts, canonical shared images and path/socket names remain.',
           '', '| Fix | Export views |','| --- | --- |',
           '| Riverfront buildings, working alleys and continuing town | `renders/checkpoint/101/hero.png`, `101/above.png` |',
           '| Riparian strip, agriculture, occupied road frontage | `renders/checkpoint/202/hero.png`, `202/above.png` |',
           '| Girder silhouette, seats, laminated pads, sole plates, anchors and keepers | both `under.png`, `bearings.png` |',
           '| Stem, wingwalls, approach and armored slope | both `abutment.png` |',
           '| Cutbank/sod/roots, point bar, bankfull wrack and broken riffle | both `bar.png`, `riffle.png` |',
           '| Warm raking light, depth/flow water, caused age and bank plants | both heroes, `pier.png`, `driver.png`, `riffle.png` |',
           '', 'All twenty comparisons are in `renders/fixes/`, 1280 pixels per side, with identical cameras.',
           'Changed inspection cameras use the reconstructed accepted `9b1c8bc` export and lighting.',
           'The unchanged cameras retain the original handoff frames. Receipts: `build/fix-evidence.json`.',
           '', '| Photo pair | RMS px |','| --- | ---: |']
    for name in ('urban','bank','under'):
        lines.append(f'| {name} | {fits[name]["residual_rms_pixels"]:.2f} |')
    lines += ['', 'Pairs: `renders/checkpoint-matches/*-pair.jpg`; assumed concrete/dock neutrals and gains are in the calibration receipt.',
              'The underside uses FHWA’s 2008 concrete I-beam photograph. Fits prove framing of the measured anchors, not appearance.',
              '', '| Module | Triangles | Referenced image MiB |','| --- | ---: | ---: |']
    for name in ('TypeIII_Girder18','DeckPanel6','Parapet6','PierColumns','PierWall','Abutment','GuardrailTerminal'):
        r=resources[name];n=sum(v['placed_triangles'] for v in r['categories'].values())
        lines.append(f'| {name} | {n:,} | {r["shared_image_mib"]:.2f} |')
    bearing=resources['RiverCrossing-101']['bearing_unit']
    lines.append(f'| Bearing stack (placed assembly) | {bearing["triangles_per_unit"]:,} | {bearing["shared_image_mib"]:.2f} |')
    lines += ['', 'Image allocations are shared, deduplicated full-mip estimates at 8bpp. Rows are not additive.',
              'New river images remain 4⅔ MiB: one 1024 bank/bed triple and two 512 images (plants/weather/foam and water normal).',
              '']
    for seed in (101,202):
        r=resources[f'RiverCrossing-{seed}']
        lines += ['| Crossing / category | Placed triangles | Unique triangles | Mesh instances | Shared image MiB |',
                  '| --- | ---: | ---: | ---: | ---: |']
        for name in ('bridge','reach','water','site','vegetation','cars','context'):
            v=r['categories'][name]
            lines.append(f'| {seed} / {name} | {v["placed_triangles"]:,} | {v["unique_triangles"]:,} | {v["mesh_instances"]:,} | {v["shared_image_mib"]:.2f} |')
        civil=sum(r['categories'][k]['placed_triangles'] for k in ('reach','water','site'))
        assert civil<150000
        lines += ['',f'{seed}: bed/banks + complete water + riverwalk/site **{civil:,} triangles**, below 150,000.',
                  f'glTF + BIN **{r["gltf_bytes"]+r["bin_bytes"]:,} bytes**; shared images **{r["shared_image_mib"]:.2f} MiB**.','']
    lines += [f'Both crossings’ image union: **{costs["texture_mib_bc8_mips"]:.2f} MiB**. Native cars/buildings/botany remain separate costs.',
              'The instanced context needs engine batching/culling/LOD; no frame-rate claim is made.',
              '', 'Proof: `make`, `make check`, `make repeat`, independent photo projection verification and exact five-image regeneration.',
              f'Preservation: **{check["preserved_files"]}** existing delivery files. Kit and top-level README are unchanged.',
              'Receipts: `build/check.json`, `resources.json`, `repeat.json`, `texture-repeat.json`, `render-check.json` and `fix-evidence.json`.',
              '', 'Full frame contact: `renders/checkpoint/contact.jpg`; photo contact: `renders/checkpoint-matches/contact.jpg`.',
              'The module sheet and 1.8m human/car scale shots are in the same checkpoint folder.',
              'Visual criticism and remaining CG cues are recorded in the last pass of [REVIEW.md](../REVIEW.md).','']
    Path('build/checkpoint-report.md').write_text('\n'.join(lines))


if __name__=='__main__':main()
