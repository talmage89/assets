"""Optional receiver photographic lighting diagnostic, never a game output.

Render each physical card independently in scene-linear EXR. The fit is a
starting point only; acceptance uses a fresh full-resolution Cycles image.
"""
import json
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
i = sys.argv.index('--member'); member = sys.argv[i+1]; del sys.argv[i:i+2]
BASE = ROOT / 'guns' / member
sys.path[:0] = [str(ROOT), str(BASE/'src')]
from guns.common.render import main
from guns.common.photo_matches import camera_shots
import final_shots as F
import interface

roughness_override=None
albedo_override=None
if '--paint-albedo' in sys.argv:
    i=sys.argv.index('--paint-albedo');albedo_override=float(sys.argv[i+1]);del sys.argv[i:i+2]
if '--paint-roughness' in sys.argv:
    i=sys.argv.index('--paint-roughness');roughness_override=float(sys.argv[i+1]);del sys.argv[i:i+2]
if roughness_override is not None or albedo_override is not None:
    original_configure=F.configure_scene
    def configure(scene,source):
        original_configure(scene,source)
        for mat in {m for ob in scene.objects if ob.type=='MESH' and not ob.get('studio') for m in ob.data.materials if m and m.use_nodes}:
            nt=mat.node_tree;bs=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
            if bs is None or not bs.inputs['Base Color'].links or not bs.inputs['Roughness'].links:continue
            image=bs.inputs['Base Color'].links[0].from_node
            if image.type!='TEX_IMAGE':continue
            old=bs.inputs['Roughness'].links[0].from_socket
            mask=nt.nodes.new('ShaderNodeMath');mask.operation='SUBTRACT';mask.inputs[1].default_value=.56;nt.links.new(image.outputs['Alpha'],mask.inputs[0])
            fraction=nt.nodes.new('ShaderNodeMath');fraction.operation='DIVIDE';fraction.inputs[1].default_value=.24;fraction.use_clamp=True;nt.links.new(mask.outputs[0],fraction.inputs[0])
            if roughness_override is not None:
                delta=nt.nodes.new('ShaderNodeMath');delta.operation='MULTIPLY';delta.inputs[1].default_value=roughness_override-(.42 if member=='ak' else .29);nt.links.new(fraction.outputs[0],delta.inputs[0])
                add=nt.nodes.new('ShaderNodeMath');add.operation='ADD';nt.links.new(old,add.inputs[0]);nt.links.new(delta.outputs[0],add.inputs[1]);nt.links.new(add.outputs[0],bs.inputs['Roughness'])
            if albedo_override is not None:
                delta=nt.nodes.new('ShaderNodeVectorMath');delta.operation='SCALE';delta.inputs[0].default_value=(albedo_override-.022,)*3;nt.links.new(fraction.outputs[0],delta.inputs['Scale'])
                add=nt.nodes.new('ShaderNodeVectorMath');add.operation='ADD';nt.links.new(image.outputs['Color'],add.inputs[0]);nt.links.new(delta.outputs[0],add.inputs[1]);nt.links.new(add.outputs[0],bs.inputs['Base Color'])
    F.configure_scene=configure
    F.RENDER_STAGE='REVIEW ONLY paint roughness override; never final acceptance'

i = sys.argv.index('--sets'); requested = sys.argv[i+1].split(','); del sys.argv[i:i+2]
broad_only='--broad-only' in sys.argv
if broad_only:sys.argv.remove('--broad-only')
nonpaint_studio='--nonpaint-studio' in sys.argv
if nonpaint_studio:sys.argv.remove('--nonpaint-studio')
assert not (broad_only and nonpaint_studio),'Choose one response basis'
sign = 1 if member == 'ak' else -1
BASES = [dict(world=True)]
for y in (-.5, .10, .7):
    for z in (-.30, .10, .65):
        BASES.append(dict(position=(sign*.65,y,z),size=(.65,.90)))
for x in (-sign*.65, 0):
    for z in (-.30,.65):
        BASES.append(dict(position=(x,.10,z),size=(.60,.80)))
for z in (.15,.28,.45):
    BASES.append(dict(position=(sign*.45,.10,z),size=(.70,.04)))
# Independent near cards resolve illumination across the complete gun. Every
# card lights all surfaces and the neutral backing; none is linked to a part.
for y,z in ((-.19,.04),(.28,.06),(.29,.107),(-.015,-.035),(.15,-.12),(.47,.085)):
    for dz in (-.10,.10):
        BASES.append(dict(position=(sign*.18,y,z+dz),size=(.10,.10),target=(0,y,z)))
