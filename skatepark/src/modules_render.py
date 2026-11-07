"""Baked external-module sheet, including assembled bowl sector sets."""
import sys,math,json
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from render import setup
from external import bundle

def main():
    source=Path('export/final/SkateparkPieces.gltf');bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
    roots=[o for o in bpy.context.scene.objects if not o.parent];singles=[r for r in roots if 'Bowl_' not in r.name]
    for i,rt in enumerate(singles):rt.location=(i%5*9.2,i//5*8.5,0)
    for rt in roots:
        if rt.name.startswith('Bowl_'):rt.location=(9,42,0)
        elif rt.name.startswith('SteelBowl_'):rt.location=(31,42,0)
    bpy.context.view_layer.update()
    groups=[([rt],rt.name.replace('_',' ')) for rt in singles]
    groups += [([r for r in roots if r.name.startswith(prefix)],label) for prefix,label in
               [('Bowl_','Kidney / 20 sectors'),('SteelBowl_','Clover / 20 sectors')]]
    bounds=[]
    for members,label in groups:
        points=[ob.matrix_world@Vector(v) for rt in members for ob in rt.children_recursive if ob.type=='MESH' for v in ob.bound_box]
        bounds.append((points,label))
    points=[p for group,_ in bounds for p in group]
    center=Vector(tuple((min(p[k] for p in points)+max(p[k] for p in points))/2 for k in range(3)))
    cam=setup(40);cam.location=center+Vector((0,-75,105));cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO'
    rotate=cam.rotation_euler.to_matrix();local=[rotate.inverted()@(p-center) for p in points]
    extent=[(min(p[k] for p in local),max(p[k] for p in local)) for k in (0,1)]
    center+=rotate@Vector(((extent[0][0]+extent[0][1])/2,(extent[1][0]+extent[1][1])/2,0))
    cam.location=center+Vector((0,-75,105));cam.data.ortho_scale=max(extent[0][1]-extent[0][0],(extent[1][1]-extent[1][0])*1600/1420)*1.15
    sc=bpy.context.scene;sc.view_settings.exposure=-.25;sc.render.resolution_x=1600;sc.render.resolution_y=1420;sc.render.resolution_percentage=100
    # Camera-only charcoal background; illumination still uses the scripted sky.
    nt=sc.world.node_tree;output=next(n for n in nt.nodes if n.type=='OUTPUT_WORLD');sky=output.inputs[0].links[0].from_socket
    bg=nt.nodes.new('ShaderNodeBackground');bg.inputs['Color'].default_value=(.025,.031,.028,1)
    ray=nt.nodes.new('ShaderNodeLightPath');mix=nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(ray.outputs['Is Camera Ray'],mix.inputs[0]);nt.links.new(sky,mix.inputs[1]);nt.links.new(bg.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],output.inputs[0])
    out=Path('renders/final/modules.png');out.parent.mkdir(parents=True,exist_ok=True);sc.render.filepath=str(out.resolve());bpy.ops.render.render(write_still=True)
    from bpy_extras.object_utils import world_to_camera_view
    from PIL import Image,ImageDraw,ImageFont
    from kit.fonts import find_font
    im=Image.open(out).convert('RGB');draw=ImageDraw.Draw(im);font=ImageFont.truetype(find_font('DejaVu Sans','Book'),16)
    bpy.context.view_layer.update()
    for group,label in bounds:
        projected=[world_to_camera_view(sc,cam,p) for p in group]
        x=(min(p.x for p in projected)+max(p.x for p in projected))*.5*im.width
        y=(1-min(p.y for p in projected))*im.height+9
        draw.text((x,y),label,font=font,anchor='mt',fill=(218,225,219))
    draw.text((30,22),'58 reusable roots / common physical scale / bowls assembled from 20 sectors each',font=font,fill=(230,235,230))
    im.save(out)
    out.with_suffix('.json').write_text(json.dumps(dict(source=str(source),bundle_sha256=bundle(source),roots=len(roots),engine='CYCLES',scope='Fresh imported external modules; layout offsets and orthographic common scale for inspection only; post-render labels'),indent=2))
if __name__=='__main__':main()
