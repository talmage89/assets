"""Rebuild the numerical checkpoint report; never writes gallery images."""
import argparse,json
from pathlib import Path


def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |',
                      *['| '+' | '.join(map(str,row))+' |' for row in rows]])+'\n'


def report(folder):
    look=json.loads(Path('build/look-check.json').read_text());checks=json.loads(Path('build/check.json').read_text())
    exports={p.stem:json.loads(p.read_text()) for p in Path('export').glob('*.json')}
    provenance=json.loads((folder/'provenance.json').read_text()) if (folder/'provenance.json').exists() else []
    text=['# Manufactured communities / numerical look-dev receipt\n']
    homes=[]
    for stem in ('SingleWide-120','SingleWide-147','SingleWide-168','DoubleWide-245','DoubleWide-228','DoubleWide-326'):
        d=exports[stem];p=d['plan'];r=look['exports'][stem]
        homes.append([stem,p['era'],' × '.join(map(str,p['nominal_ft'])),f'{d["triangles"]:,}',d['materials'],f'{r["gpu_mib"]:.2f}',f'{d["geometry_bytes"]:,}'])
    text += [table(['Home','Era','Body ft','Triangles incl. both steps','Materials','Shared GPU MiB','glTF + BIN bytes'],homes)]
    parks=[];lots=[];context=[]
    for stem,d in exports.items():
        if not stem.startswith('Park-'):continue
        p=d['plan'];r=look['exports'][stem];c=checks['construction'][stem]
        parks.append([stem,len(p['lots']),f'{p["lot_frontage"]/.3048:g} × {p["lot_depth"]/.3048:g}',p['lot_area_sqft'],
                      f'{d["gross_acres"]:.4f}',f'{d["homes_per_acre"]:.4f}',f'{d["triangles"]:,}',f'{d["unique_export_triangles"]:,}',
                      d['materials'],r['unbatched_primitives'],f'{d["geometry_bytes"]:,}',f'{r["gpu_mib"]:.4f}'])
        for lot in p['lots']:
            number=lot['number'];h=lot['home'];body=d['assemblies'][f'Lot_{number:02}_Home'];all_=d['assemblies'][f'Lot_{number:02}']
            lots.append([stem,number,h['variant_id'],h['occupant_seed'],h['era'],' × '.join(map(str,h['nominal_ft'])),
                         f'{body["triangles"]:,}',f'{all_["triangles"]:,}',f'{all_["unique_triangles"]:,}'])
        row=next((q for q in provenance if q['stem']==stem and q['shot']=='hero'),None)
        if row:
            for category,n in row['context']['triangles'].items():
                context.append([stem,category,f'{n:,}',f'{row["context"]["unique_triangles"][category]:,}'])
        text += [f'{stem}: measured core road {c["road_width_mesh_m"]:.6f}m; home-envelope separation '
                 f'{min(c["home_separation_mesh_m"]):.4f}–{max(c["home_separation_mesh_m"]):.4f}m; '
                 f'{c["static_assembly_pairs_checked"]} between-assembly comparisons.\n']
    text += [table(['Park','Homes','Lot ft','Lot sqft','Gross acres','Homes/acre','Placed triangles','Unique triangles','Materials','Unbatched primitives','glTF + BIN bytes','Shared GPU MiB'],parks)]
    text += ['Per-lot totals include home, native props, local flatwork, resident storage and small edge plants. '
             'Cars, large trees/shrubs and surrounding town are outside these exports. Unique triangles count '
             'distinct exported meshes; placed totals count every node instance.\n',
             table(['Park','Lot','Template','Occupant seed','Era','Body ft','Home triangles','Lot placed triangles','Lot unique triangles'],lots)]
    if context:text += [table(['Presentation park','Category','Placed triangles','Unique triangles'],context)]
    modules=[]
    for stem in ('Deck','Carport','UtilityService','PropaneBottles','Condenser','WindowAC','SatelliteDish','AddedRoom','Household','EntranceSign','SupportFrame'):
        d=exports[stem];modules.append([stem,f'{d["triangles"]:,}',d['materials'],f'{d["geometry_bytes"]:,}'])
    text += [table(['Inspection module','Triangles','Materials','glTF + BIN bytes'],modules)]
    new=look['new_set'];text += [f'New shared set: {new["size"]}² BaseColor / OpenGL +Y Normal / ORM, '
                               f'{sum(i["bytes"] for i in new["images"]):,} PNG bytes, {new["gpu_mib"]} MiB. '
                               f'Complete static image union {look["union_gpu_mib"]:.4f} MiB at 8bpp with full mip chains. '
                               'Shared images are allocated once when cached by canonical URI.\n']
    cameras=json.loads(Path('build/cameras.json').read_text())
    text += [table(['Comparison','Native anchor RMS px','Estimated crop lens mm','Anchor count'],
                   [[name,f'{d["residual_rms_pixels"]:.3f}',f'{d["shot"]["lens"]:.2f}',len(d['landmarks_world_m'])] for name,d in cameras.items()])]
    text += [f'Checks pass for {len(checks["exports"])} exports, {checks["plan_sweep_count"]} deterministic plans '
             f'and {checks["preserved_delivery_files"]} immutable pre-existing files. Serialization, sampled '
             'construction/motion and photographic appearance have separate scopes.\n']
    Path('build/metrics.md').write_text('\n'.join(text))
    Path('build/metrics.json').write_text(json.dumps(dict(homes=homes,parks=parks,lots=lots,context=context,new_set=new),indent=2))
    print('METRICS',len(homes),'homes,',len(lots),'lots,',len(context),'context categories')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--renders',type=Path,default=Path('renders/checkpoint/look3'));a=p.parse_args();report(a.renders)
