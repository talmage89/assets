"""Profile camera estimate; six near-wheel anchors, no body-outline fitting.

No EXIF survives in the stock photograph. A fronto-parallel wheel plane cannot
uniquely recover focal length. The 80 mm prior and 1.25 m camera-height prior
are explicit estimates, not measured camera metadata. Review also keeps the
orthographic overlay and reports 60/100 mm sensitivity.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
F=-1.475;R=F+2.82448;H=.33035
MATCHES={'side_matched':dict(title='S240 / estimated Camry profile camera',
 photo=str(ROOT/'refs/sedan-camry-side.jpg'),crop=(0,0,2100,1575),
 location=(12,0,1.25),target=(0,0,.7),lens=80,camera_height_m=(1.25,.10),
 landmarks=[dict(world=w,pixel=[v*1.75 for v in p]) for w,p in [
  ((.895,F,H),(238,541)),((.900,R,H),(924,540)),
  ((.88,F,0),(238,621)),((.885,R,0),(924,620)),
  ((.895,F,2*H),(238,459)),((.900,R,2*H),(924,458))]])}
for name,lens in [('side_matched_wide',60),('side_matched_long',100)]:
    MATCHES[name]=dict(MATCHES['side_matched'],lens=lens,title=f'S240 / profile camera sensitivity, {lens} mm prior')
