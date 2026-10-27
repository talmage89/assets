"""Bounded 1955–75 one-story ranch grammar; dimensions are authored in meters.

The total width includes the garage/carport. A step in its eave avoids
coincident roof skins; the exact family envelope resolves their intersection.
"""
import copy
import math
import random
from plan import Block,FT,merge,wall_frame

PROOF_SEEDS=(11,12,13,14,15,16)
PALETTES=(
 dict(name='red brick / ivory / olive',siding=(.34,.31,.23),trim=(.58,.55,.46),shutter=(.065,.078,.043),door=(.12,.15,.062)),
 dict(name='buff brick / walnut',siding=(.24,.20,.14),trim=(.52,.48,.39),shutter=(.07,.052,.035),door=(.115,.055,.022)),
 dict(name='brown brick / warm white / red',siding=(.58,.55,.47),trim=(.60,.57,.49),shutter=(.054,.05,.038),door=(.22,.045,.025)),
 dict(name='tan brick / moss',siding=(.20,.25,.17),trim=(.51,.49,.40),shutter=(.045,.058,.035),door=(.065,.095,.047)),
 dict(name='red brown / putty / umber',siding=(.34,.32,.26),trim=(.57,.54,.46),shutter=(.07,.06,.041),door=(.13,.066,.032)),
 dict(name='red brick / charcoal / ochre',siding=(.19,.20,.17),trim=(.48,.46,.39),shutter=(.036,.04,.032),door=(.25,.145,.035)),
)


def generate(seed,overrides=None):
 r=random.Random(seed)
 # All choices use a local RNG; the colonial sequence never consumes these.
 total=r.choice((48,52,56,60))*FT
 cars=r.choice((1,2));gw=(14 if cars==1 else 22)*FT
 total=max(total,gw+32*FT)
 spec=dict(type='ranch',main=dict(width=total-gw,depth=r.choice((24,26,28))*FT,stories=1,
             roof=r.choice(('gable','hip')),pitch=r.choice((3,4,5))/12,overhang=r.choice((18,24,30))*.0254),
    garage=dict(width=gw,depth=0,projection=r.choice((0,2))*FT,
                side=r.choice(('left','right')),stories=1,cars=cars,kind='carport' if seed%5==0 else 'garage',
                entry='side' if seed%3==0 else 'front',roof_step=.1524),
    foundation='crawlspace' if seed%4==0 else 'slab',floor=.6096 if seed%4==0 else r.choice((8,12,16))*.0254,
    wall_mix=('full_brick','wainscot','front_brick')[seed%3],brick_color=('red','buff','red_brown','tan')[seed%4],
    battens=bool(seed%2),shutters=bool(seed%3==1),chimney=('ridge','gable',None)[0 if seed%4 in (0,1) else (1 if seed%4==2 else 2)],
    window_update={11:'wood_storm',12:'vinyl',13:'bronze',14:'vinyl',15:'vinyl',16:'vinyl'}.get(seed,('wood_storm','vinyl','bronze','vinyl')[seed%4]),roof_age='newer' if seed%3==0 else 'tired',
    aerial='dish' if seed%6==0 else ('antenna' if seed%6==1 else None),
    porch='hip',rear_landing='patio',fireplace=False,shingle_color=('warm_charcoal','weathered_wood','dark_brown')[seed%3],
    colors=copy.deepcopy(PALETTES[seed%6]))
 if seed==15:spec['shingle_color']='weathered_wood'
 spec['main']['overhang']=(.5292 if seed%6==5 else (27 if seed%3==1 else 30)*.0254)
 if overrides:merge(spec,copy.deepcopy(overrides))
 m,g=spec['main'],spec['garage'];floor=spec['floor']
 assert spec['type']=='ranch' and m['stories']==g['stories']==1
 assert 44*FT-1e-8<=m['width']+g['width']<=60*FT+1e-8
 assert 24*FT<=m['depth']<=30*FT and m['width']>=30*FT
 assert m['roof'] in ('hip','gable') and 3/12<=m['pitch']<=5/12
 assert 18*.0254<=m['overhang']<=30*.0254
 assert g['side'] in ('left','right') and g['kind'] in ('garage','carport') and g['entry'] in ('front','side')
 assert g['cars'] in (1,2) and (14 if g['cars']==1 else 22)*FT<=g['width']<=24*FT
 assert 0<=g['projection']<=2*FT
 if not overrides or 'garage' not in overrides or 'depth' not in overrides['garage']:
  g['depth']=m['depth'] if g['projection']==0 else min(24*FT,m['depth'])
 assert 20*FT<=g['depth']<=30*FT and max(m['depth'],g['depth']+g['projection'])<=30*FT+1e-8
 assert .12<=g['roof_step']<=.25
 assert spec['foundation'] in ('slab','crawlspace')
 assert (.2032<=floor<=.4064) if spec['foundation']=='slab' else abs(floor-.6096)<1e-8
 assert spec['wall_mix'] in ('full_brick','wainscot','front_brick')
 assert spec['brick_color'] in ('red','red_brown','buff','tan')
 assert spec['window_update'] in ('mixed','wood_storm','bronze','aluminum','vinyl') and spec['chimney'] in ('ridge','gable',None)
 assert all(isinstance(spec[k],bool) for k in ('battens','shutters'))
 assert spec['shingle_color'] in ('warm_charcoal','weathered_wood','dark_brown')
 assert spec['roof_age'] in ('newer','tired') and spec['aerial'] in ('dish','antenna',None)
 assert all(len(spec['colors'][key])==3 and all(math.isfinite(v) and 0<=v<=.70 for v in spec['colors'][key]) for key in ('siding','trim','shutter','door'))
 if not overrides or 'garage' not in overrides or 'depth' not in overrides['garage']:
  g['depth']=m['depth'] if g['projection']==0 else min(24*FT,m['depth'])
 plate=floor+8*FT;eave=plate+.254
 main=Block('Main',-m['width']/2,m['width']/2,-m['depth']/2,m['depth']/2,0,floor,plate,eave,m['roof'],m['pitch'],'X',m['overhang'],1,0,plate)
 x0=main.x1
 if g['side']=='left':x0=main.x0-g['width']
 garage=Block('Garage',x0,x0+g['width'],main.y0-g['projection'],main.y0-g['projection']+g['depth'],0,.1016,
              plate-g['roof_step'],eave-g['roof_step'], 'gable',m['pitch'],'Y',m['overhang'],1,0,plate-g['roof_step'])
 # Total wall envelope centered at grade, patio/roof overhangs excluded.
 cx=(min(main.x0,garage.x0)+max(main.x1,garage.x1))/2
 cy=(min(main.y0,garage.y0)+max(main.y1,garage.y1))/2
 for b in (main,garage):b.x0-=cx;b.x1-=cx;b.y0-=cy;b.y1-=cy
 # Living room next to garage, bedrooms toward the opposite end.
 door_u=main.width*(.58 if g['side']=='right' else .42);door_x=main.x0+door_u
 porch=Block('Porch',door_x-1.02,door_x+1.02,main.y0-1.25,main.y0-.192,0,floor-.028,plate-.015,eave-.04,'hip',.25,'X',.18,1,0,plate)
 spec['cladding']={b.name:{f:('veneer' if spec['wall_mix']=='full_brick' or f=='front' else 'siding') for f in ('front','back','left','right')} for b in (main,garage)}
 face=('right' if g['side']=='right' else 'left') if g['entry']=='side' else 'front'
 apron=(garage.x1+.13 if g['side']=='right' else garage.x0-.13,garage.cy,.1016) if face!='front' else (garage.cx,garage.y0-.13,.1016)
 envelope=None
 if g['projection']==0 and abs(g['depth']-m['depth'])<1e-7:
  garage.roof=main.roof;garage.ridge_axis='X';garage.eave=main.eave;garage.plate=main.plate;garage.first_plate=main.plate
  envelope=copy.copy(main);envelope.x0=min(main.x0,garage.x0);envelope.x1=max(main.x1,garage.x1)
 return dict(seed=seed,spec=spec,blocks=[main,garage],porch=porch,door_x=door_x,roof_envelope=envelope,
   floor_levels=dict(Main=[floor],Garage=[garage.floor]),
   sockets=dict(FrontThreshold=(door_x,main.y0-.10,floor),Walk=(door_x,porch.y0-.3048*math.ceil(porch.floor/.18),0),GarageApron=apron))


