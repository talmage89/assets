"""Independent raw delivery, shared chart, resource and presentation receipts."""
import json,hashlib,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.gltf import GLB
from package import bundle
from check import preserve

def main():
    reports=[];images={};charts=json.loads(Path('build/atlas/layout.json').read_text());rects=list(charts.values())
    for seed in (117,228,339):
        shop=json.loads(Path(f'build/shops/{seed}.json').read_text());site=json.loads(Path(f'build/sites/{seed}.json').read_text())
        assert shop['triangles']<200000 and shop['room_triangles']<60000
        raw=GLB(Path(f'build/shops/{seed}.glb'));uv_count=0;areas=[];weights=[]
        for mesh in raw.json['meshes']:
            for pr in mesh['primitives']:
                mat=raw.json['materials'][pr['material']]
                tex=mat.get('pbrMetallicRoughness',{}).get('baseColorTexture')
                if not tex:continue
                im=raw.json['images'][raw.json['textures'][tex['index']]['source']]
                if 'CoffeeShop' not in im.get('name',''):continue
                uv=raw.accessor(pr['attributes']['TEXCOORD_0']).copy();uv[:,1]=1-uv[:,1]  # glTF top-left -> Blender chart frame
                pos=raw.accessor(pr['attributes']['POSITION']);idx=raw.accessor(pr['indices']).reshape(-1,3)
                assert np.isfinite(uv).all() and (uv>=-1e-6).all() and (uv<=1+1e-6).all()
                # The cells are shared manufacture/print charts, not unique
                # islands. Every triangle must stay inside one declared chart.
                for ids in idx:
                    a=uv[ids];lo=a.min(0);hi=a.max(0)
                    assert any(lo[0]>=r[0]-2e-6 and hi[0]<=r[2]+2e-6 and lo[1]>=r[1]-2e-6 and hi[1]<=r[3]+2e-6 for r in rects),('Chart crossing',seed,mesh['name'],lo,hi)
                    ps=pos[ids];area=np.linalg.norm(np.cross(ps[1]-ps[0],ps[2]-ps[0]))/2
                    ua=abs(np.linalg.det(np.stack((a[1]-a[0],a[2]-a[0]))))/2
                    if area>1e-9 and ua>1e-12:areas.append(float(2048*np.sqrt(ua/area)));weights.append(float(area))
                    uv_count+=1
        path=Path(f'export/sites/CoffeeSite-{seed}.gltf');assert bundle(path)==site['bundle_sha256'];doc=json.loads(path.read_text())
        context=GLB(Path(f'build/sites/{seed}.glb'));mesh_counts=[sum(context.json['accessors'][pr['indices']]['count']//3 for pr in me['primitives']) for me in context.json['meshes']]
        site_triangles=sum(mesh_counts[n['mesh']] for n in context.json['nodes'] if 'mesh' in n);assert site_triangles==site['triangles']
        paving=[];terrain=None
        for ni,node in enumerate(context.json['nodes']):
            name=node.get('name','')
            if 'mesh' not in node or name not in ('District ground','Public two-way street','Customer lot front'):continue
            xf=context.world(ni);ys=[float((xf@np.r_[v,1])[1]) for pr in context.json['meshes'][node['mesh']]['primitives'] for v in context.accessor(pr['attributes']['POSITION'])]
            if name=='District ground':terrain=max(ys)
            else:paving.append(dict(name=name,bottom_m=min(ys),top_m=max(ys)))
        assert terrain is not None and paving
        for row in paving:assert row['bottom_m']-1e-4<=terrain<=row['top_m']+1e-4,('Unsupported/buried roadway',seed,terrain,row)
        contact=dict(measured_terrain_top_m=terrain,measured_paving=paving,method='raw exported world-space heights; paving intersects supporting terrain and its top remains exposed')
        parking={}
        if seed!=117:
            intervals=set()
            for ni,node in enumerate(context.json['nodes']):
                if 'mesh' not in node or not node.get('name','').startswith('Worn parking paint'):continue
                xf=context.world(ni);ps=[(xf@np.r_[v,1])[:3] for pr in context.json['meshes'][node['mesh']]['primitives'] for v in context.accessor(pr['attributes']['POSITION'])]
                # glTF +Y is height; -Z is Blender's plan Y.
                x0=min(p[0] for p in ps);x1=max(p[0] for p in ps);y0=min(-p[2] for p in ps);y1=max(-p[2] for p in ps)
                if x1-x0<.2 and 5.3<y1-y0<5.5:intervals.add((round(float(y0),5),round(float(y1),5)))
            intervals=sorted(intervals);assert len(intervals)==2,intervals
            minimum=site.get('minimum_design_aisle_m',site.get('aisle_width_m'));assert minimum is not None
            gap=intervals[1][0]-intervals[0][1];assert gap>=minimum
            parking=dict(measured_marked_row_extents_m=intervals,measured_marked_aisle_gap_m=gap,method='raw exported positions and full node matrices, not plan constants; not a vehicle swept-path certificate')
        for im in doc.get('images',[]):
            ip=(path.parent/im['uri']).resolve();assert not im['uri'].startswith(('/','data:'))
            with Image.open(ip) as image:w,h=image.size
            images[str(ip)]=dict(path=str(ip.relative_to(ROOT)),size=[w,h],bytes=ip.stat().st_size,gpu_mib=w*h*4/3/1048576,sha256=hashlib.sha256(ip.read_bytes()).hexdigest())
        order=np.argsort(areas);av=np.asarray(areas)[order];weight=np.cumsum(np.asarray(weights)[order]);weight/=weight[-1]
        reports.append(dict(seed=seed,shop_triangles=shop['triangles'],room_triangles=shop['room_triangles'],site_triangles=site_triangles,parking=parking,terrain_contact=contact,shop_materials=shop['materials'],site_materials=site['materials'],site_bytes=site['gltf_bytes']+site['bin_bytes'],cafe_chart_triangles_checked=uv_count,density_px_m_percentiles_5_50_95=np.percentile(areas,[5,50,95]).tolist(),area_weighted_density_px_m_5_50_95=np.interp([.05,.50,.95],weight,av).tolist(),uv_policy='Intentional shared-chart reuse, cell bounds checked per triangle; no unique-island overlap claim. Both triangle- and area-weighted density include hardware and prints.'))
    maps=[]
    for channel in ('BaseColor','Normal','ORM'):
        path=Path(f'textures/ship/T_CoffeeShop_{channel}.png');im=Image.open(path);assert im.size==(2048,2048)
        if channel=='Normal':
            from kit.image_io import read_png
            a=read_png(path)[:,:,:3]*2-1;assert np.std(a[:,:,:2])>.0001;err=np.abs(np.linalg.norm(a,axis=2)-1);assert np.max(err)<.008
        maps.append(dict(channel=channel,bytes=path.stat().st_size,size=im.size))
    pieces=json.loads(Path('build/pieces/manifest.json').read_text());counts={r['piece']:r['triangles'] for r in pieces}
    assert counts['BistroChair']==2156 and counts['Umbrella_Open']==3920 and counts['Umbrella_Closed']==3908 and counts['AFrame']==220
    for seed in (117,228,339):
        path=Path(f'renders/lookdev/{seed}/hero.json')
        if '--presentation' in sys.argv:
            meta=json.loads(path.read_text());rec=meta['recipe'];assert 35<=rec['lens']<=50 and abs(rec['location'][2]-(1.65+(0 if seed==117 else .1524)))<1e-6
            assert meta['engine']=='CYCLES' and meta['bundle_sha256']==bundle(meta['source'])
    report=dict(shops=reports,unique_site_images=list(images.values()),site_union_gpu_mib=sum(r['gpu_mib'] for r in images.values()),new_maps=maps,new_gpu_mib=16,preserved_existing_files=preserve(),status='raw PBR/shared-chart/site audit; presentation checks only when images exist')
    Path('build/lookdev-check.json').write_text(json.dumps(report,indent=2)+'\n');print('LOOKDEV CHECK',[(r['seed'],r['shop_triangles'],r['site_triangles']) for r in reports],len(images),'shared images')

if __name__=='__main__':main()
