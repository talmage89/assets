"""Unsurveyed 4 ft installation: compare tips/spacing, not exact site height.

Five board tips and lower ends in the unobscured right-hand bay. The fit uses
our 3.5 ft stock-derived board length; photographic construction residuals are
reported. Landmarks are hand-measured, never texture/geometry tracing.
"""
from pathlib import Path
PHOTO=Path(__file__).resolve().parents[2]/'refs/picket-white-03.jpg'
clear=2.3495;w=.0889;gap=(clear-13*w)/14
xs=[-1.2192-clear/2+gap+w/2+i*(w+gap) for i in range(8,13)]
# Rightward in this good-side view corresponds to world +X.
landmarks=[]
for x,top,bottom in zip(xs,[(1176,413),(1327,406),(1488,401),(1642,397),(1800,390)],[(1176,1292),(1327,1320),(1488,1343),(1642,1365),(1800,1387)]):
 landmarks.append(dict(world=(x,-.034925,1.1176),pixel=top))
 if bottom[1]<1368:landmarks.append(dict(world=(x,-.034925,.0508),pixel=bottom,weight=.6))
MATCHES={'match_pickets':dict(title='Painted cedar / stock spacing and French Gothic tips',photo=str(PHOTO),crop=(1000,350,1824,1368),location=(-1.5,-2.8,1.7),target=(-.55,0,.65),lens=52,exposure=-1.15,
 hide_assemblies=['Picket_B','Picket_End','Picket_Line','Picket_Corner','Picket_GateBay'],landmarks=landmarks)}
