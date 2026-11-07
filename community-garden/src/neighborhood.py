"""Package the native neighborhood with shared external image identities.

Only this family's exports/cache are written. Native delivery files stay
read-only; their packed images are losslessly externalized when necessary.
"""
import hashlib,json,os,shutil,struct
from pathlib import Path
import bpy
import geometry as Q


def digest(path):
    p=Path(path);d=json.loads(p.read_text());files=[p]+[p.parent/r['uri'] for k in ('buffers','images') for r in d.get(k,[]) if r.get('uri')]
    return hashlib.sha256(b''.join(hashlib.sha256(f.read_bytes()).digest() for f in files)).hexdigest()


def preserve_native_corner(path,repo):
    """Retain one original native-car tangent at a Mikk rounding boundary.

    This follows kit.gltf's guarded-anchor policy. Exact source position,
    normal and UV signatures must match; only a single four-decimal rounding
    step is accepted. Never quantize geometry or use a previous site binary.
    """
    import numpy as np
    from kit.gltf import GLB
    source=GLB(repo/'cars/export/AlderH120.glb');doc=json.loads(path.read_text());binary=path.with_suffix('.bin');data=bytearray(binary.read_bytes())
    current=GLB.__new__(GLB);current.json=doc;current.binary=bytes(data)
    native=next(m for m in source.json['meshes'] if m.get('name')=='AlderH120Mesh')['primitives'][2]
    targets=[m for m in doc['meshes'] if m.get('name')=='AlderH120Mesh'];assert len(targets)==1
    target=targets[0]['primitives'][2];vertex=1343
    for attr in ('POSITION','NORMAL','TEXCOORD_0'):
        assert np.array_equal(current.accessor(target['attributes'][attr])[vertex],source.accessor(native['attributes'][attr])[vertex]),'Native tangent corner signature changed: '+attr
    expected=source.accessor(native['attributes']['TANGENT'])[vertex];actual=current.accessor(target['attributes']['TANGENT'])[vertex]
    delta=float(np.max(np.abs(actual-expected)));assert delta<=.00011,'Native tangent differs by more than one rounding step'
    ac=doc['accessors'][target['attributes']['TANGENT']];view=doc['bufferViews'][ac['bufferView']]
    assert ac['componentType']==5126 and ac['type']=='VEC4'
    offset=view.get('byteOffset',0)+ac.get('byteOffset',0)+vertex*view.get('byteStride',16)
    struct.pack_into('<4f',data,offset,*expected);binary.write_bytes(data)
    receipt=Path('build/context')/(path.stem+'-native-tangent.json');receipt.parent.mkdir(parents=True,exist_ok=True)
    receipt.write_text(json.dumps(dict(source='cars/export/AlderH120.glb',mesh='AlderH120Mesh',primitive=2,vertex=vertex,max_rounding_delta=delta,
        guards='exact original position/normal/UV; preserve original source tangent; maximum one four-decimal step'),indent=2))


def export(path,repo):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    canonical={}
    for folder in (Path('textures/checkpoint'),Path('build/context/chain'),repo/'ground/textures/ship',Path('textures/context')):
        for p in folder.glob('*.png'):canonical[hashlib.sha256(p.read_bytes()).hexdigest()]=p.resolve()
    bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLTF_SEPARATE',
        export_extras=True,export_animations=False,export_tangents=True,export_attributes=True,
        export_vertex_color='MATERIAL',export_all_vertex_colors=False,
        export_image_format='AUTO',export_texture_dir='site-cache')
    doc=json.loads(path.read_text());rows=[]
    # Semantic source swatches share exactly one stock PBR material in glTF.
    atlas=[i for i,m in enumerate(doc.get('materials',[])) if m.get('name','').startswith('Garden_') and m.get('extras',{}).get('garden_finish')]
    if atlas:
        chosen=atlas[0];doc['materials'][chosen]['name']='GardenSurfaces'
        doc['materials'][chosen].get('extras',{}).pop('garden_finish',None)
        for mesh in doc['meshes']:
            for primitive in mesh['primitives']:
                if primitive.get('material') in atlas:primitive['material']=chosen
        used={p.get('material') for m in doc['meshes'] for p in m['primitives']};remap={old:new for new,old in enumerate(sorted(used))}
        doc['materials']=[doc['materials'][i] for i in sorted(used)]
        for mesh in doc['meshes']:
            for primitive in mesh['primitives']:primitive['material']=remap[primitive['material']]
    for row in doc.get('images',[]):
        copied=path.parent/row['uri'];data=copied.read_bytes();sha=hashlib.sha256(data).hexdigest();target=canonical.get(sha)
        if target is None:
            target=Path('textures/context')/('T_Native_'+sha[:20]+'.png');target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(data);target=target.resolve();canonical[sha]=target
        rows.append(dict(image=row.get('name'),sha256=sha,path=os.path.relpath(target,Path.cwd()),bytes=len(data)))
        row['uri']=os.path.relpath(target,path.parent.resolve());row.pop('mimeType',None)
    path.write_text(json.dumps(doc,separators=(',',':'))+'\n');shutil.rmtree(path.parent/'site-cache',ignore_errors=True)
    preserve_native_corner(path,repo)
    return rows


def prepare(seed,repo,recipe,context):
    """CPU assembly/cache boundary shared by checks and GPU presentation."""
    garden=Path(f'export/checkpoint/Garden_{seed}.gltf');scene=Path(f'export/checkpoint/Site_{seed}.gltf');receipt=Path(f'build/context/site-{seed}.json')
    package_recipe=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    old=json.loads(receipt.read_text()) if receipt.exists() else {};valid=False
    if scene.exists():
        try:valid=old.get('scene_bundle')==digest(scene)
        except (OSError,KeyError):pass
    if valid and old.get('garden_bundle')==digest(garden) and old.get('render_recipe')==recipe and old.get('package_recipe')==package_recipe:return scene,receipt
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(garden.resolve()))
    p=json.loads(Path(f'build/garden-{seed}.json').read_text())['plan'];rt=context(p)
    expected=sum(Q.count(o) for o in bpy.context.scene.objects if not o.parent);maps=export(scene,repo)
    receipt.write_text(json.dumps(dict(garden_bundle=digest(garden),render_recipe=recipe,package_recipe=package_recipe,
        scene_bundle=digest(scene),triangles=expected,context_triangles=Q.count(rt),images=maps),indent=2))
    return scene,receipt
