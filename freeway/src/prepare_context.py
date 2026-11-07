"""Read existing original library deliveries; stage local context copies only.

Missing signals/utility builds are generated from their existing construction
functions with quick form materials. Existing deliveries are never rebuilt or
written. Context simplification belongs to this checkpoint, not those families.
"""
import argparse,sys,math,json
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from kit import model as G
from kit.tiling import world_uv

def export(path,objects):
    path.parent.mkdir(parents=True,exist_ok=True);bpy.ops.object.select_all(action='DESELECT')
    for ob in objects:ob.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLB',use_selection=True,
        export_extras=True,export_animations=False,export_skins=False,export_tangents=False,
        export_all_vertex_colors=False)

def native(name,path,target):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str((ROOT/path).resolve()))
    obs=list(bpy.context.scene.objects);dg=bpy.context.evaluated_depsgraph_get()
    rt=bpy.data.objects.new(name,None);bpy.context.scene.collection.objects.link(rt);parts=[]
    for ob in obs:
        if ob.type!='MESH':continue
        me=bpy.data.meshes.new_from_object(ob.evaluated_get(dg),depsgraph=dg,preserve_all_data_layers=True)
        me.transform(ob.matrix_world);copy=bpy.data.objects.new(name+'__'+ob.name,me);bpy.context.scene.collection.objects.link(copy);copy.parent=rt;parts.append(copy)
    for ob in obs:bpy.data.objects.remove(ob,do_unlink=True)
    total=sum(sum(len(p.vertices)-2 for p in ob.data.polygons) for ob in parts)
    assert total>0,('Empty native context selection',name,path)
    envelope=None
    if name in ('Ranch','Cape'):
        sys.path.insert(0,str(HERE));import house_context
        envelope=house_context.extract(parts)
        metadata=json.loads((ROOT/Path(path).with_suffix('.json')).read_text())
        for ob in parts:bpy.data.objects.remove(ob,do_unlink=True)
        parts=house_context.skins(rt,metadata,*envelope)
        parts.extend(house_context.fixtures(rt,metadata))
        # A distance house is one static mesh, not hundreds of one-quad objects.
        # Native UVs, materials and corner normals survive the join.
        bpy.ops.object.select_all(action='DESELECT')
        for ob in parts:ob.select_set(True)
        bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();parts=[bpy.context.object]
        parts[0].name=name+'__NativeEnvelope'
        for key in ('context_surface_kind','context_expected_local_normal'):
            if key in parts[0]:del parts[0][key]
        export(Path('build/context')/(name+'.glb'),[rt,*parts])
        return dict(source=path,source_triangles=total,context_triangles=sum(sum(len(p.vertices)-2 for p in ob.data.polygons) for ob in parts),target='native plan envelope',scope='Exact native roof/wall/opening plans and canonical tiles; simple distance casings, doors and porch supports. No generic triangle collapse.')
    for ob in parts:
        # Preserve alpha cards in trees. House silhouettes and vehicle wheels
        # keep their topology at this modest distance-preview reduction.
        alpha=any(m and (m.surface_render_method=='DITHERED') and any(n.type=='TEX_IMAGE' and n.image and n.image.channels==4 for n in m.node_tree.nodes) for m in ob.data.materials if m.use_nodes)
        if target and total>target and not (name.startswith('Tree') and alpha):
            # Delivered weather/atlas boundaries duplicate vertices. Collapse
            # on that triangle soup deletes isolated roof patches. Weld the
            # coincident geometry first; loop UV seams remain independent.
            import bmesh
            bm=bmesh.new();bm.from_mesh(ob.data)
            bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
            bm.normal_update();bm.to_mesh(ob.data);bm.free()
            mod=ob.modifiers.new('Freeway context simplification','DECIMATE');mod.ratio=target/total
            G.apply(ob)
            # Nearest-surface normal transfer can pick the opposite side of a
            # thin car panel. Recompute a coherent field on the local LOD.
            for f in ob.data.polygons:f.use_smooth=True
            ob.data.normals_split_custom_set([(0,0,0)]*len(ob.data.loops))
            ob.data.set_sharp_from_angle(angle=math.radians(42))
            mod=ob.modifiers.new('Coherent local surface normals','WEIGHTED_NORMAL');mod.keep_sharp=True
            G.apply(ob)
            normals=[n.vector.copy() for n in ob.data.corner_normals]
            for face in ob.data.polygons:
                for index in face.loop_indices:
                    if normals[index].dot(face.normal)<.5:normals[index]=face.normal.copy()
            ob.data.normals_split_custom_set(normals)
    # The family sources contain some zero-area bevel caps at pole hardware;
    # omit those in this local derivative, preserving every valid surface.
    import bmesh
    for ob in parts:
        bm=bmesh.new();bm.from_mesh(ob.data)
        bad=[f for f in bm.faces if f.calc_area()<1e-12]
        if bad:
            bmesh.ops.delete(bm,geom=bad,context='FACES');bm.to_mesh(ob.data)
        bm.free()
    if envelope:
        metadata=json.loads((ROOT/Path(path).with_suffix('.json')).read_text())
        parts.extend(house_context.skins(rt,metadata,*envelope))
    if name in ('Hatch','SUV','Crossover'):
        # The native normal bake targets the full mesh's tangent field. A
        # distant context LOD keeps BaseColor/ORM, using its coherent geometric
        # normals until a dedicated LOD normal bake is authorized.
        for material in {m for ob in parts for m in ob.data.materials if m and m.use_nodes}:
            for node in material.node_tree.nodes:
                if node.type=='BSDF_PRINCIPLED':
                    for link in list(node.inputs['Normal'].links):material.node_tree.links.remove(link)
    export(Path('build/context')/(name+'.glb'),[rt,*parts])
    return dict(source=path,source_triangles=total,context_triangles=sum(sum(len(p.vertices)-2 for p in ob.data.polygons) for ob in parts),target=target,scope='Local derivative for distant checkpoint context; original untouched')

