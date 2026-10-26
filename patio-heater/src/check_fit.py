"""Optional external cylinder metrology and clearance; no save/export calls."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.assembly import distance
from kit.motion import surface,penetration
from settings import VALVE_FACE

def main():
    p=argparse.ArgumentParser();p.add_argument('--grill',required=True);p.add_argument('--reference',default='');p.add_argument('--out',required=True);p.add_argument('--parts-source',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    path=Path(a.reference).expanduser()
    if not a.reference or not path.is_file():
        Path(a.out).write_text(json.dumps(dict(passed=True,skipped='Optional owner cylinder absent; published envelope remains the design basis'),indent=2));return
    assert not path.resolve().is_relative_to(ROOT)
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if Path(a.grill).suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(Path(a.grill).resolve()))
    else:bpy.ops.import_scene.gltf(filepath=str(Path(a.grill).resolve()))
    socket=bpy.data.objects['tank_socket'].matrix_world.copy();reg=bpy.data.objects['regulator_attach'].matrix_world.copy()
    error=(reg.translation-socket@Vector(VALVE_FACE)).length
    assert error<2e-5
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.parts_source).resolve()))
    components=[o for o in bpy.context.scene.objects if o.type=='MESH']
    socket=bpy.data.objects['tank_socket'].matrix_world.copy();hose=list(bpy.data.objects['HeaterBody']['hose_path_m'])
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path));imported=set(bpy.context.scene.objects)-before
    visual=[o for o in imported if o.type=='MESH' and 'collision' not in o.name.lower()]
    canonical=[o.matrix_world@v.co for o in visual for v in o.data.vertices]
    lo=Vector(tuple(min(v[k] for v in canonical) for k in range(3)));hi=Vector(tuple(max(v[k] for v in canonical) for k in range(3)))
    assert (hi-lo-Vector((.3122,.3122,.468000263))).length<.00002
    for ob in imported:ob.matrix_world=socket@ob.matrix_world
    bpy.context.view_layer.update()
    vertices=[];faces=[]
    for ob in visual:
        offset=len(vertices);vertices.extend(ob.matrix_world@v.co for v in ob.data.vertices);faces.extend(tuple(offset+i for i in f.vertices) for f in ob.data.polygons)
    tree=BVHTree.FromPolygons(vertices,faces)
    coupling=next(o for o in components if o.name=='Type 1 black handwheel')
    coupling_gap=min(distance(coupling,v)[0] for v in visual)
    assert coupling_gap<.0003,'Coupling lip does not seat near the actual tank outlet'
    gaps=[tree.find_nearest(Vector(hose[i:i+3]))[3]-.0052 for i in range(0,len(hose),3)]
    assert min(gaps)>.0005,'Hose intersects tank'
    solids=[surface(o) for o in visual];rows=[]
    prefixes=('Rolled cabinet','Cabinet rear','Curved tank door','Internal stanchion','Post support spider','Housing shoulder','Tank support floor','Tank foot ring stop')
    for ob in components:
        if not ob.name.startswith(prefixes):continue
        current=surface(ob);depth=max(penetration(current,s,.0002)[0] for s in solids);gap=min(distance(ob,v)[0] for v in visual)
        rows.append(dict(part=ob.name,maximum_penetration_m=depth,minimum_sampled_surface_distance_m=gap));assert depth<.0002,ob.name+' intersects tank'
    result=dict(passed=True,reference_sha256=sha,canonical_bounds_m=dict(min=list(lo),max=list(hi),size=list(hi-lo)),tank_socket_blender_m=list(socket.translation),tank_yaw_degrees=0,valve_face_world_m=list(socket@Vector(VALVE_FACE)),regulator_socket_error_m=error,coupling_sampled_surface_gap_m=coupling_gap,minimum_hose_clearance_m=min(gaps),surface_checks=rows,scope='Actual external tank triangle surfaces versus finalized components; socket transform error is serialization only; no removal-path proof')
    Path(a.out).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));assert hashlib.sha256(path.read_bytes()).hexdigest()==sha
if __name__=='__main__':main()
