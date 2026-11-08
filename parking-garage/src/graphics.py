"""Additive Ground parking graphics sheet; never modifies Ground's atlas.

Form colors and crisp signs only. Look-dev will supply repaints/ghosts, sealant
loss and placement-owned tire/oil decals from their actual causes.
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from kit.fonts import find_font


def generate(folder=Path('textures/checkpoint'),extra=False,extra_levels=7):
    size=2048;im=Image.new('RGBA',(size,size));d=ImageDraw.Draw(im);layout={}
    labels=['ALDER QUAY','MUNICIPAL PARKING','BELLWETHER COMMONS','PUBLIC PARKING','ENTRY','EXIT','PAY HERE','FULL',
            'CLEARANCE  8 FT 2 IN','UPPER LEVELS  7 FT','COMPACT','STAIR / LIFT','VAN ACCESSIBLE','RESERVED',
            'LEVEL 1','LEVEL 2','LEVEL 3','LEVEL 4','LEVEL 5','ONE WAY','KEEP RIGHT','NO PEDESTRIANS','♿']
    word_count=len(labels)
    labels += [f'{n:03d}' for n in range(1,121)]
    if extra:labels += ['OPEN  6 AM - MIDNIGHT','PAY BEFORE RETURNING','STAIRS','ELEVATOR','PARKING','NO ENTRY','2 HOUR PARKING','METERED PARKING']+[f'TOWER {n}' for n in range(1,6)]+['LEVEL 6','LEVEL 7','TOWER 6','TOWER 7']
    if extra:labels += [f'{key} {n}' for n in range(8,extra_levels+1) for key in ('LEVEL','TOWER')]
    level_colors=[(43,78,82,255),(126,46,29,255),(102,87,31,255),(39,76,56,255),(71,52,84,255),(32,80,75,255),(68,73,74,255),(90,61,36,255)]
    cols=8;cw=256;ch=96 if extra_levels>7 else 100
    for i,string in enumerate(labels):
        x=(i%cols)*cw;y=(i//cols)*ch;rect=(x+4,y+4,x+cw-4,y+ch-4)
        bg=(24,52,62,255) if i<word_count and string!='♿' else (0,0,0,0);fg=(235,230,204,255)
        if extra and i>=word_count+120:bg=(31,48,47,255)
        if extra and string.startswith('LEVEL '):bg=level_colors[int(string[-1])-1]
        if i==7:fg=(50,13,8,255);bg=(15,17,16,255)
        d.rectangle(rect,fill=bg);sz=48
        font=ImageFont.truetype(find_font('DejaVu Sans','Bold'),sz)
        while d.textbbox((0,0),string,font=font)[2]>cw-22:
            sz-=1;font=ImageFont.truetype(find_font('DejaVu Sans','Bold'),sz)
        d.text((x+cw/2,y+ch/2),string,fill=fg,font=font,anchor='mm')
        sample=rect
        if extra and (string.startswith('TOWER ') or string=='2 HOUR PARKING'):
            sample=(x+82,y+4,x+174,y+96)
            if string.startswith('TOWER '):
                color=level_colors[int(string[-1])-1]
                d.rectangle(rect,fill=color)
                d.text((x+128,y+20),'LEVEL',fill=fg,font=ImageFont.truetype(find_font('DejaVu Sans','Bold'),14),anchor='mm')
                d.text((x+128,y+63),string[-1],fill=fg,font=ImageFont.truetype(find_font('DejaVu Sans','Bold'),55),anchor='mm')
            else:
                d.rectangle(rect,fill=(230,228,212,255));d.rectangle(sample,outline=(35,75,51,255),width=2)
                for yy,line_text,font_size in ((23,'2 HOUR',15),(47,'PARKING',15),(74,'8 AM - 6 PM',9)):
                    d.text((x+128,y+yy),line_text,fill=(35,75,51,255),font=ImageFont.truetype(find_font('DejaVu Sans','Bold'),font_size),anchor='mm')
        if string in ('ALDER QUAY','BELLWETHER COMMONS') or (extra and (i<word_count or string.startswith('LEVEL ') or string in ('OPEN  6 AM - MIDNIGHT','STAIRS','ELEVATOR','PARKING','NO ENTRY','METERED PARKING','PAY BEFORE RETURNING'))):
            bounds=d.textbbox((x+cw/2,y+ch/2),string,font=font,anchor='mm')
            sample=(rect[0],bounds[1]-6,rect[2],bounds[3]+6)
        if string=='♿':
            bounds=d.textbbox((x+cw/2,y+ch/2),string,font=font,anchor='mm')
            sample=(bounds[0]-6,bounds[1]-6,bounds[2]+6,bounds[3]+6)
        layout[string]=[sample[0]/size,1-sample[3]/size,sample[2]/size,1-sample[1]/size]
        assert all(0<=v<=1 for v in layout[string]),(string,layout[string])
    Path('build').mkdir(exist_ok=True);folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    im.save(folder/'T_GroundParkingTrim_BaseColor.png');dest=folder/'layout.json' if extra else Path('build/graphics.json');dest.write_text(json.dumps(layout,indent=2))
    return layout
