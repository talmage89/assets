"""Independent exported geometry, layout, resource and sampled motion checks.

This checkpoint certifies script construction/serialization, not a physical
playground, surfacing impact attenuation, final UV atlases or baked look-dev.
"""
import argparse,hashlib,itertools,json,math,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.motion import sweep


def imported(path):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];pts=[];count=0
    for o in meshes:
        o.data.calc_loop_triangles();count+=len(o.data.loop_triangles)
        pts.extend(o.matrix_world@v.co for v in o.data.vertices)
        assert all(math.isfinite(v) for p in o.data.vertices for v in p.co)
        assert all(.99<loop.normal.length<1.01 for loop in o.data.loops),o.name
        assert o.data.uv_layers,o.name
        assert all(math.isfinite(v) for uv in o.data.uv_layers.active.data for v in uv.uv),o.name
    bounds=[[float(f(p[k] for p in pts)) for k in range(3)] for f in (min,max)]
    return meshes,count,bounds


def raw(path):
    doc=json.loads(path.read_text());buffers=[(path.parent/b['uri']).read_bytes() for b in doc['buffers']]
    comps={5126:np.float32,5125:np.uint32,5123:np.uint16,5121:np.uint8};sizes={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}
    def accessor(i):
        a=doc['accessors'][i];v=doc['bufferViews'][a['bufferView']];dt=np.dtype(comps[a['componentType']]);n=sizes[a['type']];offset=v.get('byteOffset',0)+a.get('byteOffset',0);stride=v.get('byteStride',dt.itemsize*n)
        return np.ndarray((a['count'],n),dtype=dt,buffer=buffers[v['buffer']],offset=offset,strides=(stride,dt.itemsize))
    for mesh in doc['meshes']:
        for p in mesh['primitives']:
            v=accessor(p['attributes']['POSITION']);idx=accessor(p['indices']).ravel();assert idx.max()<len(v)
            n=accessor(p['attributes']['NORMAL']);assert np.max(abs(np.linalg.norm(n,axis=1)-1))<.003
            assert 'TEXCOORD_0' in p['attributes'];assert len(idx)%3==0
    images=[]
    for im in doc.get('images',[]):
        assert 'uri' in im and not im['uri'].startswith('data:');p=path.parent/im['uri'];assert p.exists(),p
        images.append(dict(uri=im['uri'],bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    return dict(gltf_bytes=path.stat().st_size,bin_bytes=sum(len(b) for b in buffers),materials=len(doc.get('materials',[])),images=images)


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('build/check.json'));args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);manifest=json.loads(Path('build/manifest.json').read_text());result=dict(stage='form checkpoint only',pieces={},sites={},scope='Measured imported meshes and resources; tiling UV repetition intentional; no final unique-atlas UV or texture-bake claim')
    for name,source in manifest['pieces'].items():
        path=Path('export')/(name+'.gltf');meshes,n,bb=imported(path);cap=4000 if name.startswith('Slide') or name in ('HipRoof','Shade') else 2000
        assert n<=cap,(name,n,cap);assert n==source['triangles'],(name,n,source['triangles']);assert np.max(abs(np.array(bb)-source['bounds_m']))<3e-5,(name,bb,source['bounds_m'])
        row=dict(triangles=n,bounds_m=bb,**raw(path));result['pieces'][name]=row
        if name=='Post2339':
            coords=[o.matrix_world@v.co for o in meshes for v in o.data.vertices];ring=[p for p in coords if abs(p.z)<1e-5];r=sorted(set(round(math.hypot(p.x,p.y),7) for p in ring));row['measured_post_od_m']=2*max(r);row['measured_wall_m']=max(r)-min(r);assert abs(2*max(r)-.127)<1e-5
        if name=='Deck':
            zz=sorted(set(round((o.matrix_world@v.co).z,7) for o in meshes for v in o.data.vertices if abs((o.matrix_world@v.co).x)<.54 and abs((o.matrix_world@v.co).y)<.54));row['standing_skin_z_levels_m']=zz
        if name.startswith('Slide'):
            root=next(o for o in bpy.context.scene.objects if 'slide_kind' in o);pts=np.array(root['path_m']);ds=np.linalg.norm(np.diff(pts[:,:2],axis=0),axis=1);dz=np.diff(pts[:,2]);slopes=np.degrees(np.arctan2(abs(dz),ds));row['centerline_max_slope_degrees']=float(max(slopes));row['exit_height_m']=float(pts[-1,2]);row['last_flat_region_m']=float(sum(ds[-3:]));assert max(slopes)<50;assert .177<=pts[-1,2]<=.2795
        if name=='RampSegment':
            points=[]
            for o in meshes:
                for poly in o.data.polygons:
                    if 'QuickPerforated' in o.data.materials[poly.material_index].name and poly.normal.z>.8:
                        points.extend(o.matrix_world@o.data.vertices[v].co for v in poly.vertices)
            lo=min(p.y for p in points);hi=max(p.y for p in points);z0=max(p.z for p in points if abs(p.y-lo)<1e-5);z1=max(p.z for p in points if abs(p.y-hi)<1e-5)
            row['measured_slope']=(z1-z0)/(hi-lo);assert abs(row['measured_slope']-1/12)<1e-5
            row['nominal_infill_clear_m']=1.2192/12-.019;assert row['nominal_infill_clear_m']<.0889
    for source in manifest['sites']:
        seed=source['seed'];path=Path(f'export/Playground-{seed}.gltf');meshes,n,bb=imported(path);assert n<120000,(seed,n);assert n==source['total_triangles'],(seed,n,source['total_triangles']);row=dict(total_triangles=n,equipment_triangles=source['equipment_triangles'],**raw(path));zones=source['zones'];surface=source['surface'];gaps=[]
        for z in zones:
            a0,b0,a1,b1=z['rect'];assert surface[0]<=a0 and surface[1]<=b0 and surface[2]>=a1 and surface[3]>=b1,(seed,z,surface)
        for left,right in itertools.combinations(zones,2):
            a,b,c,d=left['rect'];e,f,g,h=right['rect'];dx=max(a-e if a>g else e-c,0);dy=max(b-f if b>h else f-d,0)
            overlap=max(0,min(c,g)-max(a,e))*max(0,min(d,h)-max(b,f));assert overlap<1e-7,(seed,left['name'],right['name'],overlap)
            gaps.append(dict(groups=[left['group'],right['group']],envelope_gap_m=math.hypot(max(a-g,e-c,0),max(b-h,f-d,0))))
        row['zone_gaps']=gaps
        # Sample real imported swing assemblies against the frame and one another.
        # Hangers belong to the fixed frame; chains are near-clearance surfaces.
        def ancestry(o):
            while o:
                yield o;o=o.parent
        for o in meshes:
            if any('Swing' in p.name for p in ancestry(o)):o['asset_set']='Playground'
            elif 'asset_set' in o:del o['asset_set']
        pivots=[o for o in bpy.context.scene.objects if o.get('motion_kind')=='rigid_swing_with_chains']
        specs=[]
        for pivot in pivots:
            ownermesh=next(o for o in pivot.children if o.type=='MESH');fixed=next(o for o in pivot.parent.children if o.type=='MESH')
            specs.append(dict(node=pivot.name,axis='X',range=[-55,55],step=11,tolerance_m=.001,allow=[dict(moving=ownermesh.name,fixed=fixed.name,reason='Intentional hanger bearing articulation at the pivot')]))
        motion=sweep(dict(MOTIONS=specs));assert motion['passed'],motion;row['swing_motion']=motion;result['sites'][str(seed)]=row
    protected=Path('build/protected.json')
    if protected.exists():
        inventory=json.loads(protected.read_text());assert all((ROOT/k).exists() and hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v for k,v in inventory.items());result['protected_existing_deliveries']=len(inventory)
    result['passed']=True;args.out.write_text(json.dumps(result,indent=2));print('CHECK PASSED',len(result['pieces']),'modules;',[(k,v['total_triangles']) for k,v in result['sites'].items()])
if __name__=='__main__':main()
