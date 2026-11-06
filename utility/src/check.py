"""Independent raw-GLB/import measurements and physical construction gates.

This is the physical geometry audit; UV, bake and texture gates live in
check_delivery.py. Source constants are compared to measured surfaces, never reported
as if they were measurements.
"""
import json,math,sys,hashlib
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit.gltf import GLB
from plan import SEEDS
from span import catenary


def triangles(ob):
    ob.data.calc_loop_triangles();return len(ob.data.loop_triangles)


def imported(path):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
    return list(bpy.context.scene.objects)


def measured_circle(ob,height):
    points=[v.co.copy() for v in ob.data.vertices if abs(v.co.z-height)<1e-4 and math.hypot(v.co.x,v.co.y)<.18]
    # glTF splits material/normal/UV vertices; deduplicate actual ring points.
    points=list({tuple(round(x,6) for x in p):p for p in points}.values())
    points.sort(key=lambda p:math.atan2(p.y,p.x));assert len(points)==20,(height,len(points))
    perimeter=sum((p-points[(i+1)%len(points)]).length for i,p in enumerate(points))
    world=[ob.matrix_world@p for p in points]
    return dict(vertices=len(points),perimeter_m=perimeter,diameter_x_m=max(p.x for p in points)-min(p.x for p in points),
                world_x_bounds_m=[min(p.x for p in world),max(p.x for p in world)])


def raw_check(path,expected):
    g=GLB(path);count=0;normal_error=0;degenerate=0
    for mesh in g.json['meshes']:
        for pr in mesh['primitives']:
            ix=g.accessor(pr['indices']).ravel();pos=g.accessor(pr['attributes']['POSITION']);n=g.accessor(pr['attributes']['NORMAL'])
            count+=len(ix)//3;normal_error=max(normal_error,float(abs(np.linalg.norm(n,axis=1)-1).max()))
            xyz=pos[ix.reshape(-1,3)];areas=np.linalg.norm(np.cross(xyz[:,1]-xyz[:,0],xyz[:,2]-xyz[:,0]),axis=1)
            degenerate+=int((areas<1e-12).sum())
            assert np.isfinite(pos).all() and np.isfinite(n).all()
    assert count==expected,(path,count,expected)
    assert normal_error<.001 and degenerate==0,(path,normal_error,degenerate)
    return dict(triangles=count,materials=len(g.json.get('materials',[])),images=len(g.json.get('images',[])),
                bytes=path.stat().st_size,unit_normal_error=normal_error,degenerate_triangles=degenerate)


def minimum_height(ob):
    return min((ob.matrix_world@v.co).z for v in ob.data.vertices)


def road_height(ob):
    """Clip actual imported triangles at both curb-back planes, not just
    their vertices: the lowest crossing can occur between sample stations.
    """
    vertices=[ob.matrix_world@v.co for v in ob.data.vertices];minimum=None
    for t in ob.data.loop_triangles:
        polygon=[vertices[i] for i in t.vertices]
        for sign in (-1,1):
            clipped=[]
            for i,p in enumerate(polygon):
                q=polygon[(i+1)%len(polygon)];dp=sign*p.x-4.2672;dq=sign*q.x-4.2672
                if dp<=0:clipped.append(p)
                if (dp<0<dq) or (dq<0<dp):clipped.append(p.lerp(q,dp/(dp-dq)))
            polygon=clipped
            if not polygon:break
        if polygon:
            h=min(p.z for p in polygon)-.16764
            minimum=h if minimum is None else min(minimum,h)
    return minimum


def roof_surfaces(homes):
    result=[]
    for row in homes:
        with bpy.data.libraries.load(str(Path('build/context',row['type']+'-look.blend').resolve()),link=False) as (src,dst):
            dst.objects=[n for n in src.objects if 'Roof' in n or 'roof' in n]
        transform=Matrix.Translation(row['location'])@Matrix.Rotation(math.radians(row['yaw']),4,'Z');vs=[];fs=[]
        for ob in dst.objects:
            if not ob or ob.type!='MESH':continue
            offset=len(vs);vs.extend(transform@(ob.matrix_world@v.co) for v in ob.data.vertices)
            ob.data.calc_loop_triangles();fs.extend(tuple(offset+i for i in t.vertices) for t in ob.data.loop_triangles)
        bvh=BVHTree.FromPolygons(vs,fs,all_triangles=True);result.append((row['name'],bvh))
        for o in dst.objects:
            if o:bpy.data.objects.remove(o,do_unlink=True)
    return result


