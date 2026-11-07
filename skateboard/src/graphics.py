"""Original vector artwork and cause-specific raster source fields; no photo input."""
from pathlib import Path
import sys,math,argparse
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from kit.fonts import find_font
FONT=find_font('DejaVu Sans','Bold');SMALL=find_font('DejaVu Sans','Book')
W,H=768,3072

def text_center(d,xy,text,size,fill,font=FONT):
    f=ImageFont.truetype(font,size);d.text(xy,text,font=f,fill=fill,anchor='mm')

def designs(out):
    panels=[]
    for k,(brand,bg,ink,accent) in enumerate([
        ('DITCHLIGHT',(17,49,48),(221,208,165),(211,88,37)),
        ('KILNLINE',(119,34,25),(234,212,156),(24,39,45)),
        ('STATIC ORCHARD',(33,37,57),(223,218,188),(177,82,65))]):
        im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im)
        # Three distinct authored motifs on one sheet; original shapes only.
        if k==0:
            for j in range(17):
                pts=[]
                for i in range(241):
                    a=math.tau*i/240;r=50+j*14
                    pts.append((W/2+math.cos(a)*r*(1+.12*math.sin(3*a)),H*.51+math.sin(a)*r*2.2+37*math.sin(a*2+j*.15)))
                d.line(pts,fill=ink if j%4 else accent,width=3 if j%4 else 9)
            d.polygon([(W*.26,H*.45),(W*.56,H*.385),(W*.70,H*.535),(W*.44,H*.60)],fill=accent)
            d.ellipse((W*.425,H*.475,W*.575,H*.525),fill=bg,outline=ink,width=5)
        elif k==1:
            for j in range(13):
                yy=770+j*105
                for i in range(4):
                    xx=105+i*140+(j%2)*47
                    d.polygon([(xx,yy),(xx+113,yy-31),(xx+135,yy+33),(xx+22,yy+64)],fill=accent if (i+j)%4 else ink)
            d.polygon([(350,850),(540,1250),(452,1420),(492,1800),(252,1480),(320,1290)],fill=ink)
            text_center(d,(W/2,2080),'FIRED / FORMED / FREE',27,ink)
        else:
            for j in range(7):
                yy=790+j*175;rr=135-j*8
                d.ellipse((W/2-rr,yy-80,W/2+rr,yy+80),fill=accent if j%2 else ink)
                d.rectangle((W/2-rr,yy-8,W/2+rr,yy+8),fill=bg)
                d.line((125,yy+40,645,yy+90),fill=ink,width=4)
            d.line((W/2,850,W/2,2020),fill=bg,width=18)
            text_center(d,(W/2,2150),'FREQUENCY / 07',28,ink)
        for yy in (405,2555):
            d.line((130,yy-95,638,yy-95),fill=accent,width=6)
            text_center(d,(W/2,yy),brand,51 if k<2 else 43,ink)
            text_center(d,(W/2,yy+90),'MAPLE / SEVEN PLY / STREET',23,ink,font=SMALL)
        text_center(d,(W/2,2190),'08  /  SIDE CHANNEL',25,ink,font=SMALL)
        text_center(d,(W/2,2250),'PRESSED TO GO SOMEWHERE',19,ink,font=SMALL)
        panels.append(im)
    sheet=Image.new('RGB',(W*3,H))
    for k,im in enumerate(panels):sheet.paste(im,(k*W,0))
    sheet.save(out/'graphics-sheet.png')
    # Circumferential wheel type, original print. Blank inner shield ring.
    im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im)
    for radius in (163,192):d.ellipse((256-radius,256-radius,256+radius,256+radius),outline=(48,52,43,220),width=3)
    for text,start in [('KILNLINE',-146),('54 / 99A',38)]:
        for j,ch in enumerate(text):
            a=math.radians(start+j*13);p=(256+178*math.cos(a),256+178*math.sin(a))
            tile=Image.new('RGBA',(60,60));td=ImageDraw.Draw(tile);text_center(td,(30,30),ch,27,(44,48,40,255))
            tile=tile.rotate(-math.degrees(a)-90,resample=Image.Resampling.BICUBIC)
            im.alpha_composite(tile,(round(p[0]-30),round(p[1]-30)))
    im.save(out/'wheel-print.png')
    stamp=Image.new('RGBA',(1024,256));sd=ImageDraw.Draw(stamp)
    text_center(sd,(512,100),'CROSSWAY',108,(43,48,45,255))
    text_center(sd,(512,205),'CAST / 137',44,(43,48,45,255))
    stamp.save(out/'truck-print.png')
    return panels

