"""Close port views of the actual imported GLB; optional receiver-wall section."""
import argparse,sys
from pathlib import Path
from types import SimpleNamespace
import bpy
from mathutils import Vector
from mathutils.kdtree import KDTree
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
import final_shots
from guns.common.render import main
import interface

def cut_receiver(source):
    """Identify receiver triangles from source, remove only its right half.

    The remaining geometry, UVs, materials, skin and clips are imported GLB
    data. Source mesh data is used solely for diagnostic face attribution.
    """
    import bmesh
    ref=BASE/'build/delivery/finalized.blend' if Path(source).parent.name=='export' else BASE/'build/bolt.blend'
    with bpy.data.libraries.load(str(ref),link=False) as (src,dst):dst.meshes=['Receiver'] if 'Receiver' in src.meshes else []
    # Mesh datablock names are not an interface: load the named object instead.
    for mesh in dst.meshes:
        if mesh and mesh.users==0:bpy.data.meshes.remove(mesh)
    with bpy.data.libraries.load(str(ref),link=False) as (src,dst):dst.objects=['Receiver']
    receiver=dst.objects[0];receiver.data.calc_loop_triangles()
    triangles=[[receiver.data.vertices[i].co.copy() for i in t.vertices] for t in receiver.data.loop_triangles]
    centers=[sum(points,Vector())/3 for points in triangles]
    tree=KDTree(len(centers))
    for i,p in enumerate(centers):tree.insert(p,i)
    tree.balance();removed=0
    for ob in [o for o in bpy.context.scene.objects if o.type=='MESH']:
        mesh=ob.data;selected=[]
        for f in mesh.polygons:
            points=[ob.matrix_world@mesh.vertices[i].co for i in f.vertices]
            p=sum(points,Vector())/len(points);_,index,distance=tree.find(p)
            if p.x>0 and distance<2e-7 and max(min((v-q).length for q in triangles[index]) for v in points)<2e-7:
                selected.append(f.index)
        if selected:
            # Keep the original imported corner normals, including hard edges.
            attr=mesh.attributes.new('SectionNormal','FLOAT_VECTOR','CORNER')
            attr.data.foreach_set('vector',[a for n in mesh.corner_normals for a in n.vector])
            bm=bmesh.new();bm.from_mesh(mesh);bm.faces.ensure_lookup_table()
            bmesh.ops.delete(bm,geom=[bm.faces[i] for i in selected],context='FACES')
            bm.to_mesh(mesh);bm.free()
            mesh.normals_split_custom_set([r.vector[:] for r in mesh.attributes['SectionNormal'].data])
            mesh.attributes.remove(mesh.attributes['SectionNormal']);removed+=len(selected)
    bpy.data.objects.remove(receiver,do_unlink=True)
    assert removed>0,'Receiver section must identify actual imported faces'
    bpy.context.scene['section_removed_receiver_triangles']=removed
    print('SECTION: removed',removed,'imported right receiver-wall triangles')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--clip',default='Fire');p.add_argument('--start',type=int,default=40)
    p.add_argument('--end',type=int,default=125);p.add_argument('--cutaway',action='store_true')
    a,remaining=p.parse_known_args(sys.argv[sys.argv.index('--')+1:])
    frames=list(range(a.start,a.end+1,2))
    if frames[-1]!=a.end:frames.append(a.end)
    shots={f'f{f:03d}':dict(location=(.34,.065,.145),target=(0,.155,.060),
            lens=58,aspect=1.8,exposure=-.15,action=a.clip,frame=f,time_s=f/60,
            background='transparent',section=a.cutaway) for f in frames}
    def configure(scene,source):
        if a.cutaway:cut_receiver(source)
        for shot in shots.values():shot['removed_receiver_triangles']=scene.get('section_removed_receiver_triangles',0)
        final_shots.configure_scene(scene,source)
        if scene.render.engine=='BLENDER_WORKBENCH':
            scene.display.shading.color_type='MATERIAL'
            for mat in bpy.data.materials:
                if not mat.use_nodes:continue
                bs=next((n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
                if bs:mat.diffuse_color=bs.inputs['Base Color'].default_value
    config=SimpleNamespace(FINAL_STAGE=True,RENDER_STAGE='actual exported GLB; receiver right wall removed for section only' if a.cutaway else 'actual exported GLB',
        DEFAULT_SHOTS=','.join(shots),SHOTS=shots,PHOTO_POSES={},
        floor_height=final_shots.floor_height,configure_scene=configure,prepare_shot=final_shots.prepare_shot)
    sys.argv=[sys.argv[0],'--',*remaining]
    main(config,interface)