def openings(plan):
 result=[];m,g=plan['blocks'];s=plan['spec'];right=s['garage']['side']=='right'
 def add(b,face,u,z,w,h,kind='window',role='bedroom',shutters=False,**kw):
  result.append(dict(id=f'{b.name}_{face}_{len(result):02}',block=b.name,face=face,u=u,z=z,w=w,h=h,kind=kind,role=role,shutters=shutters,**kw))
 living=m.width*(.84 if right else .16)
 # Picture unit: fixed center and two operable flanking sashes in one opening.
 add(m,'front',living,m.floor+.69,2.7432,1.3716,role='living picture',style='picture',system=s['window_update'] if s['window_update'] in ('wood_storm','bronze','aluminum') else 'vinyl')
 # Bedrooms are high enough for furniture, without crossing the ceiling header.
 for i,f in enumerate((.13,.385) if right else (.615,.87)):
  add(m,'front',m.width*f,m.floor+1.016,1.067,1.016,shutters=s['shutters'],system=('aluminum' if i==0 else 'vinyl') if s['window_update']=='mixed' else s['window_update'])
 add(m,'front',plan['door_x']-m.x0,m.floor,.9144,2.032,'door','entry')
 # Kitchen/utility/patio: room-driven asymmetry, no regular rear grid.
 for u,w,h,sill,role in ((.14,1.2192,1.016,1.016,'kitchen sink'),(.78,1.2192,1.016,1.016,'bedroom'),(.95,.6096,.4064,1.6256,'bathroom')):
  add(m,'back',m.width*u,m.floor+sill,w,h,role=role,system=s['window_update'] if s['window_update']!='mixed' else 'aluminum')
 add(m,'back',m.width*.46,m.floor,1.8288,2.032,'patio','kitchen patio')
 outer='left' if right else 'right'
 for f,role in ((.20,'bedroom'),(.78,'bedroom')):
  add(m,outer,m.depth*f,m.floor+1.016,1.2192,1.016,role=role,system=s['window_update'] if s['window_update'] in ('wood_storm','bronze','aluminum') else 'vinyl')
 # Bathroom 2 on the end wall, clear of the broad gable chimney.
 add(m,outer,m.depth*.44,m.floor+1.6256,.6096,.4064,role='bathroom',system=s['window_update'] if s['window_update']!='mixed' else 'aluminum')
 if s['garage']['kind']=='garage':
  face=('right' if right else 'left') if s['garage']['entry']=='side' else 'front'
  length=g.depth if face!='front' else g.width
  add(g,face,length/2,g.floor,4.8768 if s['garage']['cars']==2 else 2.7432,2.1336,'garage','closed sectional')
  add(g,'back',g.width*.70,g.floor,.8636,2.032,'service','garage service')
  add(g,'back',g.width*.22,1.45,.76,.61,system='aluminum',role='garage workshop')
 return result
