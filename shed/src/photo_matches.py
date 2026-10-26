"""Facade landmarks; reference footprint estimated as the same eight-foot class.

The used shed has a wider doorway and horizontal gable siding. Fit the wall
outline, not those different design details. Lens and residual are estimates.
"""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
MATCHES={'match_used':dict(title='Used shed / lower trim, roof and threshold weathering',photo=str(R/'refs/condition-11.jpg'),crop=(0,250,1368,1740),location=(.15,-4.8,1.2),target=(0,0,1.5),lens=35,background='transparent',exposure=0,landmarks=[
 dict(world=(-1.22,-1.55,.248),pixel=(150,1650)),dict(world=(1.22,-1.55,.248),pixel=(1212,1514)),
 dict(world=(-1.22,-1.55,2.381),pixel=(166,610)),dict(world=(1.22,-1.55,2.381),pixel=(1243,711)),
 dict(world=(0,-1.65,3.01),pixel=(816,335)),
])}
