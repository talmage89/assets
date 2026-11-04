"""Independent plan constraints and actual-surface tests for the split type."""
import math
from split_plan import openings,roof_parts
from plan import roof_faces,roof_junctions,wall_frame


def check_plan(plan):
    s=plan['spec'];lv=plan['levels'];holes=openings(plan);errors=[]
    assert lv['lower']<lv['living']<lv['upper']
    assert abs(lv['upper']-lv['lower']-s['ceiling']-s['floor_zone'])<1e-8
    assert lv['lower']<0 and .3048<=lv['upper']<=2.5
    if s['kind']=='foyer':
        assert .6096-1e-8<=s['site_grade_m']-lv['lower']<=1.2192+1e-8
        lower_windows=[o for o in holes if o['role'].startswith('lower')]
        assert all(o['h']>=.9144-1e-8 and .10<=o['z']-s['site_grade_m']<=.21 for o in lower_windows)
    for stair in plan['stairs']:
        assert stair['riser_m']<=.19685 and stair['tread_m']>=.254
        assert stair['run_m']+stair['landing_m']<min(b.depth for b in plan['blocks'])-.6
    for o in holes:
        b=next(v for v in plan['blocks'] if v.name==o['block']);origin,t,n,length=wall_frame(b,o['face'])
        margin=o['w']+.11 if o['shutters'] else o['w']/2+.13
        if not margin+.015<=o['u']<=length-margin-.015:errors.append(o['id']+' corner trim')
        for u in (o['u']-o['w']/2-.08,o['u']+o['w']/2+.08):
            x=origin[0]+u*t[0];y=origin[1]+u*t[1]
            if o['z']+o['h']+.115>b.height(x,y)-.14:errors.append(o['id']+' roof/header')
        if o['shutters'] and o['style'] in ('picture','bay'):errors.append('Picture shutters')
        if b.stories==2 and o['kind']=='window':
            if o['z']<lv['upper'] and o['z']+o['h']>lv['upper']-s['floor_zone']-.08:errors.append(o['id']+' crosses floor zone')
        if b.stories==1 and o['z']<b.floor-.001:errors.append(o['id']+' below floor')
    for i,a in enumerate(holes):
        for c in holes[i+1:]:
            if (a['block'],a['face'])!=(c['block'],c['face']):continue
            half=lambda v:v['w']+.11 if v['shutters'] else v['w']/2+.12
            if abs(a['u']-c['u'])<half(a)+half(c) and min(a['z']+a['h']+.10,c['z']+c['h']+.10)>max(a['z']-.09,c['z']-.09):errors.append(a['id']+' overlaps '+c['id'])
    roof=roof_parts(plan);faces=roof_faces(roof);junctions=roof_junctions(roof);valleys=[]
    for row in junctions:
        if row['kind']=='valley':
            a,c=row['points'];fall=abs(a[2]-c[2])/math.dist(a[:2],c[:2]);valleys.append(fall)
            if fall<.019:errors.append('Level valley')
    d=plan['driveway'];slope=abs(d['back_z']-d['front_z'])/(d['back']-1.25-d['front'])
    if slope>.18:errors.append('Unusable driveway slope')
    if errors:raise AssertionError(f"Split {plan['seed']}: "+'; '.join(sorted(set(errors))))
    return dict(seed=plan['seed'],type='split',kind=s['kind'],openings=len(holes),roof_faces=len(faces),valley_min_fall=min(valleys) if valleys else None,levels_m=lv,stairs=plan['stairs'],driveway_slope=slope)


