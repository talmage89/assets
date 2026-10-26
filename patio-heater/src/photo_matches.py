"""Inspected photo landmarks fit review cameras only; never meshes or textures."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def a(w,p):return dict(world=w,pixel=p)
MATCHES={'match_whole':dict(title='Mushroom heater / proportions and construction',photo=str(R/'refs/pro-full.jpeg'),crop=(285,20,720,990),location=(0,-7,2.0),target=(0,0,1.13),lens=70,background='transparent',emission_scale=0,
landmarks=[a((-.4191,0,2.172),(331,96)),a((.4191,0,2.172),(666,96)),a((-.155,0,2.239),(438,63)),a((.155,0,2.239),(563,63)),a((-.2286,0,.010),(410,957)),a((.2286,0,.010),(591,957)),a((-.0381,0,.833),(485,617)),a((.0381,0,.833),(516,617)),a((-.139,0,1.884),(445,181)),a((.139,0,1.884),(554,181))])}

# A used restaurant heater, photographed in service; not a catalog/studio image.
# Landmarks refer to the foreground heater only. Its stainless lift-cover differs
# from our painted door design. Fit the unchanged envelope; do not trace damage.
MATCHES['match_used']=dict(title='Patio seasons / used-heater wear',
 photo=str(R/'refs/used-terrace.jpg'),crop=(800,500,2200,3456),
 location=(0,-1.7,1.5),target=(0,0,1.13),lens=52,
 background='transparent',emission_scale=0,
 landmarks=[a((-.4191,0,2.172),(842,761)),a((.4191,0,2.172),(2066,764)),
  a((0,-.4191,2.172),(1458,618)),a((0,.4191,2.172),(1448,944)),
  a((-.2286,0,.010),(1110,3340)),a((.2286,0,.010),(1600,3374)),
  a((0,-.2286,.010),(1360,3414)),
  a((0,0,.833),(1396,2420)),a((0,0,1.637),(1442,1308))])


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--credit-dir',required=True)
    folder=Path(p.parse_args().credit_dir);folder.mkdir(parents=True,exist_ok=True)
    (folder/'REFERENCE-CREDIT.txt').write_text(
        "Used-heater comparison / photographic right panel\n"
        "Terrassenstrahler.jpg, 3268zauber, 12 February 2009.\n"
        "https://commons.wikimedia.org/wiki/File:Terrassenstrahler.jpg\n"
        "CC BY-SA 3.0: https://creativecommons.org/licenses/by-sa/3.0/\n"
        "Changes: crop, resize, and comparison layout/captions only.\n"
        "The comparison composite is available under CC BY-SA 3.0.\n"
        "The original 3D asset and its textures contain no photographic pixels.\n")
