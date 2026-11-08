"""Additive Ground parking graphics sheet; never modifies Ground's atlas.

Form colors and crisp signs only. Look-dev will supply repaints/ghosts, sealant
loss and placement-owned tire/oil decals from their actual causes.
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from kit.fonts import find_font


def generate(folder=Path('textures/checkpoint'),extra=False):
    size=2048;im=Image.new('RGBA',(size,size));d=ImageDraw.Draw(im);layout={}
    labels=['ALDER QUAY','MUNICIPAL PARKING','BELLWETHER COMMONS','PUBLIC PARKING','ENTRY','EXIT','PAY HERE','FULL',
            'CLEARANCE  8 FT 2 IN','UPPER LEVELS  7 FT','COMPACT','STAIR / LIFT','VAN ACCESSIBLE','RESERVED',
            'LEVEL 1','LEVEL 2','LEVEL 3','LEVEL 4','LEVEL 5','ONE WAY','KEEP RIGHT','NO PEDESTRIANS','♿']
    word_count=len(labels)
    labels += [f'{n:03d}' for n in range(1,121)]
    if extra:labels += ['OPEN  6 AM - MIDNIGHT','PAY BEFORE RETURNING','STAIRS','ELEVATOR','PARKING','NO ENTRY','2 HOUR PARKING','METERED PARKING']
    cols=8;cw=256;ch=100
    for i,string in enumerate(labels):
        x=(i%cols)*cw;y=(i//cols)*ch;rect=(x+4,y+4,x+cw-4,y+ch-4)
        bg=(24,52,62,255) if i<word_count and string!='♿' else (0,0,0,0);fg=(235,230,204,255)
        if extra and string.startswith('LEVEL '):bg=[(43,78,82,255),(126,46,29,255),(102,87,31,255),(39,76,56,255),(71,52,84,255)][int(string[-1])-1]
        if extra and i>=word_count+120:bg=(31,48,47,255)
        if i==7:fg=(50,13,8,255);bg=(15,17,16,255)
        d.rectangle(rect,fill=bg);sz=48
        font=ImageFont.truetype(find_font('DejaVu Sans','Bold'),sz)
        while d.textbbox((0,0),string,font=font)[2]>cw-22:
            sz-=1;font=ImageFont.truetype(find_font('DejaVu Sans','Bold'),sz)
        d.text((x+cw/2,y+ch/2),string,fill=fg,font=font,anchor='mm')
        sample=rect
        if string in ('ALDER QUAY','BELLWETHER COMMONS'):
            bounds=d.textbbox((x+cw/2,y+ch/2),string,font=font,anchor='mm')
            sample=(rect[0],bounds[1]-6,rect[2],bounds[3]+6)
        if string=='♿':
            bounds=d.textbbox((x+cw/2,y+ch/2),string,font=font,anchor='mm')
            sample=(bounds[0]-6,bounds[1]-6,bounds[2]+6,bounds[3]+6)
        layout[string]=[sample[0]/size,1-sample[3]/size,sample[2]/size,1-sample[1]/size]
    Path('build').mkdir(exist_ok=True);folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    im.save(folder/'T_GroundParkingTrim_BaseColor.png');dest=folder/'layout.json' if extra else Path('build/graphics.json');dest.write_text(json.dumps(layout,indent=2))
    return layout