def communication_sections(ob,meta):
    """Slice actual imported triangles at 21 planes per pole interval.

    Group the jacket/strand envelope of each separately hung route. An 80 mm
    grouping gap is larger than a cable+strand but smaller than the required
    120 mm free gap. Intersecting or bunched routes therefore fail the count
    as well as the measured gap gate. These are sampled vertical clearances,
    not a substitute for a full wind/load calculation.
    """
    if ob is None:return None
    vertices=np.array([tuple(ob.matrix_world@v.co) for v in ob.data.vertices])
    ob.data.calc_loop_triangles();faces=np.array([tuple(t.vertices) for t in ob.data.loop_triangles]);tri=vertices[faces]
    lo=tri[:,:,1].min(axis=1);hi=tri[:,:,1].max(axis=1);sections=[]
    expected=meta['plan']['profile']['comm_count']
    for a,b in zip(meta['plan']['poles'],meta['plan']['poles'][1:]):
        for f in np.linspace(.03,.97,21):
            y=a['location'][1]*(1-f)+b['location'][1]*f;values=[]
            for t in tri[(lo<=y)&(hi>=y)]:
                for i in range(3):
                    p,q=t[i],t[(i+1)%3];dp=p[1]-y;dq=q[1]-y
                    if dp*dq<=0 and abs(dp-dq)>1e-10:values.append(float(p[2]+(q[2]-p[2])*dp/(dp-dq)))
            bands=[]
            for z in sorted(values):
                if not bands or z-bands[-1][1]>.08:bands.append([z,z])
                else:bands[-1][1]=z
            assert len(bands)==expected,('Actual communication bands merge',meta['plan']['seed'],y,bands,expected)
            gap=min(upper[0]-lower[1] for lower,upper in zip(bands,bands[1:]))
            assert gap>=.12,('Actual communication gap',meta['plan']['seed'],y,gap,bands)
            sections.append(dict(y_m=y,bands_z_m=bands,minimum_free_vertical_gap_m=gap))
    return dict(section_count=len(sections),observed_route_counts=sorted({len(s['bands_z_m']) for s in sections}),
        minimum_free_vertical_gap_m=min(s['minimum_free_vertical_gap_m'] for s in sections),sections=sections,
        scope='Actual imported tube triangles intersected with 84 horizontal-distance station planes; each band includes jacket and strand. Gate 120 mm.')


