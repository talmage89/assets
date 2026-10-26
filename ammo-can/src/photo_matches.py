"""Observed manufacturing-photo landmarks; camera residuals are disclosed."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def a(p,pixel):return dict(world=p,pixel=pixel)
MATCHES={'match_closed':dict(title='M2A1-style ammo can / folded cover and cam closure',photo=str(ROOT/'refs/closed.jpg'),crop=(0,0,640,480),location=(.8,-.4,.30),target=(0,0,.095),lens=85,landmarks=[a((.07055,-.1416,0),(172,382)),a((.07055,.1416,0),(505,341)),a((-.07055,-.1416,0),(129,345)),a((-.0774,-.1472,.1855),(108,105)),a((.0774,-.1472,.1855),(170,119)),a((.0774,.1472,.1855),(530,113))]),
'match_latch':dict(title='M2A1-style ammo can / cam, hasp and pull bail',photo=str(ROOT/'refs/open.jpg'),crop=(150,60,460,420),location=(0,-.9,.14),target=(0,-.14,.095),lens=85,landmarks=[a((-.0774,-.1472,.1855),(205,111)),a((.0774,-.1472,.1855),(434,111)),a((-.07055,-.1416,0),(216,379)),a((.07055,-.1416,0),(424,379)),a((0,-.152,.094),(321,245)),a((0,-.1503,.018),(320,350))])}
