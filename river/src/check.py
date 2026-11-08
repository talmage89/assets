"""Independent raw-accessor and fresh-import form/construction checks.

Intentional tiling UV reuse is allowed; no unique lightmap/atlas overlap or
final baked-detail certification is claimed at this form checkpoint.
"""
import json
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
import numpy as np
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from preserve import check as preserved
from package import bundle


def accessor(d,bin,index):
    a=d['accessors'][index];v=d['bufferViews'][a['bufferView']]
    typ={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']]
    n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
    offset=v.get('byteOffset',0)+a.get('byteOffset',0);stride=v.get('byteStride',np.dtype(typ).itemsize*n)
    return np.ndarray((a['count'],n),dtype=typ,buffer=bin,offset=offset,strides=(stride,np.dtype(typ).itemsize)).copy()


def raw(path):
    d=json.loads(path.read_text());binary=(path.parent/d['buffers'][0]['uri']).read_bytes();tris=0;norm=[];uv=[];flows=[];heightfield_faces=0;water_volume=None;context_volumes={}
    for me in d['meshes']:
        for pr in me['primitives']:
            inds=accessor(d,binary,pr['indices']).ravel();tris+=len(inds)//3
            v=accessor(d,binary,pr['attributes']['POSITION']);assert np.isfinite(v).all()
            if me['name']=='WaterSurface' or me['name'].startswith('DistantWaterVolume_'):
                # UV/normal splits in glTF do not make physical shell seams.
                points,remap=np.unique(np.round(v,6),axis=0,return_inverse=True)
                faces=remap[inds.reshape(-1,3)]
                edges=np.sort(np.concatenate((faces[:,[0,1]],faces[:,[1,2]],faces[:,[2,0]])),axis=1)
                _,uses=np.unique(edges,axis=0,return_counts=True)
                assert (uses==2).all(),('Open water volume',np.unique(uses,return_counts=True))
                tri=points[faces];volume=float(np.einsum('ij,ij->i',tri[:,0],np.cross(tri[:,1],tri[:,2])).sum()/6)
                assert volume>100,('Reversed water shell',me['name'],volume)
                if me['name']=='WaterSurface':water_volume=volume
                else:context_volumes[me['name']]=volume
            if me['name'] in ('BedBanksFloodplain','DistantValleySkins'):
                tv=v[inds.reshape(-1,3)];cross=np.cross(tv[:,1]-tv[:,0],tv[:,2]-tv[:,0])
                assert (cross[:,1]>=-1e-8).all(),('Downward terrain winding',me['name'],int((cross[:,1]<-1e-8).sum()))
                heightfield_faces+=len(cross)
            n=accessor(d,binary,pr['attributes']['NORMAL']);norm.extend(np.linalg.norm(n,axis=1))
            if 'TEXCOORD_0' in pr['attributes']:
                u=accessor(d,binary,pr['attributes']['TEXCOORD_0']);assert np.isfinite(u).all()
                tv=v[inds.reshape(-1,3)];tu=u[inds.reshape(-1,3)]
                area=np.linalg.norm(np.cross(tv[:,1]-tv[:,0],tv[:,2]-tv[:,0]),axis=1)/2
                du=tu[:,1]-tu[:,0];dv=tu[:,2]-tu[:,0]
                ua=abs(du[:,0]*dv[:,1]-du[:,1]*dv[:,0])/2
                valid=(area>1e-9)&(ua>1e-12)
                if valid.any():uv.extend(np.sqrt(ua[valid]/area[valid])*1024)
            if '_FLOW' in pr['attributes']:flows.extend(accessor(d,binary,pr['attributes']['_FLOW']))
    norm=np.array(norm);assert abs(norm-1).max()<.002
    flow=np.array(flows);assert len(flow)>1000,(path,'No exported flow')
    assert (flow[:,1]>.005).all() and flow[:,2].max()>1
    assert all((path.parent/im['uri']).is_file() for im in d.get('images',[]))
    # Expanded triangles count mesh reuse through nodes, not only stored meshes.
    expanded=sum(sum(d['accessors'][pr['indices']]['count']//3 for pr in d['meshes'][n['mesh']]['primitives']) for n in d['nodes'] if 'mesh' in n)
    return dict(stored_triangles=tris,placed_triangles=expanded,materials=len(d['materials']),images=len(d.get('images',[])),
        normal_length_error=float(abs(norm-1).max()),density_at_1024_px_m=np.percentile(uv,[5,50,95]).tolist(),
        flow_vertices=len(flow),flow_speed_m_s=np.percentile(np.linalg.norm(flow[:,:2],axis=1),[0,50,100]).tolist(),
        max_flow_depth_m=float(flow[:,2].max()),closed_water_shell_volume_m3=water_volume,closed_context_water_volumes_m3=context_volumes,
        upward_heightfield_faces=heightfield_faces,bytes_gltf=path.stat().st_size,bytes_bin=len(binary),bundle_sha256=bundle(path))


def bvh(ob):
    verts=[ob.matrix_world@v.co for v in ob.data.vertices];faces=[list(f.vertices) for f in ob.data.polygons]
    return BVHTree.FromPolygons(verts,faces,all_triangles=True)


def construction(seed):
    path=Path('export')/f'RiverCrossing-{seed}.gltf';bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
    obs=list(bpy.context.scene.objects);meta=json.loads(Path(f'build/RiverCrossing-{seed}.json').read_text())
    counts={}
    for ob in obs:
        if ob.type!='MESH':continue
        ob.data.calc_loop_triangles();key=ob.get('river_category','context');counts[key]=counts.get(key,0)+len(ob.data.loop_triangles)
    assert counts==meta['triangles'],(counts,meta['triangles'])
    assert counts['bridge']<80000 and counts['reach']<150000
    pads=[bvh(o) for o in obs if o.type=='MESH' and o.name.startswith('BearingStation')]
    supports=[bvh(o) for o in obs if o.type=='MESH' and o.name.startswith(('Pier_','Abutment_'))]
    gaps=[];seat_gaps=[];lengths=[]
    for ob in obs:
        if ob.type!='MESH' or not ob.name.startswith('Girder_'):continue
        ps=[ob.matrix_world@v.co for v in ob.data.vertices];xmin=min(p.x for p in ps);xmax=max(p.x for p in ps);y=(min(p.y for p in ps)+max(p.y for p in ps))/2;z=min(p.z for p in ps)
        lengths.append(xmax-xmin)
        underside=bvh(ob)
        for x in (xmin+.26,xmax-.26):
            foot=underside.ray_cast(Vector((x,y,z-.05)),Vector((0,0,1)),.3)[0]
            assert foot is not None,('Missing girder bearing seat',ob.name)
            origin=foot+Vector((0,0,.001));hits=[tree.ray_cast(origin,Vector((0,0,-1)),.6)[0] for tree in pads]
            hit=[h for h in hits if h is not None];assert hit,('Unsupported girder',ob.name,x)
            gaps.append(min(abs(foot.z-h.z) for h in hit))
            for dx,dy in ((0,0),(-.24,-.30),(-.24,.30),(.24,-.30),(.24,.30)):
                start=Vector((x+dx,y+dy,foot.z-.5))
                bases=[t.ray_cast(start,Vector((0,0,1)),.6)[0] for t in pads]
                bases=[h for h in bases if h is not None];assert bases,('No bearing base',ob.name)
                base=min(bases,key=lambda h:h.z)
                seats=[t.ray_cast(base+Vector((0,0,.001)),Vector((0,0,-1)),1)[0] for t in supports]
                seats=[h for h in seats if h is not None];assert seats,('Unsupported bearing plinth',ob.name,x+dx,y+dy)
                seat_gaps.append(min(abs(base.z-h.z) for h in seats))
    assert max(gaps)<.002,('Girder/pad gap',max(gaps))
    assert max(seat_gaps)<.002,('Plinth/support gap',max(seat_gaps))
    # Sample actual imported reach cross-sections, not declared width constants.
    bed=next(o for o in obs if o.name=='BedBanksFloodplain');tree=bvh(bed);water=next(o for o in obs if o.name=='WaterSurface')
    rail_gaps=[]
    for rail in [o for o in obs if o.type=='MESH' and o.name.startswith('ApproachRail_')]:
        points=[rail.matrix_world@v.co for v in rail.data.vertices];bottom=min(p.z for p in points)
        for point in points:
            if point.z>bottom+1e-5:continue
            soil=tree.ray_cast(point+Vector((0,0,1)),Vector((0,0,-1)),2)[0]
            assert soil is not None,('Guardrail post has no soil',rail.name,tuple(point))
            rail_gaps.append(point.z-soil.z)
    assert rail_gaps and min(rail_gaps)>-.03 and max(rail_gaps)<.002,('Guardrail foot/soil',min(rail_gaps),max(rail_gaps))
    samples=[]
    for y in (-80,0,40,75):
        row=[v.co for v in water.data.vertices if abs(v.co.y-y)<.02]
        if not row:continue
        world=[water.matrix_world@v for v in row];samples.append(dict(y_m=y,width_m=max(v.x for v in world)-min(v.x for v in world)))
    headroom=[];socket_gaps={};building_walk_checks=0;light_gaps=[];alley_gaps=[]
    for name in ('BoatLaunch','FishingSpot'):
        socket=next((o for o in obs if o.name==name),None)
        if socket is None:continue
        surface=tree if name=='FishingSpot' else bvh(next(o for o in obs if o.name=='FloodwallTrailAndAccess'))
        pos=socket.matrix_world.translation
        hit=surface.ray_cast(pos+Vector((0,0,1)),Vector((0,0,-1)),3)[0]
        assert hit is not None,('Socket has no landing',name)
        socket_gaps[name]=abs(pos.z-hit.z)
        assert socket_gaps[name]<.025,('Socket above landing',name,socket_gaps[name])
    if seed==101:
        streets=next(o for o in obs if o.name=='MainStreetAndServiceAlleys')
        front=next(o['main_street_front_m'] for o in obs if o.name=='TownContext')
        for f in streets.data.polygons:
            point=streets.matrix_world@f.center
            if abs(point.x)>=front-1:continue
            soil=tree.ray_cast(point+Vector((0,0,1)),Vector((0,0,-1)),3)[0]
            assert soil is not None,('Alley has no ground',tuple(point))
            alley_gaps.append(point.z-soil.z)
        assert alley_gaps and min(alley_gaps)>.04 and max(alley_gaps)<.10,('Alley paving/soil',min(alley_gaps),max(alley_gaps))
        plinth=bvh(next(o for o in obs if o.name=='ParapetLightPedestals'))
        bases=[o for o in obs if o.type=='MESH' and 'Parapet light' in o.name and 'StreetLight_Mesh' in o.name]
        assert len(bases)==4,('Missing native light bases',len(bases))
        for base in bases:
            points=[base.matrix_world@v.co for v in base.data.vertices];bottom=min(p.z for p in points)
            for point in points:
                if point.z>bottom+1e-5:continue
                seat=plinth.ray_cast(point+Vector((0,0,.001)),Vector((0,0,-1)),.3)[0]
                assert seat is not None,('Unsupported lamp base',base.name,tuple(point))
                light_gaps.append(abs(point.z-seat.z))
        assert max(light_gaps)<.002,('Lamp/pedestal gap',max(light_gaps))
        trail=next(o for o in obs if o.name=='RiverbankTrail');pts=np.array(json.loads(trail['points_blender_m']))
        for building in [o for o in obs if o.name.startswith('MainStreetBack_') and o.parent and o.parent.name=='TownContext']:
            building_walk_checks+=1
            corners=[ob.matrix_world@Vector(v) for ob in building.children_recursive if ob.type=='MESH' for v in ob.bound_box]
            if not corners:continue
            bounds=np.array(corners);lo=bounds.min(axis=0);hi=bounds.max(axis=0)
            along=pts[(pts[:,1]>=lo[1]-1)&(pts[:,1]<=hi[1]+1)]
            assert all(x+1.65<lo[0] or x-1.65>hi[0] for x,y,z in along),('Building over riverwalk',building.name,lo.tolist(),hi.tolist())
        assert building_walk_checks==40,('Missing building/walk audit',building_walk_checks)
        walk=bvh(next(o for o in obs if o.name=='FloodwallTrailAndAccess'))
        beams=[bvh(o) for o in obs if o.type=='MESH' and o.name.startswith('Girder_')]
        stations=sorted({round(sum((o.matrix_world@v.co).y for v in o.data.vertices)/len(o.data.vertices),5) for o in obs if o.type=='MESH' and o.name.startswith('Girder_')})
        for y in stations:
            center=float(np.interp(y,pts[:,1],pts[:,0]))
            for offset in (-.8,0,.8):
                x=center+offset;floor=walk.ray_cast(Vector((x,y,1.0)),Vector((0,0,-1)),2)[0]
                assert floor is not None,('Walk missing',x,y)
                hits=[t.ray_cast(floor+Vector((0,0,.002)),Vector((0,0,1)),5)[0] for t in beams]
                heights=[h.z-floor.z for h in hits if h is not None]
                assert heights,('No overhead beam at walk',x,y)
                headroom.append(min(heights))
        assert min(headroom)>2.3,('Walk headroom',min(headroom))
    return dict(categories=counts,bearing_surface_samples=len(gaps),max_girder_pad_gap_m=max(gaps),
                plinth_support_samples=len(seat_gaps),max_plinth_support_gap_m=max(seat_gaps),girder_lengths_m=sorted(set(round(x,5) for x in lengths)),water_width_samples=samples,
                riverwalk_headroom_samples=len(headroom),minimum_sampled_riverwalk_headroom_m=min(headroom) if headroom else None,
                gameplay_socket_surface_gaps_m=socket_gaps,building_walk_bounds_checks=building_walk_checks,
                alley_soil_samples=len(alley_gaps),alley_paving_minus_soil_range_m=[min(alley_gaps),max(alley_gaps)] if alley_gaps else None,
                lamp_base_surface_samples=len(light_gaps),maximum_lamp_pedestal_gap_m=max(light_gaps) if light_gaps else None,
                guardrail_foot_samples=len(rail_gaps),guardrail_foot_minus_soil_range_m=[min(rail_gaps),max(rail_gaps)])


def main():
    results={}
    for seed in (101,202):results[str(seed)]=dict(raw=raw(Path(f'export/RiverCrossing-{seed}.gltf')),construction=construction(seed))
    modules=json.loads(Path('build/manifest.json').read_text())['modules']
    for m in modules:
        path=Path('export/pieces')/(m['name']+'.gltf');d=json.loads(path.read_text())
        count=sum(sum(d['accessors'][p['indices']]['count']//3 for p in d['meshes'][n['mesh']]['primitives']) for n in d['nodes'] if 'mesh' in n)
        assert count==m['triangles'] and count<=m['limit'],(m,count)
        m['serialized_triangles']=count
    path=Path('export/pieces/TypeIII_Girder18.gltf');d=json.loads(path.read_text());bin=(path.parent/d['buffers'][0]['uri']).read_bytes()
    v=np.concatenate([accessor(d,bin,p['attributes']['POSITION']) for me in d['meshes'] for p in me['primitives']])
    end=v[abs(v[:,0]-v[:,0].min())<1e-5];z=end[:,1];y=-end[:,2]
    section=dict(depth_m=float(z.max()-z.min()),top_width_m=float(np.ptp(y[z>1.14])),bottom_width_m=float(np.ptp(y[z<.21])),web_width_m=float(np.ptp(y[(z>.38)&(z<.90)])))
    section['vertical_stations_m']=np.unique(np.round(z,5)).tolist()
    assert np.allclose(section['vertical_stations_m'],[0,.01905,.1778,.3683,.8509,.9652,1.143],atol=2e-5)
    for key,target in [('depth_m',1.143),('top_width_m',.4064),('bottom_width_m',.5588),('web_width_m',.1778)]:
        assert abs(section[key]-target)<2e-5,(key,section[key],target)
    report=dict(passed=True,crossings=results,modules=modules,preserved_files=preserved(),
        measured_girder_end_section=section,scope='form, raw normals/finite tiling UV/density, flow, actual bearing contacts and serialization')
    Path('build/check.json').write_text(json.dumps(report,indent=2)+'\n');print('RIVER_CHECK_PASS')


if __name__=='__main__':main()
