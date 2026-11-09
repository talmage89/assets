"""Fresh imports, measured approach surfaces and sampled operating clearance."""
import json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
import bpy
from mathutils import Vector
from kit.motion import surface,sweep
from package import counts


def routes(seed):
    """Test exported path centerlines at body/head height against the church."""
    from mathutils.bvhtree import BVHTree
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(Path(f'export/ChurchSite-{seed}.gltf').resolve()))
    body=next(o for o in bpy.context.scene.objects if 'nave_offset' in o)
    vertices=[];faces=[]
    for ob in body.children_recursive:
        if ob.type!='MESH':continue
        base=len(vertices);vertices.extend(ob.matrix_world@v.co for v in ob.data.vertices)
        faces.extend(tuple(base+i for i in f.vertices) for f in ob.data.polygons)
    tree=BVHTree.FromPolygons(vertices,faces);tested=0
    for route in bpy.context.scene.objects:
        if route.get('socket_kind')!='walk_path':continue
        points=route['points']
        for a,b in zip(points,points[1:]):
            for height in (1.1,1.7):
                aa=Vector(a)+Vector((0,0,height));bb=Vector(b)+Vector((0,0,height));d=bb-aa;length=d.length
                if length<.05:continue
                direction=d.normalized();hit=tree.ray_cast(aa+direction*.02,direction,length-.04)
                assert hit[0] is None,('Walk crosses church construction',seed,route.name,a,b,list(hit[0]) if hit[0] else None)
                tested+=1
    result=dict(passed=True,segments_at_two_heights=tested,method='BVH rays along exported centerlines at +1.1/+1.7 m; excludes site actors and is not a full navigation-volume test')
    vertices=[];faces=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or 'Curb_DrivewayCut_concrete' not in ob.name:continue
        base=len(vertices);vertices.extend(ob.matrix_world@v.co for v in ob.data.vertices)
        faces.extend(tuple(base+i for i in f.vertices) for f in ob.data.polygons)
    curb=BVHTree.FromPolygons(vertices,faces);drive_x=12.2148 if seed==202 else -18.2652
    hit=curb.ray_cast(Vector((drive_x,(-47 if seed==202 else -31)+4.15,2)),Vector((0,0,-1)))[0]
    assert hit is not None and hit.z<-.10,('Driveway has no depressed parcel-side curb',seed,hit)
    result['street_drive_curb_center_z_m']=hit.z
    if seed==202:
        canopy=next(o for o in body.children_recursive if o.get('module_kind')=='Canopy')
        stone=[];iron=[]
        for f in canopy.data.polygons:
            name=canopy.data.materials[f.material_index].name
            dest=stone if 'stone' in name else iron if 'iron' in name else None
            if dest is not None:dest.extend((canopy.matrix_world@canopy.data.vertices[i].co).z for i in f.vertices)
        seat=min(stone)-max(iron);assert -.003<seat<.001,('Canopy post/roof gap',seat)
        ramp=next(o for o in bpy.context.scene.objects if o.name.startswith('Accessible canopy curb ramp'))
        rt=surface(ramp)['tree'];hits=[rt.ray_cast(Vector((28.216,y,3)),Vector((0,0,-1)))[0] for y in (-14.19,-12.21)]
        assert all(h is not None for h in hits)
        slope=(hits[1].z-hits[0].z)/(hits[1].y-hits[0].y);assert 0<slope<=1/12
        result['canopy_post_roof_seat_m']=seat;result['canopy_clearance_m']=min(stone)-.005
        result['curb_ramp_ratio']=1/slope
    return result