def check():
    all_rows={}
    for seed in SEEDS:
        path=Path(f'build/street-{seed}.glb');meta=json.loads(path.with_suffix('.json').read_text())
        report=raw_check(path,meta['total_triangles']);obs=imported(path)
        by_name={o.name:o for o in obs};assert sum(triangles(o) for o in obs if o.type=='MESH')==report['triangles']
        measurements={}
        for spec in meta['plan']['poles']:
            name=spec['name'];mesh=by_name[name+'__Mesh'];ring=measured_circle(mesh,0);tip=measured_circle(mesh,spec['height'])
            # Linear taper at 6-ft reference station, measured from ground/tip.
            ground_expected=spec['circumference_6ft_in']*.0254
            if spec['embed_ft']==6.5:
                ground_expected+=(21*.0254-ground_expected)*(.5*.3048)/(spec['height']+.5*.3048)
            assert abs(ring['perimeter_m']-ground_expected)<2e-5
            assert abs(tip['perimeter_m']-21*.0254)<2e-5
            # The complete imported shaft footprint must fit in the native
            # left planting strip, between curb back and sidewalk front.
            assert -6.096<=ring['world_x_bounds_m'][0] and ring['world_x_bounds_m'][1]<=-4.2672,(seed,name,ring)
            # Pole geometry includes only an installation stub below grade.
            wood_top=max(v.co.z for v in mesh.data.vertices if math.hypot(v.co.x,v.co.y)<.18 and v.co.z<spec['height']+.01)
            assert abs(wood_top-spec['height'])<2e-5
            measurements[name]=dict(ground_section=ring,cut_top_section=tip,shaft_top_local_m=wood_top,triangles=triangles(mesh))
            cap=9000 if spec['kind']=='transformer' else 4600 if spec['kind']=='riser' or spec.get('light') else 4000
            assert triangles(mesh)<=cap,(seed,name,triangles(mesh),cap)
            for key,expected in meta['sockets'][name].items():
                socket=by_name[name+'__Socket_'+key]
                assert (socket.matrix_world.translation-Vector(expected)).length<2e-5
        clearance={}
        for kind in ('primary','neutral','communication','service','comm_drop'):
            ob=by_name.get('Conductors_'+kind)
            if not ob:continue
            minimum=minimum_height(ob)-.16764
            target=6.096 if kind=='primary' else 5.4864 if kind=='neutral' else 4.8768 if kind=='service' else 3.6576 if kind=='comm_drop' else 4.7244
            assert minimum>=target,(seed,kind,minimum,target)
            clearance[kind]=dict(actual_lowest_surface_above_grade_m=minimum,gate_m=target)
            if kind in ('service','comm_drop'):
                road_min=road_height(ob);road_gate=5.4864 if kind=='service' else 4.7244
                assert road_min is None or road_min>=road_gate,(seed,kind,road_min,road_gate)
                clearance[kind].update(actual_road_minimum_m=road_min,road_gate_m=road_gate)
        route_clearance=communication_sections(by_name.get('Conductors_communication'),meta)
        gaps=[];curve_error=0.;spans=meta['spans']
        for i in range(4):
            neutral=next(s for s in spans if s['name']==f'Span_{i}_Neutral')
            if not meta['plan']['profile']['comm']:continue
            comm=next(s for s in spans if s['name']==f'Span_{i}_CommStrand')
            power=catenary(neutral['start'],neutral['end'],neutral['sag_m'])['point']
            telecom=catenary(comm['start'],comm['end'],comm['sag_m'])['point']
            gap=min(power(t/200)[2]-telecom(t/200)[2]-(neutral['diameter_m']+comm['diameter_m'])/2 for t in range(201))
            assert gap>=1.016,(seed,gap);gaps.append(gap)
        # Check the declared sample polyline against the analytic catenary.
        # Imported mesh surfaces are measured separately for ground/road
        # clearances above; this curve-error value is not a GLB surface fit.
        for span in spans:
            truth=catenary(span['start'],span['end'],span['sag_m'])['point'];L=math.hypot(span['end'][0]-span['start'][0],span['end'][1]-span['start'][1])
            for p,q in zip(span['points'],span['points'][1:]):
                for f in (.25,.5,.75):
                    mid=Vector(p).lerp(Vector(q),f);t=math.hypot(mid.x-span['start'][0],mid.y-span['start'][1])/L
                    curve_error=max(curve_error,abs(mid.z-truth(t)[2]))
        assert curve_error<=.0081
        roofs=roof_surfaces(meta['houses']);overflights=[]
        for span in spans:
            if span['kind'] not in ('service','comm_drop'):continue
            for i in range(101):
                p=Vector(catenary(span['start'],span['end'],span['sag_m'])['point'](i/100))
                for home,bvh in roofs:
                    hit=bvh.ray_cast(Vector((p.x,p.y,25)),Vector((0,0,-1)),40)[0]
                    if hit is not None:overflights.append(dict(span=span['name'],house=home,clearance_m=p.z-hit.z))
        if overflights:assert min(r['clearance_m'] for r in overflights)>=2.4384,(seed,sorted(overflights,key=lambda r:r['clearance_m'])[:3])
        report.update(poles=measurements,ground_clearance=clearance,
          supply_comm_surface_gaps_m=gaps,communication_route_clearance=route_clearance,curve_chord_error_m=curve_error,
          roof_overflight_samples=len(overflights),minimum_roof_clearance_m=min((r['clearance_m'] for r in overflights),default=None),spans=len(spans),
          span_triangles=[s['triangles'] for s in spans],scope='Raw GLB counts/normals, fresh import geometry/sockets; surface minima, measured pole sections, analytic interspace samples and actual roof rays')
        all_rows[str(seed)]=report
    parts=json.loads(Path('build/utility.json').read_text());part_check=raw_check(Path('build/utility.glb'),parts['total_triangles'])
    preservation=json.loads(Path('build/context.json').read_text())
    for path,digest in preservation['preserved_files'].items():assert hashlib.sha256((HERE.parents[1]/path).read_bytes()).hexdigest()==digest
    out=dict(streets=all_rows,parts=part_check,existing_delivery_files=len(preservation['preserved_files']),preserved=True,
      stage='Baked utility checkpoint. This file proves physical geometry and serialization; delivery-check.json separately proves the external maps, UV chart allocation, tangents and shared image reuse.')
    Path('build/checks.json').write_text(json.dumps(out,indent=2));print('UTILITY CHECK PASS',json.dumps({k:{'triangles':v['triangles'],'bytes':v['bytes'],'minimum_gap':min(v['supply_comm_surface_gaps_m'],default=None)} for k,v in all_rows.items()}))


if __name__=='__main__':check()
