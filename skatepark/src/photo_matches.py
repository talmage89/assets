"""Camera evidence for period form comparisons; inferred unsurveyed anchors.

These are different original parks. Only named construction features enter
the fits; surrounding layouts are deliberately not photographic replicas.
Large residuals disclose how far a comparison can support a shape judgment.
"""
import math

from contour import rim_xy,normal_xy

def rim(t):
    x,y=rim_xy(t);return (-10.668+x,-1.2192+y,0)
def anchor(p,uv):return dict(world=p,pixel=uv)
def normal(t):return (*normal_xy(t),0)
def tile_bottom(t):
    h=1.6764+.4572*math.cos(t);theta=math.acos(1-h/2.4384);a=theta-.156/2.4384
    distance=2.4384*(math.sin(theta)-math.sin(a));p=rim(t);n=normal(t)
    return (p[0]-n[0]*distance,p[1]-n[1]*distance,-h+2.4384*(1-math.cos(a)))
def deck(t):
    p=rim(t);n=normal(t);return (p[0]+n[0]*.30,p[1]+n[1]*.30,0)

MATCHES={
 'alondra_bowl':dict(title='2012 kidney bowl / plan and section',photo='refs/alondra.jpg',crop=(120,320,986,653),
    location=(-0.4417853251046226, -9.095106955064963, 2.999667203247387),target=(-1.1074688341465788, -8.401892939144108, 2.723406829830445),lens=27*986/866,lens_bounds_mm=(27*986/866,27*986/866+.001),camera_height_m=(3.0,1.0),
    # Measured lip outline; curve phases are nearest-contour correspondences,
    # not surveyed point identities. Report this separately from rigid corners.
    landmarks=[anchor(rim(t),uv) for t,uv in [(4.324925886441948, [150.0, 411.0]), (4.259999638267759, [160.0, 391.0]), (3.485073450382277, [188.0, 377.0]), (3.2986722862692823, [230.0, 366.0]), (3.108082331951502, [280.0, 359.0]), (2.927964353145687, [330.0, 356.0]), (2.745751979237479, [380.0, 357.0]), (2.555162024919698, [430.0, 362.0]), (2.3436281195779856, [480.0, 370.0]), (2.1153390534171272, [525.0, 381.0]), (1.910088333382594, [555.0, 395.0]), (1.757197490907891, [564.0, 404.0]), (1.767669466419857, [557.0, 416.0]), (1.7027432182456677, [570.0, 429.0]), (1.608495438637974, [600.0, 437.0]), (1.4535102010608776, [650.0, 444.0]), (1.298524963483781, [700.0, 454.0]), (1.137256540599505, [750.0, 469.0]), (0.9697049324080494, [800.0, 490.0]), (0.7853981633974482, [850.0, 517.0]), (0.5717698629533423, [900.0, 548.0]), (0.364424747816416, [932.0, 580.0]), (0.1759291886010284, [940.0, 608.0]), (0.060737457969402664, [938.0, 634.0]), (6.262241356155654, [921.0, 653.0]), (4.427551246459215, [150.0, 430.0]), (4.622329990981782, [168.0, 456.0]), (4.844335871835461, [200.0, 486.0]), (5.0453978016652075, [240.0, 517.0]), (5.208760619651876, [290.0, 545.0]), (5.323952350283502, [340.0, 569.0]), (5.4328608956079485, [400.0, 594.0]), (5.55224141644436, [480.0, 620.0]), (5.671621937280773, [570.0, 641.0])]],
    exposure=.85),
 'burnham_street':dict(title='2007 municipal hubba / steel-armored sloping ledge',photo='refs/20070329_Burnham_Park_Skatepark.JPG',crop=(1170,1110,1570,1270),
    isolate=['Stairs_5_0','UpperStreetPlaza','SkatingFlatwork'],
    location=(49,-28,1.65),target=(13.9,2.4,.6),lens=365,lens_bounds_mm=(350,390),camera_height_m=(1.65,.5),
    landmarks=[anchor(p,uv) for p,uv in [
        ((13.716,1.524,.421),(1211,1198)),((14.2748,1.524,.421),(1243,1201)),
        ((13.716,3.048,1.183),(1319,1130)),((14.2748,3.048,1.183),(1354,1136)),
        ((13.716,1.524,0),(1211,1240)),((14.2748,1.524,0),(1243,1240))]],exposure=.9),
 'memorial_coping':dict(title='2009 pool coping / projection and tile band',photo='refs/memorial.jpg',crop=(0,720,580,1220),
    location=(-13,-2,1.3),target=(-13,-5,0),lens=60,lens_bounds_mm=(49.7,78.1),camera_height_m=(1.3,.5),
    landmarks=[anchor(tuple(c+(.03175 if k==2 else 0) for k,c in enumerate(rim(t))),uv) for t,uv in [(-1.68,(8,823)),(-1.79,(175,836)),(-1.90,(365,857)),(-2.01,(560,883))]]+
       [anchor(tile_bottom(t),uv) for t,uv in [(-1.68,(8,879)),(-1.90,(365,919))]],exposure=.8)
}

