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
    wood=np.zeros((H,W,3),np.float32)+[190,155,103]
    wood+=((grain-.5)*17+(fibres-.5)*8)[:,:,None]
    raw=Image.fromarray(np.uint8(np.clip(wood,0,255)));raw.save(out/f'{state}-maple.png')
    # Discrete longitudinal/oblique gouges: board slides across ledges in the
    # belly and along the rear kick, not a uniform all-surface noise overlay.
    wear=Image.new('L',(W,H));d=ImageDraw.Draw(wear)
    def point(x,y):return ((x+.11)/.22*W,(y+.411)/.822*H)
    if age:
        # Boardslides scrape ACROSS the deck in a broken belly contact area.
        # Varying-width, ragged scars expose connected patches of maple; a
        # spray of fine longitudinal scratches would not describe that contact.
        for j in range(round(100*age)):
            cx=float(rng.normal(0,.032));cy=float(rng.normal(.012,.048))
            length=float(rng.uniform(.035,.17));drift=float(rng.uniform(-.027,.027))
            width=int(rng.integers(5,23 if state=='season' else 34))
            if j%8==0:width*=3
            upper=[];lower=[];phase=float(rng.uniform(0,math.tau))
            half=width*.822/H/2
            for q in range(49):
                u=q/48;xx=cx+(u-.5)*length
                yy=cy+(u-.5)*drift+math.sin(u*17+phase)*.0007
                envelope=math.sin(math.pi*u)**.5
                ragged=.70+.22*math.sin(u*43+phase)+float(rng.uniform(-.23,.23))
                spread=half*envelope*max(.1,ragged)
                upper.append(point(xx,yy+spread));lower.append(point(xx,yy-spread*float(rng.uniform(.65,1.25))))
            d.polygon(upper+list(reversed(lower)),fill=int(rng.integers(185,256)))
        for j in range(round(65*age)):
            cx=float(rng.normal(0,.04));cy=float(rng.normal(.015,.10));length=float(rng.uniform(.010,.060))
            d.line([point(cx-length/2,cy),point(cx+length/2,cy+float(rng.uniform(-.022,.022)))],fill=int(rng.integers(120,240)),width=int(rng.integers(1,4)))
        for j in range(round(260*age)):
            cy=float(rng.uniform(.345,.413));cx=float(rng.normal(0,.050));length=float(rng.uniform(.002,.035))
            d.line([point(cx,cy),point(cx+float(rng.normal(0,.002)),cy+length)],fill=int(rng.integers(150,256)),width=int(rng.integers(2,10)))
        # End abrasion where ollies/curb impacts contact the actual outline.
        cap=np.sqrt(np.maximum(0,1-np.maximum(0,(y-.300)/.112)**2))*.1016
        edgeband=(y>.345)&(np.abs(x)>cap-(.003+age*.007))
        w=np.asarray(wear).copy();w[edgeband]=np.maximum(w[edgeband],220);wear=Image.fromarray(w)
    mask=np.asarray(wear,dtype=np.float32)/255;mask=np.clip((mask-.16)*1.5,0,1)
    graphic=np.asarray(panels[seed%3],dtype=np.float32)
    graphic=graphic*(1-mask[:,:,None])+wood*mask[:,:,None]
    rough=.30+.38*mask+.018*(fibres-.5)
    height=-.00018*mask+(fibres-.5)*.000004
    # Shoe-goo covers a damaged patch of the beat tail, with dragged trowel ribs.
    if state=='beat':
        goo=((x+.018)/.031)**2+((y-.349)/.021)**2+np.sin(x*1500+y*240)*.12<1
        graphic[goo]=np.stack(np.broadcast_arrays(35+grain*12,34+grain*11,28+grain*10),axis=2)[goo]
        rough[goo]=.67
        height=np.where(goo,.0007+.00013*np.sin(x*1200+y*120),height)
    Image.fromarray(np.uint8(np.clip(graphic,0,255))).save(out/f'{state}-bottom.png')
    Image.fromarray(np.uint8(np.clip(rough*255,0,255))).save(out/f'{state}-bottom-rough.png')
    Image.fromarray(np.uint16(np.clip(.5+height/.004,0,1)*65535)).save(out/f'{state}-bottom-height.png')
    # Sole-shaped patches under front stance and rear kick. Grit is retained
    # at edges and between feet, burnished in the repeatedly planted zones.
    sole=np.exp(-((x+.010)/.075)**4-((y+.12)/.105)**4)+np.exp(-((x-.008)/.075)**4-((y-.277)/.072)**4)
    sole=np.clip(sole,0,1)*age
    streak=np.clip(.55+.25*np.sin(y*290+x*90)+.2*(fibres-.5),0,1)
    grip=10+fibres*13+sole*(32+14*streak)
    griprgb=np.stack([grip*1.02,grip,grip*.91],axis=2)
    gritrough=.90-.34*sole
    gripheight=(fibres-.5)*(.00027-.00017*sole)
    # Narrow filed score at the trim, and an original small orientation sticker.
    if state=='beat':
        nose=np.sqrt(np.maximum(0,1-np.maximum(0,(-y-.287)/.124)**2))*.1016
        torn=(y<-.345)&(x>nose-.026+np.sin(y*1200)*.003)
        griprgb=np.where(torn[:,:,None],wood,griprgb);gritrough=np.where(torn,.73,gritrough);gripheight=np.where(torn,-.00055,gripheight)
    im=Image.fromarray(np.uint8(np.clip(griprgb,0,255)));d=ImageDraw.Draw(im)
    d.polygon([point(-.033,.012),point(.030,.020),point(.026,.040),point(-.037,.032)],fill=(171,159,117))
    text_center(d,point(-.004,.026),'DL / 08',25,(29,46,43))
    im.save(out/f'{state}-grip.png')
    Image.fromarray(np.uint8(np.clip(gritrough*255,0,255))).save(out/f'{state}-grip-rough.png')
    Image.fromarray(np.uint16(np.clip(.5+gripheight/.004,0,1)*65535)).save(out/f'{state}-grip-height.png')
    return dict(state=state,belly_scrape_fraction=float((mask[(np.abs(y[:,0])<.16)]>.5).mean()),foot_polish_max=float(sole.max()))

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='build/art');p.add_argument('--seed',type=int,default=0);a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    panels=designs(out)
    import json
    (out/'fields.json').write_text(json.dumps([state_fields(out,panels,k,a.seed) for k in ('new','season','beat')],indent=2))
if __name__=='__main__':main()
