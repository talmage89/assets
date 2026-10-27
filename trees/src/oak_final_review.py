"""Final oak presentation provenance, contacts and optional two family docs JPGs."""
import argparse,sys,json,hashlib
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.contact import contact,review_sheet
from oak_evidence import evidence
NAMES=['hero','front','side','back','top','branchlet','cluster_3m','bark','bark_raking','lower_pins','crown_up','scale','root_flare','family','oak_match_osu','oak_match_stony']
p=argparse.ArgumentParser();p.add_argument('--renders',type=Path,default=ROOT/'trees/renders/oak-final');p.add_argument('--docs',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
r=a.renders;glb=ROOT/'trees/export/PinOak.glb';sha=hashlib.sha256(glb.read_bytes()).hexdigest()
meta=json.loads((r/'shots.json').read_text());eevee=r.parent/'oak-final-eevee';em=json.loads((eevee/'shots.json').read_text())
for name in NAMES:
    row=meta[name]
    assert (r/(name+'.png')).exists() and row['source_sha256']==sha and row['stage'].startswith('EXPORTED GLB') and row['engine']=='CYCLES','Stale/non-GLB '+name
assert em['hero']['source_sha256']==sha and em['hero']['engine']=='BLENDER_EEVEE'
assert meta['family']['maple_source_sha256']==hashlib.sha256((ROOT/'trees/export/RedMaple.glb').read_bytes()).hexdigest(),'Stale family maple'
values=evidence(r,glb)
assert all(row['within_03'] for row in values['foliage'].values()),'Foliage value mismatch'
assert values['bark_display']['within_03_warm'],'Bark brightness/hue mismatch'
assert values['engine_comparison']['within_05'],'Eevee mismatch'
assert .95<=values['raking_camera_surface_distance_m']<=1.05,'Raking view must be 1 m from the delivered bark surface'
contact([r/(n+'.png') for n in NAMES]+[eevee/'hero.png'],r/'contact.jpg',title='Pin oak / exported GLB and embedded 2048 maps / Cycles and Eevee')
contact([r/(n+'.png') for n in ['front','side','back','top']],r/'turnaround.jpg',title='Pin oak / exported GLB turnaround')
contact([r/(n+'.png') for n in ['branchlet','cluster_3m','bark','bark_raking','lower_pins','crown_up','root_flare','scale','family']]+[eevee/'hero.png'],r/'details.jpg',title='Pin oak / exported leaves, bark, pins, backlight, scale and family')
review_sheet([[r/'hero.png',r/'family.png'],[r/'turnaround.jpg'],[r/'details.jpg'],[r/'oak_match_osu-pair.jpg'],[r/'oak_match_stony-pair.jpg'],[r/'bark-pair.jpg']],r/'review-sheet.jpg',title='Pin oak / final GLB review / photographs stay local')
report=dict(passed=True,glb_sha256=sha,cycles_shots=len(NAMES),eevee_shots=1,maple_glb_sha256=meta['family']['maple_source_sha256'])
(r/'render-check.json').write_text(json.dumps(report,indent=2))
if a.docs:
    docs=ROOT/'trees/docs';docs.mkdir(exist_ok=True)
    for name,target in [('hero.png','oak-hero.jpg'),('details.jpg','oak-details.jpg')]:
        im=Image.open(r/name).convert('RGB');im.thumbnail((1600,1600))
        for quality in (91,87,82,76,69,62,55):
            im.save(docs/target,quality=quality,optimize=True)
            if (docs/target).stat().st_size<=200000:break
        assert (docs/target).stat().st_size<=200000
print(json.dumps(report,indent=2))
