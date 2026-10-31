"""Independent Cape plan constraints and actual source-surface probes.

Analytic grammar, physical ray tests, and serialization have distinct scopes.
"""
import math
from cape_plan import roof_parts
from plan import openings,wall_frame,roof_faces,roof_junctions


def check_plan(plan):
    blocks=plan['blocks'];m=blocks[0];s=plan['spec'];holes=openings(plan);errors=[];faces=roof_faces(roof_parts(plan));samples=0
    for o in holes:
        b=next(v for v in blocks if v.name==o['block']);origin,t,n,length=wall_frame(b,o['face'])
        margin=o['w']+.11 if o['shutters'] else o['w']/2+.12
        if o['u']-margin<.02 or o['u']+margin>length-.02:errors.append(o['id']+' corner')
        for u in (o['u']-o['w']/2-.09,o['u']+o['w']/2+.09):
            x=origin[0]+u*t[0];y=origin[1]+u*t[1]
            if o['z']+o['h']+.11>b.height(x,y)-.14:errors.append(o['id']+' roof/header')
        dorm=b.name.startswith('Dormer') or b.name=='RearShed'
        if dorm:
            bottom=m.height(origin[0]+t[0]*o['u'],origin[1]+t[1]*o['u'])
            if o['z']<bottom+.07:errors.append(o['id']+' roof cuts sill')
        if o['kind']=='window' and not dorm and o['z']<b.floor:errors.append(o['id']+' crosses floor')
    for i,a in enumerate(holes):
        for c in holes[i+1:]:
            if (a['block'],a['face'])!=(c['block'],c['face']):continue
            margin=lambda o:o['w']+.11 if o['shutters'] else o['w']/2+.12
            if abs(a['u']-c['u'])<margin(a)+margin(c) and min(a['z']+a['h']+.10,c['z']+c['h']+.10)>max(a['z']-.08,c['z']-.08):errors.append(a['id']+' overlaps '+c['id'])
    if s['dormers']==3 and m.width<30*.3048-1e-6:errors.append('Three dormers require five-bay width')
    for d in [b for b in blocks if b.name.startswith('Dormer')]:
        if d.height(d.cx,d.cy)>m.height(d.cx,m.cy)-.10:errors.append('Dormer ridge higher than parent')
        if d.y0-m.y0<.49:errors.append('Dormer at wall face')
    lower=sorted(m.x0+o['u'] for o in holes if o['block']=='Main' and o['face']=='front' and o['kind']=='window')
    if s['dormers']:
        bays=lower if s['dormers']==2 else [sum(lower[:2])/2,plan['door_x'],sum(lower[2:])/2]
        if any(abs(a-c)>1e-6 for a,c in zip(plan['dormer_centers'],bays)):errors.append('Dormers not centered over facade bays')
    soffit=m.eave-m.pitch*m.overhang-.151
    for o in holes:
        if o['block']=='Main' and o['face']=='front' and o['z']<m.upper_floor and o['z']+o['h']+.11>soffit:errors.append('First-floor head intersects eave')
    for row in faces:
        poly=row['polygon'];cx=sum(x for x,y in poly)/len(poly);cy=sum(y for x,y in poly)/len(poly);a,b,c=row['plane']
        for x0,y0 in poly:
            x=.85*cx+.15*x0;y=.85*cy+.15*y0;z=a*x+b*y+c
            expected=max(v.height(x,y) for v in roof_parts(plan) if all(a*x+b*y+c>=-1e-6 for a,b,c in v.occlusion_constraints()) or v.name==row['block'])
            if abs(z-expected)>1e-5:errors.append('Buried roof');
            samples+=1
    valleys=[]
    for row in roof_junctions(roof_parts(plan)):
        if row['kind']!='valley':continue
        a,c=row['points'];fall=abs(a[2]-c[2])/math.dist(a[:2],c[:2]);valleys.append(fall)
        # Main/shed intersection joins two planes falling in the same
        # direction. Water crosses this pitch break, not along its level X.
        if set(row['blocks'])=={'Main','RearShed'}:
            continue
        if fall<.019:errors.append('Level valley')
    if errors:raise AssertionError(f"Cape seed {plan['seed']}: "+'; '.join(sorted(set(errors))))
    return dict(seed=plan['seed'],type='cape',openings=len(holes),roof_faces=len(faces),roof_samples=samples,min_valley_fall=min(valleys) if valleys else None)


