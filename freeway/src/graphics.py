"""Original fictional legends, simple state rectangle and MUTCD arrow grammar.

No shield, trademark, photographic texture or regulated FHWA font is copied.
"""
import sys,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
FONT=find_font('DejaVu Sans','Condensed Bold')
PANELS=['advance','exit','through','hollow','speed','mile','chevron','wrong','route','exitSmall']

def generate():
    size=2048;im=Image.new('RGB',(size,size),(8,77,46));d=ImageDraw.Draw(im)
    def text(x,y,word,h,fill=(232,236,222)):
        d.text((x,y),word,font=ImageFont.truetype(FONT,h),fill=fill,anchor='mm')
    for i,name in enumerate(PANELS):
        x=(i%2)*1024;y=(i//2)*400;d.rectangle((x+8,y+8,x+1016,y+392),fill=(8,77,46),outline=(230,234,220),width=5)
        if name in ('advance','exit','hollow'):
            text(x+512,y+72,'EXIT 14' if name!='hollow' else 'EXIT 28',56)
            text(x+512,y+173,'Juniper Avenue' if name!='hollow' else 'Cedar Hollow',81)
            text(x+512,y+285,'1 MILE' if name=='advance' else 'EXIT  '+chr(8599),65)
        elif name=='through':
            d.rounded_rectangle((x+72,y+55,x+252,y+255),18,fill=(232,236,222))
            text(x+162,y+90,'LARK',25,(16,22,20));text(x+162,y+178,'47',107,(16,22,20))
            text(x+618,y+117,'NORTH',58);text(x+610,y+231,'Alder Junction',68)
            # 2009 through lane arrow: down-pointing block arrow, original points.
            for ax in (350,770):d.polygon([(x+ax-20,y+291),(x+ax+20,y+291),(x+ax+20,y+328),(x+ax+55,y+328),(x+ax,y+377),(x+ax-55,y+328),(x+ax-20,y+328)],fill=(232,236,222))
        elif name=='speed':
            d.rectangle((x+8,y+8,x+1016,y+392),fill=(226,226,213),outline=(22,24,22),width=12)
            text(x+512,y+75,'SPEED',66,(18,20,18));text(x+512,y+153,'LIMIT',66,(18,20,18));text(x+512,y+297,'60',160,(18,20,18))
        elif name=='mile':
            text(x+512,y+74,'NORTH',58);text(x+512,y+185,'MILE',68);text(x+512,y+300,'28.4',98)
        elif name=='chevron':
            d.rectangle((x+8,y+8,x+1016,y+392),fill=(236,173,13))
            for xx in range(0,1024,180):d.polygon([(x+xx,y+8),(x+xx+90,y+8),(x+xx+350,y+392),(x+xx+260,y+392)],fill=(18,20,17))
        elif name=='wrong':
            d.rectangle((x+8,y+8,x+1016,y+392),fill=(151,11,8),outline=(232,236,222),width=8)
            text(x+512,y+125,'DO NOT',90);text(x+512,y+276,'ENTER',115)
        elif name=='route':
            d.rectangle((x+8,y+8,x+1016,y+392),fill=(225,228,214),outline=(20,24,21),width=8)
            text(x+512,y+68,'LARK',68,(20,24,21));text(x+512,y+246,'47',220,(20,24,21))
        else:text(x+512,y+200,'EXIT 14',140)
    folder=Path('textures/checkpoint');folder.mkdir(parents=True,exist_ok=True)
    im.save(folder/'T_Freeway_Signs.png')
    Path('build/sign-charts.json').write_text(json.dumps({name:rect(name) for name in PANELS},indent=2))
    # Reuse the fence family's original analytic wire field. This small form
    # tile is temporary; look-dev will reference the canonical fence atlas.
    import importlib.util,numpy as np
    folder_src=Path(__file__).resolve().parents[2]/'fences/chain-link/src'
    sys.path.insert(0,str(folder_src))
    spec=importlib.util.spec_from_file_location('native_fence_tile',folder_src/'mesh_tile.py')
    tile=importlib.util.module_from_spec(spec);spec.loader.exec_module(tile)
    arrays=tile.tile(256,256,tile.TILE,tile.field)
    for channel,arr in zip(('BaseColor','Normal','ORM'),arrays):
        Image.fromarray(np.uint8(np.round(np.clip(np.flipud(arr),0,1)*255))).save(folder/f'T_FreewayFenceForm_{channel}.png')
    Path('build/fence-form.json').write_text(json.dumps(dict(source='fences/chain-link/src/mesh_tile.py',tile_m=tile.TILE,wire_m=tile.WIRE,scope='Reused original procedural field, temporary 256 form maps'),indent=2))

def rect(name):
    i=PANELS.index(name);x=(i%2)*1024;y=(i//2)*400
    return ((x+8)/2048,1-(y+392)/2048,(x+1016)/2048,1-(y+8)/2048)

if __name__=='__main__':generate()