if member == 'smg':
    # Narrow studio cards along the actual crown reflection directions.
    # Broad fill alone can match a histogram with the reflection on the
    # wrong flat; these fixtures resolve the photographed upper sheen.
    from guns.common.paint_review import geometry
    geo=geometry(BASE);index=list(geo['names']).index('Receiver_Shell')+1
    triangles=geo['xyz'][geo['ids']==index]
    view=np.asarray(camera_shots(BASE/'build/cameras.json')['left_photo']['location'])
    for y in (.04,.12):
        for z in (.112,.118,.124,.129):
            a,b,c=triangles.transpose(1,0,2)
            den=(b[:,2]-c[:,2])*(a[:,1]-c[:,1])+(c[:,1]-b[:,1])*(a[:,2]-c[:,2])
            valid=abs(den)>1e-12;safe=np.where(valid,den,1)
            wa=((b[:,2]-c[:,2])*(y-c[:,1])+(c[:,1]-b[:,1])*(z-c[:,2]))/safe
            wb=((c[:,2]-a[:,2])*(y-c[:,1])+(a[:,1]-c[:,1])*(z-c[:,2]))/safe;wc=1-wa-wb
            valid &= (wa>=0)&(wb>=0)&(wc>=0)
            if not valid.any():continue
            xx=wa*a[:,0]+wb*b[:,0]+wc*c[:,0];i=np.flatnonzero(valid)[np.argmin(xx[valid])]
            point=np.array((xx[i],y,z));normal=np.cross(b[i]-a[i],c[i]-a[i]);normal/=np.linalg.norm(normal)
            direction=view-point;direction/=np.linalg.norm(direction)
            reflected=2*normal*(normal@direction)-direction
            BASES.append(dict(position=(point+.35*reflected).tolist(),size=(.35,.025),target=point.tolist()))
original = F.prepare_shot

# Bare steel and oxide need cards in their actual reflection directions.
# Their geometry is independent of receiver paint; no photo value places a card.
from guns.common.paint_review import geometry
geo=geometry(BASE)
view=np.asarray(camera_shots(BASE/'build/cameras.json')[requested[0]]['location'])
NEAR=[]
NONPAINT_REFLECTIONS=[]
for part in ('Magazine_Body' if member=='smg' else 'Magazine_Sheet','Barrel'):
    if part=='Magazine_Body' and F.PHOTO_POSES[requested[0]].get('hide_detached_mag'):continue
    j=list(geo['names']).index(part)+1
    tri=geo['xyz'][geo['ids']==j]
    if part=='Barrel':
        station=tri.mean(1)[:,1];tri=tri[(station>.3765)&(station<.4001)] if member=='smg' else tri[(station>.455)&(station<.535)]
    normals=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);area=np.linalg.norm(normals,axis=1)
    normals/=np.maximum(area[:,None],1e-15);centers=tri.mean(1)
    direction=view-centers;direction/=np.linalg.norm(direction,axis=1)[:,None]
    visible=(normals*direction).sum(1)>.1
    candidates=np.flatnonzero(visible & (area>np.percentile(area,50)))
    chosen=[]
    for k in sorted(candidates,key=lambda k:-area[k]):
        reflected=2*normals[k]*(normals[k]@direction[k])-direction[k]
        if any(np.linalg.norm(reflected-r)<.25 for r in chosen):continue
        chosen.append(reflected)
        card=dict(position=(centers[k]+.35*reflected).tolist(),size=(.22,.45),target=centers[k].tolist())
        BASES.append(card);NONPAINT_REFLECTIONS.append(card)
        if part in ('Magazine_Body','Magazine_Sheet','Barrel'):
            NEAR.append(dict(position=(centers[k]+.06*reflected).tolist(),size=(.025,.12),target=centers[k].tolist()))
        if len(chosen)==10:break
BASES.extend(NEAR)
if member=='ak':
    for x,z in ((.04,.106),(.06,.16),(0,.23),(.08,.20)):
        BASES.append(dict(position=(x,.29,z),size=(.025,.12),target=(0,.29,.106)))
    for y,z in ((.55,-.08),(-.40,.20),(.60,.25)):
        BASES.append(dict(position=(-.02,y,z),size=(.12,.12),target=(-.15,y,z)))
    for x,y,z,tz in ((.04,-.205,.09,.070),(.02,-.205,.16,.070),(.045,.29,.09,.072),(.02,.29,.16,.072)):
        BASES.append(dict(position=(x,y,z),size=(.025,.12),target=(0,y,tz)))

if broad_only:
    # Overdetermined physical-studio test: world plus 16 broad cards. The
    # positions/sizes are fixed independently of all photographic statistics.
    BASES=BASES[:17]
