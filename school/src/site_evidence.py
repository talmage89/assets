"""Original program diagrams beside references; no tracing or material input.

Centerlines and reservations explain design intent. Actual source-surface
measurements remain independent in check.py. Images stay in ignored renders.
"""
import math,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from plans import school
from kit.fonts import find_font
FONT=find_font('DejaVu Sans','Book')


def diagram(p):
    im=Image.new('RGB',(1200,1100),(235,232,217));d=ImageDraw.Draw(im);a=math.radians(p['site_yaw'])
    def xy(q):
        x,y=q;return (600+4*(x*math.cos(a)-y*math.sin(a)),550-4*(x*math.sin(a)+y*math.cos(a)))
    def rect(r,color):
        l,rr,f,k=r;d.polygon([xy(q) for q in ((l,f),(rr,f),(rr,k),(l,k))],fill=color,outline=(87,91,75))
    def label(q,s,size=17):d.text(xy(q),s,font=ImageFont.truetype(FONT,size),fill=(25,32,25),anchor='mm',stroke_width=1,stroke_fill=(235,232,217))
    rect((-105,105,-92,92),(178,185,152))
    for row in p['streets']:
        at=row['at'];rect((-130,130,at-3.66,at+3.66) if row['axis']=='X' else (at-3.66,at+3.66,-130,130),(106,110,106))
    for key,color,text in [('parking',(132,134,132),'Staff lot'),('blacktop',(93,100,102),'School blacktop'),('playground',(196,173,126),'Play socket')]:
        rect(p[key],color);l,r,f,k=p[key];label(((l+r)/2,(f+k)/2),text)
    if p['type']=='finger':rect((-18.7,29,19.84,30.20),(93,100,102))
    fx,fy=p['field'];rect((fx,fx+24,fy,fy+24),(167,151,115));label((fx+12,fy+12),'Field')
    for c in p['covered']:rect(c['rect'],(203,194,169))
    for b in p['blocks']:
        rect(b['rect'],(150,120,92) if b['kind']=='gym' else (194,171,137))
        if b['kind'] in ('gym','office','kitchen','media'):
            l,r,f,k=b['rect'];label(((l+r)/2,(f+k)/2),b['kind'].title(),14)
    for name,color in [('bus',(182,80,21)),('parent',(23,99,155))]:
        points=[xy(q) for q in p[name+'_route']];d.line(points,fill=color,width=10,joint='curve')
        for j in range(1,len(points),3):
            aa,bb=points[j-1],points[j];tip=(aa[0]*.4+bb[0]*.6,aa[1]*.4+bb[1]*.6);vx,vy=bb[0]-aa[0],bb[1]-aa[1];n=math.hypot(vx,vy);vx/=n;vy/=n
            d.polygon([tip,(tip[0]-vx*20-vy*8,tip[1]-vy*20+vx*8),(tip[0]-vx*20+vy*8,tip[1]-vy*20-vx*8)],fill=color)
        d.line([xy(q) for q in p[name+'_curb']],fill=(254,240,208),width=4)
    for x,y in p['trees'][:5]:
        xx,yy=xy((x,y));d.ellipse((xx-19,yy-19,xx+19,yy+19),fill=(60,91,54))
    ex,ey=p['entry'];label((ex,ey-4),'ENTRY')
    d.text((30,22),f"{p['seed']} / {p['name']} / {p['parcel']}",font=ImageFont.truetype(FONT,23),fill=(28,34,28))
    for y,text in [(1030,'Orange: buses   Blue: parents   Pale curb: loading side'),(1062,'Authored centerlines / schematic program; actual paving is checked independently.')]:d.text((30,y),text,font=ImageFont.truetype(FONT,18),fill=(28,34,28))
    d.line((1130,125,1130,62),fill=(30,40,30),width=3);d.polygon([(1130,52),(1122,70),(1138,70)],fill=(30,40,30));d.text((1130,35),'N',anchor='mm',font=ImageFont.truetype(FONT,21),fill=(30,40,30))
    return im


def main():
    out=Path('renders/site-evidence');out.mkdir(parents=True,exist_ok=True)
    rows=[(101,'postwar-site-survey.pdf',35,(150,0,1240,875),'LAUSD 1956 site plan / Fig34; Sapphos 2018'),(102,'site-guide.pdf',50,(490,365,1280,1020),'CDE 2000 / printed p41 / corner-site diagram'),(103,'postwar-site-survey.pdf',38,(265,1010,1100,1620),'LAUSD 1974 plot plan / Fig39; Sapphos 2018')]
    for seed,pdf,page,crop,title in rows:
        prefix=Path('build')/f'site-reference-{seed}'
        subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1800','-singlefile','-png',str(Path('refs')/pdf),str(prefix)],check=True)
        reference=Image.open(prefix.with_suffix('.png')).convert('RGB').crop(crop);reference.thumbnail((1170,940))
        pair=Image.new('RGB',(2400,1100),(250,249,242));pair.paste(diagram(school(seed)),(0,0));pair.paste(reference,(1200+(1200-reference.width)//2,90+(940-reference.height)//2));d=ImageDraw.Draw(pair)
        d.text((1225,25),title,font=ImageFont.truetype(FONT,22),fill=(28,34,28));d.text((1225,1040),'Relationship comparison: original wider parcel, not a replica.',font=ImageFont.truetype(FONT,19),fill=(38,46,38));pair.save(out/f'{seed}-plan.jpg',quality=93,optimize=True)
    print('SITE RELATIONSHIP PAIRS',out)

if __name__=='__main__':main()
