"""Fresh imports, measured approach surfaces and sampled operating clearance."""
import json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
import bpy
from mathutils import Vector
from kit.motion import surface,sweep
from package import counts


def run():
    report={}
    for seed in (101,202):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(Path(f'export/Church-{seed}.gltf').resolve()))
        meta=counts(list(bpy.context.scene.objects));expected=json.loads(Path(f'export/Church-{seed}.json').read_text())
        assert meta['triangles']==expected['triangles']
        assert max(abs(a-b) for a,b in zip(meta['size_m'],expected['size_m']))<.0001
        result=dict(fresh_import=meta,serialization_passed=True)
        # Footprint-centered standalone exports: horizontal envelope center.
        assert max(abs((a+b)/2) for a,b in zip(meta['bounds_min'][:2],meta['bounds_max'][:2]))<.0001
        p=json.loads(Path(f'build/plan-{seed}.json').read_text());cx,cy,_=p['placement_offset']
        if seed==101:
            ob=next(o for o in bpy.context.scene.objects if o.name.startswith('Retrofit ramp and edge curbs'))
            tree=surface(ob)['tree'];x=p['width']/2+2.6-cx;start=-p['length']/2+1.5*p['bay']+.9144-cy;run=p['ramp']['run']
            hits=[]
            for dy in (.02,run-.02,-.9144,run+.9144):
                hit=tree.ray_cast(Vector((x,start+dy,4)),Vector((0,0,-1)))
                assert hit[0] is not None,(seed,dy);hits.append(list(hit[0]))
            grade=abs((hits[1][2]-hits[0][2])/(hits[1][1]-hits[0][1]));rise=hits[2][2]-hits[3][2]
            assert grade<=1/12+.00001 and abs(rise-.6096)<.0001,(grade,rise)
            rails=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent and o.parent.name.startswith('Ramp handrail')]
            sides=[]
            for ob in rails:
                pts=[ob.matrix_world@v.co for v in ob.data.vertices]
                grasp=[q.x for q in pts if .5<q.y-start<run-.5 and q.z-(.6096-(q.y-start)*grade)>.87]
                sides.append((min(grasp),max(grasp)))
            sides.sort();clear=sides[1][0]-sides[0][1];assert clear>=1.524-.0001,clear
            result['ramp']=dict(method='Downward BVH rays on imported solids; rail width from actual grasp-height vertices',rise_m=rise,slope=grade,ratio=1/grade,clear_handrail_m=clear,landing_z_m=[hits[2][2],hits[3][2]])
        motions=[]
        for pivot in bpy.context.scene.objects:
            if not pivot.get('moving') or pivot.get('socket_kind'):continue
            if pivot.get('pivot_axis') not in ('X','Z'):continue
            moving=[o for o in pivot.children_recursive if o.type=='MESH']
            sleeve=next((o for o in moving if o.get('component')=='door_hinge'),None)
            allow=[]
            motions.append(dict(node=pivot.name,axis=pivot['pivot_axis'],range=list(pivot['range_degrees']),step=15,tolerance_m=.001,allow=allow))
        result['motion']=sweep(dict(MOTIONS=motions));assert result['motion']['passed'],result['motion']
        report[str(seed)]=result
    Path('build/construction-check.json').write_text(json.dumps(dict(passed=True,churches=report),indent=2));print('PASS church fresh imports, ramp surfaces and sampled door sweeps')


if __name__=='__main__':run()
