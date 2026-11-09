"""Original memorial panels and a single postwar faceted composition.

Four guarded 512px cells in the existing 1K set; all drawing is analytic.
Pale cathedral fields, colored borders and medallions replace random quarries.
"""
import numpy as np
from PIL import Image,ImageDraw


def glass(out):
    n=1024;im=Image.new('RGB',(n,n),(12,15,14));d=ImageDraw.Draw(im)
    lead=(13,16,15);cream=(130,127,99);sage=(106,123,111)
    for cell in (0,2):
        ox=0;oy=512 if cell==0 else 0
        box=(ox+6,oy+6,ox+506,oy+506)
        d.rectangle(box,fill=cream if cell==0 else sage)
        # Pale rectangular cathedral lights with fine horizontal saddle lead.
        for row in range(9):
            for col in range(5):
                x=ox+36+col*88;y=oy+24+row*57
                tone=1+.035*np.sin(row*4.1+col*2.3+cell)
                base=cream if (row+col)%3 else sage
                d.rectangle((x,y,x+88,y+57),fill=tuple(int(v*tone) for v in base),outline=lead,width=1)
        # Two narrow colored borders; no solid color carpet across the field.
        for inset,c in ((10,(49,67,83)),(26,(116,87,46))):
            radius=(256-inset)/256;stem=4.904;h=stem+3**.5
            poly=[(ox+inset,oy+502),(ox+512-inset,oy+502)]
            for j in range(65):
                xx=radius*(1-2*j/64);zz=stem+max(0,4*radius*radius-(abs(xx)+radius)**2)**.5
                poly.append((ox+256+xx*256,oy+512-zz/h*512+inset*.22))
            d.line(poly+[poly[0]],fill=c,width=12)
        for y in range(36,490,44):
            for x in (16,496):
                d.polygon([(ox+x,oy+y-7),(ox+x+5,oy+y),(ox+x,oy+y+7),(ox+x-5,oy+y)],fill=(121,70,54),outline=lead)
        cx=ox+256;cy=oy+255
        d.ellipse((cx-95,cy-113,cx+95,cy+113),fill=(54,77,83),outline=lead,width=3)
        d.ellipse((cx-82,cy-100,cx+82,cy+100),outline=(139,108,58),width=5)
        if cell==0:
            d.rectangle((cx-14,cy-70,cx+14,cy+72),fill=(156,127,72),outline=lead,width=2)
            d.rectangle((cx-55,cy-33,cx+55,cy-8),fill=(156,127,72),outline=lead,width=2)
        else:
            for k in range(8):
                a=k*np.pi/4;px=cx+47*np.cos(a);py=cy+60*np.sin(a)
                d.ellipse((px-19,py-26,px+19,py+26),fill=(142,115,68),outline=lead,width=2)
            d.ellipse((cx-15,cy-15,cx+15,cy+15),fill=(119,65,48),outline=lead,width=2)
        for yy in (110,400):d.line((ox+34,oy+yy,ox+478,oy+yy),fill=lead,width=2)
    # Lower-right: faceted amber and smoke-blue glass, only used by the cross.
    rng=np.random.default_rng(906)
    for row in range(9):
        for col in range(9):
            x=512+col*64;y=512+row*64
            shade=((111,78,35),(128,96,47),(72,92,95),(104,116,107))[int(rng.integers(4))]
            d.polygon([(x,y),(x+64,y),(x+32,y+64)],fill=shade,outline=lead,width=2)
            d.polygon([(x+64,y),(x+96,y+64),(x+32,y+64)],fill=shade,outline=lead,width=2)
    # Upper-right: rose with a warm field and composed radial border.
    cx=768;cy=256;d.ellipse((514,2,1022,510),fill=(122,119,91))
    for k in range(16):
        a=k*22.5;d.pieslice((cx-242,cy-242,cx+242,cy+242),a,a+22.5,fill=(54,76,84) if k%2 else (124,86,49),outline=lead,width=2)
    d.ellipse((cx-181,cy-181,cx+181,cy+181),fill=(130,125,97),outline=lead,width=3)
    for k in range(12):
        a=k*np.pi/6;d.line((cx,cy,cx+181*np.cos(a),cy+181*np.sin(a)),fill=lead,width=2)
    d.ellipse((cx-46,cy-46,cx+46,cy+46),fill=(132,89,48),outline=lead,width=3)
    a=np.asarray(im).astype(float)/255;yy,xx=np.mgrid[:n,:n]
    ripple=np.sin(xx*.13+np.sin(yy*.034)*2)*np.sin(yy*.17)
    a*=.97+.03*ripple[:,:,None]
    # The unused upper-left chart carries gravity deposits. Alpha is ignored
    # by the three opaque glass compositions and consumed only by Church_age.
    # Reusing this quarter adds no images or GPU allocation.
    alpha=np.ones((n,n));gy,gx=np.mgrid[:256,:512];rng=np.random.default_rng(7841)
    field=np.zeros((256,512))
    for j in range(24):
        cx=rng.uniform(12,500);width=rng.uniform(8,30);reach=rng.uniform(.35,1)
        t=gy/256;wav=cx+3*np.sin(t*9+j)
        track=np.exp(-((gx-wav)/(width*(1-.65*t)))**4)*np.clip(1-t/reach,0,1)**.6
        field=np.maximum(field,track*rng.uniform(.45,.95))
    edge=np.clip(np.minimum(gx,511-gx)/18,0,1)*np.clip((255-gy)/20,0,1)
    field*=edge*(.84+.16*np.sin(gx*.13+np.sin(gy*.07)*2)**2)
    alpha[:256,:512]=field
    # The lower half follows a damp slate/tread joint. Growth meanders along
    # that joint, breaks into colonies and fades across it, rather than using
    # the vertical runoff chart as a rectangular stamp on roofs.
    seam=130+25*np.sin(gx*.019)+14*np.sin(gx*.073)+5*np.sin(gx*.21)
    spread=26+12*np.sin(gx*.037+1)**2
    colony=np.clip(.48+.39*np.sin(gx*.029)+.28*np.sin(gx*.091+1.2),0,1)
    growth=np.exp(-((gy-seam)/spread)**4)*colony
    growth*=np.clip(np.minimum(gx,511-gx)/42,0,1)*(.68+.32*np.sin(gx*.27+gy*.34)**2)
    alpha[256:512,:512]=growth*.93
    ay,ax=np.mgrid[:512,:512]
    a[:512,:512,:]=np.array((.32,.33,.30))*(.94+.06*np.sin(ax*.23+ay*.08))[:,:,None]
    rgba=np.dstack((np.clip(a,0,1),alpha))
    Image.fromarray(np.uint8(np.clip(rgba*255,0,255))).save(out/'T_ChurchGlass_BaseColor.png')
    leadfield=np.max(a,axis=2)<.075
    h=leadfield*.0004+.00004*ripple;h[:512,:512]=0
    dy,dx=np.gradient(h);norm=np.stack((-dx*n/3,dy*n/3,np.ones_like(dx)),axis=2);norm/=np.linalg.norm(norm,axis=2,keepdims=True)
    Image.fromarray(np.uint8((norm*.5+.5)*255)).save(out/'T_ChurchGlass_Normal.png')
    orm=np.ones((n,n,3));orm[:,:,1]=np.where(leadfield,.78,.29+.025*ripple);orm[:,:,2]=np.where(leadfield,.32,0)
    orm[:512,:512,1]=.92;orm[:512,:512,2]=0
    Image.fromarray(np.uint8(orm*255)).save(out/'T_ChurchGlass_ORM.png')
