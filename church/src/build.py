"""Serial family builder: modules, four ranges and two external-image sites."""
import argparse,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
import bpy
import geometry as G
from plan import church,range_plans
from surfaces import palette
from buildings import build
from package import counts,objects,canonical,publish,save_scene


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='build/family.blend');ap.add_argument('--seeds',default='101,202');ap.add_argument('--no-sites',action='store_true');ap.add_argument('--no-modules',action='store_true');ap.add_argument('--style');ap.add_argument('--bays',type=int);ap.add_argument('--width',type=float);ap.add_argument('--pitch',type=float);ap.add_argument('--tower');ap.add_argument('--top');args=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    report={};known=canonical();modules={}
    for seed in map(int,args.seeds.split(',')):
        bpy.ops.wm.read_factory_settings(use_empty=True);G.MATS.clear();palette()
        p=church(seed,args.style,args.bays,args.width,args.pitch,args.tower,args.top);rt=build(p)
        save_scene(f'build/church-{seed}.blend');report[f'Church-{seed}']=publish(rt,f'Church-{seed}',known)
        if not args.no_modules:
            for part in list(rt.children_recursive):
                kind=part.get('module_kind')
                if not kind or kind in modules:continue
                # Export independently at the module datum without mutating the
                # assembly. The clone's data are shared, not edited.
                cp=G.clone(part,'Module_'+kind);cp.location=(0,0,0);cp.rotation_euler=(0,0,0)
                modules[kind]=publish(cp,kind,known,'modules')
                for ob in reversed(objects(cp)):bpy.data.objects.remove(ob,do_unlink=True)
        if not args.no_sites:
            from site import site
            site_root=site(p,rt)
            save_scene(f'build/site-{seed}.blend');report[f'ChurchSite-{seed}']=publish(site_root,f'ChurchSite-{seed}',known)
        Path(f'build/plan-{seed}.json').write_text(json.dumps(p,indent=2))
    if not args.no_modules:
        bpy.ops.wm.read_factory_settings(use_empty=True);G.MATS.clear();palette()
        family=G.root('Generator range');x=-50
        for p in range_plans():
            rt=build(p);rt.parent=family;rt.location.x=x;x+=p['width']+24
        report['Range']=publish(family,'Range',known)
    save_scene(args.out);Path('build/metrics.json').write_text(json.dumps(dict(assets=report,modules=modules),indent=2))
    print('CHURCH METRICS',[(k,v['triangles']) for k,v in report.items()],flush=True)


if __name__=='__main__':main()
