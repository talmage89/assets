"""Serial GPU batch: exported views and photographic comparisons, one lock.

CPU modeling/packaging runs before this script. No docs are generated here.
"""
import sys,argparse,json,hashlib
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from render import render,sheet,setup,shot,bundle,RECIPE_SHA256
import geometry as Q
from kit import photo_match

def specimens(out,width,samples,species=None):
    source=Path('export/final/CommunityGardenPieces.gltf');out=Path(out)/'plants';out.mkdir(parents=True,exist_ok=True)
    for sp in (species or ('tomato','squash','bean','corn','marigold')):
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
        roots={o.name:o for o in bpy.context.scene.objects if not o.parent};keep=[roots[sp+'_2_0']]
        if sp=='tomato':keep.append(roots['TomatoCage']);roots['TomatoCage'].location.z=-.20
        if sp=='bean':keep.append(roots['BeanTrellis'])
        for r in roots.values():
            if r not in keep:
                for ob in [*r.children_recursive,r]:bpy.data.objects.remove(ob,do_unlink=True)
        if sp=='bean':
            # Compare the actual teepee-climbing prototype on its support.
            for ob in [*roots['BeanTrellis'].children_recursive,roots['BeanTrellis']]:bpy.data.objects.remove(ob,do_unlink=True)
        Q.palette();rt=Q.root('Specimen comparison grade');Q.box('Dark neutral soil',(0,0,-.04),(80,80,.08),rt,'Soil')
        h={'tomato':1.85,'bean':2.10,'corn':2.5,'squash':.80,'marigold':.45}[sp]
        cam=setup(samples);v=dict(location=(-h*1.2,-h*2.3,h*.90),target=(0,0,h*.48),lens=75,aspect=1.0,sun_energy=2.0,sun_angle=15,sky_strength=.45,exposure=-.15)
        if sp=='squash':v.update(location=(-1.4,-1.8,1.35),target=(0,0,.25),lens=50)
        shot(cam,v,out/(sp+'.png'),width)
        (out/(sp+'.json')).write_text(json.dumps(dict(source=str(source),bundle_sha256=bundle(source),render_script_sha256=RECIPE_SHA256,botanical_recipe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),camera=v,engine='CYCLES',samples=samples,scope='exported high specimen; morphology comparison, unsurveyed reference'),indent=2))

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='renders/lookdev');p.add_argument('--width',type=int,default=1200);p.add_argument('--samples',type=int,default=40);p.add_argument('--short',action='store_true');p.add_argument('--specimens-only',action='store_true');p.add_argument('--ear-only',action='store_true');p.add_argument('--species',nargs='+');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.specimens_only:specimens(a.out,a.width,a.samples,a.species);return
    if a.ear_only:ear_detail(Path(a.out)/'plants',a.width,a.samples);return
    names=['hero','above','tomato','bean','squash'] if a.short else None
    for seed in (117,229,341):render(seed,Path(a.out)/str(seed),a.width,a.samples,names)
    if not a.short:
        sheet(a.out,1600,a.samples);specimens(a.out,a.width,a.samples)
        import match
        sys.argv=['match.py','--','--out',str(Path(a.out)/'matches'),'--width',str(a.width),'--samples',str(a.samples)]
        match.main()




def ear_detail(out,width,samples,source='export/final/CommunityGardenPieces.gltf'):
    """Actual old/new corn ear assembly under an identical close camera."""
    source=Path(source);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
    roots={o.name:o for o in bpy.context.scene.objects if not o.parent};corn=roots['corn_2_0']
    for rt in roots.values():
        if rt!=corn:
            for ob in [*rt.children_recursive,rt]:bpy.data.objects.remove(ob,do_unlink=True)
    Q.palette();rt=Q.root('Corn inspection grade');Q.box('Dark neutral grade',(0,0,-.04),(80,80,.08),rt,'Soil')
    cam=setup(samples);v=dict(location=(.65,-1.05,1.48),target=(.055,0,1.29),lens=70,aspect=1.35,sun_energy=2,sun_angle=15,sky_strength=.45,exposure=-.15)
    shot(cam,v,out/'corn-ear.png',width)
    (out/'corn-ear.json').write_text(json.dumps(dict(source=str(source),bundle_sha256=bundle(source),render_script_sha256=RECIPE_SHA256,botanical_recipe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),camera=v,samples=samples,engine='CYCLES'),indent=2))


if __name__=='__main__':main()
