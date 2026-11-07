"""Independent construction and serialization checks for the look-dev gate.

Physical tile UVs and shared bakes are audited separately. Accessibility,
engineering, complete interiors and a lightmap unwrap are outside this gate.
"""
import hashlib,json,math,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(HERE),str(ROOT)]
from kit.gltf import GLB
from plans import school,validate,SEEDS


def external(path):
    raw=object.__new__(GLB);raw.json=json.loads(path.read_text());raw.binary=(path.parent/raw.json['buffers'][0]['uri']).read_bytes();raw.parents={c:i for i,n in enumerate(raw.json['nodes']) for c in n.get('children',[])};return raw


def tree(obs):
    verts=[];faces=[]
    for ob in obs:
        off=len(verts);verts += [ob.matrix_world@v.co for v in ob.data.vertices]
        faces += [tuple(off+i for i in p.vertices) for p in ob.data.polygons]
    return BVHTree.FromPolygons(verts,faces,all_triangles=False)


def door_sweeps(portable_only=False):
    sweeps=[]
    for pv in list(bpy.context.scene.objects):
        if pv.get('pivot_axis')!='Z' or '_Door_' not in pv.name:continue
        if portable_only and '__Portable_' not in pv.name:continue
        prefix,tail=pv.name.rsplit('_Door_',1);index=tail.split('_')[0]
        frame=bpy.data.objects.get(prefix+'_DoorFrame_'+index)
        if not frame:continue
        fixed=tree([frame]);moving=[o for o in pv.children if o.type=='MESH'];rest=pv.matrix_basis.copy();bad=[];nearbad=[]
        # Source surfaces, including canopy columns and the other leaves
        # at rest. Cylindrical jamb knuckles are intended hinge contacts.
        neighbors=tree([o for o in bpy.context.scene.objects if o.type=='MESH' and o not in moving and o is not frame and o.get('component')!='hinge'])
        for angle in np.linspace(*pv['range_degrees'],21):
            pv.matrix_basis=rest@Matrix.Rotation(math.radians(float(angle)),4,'Z');bpy.context.view_layer.update()
            for ob in moving:
                overlap=tree([ob]).overlap(fixed)
                if overlap:bad.append(dict(angle=float(angle),triangle_pairs=len(overlap)))
                overlap=tree([ob]).overlap(neighbors)
                if overlap:nearbad.append(dict(angle=float(angle),triangle_pairs=len(overlap)))
        pv.matrix_basis=rest;bpy.context.view_layer.update()
        # The kit adds solid-parity / edge-interval penetration to the strict
        # crossing test. Scope it to the closed casing; the neighbor crossing
        # test above also includes open building skins and room witness planes.
        from kit.motion import sweep
        excluded=[o.name for o in bpy.context.scene.objects if o.type=='MESH' and o is not frame and o not in moving]
        volume=sweep(dict(MOTIONS=[dict(node=pv.name,axis='Z',range=list(pv['range_degrees']),step=4.5,tolerance_m=.0005,exclude_fixed=excluded)]))
        sweeps.append(dict(pivot=pv.name,sampled_poses=21,casing_intersections=bad,neighbor_intersections=nearbad,kit_casing_volume=volume))
    return sweeps


