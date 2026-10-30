"""Actual delivered PBR, lossless subsets, rig and surface/motion checks."""
import hashlib,io,json,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
from PIL import Image
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import uv,weapon as W,weapon_verify as V,detachable_verify as D,motion
from kit.gltf import GLB
from interface import CLIPS
from check import meshes,contacts,ALLOW,semantics
from delivery import split_imported

def unique(objects):
    seen=set();result=[]
    for ob in objects:
        if ob.data.as_pointer() in seen:continue
        seen.add(ob.data.as_pointer());result.append(ob)
    return result
def main():
    source=BASE/'build/delivery/finalized.blend';bpy.ops.wm.open_mainfile(filepath=str(source))
    arm=bpy.data.objects['HarrowArmature'];W.pose(arm,None,0)
    u=uv.report(unique([o for o in bpy.context.scene.objects if o.type=='MESH']),2048)
    assert not u['outside_triangles'] and not u['degenerate_uv_triangles'] and u['overlap_fraction']<1e-5
    samples=[(name,float(i)) for name,s in CLIPS.items() for i in range(s['frames']+1)]
    sockets=[o.name for o in bpy.context.scene.objects if o.name.startswith('Socket_')]
    expected=V.capture(arm,samples,sockets);surfaces={}
    detached_frames={}
    for state,clip in [('loaded','Idle'),('empty','IdleEmpty')]:
        W.pose(arm,clip,0)
        members=[o for o in meshes(arm) if o.get('bone') in ('Magazine','BoxLid') or (state=='loaded' and o.get('bone') in ('BeltLink15','BeltRound15','BeltRound16'))]
        detached_frames['box_'+state]=(V.surface_points(members),bpy.data.objects['Socket_Magazine'].matrix_world.copy())
    loose_points={}
    for name,offset in [('cartridge',.4),('case',.5),('link',.6)]:
        ob=bpy.data.objects[name.title()+'_Proof']
        loose_points[name]=[tuple(ob.matrix_world@v.co-Vector((offset,0,0))) for v in ob.data.vertices]
    for clip,f in [('Idle',0),('Fire',4),('Reload',60),('ReloadEmpty',140),('BipodDeploy',84),('BeltEnd',12)]:
        W.pose(arm,clip,f);surfaces[clip,f]=V.surface_points(meshes(arm))
    bake=json.loads((BASE/'build/baked/4k/bake-report.json').read_text());assert bake['size']==4096 and bake['samples']>=32
    for channel in ('BaseColor','BaseColorAlpha','Roughness','Metallic','AO','MaterialAO','Normal'):
        assert bake[channel]['alpha_missed_interior_texels']==0,(channel,bake[channel])
    canonical=sorted(hashlib.sha256((BASE/'textures'/('T_Harrow56_'+c+'.png')).read_bytes()).hexdigest() for c in ('BaseColor','Normal','ORM'))
    outputs={}
    for name,size,limit in [('lmg',2048,48000),('box_loaded',1024,5000),('box_empty',1024,4000),('cartridge',512,1000),('case',512,800),('link',512,300)]:
        path=BASE/'export'/(name+'.glb');g=GLB(path)
        triangles=sum(len(g.accessor(p['indices']))//3 for node in g.json['nodes'] if 'mesh' in node for p in g.json['meshes'][node['mesh']]['primitives'])
        assert triangles<=limit and len(g.json['materials'])==1 and len(g.json['images'])==3,(name,triangles)
        for i in range(3):assert Image.open(io.BytesIO(g.image(i))).size==(size,size)
        assert g.json['materials'][0].get('alphaMode','OPAQUE')=='OPAQUE'
        assert 'KHR_materials_specular' in g.json['materials'][0]['extensions']
        if name=='lmg':
            assert sorted(hashlib.sha256(g.image(i)).hexdigest() for i in range(3))==canonical
            assert {a['name'] for a in g.json['animations']}==set(CLIPS)
            assert len(g.json['skins'])==1
            for prefix in ('Belt_Round_','Belt_Link_'):
                assert len({n['mesh'] for n in g.json['nodes'] if n.get('name','').startswith(prefix) and 'mesh' in n})==1
            for animation in g.json['animations']:
                duration=max(float(g.accessor(s['input']).max()) for s in animation['samplers'])
                assert abs(duration-CLIPS[animation['name']]['frames']/60)<2e-6
        else:assert not g.json.get('animations') and not g.json.get('skins')
        row=dict(triangles=triangles,materials=1,texture_size=size,bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),normal_direction=V.normal_direction(g))
        if name!='lmg':
            layout=BASE/'build/delivery/detachables'/name/'layout.json'
            # Two cartridges reuse exactly the same source chart and integer
            # translation in the loaded box. The generic verifier requires a
            # unique chart lookup. Coalesce only identical source/destination
            # rectangles, retaining every triangle in the audit manifest.
            data=json.loads(layout.read_text());canonical_rows={}
            for r in data['islands']:
                key=tuple(tuple(r[k]) for k in ('source_origin','destination_origin','shape'))
                if key in canonical_rows:
                    old=canonical_rows[key]
                    assert old.get('cluster')==r.get('cluster')
                    old['triangle_pixels'].extend(r.get('triangle_pixels',[]))
                else:canonical_rows[key]=r
            data['islands']=list(canonical_rows.values())
            audit_layout=layout.with_name('audit-layout.json');audit_layout.write_text(json.dumps(data))
            row['subset']=D.audit(path,BASE/'textures','Harrow56',audit_layout,gun=BASE/'export/lmg.glb')
            row['mips']=D.mip_bleed(path,BASE/'textures','Harrow56',audit_layout,gun=BASE/'export/lmg.glb')
        outputs[name]=row
        for mesh in g.json['meshes']:
            for primitive in mesh['primitives']:
                assert 'COLOR_0' not in primitive['attributes'], 'Inspection colors must not tint the baked atlas'
                normals=g.accessor(primitive['attributes']['NORMAL'])
                assert np.isfinite(normals).all() and np.max(abs(np.linalg.norm(normals,axis=1)-1))<1e-5
                if 'WEIGHTS_0' in primitive['attributes']:
                    weights=g.accessor(primitive['attributes']['WEIGHTS_0'])
                    assert np.max(abs(weights.sum(axis=1)-1))<1e-6 and np.all(np.sum(weights>1e-6,axis=1)==1)
    arm=V.import_glb(BASE/'export/lmg.glb')
    affine=V.compare(arm,expected,position_tolerance_m=3e-5,linear_tolerance=.001)
    deltas=[]
    for (clip,f),points in surfaces.items():
        W.pose(arm,clip,f);delta=V.surface_delta(points,V.surface_points(meshes(arm)));assert delta<3e-6,(clip,f,delta)
        deltas.append(dict(clip=clip,frame=f,delta_m=delta))
    diagnostic=split_imported(bpy.context.scene,source)
    fit=contacts(arm);assert all(r['passed'] for r in fit)
    states=semantics(arm)
    sweep=motion.sweep_clips(arm,list(CLIPS),step_frames=1,tolerance_m=.0002,allow=ALLOW);assert sweep['passed']
    W.pose(arm,'Idle',0);bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'build/delivery/imported-parts.blend'))
    for name in ('box_loaded','box_empty','cartridge','case','link'):
        V.import_glb(BASE/'export'/(name+'.glb'));objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
        points=V.surface_points(objects)
        if name in detached_frames:
            expected_points,frame=detached_frames[name]
            delta=V.surface_delta(expected_points,[tuple(frame@Vector(p)) for p in points])
        else:delta=V.surface_delta(loose_points[name],points)
        assert delta<2e-6,(name,delta)
        outputs[name]['spawn_or_template_surface_delta_m']=delta
    result=dict(passed=True,outputs=outputs,uv={k:v for k,v in u.items() if k!='island_measurements'},
                intentional_uv_reuse='17 rounds / 16 links, one charted mesh each; report counts each data block once',
                bake_size=4096,bake_samples=bake['samples'],missed_interior_texels=0,
                affine_samples=len(affine),maximum_position_delta_m=max(r['position_delta_m'] for r in affine),
                posed_surfaces=deltas,contacts=fit,states=states,motion=sweep,imported_attribution=diagnostic)
    (BASE/'build/delivery/verify.json').write_text(json.dumps(result,indent=2));print('FINAL ATLAS VERIFIED',len(affine),'poses',flush=True)
if __name__=='__main__':main()
