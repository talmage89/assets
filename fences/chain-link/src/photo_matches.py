"""Hand-measured diamond intersections for a material/mesh comparison only.

Reference is an unsurveyed commercial fence close-up; its hidden height,
terminal spacing and twisted selvage are not applied to the 4 ft asset.
"""
from pathlib import Path
PHOTO=Path(__file__).resolve().parents[2]/'refs/chainlink01.jpg'
MATCHES={'match_mesh':dict(title='Galvanized woven mesh / 2 in nominal diamonds',photo=str(PHOTO),crop=(130,70,470,310),location=(-1.32,-.48,1.00),target=(-1.30,-.034,.83),lens=52,exposure=-.9,
 hide_assemblies=['Chain_EndSection','Chain_BetweenTerminals','Chain_Terminal_End','Chain_Section','Chain_Line','Chain_Terminal','Chain_Corner','Chain_GateBay'],
 landmarks=[dict(world=(x,-.034,z),pixel=pixel) for x,z,pixel in [
 (-1.3716,.889,(200,94)),(-1.2954,.889,(301,88)),(-1.2192,.889,(402,83)),
 (-1.3335,.8509,(250,142)),(-1.2573,.8509,(350,135)),
 (-1.3716,.8128,(201,191)),(-1.2954,.8128,(301,184)),(-1.2192,.8128,(401,178)),
 (-1.3335,.7747,(251,238)),(-1.2573,.7747,(350,232))]])}
