"""Source construction rays, sampled motion, raw GLB and fresh-import proof.

Quick-material checkpoint only: no final UV/bake/age/material-count claim.
Actual surface measurements are kept separate from serialization comparisons.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy
import numpy as np
from mathutils import Vector
from mathutils.kdtree import KDTree
from kit.gltf import GLB
from kit.motion import sweep,surface as solid_surface,penetration
from check import surface,ray,meshes_under
from strip_plan import PROOF_SEEDS


def coordinates(obs):return [ob.matrix_world@v.co for ob in obs for v in ob.data.vertices]


def run(seed,folder=Path('build/strip'),motion=True):
    source=Path(folder)/f'strip-{seed}.blend';meta=json.loads(source.with_suffix('.json').read_text());b=meta['building']
    bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));bpy.context.view_layer.update()
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];src=coordinates(meshes)
    assert sum(len(o.data.polygons) for o in meshes)==meta['total_triangles']
    assert meta['building_triangles']<=80000,meta['building_triangles']
    assert 2000<=meta['triangles']['PylonSign']<=5000
    bay_counts={k:v for k,v in meta['triangles'].items() if k.startswith('Bay_')}
    assert all(3000<=v<=7000 for v in bay_counts.values()),bay_counts
    probes=[]
    for m in meta['modules']:
        root=bpy.data.objects[m['id']];tree=surface(meshes_under(root));inv=root.matrix_world.inverted();w,d=m['width'],m['depth']
        rear_part=bpy.data.objects[m['id']+'_Rear']
        assert rear_part.get('reusable_module') and any(o.type=='MESH' for o in rear_part.children),('Missing reusable rear-wall piece',m['id'])
        def local_ray(p,v):
            result=ray(tree,root.matrix_world@Vector(p),root.matrix_world.to_3x3()@Vector(v))
            return inv@Vector(result)
        a=local_ray((-w/2-1,d*.22,.07),(1,0,0));c=local_ray((w/2+1,d*.22,.07),(-1,0,0))
        measured_width=c.x-a.x
        front=local_ray((0,-.5,2.90),(0,1,0)).y
        rear=local_ray((0,d+1,2.5),(0,-1,0)).y
        roof=local_ray((w*.31,d*.17,10),(0,0,-1)).z
        soffit=local_ray((w*.18,-meta['walk']*.5,.20),(0,0,1)).z
        assert abs(measured_width-w)<3e-5,(m['id'],'width',measured_width,w)
        assert abs(front)<3e-5,(m['id'],'front plane',front)
        assert abs(rear-d)<3e-5,(m['id'],'rear plane',rear,d)
        assert abs(roof-b['roof']-.0225)<3e-5,(m['id'],'roof',roof)
        expected=3.0925 if meta['style']=='mansard' else 3.3075
        assert abs(soffit-expected)<3e-5,(m['id'],'soffit',soffit,expected)
        shaft_top=None
        if meta['style']=='mansard':
            local_points=[inv@v for v in coordinates(meshes_under(root))]
            shaft=[v.z for v in local_points if abs(v.x+w/2)<.12 and abs(v.y+meta['walk']-.24)<.12 and v.z>.81]
            assert shaft,('Missing mansard column shaft',m['id'])
            shaft_top=max(shaft)
            assert abs(shaft_top-3.10)<3e-5,('Column protrudes through mansard',m['id'],shaft_top)
        probes.append(dict(module=m['id'],outside_slab_width_m=measured_width,outside_masonry_depth_m=rear-front,membrane_top_m=roof,covered_walk_soffit_m=soffit,clear_above_walk_m=soffit-.1524,mansard_column_shaft_top_m=shaft_top))
    # Fixed assembly proof, separate from moving leaves. Test the actual
    # consolidated meter-bank skin against every other mesh, including the
    # end wall, rain leaders, gas plumbing, ladder, paving and moving leaves.
    bank=meshes_under(bpy.data.objects['MeterBank']);bank_surfaces=[solid_surface(o) for o in bank]
    fixed_max=0.;fixed_pairs=0
    for ob in meshes:
        if ob in bank:continue
        other=solid_surface(ob)
        for current in bank_surfaces:
            depth,crossings=penetration(current,other,.001)
            fixed_max=max(fixed_max,depth);fixed_pairs+=1
            assert depth<=.001,('Meter-bank fixed assembly interference',ob.name,depth)
    end_surface=surface(meshes_under(bpy.data.objects['ElbowStorage' if meta['elbow'] else 'EndCap_Right']))
    bank_gap=min(end_surface.find_nearest(v)[3] for v in coordinates(bank))
    assert bank_gap<.002,('Unsupported meter-bank mounting feet',bank_gap)
    rack=bpy.data.objects['MeterBank'];xx=-(len(meta['modules'])-1)*.38/2
    sample=rack.matrix_world@Vector((xx,0,1.6))
    bank_skin=surface(bank)
    right=b['left']+b['width']
    cabinet=ray(bank_skin,(right-.5,sample.y,1.6),(1,0,0))
    wall=ray(end_surface,(right+.6,sample.y,1.6),(-1,0,0))
    body_gap=cabinet[0]-wall[0]
    assert .06<body_gap<.10,('Meter cabinet wall clearance',body_gap)
    services=dict(tested_mesh_pairs=fixed_pairs,maximum_penetration_m=fixed_max,
                  minimum_mounting_foot_gap_m=bank_gap,cabinet_back_to_wall_m=body_gap,
                  scope='Actual consolidated bank versus every other source mesh; BVH crossings, solid parity and edge intervals. Mounting-foot gap from bank vertices to end-wall triangles; cabinet and wall skins from opposing rays.')
    # Every accessible ramp receives actual surface rays at both ends and its
    # top landing. A constant copied from the plan is never called a measure.
    paving=bpy.data.objects['SitePaving'];tree=surface(meshes_under(paving));ramp=[]
    for a in meta['access']:
        x=(a['x0']+a['x1'])/2;y0=b['front']-meta['walk'];y1=y0+a['ramp_run']
        samples=[ray(tree,(x,y,1),(0,0,-1))[2] for y in (y0+.001,y1-.001,y1+.30,b['front']-.05)]
        slope=(samples[1]-samples[0])/(a['ramp_run']-.002)
        assert abs(slope-1/12)<2e-5 and abs(samples[2]-.1524)<2e-5 and abs(samples[3]-.1524)<2e-5,(a,samples)
        ramp.append(dict(x_m=x,slope=slope,landing_heights_m=samples[2:],measured_surface_rise_m=samples[1]-samples[0]))
    all_surfaces=surface(meshes);pedestrian=[]
    bank_points=coordinates(bank);outboard=max(v.x for v in bank_points)+.005
    work_probes=0
    for y in np.linspace(min(v.y for v in bank_points),max(v.y for v in bank_points),27):
        for z in np.linspace(.15,2.1,12):
            hit=all_surfaces.ray_cast(Vector((outboard,y,z)),Vector((1,0,0)),1.2)
            assert hit[0] is None,('Obstructed meter working area',tuple(hit[0]) if hit[0] else None)
            work_probes+=1
    services.update(working_area_rays=work_probes,verified_outboard_depth_m=1.2,
                    working_area_scope='324 finite rays across the actual bank width and .15–2.1m height; 1.2m outboard test depth from actual maximum bank X. Sampled empty access corridor, not an electrical-code certification.')
    for a in meta['access']:
        errors=[];samples=0
        for x in np.linspace(a['x0']+.015,a['x1']-.015,15):
            for y in np.linspace(b['front']-meta['walk']+.02,b['front']-.28,24):
                z=ray(all_surfaces,(x,y,2.0),(0,0,-1))[2]
                expected=min(.1524,max(0,(y-(b['front']-meta['walk']))/12))
                errors.append(abs(z-expected));samples+=1
        assert max(errors)<.002,('Obstructed ramp/landing',a,max(errors))
        pedestrian.append(dict(samples=samples,maximum_expected_floor_error_m=max(errors),scope='15 x 24 actual downward surface rays across the 5-foot ramp/landing, below 2m; detects column/plinth encroachment'))
    # Actual serialized curb vertices from Ground to the new frontage triangle
    # surface, at both clear openings and an ordinary undeformed straight.
    from check_ground import canonical
    from ground_adapter import FLOW
    native=GLB(Path('../ground/export/Ground.glb'));seams=[];W,D=meta['lot']
    for kind in ('Curb_Straight','Curb_DrivewayCut'):
        points=canonical(native,kind);section=np.unique(np.round(points[np.abs(points[:,1]-1.524)<3e-5][:,[0,2]],7),axis=0)
        for driveway in meta['driveways']:
            x=driveway['center'][0] if kind.endswith('Cut') else 0
            if driveway['edge']=='south':positions=[(x,-D/2-3.3528+u,FLOW+z) for u,z in section]
            else:
                y=driveway['center'][1] if kind.endswith('Cut') else 0
                positions=[(W/2+3.3528-u,y,FLOW+z) for u,z in section]
            errors=[tree.find_nearest(Vector(q))[3] for q in positions]
            assert max(errors)<5e-5,(kind,max(errors))
            seams.append(dict(module=kind,station_x_m=x,samples=len(errors),maximum_surface_gap_m=max(errors)))
    # Rear service landings are physical slabs at the six-inch floor, and
    # loading bollards must stand clear of their outward-swinging leaves.
    landings=[]
    for m in meta['modules']:
        rt=bpy.data.objects[m['id']+'_Rear'];inv=rt.matrix_world.inverted();skin=surface(meshes_under(rt));xx=m['width']*.20
        hits=[]
        for dx in (-.55,0,.55):
            for yy in (-1.35,-.50):
                origin=rt.matrix_world@Vector((xx+dx,yy,.8));hit=ray(skin,origin,(0,0,-1));hits.append((inv@Vector(hit)).z)
        assert max(abs(z-.1524) for z in hits)<3e-5,('Service stoop',m['id'],hits)
        landings.append(dict(module=m['id'],surface_heights_m=hits))
    frames={o.name:o.matrix_world.copy() for o in bpy.context.scene.objects if o.get('pivot_axis') or o.get('socket_kind')}
    motion_report=None
    if motion:
        specs=[dict(node=o.name,axis=o['pivot_axis'],range=list(o['range_degrees']),step=5,tolerance_m=.001) for o in bpy.context.scene.objects if o.get('pivot_axis')]
        motion_report=sweep(dict(MOTIONS=specs));(Path(folder)/f'motion-{seed}.json').write_text(json.dumps(motion_report,indent=2)+'\n')
        assert motion_report['passed'],'Motion collision; see motion report'
    raw=GLB(source.with_suffix('.glb'));raw_count=0;maximum_normal_error=0.
    for node in raw.json['nodes']:
        if 'mesh' not in node:continue
        for primitive in raw.json['meshes'][node['mesh']]['primitives']:
            raw_count+=raw.accessor(primitive['indices']).size//3
            n=raw.accessor(primitive['attributes']['NORMAL']);maximum_normal_error=max(maximum_normal_error,float(np.max(np.abs(np.linalg.norm(n,axis=1)-1))))
    assert raw_count==meta['total_triangles'],(raw_count,meta['total_triangles'])
    assert maximum_normal_error<2e-4
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.with_suffix('.glb').resolve()));bpy.context.view_layer.update()
    imported=[o for o in bpy.context.scene.objects if o.type=='MESH'];points=coordinates(imported)
    def distance(a,c):
        kd=KDTree(len(c))
        for i,v in enumerate(c):kd.insert(v,i)
        kd.balance();return max(kd.find(v)[2] for v in a)
    error=max(distance(src,points),distance(points,src));assert error<4e-5,error
    frame_error=max(max(abs(o-v) for o,v in zip(sum((list(row) for row in xf),[]),sum((list(row) for row in bpy.data.objects[name].matrix_world),[]))) for name,xf in frames.items())
    assert frame_error<3e-5,frame_error
    return dict(seed=seed,passed=True,building_triangles=meta['building_triangles'],bay_triangles=bay_counts,pylon_triangles=meta['triangles']['PylonSign'],placed_triangles=raw_count,unique_mesh_triangles=meta['unique_mesh_triangles'],glb_bytes=meta['glb_bytes'],construction=dict(bays=probes,service_landings=landings,ramps=ramp,pedestrian_routes=pedestrian,native_curb=seams,services=services,scope='Source surface rays / nearest triangles; physical construction independent of GLB roundtrip'),motion=dict(parts=len(motion_report['motions']),samples=sum(row['samples'] for row in motion_report['motions'])) if motion_report else None,serialization=dict(maximum_position_error_m=error,maximum_frame_element_error=frame_error,frames=len(frames),source_vertices=len(src),imported_vertices=len(points),maximum_normal_length_error=maximum_normal_error,scope='Fresh GLB import and raw accessors; glTF splits corners at hard normals/UVs. Proves serialization, not working assembly contacts'),scope='Construction, motion and serialization only. Shared shipping maps and image charts are audited separately in delivery-check.json; appearance is judged in REVIEW.md.')


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--seeds',default=','.join(map(str,PROOF_SEEDS)));a.add_argument('--source-root',type=Path,default=Path('build/strip'));a.add_argument('--no-motion',action='store_true');a=a.parse_args(sys.argv[sys.argv.index('--')+1:])
    rows=[]
    for seed in map(int,a.seeds.split(',')):
        row=run(seed,a.source_root,not a.no_motion);rows.append(row);print('STRIP CHECK',seed,'PASS',flush=True)
    (a.source_root/'checks.json').write_text(json.dumps(dict(passed=True,rows=rows),indent=2)+'\n')