def ground_clearance():
    """Measure operating leaf undersides against completed campus surfaces."""
    pivots=[o for o in bpy.context.scene.objects if o.get('leaf_width_m')]
    moving={ob for pv in pivots for ob in pv.children_recursive if ob.type=='MESH'}
    verts=[];faces=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob in moving:continue
        for face in ob.data.polygons:
            points=[ob.matrix_world@ob.data.vertices[i].co for i in face.vertices]
            normal=ob.matrix_world.to_3x3()@face.normal
            if max(q.z for q in points)>.85 or abs(normal.z)<.5:continue
            start=len(verts);verts.extend(points);faces.append(tuple(range(start,len(verts))))
    ground=BVHTree.FromPolygons(verts,faces,all_triangles=False);rows=[]
    for pv in pivots:
        children=[ob for ob in pv.children_recursive if ob.type=='MESH']
        bottom=min((ob.matrix_world@v.co).z for ob in children for v in ob.data.vertices)
        samples=[(ob,v.co.copy()) for ob in children for v in ob.data.vertices if abs((ob.matrix_world@v.co).z-bottom)<.00001 and ((ob.matrix_world@v.co)-pv.matrix_world.translation).xy.length>.03]
        assert samples,(pv.name,'missing actual leaf underside')
        rest=pv.matrix_basis.copy();gaps=[];missing=0
        for angle in np.linspace(*pv['range_degrees'],21):
            pv.matrix_basis=rest@Matrix.Rotation(math.radians(float(angle)),4,'Z');bpy.context.view_layer.update()
            for ob,co in samples:
                point=ob.matrix_world@co;hit=ground.ray_cast(point+Vector((0,0,.30)),Vector((0,0,-1)),1.2)[0]
                if hit is None:missing+=1
                else:gaps.append(float(point.z-hit.z))
        pv.matrix_basis=rest;bpy.context.view_layer.update()
        assert not missing,(pv.name,'leaf over missing ground',missing)
        assert min(gaps)>.001,(pv.name,'leaf scrapes completed campus ground',min(gaps))
        rows.append(dict(pivot=pv.name,poses=21,actual_bottom_vertex_samples=len(samples),minimum_ground_clearance_m=min(gaps),maximum_ground_clearance_m=max(gaps),missing_surface_samples=missing))
    return rows


