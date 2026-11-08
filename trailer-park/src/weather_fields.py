"""Original gravity runoff, protected damp and ground-splash atlas masks."""
import numpy as np
from PIL import Image


def field(kind,w,h,seed):
    rng=np.random.default_rng(seed);yy,xx=np.mgrid[:h,:w];u=(xx+.5)/w;v=1-(yy+.5)/h
    def noise(cols,rows):
        grid=rng.random((rows,cols),dtype=np.float32)
        return np.clip(np.asarray(Image.fromarray(grid).resize((w,h),Image.Resampling.BICUBIC)),0,1)
    fine=rng.random((h,w));broad=noise(11,9);medium=noise(43,37)
    if kind=='Rust':
        # Four different fastener histories. Filaments widen below the head,
        # then narrow under gravity; coarse breaks leave exposed paint.
        cell=np.floor(u*4);s=(u*4)%1;t=1-v;length=.72+.065*cell
        center=.5+.035*np.sin(t*(23+cell*3)+cell)+.018*np.sin(t*71+cell)
        width=(.075+.07*np.exp(-((t-.16)/.17)**2))*np.maximum(.05,1-t/length)**.64
        core=np.exp(-((s-center)/np.maximum(width,.006))**4)
        filaments=np.exp(-((s-center-.09*np.sin(t*7+cell))/.018)**2)*.22
        mask=(core+filaments)*np.clip((length-t)/.10,0,1)*np.clip(t/.018,0,1)
        mask*=.55+.45*fine;mask*=.58+.42*broad
        color=np.stack((.20+.09*fine,.055+.035*broad,.012+.012*fine),axis=-1)
        rough=.87+.09*fine;relief=.5-.009*mask+.012*fine*mask
    elif kind=='Damp':
        # A trapped-water fan below a hood/window corner, with downward
        # tendrils and air-dried holes, never an all-over noise wash.
        t=1-v;center=.47+.14*(noise(1,17)-.5)
        width=.08+.30*t
        fan=np.exp(-((u-center)/width)**4)*np.clip((.96-t)/.17,0,1)*np.clip(t/.08,0,1)
        colonies=np.clip((broad-.25)*2.2,0,1)
        mask=fan*colonies*(.45+.55*medium)*(.55+.45*fine)
        color=np.stack((.026+.018*fine,.040+.024*broad,.016+.010*fine),axis=-1)
        rough=.94+.04*fine;relief=.5+.005*mask*fine
    else:
        # Soil reaches 6–12in up a skirt. Splash lobes and small upward drops
        # start at grade; the irregular upper boundary stays discontinuous.
        height=.10+.12*noise(13,1)
        for j in range(9):
            x=rng.uniform(.02,.98);reach=rng.uniform(.18,.57);spread=rng.uniform(.025,.13)
            height=np.maximum(height,reach*np.exp(-((u-x)/spread)**4))
        mask=np.clip((height-v+.045*(medium-.5))/.08,0,1)*(.25+.75*broad)*(.6+.4*fine)
        for j in range(55):
            x=rng.uniform(.03,.97);z=.12+.78*rng.beta(1.6,6);r=rng.uniform(.002,.008)
            mask=np.maximum(mask,.48*np.exp(-((u-x)/r)**2-((v-z)/(r*1.9))**2))
        color=np.stack((.075+.035*fine,.054+.025*broad,.026+.014*fine),axis=-1)
        rough=.94+.04*fine;relief=.5+.016*mask*fine
    # Empty borders protect neighboring opaque cells and minified alpha.
    border=np.clip(np.minimum.reduce((u,1-u,v,1-v))/.026,0,1)
    alpha=np.clip(mask*border,0,.96)
    return color,np.stack((np.ones_like(u),rough,np.zeros_like(u)),axis=-1),relief,alpha