def source_check(source):
    import json
    import bpy
    from mathutils import Vector
    from check_mesh import surface
    from plan import generate
    bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));bpy.context.view_layer.update()
    meta=json.loads(source.with_suffix('.json').read_text());plan=generate(meta['seed'],meta['spec'],house_type='cape');check_plan(plan)
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')];errors=[];tri=0;tiny=0
    for ob in obs:
        ob.data.calc_loop_triangles();tri+=len(ob.data.loop_triangles);tiny+=sum(t.area<1e-12 for t in ob.data.loop_triangles)
        if any(not all(math.isfinite(c) for c in v.co) for v in ob.data.vertices):errors.append('Nonfinite vertices')
    if tiny:errors.append(f'{tiny} degenerate triangles')
    material_count=len({ob.data.materials[p.material_index].as_pointer() for ob in obs for p in ob.data.polygons})
    if material_count>6:errors.append('More than six used materials')
    if not 0<tri<=80000 or tri!=meta['triangles']:errors.append('Budget/report mismatch')
    roof=surface([o for o in obs if o.get('component')=='roof']);walls=surface([o for o in obs if o.get('component')=='wall']);services=surface([o for o in obs if o.get('component')=='services'])
    parts=roof_parts(plan);points=[p for b in parts for p in b.domain()];x0=min(x for x,y in points);x1=max(x for x,y in points);y0=min(y for x,y in points);y1=max(y for x,y in points)
    samples=0;missing=0;error=0
    for j in range(73):
        y=y0+(j+.372)/73*(y1-y0)
        for i in range(103):
            x=x0+(i+.417)/103*(x1-x0);active=[b for b in parts if b.covers(x,y)]
            if not active:continue
            z=max(b.height(x,y) for b in active);hit=roof.ray_cast(Vector((x,y,20)),Vector((0,0,-1)),25);samples+=1
            if hit[0] is None:missing+=1
            else:
                error=max(error,abs(hit[0].z-z))
                if hit[1].z<.05:errors.append('Inward roof')
    if missing or error>2e-5:errors.append(f'Roof rays missing {missing}, max {error}')
    blocked=[];fixtures=[]
    for o in meta['openings']:
        b=next(v for v in plan['blocks'] if v.name==o['block']);origin,t,n,l=wall_frame(b,o['face']);normal=Vector((*n,0))
        for du in (-.25,0,.25):
            for dz in (.25,.5,.75):
                p=Vector((origin[0]+t[0]*(o['u']+du*o['w']),origin[1]+t[1]*(o['u']+du*o['w']),o['z']+o['h']*dz))+normal*.32
                if walls.ray_cast(p,-normal,.56)[0] is not None:blocked.append(o['id'])
                if services.ray_cast(p,-normal,.56)[0] is not None:fixtures.append(o['id'])
    if blocked:errors.append('Blocked openings '+str(sorted(set(blocked))))
    if fixtures:errors.append('Services at openings '+str(sorted(set(fixtures))))
    # Measured front eave/rake spans from roof vertices, independent of spec.
    main=plan['blocks'][0];v=[ob.matrix_world@v.co for ob in obs if ob.get('component')=='roof' and ob.get('block')=='Main' for v in ob.data.vertices]
    eave=main.y0-min(p.y for p in v);rake=main.x0-min(p.x for p in v)
    if abs(eave-main.overhang)>1e-5 or abs(rake-main.rake)>1e-5:errors.append('Actual tight overhangs mismatch')
    # Detect a parent roof across a dormer bedroom: upward rays inside the
    # opening must reach the dormer's own roof, not the parent plane below it.
    cheek=[]
    for d in [v for v in parts if v.name.startswith('Dormer')]:
        p=Vector((d.cx,d.y0+.2,d.floor+.4));hit=roof.ray_cast(p,Vector((0,0,1)),5)[0]
        if hit is None or abs(hit.z-(d.height(p.x,p.y)-.14))>2e-5:errors.append('Dormer space obstructed')
        cheek.append(dict(name=d.name,inside_ceiling_z=hit.z if hit else None))
    # Test the roofing underneath the dormer overhang skirts separately.
    parent=surface([o for o in obs if o.get('component')=='roof' and o.get('block')=='Main'])
    skirt_gaps=[]
    for d in [v for v in parts if v.name.startswith('Dormer')]:
        x=d.x0-.035;y=d.y0+.15;hit=parent.ray_cast(Vector((x,y,20)),Vector((0,0,-1)),25)[0]
        if hit is None:errors.append('Missing parent roofing under dormer skirt')
        else:skirt_gaps.append(abs(hit.z-main.height(x,y)))
    if skirt_gaps and max(skirt_gaps)>2e-5:errors.append('Dormer skirt contact')
    soffits=surface([o for o in obs if o.get('component')=='eave_rake_soffit' and o.get('block')=='Main'])
    header_clearances=[]
    for ob in obs:
        if ob.get('component')!='window' or not ob.get('opening'):continue
        o=json.loads(ob['opening'])
        if o['block']!='Main' or o['face']!='front':continue
        points=[ob.matrix_world@v.co for v in ob.data.vertices];top=max(v.z for v in points)
        x=main.x0+o['u'];hit=soffits.ray_cast(Vector((x,main.y0-.06,top+.001)),Vector((0,0,1)),2)[0]
        if hit is None:errors.append('Missing soffit above casing')
        else:header_clearances.append(hit.z-top)
    if header_clearances and min(header_clearances)<.004:errors.append('Casing touches soffit')
    steps=surface([o for o in obs if o.get('component')=='porch_steps'])
    tops=[];y=main.y0;doorx=plan['door_x']
    hit=steps.ray_cast(Vector((doorx,y-.5,4)),Vector((0,0,-1)),5)[0]
    if hit is None:errors.append('No landing surface')
    else:
        tops.append(hit.z);count=math.ceil((main.floor-.010)/.19)
        for j in range(count-1):
            hit=steps.ray_cast(Vector((doorx,y-1.02-(j+.5)*.28,4)),Vector((0,0,-1)),5)[0]
            if hit is None:errors.append('Missing tread')
            else:tops.append(hit.z)
    risers=[a-c for a,c in zip(sorted(tops,reverse=True),sorted(tops,reverse=True)[1:]+[0])]
    if risers and (max(risers)>.191 or max(risers)-min(risers)>.001):errors.append('Unequal or tall risers')
    foundation=surface([o for o in obs if o.get('component')=='foundation' and o.get('block')=='Main'])
    siding_bottom=min((ob.matrix_world@v.co).z for ob in obs if ob.get('component')=='wall' and ob.get('block')=='Main' for v in ob.data.vertices)
    concrete_top=max((ob.matrix_world@v.co).z for ob in obs if ob.get('component')=='foundation' and ob.get('block')=='Main' for v in ob.data.vertices)
    if not .2032-1e-5<=concrete_top<=.6096+1e-5:errors.append('Foundation exposure outside 8–24 inches')
    if abs(siding_bottom-concrete_top)>1e-5:errors.append('Siding covers foundation')
    if not .06<main.floor-concrete_top<.17:errors.append('Foundation does not meet sill/floor structure')
    if tops and abs(tops[0]-(main.floor-.010))>1e-5:errors.append('Stoop/threshold mismatch')
    threshold=surface([o for o in obs if o.get('component')=='door_frame'])
    # Probe inside the threshold's rounded leading edge, where the flat
    # underside actually bears on the concrete landing.
    threshold_bottom=threshold.ray_cast(Vector((doorx,y-.08,0)),Vector((0,0,1)),2)[0]
    threshold_gap=abs(threshold_bottom.z-tops[0]) if threshold_bottom is not None and tops else None
    if threshold_gap is None or threshold_gap>1e-5:errors.append('Landing does not bear on threshold underside')
    from cape_build import basement_holes
    from types import SimpleNamespace
    vent_probes=0
    for face in ('front','back'):
        origin,t,n,l=wall_frame(main,face);normal=Vector((*n,0))
        for u,z,w,h in basement_holes(SimpleNamespace(plan=plan),main,face):
            p=Vector((origin[0]+t[0]*u,origin[1]+t[1]*u,z+h/2))+normal*.25
            if foundation.ray_cast(p,-normal,.6)[0] is not None:errors.append('Foundation opening blocked')
            vent_probes+=1
    if not vent_probes:errors.append('Missing basement/crawl opening')
    supports=surface([o for o in obs if o.get('component') in ('wall','corner_posts')])
    support_dist=[]
    for d in meta['drains']:
        p=Vector(d['centerline'][3]);distance=supports.find_nearest(p)[3];support_dist.append(distance)
    if support_dist and max(support_dist)>.18:errors.append('Unsupported downspout body')
    # Roof pitch measured from triangle normals, not the input coefficient.
    normals=[t.normal for ob in obs if ob.get('component')=='roof' and ob.get('block')=='Main' for t in ob.data.loop_triangles if t.normal.z>.2]
    observed_pitch=max(abs(n.y/n.z) for n in normals)
    if abs(observed_pitch-main.pitch)>1e-4:errors.append('Measured roof pitch mismatch')
    result=dict(passed=not errors,errors=errors,triangles=tri,tiny_triangles=tiny,roof_samples=samples,roof_missing=missing,roof_max_error_m=error,opening_probes=len(meta['openings'])*9,front_eave_m=eave,rake_m=rake,dormer_interior=cheek,dormer_skirt_contact_max_m=max(skirt_gaps) if skirt_gaps else 0,window_head_soffit_clearances_m=header_clearances,stoop_tread_tops_m=tops,stoop_risers_m=risers,downspout_support_max_m=max(support_dist) if support_dist else 0,measured_pitch=observed_pitch,scope='Actual source roof/holes/services/dormer interior; no bake, UV or delivery certification')
    result.update(materials=material_count,foundation_exposure_m=concrete_top,foundation_to_floor_m=main.floor-concrete_top,siding_bottom_m=siding_bottom,foundation_opening_probes=vent_probes,threshold_to_stoop_m=main.floor-tops[0] if tops else None,landing_threshold_contact_error_m=threshold_gap)
    source.with_suffix('.check.json').write_text(json.dumps(result,indent=2))
    if errors:raise AssertionError(str(source)+': '+'; '.join(errors))
    return result