def source_check(source):
    import json
    import bpy
    from mathutils import Vector
    from check_mesh import surface
    from plan import generate
    bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));bpy.context.view_layer.update()
    meta=json.loads(source.with_suffix('.json').read_text());plan=generate(meta['seed'],meta['spec'],house_type='split');check_plan(plan)
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')];errors=[];count=0;tiny=0
    for ob in obs:
        ob.data.calc_loop_triangles();count+=len(ob.data.loop_triangles)
        tiny+=sum(t.area<1e-12 for t in ob.data.loop_triangles)
        if any(not all(math.isfinite(v) for v in p.co) for p in ob.data.vertices):errors.append('Nonfinite vertices')
    if tiny:errors.append(f'{tiny} degenerate triangles')
    if count!=meta['triangles'] or not 0<count<=80000:errors.append('Triangle count')
    materials=len({o.data.materials[p.material_index].as_pointer() for o in obs for p in o.data.polygons})
    if materials>6:errors.append('Material budget')
    roof=surface([o for o in obs if o.get('component')=='roof']);walls=surface([o for o in obs if o.get('component')=='wall'])
    parts=roof_parts(plan);points=[p for b in parts for p in b.domain()];x0=min(x for x,y in points);x1=max(x for x,y in points);y0=min(y for x,y in points);y1=max(y for x,y in points)
    roof_samples=0;missing=0;maxerror=0
    for j in range(53):
        y=y0+(j+.317)/53*(y1-y0)
        for i in range(83):
            x=x0+(i+.413)/83*(x1-x0);active=[b for b in parts if b.covers(x,y)]
            if not active:continue
            expected=max(b.height(x,y) for b in active);hit=roof.ray_cast(Vector((x,y,20)),Vector((0,0,-1)),30);roof_samples+=1
            if hit[0] is None:missing+=1
            else:maxerror=max(maxerror,abs(hit[0].z-expected))
    if missing or maxerror>2e-5:errors.append(f'Roof misses={missing} error={maxerror}')
    vent=bpy.data.objects.get('Plumbing_RoofVents');vent_clearance=None
    if vent:
        points=[vent.matrix_world@v.co for v in vent.data.vertices]
        top=max(p.z for p in points);tip=[p for p in points if abs(p.z-top)<1e-5]
        x=sum(p.x for p in tip)/len(tip);y=sum(p.y for p in tip)/len(tip)
        hit=roof.ray_cast(Vector((x,y,20)),Vector((0,0,-1)),30)[0]
        if hit is None:errors.append('Roof vent misses roof')
        else:
            vent_clearance=top-hit.z
            if vent_clearance<.30:errors.append('Roof vent below adjoining roof/eave')
    skirt_errors=[]
    if plan['spec']['kind']=='side':
        main,wing=plan['blocks'][:2]
        lower_roof=surface([o for o in obs if o.get('component')=='roof' and o.get('block')=='Main'])
        x=main.x1-.08 if wing.cx>main.cx else main.x0+.08
        for f in (.2,.5,.8):
            y=max(main.y0,wing.y0)+f*(min(main.y1,wing.y1)-max(main.y0,wing.y0))
            expected=main.height(x,y)
            if wing.height(x,y)<expected+.15:continue
            hit=lower_roof.ray_cast(Vector((x,y,expected+.10)),Vector((0,0,-1)),.3)[0]
            if hit is None:errors.append('Missing lower roofing beneath tall eave')
            else:skirt_errors.append(abs(hit.z-expected))
    opening_samples=0;blocked=[]
    for o in meta['openings']:
        block=next(b for b in plan['blocks'] if b.name==o['block']);origin,t,n,length=wall_frame(block,o['face']);normal=Vector((*n,0))
        for du in (-.25,0,.25):
            for dz in (.25,.5,.75):
                point=Vector((origin[0]+t[0]*(o['u']+du*o['w']),origin[1]+t[1]*(o['u']+du*o['w']),o['z']+o['h']*dz))+normal*.42
                if walls.ray_cast(point,-normal,.90)[0] is not None:blocked.append(o['id'])
                opening_samples+=1
    if blocked:errors.append('Blocked openings '+str(sorted(set(blocked))))
    # Actual horizontal landing and sill surfaces, independent of authored Z.
    m=plan['blocks'][0];landing=surface([o for o in obs if o.get('component')=='porch_steps'])
    p=Vector((plan['door_x'],m.y0-.45,5));hit=landing.ray_cast(p,Vector((0,0,-1)),8)[0]
    landing_z=None if hit is None else hit.z
    if landing_z is None or abs(landing_z-(plan['levels']['living']-.010))>2e-5:errors.append('Landing/threshold')
    # Ground-anchored solids are measured against the declared site plane;
    # rail posts are independently compared with the actual tread surfaces.
    grade=plan['spec']['site_grade_m'];ground_gaps={}
    for component in ('porch_steps','rear_landing','condenser','splash_block'):
        objects=[o for o in obs if o.get('component')==component]
        gaps=[min((o.matrix_world@v.co).z for v in o.data.vertices)-grade for o in objects]
        ground_gaps[component]=gaps
        if any(abs(g)>2e-5 for g in gaps):errors.append(component+' misses authored grade plane')
    rail=bpy.data.objects.get('Entry_IronRail');rail_contacts=[]
    if rail:
        rails=surface([rail])
        for x,y in json.loads(rail.get('contact_stations_xy','[]')):
            foot=rails.ray_cast(Vector((x,y,grade-2)),Vector((0,0,1)),8)[0]
            tread=landing.ray_cast(Vector((x,y,10)),Vector((0,0,-1)),15)[0]
            gap=None if foot is None or tread is None else foot.z-tread.z
            rail_contacts.append(dict(station_xy=(x,y),post_bottom_m=None if foot is None else foot.z,tread_m=None if tread is None else tread.z,gap_m=gap))
            if gap is None or abs(gap)>2e-5:errors.append('Rail post misses actual tread')
    flakes=[o for o in obs if o.get('component')=='paint_flakes'];paint_contact=None
    if flakes:
        sills=surface([o for o in obs if o.get('component') in ('window','storm_window')]);distances=[];signed=[]
        for ob in flakes:
            for v in ob.data.vertices:
                p=ob.matrix_world@v.co;q,normal,_,distance=sills.find_nearest(p)
                distances.append(distance);signed.append((p-q).dot(normal))
        paint_contact=dict(vertices=len(distances),max_distance_m=max(distances),min_outward_gap_m=min(signed),scope='Every flake/loss vertex against actual window surfaces; curled film may lift at most 4 mm. Excludes brick rowlocks and the differently shaped bay seat.')
        if max(distances)>.004 or min(signed)<-.00005:errors.append('Paint loss floats or is buried outside its actual sill surface')
    measured=[]
    for b in plan['blocks']:
        roofs=[o for o in obs if o.get('component')=='roof' and o.get('block')==b.name]
        if not roofs:continue
        values=[o.matrix_world@v.co for o in roofs for v in o.data.vertices]
        measured.append(dict(block=b.name,roof_bounds_m=[[min(v[k] for v in values) for k in range(3)],[max(v[k] for v in values) for k in range(3)]]))
    driveway=surface([o for o in obs if o.get('component')=='driveway']);d=plan['driveway'];apron=driveway.ray_cast(Vector((d['x'],d['back']-.4,5)),Vector((0,0,-1)),10)[0]
    if apron is None or abs(apron.z-(d['back_z']-.010))>2e-5:errors.append('Driveway apron misses door sill')
    result=dict(passed=not errors,errors=errors,triangles=count,materials=materials,degenerate_triangles=tiny,roof_rays=roof_samples,roof_missing=missing,max_roof_error_m=maxerror,vent_tip_above_roof_measured_m=vent_clearance,lower_roof_under_eave_error_m=skirt_errors,opening_rays=opening_samples,landing_top_measured_m=landing_z,driveway_apron_measured_m=apron.z if apron else None,roof_measurements=measured,measured_ground_solid_gaps_m=ground_gaps,measured_rail_tread_contacts=rail_contacts,measured_paint_surface_contact=paint_contact,
                scope='Actual mesh surface roof/opening/landing/apron probes; geometry and material budget. Separate GLB import and moving-leaf tests prove serialization and sampled clearance.')
    if errors:raise AssertionError(result)
    return result
