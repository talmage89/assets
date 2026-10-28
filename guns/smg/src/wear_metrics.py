"""Historical 1-D ribbon diagnostics; photographs are measurement-only.

Current receiver morphology is judged by wear_2d_review.py, not these runs.

Run lengths use 0.5-mm longitudinal bins. A column counts as worn when at
least 25% of its ribbon area is exposed. Fill isolated half-mm holes, then
discard isolated half-mm specks; do not smooth the actual image or texture.
"""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw

BASE = Path(__file__).resolve().parents[1]
BIN_MM = .5

def runs(mask):
    cuts = np.r_[0, np.flatnonzero(np.diff(mask)) + 1, len(mask)]
    return [(bool(mask[a]), int(a), int(b)) for a,b in zip(cuts[:-1],cuts[1:])]

def profile_metrics(worn, bright, valid, bin_mm=BIN_MM):
    counts = valid.sum(0)
    occupancy = (worn & valid).sum(0) / np.maximum(counts, 1)
    profile = occupancy >= .25
    for state in (False, True):
        for value,a,b in runs(profile.copy()):
            if value == state and b-a == 1 and a > 0 and b < len(profile):
                profile[a:b] = not state
    rr = runs(profile)
    def lengths(state):
        # Boundary-clipped runs do not supply a complete chip/gap length.
        values = [(b-a)*bin_mm for value,a,b in rr if value == state and a>0 and b<len(profile)]
        if not values:
            return dict(count=0,median_mm=None,p25_p75_mm=[None,None],lengths_mm=[])
        return dict(count=len(values), median_mm=float(np.median(values)),
                    p25_p75_mm=np.percentile(values,[25,75]).tolist(), lengths_mm=values)
    area = int((worn & valid).sum())
    return dict(length_worn_fraction=float(profile.mean()),
                chip=lengths(True), gap=lengths(False),
                worn_area_fraction=float(area / valid.sum()),
                gray_share_of_worn=float(((worn & ~bright) & valid).sum()/max(area,1)),
                bright_share_of_worn=float((bright & worn & valid).sum()/max(area,1)),
                longitudinal_bins=len(profile), bin_mm=bin_mm,
                missing_columns=int((counts==0).sum()),
                profile=profile.astype(int).tolist())

def reference():
    im = Image.open(BASE/'build/white-balanced/navy2.png').convert('RGB')
    # The broad pressed flank directly below the crest; skip its thin glint.
    # 1090-pixel receiver envelope corresponds approximately to 230 mm.
    box = (1900,294,2600,316)
    ppm = 1090/230
    native = np.asarray(im.crop(box)).astype(float)
    lum = native @ np.array((.2126,.7152,.0722))
    width = round(native.shape[1]/ppm/BIN_MM)
    # Area occupancy per longitudinal bin, with native pixels classified first.
    def columns(mask):
        return np.array([mask[:,round(i*native.shape[1]/width):round((i+1)*native.shape[1]/width)].mean()
                         for i in range(width)])
    # 100 sub-samples reproduce fractional column areas without interpolation.
    worn = np.arange(100)[:,None] < columns(lum>65)[None,:]*100
    bright = np.arange(100)[:,None] < columns(lum>=180)[None,:]*100
    row = profile_metrics(worn, bright, np.ones_like(worn,bool))
    # Native-pixel area fractions are the authoritative gray/bright statistics.
    row['gray_share_of_worn'] = float(((lum>65)&(lum<180)).sum()/(lum>65).sum())
    row['bright_share_of_worn'] = float((lum>=180).sum()/(lum>65).sum())
    row['worn_area_fraction'] = float((lum>65).mean())
    row.update(photo='navy2.jpg', white_balance_neutral='upper gun white selector legend',
               rectangle_native=list(box), pixels_per_mm=ppm,
               measured_span_mm=(box[2]-box[0])/ppm,
               ribbon_depth_mm=(box[3]-box[1])/ppm,
               gray_luma_range_255=[65,180], bright_luma_min_255=180,
               uncertainty='Approximate 230-mm receiver envelope, perspective and reflections; length resolution about 0.5 mm. Gray/bright are observed tonal bins, not recovered chemistry.')
    sensitivities=[]
    for threshold in (60,70):
        mask = np.arange(100)[:,None] < columns(lum>threshold)[None,:]*100
        r=profile_metrics(mask,bright,np.ones_like(mask,bool))
        sensitivities.append(dict(luma_threshold=threshold,length_worn_fraction=r['length_worn_fraction'],
                                  chip_median_mm=r['chip']['median_mm'],gap_median_mm=r['gap']['median_mm']))
    row['threshold_sensitivity']=sensitivities
    out=BASE/'build/finish-round2';out.mkdir(parents=True,exist_ok=True)
    overlay=im.crop((1800,260,2680,370));d=ImageDraw.Draw(overlay)
    d.rectangle((box[0]-1800,box[1]-260,box[2]-1800,box[3]-260),outline='orange',width=1)
    overlay.save(out/'reference-ribbon.jpg',quality=96)
    classified=np.zeros_like(native,dtype=np.uint8);classified[lum<=65]=(12,16,17)
    classified[(lum>65)&(lum<180)]=(115,120,114);classified[lum>=180]=(245,245,235)
    Image.fromarray(classified).save(out/'reference-classification.png')
    (out/'reference-wear.json').write_text(json.dumps(row,indent=2))
    return row

if __name__=='__main__':
    print(json.dumps(reference(),indent=2))