def source(stem,meta):
    bpy.ops.wm.open_mainfile(filepath=str(Path('build',stem+'.blend').resolve()));bpy.context.view_layer.update()
    pivots={o.name:np.array(o.matrix_world).tolist() for o in bpy.context.scene.objects if o.get('pivot_axis') or o.get('socket_kind') or o.get('slide_axis')}
    measurements={};p=meta['plan']
    if stem.startswith('School'):
        # Actual wall surfaces, not the dimensions echoed back from the plan.
        walls=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('component')=='wall'];solid=tree(walls)
        rooms=[]
        for b in p['blocks']:
            for j,(l,r,f,k) in enumerate(b['rooms']):
                spans=[[],[]]
                for axis in (0,1):
                    for fraction in (.18,.32,.50,.68,.82):
                        probe_z=p['floor']+.025
                        center=Vector(((l+r)/2,f+(k-f)*fraction,probe_z)) if axis==0 else Vector((l+(r-l)*fraction,(f+k)/2,probe_z))
                        hits=[]
                        for sign in (-1,1):
                            direction=Vector((sign,0,0) if axis==0 else (0,sign,0));hit,n,face,distance=solid.ray_cast(center,direction,50);hits.append(hit)
                        if all(q is not None for q in hits):spans[axis].append(float(hits[1][axis]-hits[0][axis]))
                if all(spans):
                    # Modal span across five source-surface probes rejects a
                    # doorway ray without selecting by the design dimension.
                    from collections import Counter
                    dims=tuple(Counter(round(x,4) for x in span).most_common(1)[0][0] for span in spans)
                    err=max(abs(dims[0]-(r-l)),abs(dims[1]-(k-f)))
                    rooms.append(dict(block=b['id'],room=j,measured_clear_m=dims,design_clear_m=(r-l,k-f),error_m=err,probe_height_m=probe_z,source_wall_ray_spans_m=spans))
                else:rooms.append(dict(block=b['id'],room=j,missing_surface=True))
        measurements['classrooms']=rooms
        # Sweep the actual leaf against its casing and nearby wall assembly.
        # Full leaf and hardware surfaces are tested. Stationary cylindrical
        # jamb knuckles have intentional attachment contact and are excluded.
        measurements['door_casing_sweeps']=door_sweeps()
        # Measured roof deck / masonry extrema; boiler stack excluded here.
        envelope=[]
        for b in p['blocks']:
            obs=[o for o in walls if o.get('block_id')==b['id']]
            verts=[ob.matrix_world@v.co for ob in obs for v in ob.data.vertices]
            envelope.append(dict(block=b['id'],masonry_top_m=max(v.z for v in verts),design_floor_surface_m=p['floor'],exposed_wall_height_m=max(v.z for v in verts)-min(v.z for v in verts)))
        measurements['wall_tops']=envelope
        levels=[]
        for ob in bpy.context.scene.objects:
            if ob.type!='MESH' or ob.get('component')!='floor':continue
            planes=set()
            for face in ob.data.polygons:
                zs=[float((ob.matrix_world@ob.data.vertices[i].co).z) for i in face.vertices]
                if max(zs)-min(zs)<1e-5:planes.add(round(zs[0],6))
            levels.append(dict(source_object=ob.name,horizontal_surface_levels_m=sorted(planes)))
        measurements['floor_and_ceiling_planes']=levels
        supports=[]
        for ob in bpy.context.scene.objects:
            if ob.type!='MESH' or not ob.get('roof_curb_vertices'):continue
            ids=json.loads(ob['roof_curb_vertices'])
            if not ids:continue
            verts=[ob.matrix_world@v.co for v in ob.data.vertices]
            roof_faces=[tuple(face.vertices) for face in ob.data.polygons if ob.data.materials[face.material_index].name=='SchoolPBR_Shingles' and face.normal.z>.5]
            surface=BVHTree.FromPolygons(verts,roof_faces,all_triangles=True)
            for j,indices in enumerate(ids):
                points=[verts[i] for i in indices];distances=[float(surface.find_nearest(q)[3]) for q in points]
                assert max(distances)<.0001,(ob.name,'unsupported equipment curb',distances)
                supports.append(dict(source_mesh=ob.name,unit=j,actual_curb_bottom_corners_m=[list(q) for q in points],nearest_roof_surface_distance_m=distances))
        measurements['roof_curb_supports']=supports
    if stem.startswith('Campus'):
        measurements['portable_door_sweeps']=door_sweeps(portable_only=True)
        measurements['completed_ground_door_clearance']=ground_clearance()
        measurements['site_placement']=site_placement(p)
    return pivots,measurements


