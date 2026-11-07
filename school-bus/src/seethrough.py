"""Car-family direct magenta test, independent uncut bus envelope and cabin exception."""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(HERE),str(ROOT),str(ROOT/'cars/src')]
from kit import gpu,model as G
from sedan_seethrough_review import filled_silhouette
from views import SHOTS
from build import roof_section
import spec as S
import numpy as np
from PIL import Image,ImageFilter

def emission(name,color=None):
    mat=bpy.data.materials.new(name);mat.use_nodes=True;nt=mat.node_tree;nt.nodes.clear()
    bs=nt.nodes.new('ShaderNodeBsdfTransparent' if color is None else 'ShaderNodeEmission')
    if color is not None:bs.inputs['Color'].default_value=(*color,1)
    out=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(bs.outputs[0],out.inputs[0]);return mat

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--parts',required=True);p.add_argument('--out',required=True);p.add_argument('--width',type=int,default=1200)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.parts).resolve()))
    def key(points):return tuple(sorted(tuple(round(v,5) for v in pt) for pt in points))
    optical=set()
    for ob in bpy.context.scene.objects:
        if not ob.name.startswith('Glass sealed headlamp'):continue
        ob.data.calc_loop_triangles()
        for t in ob.data.loop_triangles:optical.add(key([ob.matrix_world@ob.data.vertices[i].co for i in t.vertices]))
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path(a.source).resolve()))
    black=emission('Opaque direct blockers',(0,0,0));white=emission('Cabin glass exception',(1,1,1));clear=emission('Optical transmission')
    actual=[o for o in bpy.context.scene.objects if o.type=='MESH'];optic_faces=0
    for ob in actual:
        old=list(ob.data.materials);roles=[]
        for face in ob.data.polygons:
            glass='Glass' in old[face.material_index].name
            isopt=glass and key([ob.matrix_world@ob.data.vertices[i].co for i in face.vertices]) in optical
            roles.append(2 if isopt else 1 if glass else 0);optic_faces+=int(isopt)
        ob.data.materials.clear()
        for m in [black,white,clear]:ob.data.materials.append(m)
        for face,role in zip(ob.data.polygons,roles):face.material_index=role
    if optic_faces!=len(optical):raise ValueError(('Lost optical/cabin attribution',optic_faces,len(optical)))
    # Envelope is constructed before all body openings from independent package sections.
    before=set(bpy.context.scene.objects)
    rr=.630;cy=S.REAR_AXLE
    profile=[(-3.92,2.71),(6.006,2.71),(6.006,.755),(cy+rr,.755),(cy+rr,S.HUB)]
    profile += [(cy+rr*np.cos(np.pi*k/32),S.HUB+rr*np.sin(np.pi*k/32)) for k in range(33)]+[(cy-rr,.755),(-3.92,.755)]
    G.profile('Uncut body envelope',profile,-S.WIDTH/2,S.WIDTH/2,white,axis='X')
    G.loft('Uncut roof envelope',[roof_section(y,d) for y,d in [(-3.92,.20),(-3.78,.085),(-3.56,.015),(-3.38,0),(5.60,0),(5.80,.025),(5.96,.075),(6.006,.115)]],white)
    envelope=list(set(bpy.context.scene.objects)-before)
    for ob in envelope:ob.hide_render=True
    sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=16;sc.cycles.use_denoising=False;sc.cycles.use_adaptive_sampling=False;sc.cycles.max_bounces=0;sc.cycles.transparent_max_bounces=32
    sc.world=bpy.data.worlds.new('Direct magenta world');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs[0].default_value=(1,0,1,1)
    sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
    cam=bpy.data.objects.new('Leak camera',bpy.data.cameras.new('Leak camera'));sc.collection.objects.link(cam);sc.camera=cam;cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36
    results={}
    for name,shotname in [('front','front'),('side','side'),('rear','rear'),('top','top'),('front_three_quarter','hero'),('rear_three_quarter','rear_three_quarter')]:
        s=SHOTS[shotname];cam.location=s['location'];cam.rotation_euler=(Vector(s['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.rotation_euler.rotate_axis('Z',s.get('roll',0));cam.data.type='ORTHO' if 'ortho' in s else 'PERSP';cam.data.ortho_scale=s.get('ortho',14);cam.data.lens=s['lens']
        sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/s.get('aspect',1.78));sc.render.film_transparent=False;sc.render.filepath=str((out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        pixels=np.asarray(Image.open(out/(name+'.png')).convert('RGB'));magenta=(pixels[:,:,0]>200)&(pixels[:,:,1]<35)&(pixels[:,:,2]>200)
        # Actual coverage refines the independent die only at the exterior contour.
        silhouette=filled_silhouette(~magenta)
        for ob in actual:ob.hide_render=True
        for ob in envelope:ob.hide_render=False
        sc.render.film_transparent=True;sc.render.filepath=str((out/(name+'-envelope.png')).resolve());bpy.ops.render.render(write_still=True)
        mask=np.asarray(Image.open(out/(name+'-envelope.png')).getchannel('A').filter(ImageFilter.MinFilter(5)))>250;mask &= silhouette
        leak=mask&magenta;Image.fromarray(leak.astype('uint8')*255).save(out/(name+'-leaks.png'))
        results[name]=dict(tested_pixels=int(mask.sum()),magenta_pixels=int(leak.sum()))
        for ob in actual:ob.hide_render=False
        for ob in envelope:ob.hide_render=True
    result=dict(passed=all(r['magenta_pixels']==0 for r in results.values()),views=results,optical_faces_transmitting=optic_faces,
        method='Car family filled_silhouette and 2px contour guard intersect independent uncut bus body/roof die; actual imported delivery is the blocker',
        scope='Body and roof seams. Cabin glass emits white; sealed headlamp covers transmit to their actual opaque inserts. Nose outside the body die is assessed by mesh audits and crops.')
    (out/'counts.json').write_text(json.dumps(result,indent=2));print('BUS_SEETHROUGH',result,flush=True)
    if not result['passed']:raise SystemExit(1)
if __name__=='__main__':main()