def signal():
    sys.path.insert(0,str(ROOT/'signals/src'))
    import geometry as q,equipment,graphics,plan,surfaces
    folder=Path('build/context/signal-graphics');graphics.generate(folder)
    surfaces.ATLAS=None
    for name,c,r,met in [('zinc',(.25,.28,.28),.6,.9),('green',(.025,.065,.047),.7,.2),('black',(.009,.012,.012),.7,0),('bronze',(.065,.048,.03),.7,.3),('yellow',(.64,.37,.009),.65,0),('inside',(.004,.006,.007),.8,0),('steel',(.27,.29,.29),.45,.9),('white',(.69,.70,.66),.76,0),('concrete',(.32,.33,.30),.94,0),('cabinet',(.31,.34,.34),.55,.78),('rubber',(.008,.009,.008),.9,0),('border',(.72,.49,.008),.5,0)]:q.M[name]=q.mat('Form_'+name,c,r,met)
    for key,file in [('lit','lenses.png'),('off','lenses-off.png'),('names','names.png'),('r10','r10.png')]:
        q.M[key]=q.image_mat('Freeway_Signal_'+key,folder/file,emit=3 if key=='lit' else 0,alpha=key in ('lit','off'))
    for key in ('panel','record'):q.M[key]=q.mat('Form_'+key,(.1,.1,.1))
    rt=equipment.mast('NativeSignalMast',(0,0,0),0,plan.PLANS[201]);q.finalize_meshes()
    total=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in bpy.context.scene.objects if o.type=='MESH')
    for ob in list(bpy.context.scene.objects):
        if ob.type=='MESH' and not ob.get('signal_lens'):
            mod=ob.modifiers.new('Freeway terminal context LOD','DECIMATE');mod.ratio=3500/total;G.apply(ob)
        if ob.type=='MESH' and not ob.data.uv_layers:world_uv(ob,1.)
        if ob.type=='MESH':
            import bmesh
            bm=bmesh.new();bm.from_mesh(ob.data)
            bad=[f for f in bm.faces if f.calc_area()<1e-12]
            if bad:bmesh.ops.delete(bm,geom=bad,context='FACES');bm.to_mesh(ob.data)
            bm.free()
    export(Path('build/context/Signal.glb'),list(bpy.context.scene.objects))

def utility():
    sys.path.insert(0,str(ROOT/'utility/src'))
    import construction as c,plan,surfaces
    # Same source construction, explicit quick material palette; skip atlas UV
    # assignment in this checkpoint cache because no utility bake is requested.
    surfaces.material=lambda:None
    surfaces.uv_object=lambda ob,*args,**kwargs:world_uv(ob,2.)
    c.palette();s=plan.pole_spec(comm=True,seed=101)
    pole=c.pole('NativeUtility',s)
    for ob in pole.objects:
        G.apply(ob);world_uv(ob,2.)
    export(Path('build/context/Utility.glb'),[pole.root,*pole.root.children_recursive])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--kind',default='native');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if a.kind=='signal':signal();return
    if a.kind=='utility':utility();return
    rows={}
    for name,path,n in [
        ('Hatch','cars/export/AlderH120.glb',5500),('SUV','cars/export/AlderX220.glb',5500),
        ('Crossover','cars/export/AlderC150.glb',5500),
        ('HeroHatch','cars/export/AlderH120.glb',None),('HeroSUV','cars/export/AlderX220.glb',None),('HeroCrossover','cars/export/AlderC150.glb',None),
        ('Ranch','houses/export/HearthfieldRanch-11.gltf',5000),('Cape','houses/export/HearthfieldCape-31.gltf',5000),
        ('TreeOak','trees/export/PinOak.glb',3200),('TreeMaple','trees/export/RedMaple.glb',3200),
        ('Ground','ground/export/Ground.glb',None),('Gas','commercial/export/CommercialGas-101.gltf',None),
        ('Strip','commercial/export/CommercialStrip-201.gltf',None),
        ('StreetLight','street-light/export/StreetLight.glb',None)]:
        rows[name]=native(name,path,n)
    Path('build/context/report.json').write_text(json.dumps(rows,indent=2))
if __name__=='__main__':main()
