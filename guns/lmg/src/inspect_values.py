"""Fast whole-part preview audit using the accepted projected import masks.

Preview numbers guide iteration only. Final acceptance re-captures the actual
new GLB and verifies its hash in look_review.py.
"""
import argparse,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from look_review import REGIONS,metrics,polygon_mask,chart
from image_masks import raster
p=argparse.ArgumentParser();p.add_argument('folder');p.add_argument('--geometry',default='build/image-geometry');a=p.parse_args()
folder=BASE/a.folder;meta=json.loads((folder/'shots.json').read_text());cache={};rows={}
for role,(photo,polys,shot,prefixes) in REGIONS.items():
 if shot not in meta:continue
 im=np.asarray(Image.open(folder/(shot+'.png')).convert('RGB'));h,w=im.shape[:2]
 gpath=BASE/a.geometry/(shot+'.npz')
 if not gpath.exists():gpath=BASE/a.geometry/({'handguard_finish_photo':'used_right_photo','paint_receiver_photo':'used_photo','stock_finish_photo':'right_photo','box_finish_photo':'box_detail_photo'}[shot]+'.npz')
 geo=np.load(gpath)
 if shot not in cache:cache[shot]=raster(geo,meta[shot],w,h)
 ids,_=cache[shot];m=np.isin(ids,[i+1 for i,n in enumerate(geo['names']) if str(n).startswith(prefixes)])
 if role in ('brass','copper_green_tip'):m &=np.isin(ids,[i+1 for i,n in enumerate(geo['names']) if str(n).endswith('_Case' if role=='brass' else '_Jacket')])
 m=np.asarray(Image.fromarray(np.uint8(m)*255).filter(ImageFilter.MinFilter(3)))>0
 ref=np.asarray(Image.open(BASE/'build/white-balanced'/(photo+'.jpg')).convert('RGB'));pm=polygon_mask((ref.shape[1],ref.shape[0]),polys);pm=np.asarray(Image.fromarray(np.uint8(pm)*255).filter(ImageFilter.MinFilter(3)))>0
 r=metrics(im[m]);t=metrics(ref[pm]);row=dict(render=r,photo=t,neutral=json.loads((BASE/'build/white-balanced/corrections.json').read_text())[photo])
 rows[role]=row;chart(role+' / SOURCE PREVIEW',im,m,ref,pm,row,folder/(role+'-histograms.jpg'))
 print(role,'V',np.round(r['value_p10_p50_p90']), '/',np.round(t['value_p10_p50_p90']),'H',np.round(r['brightest_decile_rgb']), '/',np.round(t['brightest_decile_rgb']),flush=True)
(folder/'preview-values.json').write_text(json.dumps(rows,indent=2))
