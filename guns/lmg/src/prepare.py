"""Kit UV finalization of the accepted mesh, once per shared belt template.

The paired box variants reuse the gun's bin charts. The three higher-resolution
loose ammunition meshes get small reserved regions, so subsets never resample.
"""
import json,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Matrix
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import finalize,weapon as W,model as M
import geometry as G

def recover(ob):
    """Recover authored material roles from lossless inspection vertex data."""
    colors=ob.data.color_attributes.active_color
    assert colors,ob.name
    keys=list(G.MAT)
    assignments=[]
    for face in ob.data.polygons:
        row=colors.data[face.loop_indices[0]].color
        assignments.append(min(range(len(keys)),key=lambda i:sum((row[j]-G.MAT[keys[i]].diffuse_color[j])**2 for j in range(3))))
    used=sorted(set(assignments));ob.data.materials.clear()
    for i in used:ob.data.materials.append(G.MAT[keys[i]])
    for f,k in zip(ob.data.polygons,assignments):f.material_index=used.index(k)
    for attr in list(ob.data.color_attributes):ob.data.color_attributes.remove(attr)

def main():
    out=BASE/'build/delivery';out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/lmg.blend'))
    arm=bpy.data.objects['HarrowArmature'];W.pose(arm,None,0)
    G.palette()
    for ob in list(bpy.context.scene.objects):
        if ob.get('bake_only'):bpy.data.objects.remove(ob,do_unlink=True)
    seen=set()
    for ob in [o for o in bpy.context.scene.objects if o.type=='MESH']:
        if ob.data.as_pointer() in seen:continue
        seen.add(ob.data.as_pointer());recover(ob)
        for layer in list(ob.data.uv_layers):ob.data.uv_layers.remove(layer)
        if ob.name=='FeedCover_Shell':
            normals=ob.data.attributes.new('Saved delivery normals','FLOAT_VECTOR','CORNER')
            for row,n in zip(normals.data,ob.data.corner_normals):row.vector=n.vector
            before=len(ob.data.polygons)
            bm=bmesh.new();bm.from_mesh(ob.data)
            # Only the common shortest edge of the two collapsed slivers.
            # An all-edge cleanup also simplified sound bevel triangles.
            small=[f for f in bm.faces if f.calc_area()<1e-12]
            edges={min(f.edges,key=lambda e:e.calc_length()) for f in small}
            bmesh.ops.dissolve_degenerate(bm,edges=list(edges),dist=.000002)
            bm.to_mesh(ob.data);bm.free()
            ob.data.normals_split_custom_set([r.vector[:] for r in ob.data.attributes['Saved delivery normals'].data])
            ob.data.attributes.remove(ob.data.attributes['Saved delivery normals'])
            print('DELIVERY SLIVER CLEANUP',ob.name,before,'->',len(ob.data.polygons),flush=True)
    for name,offset in [('cartridge',.4),('case',.5),('link',.6)]:
        before=set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=str(BASE/'build'/(name+'.glb')))
        ob=next(o for o in bpy.data.objects if o not in before and o.type=='MESH')
        ob.name=name.title()+'_Proof';ob['asset_set']='LMG'
        if 'bone' in ob:del ob['bone']
        recover(ob)
        ob.data.transform(ob.matrix_world);ob.matrix_world=Matrix.Identity(4)
        ob.data.transform(Matrix.Translation((offset,0,0)))
        pivot=M.pivot(name.title()+'Root',(offset,0,0));pivot['static_root']=True
        pivot['delivery_variant']=name;pivot['atlas_staging_offset']=(offset,0,0)
        M.attach(ob,pivot,asset_set='LMG')
    unpacked=out/'unpacked.blend';bpy.ops.wm.save_as_mainfile(filepath=str(unpacked))
    # Loose case and cartridge can share the gun's reusable belt UVs only if
    # their geometry is identical. They are independently authored resolutions,
    # so reserve separate charts, including a real square for the steel link.
    regions=dict(gun=(.01,.01,.74,.99),cartridge=(.755,.01,.855,.23),
                 case=(.86,.01,.96,.23),link=(.755,.235,.99,.36),
                 box=(.76,.38,.99,.99))
    def group(o):
        if o.name.endswith('_Proof'):return o.name.split('_')[0].lower()
        return 'box' if o.get('bone') in ('Magazine','BoxLid') else 'gun'
    master=[]
    for key,rect in regions.items():
        bpy.ops.wm.open_mainfile(filepath=str(unpacked))
        for ob in list(bpy.context.scene.objects):
            if ob.type!='MESH':continue
            duplicate=ob.name.startswith(('Belt_Round_','Belt_Link_')) and not ob.name.endswith('_00')
            if group(ob)!=key or duplicate:bpy.data.objects.remove(ob,do_unlink=True)
        src=out/(key+'-source.blend');bpy.ops.wm.save_as_mainfile(filepath=str(src))
        cfg=out/(key+'-uv.py')
        cfg.write_text('UV_ATLAS_RECT='+repr(rect)+'\nUV_MIN_COVERAGE=.0001\nUV_PACK_SHAPE="AABB"\nUV_SMART_ASPECT=False\nUV_SMART_ANGLE=30\nUV_PRIORITY={"Receiver_Sheet":1.25,"FeedCover_Shell":1.3,"RearSight":1.3,"Stock_Sculpt":.9,"Belt_":1.2}\n')
        dst=out/(key+'-uv.blend')
        sys.argv=['blender','--','--source',str(src),'--config',str(cfg),'--out',str(dst),'--report',str(out/(key+'-uv.json')),'--size','2048','--target-density','100000','--margin','.0015']
        try:finalize.main()
        except RuntimeError:
            from kit.uv import signed_area
            for ob in [o for o in bpy.context.scene.objects if o.type=='MESH']:
                for tri in ob.data.loop_triangles:
                    area=abs(signed_area([ob.data.uv_layers.active.data[i].uv for i in tri.loops]))
                    if area<1e-12:print('TINY_UV',ob.name,tri.polygon_index,area,tri.area,flush=True)
            raise
        master.append((dst,[(o.name,o.data.name) for o in bpy.context.scene.objects if o.type=='MESH']))
    bpy.ops.wm.open_mainfile(filepath=str(unpacked))
    for path,mapping in master:
        with bpy.data.libraries.load(str(path),link=False) as (src,dst):dst.meshes=[m for n,m in mapping]
        for (name,_),mesh in zip(mapping,dst.meshes):bpy.data.objects[name].data=mesh
    for kind in ('Round','Link'):
        template=bpy.data.objects[f'Belt_{kind}_00']
        for ob in bpy.context.scene.objects:
            if ob.name.startswith(f'Belt_{kind}_'):ob.data=template.data
    bpy.context.scene['stage']='Accepted form with kit atlas; intentional shared belt UVs'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'finalized.blend'))
    # The baker sees one instance of each reused surface. No overlapping rays.
    for ob in list(bpy.context.scene.objects):
        if ob.type=='MESH' and ob.name.startswith(('Belt_Round_','Belt_Link_')) and not ob.name.endswith('_00'):
            bpy.data.objects.remove(ob,do_unlink=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'bake-target.blend'))
if __name__=='__main__':main()
