"""Measured landmarks in the CC0 installed rear photo; original pixels only.

Older casting differs in ribs and foundry layout. Camera-fit residuals measure
that uncertainty; they are not hidden by silhouette tracing or mesh adaptation.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=3508/957

def mark(name,world,pixel,weight=1):
    return dict(name=name,world=world,pixel=[p*S for p in pixel],weight=weight)

MATCHES={'installed_rear':dict(
    photo=str(ROOT/'refs/weathered.jpg'),crop=(0,0,3508,4765),
    title='Installed rear / casting, bonnet and ground flange',
    location=(.09,1.7,1.50),target=(0,0,.41),lens=50,
    landmarks=[
        mark('Operating nut crown',(0,0,.8128),(475,130),2),
        mark('Operating nut base',(0,0,.784),(473,189)),
        mark('Bonnet left silhouette',(.145,0,.648),(259,425)),
        mark('Bonnet right silhouette',(-.145,0,.648),(691,442)),
        mark('Bonnet near rim',(0,.145,.648),(476,510)),
        mark('Hose left nut',(.207772,0,.4572),(184,600),2),
        mark('Hose right nut',(-.207772,0,.4572),(776,631),2),
        mark('Traffic flange left',(.171,0,.066),(270,1087)),
        mark('Traffic flange right',(-.171,0,.066),(690,1113)),
        mark('Traffic flange near',(0,.171,.066),(474,1189)),
    ]
)}
