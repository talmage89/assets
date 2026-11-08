"""Gather independently generated checkpoints; never turns failures into passes."""
import hashlib,json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
def main():
    paths=[BASE/'build/model-check.json',BASE/'build/determinism.json',BASE/'build/front-source.json',BASE/'build/front-delivery.json',
           BASE/'build/motion.json',BASE/'build/school-fit.json',BASE/'build/school-stage.json',
           BASE/'renders/seethrough/counts.json']+[BASE/f'build/delivery-{s}.json' for s in [101,102,103]]
    rows={str(p.relative_to(BASE)):json.loads(p.read_text())['passed'] for p in paths}
    deliveries=[json.loads((BASE/f'build/delivery-{s}.json').read_text()) for s in [101,102,103]]
    signatures=[sorted((uri,row['sha256']) for uri,row in r['images'].items()) for r in deliveries]
    rows['one_shared_atlas']=all(s==signatures[0] for s in signatures)
    rows['three_2048_maps_per_seed']=all(len(r['images'])==3 and all(im['size']==[2048,2048] for im in r['images'].values()) for r in deliveries)
    before=BASE/'build/preservation-before.json'
    if before.exists():
        hashes=json.loads(before.read_text());unchanged=all((BASE.parent/p).exists() and hashlib.sha256((BASE.parent/p).read_bytes()).hexdigest()==h for p,h in hashes.items())
        rows['existing_delivery_bytes']=unchanged
    # This round also preserved all other families' deliveries and docs.
    # The optional historical manifest stays ignored, beside its archived inputs.
    preservation=BASE.parent/'build/bus-round2/other-deliveries.json'
    if preservation.exists():
        hashes=json.loads(preservation.read_text())
        rows['all_other_family_delivery_bytes']=all(
            (BASE.parent/p).is_file() and hashlib.sha256((BASE.parent/p).read_bytes()).hexdigest()==digest
            for p,digest in hashes.items())
    bake=json.loads((BASE/'textures/4k/bake-report.json').read_text())
    rows['dense_mold_projection']=bake['front_projection']['independent_triangle_center_rays']['exact_surface_fallback_area_fraction']<=.01
    result=dict(passed=all(rows.values()),checks=rows,scope='Round 2 exported look checkpoint; construction, serialization, image provenance and material appearance are distinct proofs')
    (BASE/'build/checkpoint-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
    if not result['passed']:raise SystemExit(1)
if __name__=='__main__':main()
