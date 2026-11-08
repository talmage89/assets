"""Procedural reflection stripes on source molds and delivered normal maps."""
import argparse,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from kit import gpu
from render import digest

def render(source,out,width=1200,samples=32,part=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if source.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(source.resolve()))
    else:bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
    sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable()
    sc.cycles.samples=samples;sc.cycles.use_denoising=True
    sc.world=bpy.data.worlds.new('Original reflection-line environment');sc.world.use_nodes=True
    nt=sc.world.node_tree;tc=nt.nodes.new('ShaderNodeTexCoord')
    sep=nt.nodes.new('ShaderNodeSeparateXYZ');nt.links.new(tc.outputs['Normal'],sep.inputs[0])
    mul=nt.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=40
    nt.links.new(sep.outputs['X'],mul.inputs[0])
    sine=nt.nodes.new('ShaderNodeMath');sine.operation='SINE';nt.links.new(mul.outputs[0],sine.inputs[0])
    step=nt.nodes.new('ShaderNodeMath');step.operation='GREATER_THAN';step.inputs[1].default_value=.25
    nt.links.new(sine.outputs[0],step.inputs[0]);nt.links.new(step.outputs[0],nt.nodes['Background'].inputs['Color'])
    nt.nodes['Background'].inputs['Strength'].default_value=1
    transparent=bpy.data.materials.new('Hidden diagnostic context');transparent.use_nodes=True
    tn=transparent.node_tree;tn.nodes.clear();tb=tn.nodes.new('ShaderNodeBsdfTransparent')
    tn.links.new(tb.outputs[0],tn.nodes.new('ShaderNodeOutputMaterial').inputs['Surface'])
    sc.cycles.transparent_max_bounces=32
    for ob in sc.objects:
        if ob.get('bake_only'):ob.hide_render=True
        if part and ob.type=='MESH':
            if source.suffix=='.blend':
                ob.hide_render=ob.name!=('Dense front mold' if part=='dense' else 'Compound hood shell')
            else:
                # Keep original delivered corner normals/UVs untouched. Other
                # faces become transparent, rather than re-meshing the GLTF.
                slot=len(ob.data.materials);ob.data.materials.append(transparent)
                for face in ob.data.polygons:
                    points=[ob.matrix_world@ob.data.vertices[i].co for i in face.vertices]
                    keep=('Paint' in ob.data.materials[face.material_index].name and
                          max(p.y for p in points)<-3.985 and min(p.z for p in points)>.80)
                    if not keep:face.material_index=slot
    # Keep the delivered normal binding, while suppressing albedo and wear's
    # roughness. This is a shape/normal diagnostic, never a product photograph.
    for mat in bpy.data.materials:
        if not mat.use_nodes:continue
        nt=mat.node_tree;bs=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if not bs:continue
        for name,value in [('Base Color',(.35,.35,.35,1)),('Metallic',1),('Roughness',.055),
                           ('Coat Weight',0),('Transmission Weight',0),('Emission Strength',0)]:
            for link in list(bs.inputs[name].links):nt.links.remove(link)
            bs.inputs[name].default_value=value
        nt.links.new(bs.outputs[0],next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL').inputs['Surface'])
    cam=bpy.data.objects.new('Reflection camera',bpy.data.cameras.new('Reflection camera'))
    sc.collection.objects.link(cam);sc.camera=cam;cam.data.lens=58;cam.data.clip_start=.02
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast'
    sc.render.resolution_percentage=100;sc.render.resolution_x=width;sc.render.resolution_y=round(width/1.5)
    sc.render.image_settings.file_format='PNG';out.mkdir(parents=True,exist_ok=True);rows={}
    for name,loc,target in [('three_quarter',(-3.6,-9.1,2.5),(0,-4.9,1.35)),
                            ('crown',(-2.5,-7.8,4.1),(0,-4.95,1.45))]:
        cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
        sc.render.filepath=str((out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        rows[name]=dict(source=str(source),sha256=digest(source),location=loc,target=target,
                        width=width,normal_map_retained=True,part=part,
                        isolation='Original exported Paint faces ahead of cowl and above 0.8m, unchanged normals/UVs' if part and source.suffix!='.blend' else None)
    (out/'provenance.json').write_text(json.dumps(rows,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--part',choices=['hood','dense'])
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);render(a.source,a.out,part=a.part)