def state_fields(out,panels,state,seed=0):
    rng=np.random.default_rng(317+seed);age={'new':0,'season':.58,'beat':1}[state]
    x=np.linspace(-.11,.11,W,dtype=np.float32)[None,:];y=np.linspace(-.411,.411,H,dtype=np.float32)[:,None]
    # Long grain comes from stretched anisotropic cellular variations, not a
    # photograph. The crossed plies get their own shader coordinates.
    grain=np.sin(x*2800+3*np.sin(y*18)+np.sin(x*250+y*23))*.5+.5
    fibres=rng.random((H,W),dtype=np.float32)
    wood=np.zeros((H,W,3),np.float32)+[204,172,118]
    wood+=((grain-.5)*17+(fibres-.5)*8)[:,:,None]
    raw=Image.fromarray(np.uint8(np.clip(wood,0,255)));raw.save(out/f'{state}-maple.png')
    # Ledge travel is transverse in a boardslide. Each contact pass has one
    # direction; independent passes overlap as shallow ink loss and deeper
    # wood gouges, rather than lines radiating from a point.
    wear=Image.new('L',(W,H));d=ImageDraw.Draw(wear)
    def point(x,y):return ((x+.11)/.22*W,(y+.411)/.822*H)
    if age:
        for cy,span,slope in ((.012,.052,.025),(-.028,.028,-.055)):
            for j in range(round(155*age)):
                yy=float(rng.normal(cy,span*.55))
                cx=float(rng.normal(0,.018));length=float(rng.uniform(.065,.205))
                width=int(rng.integers(1,11 if state=='season' else 20))
                upper=[];lower=[];phase=float(rng.uniform(0,math.tau))
                for q in range(49):
                    u=q/48;xx=cx+(u-.5)*length
                    mid=yy+(xx-cx)*slope+math.sin(u*23+phase)*.00022
                    taper=math.sin(math.pi*u)**.35
                    half=width*.822/H*.5*taper*(.8+float(rng.uniform(-.3,.3)))
                    upper.append(point(xx,mid+half));lower.append(point(xx,mid-half))
                # Same stroke color through its whole width: no radial fan.
                d.polygon(upper+list(reversed(lower)),fill=int(rng.integers(100,256)))
        # Tip slides and ollie dragging travel along the nose/tail, with
        # ragged termination. The nose has fewer contacts than the tail.
        for sign,count in ((1,round(250*age)),(-1,round(65*age))):
            for j in range(count):
                yy=sign*float(rng.uniform(.350,.413));xx=float(rng.normal(0,.043))
                length=float(rng.uniform(.006,.044));width=int(rng.integers(1,8))
                d.line([point(xx,yy),point(xx+float(rng.uniform(-.001,.001)),yy+sign*length)],fill=int(rng.integers(115,256)),width=width)
        # Smith/feeble contacts chip the rail, localized beside the truck,
        # rather than covering the whole bottom with an edge overlay.
        for side,cy in ((1,.125),(-1,-.105)):
            for j in range(round(34*age)):
                yy=float(rng.normal(cy,.028));xx=side*float(rng.uniform(.086,.102))
                d.line([point(xx,yy),point(xx-side*float(rng.uniform(.001,.008)),yy+.006)],fill=int(rng.integers(150,256)),width=int(rng.integers(2,7)))
        cap=np.sqrt(np.maximum(0,1-np.maximum(0,(y-.300)/.112)**2))*.1016
        edgeband=(y>.360)&(np.abs(x)>cap-(.002+age*.005))
        w=np.asarray(wear).copy();w[edgeband]=np.maximum(w[edgeband],220);wear=Image.fromarray(w)
    contact=np.asarray(wear,dtype=np.float32)/255
    # Three physical layers: lacquer abrasion, pale primer/ink base, then
    # maple. Deeper tracks retain wood grain and ingrained gray ledge dirt.
    primer=np.clip((contact-.31)/.18,0,1)
    bare=np.clip((contact-.59)/.32,0,1)
    graphic=np.asarray(panels[seed%3],dtype=np.float32)
    white=np.stack(np.broadcast_arrays(206+(fibres-.5)*12,203+(fibres-.5)*12,188+(fibres-.5)*12),axis=2)
    graphic=graphic*(1-primer[:,:,None])+white*primer[:,:,None]
    scarwood=wood*.84+np.stack(np.broadcast_arrays(grain*5,grain*3,grain),axis=2)
    graphic=graphic*(1-bare[:,:,None])+scarwood*bare[:,:,None]
    rough=.30+.16*np.clip(contact*3,0,1)+.24*bare+.018*(fibres-.5)
    height=-.000055*primer-.00017*bare+(fibres-.5)*.000004
    if state=='beat':
        goo=((x+.018)/.031)**2+((y-.349)/.021)**2+np.sin(x*1500+y*240)*.12<1
        graphic[goo]=np.stack(np.broadcast_arrays(35+grain*12,34+grain*11,28+grain*10),axis=2)[goo]
        rough[goo]=.67
        height=np.where(goo,.0007+.00013*np.sin(x*1200+y*120),height)
    Image.fromarray(np.uint8(np.clip(graphic,0,255))).save(out/f'{state}-bottom.png')
    Image.fromarray(np.uint8(np.clip(rough*255,0,255))).save(out/f'{state}-bottom-rough.png')
    Image.fromarray(np.uint16(np.clip(.5+height/.004,0,1)*65535)).save(out/f'{state}-bottom-height.png')
    # Irregular shoe contact over the front bolts and in the rear pocket.
    # Smooth random modulation has no periodic bands. Silicon carbide's
    # aggregate and facets are made in the shader at real meter scales.
    low=Image.fromarray(rng.integers(0,256,(61,17),dtype=np.uint8)).resize((W,H),Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(3))
    mottled=np.asarray(low,dtype=np.float32)/255
    sole=np.exp(-((x+.012+(y+.19)*.18)/.078)**4-((y+.19)/.088)**4)+np.exp(-((x-.010-(y-.287)*.12)/.068)**4-((y-.287)/.059)**4)
    sole=np.clip(sole*(.65+.55*mottled),0,1)*age
    grip=22+fibres*12+sole*(29+17*mottled)
    griprgb=np.stack([grip*1.015,grip,grip*.96],axis=2)
    gritrough=.79-.28*sole
    gripheight=(fibres-.5)*.000045*(1-.7*sole)
    # Filed trim and toe-drag fraying follow the actual rounded deck outline.
    cap=np.where(y<0,np.sqrt(np.maximum(0,1-np.maximum(0,(-y-.287)/.124)**2)),np.sqrt(np.maximum(0,1-np.maximum(0,(y-.300)/.112)**2)))*.1016
    inward=cap-np.abs(x)
    fray=(age>0)&(x>0)&(y>-.30)&(y<-.13)&(inward<(.007+age*.007*mottled))
    coverage=np.ones((H,W),dtype=np.uint8)*255;coverage[fray]=0
    griprgb=np.where(fray[:,:,None],wood*.76,griprgb);gritrough=np.where(fray,.75,gritrough);gripheight=np.where(fray,-.00032,gripheight)
    if state=='beat':
        torn=(y<-.345)&(x>cap-.026+np.sin(y*1200)*.003)
        coverage[torn]=0
        griprgb=np.where(torn[:,:,None],wood,griprgb);gritrough=np.where(torn,.73,gritrough);gripheight=np.where(torn,-.00055,gripheight)
    # No center label: the entire grip is abrasive sheet.
    Image.fromarray(np.uint8(np.clip(griprgb,0,255))).save(out/f'{state}-grip.png')
    Image.fromarray(np.uint8(np.clip(gritrough*255,0,255))).save(out/f'{state}-grip-rough.png')
    Image.fromarray(np.uint16(np.clip(.5+gripheight/.004,0,1)*65535)).save(out/f'{state}-grip-height.png')
    Image.fromarray(np.uint8(np.clip(sole,0,1)*255)).save(out/f'{state}-foot-contact.png')
    Image.fromarray(coverage).save(out/f'{state}-grip-coverage.png')
    return dict(state=state,belly_scrape_fraction=float((bare[(np.abs(y[:,0])<.16)]>.5).mean()),foot_polish_max=float(sole.max()))

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='build/art');p.add_argument('--seed',type=int,default=0);a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    panels=designs(out)
    import json
    (out/'fields.json').write_text(json.dumps([state_fields(out,panels,k,a.seed) for k in ('new','season','beat')],indent=2))
if __name__=='__main__':main()
