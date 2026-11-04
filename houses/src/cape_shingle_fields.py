"""Original metric cedar and cement manufacture; no reference-image inputs."""
import math,random,json
import numpy as np
from kit.image_io import write_png,linear_to_srgb


def shingle_tile(folder,size=512):
    folder.mkdir(parents=True,exist_ok=True)
    yy,xx=np.mgrid[:size//2,:size];x=(xx+.5)/size*1.2192
    colors=[];heights=[];units=[]
    for kind in ('cedar','cement'):
        exposure=.1524 if kind=='cedar' else .2794
        z=(yy+.5)/(size//2)*(.762 if kind=='cedar' else .5588)
        row=np.floor(z/exposure).astype(int);height=np.zeros_like(x);color=np.ones((*x.shape,3));ao=np.ones_like(x)
        for r in range(5 if kind=='cedar' else 2):
            rng=random.Random(417+r*97)
            if kind=='cedar':
                count=rng.choice((7,8,9));remaining=1.2192;widths=[]
                for j in range(count):
                    left=count-j-1;lo=max(.0762,remaining-.254*left);hi=min(.254,remaining-.0762*left)
                    width=rng.uniform(lo,hi);widths.append(width);remaining-=width
                shift=rng.uniform(0,1.2192);edges=np.r_[0,np.cumsum(widths)]-shift
            else:widths=[.6096,.6096];edges=np.array([0,.6096,1.2192])-.3048*(r%2)
            for j,(a,b) in enumerate(zip(edges,edges[1:])):
                butt=rng.uniform(-.003,.003) if kind=='cedar' else 0
                v=np.mod(z+butt,exposure)/exposure;key=np.minimum(x-a,b-x)
                tone=max(.08,min(1.,rng.lognormvariate(-1.05,.42))) if kind=='cedar' else rng.uniform(.94,1.02)
                silver=rng.random()
                chroma=np.array((1.14,.99,.79))*(1-silver)+np.array((.87,1.02,1.10))*silver if kind=='cedar' else np.ones(3)
                split=rng.random()<.10 if kind=='cedar' else False
                cup=rng.uniform(0,.0018) if kind=='cedar' and rng.random()<.15 else 0
                units.append(dict(kind=kind,row=r,u0_m=float(a),u1_m=float(b),width_m=float(b-a),exposure_m=exposure,butt_offset_m=butt,tone=tone,chroma=chroma.tolist(),split=split,cup_m=cup,nominal_height_m=.3048 if kind=='cement' else .4064))
                for period in (-1.2192,0,1.2192):
                    aa,bb=a+period,b+period;select=(row==r)&(x>=aa)&(x<bb);key=np.minimum(x-aa,bb-x)
                    # Resolvable 7–17 mm fibers/striations survive the 420 px/m ship filter.
                    frequency=(370,860) if kind=='cedar' else (620,1120)
                    grain=np.sin(x*frequency[0]+np.sin(z*38)*.7)+.5*np.sin(x*frequency[1]+z*27)
                    relief=(.007 if kind=='cedar' else .00437)*(1-v)-np.exp(-(key/.0024)**2)*.0025+grain*(.00021 if kind=='cedar' else .00060)
                    # The thin upper end is shaded by the next course's butt.
                    # Contrast belongs within every shingle, not in alternating
                    # nearly black and pale units across the whole elevation.
                    shadow_span=.22 if kind=='cedar' else .030
                    if kind=='cedar':
                        headlap=np.clip((v-.52)/.28,0,1);headlap=headlap*headlap*(3-2*headlap)
                        shade=1-.82*headlap-.48*np.exp(-(key/.0024)**2)
                    else:shade=1-.68*np.exp(-(1-v)/shadow_span)-.85*np.exp(-(key/.0024)**2)
                    if kind=='cement':
                        # Face nails 20 mm above each butt, 25 mm from the ends.
                        nail=np.maximum(np.exp(-((x-(aa+.025))**2+(v*exposure-.020)**2)/.000006),np.exp(-((x-(bb-.025))**2+(v*exposure-.020)**2)/.000006))
                        shade*=1-.72*nail;relief+=.0009*nail
                    else:
                        crack=np.exp(-((x-(aa+(bb-aa)*.38)-.0008*np.sin(z*84))/.0011)**2)*np.clip((.48-v)*5,0,1) if split else 0
                        shade*=1-.70*crack;relief-=.002*crack
                        relief+=cup*np.sin(np.clip((x-aa)/(bb-aa),0,1)*math.pi)*(1-v)**2
                    color[select]=((shade*tone*(1+grain*.024))[:,:,None]*chroma)[select];height[select]=relief[select]
                    ao[select]=np.clip(shade,.25,1)[select]
        colors.append(color);heights.append(height)
    # Image rows run down; UV V runs up. Cedar is the lower half of the atlas.
    rgb=np.concatenate([np.flipud(a) for a in colors[::-1]])
    # Each half is a metric chart, with independent vertical derivative scale.
    normal=[]
    for hi,span in zip(heights,(.762,.5588)):
        dx=(np.roll(hi,-1,1)-np.roll(hi,1,1))/(2*1.2192/size)
        dy=(np.roll(hi,-1,0)-np.roll(hi,1,0))/(2*span/(size//2))
        n=np.stack((-dx,-dy,np.ones_like(hi)),2);n/=np.linalg.norm(n,axis=2,keepdims=True);normal.append(n)
    write_png(folder/'T_CapeShingle_BaseColor.png',np.clip(linear_to_srgb(rgb),0,1))
    write_png(folder/'T_CapeShingle_Normal.png',np.concatenate([np.flipud(a) for a in normal[::-1]])*.5+.5)
    orm=np.zeros((size,size,3));orm[:,:,0]=1;orm[:size//2,:,1]=.92;orm[size//2:,:,1]=.86
    write_png(folder/'T_CapeShingle_ORM.png',orm)
    (folder/'manufacture.json').write_text(json.dumps(dict(units=units),indent=2))

