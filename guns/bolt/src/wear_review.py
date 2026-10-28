"""Keep the hero's native pixels when comparing visible cheek/grip paint wear."""
import sys,json,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit.photo_match import project
from value_review import stats
from final_review import panel
out=BASE/'renders/final/pairs';out.mkdir(parents=True,exist_ok=True)
hero=Image.open(BASE/'renders/final/beauty/hero.png').convert('RGBA')
meta=json.loads((BASE/'renders/final/beauty/shots.json').read_text())['hero']
loc=np.array(meta['location']);d=np.array(meta['target'])-loc
params=[math.atan2(d[1],d[0]),math.atan2(d[2],np.linalg.norm(d[:2])),*loc,math.log(meta['lens']),meta.get('roll',0)]
# Project two grip stations for a local pixel/mm scale; never enlarge our crop.
p=project(params,np.array([(.018,-.02,-.02),(.018,-.02,.02)]),hero.width,hero.height)[0]
scale=np.linalg.norm(p[1]-p[0])/.04
picks=np.array([(x,y,z) for x in (-.023,.023) for y in (-.280,.030) for z in (-.050,.081)])
coords=project(params,picks,hero.width,hero.height)[0];lo=np.floor(coords.min(0)-10).astype(int);hi=np.ceil(coords.max(0)+10).astype(int)
our=hero.crop((*lo,*hi));reference=Image.open(BASE/'build/white-balanced/open.png').convert('RGB').crop((1810,1050,2650,1340))
# The reference spans approximately 240 mm in this perspective, estimated
# from its 35 mm receiver diameter; report that uncertainty explicitly.
reference_width=round(.240*scale);reference=reference.resize((reference_width,round(reference.height*reference_width/reference.width)),Image.Resampling.LANCZOS)
# A second native row compares cap-edge scale. The reference cap is field
# painted, so this is an apparent edge-width comparison, not identical coating.
cap_points=np.array([(x,y,z) for x in (-.016,.016) for y in (.046,.078) for z in (.129,.152)])
cap_pixels=project(params,cap_points,hero.width,hero.height)[0]
cap_lo=np.floor(cap_pixels.min(0)-4).astype(int);cap_hi=np.ceil(cap_pixels.max(0)+4).astype(int)
our_cap=hero.crop((*cap_lo,*cap_hi))
ref_cap=Image.open(BASE/'build/white-balanced/open.png').convert('RGB').crop((1260,220,1620,430))
cap_width=round(.032*scale);ref_cap=ref_cap.resize((cap_width,round(ref_cap.height*cap_width/ref_cap.width)),Image.Resampling.LANCZOS)
row2=max(our.height,reference.height)+105
canvas=Image.new('RGB',(max(our.width,reference.width)*2+100,row2+max(our_cap.height,ref_cap.height)+75),(225,226,222))
left=Image.new('RGBA',our.size,(59,62,66,255));left.alpha_composite(our);canvas.paste(left.convert('RGB'),(25,55));canvas.paste(reference,(canvas.width//2+20,55))
ImageDraw.Draw(canvas).text((20,15),'Native hero pixels / comb and palm rub',fill=(20,30,25));ImageDraw.Draw(canvas).text((canvas.width//2+20,15),'Used stock / estimated same mm scale',fill=(20,30,25))
cap_panel=Image.new('RGBA',our_cap.size,(59,62,66,255));cap_panel.alpha_composite(our_cap)
canvas.paste(cap_panel.convert('RGB'),(25,row2+35));canvas.paste(ref_cap,(canvas.width//2+20,row2+35))
ImageDraw.Draw(canvas).text((20,row2),'Native hero cap / silver edge',fill=(20,30,25))
ImageDraw.Draw(canvas).text((canvas.width//2+20,row2),'Used painted cap / edge scale only',fill=(20,30,25))
canvas.save(out/'hero-wear-pair.jpg',quality=94,optimize=True)
result=dict(hero_pixels_per_meter=float(scale),render_crop=lo.tolist()+hi.tolist(),reference_crop_native=[1810,1050,2650,1340],reference_span_estimate_m=.240,reference_scale_status='receiver-diameter visual estimate, perspective uncertainty; not calibrated metrology',hero_not_resampled=True,scope_cap_crop=cap_lo.tolist()+cap_hi.tolist(),scope_reference_crop=[1260,220,1620,430],scope_reference_width_estimate_m=.032,scope_coating_difference='Photo cap is field painted; apparent edge scale only, not identical anodizing',glb_sha256=meta['sha256'],scope='Native hero stock region versus used forend paint; different stock contours/coats, mm scale estimated from receiver diameter')
(out/'hero-wear-values.json').write_text(json.dumps(result,indent=2))
