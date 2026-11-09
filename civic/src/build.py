"""Build six civic programs and two separate seeded places."""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from plans import cases,site
from buildings import hall
from station import station
from delivery import counts,consolidate,publish


def make_building(p):return station(p) if p['program']=='station' else hall(p)


def center(a,off=None):
    c=counts(a.root.children_recursive)
    off=Vector(off) if off is not None else Vector(((c['bounds_min'][0]+c['bounds_max'][0])/2,(c['bounds_min'][1]+c['bounds_max'][1])/2,0))
    # Center physical footprint while retaining real hinge/threshold frames.
    for ob in list(a.root.children):
        if ob.type=='MESH':
            ob.data.transform(ob.matrix_basis);ob.matrix_basis.identity();ob.data.transform(__import__('mathutils').Matrix.Translation(-off))
        else:ob.location-=off
    return off


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--buildings-only',action='store_true');ap.add_argument('--seeds',default='101,202');args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    report={};Path('build').mkdir(exist_ok=True)
    for p in cases():
        bpy.ops.wm.read_factory_settings(use_empty=True);a=make_building(p)
        source=counts(a.root.children_recursive);off=center(a);p['origin_offset_m']=list(off)
        bpy.ops.wm.save_as_mainfile(filepath=str(Path('build',f"Civic-{p['seed']}-source.blend").resolve()))
        consolidate(a);name=f"Civic-{p['seed']}";data=publish(name,[a.root]+list(a.root.children_recursive));data.update(plan=p,source=source)
        report[name]=data
        if not args.buildings_only and str(p['seed']) in args.seeds.split(','):
            from sites import build_site
            sp=site(p['seed']);sp['building']=p
            s=build_site(sp,a,off);consolidate(s)
            l,r,f,k=sp['parcel'];sp['origin_offset_m']=list(center(s,((l+r)/2,(f+k)/2,0)))
            report[f"Site-{p['seed']}"]=publish(f"Site-{p['seed']}",[s.root]+list(s.root.children_recursive))
            report[f"Site-{p['seed']}"]['plan']=sp
            bpy.ops.wm.save_as_mainfile(filepath=str(Path('build',f"Site-{p['seed']}.blend").resolve()))
    from sheets import build as build_sheets
    build_sheets()
    Path('build/family.json').write_text(json.dumps(report,indent=2)+'\n')
    used={(path.parent/im['uri']).resolve() for path in Path('export').glob('*.gltf') for im in json.loads(path.read_text()).get('images',[])}
    for path in Path('export/shared').glob('*.png'):
        if path.resolve() not in used:path.unlink()


if __name__=='__main__':main()
