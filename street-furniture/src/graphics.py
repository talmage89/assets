"""Original fictional graphic source plus source-only finish swatches.

The graphic region becomes the independent 1024 delivery sheet. Flat swatches
are UV staging inputs only; surfaces.py and the GPU bake supply delivered PBR.
"""
import json,sys,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
FONT=find_font('DejaVu Sans','Condensed Bold');SERIF=find_font('DejaVu Serif','Bold')
SWATCHES=dict(Black=(27,32,31),Paint=(38,55,49),Zinc=(139,147,146),Aluminum=(156,162,160),Blue=(13,49,104),Red=(151,27,22),Cream=(192,182,146),Paper=(198,192,166),Rubber=(16,20,19),Inside=(18,23,22),Concrete=(123,125,116),White=(217,219,208),Orange=(184,100,28),Rust=(98,48,24),Flag=(173,25,19),Lamp=(242,227,184))

def text(im,txt,box,fill=(220,220,203),serif=False):
    font=ImageFont.truetype(SERIF if serif else FONT,160);b=font.getbbox(txt)
    mask=Image.new('L',(b[2]-b[0]+3,b[3]-b[1]+3));ImageDraw.Draw(mask).text((-b[0],-b[1]),txt,font=font,fill=255)
    mask=mask.crop(mask.getbbox());mask.thumbnail((round(box[2]-box[0]),round(box[3]-box[1])),Image.Resampling.LANCZOS)
    im.paste(fill,(round((box[0]+box[2]-mask.width)/2),round((box[1]+box[3]-mask.height)/2)),mask)

