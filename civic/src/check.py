"""Independent external glTF, fresh import and real-surface dimensional audit."""
import hashlib,json,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from kit.gltf import GLB
from geo import ROOT


def document(path):
    d=json.loads(path.read_text());raw=object.__new__(GLB);raw.json=d
    raw.binary=(path.parent/d['buffers'][0]['uri']).read_bytes();return raw


def audit(path):
    from PIL import Image
    raw=document(path);d=raw.json;stored=0;bad_uv=0;min_area=float('inf');norm_error=0;density={};sizes={}
    for i,im in enumerate(d.get('images',[])):
        with Image.open(path.parent/im['uri']) as image:sizes[i]=image.size
    for m in d['meshes']:
        for pr in m['primitives']:
            at=pr['attributes'];pos=raw.accessor(at['POSITION']);normal=raw.accessor(at['NORMAL']);uv=raw.accessor(at['TEXCOORD_0']) if 'TEXCOORD_0' in at else None;idx=raw.accessor(pr['indices']).reshape(-1,3)
            assert np.isfinite(pos).all() and np.isfinite(normal).all() and (uv is None or np.isfinite(uv).all()),path
            norm_error=max(norm_error,float(np.abs(np.linalg.norm(normal,axis=1)-1).max()))
            tri=pos[idx];area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)/2
            min_area=min(min_area,float(area.min()));assert not np.any(area<1e-12),(path,m['name'],'degenerate geometry')
            if uv is not None:
                t=uv[idx];det=(t[:,1,0]-t[:,0,0])*(t[:,2,1]-t[:,0,1])-(t[:,1,1]-t[:,0,1])*(t[:,2,0]-t[:,0,0])
                bad_uv+=int((np.abs(det)<1e-12).sum())
                ma=d['materials'][pr['material']];texture=ma.get('pbrMetallicRoughness',{}).get('baseColorTexture')
                if texture:
                    w,h=sizes[d['textures'][texture['index']]['source']]
                    values=np.sqrt(abs(det)*w*h/(2*area));density.setdefault(ma['name'],[]).append((values,area))
            stored+=len(idx)
    assert norm_error<.002,(path,norm_error)
    assert bad_uv==0,(path,'degenerate texture triangles',bad_uv)
    placed=sum(d['accessors'][p['indices']]['count']//3 for n in d['nodes'] if 'mesh' in n for p in d['meshes'][n['mesh']]['primitives'])
    images=[]
    for im in d.get('images',[]):
        assert 'uri' in im and not im['uri'].startswith(('data:','/')),(path,im)
        p=(path.parent/im['uri']).resolve();assert p.exists(),p
        with Image.open(p) as image:w,h=image.size
        images.append(dict(uri=im['uri'],path=str(p.relative_to(ROOT)),width=w,height=h,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),gpu_mib=w*h*4/3/1048576))
    bands={}
    for name,parts in density.items():
        values=np.concatenate([p[0] for p in parts]);weights=np.concatenate([p[1] for p in parts]);order=np.argsort(values);cumulative=np.cumsum(weights[order]);quantiles=np.interp(np.array((.05,.5,.95))*cumulative[-1],cumulative,values[order])
        bands[name]=dict(area_weighted_p5_median_p95_px_m=quantiles.tolist(),surface_area_m2=float(weights.sum()))
        if name=='Civic_Veneer':assert 400<quantiles[1]<440,(path,'Masonry physical texel scale',quantiles.tolist())
    return dict(stored_triangles=stored,placed_triangles=placed,materials=len(d['materials']),primitives=sum(len(m['primitives']) for m in d['meshes']),min_area_m2=min_area,max_normal_length_error=norm_error,degenerate_uv_triangles=bad_uv,texel_density=bands,images=images,uv_policy='Meter-repeating manufacture / guarded trim charts; overlaps intentional; this is not a unique-atlas pack')


def surface(ob):
    ob.data.calc_loop_triangles();return BVHTree.FromPolygons([ob.matrix_world@v.co for v in ob.data.vertices],[tuple(t.vertices) for t in ob.data.loop_triangles],all_triangles=True)


def station_measurements(p):
    rt=bpy.data.objects['Station_'+str(p['seed'])];fixed=next(o for o in rt.children if o.type=='MESH' and not o.get('kinematic_guide'));tree=surface(fixed)
    off=Vector(p['origin_offset_m']);rows=[]
    for j in range(p['bays']):
        center=Vector((-p['width']/2+.4572+(j+.5)*p['bay_width'],-p['depth']/2+.22,p['floor']+2))-off
        hits=[tree.ray_cast(center,Vector((side,0,0)),8) for side in (-1,1)];assert all(h[0] is not None for h in hits)
        width=sum(h[3] for h in hits)
        up=tree.ray_cast(center,Vector((0,0,1)),8);down=tree.ray_cast(center,Vector((0,0,-1)),4);assert up[0] and down[0]
        height=up[0].z-down[0].z;rows.append(dict(bay=j+1,clear_width_m=width,clear_height_m=height))
        assert abs(width-4.2672)<.003 and abs(height-4.2672)<.003,rows[-1]
    return rows


