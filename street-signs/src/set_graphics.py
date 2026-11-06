"""Original, dimension-driven sign artwork. References supply no pixels/paths."""
import json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from set_catalog import SIGNS
from set_symbols import place as symbol
FONT=find_font('DejaVu Sans','Condensed')
WHITE=(219,222,211);BLACK=(8,10,9);RED=(174,12,22);YELLOW=(231,174,12);FYG=(174,211,20)
COLORS=dict(white=WHITE,black=BLACK,yellow=YELLOW,fyg=FYG)

def word(im,text,cx,top,w,h,color=BLACK):
    f=ImageFont.truetype(FONT,220);b=f.getbbox(text)
    mask=Image.new('L',(b[2]-b[0]+2,b[3]-b[1]+2));ImageDraw.Draw(mask).text((-b[0],-b[1]),text,font=f,fill=255)
    mask=mask.crop(mask.getbbox()).resize((max(1,round(w)),max(1,round(h))),Image.Resampling.LANCZOS)
    im.paste(color,(round(cx-w/2),round(top)),mask)

def arrow(draw,points,width,fill=BLACK):
    draw.line(points,fill=fill,width=round(width),joint='curve')
    a,b=points[-2:];dx,dy=b[0]-a[0],b[1]-a[1];r=math.hypot(dx,dy);dx,dy=dx/r,dy/r
    p=(b[0]-dx*width*1.8,b[1]-dy*width*1.8)
    draw.polygon([b,(p[0]-dy*width*1.2,p[1]+dx*width*1.2),(p[0]+dy*width*1.2,p[1]-dx*width*1.2)],fill=fill)