elif nonpaint_studio:
    # Broad fixtures and .35 m reflection cards inferred ONLY from visible
    # nonpaint geometry; exclude all close lights and receiver-derived cards.
    BASES=BASES[:17]+NONPAINT_REFLECTIONS


def exr(scene, *_):
    scene.render.image_settings.file_format = 'OPEN_EXR'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '32'
    scene.render.filepath = str(Path(scene.render.filepath).with_suffix('.exr'))


def prepare(scene, shot):
    original(scene, shot)
    from guns.common.paint_review import photographic_backdrop
    spec=next(v for v in json.loads((BASE/'src/paint_review.json').read_text()).values() if v['shot']==shot['anchor_shot'])
    photographic_backdrop(scene,shot,spec.get('backdrop'))
    scene.cycles.use_denoising = False
    for ob in scene.objects:
        if ob.type == 'LIGHT':
            ob.data.energy = 0
    bg = scene.world.node_tree.nodes['Background']
    bg.inputs['Strength'].default_value = 0
    bg.inputs['Color'].default_value = (.25,.25,.25,1)
    key = 'Independent paint basis'
    if key not in scene.objects:
        data = bpy.data.lights.new(key,'AREA'); data.shape = 'RECTANGLE'
        ob = bpy.data.objects.new(key,data); scene.collection.objects.link(ob)
    scene.objects[key].data.energy=0
    b = BASES[shot['basis_index']]
    if b.get('world'):
        bg.inputs['Strength'].default_value = 1
    else:
        ob=scene.objects[key]; ob.hide_render=False; ob.data.energy=1;ob.data.color=(1,1,1)
        ob.location=b['position']; ob.data.size,ob.data.size_y=b['size']
        ob.rotation_euler=(Vector(b.get('target',(0,.10,.09)))-ob.location).to_track_quat('-Z','Y').to_euler()
    active=[o.name for o in scene.objects if o.type=='LIGHT' and not o.hide_render and o.data.energy>0]
    assert active==([] if b.get('world') else [key]),('Contaminated response basis',shot['basis_index'],active)
    shot['basis_fixture_audit']=dict(active_area_lights=active,world_strength=float(bg.inputs['Strength'].default_value))
    if exr not in bpy.app.handlers.render_pre:
        bpy.app.handlers.render_pre.append(exr)


F.prepare_shot = prepare
matches = camera_shots(BASE/'build/cameras.json')
F.SHOTS = {name+'__'+str(i):dict(matches[name],**F.PHOTO_POSES[name],basis_index=i,anchor_shot=name)
           for name in requested for i in range(len(BASES))}
indices=None
out = Path(sys.argv[sys.argv.index('--out')+1]);out.mkdir(parents=True,exist_ok=True)
if '--append' in sys.argv:
    sys.argv.remove('--append')
    previous=json.loads((out/'bases.json').read_text())
    indices=set(range(len(previous),len(BASES)))
if '--indices' in sys.argv:
    k=sys.argv.index('--indices');indices={int(v) for v in sys.argv[k+1].split(',')};del sys.argv[k:k+2]
if indices is not None:
    F.SHOTS={k:v for k,v in F.SHOTS.items() if v['basis_index'] in indices}
assert F.SHOTS,'No requested basis indices exist; inspect the recorded bases.json'
F.DEFAULT_SHOTS = ','.join(F.SHOTS)
old_meta=json.loads((out/'shots.json').read_text()) if indices is not None and (out/'shots.json').exists() else {}
if old_meta:
    old_bases=json.loads((out/'bases.json').read_text());assert old_bases==json.loads(json.dumps(BASES[:len(old_bases)])),'Response basis order changed; use a new folder'
main(F,interface)
if old_meta:
    current=json.loads((out/'shots.json').read_text());assert {r['sha256'] for r in current.values()}=={r['sha256'] for r in old_meta.values()},'Mixed source exports in response batches'
    old_meta.update(current);(out/'shots.json').write_text(json.dumps(old_meta,indent=2))
(out/'bases.json').write_text(json.dumps(BASES,indent=2))
(out/'diagnostic-parameters.json').write_text(json.dumps(dict(paint_roughness_override=roughness_override,paint_albedo_override=albedo_override,broad_only=broad_only,nonpaint_studio=nonpaint_studio),indent=2))
for path in out.glob('*.png'):
    if path.read_bytes()[:4] == bytes((118,47,49,1)):
        path.rename(path.with_suffix('.exr'))
configs=[Path(bpy.utils.resource_path(k))/'datafiles/colormanagement/config.ocio' for k in ('LOCAL','SYSTEM')]
(out/'ocio-path.txt').write_text(str(next(p for p in configs if p.exists())))