def site_placement(p):
    """Actual trunk bases / walk surfaces against authored program bounds."""
    from geometry import H
    def area(poly):return abs(sum(x*yy-xx*y for (x,y),(xx,yy) in zip(poly,poly[1:]+poly[:1])))/2 if poly else 0
    def constraints(rect):
        l,r,f,k=rect;return [(1,0,-l),(-1,0,r),(0,1,-f),(0,-1,k)]
    campus=bpy.data.objects['Campus_'+str(p['seed'])];inv=campus.matrix_world.inverted()
    def local(ob,v):return inv@ob.matrix_world@v.co
    def polygons(ob):return [[tuple(local(ob,ob.data.vertices[i])[:2]) for i in face.vertices] for face in ob.data.polygons]
    routes={kind:polygons(bpy.data.objects['Campus_'+str(p['seed'])+'__'+label+'_paving']) for kind,label in [('bus','Bus_loading_lane'),('parent','Parent_one_way')]}
    def overlap(poly,cuts):
        result=poly
        for a,b,c in cuts:result=H.clip(result,a,b,c)
        return area(result)
    from siteworks import convex_cuts
    crossing=sum(overlap(a,convex_cuts(b)) for a in routes['bus'] for b in routes['parent'])
    incursions={kind:{b['id']:sum(overlap(poly,constraints(b['rect'])) for poly in polygons) for b in p['blocks']} for kind,polygons in routes.items()}
    assert crossing<.001,('Bus and parent pavement crosses',crossing)
    assert all(v<.001 for row in incursions.values() for v in row.values()),('Drive through building',incursions)
    trunks=[]
    for root in bpy.context.scene.objects:
        if not root.name.startswith('Mature_tree_') or '__' in root.name:continue
        points=[local(ob,v) for ob in root.children_recursive if ob.type=='MESH' and ob.data.name.startswith('Trunk and branches') for v in ob.data.vertices if local(ob,v).z<.30]
        assert points,(root.name,'missing source trunk base')
        bounds=(min(v.x for v in points),max(v.x for v in points),min(v.y for v in points),max(v.y for v in points))
        collisions=[b['id'] for b in p['blocks'] if min(bounds[1],b['rect'][1])>max(bounds[0],b['rect'][0]) and min(bounds[3],b['rect'][3])>max(bounds[2],b['rect'][2])]
        assert not collisions,(root.name,'tree base inside building',collisions)
        trunks.append(dict(instance=root.name,actual_base_bounds_xy_m=bounds,building_overlaps=collisions))
    pl,pr,pf,pk=p['playground'];gx=pl+3.5*3.048;reserve=(pl,pr,pf,pk)
    obstacles=[('playground beyond gate apron',reserve,(gx-1,gx+1,pf,pf+1))]
    fx,fy=p['field'];obstacles.append(('ballfield dirt envelope',(fx,fx+24,fy,fy+24),None))
    cl,cr,cf,ck=p['blacktop'];aprons=[(cl,cr,cf,cf+1.3)]
    if p['type']=='compact':
        from plans import world
        for b in p['blocks']:
            for o in b['openings']:
                if o['face']!='north' or o['type'] not in ('door','double'):continue
                x,y,z=world((o['u'],0,0),o['origin'],o['yaw'])
                if abs(y-cf)<.02:aprons.append((x-max(1,o['w']/2+.30),x+max(1,o['w']/2+.30),y,y+2.744))
    obstacles.append(('blacktop beyond entry apron',(cl,cr,cf,ck),aprons))
    for j in range(len(p['portables'])):
        obs=[ob for ob in bpy.context.scene.objects if ob.type=='MESH' and ob.get('component')=='wall' and ('__Portable_'+str(j)+'_') in ob.name]
        points=[local(ob,v) for ob in obs for v in ob.data.vertices]
        obstacles.append(('actual portable wall footprint '+str(j),(min(v.x for v in points),max(v.x for v in points),min(v.y for v in points),max(v.y for v in points)),None))
    walk=bpy.data.objects['Campus_'+str(p['seed'])+'__School_walk_network'];intersections={name:0. for name,rect,allow in obstacles}
    for face in walk.data.polygons:
        poly=[tuple(local(walk,walk.data.vertices[i])[:2]) for i in face.vertices]
        if area(poly)<1e-8:continue
        for name,rect,allow in obstacles:
            overlap=poly
            for a,b,c in constraints(rect):overlap=H.clip(overlap,a,b,c)
            pieces=[overlap]
            allowed=allow if allow and isinstance(allow[0],(tuple,list)) else [allow] if allow else []
            for region in allowed:pieces=[q for poly in pieces for q in H.subtract(poly,constraints(region))]
            intersections[name]+=sum(area(q) for q in pieces)
    assert all(v<1e-4 for v in intersections.values()),('Walk consumes program reservation',intersections)
    surfaces=tree([ob for ob in bpy.context.scene.objects if ob.type=='MESH']);missing=[];probes=0
    for name in ('bus','parent'):
        sx,sy=p[name+'_route'][0]
        if abs(sy+89.7)<1:sy=-86.0;horizontal=True
        else:sx=104.3;horizontal=False
        for dx in np.linspace(-3,3,17):
            for dy in np.linspace(-3,3,17):
                probes+=1;origin=campus.matrix_world@Vector((sx+float(dx),sy+float(dy),2));hit=surfaces.ray_cast(origin,Vector((0,0,-1)),3)
                if hit[0] is None:missing.append((name,float(origin.x),float(origin.y)))
    assert not missing,('Uncovered entrance surface probes',missing)
    program={}
    for name in ('Blacktop','Staff_paving','Playground_base'):
        ob=bpy.data.objects['Campus_'+str(p['seed'])+'__'+name];vs=[local(ob,v) for v in ob.data.vertices]
        program[name]=dict(actual_min_xy_m=[min(v[k] for v in vs) for k in (0,1)],actual_max_xy_m=[max(v[k] for v in vs) for k in (0,1)])
    return dict(trunk_base_measurements=trunks,walk_intersection_area_m2=intersections,bus_parent_surface_crossing_m2=crossing,drive_building_intersection_m2=incursions,program_surface_bounds=program,entrance_downward_surface_probes=probes,uncovered_probes=missing,reservation_scope='Source surfaces in the campus local frame. Actual drive polygons versus one another and building footprints; actual walk polygons versus play/portable reservations, with explicit classroom ramp aprons. 6 x 6m entrance samples, not complete site coverage or a vehicle swept-path certification.')


