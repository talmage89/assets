"""Fresh exported actors, actual tire/deck support and resource accounting."""
import hashlib,json,sys
from collections import Counter
from pathlib import Path
import bpy
from mathutils import Vector
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
import geometry as G
from service_age import floor_surface


def main():
    from runpy import run_path
    run_path(str(HERE/'preserve.py'),run_name='__main__')
    results=[]
    for seed in (101,202):
        path=Path(f'export/lookdev/sites/ParkingGarageLookSite-{seed}.gltf');doc=json.loads(path.read_text())
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
        garage=bpy.data.objects[f'Garage_{seed}'];surface,floor_meta=floor_surface(garage,details=True)
        manifest=json.loads(Path(f'build/lookdev/traffic-{seed}.json').read_text());p=json.loads(Path(f'build/lookdev/look-{seed}.json').read_text())
        actual=G.triangles(bpy.context.scene.objects);assert actual==p['garage_triangles']+manifest['context_triangles'],(seed,actual)
        parked=[a for a in manifest['actors'] if a['category']=='garage']
        assert len(parked)==sum(s['occupied'] for s in p['stalls'])
        assert len(set(a['kind'] for a in parked))==4
        paints=Counter(a['paint'] for a in parked);assert len(paints)>=6
        gaps=[];overhang=[]
        for row in parked:
            car=bpy.data.objects[row['name']];inv=car.matrix_world.inverted();points=[]
            for ob in car.children_recursive:
                if ob.type=='MESH':points.extend(inv@ob.matrix_world@v.co for v in ob.data.vertices)
            low=min(v.z for v in points);groups={}
            for v in points:
                if v.z<low+.003:groups.setdefault((v.x>0,v.y>0),[]).append(v)
            assert len(groups)==4,(row['name'],'Native low tire groups',len(groups))
            for group in groups.values():
                errors=[]
                for v in group:
                    q=car.matrix_world@v;hit=surface.ray_cast(q+Vector((0,0,.25)),Vector((0,0,-1)),.5)
                    assert hit[0] is not None,(row['name'],q)
                    errors.append(q.z-hit[0].z)
                gaps.append(min(errors))
            s=next(s for s in p['stalls'] if row['name']=='Parked '+s['id'])
            world=[car.matrix_world@v for v in points]
            lateral=max(abs(v.x-s['x']) for v in world)-s['width']/2
            assert lateral<.06,(row['name'],'Crosses neighboring stall',lateral)
            overhang.append(max(abs(v.y-s['y']) for v in world)-s['depth']/2)
        assert max(abs(v) for v in gaps)<.015,(seed,'Tire/deck contact',min(gaps),max(gaps))
        film=bpy.data.objects['Cause-driven service history'];film_gaps=[];seal_gaps=[]
        layout=json.loads(Path('build/lookdev/atlas-layout.json').read_text());film_uv=film.data.uv_layers.active
        for face in film.data.polygons:
            uv=sum((film_uv.data[i].uv for i in face.loop_indices),Vector((0,0)))/len(face.loop_indices)
            if not any(a<=uv.x<=c and b<=uv.y<=d for a,b,c,d in (layout[k]['rect'] for k in ('oil','rubber','scuff','droppings'))):continue
            pts=[film.matrix_world@film.data.vertices[i].co for i in face.vertices]
            normal=(pts[1]-pts[0]).cross(pts[2]-pts[0]).normalized()
            if normal.z<.7:continue
            for weights in ((1/3,1/3,1/3),(.6,.2,.2),(.2,.6,.2),(.2,.2,.6)):
                point=sum((v*w for v,w in zip(pts,weights)),Vector())
                hit=surface.ray_cast(point+Vector((0,0,.20)),Vector((0,0,-1)),.40)
                assert hit[0] is not None,(seed,'Unsupported floor film',point)
                gap=point.z-hit[0].z;u,v=floor_meta[hit[2]]['uv'];a,b,c,d=layout['Seal']['rect']
                if a<=u<=c and b<=v<=d:seal_gaps.append(gap)
                else:film_gaps.append(gap)
        assert min(film_gaps)>0 and max(film_gaps)<.0013,(seed,'Buried/floating floor film',min(film_gaps),max(film_gaps))
        assert not seal_gaps or (min(seal_gaps)>0 and max(seal_gaps)<.0013),(seed,'Film/seal strips',min(seal_gaps),max(seal_gaps))
        images=[]
        for im in doc.get('images',[]):
            q=(path.parent/im['uri']).resolve();assert q.exists();w,h=Image.open(q).size
            images.append(dict(uri=im['uri'],sha256=hashlib.sha256(q.read_bytes()).hexdigest(),bytes=q.stat().st_size,mib=w*h*4/3/2**20))
        meshcounts=[sum(doc['accessors'][p['indices']]['count']//3 for p in m['primitives']) for m in doc['meshes']]
        categories={k:dict(count=sum(a['category']==k for a in manifest['actors']),triangles=sum(a['triangles'] for a in manifest['actors'] if a['category']==k)) for k in sorted(set(a['category'] for a in manifest['actors']))}
        results.append(dict(seed=seed,expanded_triangles=actual,unique_mesh_triangles=sum(meshcounts),gltf_bytes=path.stat().st_size,bin_bytes=path.with_suffix('.bin').stat().st_size,
            materials=len(doc['materials']),images=images,texture_mib=sum(i['mib'] for i in images),actors=categories,paint_counts=dict(paints),
            tire_surface_samples=len(gaps),tire_min_signed_gap_m=min(gaps),tire_max_signed_gap_m=max(gaps),max_longitudinal_bumper_overhang_m=max(overhang),
            floor_film_surface_samples=len(film_gaps),floor_film_min_signed_gap_m=min(film_gaps),floor_film_max_signed_gap_m=max(film_gaps),
            seal_film_surface_samples=len(seal_gaps),seal_film_min_signed_gap_m=min(seal_gaps,default=0),seal_film_max_signed_gap_m=max(seal_gaps,default=0),
            context_without_actors_triangles=manifest['context_triangles']-manifest['actor_triangles']))
    Path('build/delivery-check.json').write_text(json.dumps(dict(passed=True,sites=results),indent=2)+'\n')
    print('DELIVERY ACTOR/RESOURCE CHECK PASS',[(r['seed'],r['tire_min_signed_gap_m'],r['tire_max_signed_gap_m']) for r in results],flush=True)


if __name__=='__main__':main()
