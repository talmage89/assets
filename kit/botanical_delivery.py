"""Independent botanical serialization checks; no constant is called a measurement.

Compare delivered accessors and a fresh Blender import against actual finalized
positions, linear Wind data and authored split normals. Generic kit verification
separately checks UVs, embedded PBR maps, material policy and budgets.
"""
import argparse,sys,json,hashlib,struct
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
from mathutils.kdtree import KDTree
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit.gltf import GLB


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--glb',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()))
    wanted={}
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH':continue
        tree=KDTree(len(ob.data.vertices));points=[]
        for v in ob.data.vertices:
            q=ob.matrix_world@v.co;tree.insert(q,v.index);points.append(list(q))
        tree.balance();normals={i:[] for i in range(len(points))}
        for loop,n in zip(ob.data.loops,ob.data.corner_normals):normals[loop.vertex_index].append(np.array(ob.matrix_world.to_3x3()@n.vector))
        wanted[ob.name]=dict(tree=tree,normals=normals,wind=np.array([v.color for v in ob.data.color_attributes['Wind'].data]))
    raw=GLB(a.glb);rows={};errors=[]
    for mesh in raw.json['meshes']:
        expected=wanted[mesh['name']];position_error=wind_error=normal_error=0.;count=0
        for prim in mesh['primitives']:
            attrs=prim['attributes']
            if '_WIND' not in attrs or any(k.startswith('COLOR_') for k in attrs):raise RuntimeError('Wind missing or multiplies albedo')
            w=raw.accessor(attrs['_WIND']);pos=raw.accessor(attrs['POSITION']);ns=raw.accessor(attrs['NORMAL'])
            # glTF +Y up back to Blender +Z up; root transforms are identity.
            pos=np.c_[pos[:,0],-pos[:,2],pos[:,1]];ns=np.c_[ns[:,0],-ns[:,2],ns[:,1]]
            for point,wind,n in zip(pos,w,ns):
                _,nearest,d=expected['tree'].find(Vector(point));position_error=max(position_error,d)
                candidates=expected['tree'].find_range(Vector(point),max(1e-7,d+1e-7))
                # Separate blades can share their petiole position but retain
                # different flutter and split normals. Match both on ONE
                # candidate; never pick unrelated independent minima.
                matches=[]
                for _,i,_ in candidates:
                    we=float(np.max(np.abs(wind-expected['wind'][i])))
                    ne=min(float(np.linalg.norm(n-e)) for e in expected['normals'][i])
                    matches.append((max(we/1e-6,ne/3e-4),we,ne))
                _,we,ne=min(matches);wind_error=max(wind_error,we);normal_error=max(normal_error,ne)
            count+=len(pos)
        rows[mesh['name']]=dict(delivered_vertices=count,max_position_error_m=position_error,max_wind_error=wind_error,max_normal_vector_error=normal_error)
        if position_error>2e-5 or wind_error>1e-6 or normal_error>3e-4:errors.append(mesh['name']+': botanical serialization changed')
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH':continue
        expected=wanted[ob.name];attr=ob.data.color_attributes.get('_WIND')
        if attr is None:errors.append(ob.name+': importer lost RGBA wind attribute');continue
        error=0
        for v,value in zip(ob.data.vertices,attr.data):
            point=ob.matrix_world@v.co;_,_,distance=expected['tree'].find(point)
            candidates=expected['tree'].find_range(point,max(1e-7,distance+1e-7))
            error=max(error,min(float(np.max(np.abs(np.array(value.color)-expected['wind'][i]))) for _,i,_ in candidates))
        rows[ob.name]['reimport_wind_max_error']=error
        if error>1e-6:errors.append(ob.name+': imported wind changed')
    texture_bytes=sum(len(raw.image(i)) for i in range(len(raw.json['images'])))
    used=set()
    for mesh in raw.json['meshes']:
        for primitive in mesh['primitives']:
            used.update(primitive['attributes'].values());used.add(primitive['indices'])
    geometry_bytes=sum(raw.accessor(i).nbytes for i in used)
    image_sizes=[struct.unpack_from('>II',raw.image(i),16) for i in range(len(raw.json['images']))]
    texture_mib=sum(w*h*4/3 for w,h in image_sizes)/1024**2
    result=dict(passed=not errors,errors=errors,glb_bytes=a.glb.stat().st_size,embedded_texture_bytes=texture_bytes,
                glb_sha256=hashlib.sha256(a.glb.read_bytes()).hexdigest(),meshes=rows,
                gpu_mib_bc7_bc5_bc7_full_mips=texture_mib,embedded_image_dimensions=image_sizes,geometry_accessor_bytes=geometry_bytes,
                estimated_total_gpu_mib=texture_mib+geometry_bytes/1024**2,
                memory_scope='Estimate for 8-bpp BaseColor-alpha, BC5 normal, 8-bpp ORM, full mip chains; PNG and uncompressed runtime sizes differ',
                scope='Serialization of actual finalized positions, split normals and vertex RGBA wind; appearance established only by GLB photo pairs')
    a.out.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
    if errors:raise RuntimeError('Botanical delivery failed')

if __name__=='__main__':main()