def raw_check(stem,meta):
    path=Path('export',stem+'.gltf');raw=external(path);d=raw.json
    total=0;unique=0;collapsed=0;bad_norm=0;bad_uv=0;zero_uv=0;density=[];color_prims=0
    for mesh in d['meshes']:
        for p in mesh['primitives']:
            ma=d['materials'][p['material']]
            if 'Summer leaf cards' in mesh['name']:
                assert '_WIND' in p['attributes'] and 'COLOR_0' not in p['attributes'],(stem,'canonical tree Wind wrongly used as color')
                assert ma.get('alphaMode')=='MASK',(stem,'opaque tree cards')
            if 'Boxwood leaf cards' in mesh['name']:assert ma.get('alphaMode')=='MASK',(stem,'opaque shrub cards')
            v=raw.accessor(p['attributes']['POSITION']);n=raw.accessor(p['attributes']['NORMAL']);ids=raw.accessor(p['indices']).astype(int).ravel();tri=v[ids.reshape(-1,3)];areas=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)/2
            assert np.isfinite(v).all() and np.isfinite(n).all(),(stem,'nonfinite vertex data')
            collapsed+=int((areas<1e-12).sum());bad_norm=max(bad_norm,float(np.max(abs(np.linalg.norm(n,axis=1)-1))));unique+=len(ids)//3
            if 'COLOR_0' in p['attributes']:color_prims+=1
            if 'TEXCOORD_0' in p['attributes']:
                uv=raw.accessor(p['attributes']['TEXCOORD_0']);bad_uv+=int((~np.isfinite(uv)).sum());ut=uv[ids.reshape(-1,3)];aa=ut[:,1]-ut[:,0];bb=ut[:,2]-ut[:,0];ua=abs(aa[:,0]*bb[:,1]-aa[:,1]*bb[:,0])/2;zero_uv+=int((ua<1e-14).sum())
            else:bad_uv+=len(ids)//3
    for node in d['nodes']:
        if 'mesh' in node:total+=sum(d['accessors'][p['indices']]['count']//3 for p in d['meshes'][node['mesh']]['primitives'])
        if 'scale' in node:assert max(abs(x-1) for x in node['scale'])<1e-5,(stem,node.get('name'),'unapplied scale')
    assert total==meta['triangles'],(stem,total,meta['triangles']);assert collapsed==0,(stem,collapsed,'collapsed triangles');assert bad_norm<2e-4,(stem,bad_norm);assert not bad_uv,(stem,bad_uv)
    if stem.startswith('School'):
        assert total<=150000 and len(d['materials'])<=6,(stem,total,len(d['materials']))
        for mesh in d['meshes']:
            for primitive in mesh['primitives']:
                material=d['materials'][primitive['material']]
                if material.get('extras',{}).get('tiling_vertex_tint'):assert 'COLOR_0' in primitive['attributes'],'Lost causal surface tint'
        assert zero_uv==0,(stem,'degenerate finished UV triangles',zero_uv)
    else:assert total<300000,(stem,total,'whole site budget')
    images=[]
    from PIL import Image
    for row in d.get('images',[]):
        q=path.parent/row['uri'];assert q.exists() and not Path(row['uri']).is_absolute()
        im=Image.open(q);images.append(dict(uri=row['uri'],pixels=im.size,bytes=q.stat().st_size,gpu_mib_bc7_mips=im.width*im.height*4/3/1048576,sha256=hashlib.sha256(q.read_bytes()).hexdigest()))
    return dict(placed_triangles=total,unique_triangles=unique,materials=len(d['materials']),zero_area_triangles=collapsed,unit_normal_max_error=bad_norm,zero_area_uv_triangles=zero_uv,color_primitives=color_prims,images=images,gltf_bytes=path.stat().st_size,bin_bytes=len(raw.binary))


def imported(stem,meta,pivots):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path('export',stem+'.gltf').resolve()));bpy.context.view_layer.update();total=0;verts=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH':continue
        ob.data.calc_loop_triangles();total+=len(ob.data.loop_triangles);verts += [ob.matrix_world@v.co for v in ob.data.vertices]
    assert total==meta['triangles'],(stem,total,meta['triangles']);coords=np.array(verts);lo=coords.min(0);hi=coords.max(0);error=max(np.max(abs(lo-np.array(meta['bounds_min']))),np.max(abs(hi-np.array(meta['bounds_max']))));assert error<.001,(stem,error)
    perr=0
    for name,xf in pivots.items():
        ob=bpy.data.objects.get(name);assert ob is not None,(stem,'missing frame',name)
        perr=max(perr,float(np.max(abs(np.array(ob.matrix_world)-np.array(xf)))))
    assert perr<.001,(stem,'pivot serialization',perr)
    return dict(triangles=total,bounds_max_error_m=float(error),pivot_frame_max_error=float(perr),frames=len(pivots))


