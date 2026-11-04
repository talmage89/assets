"""Four real builder comparisons, native pixels and visible structure anchors.

Original proof houses, not replicas. Clear bedroom/upper-story surfaces
calibrate each camera; held-out features separately expose plan differences.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from plan import generate
PAIR_SEEDS={'side_pa':53,'side_oh':51,'foyer_pa':55,'foyer_oh':55}

def point(world,pixel,label):return dict(world=world,pixel=pixel,label=label)

def front_corners(b,bottom,top,pixels):
    return [point((x,b.y0,z),p,label) for x,z,p,label in (
      (b.x0,bottom,pixels[0],'left material break'),(b.x1,bottom,pixels[1],'right material break'),
      (b.x0,top,pixels[2],'left soffit/wall junction'),(b.x1,top,pixels[3],'right soffit/wall junction'))]

p=generate(53,house_type='split');m,w=p['blocks'][:2]
q=generate(51,house_type='split');a,b=q['blocks'][:2]
r=generate(55,house_type='split');f=r['blocks'][0]
MATCHES={
 'side_pa':dict(title='Common builder side-split / Pennsylvania / seed 53',photo='refs/split-pair-side_pa.jpg',crop=(120,150,850,480),
   location=(w.cx-2,w.y0-26,1.7),target=(w.cx,w.y0,2.8),lens=55,lens_bounds_mm=(28,160),camera_height_m=(1.7,.8),background='transparent',
   landmarks=front_corners(w,p['levels']['upper']-.254,w.plate,[(445,353),(782,351),(445,250),(781,246)])+
      [point((w.x0,w.cy,w.height(w.x0,w.cy)),(455,211),'left ridge end'),point((w.x1,w.cy,w.height(w.x1,w.cy)),(782,208),'right ridge end')],
   held_out=[point((m.x0,m.y0,m.plate),(208,280),'living left bearing'),point((p['door_x'],m.y0,p['levels']['living']),(403,377),'living threshold')]),
 'side_oh':dict(title='Common builder side-split / Ohio / seed 51',photo='refs/split-pair-side_oh.jpg',crop=(0,35,665,330),
   location=(b.cx+7,b.y0-29,1.8),target=(b.cx,b.y0,3.2),lens=52,lens_bounds_mm=(28,160),camera_height_m=(1.8,1.0),background='transparent',
   landmarks=front_corners(b,q['levels']['upper']-.254,b.plate,[(208,218),(432,222),(211,146),(431,151)])+
      [point((b.cx,b.y0,b.height(b.cx,b.y0)),(312,83),'front gable ridge'),point((b.x1,b.y0+2.8,b.plate),(469,181),'receding bedroom eave')],
   held_out=[point((q['door_x'],a.y0,q['levels']['living']),(180,251),'living threshold'),point((a.x0+a.width*.34,a.y0,q['levels']['living']+.66),(100,239),'living picture sill')]),
 'foyer_pa':dict(title='True split-foyer / Pennsylvania / seed 55',photo='refs/split-pair-foyer_pa.jpg',crop=(30,20,630,325),
   location=(f.cx-3,f.y0-28,1.7),target=(f.cx,f.y0,2.3),lens=50,lens_bounds_mm=(28,160),camera_height_m=(1.7,1),background='transparent',
   landmarks=[point((f.x0,f.y0,r['levels']['upper']-.254),(61,209),'left material break'),
      point((f.x1,f.y0,r['levels']['upper']-.254),(605,207),'right material break'),
      point((f.x1,f.y0,f.plate),(601,103),'right frieze/bearing corner'),
      point((r['door_x']-.4572,f.y0,r['levels']['living']),(307,252),'entry left sill'),
      point((r['door_x']+.4572,f.y0,r['levels']['living']),(340,252),'entry right sill'),
      point((r['door_x']-.4572,f.y0,r['levels']['living']+2.032),(307,171),'entry left head'),
      point((r['door_x']+.4572,f.y0,r['levels']['living']+2.032),(340,169),'entry right head')],
   held_out=[point((f.x0+f.width*.19,f.y0,0.),(170,261),'left lower full-sash sill'),
      point((f.x0+f.width*.73,f.y0,0.),(469,262),'right lower full-sash sill')]),
 'foyer_oh':dict(title='Split-entry raised ranch / Ohio / seed 55',photo='refs/split-pair-foyer_oh.jpg',crop=(140,110,840,425),
   location=(f.cx-5,f.y0-30,1.7),target=(f.cx,f.y0,2.2),lens=50,lens_bounds_mm=(28,160),camera_height_m=(1.7,1.2),background='transparent',
   landmarks=front_corners(f,r['levels']['upper']-.254,f.plate,[(200,281),(786,283),(200,159),(785,159)])+
      [point((r['door_x'],f.y0,r['levels']['living']),(486,338),'entry threshold'),point((r['door_x'],f.y0,r['levels']['living']+2.032),(485,235),'entry head')],
   held_out=[point((f.x0+f.width*.19,f.y0,0.),(351,345),'lower full-sash sill')]),
}

# Fit only corresponding structure. Entry locations and differing roof forms
# are diagnostic hold-outs, not weights that can distort the camera.
for name,match in MATCHES.items():
    count=5 if name=='side_oh' else 6 if name=='foyer_oh' else 7 if name=='foyer_pa' else 4
    match['held_out']=match['landmarks'][count:]+match.get('held_out',[])
    match['landmarks']=match['landmarks'][:count]
