"""Comparison-only matched blade views; manual angle and scale estimates."""
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
MATCHES={
 'trigger_right':dict(title='Muzzle-facing concavity / service trigger',
  photo=str(BASE/'build/references/side-atf.png'),crop=(0,0,1200,600),
  trigger_crop=(480,265,610,375),matched_view=dict(direction=(1,0,.02),
   target=(0,.036,.010),span_m=.023,span_pixels=70,anchor_pixel=(532,313))),
 'trigger_quarter':dict(title='Broad blade / open-cylinder photograph',
  photo=str(BASE/'build/references/open.png'),crop=(0,0,4032,3024),
  trigger_crop=(1700,1120,2230,1580),matched_view=dict(direction=(-1,-.22,.23),
   target=(0,.036,.010),span_m=.023,span_pixels=240,anchor_pixel=(1912,1365))),
}