def main():
    family=json.loads(Path('build/family.json').read_text());report={};unique={}
    for name,row in family.items():
        path=Path(row['gltf']);result=audit(path);assert result['placed_triangles']==row['placed_triangles']
        for im in result['images']:unique[im['path']]=im
        if name.startswith('Civic-'):assert result['placed_triangles']<=120000,(name,result['placed_triangles'])
        else:assert row['plan']['static_site']['triangles']<250000
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
        imported=sum(len(o.data.loop_triangles) for o in bpy.context.scene.objects if o.type=='MESH' and not o.data.calc_loop_triangles())
        assert imported==result['placed_triangles'],(name,imported,result['placed_triangles']);result['fresh_import_triangles']=imported
        if name.startswith('Civic-') and row['plan']['program']=='station':result['measured_openings']=station_measurements(row['plan'])
        if name.startswith('Site-'):
            stalls=[o for o in bpy.context.scene.objects if o.get('socket_kind')=='parked_car'];paths=[o for o in bpy.context.scene.objects if o.get('path_kind')];assert stalls and len(paths)>=2
            result['stall_sockets']=len(stalls);result['occupied_sockets']=sum(bool(o.get('occupied')) for o in stalls);result['paths']=len(paths)
            site_root=bpy.data.objects['CivicSite_'+str(row['plan']['seed'])]
            skin=next(o for o in site_root.children if o.type=='MESH');ground_tree=surface(skin)
            offset=Vector(row['plan'].get('origin_offset_m',(0,0,0)));ramps=[]
            for q in row['plan']['ramps']:
                aa,bb,ff,kk=q['rect'];yy=(ff+kk)/2;points=[]
                for xx in (aa+.05,bb-.05):
                    hit=ground_tree.ray_cast(Vector((xx,yy,2))-offset,Vector((0,0,-1)),4);assert hit[0] is not None;points.append(hit[0])
                slope=abs((points[1].z-points[0].z)/(points[1].x-points[0].x))
                mid=(points[0]+points[1])/2;mid.z-=.012
                sides=[ground_tree.ray_cast(mid,Vector((0,s,0)),3) for s in (-1,1)];assert all(h[0] is not None for h in sides)
                width=sum(h[3] for h in sides);assert slope<=1/12+.0001 and width>=1.524-.001,(name,slope,width)
                ramps.append(dict(surface_points_m=[list(p) for p in points],measured_running_slope=slope,measured_clear_width_m=width))
            result['measured_ramps']=ramps
            if name=='Site-202':
                # Actual placed shrub/bench bounds must miss every apparatus
                # corridor. These points come from imported surfaces.
                p=row['plan']['building'];x,y,_=row['plan']['building_at'];offset=row['plan'].get('origin_offset_m',(0,0,0));x-=offset[0];y-=offset[1];obstacles=[]
                for o in bpy.context.scene.objects:
                    if o.type!='MESH' or not any(q in o.name for q in ('FoundationBoxwood','EntryBench','BikeRack')):continue
                    xyz=np.array([o.matrix_world@v.co for v in o.data.vertices]);lo=xyz.min(0);hi=xyz.max(0)
                    for j in range(p['bays']):
                        cx=x-p['width']/2+.4572+(j+.5)*p['bay_width'];overlap=min(hi[0],cx+2.1336)-max(lo[0],cx-2.1336)>0 and min(hi[1],y-p['depth']/2)-max(lo[1],-34-offset[1])>0
                        if overlap:obstacles.append(o.name)
                assert not obstacles,obstacles;result['exit_obstructions']=obstacles
        result['passed']=True;report[name]=result
    from prepare import snapshot
    before=json.loads(Path('build/preservation.json').read_text());after=snapshot();changed=[p for p,h in before.items() if after.get(p)!=h];assert not changed,changed
    modules=json.loads(Path('build/modules.json').read_text())
    for m in modules['modules']:assert m['triangles']<=(12000 if m['name']=='HoseTower' else 2000),(m['name'],m['triangles'])
    report['CivicPieces']=audit(Path('export/CivicPieces.gltf'));report['CivicPieces']['passed']=True
    out=dict(passed=True,files=report,unique_images=list(unique.values()),shared_gpu_mib=sum(im['gpu_mib'] for im in unique.values()),preserved_files=len(before),scope='Serialization, geometry and selected actual construction measurements; photographic quality judged separately')
    Path('build/check.json').write_text(json.dumps(out,indent=2)+'\n');print('CIVIC CHECK PASS',len(report),'packages;',len(before),'existing files unchanged')


if __name__=='__main__':main()
