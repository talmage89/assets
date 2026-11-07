"""Independent export measurements, clear routes, resource reuse and repeat.

Form checkpoint checks do not claim baked unique UVs or final wear quality.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
from plan import generate,PROOFS


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def preserve(capture=False):
    path=Path('build/preservation.json')
    if capture:
        files=[]
        for fam in ('downtown','commercial','patio-set','street-furniture','ground','trees','shrubs','street-light','cars'):
            for folder in ('export','textures/ship'):
                files.extend(p for p in (REPO/fam/folder).rglob('*') if p.is_file())
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps({str(p.relative_to(REPO)):sha(p) for p in sorted(set(files))},indent=2)+'\n')
    expected=json.loads(path.read_text());bad=[name for name,digest in expected.items() if sha(REPO/name)!=digest]
    if bad:raise AssertionError(('Existing delivery changed',bad))
    return len(expected)


def repeat():
    import shutil
    base=Path.cwd();folder=base/'build/repeat'
    if folder.exists():shutil.rmtree(folder)
    (folder/'build').mkdir(parents=True);shutil.copytree(base/'build/hosts',folder/'build/hosts')
    log=base/'build/repeat.log'
    with log.open('w') as f:subprocess.run(['blender','-b','--factory-startup','--python-exit-code','1','--python',str(HERE/'build.py'),'--','--out','build/coffee.blend'],cwd=folder,stdout=f,stderr=subprocess.STDOUT,check=True)
    rows=[]
    for p in sorted((base/'export').rglob('*')):
        if not p.is_file() or p.suffix not in ('.gltf','.bin','.png'):continue
        other=folder/p.relative_to(base)
        if p.suffix=='.gltf':
            d=json.loads(other.read_text())
            for im in d.get('images',[]):
                target=(other.parent/im['uri']).resolve()
                if folder not in target.parents:im['uri']=os.path.relpath(target,p.parent)
            other.write_text(json.dumps(d,separators=(',',':'))+'\n')
        if sha(p)!=sha(other):raise AssertionError(('Repeat differs',str(p)))
        rows.append(dict(path=str(p.relative_to(base)),bytes=p.stat().st_size,sha256=sha(p)))
    for p in sorted((base/'build/hosts').glob('*.glb')):
        dest=folder/'build/hosts'/p.name
        with (base/'build/repeat-hosts.log').open('a') as f:subprocess.run(['blender','-b','--factory-startup','--python-exit-code','1','--python',str(HERE/'hosts.py'),'--','--kind',p.stem,'--out',str(dest)],cwd=folder,stdout=f,stderr=subprocess.STDOUT,check=True)
        if sha(p)!=sha(dest):raise AssertionError(('Host repeat differs',p.name))
    (base/'build/repeat.json').write_text(json.dumps(dict(files=rows,bytes=sum(r['bytes'] for r in rows),status='byte-identical deterministic geometry, quick fields, graphics and canonical package URIs; no GPU bake at this gate'),indent=2)+'\n')
    print('REPEAT PASS',len(rows),'files',sum(r['bytes'] for r in rows),'bytes')


def clip(poly,axis,value,above):
    out=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        aa=a[axis]>=value if above else a[axis]<=value;bb=b[axis]>=value if above else b[axis]<=value
        if aa:out.append(a)
        if aa!=bb:
            t=(value-a[axis])/(b[axis]-a[axis]);out.append(tuple(a[k]+t*(b[k]-a[k]) for k in range(3)))
    return out


def route_obstacles(obs,route,depth,grade):
    rect=route['rect'];hits=[]
    # Floor boxes end at grade. Test the occupied route from 25mm through 2.03m.
    cuts=[(0,rect[0],True),(0,rect[1],False),(1,rect[2]-depth/2,True),(1,rect[3]-depth/2,False),(2,grade+.025,True),(2,grade+2.03,False)]
    for ob in obs:
        if ob.type!='MESH':continue
        if 'door approach' in route['name'].lower() and ('Entry' in ob.name):continue
        pts=[tuple(ob.matrix_world@v.co) for v in ob.data.vertices]
        # Broadphase then actual triangle/box clipping, not object centers.
        if any(max(p[axis] for p in pts)<value or min(p[axis] for p in pts)>value for axis,value,_ in []):continue
        if max(p[0] for p in pts)<rect[0] or min(p[0] for p in pts)>rect[1] or max(p[1] for p in pts)<rect[2]-depth/2 or min(p[1] for p in pts)>rect[3]-depth/2 or max(p[2] for p in pts)<grade+.025:continue
        for f in ob.data.polygons:
            poly=[pts[i] for i in f.vertices]
            for axis,value,above in cuts:
                if len(poly)<3:break
                poly=clip(poly,axis,value,above)
            if len(poly)>=3:
                # Ignore zero-area contacts on an explicitly drawn boundary.
                from mathutils import Vector
                area=sum((Vector(poly[i])-Vector(poly[0])).cross(Vector(poly[i+1])-Vector(poly[0])).length/2 for i in range(1,len(poly)-1))
                if area>1e-7:hits.append(ob.name);break
    return sorted(set(hits))


def main():
    import bpy
    import numpy as np
    from kit.gltf import GLB
    from PIL import Image
    from package import bundle
    rows=[];image_uris={};preserved=preserve()
    for seed,kind in PROOFS:
        bpy.ops.wm.read_factory_settings(use_empty=True);p=json.loads(Path(f'build/shops/{seed}.json').read_text());path=Path(f'export/CoffeeShop-{seed}.gltf');doc=json.loads(path.read_text());raw=GLB(Path(f'build/shops/{seed}.glb'))
        assert p['bundle_sha256']==bundle(path)
        for im in doc.get('images',[]):
            assert 'uri' in im and not im['uri'].startswith(('data:','/'))
            ip=(path.parent/im['uri']).resolve();image_uris[str(ip)]=sha(ip)
        for mesh in raw.json['meshes']:
            for pr in mesh['primitives']:
                pos=raw.accessor(pr['attributes']['POSITION']);ns=raw.accessor(pr['attributes']['NORMAL'])
                assert np.isfinite(pos).all() and np.isfinite(ns).all();assert np.max(np.abs(np.linalg.norm(ns,axis=1)-1))<.002
                assert 'TEXCOORD_0' in pr['attributes']
        bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update();obs=list(bpy.context.scene.objects)
        tri=sum(sum(len(f.vertices)-2 for f in o.data.polygons) for o in obs if o.type=='MESH');assert tri==p['triangles'] and tri<200000
        room=[o for o in obs if o.type=='MESH' and any(par.name=='Room' for par in ancestors(o))];room_tri=sum(sum(len(f.vertices)-2 for f in o.data.polygons) for o in room);assert room_tri==p['room_triangles'] and room_tri<60000
        routes=[]
        for r in p['routes']:
            width=min(r['rect'][1]-r['rect'][0],r['rect'][3]-r['rect'][2]);hits=route_obstacles(obs,r,p['depth'],p['grade']);assert width+1e-6>=r['required']
            routes.append(dict(name=r['name'],drawn_width_m=width,required_m=r['required'],actual_surface_intrusions=hits))
        assert not any(r['actual_surface_intrusions'] for r in routes),('ROUTE FAIL',seed,[(r['name'],r['actual_surface_intrusions']) for r in routes if r['actual_surface_intrusions']])
        # A deliberately inserted solid must fail the same surface checker.
        from kit import model as model_helpers
        test=p['routes'][0];x0,x1,y0,y1=test['rect'];block=model_helpers.box('NegativeRouteFixture',((x0+x1)/2,(y0+y1)/2-p['depth']/2,p['grade']+.8),(.12,.12,.12),None,0)
        bpy.context.view_layer.update();assert block.name in route_obstacles(obs+[block],test,p['depth'],p['grade']);bpy.data.objects.remove(block,do_unlink=True)
        roots=[o for o in obs if o.get('socket_kind')=='seated_person'];assert roots
        rows.append(dict(seed=seed,triangles=tri,room_triangles=room_tri,materials=len(doc.get('materials',[])),primitives=sum(len(m['primitives']) for m in doc['meshes']),routes=routes,seat_sockets=len(roots),gltf_bytes=path.stat().st_size,bin_bytes=path.with_suffix('.bin').stat().st_size))
    # Geometry measurements of the independent pieces, without their site transform.
    pieces=[]
    for item in json.loads(Path('build/pieces/manifest.json').read_text()):
        bpy.ops.wm.read_factory_settings(use_empty=True);path=Path('export/pieces')/(item['piece']+'.gltf');bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
        pts=[o.matrix_world@v.co for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices];lo=[min(v[k] for v in pts) for k in range(3)];hi=[max(v[k] for v in pts) for k in range(3)]
        assert abs(lo[2])<.022,(item['piece'],lo)
        pieces.append(dict(piece=item['piece'],triangles=item['triangles'],bounds_min=lo,bounds_max=hi,dimensions=[b-a for a,b in zip(lo,hi)]))
    # Measure usable knee space on actual imported triangles, rather than
    # repeating constants from the model's socket metadata.
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path('export/pieces/AccessibleTable.gltf').resolve()));bpy.context.view_layer.update();v=[];f=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH':continue
        n=len(v);v.extend(tuple(ob.matrix_world@p.co) for p in ob.data.vertices);f.extend(tuple(n+i for i in p.vertices) for p in ob.data.polygons)
    tree=BVHTree.FromPolygons(v,f,all_triangles=True)
    _,_,_,plus=tree.ray_cast(Vector((0,0,.700)),Vector((0,1,0)),1);_,_,_,minus=tree.ray_cast(Vector((0,0,.700)),Vector((0,-1,0)),1)
    underside=tree.ray_cast(Vector((0,0,.1)),Vector((0,0,1)),1)[0].z
    assert plus+minus>=.762 and underside>=.6858
    for y in np.linspace(-.381,.381,13):
        for z in np.linspace(.025,.6858,15):
            hit=tree.ray_cast(Vector((-1.1932,y,z)),Vector((1,0,0)),1.2192)[0];assert hit is None,('Knee approach blocked',list(hit))
    knee=dict(measured_width_at_700mm_m=plus+minus,measured_center_underside_m=underside,clear_forward_rays=195,ray_box_m=[1.2192,.762,.6608],method='actual triangle BVH; forward rays from outside edge through 483mm under top')
    resources=[]
    for name,digest in sorted(image_uris.items()):
        with Image.open(name) as im:w,h=im.size
        resources.append(dict(uri=os.path.relpath(name,Path('export')),size=[w,h],bytes=Path(name).stat().st_size,gpu_mib_8bpp_mips=w*h*4/3/1048576))
    # Independent same-scene imports exercise decoded image identity reuse.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for seed,_ in PROOFS:bpy.ops.import_scene.gltf(filepath=str(Path(f'export/CoffeeShop-{seed}.gltf').resolve()))
    before=len(bpy.data.images);bpy.ops.import_scene.gltf(filepath=str(Path('export/CoffeeShop-117.gltf').resolve()));after=len(bpy.data.images);assert before==after
    if Path('build/photo-calibration.json').exists():
        from kit.photo_match import verify
        verify('build/photo-calibration.json')
    report=dict(status='form-stage export/resource/scale audit',shops=rows,pieces=pieces,accessible_knee_space=knee,preserved_existing_files=preserved,unique_images=len(image_uris),resources=resources,image_bytes=sum(Path(p).stat().st_size for p in image_uris),same_scene_image_counts=[before,after],limits='Reused charts overlap intentionally; quick swatch charts are not a unique baked UV atlas. Material finish, wear and full swept-door certification remain later gates.')
    Path('build/check.json').write_text(json.dumps(report,indent=2)+'\n');print('COFFEE CHECK',[(r['seed'],r['triangles']) for r in rows])


def ancestors(o):
    while o.parent:o=o.parent;yield o


if __name__=='__main__':
    if '--capture' in sys.argv:preserve(True);print('PRESERVATION CAPTURED')
    elif '--repeat' in sys.argv:repeat()
    else:main()
