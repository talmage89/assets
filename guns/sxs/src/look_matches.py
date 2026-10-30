"""Review-only finish masks and camera landmarks; never imported by asset code.

Coordinates are on the declared comparison image. Whole-side polygons encompass
entire visible parts, including their darks/highlights. No measured photo field
is passed to modeling, shaders, UVs or baking.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).resolve().parents[1]
PHOTOS={
 'side':dict(file='look-gray-284.jpg',width=1400,angle=0,neutral=(50,40,300,100),
             neutral_name='unshadowed neutral gray studio paper above the butt'),
 'macro':dict(file='look-gray-case.jpg',width=1600,angle=-35,neutral=(40,40,500,300),
              neutral_name='unshadowed neutral gray studio paper in the native upper-left corner'),
 'muzzle':dict(file='look-field-12.jpg',width=1280,angle=0,neutral=(220,540,232,548),neutral_in_preview=True,
               neutral_name='exposed, uncolored steel muzzle chamfer; estimated neutral, not the clipped white cutout'),
}
# Normalized macro coordinates are measured after a rigid in-plane -35-degree
# rotation. The complete transformation and native neutral are in the report.
FINISHES={
 'barrels':dict(photo='side',shot='look_side',parts=['Barrel_R','Barrel_L'],
  polygons=[[(570,125),(1301,120),(1301,141),(570,150)]],crop=(550,105,1310,165)),
 'case_action':dict(photo='macro',shot='look_macro',parts=['Action_Body','Trigger_Plate','Hinge_Pin'],
  polygons=[[(631,686),(659,677),(672,743),(742,765),(1037,776),(1031,869),(627,869)],
            [(660,674),(692,655),(733,647),(743,648),(744,755),(708,762),(676,741)]],crop=(614,635,1045,884)),
 'top_lever':dict(photo='macro',shot='look_macro',parts=['Top_Lever'],
  polygons=[[(367,691),(371,679),(393,673),(412,683),(432,696),(562,671),(562,681),(435,707),(413,714),(392,719),(374,711)]],crop=(355,657,575,731)),
 'safety':dict(photo='macro',shot='look_macro',parts=['Tang_Safety'],
  polygons=[[(294,742),(302,736),(314,736),(320,741),(310,743)]],crop=(283,726,329,751)),
 'triggers':dict(photo='macro',shot='look_macro',parts=['Front_Trigger','Rear_Trigger'],
  polygons=[[(491,896),(503,899),(484,922),(477,950),(484,985),(496,1005),(490,1009),(477,991),(468,952),(475,922)],
            [(410,911),(420,908),(408,930),(405,957),(414,985),(429,1002),(424,1005),(407,985),(398,957),(400,931)]],crop=(384,886,513,1018)),
 'guard':dict(photo='macro',shot='look_macro',parts=['Trigger_Guard'],
  polygons=[[(311,927),(349,909),(480,884),(539,895),(605,913),(628,952),(633,980),(606,1012),(544,1033),(448,1031),(372,1016),(343,987)]],
  holes=[[(348,931),(372,922),(484,895),(535,901),(587,918),(612,951),(615,980),(594,1000),(542,1017),(454,1016),(389,1003),(364,979)]],crop=(300,875,645,1042)),
 'walnut_stock':dict(photo='side',shot='look_side',parts=['Stock_Walnut'],
  polygons=[[(106,195),(352,166),(362,165),(376,177),(402,174),(461,148),(536,132),(539,180),(481,191),(450,205),(408,221),(375,249),(341,242),(333,249),(111,334)]],crop=(92,120,546,348)),
 'walnut_forend':dict(photo='side',shot='look_side',parts=['Forend_Walnut'],
  polygons=[[(650,152),(841,147),(847,153),(835,162),(720,177),(651,178)]],crop=(642,139,856,187)),
 'brass_bead':dict(photo='muzzle',shot='look_muzzle',parts=['Front_Bead'],
  polygons=[[(327,548),(335,543),(342,544),(348,550),(348,559),(340,566),(331,565),(324,558)]],crop=(312,534,358,576)),
}
# A neutral key and soft fill estimate the gray-paper photographs' studio.
# One light setup serves every finish in a view; measured RGB is never graded.
PHOTO_LIGHT=[((.65,.24,.78),35,.20,2.0),((.75,.24,-.45),20,.90,1.3),((-.8,.24,.4),5,1.0,1.5)]
SHOTS={
 'look_side':dict(location=(2.5,.24,1.05),target=(0,.24,0),lens=82,aspect=1400/407,look_light=PHOTO_LIGHT),
 'look_macro':dict(location=(.68,.13,.31),target=(0,.105,.025),lens=60,aspect=1600/450,look_light=PHOTO_LIGHT),
 'look_muzzle':dict(location=(.12,.95,.17),target=(0,.760,.044),lens=65,aspect=1.5,look_light=PHOTO_LIGHT),
}
for s in SHOTS.values():s.update(action='Idle',frame=0,exposure=-.15,background='transparent')

def definitions():
 from guns.common.photo_matches import L
 # Landmarks identify visible construction, not highlights or finish edges.
 # Their camera residuals remain explicit; other makers' forms differ.
 return {
 'look_side':dict(photo=str(BASE/'build/look-photos/side.png'),crop=(0,70,1400,360),title='Used plain field boxlock / whole finish regions',
  location=SHOTS['look_side']['location'],target=(0,.235,0),lens=82,exposure=-.15,
  landmarks=[L((12.6,115,57.35),(565,124)),L((10.9,775.4,54.6),(1302,120)),
             L((0,-299,-5),(105,193)),L((0,-299,-117),(111,336)),L((25.95,170,19),(627,166))]),
 'look_macro':dict(photo=str(BASE/'build/look-photos/macro.png'),crop=(280,635,1550,1045),title='Faded case, blued controls and polished triggers / gray paper',
  location=SHOTS['look_macro']['location'],target=SHOTS['look_macro']['target'],lens=60,exposure=-.15,
  landmarks=[L((12.6,115,57.35),(742,649)),L((25.95,170,19),(969,829)),
             L((25.95,75,13),(632,868)),L((25.95,85,42),(633,686))]),
 }
# The first guard annotation included backdrop/trigger pixels. This follows
# only the open-ended bow, including its dark outer face and bright inner rim.
FINISHES['guard']['polygons']=[[(284,917),(292,923),(303,944),(326,976),(352,997),(386,1013),(428,1027),(477,1037),(532,1042),(580,1037),(609,1020),(628,996),(638,967),(634,939),(621,915),(600,898),(572,887),(550,885),
 (550,893),(575,896),(596,907),(614,925),(626,946),(630,966),(623,989),(605,1010),(577,1025),(531,1031),(479,1026),(431,1016),(391,1004),(360,987),(336,965),(314,937),(301,918)]]
FINISHES['guard'].pop('holes',None)
FINISHES['guard']['crop']=(278,877,646,1048)
FINISHES['triggers']['polygons']=[
 [(536,896),(504,918),(483,940),(473,967),(472,995),(479,1026),(487,1027),(482,998),(483,970),(491,945),(505,923),(539,899)],
 [(475,905),(410,918),(379,933),(365,955),(365,976),(373,995),(375,1003),(365,999),(357,977),(358,952),(366,935),(390,921),(438,907)]]
FINISHES['triggers']['crop']=(349,890,545,1033)
PHOTOS['controls']=dict(file='look-controls.jpg',width=1200,angle=0,neutral=(884,407,907,443),
 neutral_name='uncolored polished steel safety guide beside the pad; estimated neutral, white cutout clipped')
FINISHES['safety'].update(photo='controls',shot='look_safety',
 polygons=[[(923,408),(950,409),(1004,418),(1034,426),(1049,435),(1044,444),(1008,455),(960,456),(929,450),(919,434)]],crop=(911,398,1062,464))
SHOTS['look_safety']=dict(location=(.025,-.012,.16),target=(0,.007,.025),lens=70,aspect=2.5,
 look_light=PHOTO_LIGHT,action='Idle',frame=0,exposure=-.15,background='transparent')

# Each photographer's illumination is estimated as a neutral physical rig.
# Targets follow the photographed region, rather than the whole-gun origin.
SHOTS['look_side']['look_light']=[((.65,.24,.78),35,.20,2.0),((.75,.24,-.45),6,.90,1.3),((-.8,.24,.4),5,1.0,1.5)]
SHOTS['look_side']['light_target']=(0,.235,0)
SHOTS['look_macro']['look_light']=[((.65,.08,.78),42,.50,1.0),((-.8,.12,.4),5,1.0,1.0)]
SHOTS['look_macro']['light_target']=(0,.11,.025)
SHOTS['look_safety']['light_target']=(0,.007,.025)
SHOTS['look_muzzle']['look_light']=[((.10,.95,.38),3.0,.20,.30),((-.14,.68,.26),2.5,.25,.30),((.08,.70,-.10),.4,.25,.25)]
SHOTS['look_muzzle']['light_target']=(0,.76,.044)
SHOTS['look_muzzle']['look_world']=3.0
# The reference's long rectangular catchlight runs along the gun. The area
# light's local X follows that axis; exchanging width/height is a physical
# orientation correction, not an image correction.
SHOTS['look_side']['look_light']=[((.65,.24,.42),22,1.8,.32),((.75,.24,-.45),6,1.5,.65),((-.8,.24,.4),5,1.4,.7)]
SHOTS['look_macro']['look_light']=[((.65,.08,.60),32,1.2,.35),((.65,.12,-.30),2,1.0,.65)]

# White seamless on the bead reference is a reflector, not a balance target.
SHOTS['look_muzzle'].update(look_paper=(.90,.90,.90),look_world_color=(1,1,1),look_world=1.0)
# A broader key supplies the broad soft oil reflection visible on the stock.
SHOTS['look_side']['look_light']=[((.65,.24,.24),38,1.8,.60),((.75,.24,-.45),3,1.5,.65),((-.8,.24,.4),3,1.4,.7)]
SHOTS['look_macro']['look_world']=1.5
