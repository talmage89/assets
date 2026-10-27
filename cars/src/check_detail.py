"""Independent source measurements: coordinates, optics, brake and static fits.

Not a UV, export or full motion certificate. Checks actual mesh surfaces, not
comments or shape parameters, and records source hashes for the review gate.
"""
import argparse,hashlib,json,sys,math
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
import pickup_spec as S


def points(ob):return [ob.matrix_world@v.co for v in ob.data.vertices]
def tree(ob):return BVHTree.FromPolygons(points(ob),[tuple(f.vertices) for f in ob.data.polygons])
def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve();bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.view_layer.update()
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')];errors=[];rest=[]
    for ob in obs:
        attr=ob.data.attributes.get('VehicleRest')
        if attr is None:errors.append('Missing rest positions: '+ob.name);continue
        rest.extend((p-attr.data[i].vector).length for i,p in enumerate(points(ob)))
    if max(rest)>1e-5:errors.append('Wear position attribute differs from actual world positions')
    under=[o for o in obs if o['part_category']=='underbody'];clear=min(p.z for o in under for p in points(o))
    if abs(clear-S.GROUND_CLEARANCE_TARGET)>.001:errors.append('Actual underbody ground clearance')
    gauges=[]
    for ob in obs:
        count=ob.get('sheet_vertex_count')
        if count:
            ps=points(ob);offsets=[(ps[i+count]-ps[i]).length for i in range(count)]
            gauges.append(dict(part=ob.name,max_offset_m=max(offsets),specified_gauge_m=ob['sheet_gauge_m']))
            if max(offsets)>ob['sheet_gauge_m']*1.1:errors.append('Exploded sheet-gauge miter '+ob.name)
    wheels={};axial=[]
    for code in ['FL','FR','RL','RR']:
        cx,y,z=bpy.data.objects['Wheel_'+code].matrix_world.translation
        sign=-1 if code[-1]=='L' else 1
        cal=bpy.data.objects['Brake caliper_'+code];cp=points(cal)
        spokes=[o for o in obs if o.name.startswith('Cast spoke_'+code+'_')]
        wheel=tree(bpy.data.objects['Wheel barrel_'+code]);clearance=min(wheel.find_nearest(p)[3] for p in cp)
        spoke_in=min(sign*(p.x-cx) for o in spokes for p in points(o));cal_out=max(sign*(p.x-cx) for p in cp)
        separation=spoke_in-cal_out;axial.append(separation)
        wheels[code]=dict(caliper_to_barrel_min_vertex_surface_m=clearance,spoke_caliper_axial_gap_m=separation,
          caliper_parent=cal.parent.name,spoke_parent=spokes[0].parent.name)
        if separation<.010 or clearance<.004:errors.append('Brake clearance '+code)
        if cal.parent.name=='Wheel_'+code:errors.append('Caliper rotates with wheel '+code)
    mirror_sections=[]
    for side in ['L','R']:
        ob=bpy.data.objects['Molded mirror shell_'+side];ps=points(ob);count=ob['section_vertices'];minimum=1
        for row in range(ob['housing_sections']):
            loop=ps[row*count:(row+1)*count]
            for i in range(count):
                va,vb,vc=loop[i-1],loop[i],loop[(i+1)%count]
                cross=(vb.x-va.x)*(vc.z-vb.z)-(vb.z-va.z)*(vc.x-vb.x);minimum=min(minimum,cross)
        mirror_sections.append(dict(part=ob.name,minimum_convex_cross_m2=minimum))
        if minimum< -1e-9:errors.append('Folded mirror housing section '+side)
    sill_gaps={}
    for side in ['L','R']:
        sill=tree(bpy.data.objects['Rocker return_'+side]);ds=[]
        for end in ['F','R']:
            door=bpy.data.objects['Door skin_'+end+side];ps=points(door);lo=min(p.z for p in ps[:door['sheet_vertex_count']])
            ds.extend(sill.find_nearest(p)[3] for p in ps[:door['sheet_vertex_count']] if abs(p.z-lo)<1e-5 and S.DOOR_FRONT+.10<p.y<S.DOOR_REAR-.10)
        sill_gaps[side]=dict(samples=len(ds),min_m=min(ds),max_m=max(ds))
        if min(ds)<.004 or max(ds)>.0052:errors.append('Door-to-sill gap '+side)
    supports=[]
    for code in ['FL','FR','RL','RR']:
        sign=-1 if code[-1]=='L' else 1
        spindle=bpy.data.objects['Hub bearing spindle_'+code[0]+str(sign)];hub=bpy.data.objects['Wheel center_'+code]
        crossings=len(tree(spindle).overlap(tree(hub)));supports.append(dict(parts=[spindle.name,hub.name],crossing_triangle_pairs=crossings))
        if not crossings:errors.append('Unsupported hub '+code)
    cable=bpy.data.objects['Spare hanger'];beam=bpy.data.objects['Frame crossmember 2.25']
    crossings=len(tree(cable).overlap(tree(beam)));supports.append(dict(parts=[cable.name,beam.name],crossing_triangle_pairs=crossings))
    if not crossings:errors.append('Spare hanger misses crossmember')
    for mount in ['Skid frame mount -2.3','Skid frame mount -1.65']:
        plate=bpy.data.objects['Front formed skid'];crossings=len(tree(plate).overlap(tree(bpy.data.objects[mount])));supports.append(dict(parts=[plate.name,mount],crossing_triangle_pairs=crossings))
        if not crossings:errors.append('Skid misses frame support '+mount)
    clear_pairs=[]
    for one,two in [('Front formed skid','Front differential')]+[('Front halfshaft '+str(sign),'Front strut_'+str(sign)) for sign in [-1,1]]:
        crossings=len(tree(bpy.data.objects[one]).overlap(tree(bpy.data.objects[two])));clear_pairs.append(dict(parts=[one,two],crossing_triangle_pairs=crossings))
        if crossings:errors.append('Underbody surface interference '+one+' / '+two)
    glass=[o for o in obs if o.get('part_category')=='glass'];lamp=[]
    from forms import lamp_surface,side_x
    for sign in [-1,1]:
        ob=bpy.data.objects['Headlamp envelope_'+str(sign)];ps=points(ob)
        terminal=[p for p in ps if abs(p.y+2.499)<1e-5]
        inset=[side_x(p.y,p.z)-abs(p.x) for p in terminal]
        lamp.append(dict(side=sign,terminal_samples=len(inset),fender_inset_m=[min(inset),max(inset)]))
        if min(inset)<-.001 or max(inset)>.007:errors.append('Lamp wrap outboard/too recessed')
    # Fit the ACTUAL outer surround vertices to its face plane, then compare
    # actual frontmost lamella vertices. This measures recess, not an input.
    rim=points(bpy.data.objects['Grille form surround']);stride=len(rim)//8
    # Solidify doubles the original four equally sampled perimeter rings.
    outer=[p for p in rim[:stride] if abs(p.x)<.65]
    mz=sum(p.z for p in outer)/len(outer);my=sum(p.y for p in outer)/len(outer)
    slope=sum((p.z-mz)*(p.y-my) for p in outer)/sum((p.z-mz)**2 for p in outer)
    recess=[]
    for ob in obs:
        if ob.name.startswith('Alder grille lamella_'):
            values=[p.y-(my+slope*(p.z-mz)) for p in points(ob)]
            recess.append(dict(part=ob.name,min_m=min(values),max_m=max(values)))
            if min(values)<.060 or min(values)>.100:errors.append('Grille depth '+ob.name)
    hood=bpy.data.objects['Hood outer'];hp=points(hood)[:hood['sheet_vertex_count']]
    # Front rows are the first vertices in the authored skin grid.
    front_y=min(p.y for p in hp);front=[p for p in hp if p.y<front_y+.007 and abs(p.x)<.63]
    rv=tree(bpy.data.objects['Grille form surround']);gaps=[rv.find_nearest(p)[3] for p in front]
    hood_gap=dict(samples=len(gaps),min_m=min(gaps),max_m=max(gaps))
    if min(gaps)<.002 or max(gaps)>.016:errors.append('Hood/surround shut line')
    laminate=[]
    for ob in obs:
        count=ob.get('sheet_vertex_count')
        if not count or not any(m.get('vehicle_glass') for m in ob.data.materials):continue
        front={}
        for face in ob.data.polygons[:ob['outer_skin_faces']]:
            for li in face.loop_indices:front[ob.data.loops[li].vertex_index]=ob.data.corner_normals[li].vector.copy()
        deviations=[]
        for face in ob.data.polygons:
            if all(i>=count for i in face.vertices):
                for li in face.loop_indices:
                    expected=-front[ob.data.loops[li].vertex_index-count]
                    deviations.append(math.degrees(expected.angle(ob.data.corner_normals[li].vector)))
        laminate.append(dict(part=ob.name,exit_normal_samples=len(deviations),max_paired_normal_deviation_degrees=max(deviations)))
        if max(deviations)>.1:errors.append('Faceted inner glazing '+ob.name)
    required=['Fuel_Door','Mirror_L','Mirror_R','Tailgate','Hood','Door_FL','Door_FR','Door_RL','Door_RR','Wiper_0','Wiper_1']
    pivots={n:dict(position_m=list(bpy.data.objects[n].matrix_world.translation),axis=bpy.data.objects[n].get('pivot_axis'),range_degrees=list(bpy.data.objects[n].get('range_degrees',[]))) for n in required}
    mats={m.name for o in obs for m in o.data.materials};images={im.name:list(im.size) for im in bpy.data.images if im.source=='FILE' and im.size[0]>0}
    report=dict(source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),quality=bpy.context.scene['quality'],
       sheet_gauge_measurements=gauges,rest_position_max_error_m=max(rest),actual_underbody_ground_clearance_m=clear,
       wheel_static_clearances=wheels,mirror_section_checks=mirror_sections,door_sill_gaps=sill_gaps,measured_support_intersections=supports,underbody_noninterference=clear_pairs,lamp_wrap_insets=lamp,grille_lamella_recess=recess,hood_surround_shutline=hood_gap,glass_paired_normal_checks=laminate,pivots=pivots,source_materials=sorted(mats),original_source_images=images,
       passed=not errors,errors=errors,pending=['continuous loaded tire deformation when rolling','kingpin caster/SAI and full wheel steering sweep','doors/hood/tailgate/wiper full assembly sweeps','UV/bake/export/re-import and delivery material verification'])
    Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
    if errors:raise AssertionError(errors)

if __name__=='__main__':main()
