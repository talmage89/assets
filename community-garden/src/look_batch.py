"""Serial GPU batch: exported views and photographic comparisons, one lock.

CPU modeling/packaging runs before this script. No docs are generated here.
"""
import sys,argparse,json
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from render import render,sheet,setup,shot,bundle
import geometry as Q
from kit import photo_match

def specimens(out,width,samples):
    source=Path('export/checkpoint/CommunityGardenPieces.gltf');out=Path(out)/'plants';out.mkdir(parents=True,exist_ok=True)
    for sp in ('tomato','squash','bean','corn','marigold'):
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
        (out/(sp+'.json')).write_text(json.dumps(dict(source=str(source),bundle_sha256=bundle(source),camera=v,engine='CYCLES',samples=samples,scope='exported high specimen; morphology comparison, unsurveyed reference'),indent=2))

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='renders/lookdev');p.add_argument('--width',type=int,default=1200);p.add_argument('--samples',type=int,default=40);p.add_argument('--short',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    names=['hero','above','tomato','bean','squash'] if a.short else None
    for seed in (117,229,341):render(seed,Path(a.out)/str(seed),a.width,a.samples,names)
    if not a.short:
        sheet(a.out,1600,a.samples);specimens(a.out,a.width,a.samples)
        import match
        sys.argv=['match.py','--','--out',str(Path(a.out)/'matches'),'--width',str(a.width),'--samples',str(a.samples)]
        match.main()

if __name__=='__main__':main()
