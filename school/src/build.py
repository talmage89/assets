"""Deterministic school look-dev, six external-image glTF packages."""
import argparse,hashlib,json,os,struct,sys,math
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(HERE),str(ROOT)]
from geometry import consolidate,clean_surfaces
from plans import school
from buildings import build_school
from siteworks import build_site,clear_templates,CACHE


def preserve_library_tangent(path):
    """Retain the accepted oak's one four-decimal MikkTSpace boundary corner.

    Exact position/normal/UV signatures and the kit's one-step bound guard the
    repair. Geometry, UVs and normals are never rounded or changed. The source
    of truth is the read-only canonical oak, never a previous school export.
    """
    if not path.stem.startswith('Campus'):return
    from kit.gltf import GLB,stabilize_tangents
    canonical=GLB(ROOT/'trees/export/PinOak.glb');cp=canonical.json['meshes'][1]['primitives'][0]
    reference={key:canonical.accessor(cp['attributes'][semantic])[10180].tolist() for key,semantic in [('position','POSITION'),('normal','NORMAL'),('uv','TEXCOORD_0'),('tangent','TANGENT')]}
    doc=json.loads(path.read_text());binary=(path.parent/doc['buffers'][0]['uri']).read_bytes()
    raw=object.__new__(GLB);raw.json=doc;raw.binary=binary;anchors=[]
    for mi,mesh in enumerate(doc['meshes']):
        if not mesh['name'].startswith('Trunk and branches'):continue
        for pi,primitive in enumerate(mesh['primitives']):
            at=primitive['attributes'];mask=np.ones(doc['accessors'][at['POSITION']]['count'],dtype=bool)
            for key,semantic in [('position','POSITION'),('normal','NORMAL'),('uv','TEXCOORD_0')]:mask &= np.all(raw.accessor(at[semantic])==np.asarray(reference[key],dtype=np.float32),axis=1)
            for vertex in np.flatnonzero(mask):anchors.append(dict(mesh=mi,primitive=pi,vertex=int(vertex),**reference))
    assert len(anchors)==1,('Canonical oak rounding signature changed',path,len(anchors))
    # The existing guarded kit helper consumes GLB. Wrap the external payload
    # temporarily; external image URIs need no conversion or image rewriting.
    wrapped=json.loads(path.read_text());wrapped['buffers'][0].pop('uri')
    js=json.dumps(wrapped,separators=(',',':')).encode();js+=b' '*((-len(js))%4)
    payload=binary+b'\0'*((-len(binary))%4)
    stage=Path('build/tangent-stage.glb')
    stage.write_bytes(struct.pack('<III',0x46546c67,2,28+len(js)+len(payload))+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(payload),0x004e4942)+payload)
    stabilize_tangents(stage,anchors)
    (path.parent/doc['buffers'][0]['uri']).write_bytes(GLB(stage).binary[:len(binary)])
    stage.unlink()


def counts(objects=None):
    obs=[o for o in (objects or bpy.context.scene.objects) if o.type=='MESH']
    bpy.context.view_layer.update();lo=np.full(3,np.inf);hi=-lo;triangles=0;materials=set();unique=set();uniquetris=0
    for ob in obs:
        me=ob.data;me.calc_loop_triangles();triangles+=len(me.loop_triangles)
        if me not in unique:uniquetris+=len(me.loop_triangles);unique.add(me)
        for f in me.polygons:
            if ob.material_slots and ob.material_slots[f.material_index].material:materials.add(ob.material_slots[f.material_index].material.name)
        xyz=np.empty(len(me.vertices)*3);me.vertices.foreach_get('co',xyz);xyz=xyz.reshape(-1,3);xf=np.array(ob.matrix_world);xyz=xyz@xf[:3,:3].T+xf[:3,3]
        if len(xyz):lo=np.minimum(lo,xyz.min(0));hi=np.maximum(hi,xyz.max(0))
    return dict(triangles=triangles,unique_triangles=uniquetris,materials=len(materials),material_names=sorted(materials),meshes=len(obs),bounds_min=lo.tolist(),bounds_max=hi.tolist(),size_m=(hi-lo).tolist())


