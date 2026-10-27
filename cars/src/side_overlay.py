"""Wheelbase-calibrated true-profile comparison. No geometry is traced.

Only two axle pixels determine a similarity transform. Body silhouettes are
never used to fit the transform; the photograph remains a comparison artifact.
"""
import argparse,json,math,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[1]
FONT='/usr/share/fonts/noto/NotoSans-Regular.ttf'
# Inspected on the 1500 px preview, converted to the original 2100 px frame.
FRONT=(246*1.4,720*1.4);REAR=(1164*1.4,722*1.4)
RAKE=[(367*1.4,478*1.4),(529*1.4,367*1.4)]
WB=3.683;HUB=.39535

def main():
 p=argparse.ArgumentParser();p.add_argument('--renders',required=True);a=p.parse_args();out=Path(a.renders)
 data=json.loads((out/'shots.json').read_text())['side'];photo=ImageOps.exif_transpose(Image.open(ROOT/'refs/stock-side.jpg')).convert('RGBA')
 source=Image.open(out/'side.png').convert('RGBA');ppm=data['width']/data['ortho']
 sf=np.array(data['points']['front_axle']);sr=np.array(data['points']['rear_axle']);sf[1]-=HUB*ppm;sr[1]-=HUB*ppm
 pf=np.array(FRONT);pr=np.array(REAR);a0=sr-sf;b0=pr-pf
 scale=np.linalg.norm(b0)/np.linalg.norm(a0);theta=math.atan2(b0[1],b0[0])-math.atan2(a0[1],a0[0])
 co,si=math.cos(theta),math.sin(theta);matrix=scale*np.array([[co,-si],[si,co]]);offset=pf-matrix@sf
 inverse=np.linalg.inv(matrix);trans=-inverse@offset
 warped=source.transform(photo.size,Image.Transform.AFFINE,(*inverse[0],trans[0],*inverse[1],trans[1]),Image.Resampling.BICUBIC)
 alpha=warped.getchannel('A').point(lambda x:round(x*.5));tint=Image.new('RGBA',photo.size,(13,111,205,0));tint.putalpha(alpha)
 photo.alpha_composite(tint);im=photo.convert('RGB');d=ImageDraw.Draw(im);font=ImageFont.truetype(FONT,28);small=ImageFont.truetype(FONT,23)
 d.text((35,35),'ALDER C150 / 50% ORTHOGRAPHIC SILHOUETTE OVER STOCK CREW 5.5 FT PROFILE',font=font,fill=(22,46,67))
 d.text((35,78),'Two wheel centers only: 3683 mm wheelbase. No body-shape fitting or image-to-mesh projection.',font=small,fill=(22,46,67))
 for x,y in [FRONT,REAR]:d.ellipse((x-8,y-8,x+8,y+8),outline=(0,67,138),width=3)
 im.save(out/'side-overlay.jpg',quality=94)
 angle=math.degrees(math.atan2(abs(RAKE[1][1]-RAKE[0][1]),abs(RAKE[1][0]-RAKE[0][0])))
 ref=Image.open(ROOT/'refs/stock-side.jpg').convert('RGB');d=ImageDraw.Draw(ref);d.line((*RAKE[0],*RAKE[1]),fill=(220,30,15),width=5)
 for x,y in RAKE:d.ellipse((x-6,y-6,x+6,y+6),outline=(220,30,15),width=3)
 d.text((35,35),f'A-PILLAR STRAIGHT SEGMENT: {angle:.1f} degrees above horizontal (photo estimate +/- 1.5 deg)',font=font,fill=(50,50,50))
 ref.save(out/'side-rake.jpg',quality=94)
 report=dict(reference='refs/stock-side.jpg',reference_sha256=hashlib.sha256((ROOT/'refs/stock-side.jpg').read_bytes()).hexdigest(),
 source_sha256=data['source_sha256'],wheelbase_m=WB,front_pixel=FRONT,rear_pixel=REAR,reference_pixels_per_m=float(np.linalg.norm(b0)/WB),
 scale=float(scale),rotation_degrees=math.degrees(theta),translation_pixels=offset.tolist(),opacity=.5,photo_rake_degrees=angle,
 caveat='Published photo caption is 4x2; model is 4x4. Axles align; nominal suspension/roof-height differences are visible, not fitted away.')
 (out/'side-overlay.json').write_text(json.dumps(report,indent=2));print('SIDE OVERLAY',out/'side-overlay.jpg',report['reference_pixels_per_m'])
if __name__=='__main__':main()
