"""Ignored round-three contact, measured comparisons and display-value checks."""
import argparse,sys,json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.contact import contact,review_sheet
from kit.fonts import find_font
from crown_measure import projected_image
from reference_measurements import MEASUREMENTS,values
from color_values import comparisons
p=argparse.ArgumentParser();p.add_argument('--renders',type=Path,required=True);p.add_argument('--final',action='store_true');a=p.parse_args()
names=['hero','front','side','back','top','bark','bark_2m','branchlet','crown_up','scale','root_flare','unions','unions_reverse','unions_upper','unions_upper_reverse','dripline','silhouette','structure','daylight'] if a.final else ['daylight','crown_up','silhouette','scale','structure','unions','unions_reverse','unions_upper','unions_upper_reverse','dripline','root_flare']
paths=[a.renders/(n+'.png') for n in names]
if a.final:paths.append(a.renders.parent/'final-eevee/hero.png')
else:
    paths=[p for p in paths if p.exists()]
    paths += [p for p in sorted(a.renders.glob('*.png')) if not p.stem.startswith('match_') and p not in paths]
contact(paths,a.renders/'contact.jpg',title='Red maple / exported GLB and baked textures' if a.final else 'Red maple / source look development')
refs=json.loads((ROOT/'trees/build/reference-measurements.json').read_text());stats={}
font=ImageFont.truetype(find_font('Noto Sans','Regular'),22)
for name in ['psu','osu']:
    row=projected_image(a.renders/('match_'+name+'.png'))
    if not .08<row['base_fraction_of_tree']<.35:raise ValueError('Crown image mask includes bole or misses foliage: '+name)
    row['reference']=refs[name];stats[name]=row
    # Leave original kit composites intact. Put measured image ratios alongside
    # the actual render and photograph in separate, clearly labeled review pairs.
    original=Image.open(a.renders/('match_'+name+'-pair.jpg')).convert('RGB')
    canvas=Image.new('RGB',(original.width,original.height+105),(238,239,236));canvas.paste(original,(0,105));d=ImageDraw.Draw(canvas)
    half=canvas.width//2
    d.text((18,15),f"MODEL projected crown W/H {row['width_height']:.3f}; base {100*row['base_fraction_of_tree']:.1f}% of tree",font=font,fill=(22,38,29))
    v=values(MEASUREMENTS[name])
    d.text((half+18,15),f"PHOTO crown W/H {v['crown_width_height']:.3f}; base {100*v['base_fraction_of_tree']:.1f}% of tree",font=font,fill=(22,38,29))
    d.text((18,52),f"Widest at {100*row['widest_height_fraction_of_crown']:.1f}% above crown base / {row['widest_height_at_12_4m']:.2f} m on 12.4 m scale",font=font,fill=(22,38,29))
    d.text((half+18,52),f"Widest at {100*v['widest_height_fraction_of_crown']:.1f}% above base / {v['widest_height_at_12_4m']:.2f} m IF 12.4 m tall",font=font,fill=(22,38,29))
    canvas.save(a.renders/('match_'+name+'-measured-pair.jpg'),quality=94,optimize=True)
(a.renders/'tonal-check.json').write_text(json.dumps(stats,indent=2))
(a.renders/'color-value-populations.json').write_text(json.dumps(comparisons(a.renders),indent=2))
review_sheet([[a.renders/'contact.jpg'],[a.renders/'match_psu-measured-pair.jpg'],[a.renders/'match_osu-measured-pair.jpg'],
              [ROOT/'trees/renders/round3-measurements/psu-measurements.jpg',ROOT/'trees/renders/round3-measurements/osu-measurements.jpg']],
              a.renders/'review-sheet.jpg',title='Final GLB / summer photo pairs and measured crown proportions' if a.final else 'Source / summer photo pairs and measured crown proportions')
(a.renders/'REFERENCE-CREDIT.txt').write_text('Reference photos: Jodi Sulpizio / Penn State Extension; Oregon State University Landscape Plants (site by Patrick Breen; individual photographer unspecified). Copyright retained. Local study only; no redistribution. URLs in refs/SOURCES.md. Original mathematical asset geometry and texels; photographs are only compared/measured.\n')
print(json.dumps(stats,indent=2))

if a.final:
    current_sha=hashlib.sha256((ROOT/'trees/export/RedMaple.glb').read_bytes()).hexdigest()
    metadata=json.loads((a.renders/'shots.json').read_text())
    eevee=json.loads((a.renders.parent/'final-eevee/shots.json').read_text())
    for name,row in list(metadata.items())+list(eevee.items()):
        if row['source_sha256']!=current_sha or not row['stage'].startswith('EXPORTED GLB'):
            raise RuntimeError('Final render is stale or not from GLB: '+name)
    (a.renders/'render-check.json').write_text(json.dumps(dict(passed=True,glb_sha256=current_sha,cycles_shots=len(metadata),eevee_shots=len(eevee)),indent=2))
    docs=ROOT/'trees/docs';docs.mkdir(exist_ok=True)
    def jpg(source,target):
        im=Image.open(source).convert('RGB');im.thumbnail((1600,1600))
        for quality in (91,87,82,76,69,62,55):
            im.save(docs/target,quality=quality,optimize=True)
            if (docs/target).stat().st_size<=200000:break
        if (docs/target).stat().st_size>200000:raise RuntimeError('Docs image exceeds budget')
    jpg(a.renders/'hero.png','hero.jpg')
    contact([a.renders/(n+'.png') for n in ['front','side','back','top']],a.renders/'turnaround.jpg',title='Red maple / exported GLB turnaround')
    contact([a.renders/(n+'.png') for n in ['bark','bark_2m','branchlet','root_flare','scale']]+[a.renders.parent/'final-eevee/hero.png'],a.renders/'details.jpg',title='Red maple / baked GLB details, scale and Eevee')
    jpg(a.renders/'turnaround.jpg','turnaround.jpg');jpg(a.renders/'details.jpg','details.jpg')
