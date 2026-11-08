"""Original fictional legends, simple state rectangle and MUTCD arrow grammar.

No shield, trademark, photographic texture or regulated FHWA font is copied.
"""
import sys,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
FONT=find_font('DejaVu Sans','Condensed Bold')
PANELS=['through_south','exit','through','gore_exit','speed','mile','chevron','wrong','mile_south','exitSmall','wrong_way','entrance','route']

def generate():
    size=2048;im=Image.new('RGB',(size,2800),(14,108,76));d=ImageDraw.Draw(im)
    def text(x,y,word,h,fill=(232,236,222)):
        d.text((x,y),word,font=ImageFont.truetype(FONT,h),fill=fill,anchor='mm')
    for i,name in enumerate(PANELS):
        x=(i%2)*1024;y=(i//2)*400;d.rectangle((x+8,y+8,x+1016,y+392),fill=(14,108,76),outline=(230,234,220),width=5)
        if name in ('advance','exit','hollow'):
            text(x+512,y+72,'EXIT 14' if name!='hollow' else 'EXIT 28',56)
            text(x+512,y+173,'Juniper Avenue' if name!='hollow' else 'Cedar Hollow',81)
            text(x+512,y+285,'1 MILE' if name=='advance' else 'EXIT  '+chr(8599),65)
        elif name in ('through','through_south'):
            d.rounded_rectangle((x+72,y+55,x+252,y+255),18,fill=(232,236,222))
            text(x+162,y+90,'LARK',25,(16,22,20));text(x+162,y+178,'47',107,(16,22,20))
            text(x+618,y+117,'SOUTH' if name=='through_south' else 'NORTH',58)
            text(x+610,y+231,'Cedar Hollow' if name=='through_south' else 'Alder Junction',68)
            # 2009 through lane arrow: down-pointing block arrow, original points.
            for ax in (244,779):d.polygon([(x+ax-20,y+291),(x+ax+20,y+291),(x+ax+20,y+328),(x+ax+55,y+328),(x+ax,y+377),(x+ax-55,y+328),(x+ax-20,y+328)],fill=(232,236,222))
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
    # Regulatory/mile/gore charts are rasterized at their *physical aspect*
    # before packing; their square or tall panel must not squeeze the letters.
    def packed(name,canvas):
        i=PANELS.index(name);x=(i%2)*1024;y=(i//2)*400
        im.paste(canvas.resize((1008,384),Image.Resampling.LANCZOS),(x+8,y+8))
    def label(canvas,word,xy,size,color):
        ImageDraw.Draw(canvas).text(xy,word,font=ImageFont.truetype(FONT,size),fill=color,anchor='mm')
    card=Image.new('RGB',(300,400),(226,226,213));dd=ImageDraw.Draw(card);dd.rounded_rectangle((4,4,295,395),12,outline=(18,20,18),width=7)
    for word,yy,size in [('SPEED',64,45),('LIMIT',126,45),('60',280,155)]:label(card,word,(150,yy),size,(18,20,18))
    packed('speed',card)
    for name,direction in [('mile','NORTH'),('mile_south','SOUTH')]:
        card=Image.new('RGB',(100,400),(14,108,76));dd=ImageDraw.Draw(card);dd.rounded_rectangle((3,3,96,396),5,outline=(232,236,222),width=2)
        for word,yy,size in [(direction,34,17),('MILE',105,24),('28',206,59),('.4',310,48)]:label(card,word,(50,yy),size,(232,236,222))
        packed(name,card)
    card=Image.new('RGB',(400,400),(232,236,222));dd=ImageDraw.Draw(card);dd.ellipse((12,12,388,388),fill=(151,11,8));dd.rectangle((60,175,340,225),fill=(232,236,222))
    label(card,'DO NOT',(200,106),57,(232,236,222));label(card,'ENTER',(200,298),71,(232,236,222));packed('wrong',card)
    card=Image.new('RGB',(400,320),(14,108,76));dd=ImageDraw.Draw(card);dd.rounded_rectangle((4,4,396,316),12,outline=(232,236,222),width=5)
    label(card,'EXIT',(200,75),79,(232,236,222));dd.line([(128,254),(285,143)],fill=(232,236,222),width=27);dd.polygon([(228,134),(309,126),(296,205)],fill=(232,236,222));packed('gore_exit',card)
    card=Image.new('RGB',(640,400),(155,13,11));dd=ImageDraw.Draw(card);dd.rounded_rectangle((5,5,634,394),16,outline=(232,236,222),width=9)
    label(card,'WRONG',(320,125),105,(232,236,222));label(card,'WAY',(320,285),105,(232,236,222));packed('wrong_way',card)
    card=Image.new('RGB',(640,400),(14,108,76));dd=ImageDraw.Draw(card);dd.rounded_rectangle((5,5,634,394),14,outline=(232,236,222),width=8)
    label(card,'FREEWAY',(320,115),88,(232,236,222));label(card,'ENTRANCE',(320,255),82,(232,236,222));packed('entrance',card)
    card=Image.new('RGB',(320,400),(232,236,222));dd=ImageDraw.Draw(card);dd.rounded_rectangle((5,5,314,394),18,outline=(18,22,20),width=8)
    label(card,'LARK',(160,68),52,(18,22,20));label(card,'47',(160,247),190,(18,22,20));packed('route',card)
    # Guarded 4x4 charts; physical-aspect canvases precede storage packing.
    atlas=Image.new('RGB',(2048,2048),(14,108,76))
    for i,name in enumerate(PANELS):
        x=i%2*1024;y=i//2*400
        atlas.paste(im.crop((x+8,y+8,x+1016,y+392)).resize((496,496),Image.Resampling.LANCZOS),(i%4*512+8,i//4*512+8))
    im=atlas
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
    i=PANELS.index(name);x=(i%4)*512;y=(i//4)*512
    return ((x+8)/2048,1-(y+504)/2048,(x+504)/2048,1-(y+8)/2048)

if __name__=='__main__':generate()
