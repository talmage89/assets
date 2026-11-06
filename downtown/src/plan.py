"""Main Street plan grammar. Pure Python, meters; street front is global -Y.

Lots describe masonry center lines. Equal adjacent lines share a wall, owned
half by each placeable shell. Four regional rule sets, never random style soup.
"""
import copy
import json
import random
from dataclasses import dataclass, asdict
from pathlib import Path

FT = .3048
PROOF = ((411, 'midwest'), (512, 'western'), (613, 'northeast'), (714, 'southern'))
TENANTS = {
 'diner': ('RILL & RYE', 'DINER • COFFEE'),
 'hardware': ('MILLSTONE', 'HARDWARE & SUPPLY'),
 'barber': ('SECOND CHAIR', 'BARBER SHOP'),
 'antiques': ('YESTERDAY HOUSE', 'ANTIQUES • BOOKS'),
 'vacant': ('RETAIL SPACE', 'AVAILABLE FOR LEASE'),
 'pharmacy': ('OAK LEDGER', 'APOTHECARY'),
 'bank': ('UNION LANDING', 'SAVINGS & TRUST'),
 'hotel': ('THE MERIDIAN', 'ROOMS • OFFICES'),
}
REGIONS = {
 'midwest': dict(widths=(22,25,27,30), stories=(2,2,2,3), styles=('italianate','italianate','romanesque','commercial'), walk=14, parking='parallel', depth=(90,100,110), colors=((.27,.085,.043),(.34,.15,.072),(.22,.058,.034),(.46,.36,.22))),
 'western': dict(widths=(20,24,25,28), stories=(1,1,2,2), styles=('vernacular','commercial','vernacular','italianate'), walk=12, parking='angle', depth=(80,90,100), colors=((.29,.135,.075),(.39,.29,.19),(.27,.16,.09),(.44,.40,.31))),
 'northeast': dict(widths=(20,22,24,26), stories=(3,3,3,2), styles=('romanesque','commercial','italianate','commercial'), walk=12, parking='parallel', depth=(100,120,140), colors=((.19,.048,.027),(.29,.077,.038),(.26,.11,.061),(.43,.31,.16))),
 'southern': dict(widths=(23,25,28,30), stories=(2,2,3,2), styles=('italianate','vernacular','commercial','italianate'), walk=16, parking='angle', depth=(90,100,120), colors=((.35,.20,.11),(.39,.34,.25),(.29,.105,.053),(.46,.41,.30))),
}


def generate(seed=411, region='midwest', count=7, overrides=None):
    if region not in REGIONS: raise ValueError('Unknown region')
    if not 4 <= count <= 12: raise ValueError('Choose 4–12 lots')
    rng=random.Random(seed);r=copy.deepcopy(REGIONS[region]);r.update(overrides or {})
    order=['diner','hardware','barber','antiques','vacant','pharmacy'];rng.shuffle(order)
    lots=[];cursor=0
    for i in range(count):
        corner='left' if i==0 else 'right' if i==count-1 else None
        w=(rng.choice((32,36,40)) if corner else rng.choice(r['widths']))*FT
        d=rng.choice(r['depth'])*FT
        n=(3 if region=='northeast' else 2) if corner else rng.choice(r['stories'])
        # One restrained mid-century infill per less-dense block.
        infill=i==count//2 and region in ('midwest','western')
        if infill:n=1
        style='infill' if infill else rng.choice(r['styles'])
        h0=(13 if infill else rng.choice((14,15,16)))*FT
        upper=rng.choice((11,12))*FT
        parapet=rng.choice((2.5,3,3.5))*FT
        roof=h0+(n-1)*upper
        bays=max(2,round((w-.7)/1.95))
        cornice='metal' if style=='italianate' else 'corbel' if style=='romanesque' else 'brick'
        tenant=('bank' if i==0 else 'hotel') if corner else order[(i-1)%len(order)]
        storefront='aluminum' if infill or rng.random()<.35 else 'iron' if region=='southern' or style=='italianate' else 'wood'
        color=rng.choice(r['colors']);painted=rng.random()<.17
        if painted:color=rng.choice(((.39,.38,.31),(.27,.31,.28),(.46,.40,.29)))
        lots.append(dict(id=f'{region.title()}_{seed}_{i+1:02}', index=i,
            width=w, depth=d, x=cursor+w/2, y=d/2, stories=n, floor_first=h0,
            upper=upper, roof=roof, height=roof+parapet, parapet=parapet,
            window_height={'italianate':2.20,'romanesque':2.14}.get(style,1.96),
            style=style, cornice=cornice, corner=corner, chamfer=1.45 if corner else 0,
            bays=bays, tenant=tenant, storefront=storefront, awning=not corner and tenant!='vacant' and (i%3!=2),
            transom='covered' if storefront=='aluminum' and i%2==0 else 'prism' if i%3==1 else 'clear',
            brick=color, painted=painted, fire_escape=n>1 and (i%3==1 or corner=='right'),
            bay_window=region=='northeast' and i==2, gallery=region=='southern' and i in (1,2,3),
            seed=rng.randrange(1000000), date=rng.randrange(1882,1925), infill=infill))
        cursor+=w
    for lot in lots:
        lot['x']-=cursor/2
        lot['date']=1962 if lot['infill'] else 1898 if lot['index']%2==0 else 1906
        i=lot['index']
        lot['neighbor_left']=lots[i-1]['height'] if i else None
        lot['neighbor_right']=lots[i+1]['height'] if i+1<len(lots) else None
    return dict(seed=seed,region=region,count=count,width=cursor,walk=r['walk']*FT,
                parking=r['parking'],road_width=(48 if r['parking']=='angle' else 40)*FT,
                lots=lots,stage='form and construction checkpoint; quick materials')


def validate(p):
    assert p['lots'][0]['corner']=='left' and p['lots'][-1]['corner']=='right'
    for i,b in enumerate(p['lots']):
        assert 20*FT<=b['width']<=40*FT and 80*FT<=b['depth']<=140*FT
        assert 1<=b['stories']<=3 and b['height']>b['roof']
        assert b['bays']>=2 and b['floor_first']>3.9
        if i:assert abs((b['x']-b['width']/2)-(p['lots'][i-1]['x']+p['lots'][i-1]['width']/2))<1e-8
    assert 10*FT<=p['walk']<=16*FT
    return p


def load(seed,region,count=7,path=None):
    if path:
        p=json.loads(Path(path).read_text());return validate(p)
    return validate(generate(seed,region,count))
