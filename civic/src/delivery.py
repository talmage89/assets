"""Consolidate fixed construction, externalize exact maps, count real payloads."""
import hashlib,json,os,copy,struct
from pathlib import Path
import bpy,bmesh,numpy as np
from mathutils import Matrix
from geo import ROOT,LOCAL


def counts(obs):
    bpy.context.view_layer.update();rows=[];lo=np.full(3,np.inf);hi=-lo;materials=set();unique={};image_cache={};all_images={}
    def images_for(names):
        images={}
        for name in sorted(names):
            material=bpy.data.materials[name]
            if not material.use_nodes:continue
            for node in material.node_tree.nodes:
                if node.type!='TEX_IMAGE' or not node.image:continue
                im=node.image
                if im.name not in image_cache:
                    data=bytes(im.packed_file.data) if im.packed_file else Path(bpy.path.abspath(im.filepath)).read_bytes()
                    w,h=im.size;key=hashlib.sha256(data).hexdigest()
                    image_cache[im.name]=(key,dict(name=im.name,sha256=key,width=w,height=h,bytes=len(data),gpu_mib=w*h*4/3/1048576))
                key,row=image_cache[im.name];images[key]=row
        return images
    for ob in obs:
        if ob.type!='MESH':continue
        me=ob.data;me.calc_loop_triangles();n=len(me.loop_triangles);unique[me.name]=n
        xyz=np.array([ob.matrix_world@v.co for v in me.vertices])
        if len(xyz):lo=np.minimum(lo,xyz.min(0));hi=np.maximum(hi,xyz.max(0))
        used={ob.material_slots[f.material_index].material.name for f in me.polygons if ob.material_slots}
        images=images_for(used);all_images.update(images)
        materials.update(used);rows.append(dict(name=ob.name,kind=ob.get('module_kind','context'),triangles=n,materials=len(used),material_names=sorted(used),image_gpu_mib=sum(v['gpu_mib'] for v in images.values())))
    ordered=[v for _,v in sorted(all_images.items())]
    return dict(triangles=sum(r['triangles'] for r in rows),unique_triangles=sum(unique.values()),materials=len(materials),material_names=sorted(materials),bounds_min=lo.tolist(),bounds_max=hi.tolist(),size_m=(hi-lo).tolist(),image_gpu_mib=sum(v['gpu_mib'] for v in ordered),images=ordered,pieces=rows)


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


def preserve_known_tangents(path):
    """Use the existing signature-bound guard for two four-decimal ties.

    Blender's MikkTSpace re-encoding occasionally rounds this single component
    by .0001. The original oak is read only; no geometry/UV/normal can change.
    """
    if not path.stem.startswith('Site-'):return
    from kit.gltf import GLB,stabilize_tangents
    original=GLB(ROOT/'trees/export/PinOak.glb');pr=original.json['meshes'][1]['primitives'][0]
    signature={key:original.accessor(pr['attributes'][semantic])[10180].tolist() for key,semantic in [('position','POSITION'),('normal','NORMAL'),('uv','TEXCOORD_0'),('tangent','TANGENT')]}
    doc=json.loads(path.read_text());binary=(path.parent/doc['buffers'][0]['uri']).read_bytes();raw=object.__new__(GLB);raw.json=doc;raw.binary=binary;anchors=[]
    for mi,mesh in enumerate(doc['meshes']):
        if not mesh['name'].startswith('Trunk and branches'):continue
        for pi,primitive in enumerate(mesh['primitives']):
            at=primitive['attributes'];mask=np.ones(doc['accessors'][at['POSITION']]['count'],dtype=bool)
            for key,semantic in [('position','POSITION'),('normal','NORMAL'),('uv','TEXCOORD_0')]:mask &= np.all(raw.accessor(at[semantic])==np.asarray(signature[key],dtype=np.float32),axis=1)
            for vertex in np.flatnonzero(mask):anchors.append(dict(mesh=mi,primitive=pi,vertex=int(vertex),**signature))
    assert len(anchors)==1,('Native oak signature changed',path,len(anchors))
    if path.stem=='Site-202':
        # The curved corner-cut sheet has one MikkTSpace component on a
        # four-decimal rounding boundary. Keep the first measured export's
        # .2175 value. Exact position/normal/UV signatures and the kit's one-
        # step bound reject any geometry change instead of hiding it.
        owned=dict(position=[-1.0731210708618164,.020999999716877937,25.114761352539062],normal=[0,-1,0],uv=[.15000000596046448,.9240909218788147],tangent=[-.9760000109672546,0,.2175000011920929,1])
        found=[]
        for mi,mesh in enumerate(doc['meshes']):
            for pi,pr in enumerate(mesh['primitives']):
                if doc['materials'][pr['material']]['name']!='CivicWeather':continue
                at=pr['attributes'];mask=np.ones(doc['accessors'][at['POSITION']]['count'],dtype=bool)
                for key,semantic in [('position','POSITION'),('normal','NORMAL'),('uv','TEXCOORD_0')]:mask &= np.all(raw.accessor(at[semantic])==np.asarray(owned[key],dtype=np.float32),axis=1)
                found += [dict(mesh=mi,primitive=pi,vertex=int(vertex),**owned) for vertex in np.flatnonzero(mask)]
        assert len(found)==1,('Civic weather tangent signature changed',len(found));anchors.extend(found)
    stage=Path('build/tangent-stage.glb');wrapped=copy.deepcopy(doc);wrapped['buffers'][0].pop('uri');js=json.dumps(wrapped,separators=(',',':')).encode();js+=b' '*(-len(js)%4);data=binary+b'\0'*(-len(binary)%4)
    payload=struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(data),0x004e4942)+data;stage.write_bytes(struct.pack('<III',0x46546c67,2,12+len(payload))+payload)
    stabilize_tangents(stage,anchors);(path.parent/doc['buffers'][0]['uri']).write_bytes(GLB(stage).binary[:len(binary)]);stage.unlink()


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
    path.write_text(json.dumps(doc,separators=(',',':'))+'\n');preserve_known_tangents(path);embed(path,Path('build/review')/(stem+'.glb'))
    result=dict(gltf=str(path),sha256=bundle(path),gltf_bytes=path.stat().st_size,bin_bytes=path.with_suffix('.bin').stat().st_size,images=images,materials=len(doc.get('materials',[])))
    result['placed_triangles']=sum(doc['accessors'][p['indices']]['count']//3 for n in doc.get('nodes',[]) if 'mesh' in n for p in doc['meshes'][n['mesh']]['primitives'])
    print('CIVIC EXPORT',stem,result['placed_triangles'],flush=True);return result