def main():
    report={};family=json.loads(Path('build/family.json').read_text())
    for seed in range(101,401):validate(school(seed))
    for stem,meta in family.items():
        print('CHECK',stem,flush=True);pivots,measured=source(stem,meta)
        Path('build',stem+'-construction.json').write_text(json.dumps(measured,indent=2))
        if stem.startswith('School'):
            assert all(not q.get('missing_surface') and q['error_m']<.003 for q in measured['classrooms']),(stem,'classroom surfaces',measured['classrooms'])
            assert all(not q['casing_intersections'] for q in measured['door_casing_sweeps']),(stem,'door casing interference')
            assert all(not q['neighbor_intersections'] for q in measured['door_casing_sweeps']),(stem,'door neighbor interference')
            assert all(q['kit_casing_volume']['passed'] for q in measured['door_casing_sweeps']),(stem,'kit casing penetration')
        if stem.startswith('Campus'):
            assert all(not q['casing_intersections'] and not q['neighbor_intersections'] and q['kit_casing_volume']['passed'] for q in measured['portable_door_sweeps']),(stem,'portable door interference')
        r=raw_check(stem,meta);r['construction']=measured;r['fresh_import']=imported(stem,meta,pivots);report[stem]=r
    preserved=json.loads(Path('build/preservation.json').read_text());changed=[p for p,h in preserved.items() if not (ROOT/p).exists() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h];assert not changed,changed
    report['preservation']=dict(files=len(preserved),changed=changed);report['plan_seeds_checked']=300
    Path('build/check.json').write_text(json.dumps(report,indent=2));print('SCHOOL LOOK-DEV CHECK PASS',flush=True)

if __name__=='__main__':main()
