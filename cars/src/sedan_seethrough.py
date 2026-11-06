"""Direct-camera saturated-magenta tests of the actual delivery geometry.

All manufactured opaque faces emit black; actual cabin glazing emits white under the permitted glass
exception. Optical covers transmit into their real opaque cassettes. Sixteen
primary samples resolve subpixel edge coverage without single-ray speckles. The independent, uncut die defines
body coverage. The companion review fills only enclosed silhouette holes and
excludes antialiasing at the true exterior contour. Raw images are retained.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import gpu
from sedan_views import SHOTS
VIEWS=['front','side','rear','top','front_three_quarter','rear_three_quarter']


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    p.add_argument('--width',type=int,default=1600)
    p.add_argument('--envelope',required=True,help='Uncut manufactured body, with actual wheel arches')
    p.add_argument('--parts-source',help='Finalized source supplies names only; every test triangle comes from the GLB')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    source=Path(a.source).resolve();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if source.suffix=='.glb':
        if not a.parts_source:raise ValueError('GLB tests need --parts-source for cabin-only glass attribution')
        from sedan_surface_proof import delivery_parts
        _,correspondence=delivery_parts(Path(a.parts_source).resolve(),source)
    else:bpy.ops.wm.open_mainfile(filepath=str(source))
    sc=bpy.context.scene
    def material(name,color=None):
        mat=bpy.data.materials.new(name);mat.use_nodes=True;nodes=mat.node_tree.nodes;nodes.clear()
        shader=nodes.new('ShaderNodeEmission' if color is not None else 'ShaderNodeBsdfTransparent')
        if color is not None:shader.inputs['Color'].default_value=(*color,1)
        output=nodes.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(shader.outputs[0],output.inputs['Surface'])
        return mat
    black=material('Opaque direct-ray blocker',(0,0,0));white=material('Cabin glazing exception',(1,1,1));clear=material('Optical cover transmission')
    actual=[ob for ob in sc.objects if ob.type=='MESH']
    for ob in actual:
        cabin=ob.name in ['Windshield','Backlight'] or ob.name.startswith(('Front side glass','Rear side glass','Quarter glass'))
        optical=ob.name.startswith(('Headlamp opening','Taillamp opening','S240 low optic '))
        ob.data.materials.clear();ob.data.materials.append(white if cabin else clear if optical else black)
        for face in ob.data.polygons:face.material_index=0
    envelope_path=Path(a.envelope).resolve()
    with bpy.data.libraries.load(str(envelope_path),link=False) as (data,target):target.objects=data.objects
    envelopes=[]
    for ob in target.objects:
        if ob is None:continue
        sc.collection.objects.link(ob);ob.hide_render=True;envelopes.append(ob)
        ob.data.materials.clear();ob.data.materials.append(white)
        for face in ob.data.polygons:face.material_index=0
    world=bpy.data.worlds.new('Saturated magenta direct background');world.use_nodes=True;sc.world=world
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,0,1,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
    camera=bpy.data.objects.new('Leak camera',bpy.data.cameras.new('Leak camera'));sc.collection.objects.link(camera);sc.camera=camera
    sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=16;sc.cycles.use_denoising=False;sc.cycles.use_adaptive_sampling=False
    sc.cycles.max_bounces=0;sc.cycles.transparent_max_bounces=32;sc.render.film_transparent=False
    sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;sc.view_settings.gamma=1
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGB';sc.render.resolution_percentage=100
    metadata={}
    for name in VIEWS:
        shot=SHOTS[name];camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler()
        camera.data.sensor_fit='HORIZONTAL';camera.data.sensor_width=36;camera.data.lens=shot.get('lens',58)
        camera.data.type='ORTHO' if 'ortho' in shot else 'PERSP';camera.data.ortho_scale=shot.get('ortho',5.7)
        sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/shot.get('aspect',1.65))
        sc.render.filepath=str((out/(name+'.png')).resolve());bpy.context.view_layer.update();bpy.ops.render.render(write_still=True)
        for ob in actual:ob.hide_render=True
        for ob in envelopes:ob.hide_render=False
        sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
        sc.render.filepath=str((out/(name+'-envelope.png')).resolve());bpy.ops.render.render(write_still=True)
        for ob in actual:ob.hide_render=False
        for ob in envelopes:ob.hide_render=True
        sc.render.film_transparent=False;sc.render.image_settings.color_mode='RGB'
        metadata[name]=dict(shot,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),width=a.width,height=sc.render.resolution_y,
            envelope_sha256=hashlib.sha256(envelope_path.read_bytes()).hexdigest(),samples=sc.cycles.samples,
            mask='Uncut manufactured body before shut lines and wells, with physical wheel-arch cutouts; actual appendages preserve exterior negative space',
            glass='Actual cabin panes are excepted; optical covers transmit into their real opaque cassettes; adjacent gaps remain tested')
        if source.suffix=='.glb':metadata[name]['glb_triangle_correspondence']=correspondence
    (out/'shots.json').write_text(json.dumps(metadata,indent=2))


def write_envelope(source,path,lower_mold=None):
    """Independent continuous body silhouette BEFORE any shut lines or wells.

    Actual wheel arches are cut out. Thus genuine exterior negative spaces
    (wheel spokes and the air around mirror stalks) are outside this envelope;
    real body gaps remain inside it. No image-based hole classification is used.
    The exported car itself always supplies the magenta test's occluding mesh.
    """
    from sedan_body import trim_arch
    import sedan_spec as S
    ob=source.copy();ob.data=source.data.copy();bpy.context.collection.objects.link(ob);ob.name='Continuous manufactured silhouette envelope'
    if lower_mold is not None:lower_mold.apply([ob])
    for axle in [S.FRONT_AXLE,S.REAR_AXLE]:trim_arch(ob,axle,64)
    path=Path(path).resolve();path.parent.mkdir(parents=True,exist_ok=True)
    bpy.data.libraries.write(str(path),{ob},fake_user=True)
    bpy.data.objects.remove(ob,do_unlink=True)

if __name__=='__main__':main()
