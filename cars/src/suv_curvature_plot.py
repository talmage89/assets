"""Plot sampled evaluated geometry/normal curvature; retain every sign crossing."""
import argparse,json,math,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
FONT=find_font('Noto Sans','Regular')
def font(n):return ImageFont.truetype(FONT,n)
def main():
 p=argparse.ArgumentParser();p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args()
 report=json.loads(Path(a.report).read_text());out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 for group,names in [('body',[r for r in report['sections'] if r['kind']=='side']),('hood-roof',[r for r in report['sections'] if r['kind']=='top'])]:
  width=1500;height=120+len(names)*300;im=Image.new('RGB',(width,height),(242,243,240));d=ImageDraw.Draw(im)
  d.text((25,20),'EVALUATED SECTION / SIGNED NORMAL CURVATURE',font=font(26),fill=(25,44,53))
  d.text((25,60),report['scope']+'; blue geometry, orange curvature; shaded construction-line zones. Cuts split runs.',font=font(18),fill=(50,68,74))
  for index,row in enumerate(names):
   top=120+index*300;samples=row['samples']
   if not samples:continue
   ts=[r['t'] for r in samples];vs=[r['value'] for r in samples];ks=[r['curvature_m_inv'] for r in samples]
   tlo,thi=min(ts),max(ts);vlo,vhi=min(vs),max(vs);kmax=max(1,max(abs(k) for k in ks));kmax=min(100,kmax)
   d.text((25,top+5),row['name'],font=font(21),fill=(25,44,53))
   d.text((25,top+37),f'Geometry range {vlo:.3f} to {vhi:.3f} m; curvature plot +/-{kmax:.2f} /m',font=font(16),fill=(60,75,80))
   for x0,key,low,high,color in [(50,'value',vlo-.005,vhi+.005,(30,87,123)),(795,'curvature_m_inv',-kmax,kmax,(184,76,20))]:
    def xy(r):return (x0+(r['t']-tlo)/(thi-tlo)*650,top+260-(max(low,min(high,r[key]))-low)/(high-low)*180)
    if key=='curvature_m_inv':
     for zone in row.get('character_line_zones',[]):
      a,b=zone['range'];xa=x0+(max(tlo,a)-tlo)/(thi-tlo)*650;xb=x0+(min(thi,b)-tlo)/(thi-tlo)*650
      if xb>xa:d.rectangle((xa,top+80,xb,top+260),fill=(228,233,221))
    for frac in [0,.25,.5,.75,1]:d.line((x0,top+80+180*frac,x0+650,top+80+180*frac),fill=(209,215,211))
    if key=='curvature_m_inv':d.line((x0,top+170,x0+650,top+170),fill=(110,120,115),width=2)
    run=[]
    for r in samples:
     if r.get('break_before') and run:
      if len(run)>1:d.line(run,fill=color,width=2)
      run=[]
     run.append(xy(r))
    if len(run)>1:d.line(run,fill=color,width=2)
    d.text((x0,top+265),f'{tlo:+.3f} m',font=font(14),fill=(65,75,77));d.text((x0+570,top+265),f'{thi:+.3f} m',font=font(14),fill=(65,75,77))
  im.save(out/f'curvature-{group}.jpg',quality=92,optimize=True)
if __name__=='__main__':main()
