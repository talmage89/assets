"""Ignored checkpoint sheets and measured output inventory. No docs JPGs."""
import json
from pathlib import Path
import sys
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import review_sheet


def main():
    out=Path('renders/checkpoint');rows=[];stats={}
    for seed in (101,202):
        f=out/str(seed)
        for names in (('hero',),('above',),('aisle','ramp_turn'),('top_deck','entry'),('tower','scale')):
            paths=[f/(n+'.png') for n in names if (f/(n+'.png')).exists()]
            if paths:rows.append(paths)
        hero=f/'hero.png'
        if hero.exists():
            a=np.asarray(Image.open(hero).convert('RGB'),dtype=float)/255;y=a@np.array([.2126,.7152,.0722])
            stats[str(seed)]=dict(display_y_percentiles=np.percentile(y,[1,5,50,95,99]).tolist(),white_clipped_fraction=float((a.min(axis=2)>.985).mean()),
                caveat='Full frame includes sky and town; this is an exposure diagnostic, not physical albedo or a segmented garage mask.')
    if (out/'modules.png').exists():rows.append([out/'modules.png'])
    if rows:review_sheet(rows,out/'contact.jpg',width=2000,title='Parking garages / construction checkpoint / exported glTF')
    (Path('build')/'render-values.json').write_text(json.dumps(stats,indent=2)+'\n')
    manifest=json.loads(Path('build/manifest.json').read_text());lines=['# Checkpoint measured inventory','', '| Seed | Garage triangles | Stalls | Occupied | glTF + BIN bytes | Materials |','| --- | ---: | ---: | ---: | ---: | ---: |']
    for p in manifest['garages']:
        r=p['delivery'];lines.append(f"| {p['seed']} | {p['garage_triangles']:,} | {len(p['stalls'])} | {p['occupied']} | {r['gltf_bytes']+r['bin_bytes']:,} | {r['materials']} |")
    lines+=['','| Module | Triangles | glTF + BIN bytes |','| --- | ---: | ---: |']
    for name,r in manifest['modules'].items():lines.append(f"| {name} | {r['triangles']:,} | {r['gltf_bytes']+r['bin_bytes']:,} |")
    Path('build/metrics.md').write_text('\n'.join(lines)+'\n')
    print('CHECKPOINT SHEETS',out/'contact.jpg',flush=True)


if __name__=='__main__':main()
