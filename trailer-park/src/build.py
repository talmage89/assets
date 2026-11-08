"""Build component libraries, example lots and two external-image communities."""
import argparse,hashlib,json,math,os,sys
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from geometry import Assembly,place,consolidate,ROOT
from plans import home,park
import homes,addons,site as _builtin_site
_IMAGE_CACHE=None
# Python's startup site module owns this name; load the local site explicitly.
import importlib.util
spec=importlib.util.spec_from_file_location('manufactured_site',HERE/'site.py');SITE=importlib.util.module_from_spec(spec);spec.loader.exec_module(SITE)


def counts(obs):
    bpy.context.view_layer.update();triangles=0;unique=0;seen=set();materials=set();lo=np.full(3,1e10);hi=-lo;parts={}
    for o in obs:
        if o.type!='MESH' or not len(o.data.vertices):continue
        o.data.calc_loop_triangles();n=len(o.data.loop_triangles);triangles+=n
        if o.data not in seen:unique+=n;seen.add(o.data)
        part=o.get('component',o.parent.name if o.parent else o.name);parts[part]=parts.get(part,0)+n
        if not o.data.materials:raise ValueError(('Unassigned mesh material',o.name,len(o.data.vertices),len(o.data.polygons)))
        for f in o.data.polygons:materials.add(o.data.materials[f.material_index].name)
        v=np.empty(len(o.data.vertices)*3);o.data.vertices.foreach_get('co',v);v=v.reshape(-1,3);xf=np.array(o.matrix_world);v=v@xf[:3,:3].T+xf[:3,3]
        lo=np.minimum(lo,v.min(0));hi=np.maximum(hi,v.max(0))
    return dict(triangles=triangles,unique_triangles=unique,unique_meshes=len(seen),materials=len(materials),bounds_min=lo.tolist(),bounds_max=hi.tolist(),size_m=(hi-lo).tolist(),parts=parts)


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.unit_settings.system='METRIC'


def canonical_images():
    global _IMAGE_CACHE
    if _IMAGE_CACHE is not None:return _IMAGE_CACHE
    known={}
    for family in ('ground','fences','mailbox','trash-cart','patio-set','gas-grill','houses','trees','shrubs','trailer-park'):
        for q in (ROOT/family).rglob('*.png'):
            if 'ship' in q.parts:known[hashlib.sha256(q.read_bytes()).hexdigest()]=q
    for q in Path('build/library').rglob('*.png'):
        if 'ship' in q.parts:known[hashlib.sha256(q.read_bytes()).hexdigest()]=q.resolve()
    q=Path('textures/checkpoint/T_ManufacturedForm.png');known[hashlib.sha256(q.read_bytes()).hexdigest()]=q.resolve()
    _IMAGE_CACHE=known;return known


