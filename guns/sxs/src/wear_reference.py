"""Review-only annotations of visible wear, never inputs to asset generation.

Polygons identify physical wear fields, not a traced texture. Each denominator
is the complete visible named part in a whole-gun photograph, except the lever,
guard and action, whose complete visible sides are in the sharper macro. Dark
paint/oxide islands remain inside the denominator. Specular strips on intact
barrels are deliberately excluded. Photographic wear attribution is uncertain:
the report retains a boundary band and does not call reflection a measurement
of missing bluing.
"""
from look_matches import FINISHES

def row(finish,polygons,description,**kwargs):
    r=FINISHES[finish]
    return dict(photo=r['photo'],parts=r['parts'],part_polygons=r['polygons'],
                polygons=polygons,description=description,**kwargs)

SITES={
 'barrel_carry':row('barrels',[
    [(620,139),(661,138),(689,137),(741,137),(787,136),(828,137),
     (869,138),(903,137),(934,139),(917,143),(854,143),(791,144),
     (734,145),(684,146),(645,146),(621,145)]],
    'Gray lower-flank field around the balance/carry region; the crisp upper softbox reflection is excluded.',
    uncertainty='Thinned bluing and a reflected gray card cannot be separated uniquely in this single photograph; cross-view macro is qualitative support.'),
 'muzzles':row('barrels',[
    [(1296,120),(1302,120),(1303,140),(1297,141),(1297,134),(1295,130)]],
    'Narrow gray end rim, with the black blued tube immediately behind it.',
    uncertainty='Only a few pixels at whole-gun scale; the separate muzzle photograph confirms bare chamfers but is not substituted as a differently cropped denominator.'),
 'action_fade':row('case_action',[
    [(634,778),(648,771),(667,779),(698,782),(726,784),(755,784),
     (794,787),(826,786),(854,795),(877,812),(886,833),(881,847),
     (863,859),(824,860),(781,862),(743,861),(705,864),(674,862),(634,863)],
    [(668,679),(692,659),(725,651),(736,651),(739,713),(725,737),(702,745),(681,727)],
    [(911,789),(939,796),(963,817),(972,845),(953,862),(917,866),(899,858),(901,841)],
    [(644,755),(665,757),(688,767),(731,769),(774,774),(829,774),(867,778),
     (882,785),(880,793),(860,786),(825,782),(774,782),(729,778),(683,775),(643,767)]],
    'Handled side flats, knuckle face and exposed lip faded to silver gray; protected case oxide survives around returns.',
    uncertainty='Engraving, screw and pivot construction differ. Annotation follows finish fields, excluding the black screw recess.'),
 'lever_thumb':row('top_lever',[
    [(397,676),(410,681),(423,689),(435,696),(461,692),(477,688),
     (474,694),(445,705),(420,713),(403,717),(395,711),(407,704),(414,695),(407,685)]],
    'A merged bright pressure field on the thumb paddle and its rounded rim; the neck remains blued.',
    uncertainty='Bright metal is partly specular. Boundary band records the uncertain transition to intact blue.'),
 'guard_fingers':row('guard',[
    [(295,923),(306,942),(331,975),(358,997),(392,1012),(433,1025),
     (477,1035),(532,1041),(577,1036),(607,1020),(626,996),(635,968),
     (630,941),(620,922),(614,926),(626,948),(628,970),(621,990),
     (603,1008),(575,1023),(531,1029),(479,1024),(433,1015),(393,1003),
     (362,985),(337,964),(314,936),(302,920)]],
    'Continuous rubbed inner bow, strongest below and behind the fingers, with intact dark outer margins.',
    uncertainty='The rounded bow also catches a reflection. This annotation is an upper estimate of visibly rubbed steel.'),
 'wrist_points':row('walnut_stock',[
    [(375,190),(392,184),(414,177),(434,172),(447,173),(438,184),
     (419,195),(405,211),(393,224),(378,237),(366,232),(373,214)]],
    'Flattened warm diamond points in the hand-pressure field; deep dark grooves survive.',
    threshold=105,
    uncertainty='Bright point tops are a visible-wear proxy, not a claim that every bright cutter point was flattened by use.'),
 'forend_points':row('walnut_forend',[
    [(698,161),(725,157),(760,155),(796,154),(823,155),(830,158),
     (815,163),(785,166),(754,169),(722,173),(702,173)]],
    'Polished diamond tops in the supporting palm field, with unhandled borders and grooves.',
    threshold=70,
    uncertainty='Whole-gun point resolution is limited. Native pixels are used; the boundary/threshold sensitivity is retained.'),
 'stock_toe':row('walnut_stock',[
    [(170,308),(176,304),(181,303),(185,298),(190,299),(190,302),
     (185,306),(180,309),(174,312),(170,313)],
    [(108,325),(112,322),(116,324),(117,329),(112,333),(109,334)],
    [(112,203),(119,202),(120,205),(116,207),(112,207)]],
    'Small compressed/damaged finish islands along the heel/toe edge; no overall dirt band.',
    uncertainty='The reference has one larger edge chip; ours has one compressed toe impact and two smaller edge impacts, with original shapes.'),
 'forend_edges':row('walnut_forend',[
    [(655,159),(659,157),(662,158),(664,162),(661,165),(656,165)],
    [(670,166),(674,166),(675,169),(671,171),(669,169)],
    [(831,150),(836,148),(841,149),(842,152),(837,155),(833,154)]],
    'Small finish breaks/dings at the handguard ends and lower edge; checker field is excluded.',
    uncertainty='Shallow dark dents are difficult to separate from pores; annotated obvious impacts only.'),
}
# The whole-part outline is corrected from native steel/shadow edges in
# look_matches.py. A three-pixel gray/bright inner field is the visible rub
# estimate; its normal-direction boundary band is explicitly uncertain.
from look_matches import GUARD_EDGE,strip_polygon
SITES['guard_fingers']['polygons']=[strip_polygon(GUARD_EDGE,2.0,1.0)]
SITES['guard_fingers']['part_polygons']=FINISHES['guard']['polygons']
SITES['guard_fingers']['uncertainty']='Revised native annotation excludes cast shadow. The three-pixel inner gray/bright field is an upper estimate because specular light also brightens intact bluing.'