def face(key,spec,res=1024):
    w,h=spec['w'],spec['h'];scale=res/max(w,h);W,H=round(w*scale),round(h*scale)
    bg=COLORS[spec['color']];im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im)
    dimscale=scale/math.sqrt(2) if spec['shape']=='diamond' else scale
    t=spec['border']*dimscale;i=spec['inset']*dimscale;r=spec['radius']*dimscale
    if spec['shape']=='rect' and t:
        d.rounded_rectangle((i,i,W-i,H-i),radius=max(1,r-i),outline=RED if spec['code'].startswith('R7') else BLACK,width=round(t))
    if spec['shape']=='diamond':
        # Artwork stays upright; blank rotation is already in its mesh outline.
        d.polygon([(W*.5,i),(W-i,H*.5),(W*.5,H-i),(i,H*.5)],fill=BLACK)
        q=(i+t)*1.42;d.polygon([(W*.5,q),(W-q,H*.5),(W*.5,H-q),(q,H*.5)],fill=bg)
    if key.startswith('speed'):
        large=w==30;word(im,'SPEED',W/2,(4.5 if large else 4)*scale,(23.508 if large else 18.806)*scale,spec['caps']*scale)
        word(im,'LIMIT',W/2,(12 if large else 10)*scale,(18.302 if large else 14.642)*scale,spec['caps']*scale)
        word(im,str(spec['value']),W/2,(19.5 if large else 16)*scale,(17.0 if large else 14)*scale,spec['digits']*scale)
    elif key=='yield':
        def triangle(inches):
            f=1-inches/(h/3)
            return [(W/2+(x-W/2)*f,H/3+(y-H/3)*f) for x,y in [(0,0),(W,0),(W/2,H)]]
        d.polygon(triangle(.75),fill=RED);d.polygon(triangle(5.0),fill=WHITE)
        word(im,'YIELD',W/2,7*scale,9.063*scale,3*scale,RED)
    elif key.startswith('oneway') and key!='onewayVertical':
        pts=[(W*.055,H*.28),(W*.76,H*.28),(W*.76,H*.10),(W*.96,H*.50),(W*.76,H*.90),(W*.76,H*.72),(W*.055,H*.72)]
        if key.endswith('L'):pts=[(W-x,y) for x,y in pts]
        d.polygon(pts,fill=WHITE);word(im,'ONE WAY',W*.48,H*.33,W*.68,4*scale)
    elif key=='onewayVertical':
        word(im,'ONE',W/2,3*scale,14.97*scale,6*scale);word(im,'WAY',W/2,10.875*scale,14.65*scale,6*scale)
        arrow(d,[(W*.20,H*.73),(W*.83,H*.73)],H*.08)
    elif key=='doNotEnter':
        d.ellipse((W*.015,H*.015,W*.985,H*.985),fill=RED)
        d.rectangle((W*.08,H*.417,W*.92,H*.583),fill=WHITE)
        word(im,'DO NOT',W/2,H*.217,W*.65,4*scale,WHITE);word(im,'ENTER',W/2,H*.65,W*.62,4*scale,WHITE)
    elif key=='parkingTimePlate':
        word(im,'8 AM TO 6 PM',W/2,1.05*scale,10*scale,1.5*scale,RED)
        word(im,'MON — FRI',W/2,3.45*scale,9.5*scale,1.5*scale,RED)
    elif key=='parkingTimedHead':
        word(im,'NO',W/2,1.4*scale,5.3*scale,3*scale,RED);word(im,'PARKING',W/2,5.0*scale,9.75*scale,3*scale,RED)
        arrow(d,[(W*.25,H*.84),(W*.79,H*.84)],W*.045,RED)
    elif key.startswith('noParking') or key=='parkingTime':
        for txt,top,width,height in [('NO',1.875,5.3,3),('PARKING',5.75,9.75,3)]:word(im,txt,W/2,top*scale,width*scale,height*scale,RED)
        if key=='parkingTime':
            word(im,'8:30 AM',W/2,9.5*scale,9.0*scale,2*scale,RED);word(im,'TO 5:30 PM',W/2,12.125*scale,10*scale,2*scale,RED)
        else:
            word(im,'ANY',W/2,9.375*scale,4.375*scale,2*scale,RED);word(im,'TIME',W/2,12*scale,5.25*scale,2*scale,RED)
        if key.endswith('L'):arrow(d,[(W*.80,H*.86),(W*.18,H*.86)],W*.045,RED)
        elif key.endswith('R'):arrow(d,[(W*.20,H*.86),(W*.82,H*.86)],W*.045,RED)
        else:
            arrow(d,[(W*.5,H*.86),(W*.18,H*.86)],W*.042,RED);arrow(d,[(W*.5,H*.86),(W*.82,H*.86)],W*.042,RED)
    elif key=='noTurnRed':
        # R10-11 is the red circular signal version; the all-text sign is R10-11a.
        word(im,'NO',W/2,2.75*scale,9.362*scale,5*scale)
        word(im,'TURN',W/2,9.75*scale,12.82*scale,4*scale)
        word(im,'ON RED',W/2,15.75*scale,18.598*scale,4*scale)
        d.ellipse((W/2-3*scale,21.25*scale,W/2+3*scale,27.25*scale),fill=RED)
    elif key=='schoolPlaque':word(im,'SCHOOL',W/2,2*scale,20.25*scale,4*scale)
    elif key=='schoolTime':
        word(im,'7:30 TO 9 AM',W/2,1.3*scale,20*scale,2.5*scale);word(im,'2:30 TO 4 PM',W/2,5.8*scale,20*scale,2.5*scale)
    elif key=='curve':
        pts=[(W*.39,H*.75),(W*.39,H*.59),(W*.41,H*.52),(W*.47,H*.45),(W*.57,H*.35),(W*.66,H*.26)]
        arrow(d,pts,4.375*dimscale)
    elif key=='stopAhead':
        arrow(d,[(W*.5,H*.40),(W*.5,H*.18)],W*.065)
        cx,cy=W*.5,H*.63;rr=W*.205
        pts=[(cx+rr*math.cos(math.pi/8+k*math.pi/4),cy+rr*math.sin(math.pi/8+k*math.pi/4)) for k in range(8)]
        d.polygon(pts,fill=WHITE);pts=[(cx+(rr-W*.012)*math.cos(math.pi/8+k*math.pi/4),cy+(rr-W*.012)*math.sin(math.pi/8+k*math.pi/4)) for k in range(8)];d.polygon(pts,fill=RED)
    elif key.startswith('pedestrian'):symbol(im,'pedestrian',(W*.27,H*.16,W*.73,H*.82),BLACK)
    elif key=='schoolCrossing':
        d.polygon([(W*.5,i),(W-i,H*.50),(W-i,H-i),(i,H-i),(i,H*.50)],fill=BLACK)
        q=(i+t);d.polygon([(W*.5,q*1.3),(W-q,H*.52),(W-q,H-q),(q,H-q),(q,H*.52)],fill=bg)
        symbol(im,'school',(W*.12,H*(8.5/36),W*.88,H*(32.5/36)),BLACK)
    elif key.startswith('arrow'):arrow(d,[(W*.72,H*.22),(W*.28,H*.75)],H*.12)
    # Causal sheeting age: slight exposed upper fading, lower-edge road film,
    # and narrow tracks below the two actual mounting holes. Printed black
    # remains black. No uniform dirt/noise overlay or circular rust blobs.
    a=np.asarray(im).astype(np.float32);yy,xx=np.mgrid[:H,:W];u=xx/max(1,W-1);v=yy/max(1,H-1)
    light=np.mean(a,axis=2)>45
    fade=(1-v)**4*.045;edge=np.minimum.reduce([u,1-u,v,1-v]);dirt=np.exp(-edge/.010)*( .025+.055*v)
    streak=np.exp(-((u-.5)/.007)**2)*np.maximum(0,1-np.abs(v-.88)/.07)*.12
    a=a*(1-(dirt+streak)[:,:,None]);a+=fade[:,:,None]*light[:,:,None]*9
    return Image.fromarray(np.uint8(np.clip(a,0,255)))

