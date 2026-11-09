"""Native H-54 game mesh on shared civic finishes, written only locally."""
import importlib.util,sys
from pathlib import Path
import bpy,bmesh
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from geo import ROOT,Assembly
from kit.tiling import export


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    spec=importlib.util.spec_from_file_location('_civic_native_hydrant',ROOT/'fire-hydrant/src/build.py')
    native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
    b=native.Hydrant(False,.65);b.body();b.caps();b.chains();a=Assembly('HydrantSharedFinish')
    ma=a.materials[4];dg=bpy.context.evaluated_depsgraph_get()
    for ob in list(b.root.children_recursive):
        if ob.type!='MESH':continue
        old=ob.data.materials[0].name.lower() if ob.data.materials else ''
        c=(.23,.006,.004) if 'red' in old else (.69,.67,.57) if 'bonnet' in old else (.25,.27,.25) if 'zinc' in old else (.24,.17,.075) if 'bronze' in old else (.011,.014,.012)
        strip=2 if 'zinc' in old or 'bronze' in old else 5
        ob.data=bpy.data.meshes.new_from_object(ob.evaluated_get(dg),depsgraph=dg,preserve_all_data_layers=True);ob.modifiers.clear()
        ob.data.materials.clear();ob.data.materials.append(ma)
        attr=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER');ob.data.color_attributes.active_color=attr
        uv=ob.data.uv_layers.new(name='UVMap')
        for f in ob.data.polygons:
            f.material_index=0;axis=max(range(3),key=lambda k:abs(f.normal[k]));axes=[(1,2),(0,2),(0,1)][axis];aa,bb=axes
            low=min(ob.data.vertices[i].co[bb] for i in f.vertices);high=max(ob.data.vertices[i].co[bb] for i in f.vertices)
            for li in f.loop_indices:
                q=ob.data.vertices[ob.data.loops[li].vertex_index].co
                uv.data[li].uv=(q[aa]/4,strip/8+.004+(q[bb]-low)/max(high-low,1e-8)*.117)
                attr.data[li].color=(*c,1)
        bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    bpy.data.objects.remove(a.root,do_unlink=True)
    export(Path('build/context/hydrant.glb'),[b.root]+list(b.root.children_recursive))


if __name__=='__main__':main()
