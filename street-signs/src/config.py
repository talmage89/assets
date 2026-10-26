import os
TITLE='Aldervale / residential street signs'
EXPORT_VARIANT=int(os.environ.get('NAME_VARIANT','0'))
BUDGETS={'StreetSigns':1200}
BOUNDS={'StreetSigns':dict(size=(.762,.762,3.4482),tolerance=(.002,.002,.008))}
BAKE_CAGE=.00015
BAKE_RAY=.003
UV_MIN_COVERAGE=.22
UV_PRIORITY={'Stop plate':1.8,'Street blade':1.5,'Square perforated':.6}
UV_DENSITY_BANDS=dict(p5_min=150,median_min=300,median_max=1100,p95_max=1800)
SHOTS={
'hero_closed':dict(location=(2.3,-4.8,3.5),target=(0,0,1.9),lens=48,aspect=.8),
'front':dict(location=(0,-6,1.724),target=(0,0,1.724),ortho=2.9,aspect=.8),
'side':dict(location=(6,0,1.724),target=(0,0,1.724),ortho=2.9,aspect=.8),
'back':dict(location=(0,6,1.724),target=(0,0,1.724),ortho=2.9,aspect=.8),
'top':dict(location=(0,0,6),target=(0,0,2.8),ortho=1.15,aspect=1),
'controls':dict(location=(.8,-1.6,3.6),target=(0,0,3.1),lens=65,aspect=1.2),
'casting':dict(location=(.8,1.6,2.9),target=(0,0,2.53),ortho=1.1,aspect=1.2),
'scale':dict(location=(2.4,-6,3),target=(-.3,0,1.7),lens=48,aspect=.9,human=True),
}
SHOTS['hero_open']=SHOTS['hero_closed']

CONTACTS=[('Stop plate','Stop back mounting spacer',.0015),('Stop back mounting spacer','Square perforated galvanized post',.001),('Square perforated galvanized post','Post cap blade saddle',.001),('Post cap blade saddle','Street blade 0-0',.001),('Street blade 0-0','Cross bracket saddle',.001),('Cross bracket saddle','Street blade 0-1',.001)]
CONTACTS += [('Anchor through pin','Breakaway anchor sleeve',.001),('Anchor through pin','Square perforated galvanized post',.001)]
UV_PACK_SHAPE='AABB'
UV_SMART_ASPECT=False
