"""Original dimensioned plan reservations; no photographed/traced linework."""
from pathlib import Path
import sys
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from plans import garden,row,complex_plan,transform
from kit.fonts import find_font


def make():
    out=Path('renders/plans');out.mkdir(parents=True,exist_ok=True)
    fontpath=str(find_font('DejaVu Sans','Book'));font=ImageFont.truetype(fontpath,20);small=ImageFont.truetype(fontpath,16);title=ImageFont.truetype(fontpath,27)
    im=Image.new('RGB',(1600,2070),'#efeee7');dr=ImageDraw.Draw(im)
    colors=('#ccd4c0','#d7cdb7','#c6d3d5','#d9d7c9')
    def panel(x0,y0,name,w,d,rooms):
        scale=min(610/w,430/d);dr.text((x0,y0),name,font=title,fill='#273028');dr.text((x0,y0+37),f'{w:.4f} × {d:.4f} m gross',font=font,fill='#39413b')
        y0+=82
        for j,r in enumerate(rooms):
            x1,x2,y1,y2=r['rect'];box=(x0+x1*scale,y0+y1*scale,x0+x2*scale,y0+y2*scale)
            dr.rectangle(box,fill=colors[j%len(colors)],outline='#29362d',width=3)
            text=r['name'];parts=text.split(' / ')
            dr.multiline_text((box[0]+5,box[1]+6),'\n'.join(parts),font=small,fill='#29362d',spacing=3)
        dr.text((x0,y0+d*scale+13),'Front facade at upper edge',font=small,fill='#29362d')
    for x,seed,name in ((55,301,'Central hall / two-bedroom unit'),(840,304,'Exterior gallery / one-bedroom unit')):
        p=garden(seed);panel(x,40,name,p['unit_width'],p['unit_depth'],p['unit_rooms'])
    r=row(401);w,d=r['width'],r['depth']
    downstairs=[dict(name=n,rect=(a*w,b*w,c*d,e*d)) for n,a,b,c,e in (('Living',0,1,0,.35),('Stair / hall',0,.4,.35,.68),('Kitchen / WC',.4,1,.35,.68),('Dining',0,1,.68,1))]
    upstairs=[dict(name=n,rect=(a*w,b*w,c*d,e*d)) for n,a,b,c,e in (('Bedroom 1',0,1,0,.35),('Stair / hall',0,.4,.35,.68),('Bath / storage',.4,1,.35,.68),('Bedroom 2',0,1,.68,1))]
    panel(55,710,'20 ft townhouse / ground',w,d,downstairs);panel(840,710,'20 ft townhouse / upper',w,d,upstairs)
    r=row(403);w,d=r['width'],r['depth']
    rooms=[dict(name=n,rect=(a*w,b*w,c*d,e*d)) for n,a,b,c,e in (('Garage',0,.64,0,.48),('Entry / stair',.64,1,0,.48),('Kitchen / WC',0,.44,.48,.72),('Living / dining',.44,1,.48,1),('Utility',0,.44,.72,1))]
    upper=[dict(name=n,rect=(a*w,b*w,c*d,e*d)) for n,a,b,c,e in (('Bedroom 1',0,.64,0,.37),('Stair / hall',.64,1,0,.68),('Bath / storage',0,.64,.37,.68),('Bedroom 2',0,1,.68,1))]
    panel(55,1390,'24 ft garage townhouse / ground',w,d,rooms);panel(840,1390,'24 ft garage townhouse / upper',w,d,upper)
    dr.text((55,2020),'Original schematic reservations; projecting garage bay is additional. Mesh has common circulation and shallow window rooms, not full interiors.',font=small,fill='#29362d')
    im.save(out/'floor-plans.jpg',quality=94,optimize=True)
    # The footprint diagrams use the exact seeded wall polygons, placements,
    # private aisle and unit-party lines; trees/cars are presentation markers.
    im=Image.new('RGB',(1600,1200),'#efeee7');dr=ImageDraw.Draw(im)
    for k,seed in enumerate((301,302,303,304)):
        p=complex_plan(seed);W,D=p['lot'];xx=45+(k%2)*800;yy=40+(k//2)*570;s=min(700/W,470/D)
        def q(v):return (xx+350+v[0]*s,yy+65+D*s/2-v[1]*s)
        dr.text((xx,yy),f'{p["name"]} / {sum(p["building"]["units"] for _ in p["buildings"])} units',font=title,fill='#273028')
        dr.rectangle((*q((-W/2,D/2)),*q((W/2,-D/2))),fill='#c3cdb7',outline='#29362d',width=2)
        dr.rectangle((*q((-W/2+4,9.54)),*q((W/2-4,-9.54))),fill='#858680')
        for b in p['buildings']:
            for poly in p['building']['footprint_polygons']:
                dr.polygon([q(transform(v,b['origin'],b['yaw'])) for v in poly],fill='#bca990',outline='#29362d',width=2)
        dr.text((xx,yy+535),f'{W:.0f} × {D:.0f} m parcel; buildings {p["building"]["units"]} units each',font=font,fill='#29362d')
    im.save(out/'complex-plans.jpg',quality=94,optimize=True)


if __name__=='__main__':make()
