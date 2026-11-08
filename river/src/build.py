"""Build original bridge modules and two places, then external glTF exports."""
import argparse
import json
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
sys.path[:0]=[str(REPO),str(HERE)]
import bpy
from kit import tiling
import geometry as G
import materials
import bridge
import channel
import site as builtin_site
import importlib.util
# Python already owns `site`; keep this asset module out of that namespace.
spec=importlib.util.spec_from_file_location('river_site',HERE/'site.py');site=importlib.util.module_from_spec(spec);spec.loader.exec_module(site)
import context
from plan import generate
from package import externalize


def counts(objects=None):
    result={};pieces=[]
    for ob in objects or bpy.context.scene.objects:
        if ob.type!='MESH':continue
        ob.data.calc_loop_triangles();n=len(ob.data.loop_triangles);key=ob.get('river_category','context')
        result[key]=result.get(key,0)+n
    return result


def save(stem,root,meta):
    bpy.context.view_layer.update();objects=G.descendants(root)
    meta['triangles']=counts(objects)
    path=Path('build/embedded')/(stem+'.glb');tiling.export(path,objects)
    meta.update(externalize(path,Path('export')/(stem+'.gltf')))
    Path('build/'+stem+'.json').write_text(json.dumps(meta,indent=2)+'\n')
    return meta


def library():
    bpy.ops.wm.read_factory_settings(use_empty=True);materials.palette(REPO)
    rt=G.root('RiverModules');pieces=[]
    for name,fn in [('TypeIII_Girder18',bridge.girder),('DeckPanel6',bridge.deck),('Parapet6',bridge.parapet),
                    ('PierColumns',bridge.pier),('PierWall',lambda n:bridge.pier(n,kind='wall')),
                    ('Abutment',bridge.abutment),('GuardrailTerminal',bridge.guardrail)]:
        ob=fn(name);ob.parent=rt
        row=save('pieces/'+name,ob,dict(module=name))
        tris=sum(row['triangles'].values());limit=8000 if name.startswith(('Pier','Abutment')) else 2000
        if tris>limit:raise ValueError((name,tris,limit))
        pieces.append(dict(name=name,triangles=tris,limit=limit))
        i=len(pieces)-1;ob.location=((i%3)*23,(i//3)*17,0)
    save('RiverModules',rt,dict(pieces=pieces))
    return pieces


def crossing(seed):
    bpy.ops.wm.read_factory_settings(use_empty=True);G.M.clear();materials.palette(REPO)
    p=generate(seed);rt=G.root('Crossing_'+str(seed),plan=p.data(),checkpoint='form / quick materials')
    reach=channel.terrain(p,rt);channel.water(p,reach)
    bridge.assemble(p,rt);site.road(p,rt);site.fixtures(p,rt);site.plants(p,rt)
    context.add(p,rt);context.clear_templates()
    # Curves also remain natively editable in the construction scene. Export
    # sockets carry the same sampled paths in extras for stock glTF consumers.
    for ob in list(rt.children_recursive):
        if ob.get('points_blender_m'):
            curve=bpy.data.curves.new(ob.name+'__Curve','CURVE');curve.dimensions='3D'
            sp=curve.splines.new('POLY');pts=json.loads(ob['points_blender_m']);sp.points.add(len(pts)-1)
            for point,co in zip(sp.points,pts):point.co=(*co,1)
            cu=bpy.data.objects.new(curve.name,curve);bpy.context.collection.objects.link(cu);cu.parent=ob
    data=save('RiverCrossing-'+str(seed),rt,dict(plan=p.data()))
    Path('build/scenes').mkdir(exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(Path('build/scenes',str(seed)+'.blend').resolve()))
    return data


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seeds',nargs='+',type=int,default=[101,202]);ap.add_argument('--out',default='build/river.blend');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    Path('build/pieces').mkdir(parents=True,exist_ok=True)
    pieces=library();rows=[crossing(seed) for seed in a.seeds]
    Path('build/manifest.json').write_text(json.dumps(dict(modules=pieces,crossings=rows),indent=2)+'\n')
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
    print('RIVER_BUILD',[(r['plan']['seed'],r['triangles']) for r in rows])


if __name__=='__main__':main()