def share_images(path):
    from PIL import Image
    d=json.loads(path.read_text());candidates=[]
    # Untinted library materials must never receive the active botanical Wind
    # color attribute as COLOR_0. Keep _WIND data; remove the unintended color
    # multiplier, exactly as the kit's tiling exporter does for untinted PBR.
    for mesh in d['meshes']:
        for primitive in mesh['primitives']:
            ma=d['materials'][primitive['material']]
            if ma.get('extras',{}).get('tiling_vertex_tint') is not True:primitive['attributes'].pop('COLOR_0',None)
    for folder in (ROOT/'ground/textures/ship',ROOT/'commercial/textures/ship',ROOT/'houses/textures/ranch-ship',ROOT/'trees/textures/ship',ROOT/'trees/textures/oak/ship',ROOT/'fences/chain-link/textures/ship',Path('textures/checkpoint')):
        candidates.extend(folder.resolve().glob('*.png'))
    hashes={hashlib.sha256(p.read_bytes()).digest():p for p in candidates};used=[]
    for row in d.get('images',[]):
        copied=path.parent/row['uri'];digest=hashlib.sha256(copied.read_bytes()).digest();target=hashes.get(digest)
        if target is None:
            # glTF sometimes re-encodes an imported embedded PNG. Redirect only
            # after a pixel-by-pixel identity check to the canonical original.
            image=Image.open(copied);a=np.array(image.convert('RGBA'))
            for candidate in candidates:
                im=Image.open(candidate)
                if im.size==image.size and np.array_equal(a,np.array(im.convert('RGBA'))):target=candidate;break
        if target is None:
            target=Path('textures/checkpoint')/copied.name;target.parent.mkdir(parents=True,exist_ok=True)
            if not target.exists() or target.read_bytes()!=copied.read_bytes():target.write_bytes(copied.read_bytes())
            target=target.resolve()
        row['uri']=Path(os.path.relpath(target,path.parent.resolve())).as_posix();used.append(row['uri'])
    path.write_text(json.dumps(d,separators=(',',':'))+'\n')
    return used


def publish(stem,p,root,building_count=None):
    clear_templates();bpy.context.view_layer.update();meta=counts();meta.update(plan=p,stage=p['stage'],building=building_count or meta.copy())
    source=Path('build')/(stem+'.blend');source.parent.mkdir(exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(source.resolve()))
    consolidate();out=Path('export')/(stem+'.gltf');out.parent.mkdir(exist_ok=True)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(filepath=str(out.resolve()),export_format='GLTF_SEPARATE',export_texture_dir='shared',use_selection=True,export_yup=True,export_extras=True,export_animations=False,export_tangents=True,export_attributes=True,export_vertex_color='NAME',export_vertex_color_name='Tint',export_all_vertex_colors=False)
    meta['images']=share_images(out);preserve_library_tangent(out);doc=json.loads(out.read_text());meta['gltf_bytes']=out.stat().st_size;meta['bin_bytes']=sum((out.parent/r['uri']).stat().st_size for r in doc['buffers'])
    meta['serialized_triangles']=sum(sum(doc['accessors'][q['indices']]['count']//3 for q in doc['meshes'][n['mesh']]['primitives']) for n in doc['nodes'] if 'mesh' in n)
    meta['primitives']=sum(len(doc['meshes'][n['mesh']]['primitives']) for n in doc['nodes'] if 'mesh' in n)
    assert meta['serialized_triangles']==meta['triangles'],(stem,meta['serialized_triangles'],meta['triangles'])
    out.with_suffix('.json').write_text(json.dumps(meta,indent=2));source.with_suffix('.json').write_text(json.dumps(meta,indent=2))
    print('PUBLISHED',stem,meta['triangles'],meta['materials'],flush=True);return meta


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seeds',default='101,102,103');ap.add_argument('--out',type=Path,default=Path('build/family.blend'));args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);report={}
    for seed in map(int,args.seeds.split(',')):
        bpy.ops.wm.read_factory_settings(use_empty=True);CACHE.clear();bpy.context.scene.unit_settings.system='METRIC'
        from surfaces import apply
        p=school(seed);a=build_school(p);apply(p);p['source_zero_area_cleanup']=clean_surfaces();bc=counts()
        report[f'School-{seed}']=publish(f'School-{seed}',p,a.root)
        site=build_site(p,a);apply(p);p['site_zero_area_cleanup']=clean_surfaces();site.root.rotation_euler.z=math.radians(p['site_yaw'])
        report[f'Campus-{seed}']=publish(f'Campus-{seed}',p,site.root,bc)
    args.out.parent.mkdir(exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(args.out.resolve()))
    Path('build/family.json').write_text(json.dumps(report,indent=2))
    used={(f.parent/row['uri']).resolve() for f in Path('export').glob('*.gltf') for row in json.loads(f.read_text()).get('images',[])}
    for image in Path('export/shared').glob('*.png'):
        if image.resolve() not in used:image.unlink()

if __name__=='__main__':main()
