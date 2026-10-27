"""Checkpoint contact and provenance checks. Never creates final docs images."""
import argparse,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.contact import contact,review_sheet
from crown_measure import projected_image

def main():
    p=argparse.ArgumentParser();p.add_argument('--renders',type=Path);p.add_argument('--check-audits',action='store_true');a=p.parse_args()
    build=ROOT/'trees/build/oak'
    if a.check_audits:
        reports=[json.loads((build/name).read_text()) for name in ['source-audit.json','game-audit.json']]
        digests=[r['sets']['PinOak']['geometry_sha256'] for r in reports]
        assert all(r['passed'] for r in reports) and digests[0]==digests[1], 'Independent source/game geometry differs'
        print('SOURCE/GAME geometry identical:',digests[0]);return
    r=a.renders
    names=['daylight','crown_up','silhouette','scale','structure','lower_pins','bark','family','oak_match_osu','oak_match_stony']
    meta=json.loads((r/'shots.json').read_text());sha=hashlib.sha256((build/'lookdev.blend').read_bytes()).hexdigest()
    for n in names:
        assert (r/(n+'.png')).is_file(),n
        assert meta[n]['source_sha256']==sha and meta[n]['engine']=='CYCLES', 'Stale/wrong-engine render: '+n
    paths=[r/(n+'.png') for n in names]
    contact(paths,r/'contact.jpg',title='Pin oak / STRUCTURE CHECKPOINT / prototype leaves')
    review_sheet([[r/'daylight.png',r/'structure.png'],[r/'family.png'],[r/'crown_up.png',r/'silhouette.png'],
                  [r/'oak_match_osu-pair.jpg'],[r/'oak_match_stony-pair.jpg'],[r/'bark.png',r/'lower_pins.png']],
                 r/'review-sheet.jpg',title='Pin oak / source form review; no final delivery claimed')
    tonal={n:projected_image(r/(n+'.png')) for n in ['oak_match_osu','oak_match_stony']}
    for row in tonal.values():
        row.pop('widest_height_at_12_4m',None)
        row['scope']='Selected green source-render pixels, display RGB, not albedo. No photographic color calibration.'
    report=dict(passed=True,stage='source structure checkpoint',source_sha256=sha,cycles_views=len(names),tonal=tonal)
    (r/'render-check.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
