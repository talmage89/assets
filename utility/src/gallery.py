"""Cycles gallery turnarounds of the delivered family, with provenance.

Cropped top/communication/bracket studies keep the imported triangles and
use the studio floor to hide the shaft below the documented cut height.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from kit import studio,gpu
from deliver import bundle

from gallery_views import ITEMS


def render(name,row,a):
    stem,rootname,floor,top=row;bpy.ops.wm.read_factory_settings(use_empty=True)
    path=Path('export')/(stem+'.gltf');digest=bundle(path)
    bpy.ops.import_scene.gltf(filepath=str(path.resolve()));root=bpy.data.objects[rootname]
    selected={root,*root.children_recursive}
    if name=='deadend-guy':
        guy=bpy.data.objects['Guy_0']
        selected|={guy,*guy.children_recursive}
    for o in list(bpy.context.scene.objects):
        if o not in selected:bpy.data.objects.remove(o,do_unlink=True)
    origin=root.matrix_world.translation.copy()
    for o in selected:
        if o.parent is None:o.matrix_world=Matrix.Translation(-origin)@o.matrix_world
    bpy.context.view_layer.update()
    # Sectional inspection copies omit triangles outside the named height
    # window. Uncut imported vertices/UVs/normals remain the evidence; the
    # delivery is unchanged. This makes the splice visible in its top view.
    for o in selected:
        if o.type!='MESH':continue
        source=o.data;uv=source.uv_layers.active;vs=[];faces=[];normals=[];coords=[];materials=[]
        for face in source.polygons:
            if any(not floor-.02<=(o.matrix_world@source.vertices[i].co).z<=top for i in face.vertices):continue
            k=len(vs);vs.extend(source.vertices[i].co.copy() for i in face.vertices);faces.append(tuple(range(k,len(vs))))
            normals.extend(source.corner_normals[li].vector[:] for li in face.loop_indices);coords.extend(uv.data[li].uv[:] for li in face.loop_indices);materials.append(face.material_index)
        me=bpy.data.meshes.new('Gallery selection of exported triangles');me.from_pydata(vs,[],faces);me.update()
        for m in source.materials:me.materials.append(m)
        dst=me.uv_layers.new(name='UVMap')
        for d,v in zip(dst.data,coords):d.uv=v
        for f,i in zip(me.polygons,materials):f.material_index=i;f.use_smooth=True
        me.normals_split_custom_set(normals);o.data=me
    # Independent imported coordinates set studio/camera framing.
    pts=[o.matrix_world@v.co for o in selected if o.type=='MESH' for v in o.data.vertices if floor-.02<=(o.matrix_world@v.co).z<=top]
    lo=Vector(tuple(min(p[k] for p in pts) for k in range(3)));hi=Vector(tuple(max(p[k] for p in pts) for k in range(3)))
    target=(lo+hi)/2;scale=max(1,(hi-lo).length/2)
    cam=studio.add_studio(scale=scale,light_center=tuple(target),backdrop_half_width=18,backdrop_height=30,backdrop_color=(.24,.255,.26))
    # Translate only seamless to section-floor level; lights already surround
    # the actual measured mesh centre. No shipped triangle is edited.
    seamless=bpy.data.objects['Studio seamless'];material=seamless.data.materials[0];bpy.data.objects.remove(seamless,do_unlink=True)
    from kit import model as G
    G.box('Gallery continuous floor',(0,0,floor-.012),(1000,1000,.02),material,0)
    if name=='scale':
        people=studio.human()
        for o in people:o.location.x+=2.15
    sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=True
    sc.render.threads_mode='FIXED';sc.render.threads=4;sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-1.2
    sc.render.resolution_x=a.width;sc.render.resolution_y=a.width;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG'
    cam.data.type='ORTHO';cam.data.clip_end=1000;cam.data.ortho_scale=max(hi.z-lo.z,hi.x-lo.x,hi.y-lo.y)*1.22
    out=Path('renders/gallery');out.mkdir(parents=True,exist_ok=True);reports={}
    views=dict(front=(0,-1,.12)) if name=='scale' else dict(front=(0,-1,.12),side=(1,0,.12),back=(0,1,.12),top=(.01,0,1))
    for view,direction in views.items():
        cam.location=target+Vector(direction).normalized()*30;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();sc.camera=cam
        sc.render.filepath=str((out/f'{name}-{view}.png').resolve());result=bpy.ops.render.render(write_still=True);assert 'FINISHED' in result
        recipe=hashlib.sha256((HERE/'gallery.py').read_bytes()+(HERE/'gallery_views.py').read_bytes()).hexdigest()
        reports[view]=dict(source=str(path),sha256=digest,recipe_sha256=recipe,root=rootname,section_floor_m=floor,observed_bounds_m=[list(lo),list(hi)],camera=list(cam.location),engine='Cycles GPU')
    assert bundle(path)==digest
    (out/(name+'.json')).write_text(json.dumps(reports,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=800);p.add_argument('--samples',type=int,default=48);p.add_argument('--items');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    for name in a.items.split(',') if a.items else ITEMS:render(name,ITEMS[name],a)
