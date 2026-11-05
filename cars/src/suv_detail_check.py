"""Actual triangle/axis/attribute/strut measurements for the source checkpoint.

This checks construction, separately from kit.audit and the sampled solid
motion test. It makes no UV, bake, serialization or final GLB claim.
"""
import argparse,hashlib,json,math,sys
from collections import Counter
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from suv_mechanics import update_supports
from suv_exterior import tree_for
import suv_spec as S


def points(ob):return [ob.matrix_world@v.co for v in ob.data.vertices]

def laminate(ob):
    """Independent entrance/exit shading-normal rays through actual glass."""
    me=ob.data;me.calc_loop_triangles();ps=points(ob);ts=list(me.loop_triangles)
    tree=BVHTree.FromPolygons(ps,[tuple(t.vertices) for t in ts],all_triangles=True)
    matrix=ob.matrix_world.to_3x3().inverted().transposed();angles=[];thickness=[]
    def normal(hit,index):
        t=ts[index];return barycentric_transform(hit,*[ps[i] for i in t.vertices],*[matrix@me.corner_normals[i].vector for i in t.loops]).normalized()
    sign=-1 if ob.name.endswith('_L') else 1;direction=Vector((-sign,0,0))
    yl,yh=min(p.y for p in ps),max(p.y for p in ps);zl,zh=min(p.z for p in ps),max(p.z for p in ps)
    for j in range(13):
        for k in range(13):
            origin=Vector((sign*2,yl+(yh-yl)*(.08+.84*j/12),zl+(zh-zl)*(.08+.84*k/12)))
            hit,ng,fi,_=tree.ray_cast(origin,direction,2)
            if hit is None or abs(ng.x)<.6:continue
            end,back,bi,_=tree.ray_cast(hit+direction*.00005,direction,.02)
            if end is None or ng.dot(back)>-.7 or not .002<(end-hit).length<.010:continue
            angles.append(math.degrees(normal(hit,fi).angle(-normal(end,bi))));thickness.append((end-hit).length)
    # Five degrees admits the tightly curved lower A-corner and coarse chord
    # interpolation. The 48-degree rim/pane mix that broke the cabin fails it.
    return dict(part=ob.name,probe_count=len(angles),mean_normal_mismatch_degrees=sum(angles)/len(angles) if angles else None,max_normal_mismatch_degrees=max(angles) if angles else None,ray_thickness_range_m=[min(thickness),max(thickness)] if thickness else None,tolerance_degrees=5)

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
    optical=[laminate(ob) for ob in obs if 'side glazing_' in ob.name]
    for row in optical:
        if not row['probe_count'] or row['max_normal_mismatch_degrees']>row['tolerance_degrees']:errors.append('Glass laminate acts as an optical prism: '+row['part'])
    liner_normals=[]
    for sign in [-1,1]:
        ob=bpy.data.objects['Cargo quarter molded liner '+str(sign)];me=ob.data;count=ob['trim_sheet_vertex_count'];role=me.attributes.get('skin_face_role')
        faces=[f for f in me.polygons if (role.data[f.index].value==0 if role else all(i<count for i in f.vertices)) and .77<f.center.z<1.0 and f.center.y<1.9]
        facing=sum(f.area*f.normal.x*(-sign) for f in faces)/sum(f.area for f in faces)
        liner_normals.append(dict(part=ob.name,area_weighted_inward_normal_component=facing))
        if facing<.5:errors.append('Cargo visible liner faces away from cavity: '+ob.name)
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
    for y in [-.77,.55,1.68]:
        hanger=bpy.data.objects['Exhaust hanger '+str(y)];carrier=bpy.data.objects['Unibody rail 1' if y>1 else 'Cabin floor']
        crossings=len(tree_for([hanger]).overlap(tree_for([carrier])))
        supports.append(dict(parts=[hanger.name,carrier.name],triangle_crossings=crossings))
        if not crossings:errors.append('Exhaust hanger lacks a body attachment: '+str(y))
    for sign in [-1,1]:
        seat=bpy.data.objects['Hood strut '+str(sign)+' body ball seat'];ret=bpy.data.objects['Hood strut body return '+str(sign)];fender=bpy.data.objects['Front fender_'+('L' if sign<0 else 'R')]
        crossings=len(tree_for([seat]).overlap(tree_for([ret])));attachment=len(tree_for([ret]).overlap(tree_for([fender])))
        plate=bpy.data.objects['Hood hinge '+str(sign)];hoodtree=tree_for([bpy.data.objects['Hood outer']]);distance=min(hoodtree.find_nearest(p)[3] for p in points(plate))
        supports.append(dict(parts=[seat.name,ret.name,fender.name,plate.name],seat_return_triangle_crossings=crossings,return_fender_triangle_crossings=attachment,hinge_to_inner_skin_min_vertex_distance_m=distance))
        if not crossings or not attachment or distance>.002:errors.append('Unsupported hood mounting hardware: '+str(sign))
    for code in ['FL','FR','RL','RR']:
        handle=bpy.data.objects['Pull handle '+code];seat=bpy.data.objects['Handle escutcheon '+code]
        skin=bpy.data.objects['Door '+code[0]+'_'+code[1]]
        crossings=len(tree_for([handle]).overlap(tree_for([seat])));nearest=min(tree_for([skin]).find_nearest(p)[3] for p in points(seat))
        supports.append(dict(parts=[handle.name,seat.name],triangle_crossings=crossings,seat_min_vertex_to_paint_m=nearest))
        if not crossings or nearest>.002:errors.append('Handle lacks a measured seat: '+code)
    resources=dict(source_materials=sorted({m.name for o in obs for m in o.data.materials}),source_images={im.name:list(im.size) for im in bpy.data.images if im.source=='FILE' and im.size[0]},delivery_plan=dict(texture_size=2048,maps=['BaseColor RGBA','OpenGL +Y Normal','ORM'],compressed_full_mips_MiB=16,status='planned; no SUV UV/bake/export at this checkpoint'))
    report=dict(passed=not errors,errors=errors,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),quality=bpy.context.scene['quality'],triangles=sum(parts.values()),categories=dict(categories),assemblies=dict(assemblies),parts=parts,actual_vertex_bounds_m=dict(min=low,max=high,size=size),underbody_lowest_m=ground[0],underbody_lowest_part=ground[1],rest_position_max_error_m=max(rest_errors),glass_normal_checks=glass,glass_laminate_rays=optical,cargo_liner_normals=liner_normals,paint_border_distances=edge,pivots=pivots,steering=steering,hinge_axis_measurements=hinges,strut_strokes=strokes,measured_fitting_supports=supports,resources=resources,scope='Source construction only; mechanical sweeps are separate; delivery is pending')
    Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(report,indent=2));print('SUV_CONSTRUCTION',report['passed'],report['triangles'],errors,flush=True)
    if errors:raise AssertionError(errors)

if __name__=='__main__':main()
