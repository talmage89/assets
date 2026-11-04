"""Actual triangle/axis/attribute/strut measurements for the source checkpoint.

This checks construction, separately from kit.audit and the sampled solid
motion test. It makes no UV, bake, serialization or final GLB claim.
"""
import argparse,hashlib,json,math,sys
from collections import Counter
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from suv_mechanics import update_supports
from suv_exterior import tree_for
import suv_spec as S


def points(ob):return [ob.matrix_world@v.co for v in ob.data.vertices]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source',required=True);parser.add_argument('--out',required=True)
    a=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.source);bpy.ops.wm.open_mainfile(filepath=str(src.resolve()));bpy.context.view_layer.update()
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')==S.ASSET_SET]
    errors=[];parts={};categories=Counter();assemblies=Counter();allpoints=[];rest_errors=[];glass=[];edge={}
    for ob in obs:
        ps=points(ob);allpoints.extend(ps);ob.data.calc_loop_triangles();count=len(ob.data.loop_triangles)
        parts[ob.name]=count;categories[ob['part_category']]+=count
        parent=ob.parent
        while parent.parent and parent.parent!=bpy.data.objects[S.NAME]:parent=parent.parent
        assemblies[parent.name]+=count
        attr=ob.data.attributes.get('VehicleRest')
        if attr is None:errors.append('No stable rest coordinates: '+ob.name)
        else:rest_errors.extend((p-d.vector).length for p,d in zip(ps,attr.data))
        if any(m.get('vehicle_paint') for m in ob.data.materials):
            attr=ob.data.attributes.get('WearEdgeDistance')
            if attr is None:errors.append('No measured paint-border distances: '+ob.name)
            else:edge[ob.name]=dict(min_m=min(d.value for d in attr.data),max_m=max(d.value for d in attr.data))
        if ob.get('part_category')=='glass':
            dots=[f.normal.dot(ob.data.corner_normals[li].vector) for f in ob.data.polygons for li in f.loop_indices]
            glass.append(dict(part=ob.name,minimum_corner_geometric_normal_dot=min(dots),opposed_corners=sum(d<-.02 for d in dots)))
            if any(d<-.02 for d in dots):errors.append('Opposed transmission normals: '+ob.name)
    low=[min(p[k] for p in allpoints) for k in range(3)];high=[max(p[k] for p in allpoints) for k in range(3)];size=[b-a for a,b in zip(low,high)]
    if any(abs(x-y)>t for x,y,t in zip(size,[2.117,4.600,1.735],[.010,.008,.005])):errors.append('Actual vertex envelope')
    if max(rest_errors)>1e-5:errors.append('Rest coordinates drift from actual positions')
    ground=min((p.z,o.name) for o in obs if o['part_category']=='underbody' for p in points(o))
    if abs(ground[0]-.205)>.001:errors.append('Actual ground clearance')
    pivots={};hinges=[];steering={}
    for ob in bpy.context.scene.objects:
        if 'pivot_axis' not in ob:continue
        direction=(ob.matrix_world.to_3x3()@Vector(tuple(1 if c==ob['pivot_axis'] else 0 for c in 'XYZ'))).normalized()
        pivots[ob.name]=dict(position_m=list(ob.matrix_world.translation),local_axis=ob['pivot_axis'],vehicle_axis=list(direction),range_degrees=list(ob.get('range_degrees',[])))
        if ob.name.startswith('Steer_'):
            hub=bpy.data.objects['Wheel_'+ob.name[-2:]].matrix_world.translation
            intercept=ob.matrix_world.translation-direction*(ob.matrix_world.translation.z/direction.z)
            steering[ob.name]=dict(inclination_degrees=math.degrees(math.atan2(abs(direction.x),direction.z)),caster_degrees=math.degrees(math.atan2(direction.y,direction.z)),scrub_m=abs(intercept.x-hub.x),trail_m=abs(intercept.y-hub.y))
    for code in ['FL','FR','RL','RR']:
        pivot=bpy.data.objects['Door_'+code];origin=pivot.matrix_world.translation;axis=Vector(pivots[pivot.name]['vehicle_axis'])
        for pin in [o for o in obs if o.name.startswith('Door hinge '+code) and o.name.endswith(' pin')]:
            center=sum(points(pin),Vector())/len(pin.data.vertices);delta=center-origin
            offset=(delta-axis*delta.dot(axis)).length
            hinges.append(dict(part=pin.name,axis_offset_m=offset))
            if offset>1e-5:errors.append('Door bearing not on actual hinge line: '+pin.name)
    strokes=[]
    for name in ['Hood','Liftgate']:
        pivot=bpy.data.objects[name];rest=pivot.matrix_basis.copy();limits=list(pivot['range_degrees']);sampled=[]
        barrels=[o for o in obs if o.get('support_pivot')==name and o.get('support_kind')=='barrel']
        lengths={o.name:max(v.co.z for v in o.data.vertices)-min(v.co.z for v in o.data.vertices) for o in barrels}
        rods={o.name:bpy.data.objects[o.name.removesuffix('barrel')+'rod'] for o in barrels}
        rodlengths={key:max(v.co.z for v in rod.data.vertices)-min(v.co.z for v in rod.data.vertices) for key,rod in rods.items()}
        for j in range(76):
            value=limits[0]+(limits[1]-limits[0])*j/75;pivot.matrix_basis=rest@Matrix.Rotation(math.radians(value),4,'X');update_supports()
            for barrel in barrels:
                distance=(pivot.matrix_world@Vector(barrel['support_moving_local'])-Vector(barrel['support_fixed'])).length
                sampled.append((barrel.name,distance))
        pivot.matrix_basis=rest;update_supports()
        for barrel in barrels:
            ds=[d for label,d in sampled if label==barrel.name];barrel_length=lengths[barrel.name];rod_length=rodlengths[barrel.name]
            clearance=min(ds)-max(barrel_length,rod_length);engagement=barrel_length+rod_length-max(ds)
            strokes.append(dict(part=barrel.name,barrel_mesh_length_m=barrel_length,rod_mesh_length_m=rod_length,attachment_distance_range_m=[min(ds),max(ds)],compressed_end_clearance_m=clearance,minimum_rod_engagement_m=engagement))
            if clearance<.005 or engagement<.02:errors.append('Impossible telescoping support stroke: '+barrel.name)
    if bpy.context.scene['quality']=='game' and sum(parts.values())>65000:errors.append('Game budget')
    supports=[]
    for code in ['FL','FR','RL','RR']:
        handle=bpy.data.objects['Pull handle '+code];seat=bpy.data.objects['Handle escutcheon '+code]
        skin=bpy.data.objects['Door '+code[0]+'_'+code[1]]
        crossings=len(tree_for([handle]).overlap(tree_for([seat])));nearest=min(tree_for([skin]).find_nearest(p)[3] for p in points(seat))
        supports.append(dict(parts=[handle.name,seat.name],triangle_crossings=crossings,seat_min_vertex_to_paint_m=nearest))
        if not crossings or nearest>.002:errors.append('Handle lacks a measured seat: '+code)
    resources=dict(source_materials=sorted({m.name for o in obs for m in o.data.materials}),source_images={im.name:list(im.size) for im in bpy.data.images if im.source=='FILE' and im.size[0]},delivery_plan=dict(texture_size=2048,maps=['BaseColor RGBA','OpenGL +Y Normal','ORM'],compressed_full_mips_MiB=16,status='planned; no SUV UV/bake/export at this checkpoint'))
    report=dict(passed=not errors,errors=errors,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),quality=bpy.context.scene['quality'],triangles=sum(parts.values()),categories=dict(categories),assemblies=dict(assemblies),parts=parts,actual_vertex_bounds_m=dict(min=low,max=high,size=size),underbody_lowest_m=ground[0],underbody_lowest_part=ground[1],rest_position_max_error_m=max(rest_errors),glass_normal_checks=glass,paint_border_distances=edge,pivots=pivots,steering=steering,hinge_axis_measurements=hinges,strut_strokes=strokes,measured_handle_supports=supports,resources=resources,scope='Source construction only; mechanical sweeps are separate; delivery is pending')
    Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(report,indent=2));print('SUV_CONSTRUCTION',report['passed'],report['triangles'],errors,flush=True)
    if errors:raise AssertionError(errors)

if __name__=='__main__':main()