def main():
    out=Path(sys.argv[1] if len(sys.argv)>1 else 'build/set');out.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(2048,2048),(142,149,146));layout={};cellw,cellh=409,341
    for j,(key,spec) in enumerate(SIGNS.items()):
        im=face(key,spec);im.thumbnail((cellw-24,cellh-24),Image.Resampling.LANCZOS)
        x=(j%5)*cellw+(cellw-im.width)//2;y=(j//5)*cellh+(cellh-im.height)//2
        sheet.paste(im,(x,y));layout[key]=[x/2048,1-(y+im.height)/2048,(x+im.width)/2048,1-y/2048]
    # Hardware/aluminum and rear inspection labels share this very same image.
    d=ImageDraw.Draw(sheet);d.rectangle((1660,1740,2010,1820),fill=(158,165,162));layout['metal']=[1664/2048,(2048-1816)/2048,2006/2048,(2048-1744)/2048]
    rng=np.random.default_rng(271);metal=np.full((80,350,3),(158,165,162),np.float32)
    # Original zinc crystal variation / rolled-aluminum streaks in one shared
    # hardware swatch; plain metal remains metallic in the delivered shader.
    cloud=rng.normal(0,3,(10,44));cloud=np.asarray(Image.fromarray(np.uint8(np.clip(128+cloud*5,0,255))).resize((350,80),Image.Resampling.BILINEAR)).astype(float)-128
    metal+=cloud[:,:,None]*.32;metal+=rng.normal(0,1,(80,350,1));sheet.paste(Image.fromarray(np.uint8(np.clip(metal,0,255))),(1660,1740))
    label=Image.new('RGB',(360,150),(185,187,170));word(label,'ALDERVALE • STREETS',180,12,320,26);word(label,'INSPECTED 06 / 2009',180,57,290,23);word(label,'PROPERTY 03714',180,103,270,22)
    sheet.paste(label,(1650,1860));layout['backlabel']=[1650/2048,(2048-2010)/2048,2010/2048,(2048-1860)/2048]
    rgb=np.asarray(sheet);luma=rgb.max(axis=2).astype(float)/255
    # Opaque alpha is linear specular-factor data: black printing suppresses
    # the bright substrate lobe. It never controls coverage or adds an image.
    alpha=np.uint8(np.clip(.07+.89*np.clip((luma-.035)/.70,0,1),0,1)*255+.5)
    sheet=Image.fromarray(np.dstack([rgb,alpha]),'RGBA')
    sheet.save(out/'T_RoadSigns_Faces.png');(out/'layout.json').write_text(json.dumps(layout,indent=2))
if __name__=='__main__':main()
