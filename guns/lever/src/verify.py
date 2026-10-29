"""Raw GLB checks, fresh imports, intended states and independent construction."""
import argparse
import json
import sys
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import weapon as W, weapon_verify as V
from kit.motion import surface
from kit.gltf import GLB
from check import geometry,contacts,semantics,sweep,parts
from build import source_hash
import interface


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',default='build/lever.blend');p.add_argument('--out',default='build/serialization.json')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve()
    bpy.ops.wm.open_mainfile(filepath=str(source));arm=bpy.data.objects['LeverArmature']
    assert bpy.context.scene['generator_sha256']==source_hash(),'Stale modeled source'
    srcgeo=geometry(arm);srccontacts=contacts(arm);srcstates=semantics(arm)
    samples=[(c,f*.5) for c,s in interface.CLIPS.items() for f in range(s['frames']*2+1)]
    sockets=[o.name for o in bpy.context.scene.objects if o.name.startswith('Socket_')]
    expected=V.capture(arm,samples,sockets)
    surfaces={}
    for c,s in interface.CLIPS.items():
        for f in {0,s['frames'],*s['events'].values()}:
            W.pose(arm,c,f);surfaces[c,f]=V.surface_points(parts())
    raw=GLB(source.with_suffix('.glb'));triangles=0
    for mesh in raw.json['meshes']:
        for prim in mesh['primitives']:
            triangles+=len(raw.accessor(prim['indices']))//3
            attrs=prim['attributes'];weights=raw.accessor(attrs['WEIGHTS_0'])
            assert np.all(np.sum(weights>1e-6,axis=1)==1)
            assert np.max(np.abs(weights.sum(axis=1)-1))<1e-6
            normal=raw.accessor(attrs['NORMAL']);position=raw.accessor(attrs['POSITION'])
            assert np.isfinite(normal).all() and np.isfinite(position).all()
            assert np.max(np.abs(np.linalg.norm(normal,axis=1)-1))<1e-5
    assert triangles==srcgeo['triangles']
    assert not raw.json.get('images')
    assert {c['name'] for c in raw.json['animations']}==set(interface.CLIPS)
    duration={}
    for clip in raw.json['animations']:
        times=[raw.accessor(s['input']) for s in clip['samplers']]
        actual=max(float(t.max()) for t in times)-min(float(t.min()) for t in times)
        wanted=interface.CLIPS[clip['name']]['frames']/60
        assert abs(actual-wanted)<1e-5,(clip['name'],actual,wanted)
        duration[clip['name']]=actual
    normal=V.normal_direction(raw)
    arm=V.import_glb(source.with_suffix('.glb'));impgeo=geometry(arm)
    impcontacts=contacts(arm);impstates=semantics(arm)
    assert all(r['passed'] for r in srccontacts+impcontacts),'Independent required contacts'
    motion=sweep(arm)
    Path(a.out).with_name('imported-motion.json').write_text(json.dumps(motion,indent=2))
    assert motion['passed'],'Imported clearance sweep'
    affine=V.compare(arm,expected,position_tolerance_m=3e-6,linear_tolerance=2e-5)
    deltas=[]
    for (clip,frame),points in surfaces.items():
        W.pose(arm,clip,frame);delta=V.surface_delta(points,V.surface_points(parts()))
        assert delta<3e-6,(clip,frame,delta)
        deltas.append(dict(clip=clip,frame=frame,surface_delta_m=delta))
    standalone={}
    for name,length in [('cartridge',.06477),('case',.0518)]:
        path=source.parent/(name+'.glb');raw=GLB(path)
        count=sum(len(raw.accessor(p['indices']))//3 for m in raw.json['meshes'] for p in m['primitives'])
        assert count<=1600 and not raw.json.get('skins') and not raw.json.get('animations')
        normals=V.normal_direction(raw)
        V.import_glb(path);obs=[o for o in bpy.context.scene.objects if o.type=='MESH']
        assert len(obs)==1 and obs[0].matrix_world.is_identity
        pts=np.asarray(V.surface_points(obs));low=pts.min(axis=0);high=pts.max(axis=0)
        # The headstamp is a comparison-only dark marking .025 mm behind the
        # head; the cartridge exterior itself retains the head-centered origin.
        assert abs(high[1]-length)<1e-6 and -.00005<low[1]<0
        assert abs(high[0]-low[0]-.01285)<1e-6
        assert abs(high[2]-low[2]-.01285)<1e-6
        solid=surface(obs[0])
        # Published exterior stations, independently measured on the actual
        # imported brass surface. The body, shoulder and neck must each be a
        # straight taper, with no bulge or dent between the C.I.P. stations.
        exterior=[]
        for begin,end,r0,r1,stations in [
            (.0031,.03660,.005355,.005095,(.0032,.010,.020,.030,.0365)),
            (.03660,.03969,.005095,.00423,(.0367,.038,.03959)),
            (.03969,.0518,.00423,.00419,(.040,.045,.0517))]:
            for y in stations:
                hit=solid['tree'].ray_cast(Vector((.02,y,0)),Vector((-1,0,0)),.03)[0]
                assert hit is not None
                wanted=r0+(r1-r0)*(y-begin)/(end-begin)
                assert abs(hit.x-wanted)<2e-6,(name,'C.I.P. straight exterior profile',y,hit.x,wanted)
                exterior.append(dict(y_m=y,radius_m=hit.x,reference_radius_m=wanted))
        primer_hits=[solid['tree'].ray_cast(Vector((x,-.001,0)),Vector((0,1,0)),.003)[0] for x in (0,.0015)]
        assert all(p is not None for p in primer_hits),'Visible primer face'
        dent=primer_hits[0].y-primer_hits[1].y
        expected_dent=(.00015<dent<.00027) if name=='case' else abs(dent)<1e-6
        assert expected_dent,(name,'primer accessibility',dent)
        rear=solid['tree'].ray_cast(Vector((0,.003,0)),Vector((0,-1,0)),.004)[0]
        assert rear is not None and rear.y-primer_hits[0].y>.00003,'Primer dent retains actual solid thickness'
        standalone[name]=dict(cip_exterior_samples=exterior,primer_center_and_edge_m=[list(p) for p in primer_hits],primer_dent_m=dent,primer_axial_thickness_m=rear.y-primer_hits[0].y,triangles=count,bytes=path.stat().st_size,dimensions_m=(high-low).tolist(),
            normal_direction=normals,fresh_import=True)
    result=dict(passed=True,triangles=triangles,bytes=source.with_suffix('.glb').stat().st_size,
        materials=len(GLB(source.with_suffix('.glb')).json['materials']),texture_images=0,
        named_meshes=len(srcgeo['parts']),clips=duration,normal_direction=normal,
        source_geometry=srcgeo,imported_geometry=impgeo,source_contacts=srccontacts,imported_contacts=impcontacts,
        source_states=srcstates,imported_states=impstates,imported_motion=motion,
        affine_samples=len(affine),maximum_position_delta_m=max(r['position_delta_m'] for r in affine),
        maximum_linear_delta=max(r['linear_delta'] for r in affine),surface_samples=deltas,standalones=standalone)
    Path(a.out).write_text(json.dumps(result,indent=2))
    print('VERIFIED',triangles,len(affine),'complete affine samples; imported contacts, states, clearances, detachables')


if __name__=='__main__':main()
