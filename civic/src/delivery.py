"""Consolidate fixed construction, externalize exact maps, count real payloads."""
import hashlib,json,os,copy,struct
from pathlib import Path
import bpy,bmesh,numpy as np
from mathutils import Matrix
from geo import ROOT,LOCAL


def counts(obs):
    bpy.context.view_layer.update();rows=[];lo=np.full(3,np.inf);hi=-lo;materials=set();unique={}
    for ob in obs:
        if ob.type!='MESH':continue
        me=ob.data;me.calc_loop_triangles();n=len(me.loop_triangles);unique[me.name]=n
        xyz=np.array([ob.matrix_world@v.co for v in me.vertices])
        if len(xyz):lo=np.minimum(lo,xyz.min(0));hi=np.maximum(hi,xyz.max(0))
        used={ob.material_slots[f.material_index].material.name for f in me.polygons if ob.material_slots}
        materials.update(used);rows.append(dict(name=ob.name,kind=ob.get('module_kind','context'),triangles=n))
    return dict(triangles=sum(r['triangles'] for r in rows),unique_triangles=sum(unique.values()),materials=len(materials),material_names=sorted(materials),bounds_min=lo.tolist(),bounds_max=hi.tolist(),size_m=(hi-lo).tolist(),pieces=rows)


def consolidate(assembly):
    # Preserve modules as source evidence; only fixed immediate children join.
    bpy.context.view_layer.update()
    for parent in [assembly.root]+list(assembly.moving.values()):
        obs=[o for o in parent.children if o.type=='MESH' and not o.get('kinematic_guide')]
        if not obs:continue
        bpy.ops.object.select_all(action='DESELECT')
        for ob in obs:ob.select_set(True)
        bpy.context.view_layer.objects.active=obs[0]
        if len(obs)>1:bpy.ops.object.join()
        ob=bpy.context.object;ob.name=parent.name+'__Mesh';ob.data.transform(ob.matrix_basis);ob.matrix_basis=Matrix.Identity(4)


def bundle(path):
    doc=json.loads(path.read_text());files=[path]+[path.parent/r['uri'] for k in ('buffers','images') for r in doc.get(k,[])]
    return hashlib.sha256(b''.join(p.name.encode()+p.read_bytes() for p in files)).hexdigest()


def embed(path,out):
    doc=json.loads(path.read_text());data=bytearray((path.parent/doc['buffers'][0].pop('uri')).read_bytes())
    for im in doc.get('images',[]):
        payload=(path.parent/im.pop('uri')).read_bytes();data.extend(b'\0'*(-len(data)%4))
        im.update(bufferView=len(doc['bufferViews']),mimeType='image/png')
        doc['bufferViews'].append(dict(buffer=0,byteOffset=len(data),byteLength=len(payload)));data.extend(payload)
    doc['buffers'][0]['byteLength']=len(data);data.extend(b'\0'*(-len(data)%4))
    js=json.dumps(doc,separators=(',',':')).encode();js+=b' '*(-len(js)%4)
    payload=struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(data),0x004e4942)+data
    out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(struct.pack('<III',0x46546c67,2,12+len(payload))+payload)


def publish(stem,objects):
    from PIL import Image
    bpy.ops.object.select_all(action='DESELECT')
    for ob in objects:ob.select_set(True)
    path=Path('export')/(stem+'.gltf');path.parent.mkdir(exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLTF_SEPARATE',export_texture_dir='shared',use_selection=True,export_yup=True,export_extras=True,export_animations=False,export_tangents=True,export_attributes=True,export_vertex_color='NAME',export_vertex_color_name='Tint',export_all_vertex_colors=False)
    doc=json.loads(path.read_text());known={}
    for folder in (LOCAL/'textures',ROOT/'ground/textures',ROOT/'trees/textures',ROOT/'shrubs/textures',ROOT/'fences/chain-link/textures',ROOT/'cars/textures',ROOT/'street-light/textures'):
        for p in folder.rglob('*.png'):
            if '/ship/' in p.as_posix():known[hashlib.sha256(p.read_bytes()).digest()]=p
    images=[]
    for im in doc.get('images',[]):
        copied=path.parent/im['uri'];target=known.get(hashlib.sha256(copied.read_bytes()).digest())
        if target is None:
            # Preserve exact canonical PNG bytes when import/export re-encodes.
            pix=np.array(Image.open(copied).convert('RGBA'))
            for candidate in known.values():
                with Image.open(candidate) as image:
                    if image.size==(pix.shape[1],pix.shape[0]) and np.array_equal(pix,np.array(image.convert('RGBA'))):target=candidate;break
        if target is None:target=copied.resolve()
        im['uri']=Path(os.path.relpath(target,path.parent.resolve())).as_posix();images.append(im['uri'])
    for mesh in doc.get('meshes',[]):
        for pr in mesh['primitives']:
            ma=doc['materials'][pr['material']]
            if ma.get('extras',{}).get('tiling_vertex_tint') is not True:pr['attributes'].pop('COLOR_0',None)
    path.write_text(json.dumps(doc,separators=(',',':'))+'\n');embed(path,Path('build/review')/(stem+'.glb'))
    result=dict(gltf=str(path),sha256=bundle(path),gltf_bytes=path.stat().st_size,bin_bytes=path.with_suffix('.bin').stat().st_size,images=images,materials=len(doc.get('materials',[])))
    result['placed_triangles']=sum(doc['accessors'][p['indices']]['count']//3 for n in doc.get('nodes',[]) if 'mesh' in n for p in doc['meshes'][n['mesh']]['primitives'])
    print('CIVIC EXPORT',stem,result['placed_triangles'],flush=True);return result
