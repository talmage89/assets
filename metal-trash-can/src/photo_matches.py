"""Manually observed landmarks; photos never enter the material pipeline."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def a(world,pixel):return dict(world=world,pixel=pixel)
MATCHES={'match_front':dict(title='Galvanized garbage can / pressed lid and corrugation',photo=str(ROOT/'refs/can-front.jpg'),crop=(0,0,600,600),location=(0,-2.5,1.05),target=(0,0,.38),lens=80,landmarks=[
 a((-.2667,0,.680),(104,109)),a((.2667,0,.680),(499,109)),
 a((-.2286,0,.008),(154,533)),a((.2286,0,.008),(445,533)),
 a((0,-.2286,0),(300,569)),a((0,.214,.718),(300,35)),a((0,-.260,.706),(300,130))])}