def run():
    report={}
    for seed in (101,202):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(Path(f'export/Church-{seed}.gltf').resolve()))
        meta=counts(list(bpy.context.scene.objects));expected=json.loads(Path(f'export/Church-{seed}.json').read_text())
        assert meta['triangles']==expected['triangles']
        assert max(abs(a-b) for a,b in zip(meta['size_m'],expected['size_m']))<.0001
        result=dict(fresh_import=meta,serialization_passed=True)
        tower=next(o for o in bpy.context.scene.objects if o.get('module_kind')=='Tower')
        cross=next(o for o in tower.children_recursive if o.type=='MESH' and o.name.startswith('Tower top'))
        crossz=[(cross.matrix_world@v.co).z for f in cross.data.polygons if 'iron' in cross.data.materials[f.material_index].name for i in f.vertices for v in [cross.data.vertices[i]]]
        capz=[(ob.matrix_world@ob.data.vertices[i].co).z for ob in tower.children_recursive if ob.type=='MESH' for f in ob.data.polygons if ('slate' if seed==101 else 'stone') in ob.data.materials[f.material_index].name for i in f.vertices]
        gap=min(crossz)-max(capz);assert gap<.001,('Unsupported tower cross',gap)
        result['cross_vertical_seat_gap_m']=gap
        # Footprint-centered standalone exports: horizontal envelope center.
        assert max(abs((a+b)/2) for a,b in zip(meta['bounds_min'][:2],meta['bounds_max'][:2]))<.0001
        p=json.loads(Path(f'build/plan-{seed}.json').read_text());cx,cy,_=p['placement_offset']
        outward=0
        for ob in bpy.context.scene.objects:
            if ob.type!='MESH' or not ob.name.startswith(('Roof panel','Front rose gable')):continue
            points=[ob.matrix_world@v.co for v in ob.data.vertices];front=min(v.y for v in points)
            for face in ob.data.polygons:
                pp=[points[i] for i in face.vertices];n=(pp[1]-pp[0]).cross(pp[2]-pp[0]).normalized()
                if ob.name.startswith('Front rose gable') and all(abs(v.y-front)<1e-5 for v in pp):
                    assert n.y<-.99,('Front masonry winding',ob.name,face.index);outward+=1
                if ob.name.startswith('Roof panel'):
                    distances=[v.z-(p['ridge']-abs(v.x+cx)*math.tan(math.radians(p['pitch']))) for v in pp]
                    if max(abs(v) for v in distances)<1e-5:
                        assert n.z>0,('Roof outward winding',ob.name,face.index);outward+=1
                    elif max(abs(v+.13) for v in distances)<1e-5:
                        assert n.z<0,('Roof underside winding',ob.name,face.index);outward+=1
        assert outward>=8*p['bays'];result['outward_face_checks']=outward
        if seed==101:
            tread=next(o for o in bpy.context.scene.objects if o.name.startswith('Entrance landing and measured steps'))
            tree=surface(tread)['tree'];hollows=[]
            for i in range(4):
                yy=-p['length']/2-2.34-(i+.5)*.3302-cy
                hits=[tree.ray_cast(Vector((xx-cx,yy,3)),Vector((0,0,-1)))[0] for xx in (0,1.6)]
                assert all(h is not None for h in hits)
                depth=hits[1].z-hits[0].z;assert .010<depth<.013,(i,depth)
                hollows.append(depth)
            result['tread_midpoint_hollows_m']=dict(measured=hollows,method='Downward rays on imported tread center and unworn shoulder; construction, not serialization')
            hall=next(o for o in bpy.context.scene.objects if o.get('module_kind')=='ParishHall')
            hall_top=max((o.matrix_world@v.co).z for o in hall.children_recursive if o.type=='MESH' for v in o.data.vertices)
            glass=[]
            for bay in bpy.context.scene.objects:
                if not bay.name.startswith('Nave bay 1_') or int(bay.name.rsplit('_',1)[1].split('.')[0])<p['bays']-3:continue
                glass.extend((o.matrix_world@v.co).z for o in bay.children_recursive if o.type=='MESH' and o.name.startswith('Stained glass') for v in o.data.vertices)
            lowest=min(glass);assert lowest>hall_top+.10,('Annex roof crosses nave glass',lowest,hall_top)
            result['annex_glass_clearance_m']=lowest-hall_top
            ob=next(o for o in bpy.context.scene.objects if o.name.startswith('Retrofit ramp and edge curbs'))
            tree=surface(ob)['tree'];x=p['width']/2+2.6-cx;start=-p['length']/2+.5*p['bay']+.9144-cy;run=p['ramp']['run']
            hits=[]
            for dy in (.02,run-.02,-.9144,run+.9144):
                hit=tree.ray_cast(Vector((x,start+dy,4)),Vector((0,0,-1)))
                assert hit[0] is not None,(seed,dy);hits.append(list(hit[0]))
            grade=abs((hits[1][2]-hits[0][2])/(hits[1][1]-hits[0][1]));rise=hits[2][2]-hits[3][2]
            assert grade<=1/12+.00001 and abs(rise-.6096)<.0001,(grade,rise)
            start_bottom=min((ob.matrix_world@v.co).z for v in ob.data.vertices if abs((ob.matrix_world@v.co).y-start)<.001)
            assert start_bottom<=0,('Ramp floats above grade at upper end',start_bottom)
            rails=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent and o.parent.name.startswith('Ramp handrail')]
            sides=[]
            for ob in rails:
                pts=[ob.matrix_world@v.co for v in ob.data.vertices]
                grasp=[q.x for q in pts if .5<q.y-start<run-.5 and q.z-(.6096-(q.y-start)*grade)>.87]
                sides.append((min(grasp),max(grasp)))
            sides.sort();clear=sides[1][0]-sides[0][1];assert clear>=1.524-.0001,clear
            result['ramp']=dict(method='Downward BVH rays on imported solids; rail width from actual grasp-height vertices',rise_m=rise,slope=grade,ratio=1/grade,clear_handrail_m=clear,landing_z_m=[hits[2][2],hits[3][2]],upper_end_base_z_m=start_bottom)
        motions=[]
        for pivot in bpy.context.scene.objects:
            if not pivot.get('moving') or pivot.get('socket_kind'):continue
            if pivot.get('pivot_axis') not in ('X','Z'):continue
            moving=[o for o in pivot.children_recursive if o.type=='MESH']
            sleeve=next((o for o in moving if o.get('component')=='door_hinge'),None)
            allow=[]
            motions.append(dict(node=pivot.name,axis=pivot['pivot_axis'],range=list(pivot['range_degrees']),step=15,tolerance_m=.001,allow=allow))
        result['motion']=sweep(dict(MOTIONS=motions));assert result['motion']['passed'],result['motion']
        result['routes']=routes(seed)
        report[str(seed)]=result
    Path('build/construction-check.json').write_text(json.dumps(dict(passed=True,churches=report),indent=2));print('PASS church fresh imports, ramp surfaces and sampled door sweeps')


if __name__=='__main__':run()