def cell(key):
    im=Image.new('RGB',(512,512),(214,215,203));d=ImageDraw.Draw(im)
    if key=='transit':
        im.paste((23,68,74),(0,0,512,512));text(im,'RILL TRANSIT',(20,20,492,83));d.rounded_rectangle((105,110,407,355),radius=30,fill=(222,222,206))
        d.rectangle((130,145,380,265),fill=(23,68,74));d.rectangle((150,110,360,130),fill=(23,68,74))
        for x in (145,330):d.ellipse((x,286,x+39,325),fill=(23,68,74));d.rectangle((x,338,x+38,373),fill=(222,222,206))
        text(im,'BUS STOP',(35,402,477,470))
    elif key=='routes':
        d.rectangle((0,0,512,512),fill=(220,219,202));text(im,'12  /  24',(20,30,492,200),(24,62,66));text(im,'TOWN CENTER',(25,245,487,326),(24,62,66));text(im,'VIA LIBRARY',(25,365,487,430),(24,62,66))
    elif key=='schedule':
        text(im,'RILL TRANSIT',(20,20,492,60),(23,68,74));text(im,'WEEKDAY SERVICE',(20,85,492,118),(15,20,19))
        for j in range(10):
            y=150+j*30;d.line((22,y,490,y),fill=(106,112,103),width=1)
            for i in range(4):text(im,f'{6+j:02d}:{(i*15+7)%60:02d}',(25+i*121,y+4,130+i*121,y+22),(30,36,33))
    elif key.startswith('mast'):
        j=int(key[-1]);im.paste(((135,26,23),(26,59,98),(195,183,142))[j],(0,0,512,512))
        text(im,('THE RILL','DAYBREAK','TOWN WEEKLY')[j],(15,105,497,220),serif=True);text(im,('DAILY RECORD','NEWS • LOCAL','INDEPENDENT')[j],(25,264,487,328));text(im,('50 CENTS','75 CENTS','25 CENTS')[j],(25,395,487,453))
    elif key.startswith('paper'):
        j=int(key[-1]);im.paste((204,199,176),(0,0,512,512));text(im,('The Rill','Daybreak','Town Weekly')[j],(15,12,497,78),(23,27,26),True)
        d.line((15,94,497,94),fill=(25,31,30),width=4);text(im,('RIVER WALK OPENS','LIBRARY ADDS HOURS','LOCAL FAIR RETURNS')[j],(20,115,492,188),(28,32,30))
        # Original abstract press illustration: bridge, roofline and trees.
        d.rectangle((18,213,310,357),fill=(126,134,126))
        for x in range(26,300,47):d.rectangle((x,285,x+22,357),fill=(49,62,60))
        d.line((26,280,288,280),fill=(49,62,60),width=6)
        for col in range(4):
            for line in range(19):
                y=376+line*6 if col<3 else 220+line*7;x=20+col*122;d.line((x,y,x+104-(line*17+col*9)%22,y),fill=(77,81,73),width=1)
    elif key=='meter':
        im.paste((206,207,186),(0,0,512,512));d.arc((55,35,457,440),180,360,fill=(23,29,26),width=8)
        for j in range(13):
            t=math.pi+j*math.pi/12;x,y=256+190*math.cos(t),238+190*math.sin(t);xx,yy=256+170*math.cos(t),238+170*math.sin(t);d.line((x,y,xx,yy),fill=(23,29,26),width=4)
        text(im,'MINUTES',(95,240,417,288),(21,25,22));text(im,'25¢ / 15 MIN',(40,362,472,410),(21,25,22));text(im,'2 HOUR LIMIT',(45,432,467,479),(21,25,22))
    elif key=='expired':
        im.paste((155,22,19),(0,0,512,512));text(im,'EXPIRED',(18,165,494,320))
    elif key=='mail':
        im.paste((13,49,104),(0,0,512,512));text(im,'TOWN POST',(22,32,490,118));d.rectangle((40,163,472,277),outline=(205,214,216),width=8)
        d.line((40,163,256,255,472,163),fill=(205,214,216),width=7);text(im,'LETTERS',(25,328,487,395));text(im,'DAILY COLLECTION',(25,437,487,482))
    elif key=='collection':
        text(im,'COLLECTION',(25,30,487,90),(21,30,31));text(im,'MON — SAT',(25,137,487,198),(21,30,31));text(im,'4:30 PM',(30,242,482,350),(21,30,31));text(im,'NO SUNDAY SERVICE',(20,410,492,466),(21,30,31))
    elif key=='advert':
        im.paste((20,65,68),(0,0,512,512));text(im,'TAKE A',(28,30,484,118));text(im,'SLOW DAY',(25,126,487,209));d.ellipse((135,248,377,490),fill=(201,145,50));d.polygon([(90,512),(265,287),(432,512)],fill=(31,87,71));text(im,'RILL RIVER PARK',(20,428,492,481))
    elif key=='recycle':
        im.paste((25,64,62),(0,0,512,512));text(im,'RECYCLE',(25,80,487,164));text(im,'BOTTLES + CANS',(20,350,492,422))
        for j in range(3):
            t=j*math.tau/3;x,y=256+84*math.cos(t),260+84*math.sin(t);d.regular_polygon((x,y,42),3,rotation=120*j+20,fill=(198,211,183))
    elif key=='litter':
        im.paste((31,40,35),(0,0,512,512));text(im,'LITTER',(25,105,487,240));text(im,'KEEP RILL CLEAN',(20,350,492,422))
    elif key=='tag':
        im.paste((38,55,49),(0,0,512,512));d.line([(55,355),(150,135),(170,385),(210,220),(235,370),(330,160),(280,340),(420,260)],fill=(163,151,120),width=13,joint='curve');text(im,'F9',(350,380,482,470),(163,151,120))
    return im

def main():
    out=Path('build');out.mkdir(exist_ok=True);im=Image.new('RGB',(2048,2048));layout={}
    # Left four columns are material-color cells; right four contain graphics.
    for j,(name,col) in enumerate(SWATCHES.items()):
        x=j%4*256;y=j//4*256;im.paste(col,(x,y,x+256,y+256));layout[name]=[x/2048,(2048-y-256)/2048,(x+256)/2048,(2048-y)/2048]
    keys=['transit','routes','schedule','mast0','mast1','mast2','paper0','paper1','paper2','meter','expired','mail','collection','advert','recycle','litter','tag']
    graphics=Image.new('RGB',(1024,2048),(28,38,34))
    for j,key in enumerate(keys):
        x=j%4*256;y=j//4*384
        art=cell(key).resize((240,368),Image.Resampling.LANCZOS);graphics.paste(art,(x+8,y+8));im.paste(art,(1024+x+8,y+8))
        layout[key]=[(1032+x)/2048,(2048-y-376)/2048,(1272+x)/2048,(2048-y-8)/2048]
    im.save(out/'T_StreetFurniture_Checkpoint.png');graphics.save(out/'T_StreetFurniture_GraphicsSource.png');(out/'graphics.json').write_text(json.dumps(layout,indent=2))
if __name__=='__main__':main()
