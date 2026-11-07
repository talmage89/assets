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
    theta=np.arcsin((.755-S.HUB)/rr)
    # Match the independent windshield rake. A flat 2.71m-high front slab
    # falsely includes open space between the raked screen and mirror brackets.
    back=[(6.006,2.71),(6.006,.755)]+[(cy+rr*np.cos(theta+(np.pi-2*theta)*k/32),S.HUB+rr*np.sin(theta+(np.pi-2*theta)*k/32)) for k in range(33)]+[(-3.92,.755),(-3.92,1.88)]
    def front(x,v,z=None):
        ax=abs(x)
        if ax<=1.138:y=-3.998+.273*v+.035*(ax/1.138)**2
        elif ax<=1.157:y=-3.963+.273*v+.010*(ax-1.138)/.019
        else:
            u=min(1,(ax-1.157)/.054);y=(-3.953+.273*v)*(1-u)-3.75*u
        if ax>=1.1375:
            z=1.9+.772*v if z is None else z;dx=min(ax-1.1375,1.223-ax);dz=min(z-1.887,2.717-z)
            chamfer=max(0,.016-dx,.016-dz,.032-dx-dz)
            y=min(y,-3.85+chamfer)
        return y
    stations=[0,.55,1.1,1.1374,1.1375,1.138,1.157,1.17,1.18,1.19,1.20,1.211,S.WIDTH/2]
    rings=[]
    for x in sorted(set(stations+[-v for v in stations])):
        contour=[(front(x,1,z=2.71),2.71)]+back+[(front(x,v),1.9+.772*v) for v in np.linspace(0,1,65)]
        rings.append([(x,y,z) for y,z in contour])
    die=G.loft('Uncut body envelope',rings,white)
    # The skirt is a wall below the actual cabin floor, not a filled block.
    # Wheel-arch rays may legitimately pass beneath that floor to open space.
    cavity=G.box('Uncut underfloor negative space',(0,1.043,-.433),(2.392,9.882,3.134),None,0)
    G.boolean(die,cavity)
    G.loft('Uncut roof envelope',[roof_section(y,d) for y,d in [(-3.92,.20),(-3.78,.085),(-3.56,.015),(-3.38,0),(5.60,0),(5.80,.025),(5.96,.075),(6.006,.115)]],white)
    hood=[]
    for y,w,top,bottom in [(-5.916,.725,1.520,1.060),(-5.87,.755,1.565,1.035),(-5.55,.780,1.642,1.015),(-4.95,.800,1.765,1.045),(-4.38,.825,1.860,1.145),(-3.96,.858,1.888,1.240)]:
        sec=[(-w,bottom),(-w,top-.145),(-w*.98,top-.078),(-w*.91,top-.026),(-w*.76,top),(-w*.42,top+.017),(0,top+.025),(w*.42,top+.017),(w*.76,top),(w*.91,top-.026),(w*.98,top-.078),(w,top-.145),(w,bottom)]
        hood.append([(x,y,z) for x,z in sec])
    G.loft('Uncut hood envelope',hood,white)
    # Keep the real open rear of each pressed C section. A filled bounding box
    # falsely classified wheel vent holes behind its swept corner as body leaks.
    for front,width,depth,z0,z1 in [(True,2.35,.204,.470,.790),(False,2.43,.180,.500,.800)]:
        end=S.FRONT if front else S.REAR;direction=1 if front else -1;g=.006;rings=[]
        for x,back in [(-width/2,.09),(-width/2+.12,.02),(-width/2+.20,0),(width/2-.20,0),(width/2-.12,.02),(width/2,.09)]:
            y=end+direction*back
            section=[(y,z0),(y,z1),(y+direction*depth,z1),(y+direction*depth,z1-g),(y+direction*g,z1-g),(y+direction*g,z0+g),(y+direction*depth,z0+g),(y+direction*depth,z0)]
            rings.append([(x,yy,zz) for yy,zz in section])
        G.apply(G.bevel(G.loft('Uncut pressed bumper envelope',rings,white),.0015,1))
    for sign in [-1,1]:G.box('Uncut optical molding',(sign*.948,-5.688,1.052),(.400,.185,.365),white,.070,3)
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
        scope='Body, roof, hood, bumpers and optical molding. Cabin glass emits white; sealed headlamp covers transmit to their actual opaque inserts. Exterior gaps around mirrors and wheel arches remain negative space.')
    (out/'counts.json').write_text(json.dumps(result,indent=2));print('BUS_SEETHROUGH',result,flush=True)
    if not result['passed']:raise SystemExit(1)
if __name__=='__main__':main()
