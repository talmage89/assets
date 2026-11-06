"""Reserve guarded material-state cells and the independent original graphics."""
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
p=Path('textures/ship');p.mkdir(parents=True,exist_ok=True)
for role,color in [('BaseColor',(190,195,188)),('Normal',(128,128,255)),('ORM',(0,143,0))]:
    path=p/f'T_StreetFurniture_{role}.png';im=Image.open(path).convert('RGB');d=ImageDraw.Draw(im)
    d.rectangle((0,0,2047,43),fill=color)
    if role=='ORM':
        yy,xx=np.mgrid[:44,:1024];u=xx/1023;v=1-yy/43;edge=np.exp(-np.minimum.reduce([u,1-u,v,1-v])/.035);streak=np.exp(-((u-.28)/.018)**2)*np.maximum(0,(.75-v))
        rough=np.uint8(np.clip(38+edge*105+streak*38,0,255));a=np.stack([np.full_like(rough,255),rough,np.zeros_like(rough)],axis=2);im.paste(Image.fromarray(a),(0,0))
    im.save(path)
gfx=Image.open('build/T_StreetFurniture_GraphicsSource.png').convert('RGB').resize((1024,1024),Image.Resampling.LANCZOS)
yy,xx=np.mgrid[:176,:240];u=xx/239;v=1-yy/175;edge=np.exp(-np.minimum.reduce([u,1-u,v,1-v])/.035);deposits=np.maximum(0,(.10-v))*.7
glass=np.ones((176,240,3))*np.array([233,238,231]);glass*=1-(edge*.22+deposits)[:,:,None];gfx.paste(Image.fromarray(np.uint8(glass)),(264,776))
# Glass is pale neutral dielectric. Surface grime/roughness belongs in its
# transmission state, not a gray opaque paint layer.
gfx.save(p/'T_StreetFurniture_Graphics.png')
