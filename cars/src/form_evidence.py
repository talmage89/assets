"""Measurements on evaluated checkpoint meshes, independent of shape controls.

Surface rays/vertices prove geometric changes. They do not certify reflection
fairness, which is judged in the photograph/stripe pairs. No photo is sampled.
"""
import math
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def world_points(ob):return [ob.matrix_world@v.co for v in ob.data.vertices]


def grid(name):
    ob=bpy.data.objects[name];ps=world_points(ob)
    nu=sorted(ob.data.polygons[0].vertices)[2]
    nv=ob['outer_skin_faces']//(nu-1)+1
    return [ps[i:i+nu] for i in range(0,nu*nv,nu)]


def tree(names):
    ps=[];fs=[]
    for name in names:
        ob=bpy.data.objects[name];offset=len(ps);ps+=world_points(ob)
        fs += [tuple(offset+i for i in f.vertices) for f in ob.data.polygons]
    return BVHTree.FromPolygons(ps,fs)


def collect():
    door=tree(['Door skin_FR','Door skin_FR shoulder'])
    def side_x(y,z,which=door):
        p,n,f,d=which.ray_cast(Vector((3,y,z)),Vector((-1,0,0)),3)
        if p is None:raise AssertionError(('No side surface at measurement',y,z))
        return p.x
    zs=[.65,.73,.75,.82,.90,1.00,1.10,1.20,1.32]
    profile=[dict(z_m=z,x_m=side_x(-.60,z)) for z in zs]
    a=side_x(-.60,.82);c=side_x(-.60,1.20);mid=side_x(-.60,1.01)
    crown=mid-(a+c)/2
    hrows=grid('Hood outer');hood_front=min(hrows[0],key=lambda p:abs(p.x));hood_rear=min(hrows[-1],key=lambda p:abs(p.x))
    rows=grid('Roof crown');roof_peak=max((p for row in rows for p in row),key=lambda p:p.z)
    roof_rear=min(rows[-1],key=lambda p:abs(p.x));roof_rear_corner=rows[-1][-1]
    roof_front_corner=rows[0][-1]
    wind=grid('Windshield');wind_top=min(wind[-1],key=lambda p:abs(p.x))
    rt=tree(['Roof crown']);nearest=rt.find_nearest(wind_top)
    pillars=grid('A pillar_R');pillar_bottom=pillars[0][-1];pillar_top=pillars[-1][-1]
    rake=math.degrees(math.atan2(pillar_top.z-pillar_bottom.z,pillar_top.y-pillar_bottom.y))
    if 'Fascia shared frame' in bpy.data.objects:
        fascia=tree(['Fascia shared frame'])
        lo=fascia.ray_cast(Vector((0,-4,.810)),Vector((0,1,0)),4)[0]
        hi=fascia.ray_cast(Vector((0,-4,1.285)),Vector((0,1,0)),4)[0]
        grille=bpy.data.objects['Fascia shared frame']
    else:
        low=grid('Lower fascia')[0];lo=min(low,key=lambda p:abs(p.x))
        high=grid('Nose brow')[0];hi=min(high,key=lambda p:abs(p.x))
        grille=bpy.data.objects.get('Grille form surround') or bpy.data.objects['Grille envelope']
    face_rake=math.degrees(math.atan2(hi.y-lo.y,hi.z-lo.z))
    gpoints=world_points(grille)
    stand=max((lo.y+(p.z-lo.z)*math.tan(math.radians(face_rake)))-p.y for p in gpoints if abs(p.x)<.75)
    lamps=world_points(bpy.data.objects['Headlamp envelope_1'])
    rail_clearances=[]
    if 'Cab roof rail_R' in bpy.data.objects:
        rail=tree(['Cab roof rail_R'])
        for name,y,z in [('Door sash_FR',-.35,1.866),('Door sash_RR',.15,1.865),('Door sash_RR',.55,1.848)]:
            sash=tree([name])
            rail_clearances.append(dict(y_m=y,z_m=z,sash_outboard_of_rail_m=side_x(y,z,sash)-side_x(y,z,rail)))
    arches=[];landmarks={
        'hood_leading_center':hood_front,'hood_rear_center':hood_rear,'roof_peak':roof_peak,
        'roof_rear_center':roof_rear,'roof_rear_corner':roof_rear_corner,
        'a_pillar_lower':pillar_bottom,'a_pillar_upper':pillar_top,
        'front_bumper_tip':min((p for ob in bpy.context.scene.objects if ob.type=='MESH' and ob.get('part_category')=='bumpers' for p in world_points(ob)),key=lambda p:p.y),
        'rear_bumper_tip':max((p for ob in bpy.context.scene.objects if ob.type=='MESH' and ob.get('part_category')=='bumpers' for p in world_points(ob)),key=lambda p:p.y),
    }
    for end in ['F','R']:
        edge=grid('Arch return_'+end+'R')[0]
        peak=max(edge,key=lambda p:p.z);axle=bpy.data.objects['Wheel_'+end+'R'].matrix_world.translation.y
        names=[('Front fender_R' if end=='F' else 'Bed outer_R')]
        if 'Arch flare_'+end+'R' in bpy.data.objects:names.append('Arch flare_'+end+'R')
        side=tree(names)
        # At 10 mm above the opening's top, both side and the same-height
        # unflared door section exist. The rays measure the broad die draw.
        z=peak.z+.010;depth=side_x(axle,z,side)-side_x(-.60,z)
        span=0
        for j in range(1,50):
            z=peak.z+j*.005
            if side_x(axle,z,side)-side_x(-.60,z)>.002:span=j*.005
        width=max(p.y for p in edge)-min(p.y for p in edge)
        level=.430+.8*(peak.z-.430);ys=[]
        for a,b in zip(edge,edge[1:]):
            if (a.z-level)*(b.z-level)<=0 and abs(b.z-a.z)>1e-8:
                ys.append(a.y+(b.y-a.y)*(level-a.z)/(b.z-a.z))
        width80=max(ys)-min(ys)
        arches.append(dict(end=end,opening_top_m=peak.z,opening_width_at_rocker_m=width,
            width_at_80_percent_rise_m=width80,squared_crown_ratio=width80/width,
            measured_flare_depth_above_crown_m=depth,measured_draw_height_above_opening_m=span))
        landmarks[end.lower()+'_arch_crown']=peak
        # Body ray at the upper extent of the broad draw, compared in the profile.
        landmarks[end.lower()+'_draw_top']=Vector((side_x(axle,peak.z+span,side),axle,peak.z+span))
    return dict(method='actual vertex rows and BVH outer-surface rays; no input constant returned as a measurement',
        door_crown_above_820_1200_chord_m=crown,door_section=profile,
        hood_leading_center_m=list(hood_front),hood_rear_center_m=list(hood_rear),
        hood_center_slope_degrees=math.degrees(math.atan2(hood_rear.z-hood_front.z,hood_rear.y-hood_front.y)),
        grille_face_rake_degrees=face_rake,grille_surround_standoff_m=stand,
        lamp_fore_aft_extent_m=max(p.y for p in lamps)-min(p.y for p in lamps),
        roof_peak_m=list(roof_peak),roof_rear_drop_from_peak_m=roof_peak.z-roof_rear.z,
        roof_front_corner_m=list(roof_front_corner),roof_rear_corner_m=list(roof_rear_corner),
        roof_corner_halfwidth_taper_m=abs(roof_front_corner.x)-abs(roof_rear_corner.x),
        windshield_top_to_roof_surface_m=nearest[3],outer_a_pillar_rake_degrees=rake,
        roof_rail_to_sash_clearances=rail_clearances,
        arches=arches,landmarks_world_m={k:list(v) for k,v in landmarks.items()})


if __name__=='__main__':
    import argparse,json,sys
    from pathlib import Path
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
    bpy.context.view_layer.update();Path(a.out).write_text(json.dumps(collect(),indent=2))
