"""Kit atlas + detachable export, preserving the accepted shared belt meshes.

The kit's static consolidator would join all bone-parented instances into the
skin. This asset keeps those two repeated meshes intact, joining only rigid
skinned parts through kit.weapon. Materials, GLB serialization and lossless
subsets use the same kit functions as the other guns.
"""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import export,weapon as W,detachable_textures as D
from kit.gltf import GLB

def atlas(folder):
    mat=export.atlas_material('Harrow56',folder);nt=mat.node_tree;surface=nt.nodes['SURFACE']
    tex=surface.inputs['Base Color'].links[0].from_node
    scale=nt.nodes.new('ShaderNodeMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=.5
    nt.links.new(tex.outputs['Alpha'],scale.inputs[0]);nt.links.new(scale.outputs[0],surface.inputs['Specular IOR Level'])
    return mat
def prepare_uv(ob,mat):
    ob.data.materials.clear();ob.data.materials.append(mat)
    for f in ob.data.polygons:f.material_index=0
    for layer in list(ob.data.uv_layers):
        if layer.name!='BakeUV':ob.data.uv_layers.remove(layer)
    if ob.data.uv_layers.get('BakeUV'):ob.data.uv_layers['BakeUV'].name='UVMap'
    for attr in list(ob.data.color_attributes):ob.data.color_attributes.remove(attr)
def main():
    p=argparse.ArgumentParser();p.add_argument('--textures',default='textures');p.add_argument('--out',default='export')
    p.add_argument('--detachables',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    out=BASE/a.out;out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
    arm=bpy.data.objects['HarrowArmature'];W.pose(arm,None,0);mat=atlas((BASE/a.textures).resolve())
    parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent==arm]
    seen=set()
    for ob in [o for o in bpy.context.scene.objects if o.type=='MESH']:
        if ob.data.as_pointer() not in seen:seen.add(ob.data.as_pointer());prepare_uv(ob,mat)
    records={}
    if a.detachables:
        for state,clip in [('loaded','Idle'),('empty','IdleEmpty')]:
            W.pose(arm,clip,0)
            members=[o for o in parts if o.get('bone') in ('Magazine','BoxLid') or (state=='loaded' and o.get('bone') in ('BeltLink15','BeltRound15','BeltRound16'))]
            ob=W.detachable(members,arm,'Magazine','Box')
            ob.data.uv_layers.active.name='BakeUV'
            name='box_'+state
            layout=D.extract([ob],(BASE/a.textures).resolve(),'Harrow56',BASE/'build/delivery/detachables'/name,1024,layer='BakeUV',clusters=True)
            ob.data.uv_layers.active.name='UVMap';W.export(out/(name+'.glb'),[ob],animations=False)
            records[name]=dict(size=1024,layout=layout,bytes=(out/(name+'.glb')).stat().st_size)
            bpy.data.objects.remove(ob,do_unlink=True)
        W.pose(arm,None,0)
        for name,offset in [('cartridge',.4),('case',.5),('link',.6)]:
            original=bpy.data.objects[name.title()+'_Proof'];ob=original.copy();ob.data=original.data.copy();bpy.context.scene.collection.objects.link(ob)
            ob.data.transform(ob.matrix_world);ob.parent=None;ob.matrix_world=Matrix.Identity(4);ob.data.transform(Matrix.Translation((-offset,0,0)))
            ob.data.uv_layers.active.name='BakeUV'
            layout=D.extract([ob],(BASE/a.textures).resolve(),'Harrow56',BASE/'build/delivery/detachables'/name,512,layer='BakeUV',clusters=True)
            ob.data.uv_layers.active.name='UVMap';W.export(out/(name+'.glb'),[ob],animations=False)
            records[name]=dict(size=512,layout=layout,bytes=(out/(name+'.glb')).stat().st_size)
            bpy.data.objects.remove(ob,do_unlink=True)
    skin=[o for o in parts if o.parent_type!='BONE'];belt=[o for o in parts if o.parent_type=='BONE']
    joined=W.joined_copy(skin,'Harrow56')
    modifier=joined.modifiers.new('Rigid skin','ARMATURE');modifier.object=arm
    sockets=[o for o in bpy.context.scene.objects if o.name.startswith('Socket_')]
    W.pose(arm,'Idle',0);path=out/'lmg.glb';W.export(path,[arm,joined,*belt,*sockets])
    g=GLB(path);records['lmg']=dict(bytes=path.stat().st_size,materials=len(g.json['materials']),images=len(g.json['images']),
        evaluated_triangles=sum(len(g.accessor(p['indices']))//3 for n in g.json['nodes'] if 'mesh' in n for p in g.json['meshes'][n['mesh']]['primitives']),
        unique_mesh_triangles=sum(len(g.accessor(p['indices']))//3 for m in g.json['meshes'] for p in m['primitives']))
    (out/'delivery.json').write_text(json.dumps(records,indent=2));print('DELIVERED',records['lmg'],flush=True)
if __name__=='__main__':main()
