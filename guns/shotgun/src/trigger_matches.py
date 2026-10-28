"""Trigger comparison framing only; view angles and blade scale are estimates."""
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
MATCHES={
 'trigger_right_photo':dict(title='Trigger / right side / muzzle right',
  photo=str(BASE/'refs/stock-sharp.jpg'),crop=(0,0,5228,996),trigger_crop=(1720,310,2110,510),
  matched_view=dict(target=(0,.086,-.0145),direction=(1,.08,.16),roll=-.04,
   anchor_pixel=(1872,401),span_pixels=98,span_m=.0203)),
 'trigger_quarter_photo':dict(title='Trigger / right rear three-quarter / muzzle right',
  photo=str(BASE/'refs/trigger-oblique.png'),crop=(0,0,2379,1784),trigger_crop=(1060,600,1360,800),
  matched_view=dict(target=(0,.086,-.0145),direction=(1,-.45,.9),roll=.05,
   anchor_pixel=(1170,678),span_pixels=48,span_m=.0203))}
