"""2009 MUTCD / 2004 SHS + 2012 supplement form checkpoint, inches.

No existing StreetSigns input is imported or changed. Layout dimensions are
explicit; the open DejaVu alphabet is fitted to SHS line widths/cap heights.
"""
INCH = .0254
SIGNS = {}

def add(key, code, w, h, shape='rect', color='white', radius=1.5, border=.375, inset=.375, **kw):
    SIGNS[key] = dict(code=code,w=w,h=h,shape=shape,color=color,radius=radius,border=border,inset=inset,**kw)

for value in (20,25,30,35,45):
    add('speed'+str(value),'R2-1',24,30,value=value,series='E',caps=4,digits=10,page='2012 R2-1')
for value in (30,45):
    add('speed'+str(value)+'large','R2-1',30,36,value=value,series='E',caps=5,digits=12,border=.5,inset=.5,radius=1.875,page='2012 R2-1')
add('yield','R1-2',36,36*3**.5/2,'yield','white',2,.75,.0,page='1-2')
add('onewayR','R6-1',36,12,color='black',radius=2,border=0,page='1-86')
add('onewayL','R6-1',36,12,color='black',radius=2,border=0,page='1-86')
add('onewayVertical','R6-2',24,30,border=.625,page='1-87')
add('doNotEnter','R5-1',30,30,radius=1.5,border=0,page='1-73')
for direction in ('L','R','Both'):
    add('noParking'+direction,'R7-1',12,18,radius=1.5,border=.375,inset=.375,page='1-90')
add('parkingTime','R7-2',12,18,radius=1.5,border=.375,inset=.375,page='1-90')
add('parkingTimedHead','R7 series / agency split R7-2',12,12,radius=1.5,border=.375,inset=.375,page='1-90 / agency two-blank adaptation')
add('parkingTimePlate','R7 series / time plaque',12,6,radius=1.5,border=.375,inset=.375,page='1-90 / agency two-blank adaptation')
add('noTurnRed','R10-11',24,30,border=.625,page='1-139')
add('schoolPlaque','S4-3',24,8,color='fyg',border=.625,page='5-5')
add('schoolTime','S4-1',24,10,border=.625,page='5-3')
add('curve','W1-2',30,30,'diamond','yellow',1.875,.5,.5,page='2-3/2-4')
add('stopAhead','W3-1',30,30,'diamond','yellow',1.875,.5,.5,page='2-20')
add('pedestrian','W11-2',30,30,'diamond','fyg',1.875,.5,.5,page='2-92/6-10')
add('pedestrianYellow','W11-2',30,30,'diamond','yellow',1.875,.5,.5,page='2-92/6-10')
add('schoolCrossing','S1-1',36,36,'school','fyg',2.25,.625,.625,page='5-1/6-58')
for color in ('fyg','yellow'):
    add('arrow'+color,'W16-7P',24,12,color=color,border=.625,page='2-126')

# Lowest plate edge is 7 ft. Crossings carry a related diagonal plaque only;
# unrelated regulatory and warning legends are never stacked together.
ASSEMBLIES = [dict(name=k,faces=[k],post=('round','u2','square')[i%3])
              for i,k in enumerate(SIGNS) if k not in ('schoolPlaque','schoolTime','arrowfyg','arrowyellow','pedestrian','pedestrianYellow','schoolCrossing','parkingTimedHead','parkingTimePlate')]
ASSEMBLIES += [dict(name='schoolSpeed',faces=['schoolTime','speed20','schoolPlaque'],post='square'),
               dict(name='parkingWithTimePlate',faces=['parkingTimePlate','parkingTimedHead'],post='round'),
               dict(name='pedestrian',faces=['arrowfyg','pedestrian'],post='u2'),
               dict(name='pedestrianYellow',faces=['arrowyellow','pedestrianYellow'],post='round'),
               dict(name='schoolCrossing',faces=['arrowfyg','schoolCrossing'],post='u3')]
