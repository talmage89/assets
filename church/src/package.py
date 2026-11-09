"""External-image glTF packages, exact embedded review copies and ledgers."""
import copy,hashlib,json,os,struct
from pathlib import Path
import numpy as np
import bpy
from kit.gltf import GLB,stabilize_tangents
from kit import tiling
import geometry as G


def objects(rt):return [rt,*rt.children_recursive]


def counts(obs):
    seen=set();unique=0;total=0;lo=np.full(3,np.inf);hi=-lo;materials=set();meshes=0
    bpy.context.view_layer.update()
    for ob in obs:
        if ob.type!='MESH':continue
        me=ob.data;me.calc_loop_triangles();n=len(me.loop_triangles);total+=n;meshes+=1
        if me not in seen:unique+=n;seen.add(me)
        materials.update(m.name for m in me.materials if m)
        xyz=np.array([ob.matrix_world@v.co for v in me.vertices])
        if len(xyz):lo=np.minimum(lo,xyz.min(0));hi=np.maximum(hi,xyz.max(0))
    return dict(triangles=total,unique_triangles=unique,meshes=meshes,materials=len(materials),material_names=sorted(materials),bounds_min=lo.tolist(),bounds_max=hi.tolist(),size_m=(hi-lo).tolist())


def canonical():
    folders=('downtown','houses','commercial','ground','trees','shrubs','cars','street-light','street-signs','street-furniture','fences','utility','church')
    out={}
    for folder in folders:
        for p in (G.ROOT/folder/'textures').rglob('*.png'):
            out.setdefault(hashlib.sha256(p.read_bytes()).digest(),p)
    return out


def externalize(source,out,known):
    raw=GLB(source);doc=copy.deepcopy(raw.json);data=raw.binary
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    for row in doc.get('images',[]):
        v=doc['bufferViews'][row.pop('bufferView')];a=v.get('byteOffset',0);payload=data[a:a+v['byteLength']]
        digest=hashlib.sha256(payload).digest();target=known.get(digest)
        if target is None:
            target=Path('textures/imported')/(digest.hex()[:20]+'.png');target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(payload);known[digest]=target.resolve()
        row['uri']=Path(os.path.relpath(target.resolve(),out.parent.resolve())).as_posix();row.pop('mimeType',None)
    ids=sorted({a['bufferView'] for a in doc['accessors']});remap={};views=[];binary=bytearray()
    for old in ids:
        v=copy.deepcopy(doc['bufferViews'][old]);start=v.get('byteOffset',0);payload=data[start:start+v['byteLength']]
        binary.extend(b'\0'*(-len(binary)%4));v['byteOffset']=len(binary);v['buffer']=0;binary.extend(payload)
        remap[old]=len(views);views.append(v)
    for accessor in doc['accessors']:accessor['bufferView']=remap[accessor['bufferView']]
    doc['bufferViews']=views;doc['buffers']=[dict(uri=out.with_suffix('.bin').name,byteLength=len(binary))]
    out.with_suffix('.bin').write_bytes(binary);out.write_text(json.dumps(doc,separators=(',',':'))+'\n')
    return doc


def publish(rt,stem,known,subdir=''):
    folder=Path('export')/subdir;review=Path('build/glb')/subdir;review.mkdir(parents=True,exist_ok=True)
    obs=objects(rt);meta=counts(obs);path=review/(stem+'.glb');tiling.export(path,obs)
    # Native MikkTSpace corners can straddle the exporter's fourth-decimal
    # rounding boundary. Exact position/normal/UV signatures guard these five
    # accepted corners; the kit permits at most one tangent rounding step.
    anchors=json.loads(Path(__file__).with_name('tangent_rounding.json').read_text())
    if stem in anchors:stabilize_tangents(path,anchors[stem])
    doc=externalize(path,folder/(stem+'.gltf'),known)
    meta['gltf_bin_bytes']=(folder/(stem+'.gltf')).stat().st_size+(folder/(stem+'.bin')).stat().st_size
    meta['glb_bytes']=path.stat().st_size;meta['images']=[r['uri'] for r in doc.get('images',[])]
    meta['source_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    (folder/(stem+'.json')).write_text(json.dumps(meta,indent=2));return meta


def save_scene(path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(path.resolve()))