LIGHT={
 'alondra_bowl':dict(sun_direction=(-.35,-.8,-1),sun_energy=3.8,sky_strength=.11,sky_saturation=.4),
 'burnham_street':dict(sun_direction=(-.5,.4,-1),sun_energy=1.3,sky_strength=.18,sky_saturation=.2,sun_angle_degrees=12),
 'memorial_coping':dict(sun_direction=(-.3,-.6,-1),sun_energy=1.2,sky_strength=.14,sky_saturation=.2,sun_angle_degrees=12),
}
# Neutral concrete ROIs avoid paint, people and foliage. Gains are comparison
# white-balance estimates, not an inversion of unknown photographic exposure.
NEUTRALS={'alondra_bowl':(160,330,210,350),'burnham_street':(1600,1150,1650,1180),'memorial_coping':(20,780,90,810)}

# Crop-equivalent lenses use the cropped image's pixel width, as kit.project
# requires. Report native sensor-equivalent focal length separately. A 365mm
# crop camera here represents roughly 48mm on the full 3072px Burnham photo.
LENS_EVIDENCE={
 'alondra_bowl':dict(full_width=986,crop_width=866,native_equivalent_mm=27,source='EXIF FocalLengthIn35mmFilm 27; 18mm on Nikon D7000'),
 'burnham_street':dict(full_width=3072,crop_width=400,native_equivalent_mm=48,source='EXIF 9.565mm; Canon A620 sensor-width conversion approximately 48mm'),
 'memorial_coping':dict(full_width=2058,crop_width=580,native_equivalent_mm=None,source='No retained EXIF; bounded 14–22mm full-frame equivalent estimate'),
}

# Upright/exif-constrained contour comparison. A free pinhole fit preferred
# approximately 9.4 degrees of image roll, contradicted by the photograph's
# near-level fence/horizon. Freeze the upright refit and disclose its larger
# outline residual. Phases are inferred nearest points, never surveyed corners.
UPRIGHT_ALONDRA = {'location': [-0.4292752469944748, -9.018189947945116, 3.0028154617981513], 'target': [-1.1169460983606951, -8.351789007266106, 2.714686000542646], 'phases': [3.743207646752239, 3.6426766818373655, 3.49659262344544, 3.3190926385176165, 3.127455486648639, 2.948384705394021, 2.767743127812608, 2.5792475685972205, 2.373473249787089, 2.1504201713822133, 1.9399334635916974, 1.8331193133696444, 1.8142697574481057, 1.7451547190691301, 1.6524777357882312, 1.4969688994355366, 1.3414600630828417, 1.1812388377497622, 1.0115928344559135, 0.8230972752405259, 6.138672045114456, 6.182654342264713, 6.171658767977149, 6.144955230421636, 6.102543729598174, 3.843738611667112, 4.258428841940965, 4.571017310973149, 4.842765075508666, 5.072101339220722, 5.240176546187775, 5.3689818449849565, 5.497787143782138, 5.62030925727214]}

def calibrated_match(name):
    import numpy as np
    from kit import photo_match
    match=MATCHES[name].copy()
    if name=='alondra_bowl':
        match['landmarks']=[anchor(rim(t),row['pixel']) for t,row in zip(UPRIGHT_ALONDRA['phases'],match['landmarks'])]
    result=photo_match.calibrate(match)
    if name=='alondra_bowl':
        shot=result['shot'];shot.update(location=UPRIGHT_ALONDRA['location'],target=UPRIGHT_ALONDRA['target'],roll=0.,lens=27*986/866)
        camera=np.array(shot['location']);direction=np.array(shot['target'])-camera
        parameters=[math.atan2(direction[1],direction[0]),math.atan2(direction[2],np.linalg.norm(direction[:2])),*camera,math.log(shot['lens']),0.]
        w,h=match['crop'][2]-match['crop'][0],match['crop'][3]-match['crop'][1]
        uv,depth,_=photo_match.project(parameters,np.array(result['landmarks_world_m']),w,h)
        errors=np.linalg.norm(uv-np.array(result['measured_pixels']),axis=1)
        result.update(projected_pixels=uv.tolist(),residuals_pixels=errors.tolist(),residual_rms_pixels=float(np.sqrt(np.mean(errors**2))),fit_method='Frozen upright / EXIF 27mm; nearest-outline phases, 3m height comparator, different original kidney; not a surveyed correspondence fit')
    return result