def publish(stem,root,plan=None):
    report=counts(list(bpy.context.scene.objects));report['stage']='look-dev checkpoint / baked shared manufacture and causal mesh colors / no final docs'
    report['plan']=plan;report['root']=root.name
    report['assemblies']={o.name:counts([o,*o.children_recursive]) for o in bpy.context.scene.objects if o.type=='EMPTY' and ('home_spec' in o or o.get('lot_record'))}
    report['components']={o.name:counts([o,*o.children_recursive]) for o in root.children if o.type=='EMPTY' and o.get('asset_set')=='Manufactured'}
    consolidate();source=Path('build')/(stem+'.blend');source.parent.mkdir(exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(source.resolve()))
    path=Path('export')/(stem+'.gltf');path.parent.mkdir(exist_ok=True)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLTF_SEPARATE',export_texture_dir='shared',use_selection=True,
        export_yup=True,export_extras=True,export_animations=False,export_tangents=False,export_attributes=True,
        export_all_vertex_colors=False,export_image_format='AUTO')
    doc=json.loads(path.read_text());known=canonical_images()
    # Hash-identify original image files; preserve one canonical URI per image
    # across the entire town. No inherited delivery file is opened for writing.
    for im in doc.get('images',[]):
        q=path.parent/im['uri'];digest=hashlib.sha256(q.read_bytes()).hexdigest()
        if digest in known:im['uri']=Path(os.path.relpath(known[digest],path.parent)).as_posix()
    # Vertex tint belongs only to materials explicitly using it. The stock
    # glTF multiplier must not darken untinted native primitives accidentally.
    for mesh in doc['meshes']:
        for primitive in mesh['primitives']:
            ma=doc['materials'][primitive['material']]
            if ma.get('extras',{}).get('tiling_vertex_tint') is False:primitive['attributes'].pop('COLOR_0',None)
    path.write_text(json.dumps(doc,separators=(',',':'))+'\n')
    report['triangles_export']=sum(sum(doc['accessors'][pr['indices']]['count']//3 for pr in doc['meshes'][n['mesh']]['primitives']) for n in doc['nodes'] if 'mesh' in n)
    report['unique_export_triangles']=sum(doc['accessors'][pr['indices']]['count']//3 for mesh in doc['meshes'] for pr in mesh['primitives'])
    if plan and 'lots' in plan:report['gross_acres']=plan['size'][0]*plan['size'][1]/4046.8564224;report['homes_per_acre']=len(plan['lots'])/report['gross_acres']
    assert report['triangles_export']==report['triangles'],(stem,report['triangles_export'],report['triangles'])
    report['geometry_bytes']=path.stat().st_size+sum((path.parent/b['uri']).stat().st_size for b in doc['buffers'])
    report['images']=[dict(uri=im['uri'],bytes=(path.parent/im['uri']).stat().st_size,sha256=hashlib.sha256((path.parent/im['uri']).read_bytes()).hexdigest()) for im in doc.get('images',[])]
    report['pivots']=[dict(name=n['name'],**n['extras']) for n in doc['nodes'] if 'pivot_axis' in n.get('extras',{})]
    report['sockets']=sum('socket_kind' in n.get('extras',{}) for n in doc['nodes'])
    from inspection import mirror
    embedded=mirror(path);report['inspection_glb']=str(embedded);report['inspection_glb_bytes']=embedded.stat().st_size
    path.with_suffix('.json').write_text(json.dumps(report,indent=2))
    print('PUBLISHED',stem,report['triangles'],report['geometry_bytes'],flush=True);return report


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='build/family.blend');p.add_argument('--old-seed',type=int,default=101);p.add_argument('--new-seed',type=int,default=202);p.add_argument('--rows',type=int,default=9);p.add_argument('--only',default='all');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);report={}
    definitions=[('SingleWide-120',home(120,'1972',12,60)),('SingleWide-147',home(147,'1984',14,70)),('SingleWide-168',home(168,'1984',16,80)),
                 ('DoubleWide-245',home(245,'1996',24,52)),('DoubleWide-228',home(228,'1996',28,60)),('DoubleWide-326',home(326,'1996',32,64))]
    for stem,spec in definitions:
        if a.only not in ('all',stem):continue
        reset();obj=homes.build(spec,stem);report[stem]=publish(stem,obj.root,spec)
    if a.only in ('all','HomeForms'):
        reset();sheet=Assembly('HomeForms')
        from geometry import label
        for j,(stem,spec) in enumerate(definitions):
            obj=homes.build(spec,stem);place(obj.root,((j%3-1)*29,(j//3)*21,0),0,sheet.root)
            label(sheet,f'{spec["nominal_ft"][0]} x {spec["nominal_ft"][1]} ft / {spec["era"]}',((j%3-1)*29,(j//3)*21-spec['width']/2-1.0,.15),.70,(.6,.6,.5))
        report['HomeForms']=publish('HomeForms',sheet.root)
    factories=dict(Deck=lambda:addons.deck(),Carport=addons.carport,UtilityService=addons.utility,PropaneBottles=addons.propane,Condenser=addons.conditioner,
                   WindowAC=lambda:addons.conditioner(kind='window'),SatelliteDish=addons.dish,AddedRoom=addons.room,Household=addons.dressing,EntranceSign=addons.sign,
                   SupportFrame=lambda:homes.build(home(120,'1972',12,60),'SupportFrame',support_only=True))
    for stem,fn in factories.items():
        if a.only not in ('all',stem):continue
        reset();obj=fn();report[stem]=publish(stem,obj.root)
    if a.only in ('all','Modules'):
        reset();sheet=Assembly('ManufacturedModules')
        for j,(stem,fn) in enumerate(list(factories.items())[:-1]):
            obj=fn();place(obj.root,((j%5-2)*8,(j//5)*9,0),0,sheet.root)
            from geometry import label
            label(sheet,stem,((j%5-2)*8,(j//5)*9-3.0,.10),.40,(.6,.6,.5))
        report['Modules']=publish('Modules',sheet.root)
    for seed,kind in ((a.old_seed,'old'),(a.new_seed,'new')):
        stem='Park-'+str(seed)
        if a.only not in ('all',stem):continue
        reset();plan=park(seed,kind,a.rows);obj=SITE.build(plan);report[stem]=publish(stem,obj.root,plan)
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
    if a.only=='all':Path('build/family.json').write_text(json.dumps(report,indent=2))
    used={(p.parent/i['uri']).resolve() for p in Path('export').glob('*.gltf') for i in json.loads(p.read_text()).get('images',[])}
    for q in Path('export/shared').glob('*.png'):
        if q.resolve() not in used:q.unlink()

if __name__=='__main__':main()
