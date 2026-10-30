"""Review-only native-photo regions and estimated physical light rigs.

No photographic pixels, outlines or measurements enter asset generation.
Camera landmarks register views of other makers' guns; accepted form stays.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).resolve().parents[1]

PHOTOS={'side': {'file': 'look-gray-284.jpg',
          'width': 1400,
          'angle': 0,
          'neutral': (50, 40, 300, 100),
          'neutral_name': 'unshadowed neutral gray studio paper above the butt'},
 'macro': {'file': 'look-gray-case.jpg',
           'width': 1600,
           'angle': -35,
           'neutral': (40, 40, 500, 300),
           'neutral_name': 'unshadowed neutral gray studio paper in the native upper-left corner'},
 'muzzle': {'file': 'look-field-12.jpg',
            'width': 1280,
            'angle': 0,
            'neutral': (220, 540, 232, 548),
            'neutral_in_preview': True,
            'neutral_name': 'exposed, uncolored steel muzzle chamfer; estimated neutral, not the clipped '
                            'white cutout'},
 'controls': {'file': 'look-controls.jpg',
              'width': 1200,
              'angle': 0,
              'neutral': (884, 407, 907, 443),
              'neutral_name': 'uncolored polished steel safety guide beside the pad; estimated neutral, '
                              'white cutout clipped'}}

FINISHES={'barrels': {'photo': 'side',
             'shot': 'look_side',
             'parts': ['Barrel_R', 'Barrel_L'],
             'polygons': [[(570, 125), (1301, 120), (1301, 141), (570, 150)]],
             'crop': (550, 105, 1310, 165)},
 'case_action': {'photo': 'macro',
                 'shot': 'look_macro',
                 'parts': ['Action_Body', 'Trigger_Plate', 'Hinge_Pin'],
                 'polygons': [[(631, 686),
                               (659, 677),
                               (672, 743),
                               (742, 765),
                               (1037, 776),
                               (1031, 869),
                               (627, 869)],
                              [(660, 674),
                               (692, 655),
                               (733, 647),
                               (743, 648),
                               (744, 755),
                               (708, 762),
                               (676, 741)]],
                 'crop': (614, 635, 1045, 884)},
 'top_lever': {'photo': 'macro',
               'shot': 'look_macro',
               'parts': ['Top_Lever'],
               'polygons': [[(367, 691),
                             (371, 679),
                             (393, 673),
                             (412, 683),
                             (432, 696),
                             (562, 671),
                             (562, 681),
                             (435, 707),
                             (413, 714),
                             (392, 719),
                             (374, 711)]],
               'crop': (355, 657, 575, 731)},
 'safety': {'photo': 'controls',
            'shot': 'look_safety',
            'parts': ['Tang_Safety'],
            'polygons': [[(923, 408),
                          (950, 409),
                          (1004, 418),
                          (1034, 426),
                          (1049, 435),
                          (1044, 444),
                          (1008, 455),
                          (960, 456),
                          (929, 450),
                          (919, 434)]],
            'crop': (911, 398, 1062, 464)},
 'triggers': {'photo': 'macro',
              'shot': 'look_macro',
              'parts': ['Front_Trigger', 'Rear_Trigger'],
              'polygons': [[(536, 896),
                            (504, 918),
                            (483, 940),
                            (473, 967),
                            (472, 995),
                            (479, 1026),
                            (487, 1027),
                            (482, 998),
                            (483, 970),
                            (491, 945),
                            (505, 923),
                            (539, 899)],
                           [(475, 905),
                            (410, 918),
                            (379, 933),
                            (365, 955),
                            (365, 976),
                            (373, 995),
                            (375, 1003),
                            (365, 999),
                            (357, 977),
                            (358, 952),
                            (366, 935),
                            (390, 921),
                            (438, 907)]],
              'crop': (349, 890, 545, 1033)},
 'guard': {'photo': 'macro', 'shot': 'look_macro', 'parts': ['Trigger_Guard'], 'crop': (278, 877, 646, 1048)},
 'walnut_stock': {'photo': 'side',
                  'shot': 'look_side',
                  'parts': ['Stock_Walnut'],
                  'polygons': [[(106, 195),
                                (352, 166),
                                (362, 165),
                                (376, 177),
                                (402, 174),
                                (461, 148),
                                (536, 132),
                                (539, 180),
                                (481, 191),
                                (450, 205),
                                (408, 221),
                                (375, 249),
                                (341, 242),
                                (333, 249),
                                (111, 334)]],
                  'crop': (92, 120, 546, 348)},
 'walnut_forend': {'photo': 'side',
                   'shot': 'look_side',
                   'parts': ['Forend_Walnut'],
                   'polygons': [[(650, 152), (841, 147), (847, 153), (835, 162), (720, 177), (651, 178)]],
                   'crop': (642, 139, 856, 187)},
 'brass_bead': {'photo': 'muzzle',
                'shot': 'look_muzzle',
                'parts': ['Front_Bead'],
                'polygons': [[(327, 548),
                              (335, 543),
                              (342, 544),
                              (348, 550),
                              (348, 559),
                              (340, 566),
                              (331, 565),
                              (324, 558)]],
                'crop': (312, 534, 358, 576)}}

GUARD_EDGE=[(282, 918),
 (292, 929),
 (305, 947),
 (327, 976),
 (352, 997),
 (385, 1011),
 (430, 1022),
 (480, 1027),
 (520, 1028),
 (560, 1024),
 (599, 1008),
 (620, 985),
 (629, 964),
 (625, 944),
 (615, 925),
 (597, 909),
 (575, 898),
 (550, 892)]

def strip_polygon(path,outward,inward):
 import math
 normals=[]
 for i,p in enumerate(path):
  a=path[max(0,i-1)];b=path[min(len(path)-1,i+1)];dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
  normals.append((-dy/length,dx/length))
 return [(x+outward*nx,y+outward*ny) for (x,y),(nx,ny) in zip(path,normals)]+[(x-inward*nx,y-inward*ny) for (x,y),(nx,ny) in reversed(list(zip(path,normals)))]

# Native steel/shadow boundary, including the complete dark and bright bow.
FINISHES['guard']['polygons']=[strip_polygon(GUARD_EDGE,6.0,2.0)]

# Procedural studio lights, shared by all finishes within a photograph.
SHOTS={'look_side': {'location': (2.5, 0.24, 1.05),
               'target': (0, 0.24, 0),
               'lens': 82,
               'aspect': 3.43980343980344,
               'look_light': [((0.65, 0.24, 0.24), 33.8, 1.8, 0.3),
                              ((0.75, 0.24, -0.45), 1, 1.5, 0.65),
                              ((-0.8, 0.24, 0.4), 2, 1.4, 0.7)],
               'action': 'Idle',
               'frame': 0,
               'exposure': -0.15,
               'background': 'transparent',
               'light_target': (0, 0.235, 0),
               'look_world': 0.4, 'look_light_colors': [(1,.96,.95),(1,1,1),(1,1,1)]},
 'look_macro': {'location': (0.68, 0.13, 0.31),
                'target': (0, 0.105, 0.025),
                'lens': 60,
                'aspect': 3.5555555555555554,
                'look_light': [((0.5, -0.5, 0.12), 30, 0.4, 0.75),
                               ((0.5, 0.6, 0.12), 24, 0.4, 0.75),
                               ((0.65, 0.08, 0.6), 12, 1.2, 0.35)],
                'action': 'Idle',
                'frame': 0,
                'exposure': -0.15,
                'background': 'transparent',
                'light_target': (0, 0.11, 0.025),
                'look_world': 0.65},
 'look_muzzle': {'location': (0.12, 0.95, 0.17),
                 'target': (0, 0.76, 0.044),
                 'lens': 65,
                 'aspect': 1.5,
                 'look_light': [((0.1, 0.95, 0.38), 3.0, 0.2, 0.3),
                                ((-0.14, 0.68, 0.26), 2.5, 0.25, 0.3),
                                ((0.08, 0.7, -0.1), 0.4, 0.25, 0.25)],
                 'action': 'Idle',
                 'frame': 0,
                 'exposure': -0.15,
                 'background': 'transparent',
                 'light_target': (0, 0.76, 0.044),
                 'look_world': 1.0,
                 'look_paper': (0.9, 0.9, 0.9),
                 'look_world_color': (1, 1, 1)},
 'look_safety': {'location': (0.025, -0.012, 0.16),
                 'target': (0, 0.007, 0.025),
                 'lens': 70,
                 'aspect': 2.5,
                 'look_light': [((0.65, 0.24, 0.78), 35, 0.2, 2.0),
                                ((0.75, 0.24, -0.45), 20, 0.9, 1.3),
                                ((-0.8, 0.24, 0.4), 5, 1.0, 1.5)],
                 'action': 'Idle',
                 'frame': 0,
                 'exposure': -0.15,
                 'background': 'transparent',
                 'light_target': (0, 0.007, 0.025),
                 'roll': 0.7853981633974483}}

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


# An additional used field gun retains deep blue over its whole barrel length.
# Keep the older gray-field comparison above as additional evidence.
PHOTOS['deep_blue']=dict(file='look-field-4.jpg',width=1400,angle=0,
 neutral=(875,521,882,524),neutral_in_preview=True,
 neutral_name='uncolored rubbed steel at the bottom of the guard bow; estimated neutral, clipped white cutout excluded')
FINISHES['barrels_deep_blue']=dict(photo='deep_blue',shot='look_deep_blue',
 parts=['Barrel_R','Barrel_L'],polygons=[[(83,444),(835,437),(835,459),(83,460)]],crop=(74,428,846,468))
SHOTS['look_deep_blue']=dict(location=(-3.0,.24,.04),target=(0,.235,0),lens=82,
 aspect=850/100,action='Idle',frame=0,exposure=-.15,background='transparent',
 look_light=[((-.65,.24,.40),10.0,1.8,.05),((-.75,.24,-.20),.5,1.5,.70)],
 light_target=(0,.35,.04),look_world=.98,look_paper=(.9,.9,.9),look_paper_x=.06,
 look_reflection_card=dict(location=(-.25,.45,.10),size=(.002,.80,.10),color=(.20,.20,.20)))
_original_definitions=definitions

def definitions():
 from guns.common.photo_matches import L
 rows=_original_definitions()
 rows['look_deep_blue']=dict(photo=str(BASE/'build/look-photos/deep_blue.png'),crop=(40,405,890,505),
  title='Used field gun with retained deep bluing / full barrel length',
  fit_location=(-3.0,.24,.04),fit_target=(0,.235,0),fit_lens=82,
  landmarks=[L((-12.6,115,57.35),(835,436)),L((-10.9,775.4,54.6),(82,443)),
   L((0,-299,-5),(1297,497)),L((0,-299,-117),(1290,631)),L((-25.95,170,19),(787,477))])
 return rows


# Material review annotations; never imported by procedural source shaders.
for _name,_note in {
 'barrels':'The photograph has a broad gray lower flank; ours retains deep bluing outside the short carry field. The cyan/yellow overlays locate the missing middle values and wider reflected strip. The retained-blue photograph is a separate check; this gray-field comparison remains a miss.',
 'case_action':'Original faded blue/straw/brown oxide survives near fences and the bar; handled flats are silver-gray. Whole-part tolerances are tested above; different oxide placement and the photo engraving remain visible, with no copied pattern.',
 'top_lever':"The full accepted narrow leaf and stem are included. The thumb-contact land is bright; protected blued stem remains dark. Passing quantiles do not equate the accepted leaf to the photo maker's rounded paddle.",
 'safety':"Dark cut valleys and polished diamond facets both remain in the denominator. The original accepted pad includes its recessed slot; the photo has another maker's unslotted pad. Source/export quantiles below expose any filtered loss of the dark valleys.",
 'triggers':"The cyan low decile lies on our broad blade faces, versus the photo's thin, partly shadowed blade profiles. The whole-part median and bright edges are tested separately; preserved accepted blade shape and broad-face illumination leave a low-tail mismatch.",
 'guard':"The accepted guard's broad inner land reflects the gray field; the photographed thin rounded edge catches a white strip. The yellow overlay and full histogram show too little bright area. A low-light trial improved this guard but overlit both triggers; the joint rig was rejected.",
 'walnut_stock':"The photo's low decile covers its checked wrist and lower butt, with a warmer broad oil highlight. Ours has a smaller straight-hand checker field. Retain every planed land, dark vessel and cut valley in the full-part test; no selected wood patch substitutes for it.",
 'walnut_forend':"The whole visible splinter, bare edges and checker field are included. Individual tips survive in our delivered normal; the photo's handled points are broader. Read median and tails together with source/export loss and the separate native 2D wear pair.",
 'brass_bead':'The complete round Front_Bead is measured, including its shadowed lower hemisphere. Its separate raised foot remains visible in context; the photographed bead sits almost flush on the rib. No dark bead pixels are omitted. A physical front fill, below the bead center, is identical in source and export.',
 'barrels_deep_blue':'This second used gun retains blue-black oxide along its tubes. Whole visible barrels are retained, with an estimated rubbed-steel neutral and disclosed narrow photographic cross-section resolution. The native photograph is 2560 pixels wide; no sharper upload was available.',
}.items():
 FINISHES[_name]['residual_note']=_note


# Estimated photographed inner-bow reflection. A physical slit and upper barn
# door share the same light transport with every control. No part grading.
SHOTS['look_macro']['look_strips']=[dict(name='inner bow',location=(-.040,.060,-.002),
 power=.26,size=(.14,.001),target=(.003,.060,-.030))]
SHOTS['look_macro']['look_flags']=[dict(name='slit upper barn door',
 location=(-.020,.060,.0065),size=(.001,.18,.040))]
SHOTS['look_muzzle']['look_strips']=[dict(name='muzzle front lower fill',
 location=(.04,.82,.052),power=.04,size=(.06,.06),target=(0,.766,.0547))]
FINISHES['guard']['residual_note']="The accepted broad inner land and the photograph's thin rounded edge remain distinct. Intact polished blue, satin filed edges and the bright contact core share one estimated rig; the same physical slit/barn door is present in source and export. Any remaining tail or peak miss stays in the whole-part table above."
FINISHES['barrels']['role']='supplementary older gray-use context'
FINISHES['barrels_deep_blue']['role']='primary retained rust-blue finish'
