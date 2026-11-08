"""Kit atlas/pivot export, then lossless external glTF with family-shared images."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(Path(__file__).resolve().parent),str(ROOT)]
from kit import export
from kit.gltf import GLB

def main():
    parser=argparse.ArgumentParser(add_help=False);parser.add_argument('--out',required=True);parser.add_argument('--report',required=True);parser.add_argument('--variant',type=int,default=101)
    a,_=parser.parse_known_args(sys.argv[sys.argv.index('--')+1:])
    # The general exporter keeps orphan roots, including untagged bake molds.
    # Strip this asset's explicit bake-only sources in an ignored staging copy.
    index=sys.argv.index('--source')+1;source=Path(sys.argv[index]).resolve()
    bpy.ops.wm.open_mainfile(filepath=str(source))
    for ob in list(bpy.context.scene.objects):
        if ob.get('bake_only'):bpy.data.objects.remove(ob,do_unlink=True)
    staged=source.parent/'export-source.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(staged))
    old_source=sys.argv[index];sys.argv[index]=str(staged)
    try:export.main()
    finally:sys.argv[index]=old_source
    path=Path(a.out);glb=GLB(path);d=glb.json
    root=next(n for n in d['nodes'] if n['name']=='SchoolBus');root.setdefault('extras',{})['seed']=a.variant
    from spec import SEEDS
    root['extras'].update(SEEDS[a.variant])
    for mat in d['materials']:
        if 'Lamps' in mat['name']:mat.setdefault('extras',{}).update(alpha_semantic='emission power divided by 80',states={'red':14,'amber':10,'headlight':5,'dome':2,'strobe':20},default='off')
        if 'Paint' in mat['name']:
            mat['extensions']['KHR_materials_clearcoat']['clearcoatFactor']={101:.25,102:.20,103:.14}[a.variant]
    d['asset']['extras']=dict(checkpoint='round 2 look development',seed=a.variant,
        age_variation='Shared baked wear; seed-specific causal vertex deposits and enamel coat loss')
    shared=path.parent/'shared';shared.mkdir(exist_ok=True);image_views=[];image_hashes={}
    source_hash=hashlib.sha256(b''.join((path.parent.parent/'textures/2k'/f'T_SchoolBus_{c}.png').read_bytes() for c in ['BaseColor','Normal','ORM'])).hexdigest()
    stamp=shared/'atlas-source.json';new_generation=not stamp.exists() or json.loads(stamp.read_text())['source_hash']!=source_hash
    for i,im in enumerate(d['images']):
        name=im.get('name','image-'+str(i));filename=name if name.endswith('.png') else name+'.png';payload=glb.image(i);target=shared/filename
        if target.exists() and target.read_bytes()!=payload and not new_generation:raise ValueError('Shared atlas changed across seeds: '+filename)
        target.write_bytes(payload);image_views.append(im.pop('bufferView'));im.pop('mimeType',None);im['uri']='shared/'+filename;image_hashes[filename]=hashlib.sha256(payload).hexdigest()
    stamp.write_text(json.dumps(dict(source_hash=source_hash,images=image_hashes),indent=2))
    # Remove image views and their bytes; geometry stays byte-exact.
    used=[i for i in range(len(d['bufferViews'])) if i not in image_views];remap={old:new for new,old in enumerate(used)};payload=bytearray();views=[]
    for old in used:
        view=dict(d['bufferViews'][old]);start=view.get('byteOffset',0);block=glb.binary[start:start+view['byteLength']]
        payload.extend(b'\0'*((-len(payload))%4));view['byteOffset']=len(payload);payload.extend(block);views.append(view)
    positions={prim['attributes']['POSITION']:glb.accessor(prim['attributes']['POSITION']) for mesh in d['meshes'] for prim in mesh['primitives']}
    for ac in d['accessors']:ac['bufferView']=remap[ac['bufferView']]
    # Fleet age darkens only the actual lower-body splash/wake region, in vertex color.
    # All seeds retain byte-identical shared images and stock glTF PBR behavior.
    strength={101:0,102:.17,103:.30}[a.variant]
    for node_index,node in enumerate(d['nodes']):
        if 'mesh' not in node:continue
        xf=glb.world(node_index)
        for prim in d['meshes'][node['mesh']]['primitives']:
            name=d['materials'][prim['material']]['name']
            if not any(k in name for k in ['Paint','Opaque']):continue
            ps=positions[prim['attributes']['POSITION']];world=(xf@np.c_[ps,np.ones(len(ps))].T).T
            y=-world[:,2];z=world[:,1]
            side=np.clip((np.abs(world[:,0])-.88)/.28,0,1)
            grain=.70+.30*np.sin(y*(8.7+a.variant*.011)+z*23)**2
            wake=np.maximum(*[np.clip((y-ax-.18)/.25,0,1)*np.clip((ax+1.8-y)/1.4,0,1)*np.clip((1.30-.18*(y-ax)-z)/.35,0,1) for ax in [-4.953,1.9812]])
            mask=side*np.maximum(np.clip((1.08-z)/.31,0,1)*.55,wake)*grain
            if 'Opaque' in name:
                wheel=np.maximum(*[np.clip((.44-np.hypot(y-ax,z-.523))/.22,0,1) for ax in [-4.953,1.9812]])
                mask=np.maximum(mask,side*wheel*.75)
            mask=np.clip(mask,0,1)
            rgb=np.c_[1-strength*mask*.94,1-strength*mask*1.04,1-strength*mask*1.18,np.ones(len(ps))].astype('<f4')
            payload.extend(b'\0'*((-len(payload))%4));view_index=len(views);views.append(dict(buffer=0,byteOffset=len(payload),byteLength=rgb.nbytes,target=34962));payload.extend(rgb.tobytes())
            accessor_index=len(d['accessors']);d['accessors'].append(dict(bufferView=view_index,componentType=5126,count=len(rgb),type='VEC4'));prim['attributes']['COLOR_0']=accessor_index
    d['bufferViews']=views;binpath=path.with_suffix('.bin');binpath.write_bytes(payload);d['buffers']=[dict(uri=binpath.name,byteLength=len(payload))]
    gltf=path.with_suffix('.gltf');gltf.write_text(json.dumps(d,separators=(',',':')))
    report=json.loads(Path(a.report).read_text());report.update(external_gltf=gltf.name,external_bytes=gltf.stat().st_size+binpath.stat().st_size,shared_images=image_hashes)
    Path(a.report).write_text(json.dumps(report,indent=2));print('BUS_EXTERNAL',gltf,report['external_bytes'],flush=True)
if __name__=='__main__':main()
