"""Form and construction checkpoint: no baked look-dev or final docs."""
import argparse,json,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).resolve().parent))
import forms as F
import pieces as P

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('build/StreetFurniture.blend'));a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.unit_settings.system='METRIC';F.init();roots=[];records={}
    jobs=[('BusStop',P.stop,{}),('Shelter',P.shelter,{'seed':11}),('Bench',P.bench,{}),('BikeRack',P.rack,{}),('BikeRackRow',P.rack,{'count':4}),('NewsDaily',P.newspaper,{'kind':0}),('NewsPedestal',P.newspaper,{'kind':1}),('NewsWeekly',P.newspaper,{'kind':2}),('CollectionBox',P.collection,{}),('MeterSingle',P.meter,{}),('MeterTwin',P.meter,{'twin':True}),('Litter',P.receptacle,{}),('Recycling',P.receptacle,{'recycle':True}),('ShelterMissingPanel',P.shelter,{'seed':12})]
    for i,(name,build,kw) in enumerate(jobs):
        rt=F.root(name);build(rt,**kw);records[name]=F.consolidate(rt);rt.location=(i%5*5.0,i//5*4.3,0);roots.append(rt)
    # Row prefab consists of linked modules; never spend another texture set.
    row=F.root('NewsRow',(15,8.6,0));sources=[roots[i] for i in (5,6,7)]
    for j,source in enumerate(sources):
        copies={o:o.copy() for o in [source,*source.children_recursive]}
        for o,cp in copies.items():
            bpy.context.collection.objects.link(cp);cp.parent=copies.get(o.parent,row);cp.matrix_basis=o.matrix_basis.copy();cp.name='Row_'+o.name
        copies[source].location=((j-1)*.72,0,0)
    row['module_kind']='Row prefab / three independent boxes';records[row.name]=dict(triangles=sum(records[s.name]['triangles'] for s in sources),materials=['StreetFurniture_FormSheet','StreetFurniture_Glazing'],member_count=3);roots.append(row)
    a.out.parent.mkdir(parents=True,exist_ok=True);bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(a.out.resolve()))
    out=Path('export/StreetFurniture.gltf');out.parent.mkdir(exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=str(out.resolve()),export_format='GLTF_SEPARATE',export_texture_dir='textures',export_extras=True,export_animations=False,export_tangents=False)
    for rt in roots:
        bpy.ops.object.select_all(action='DESELECT')
        for ob in [rt,*rt.children_recursive]:ob.select_set(True)
        old=rt.location.copy();rt.location=(0,0,0)
        bpy.ops.export_scene.gltf(filepath=str(out.with_name(rt.name+'.gltf').resolve()),use_selection=True,export_format='GLTF_SEPARATE',export_texture_dir='textures',export_extras=True,export_animations=False,export_tangents=False)
        rt.location=old
    Path('build/manifest.json').write_text(json.dumps(dict(stage='form/construction checkpoint, quick shared palette, no baked wear',pieces=records,texture_size=[2048,2048],total_triangles=sum(r['triangles'] for r in records.values())),indent=2))
    for k,v in records.items():print('PIECE',k,v['triangles'],'triangles')
if __name__=='__main__':main()
