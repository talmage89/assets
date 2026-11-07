"""Measured per-package and deduplicated external family costs."""
import hashlib,json
from pathlib import Path
from PIL import Image


def run():
    check=json.loads(Path('build/check.json').read_text());assert check['passed'];rows={};images={};geometry={}
    for stem,a in check['assets'].items():
        path=Path('export')/(stem+'.gltf');doc=json.loads(path.read_text());meta=json.loads(path.with_suffix('.json').read_text())
        files=[path,*[path.parent/q['uri'] for q in doc['buffers']]]
        geometry.update({str(p):p.stat().st_size for p in files})
        for q in doc.get('images',[]):
            p=(path.parent/q['uri']).resolve();key=str(p.relative_to(Path.cwd().parent))
            w,h=Image.open(p).size
            images[key]=dict(bytes=p.stat().st_size,width=w,height=h,gpu_mib=w*h*4/3/1024**2,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
        rows[stem]=dict(units=(meta['plan']['count'] if stem.startswith('Row') else meta['plan']['units']) if not stem.startswith('Complex') else meta['plan']['building']['units']*len(meta['plan']['buildings']),
                        triangles=a['runtime_triangles'],architecture_triangles=a['physical']['architecture_triangles'],materials=a['materials'],draw_primitives=a['draw_primitives'],
                        geometry_bytes=sum(p.stat().st_size for p in files),cold_bytes=a['bytes'],gpu_mib=a['gpu_mib_8bpp_full_mips'])
    new=[v for k,v in images.items() if k.startswith('apartments/') and not k.endswith(('T_ApartmentsCedar_Normal.png','T_ApartmentsCedar_ORM.png'))]
    report=dict(assets=rows,unique_images=images,image_count=len(images),image_bytes=sum(v['bytes'] for v in images.values()),image_gpu_mib=sum(v['gpu_mib'] for v in images.values()),
                new_image_gpu_mib=sum(v['gpu_mib'] for v in new),geometry_bytes=sum(geometry.values()),family_cold_bytes=sum(geometry.values())+sum(v['bytes'] for v in images.values()))
    Path('build/delivery-summary.json').write_text(json.dumps(report,indent=2)+'\n')
    for k,v in rows.items():print(k,v)
    print('FAMILY',{k:v for k,v in report.items() if k not in ('assets','unique_images')})


if __name__=='__main__':run()
