"""Measured landmark camera calibration, not mesh tracing or texture projection.

Reference image pixel positions were inspected on a 100 px grid. World anchors
come from the published envelope and our declared construction dimensions. Small
remaining residuals quantify the photographic/geometry uncertainty.
"""
from pathlib import Path
import math
ROOT=Path(__file__).resolve().parents[1]
SHIFT=-.0555

def point(x,y,z):return (x+SHIFT,y,z)
def anchor(world,pixel,weight=1):return dict(world=world,pixel=pixel,weight=weight)

MATCHES={
 'match_closed':dict(title='Closed grill / front three-quarter',photo=str(ROOT/'refs/grill-three-quarter.jpeg'),
    crop=(0,0,1200,1200),location=(-1.5,-3,1.7),target=point(0,0,.60),lens=80,
    hide_assemblies=['HoseRig'],hide=['HoseAssembly','LP flexible','Foot ring','Type 1','Coupling','Regulator','Hose','Tank scale','Scale ','Tank collar'],
    landmarks=[anchor(point(-.205,-.310,.795),(610,421)),anchor(point(0,-.310,.795),(768,407)),
       anchor(point(.205,-.310,.795),(927,395)),anchor(point(-.296,-.222,0),(478,1124)),
       anchor(point(-.296,.222,0),(312,993)),anchor(point(.357,-.253,.09),(995,958)),
       anchor(point(.357,.253,.09),(749,845)),anchor(point(-.660,-.229,.865),(177,367),.5)]),
 'match_interior':dict(title='Open lid / cooking construction',photo=str(ROOT/'refs/open-photo.png'),
    crop=(150,0,1050,675),location=(0,-.80,1.63),target=point(0,.04,.88),lens=28,lid=-104,
    landmarks=[anchor(point(-.304,-.207,.887),(154,568)),anchor(point(.304,-.207,.887),(1048,603)),
       anchor(point(-.304,.239,.887),(350,218)),anchor(point(.304,.239,.887),(884,225)),
       anchor(point(-.2785,.094,.974),(282,196),.7),anchor(point(.2785,.094,.974),(953,202),.7),
       anchor(point(-.2785,.215,.974),(332,131),.7),anchor(point(.2785,.215,.974),(917,134),.7)]),
}
