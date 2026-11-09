"""Supplementary source pairs under the exported pairs' measured light/cameras.

Primary checkpoint evidence always imports the exports. These separate views
test whether consolidation/color encoding lost the newly authored weather.
"""
import hashlib,json,sys
from pathlib import Path
from types import SimpleNamespace
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from render import light,camera,context_signature
from sites import build_site
from town import context


def main():
    family=json.loads(Path('build/family.json').read_text());matches=json.loads(Path('build/matched-cameras.json').read_text());out=Path('renders/source-matches');out.mkdir(parents=True,exist_ok=True)
    for name,row in matches.items():
        seed=row['seed'];p=family['Civic-'+str(seed)]['plan'];source=Path('build',f'Civic-{seed}-source.blend')
        bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));roots=[o for o in bpy.context.scene.objects if o.parent is None and o.get('static_root')];assert len(roots)==1
        if row.get('building_only'):
            roots[0].location+=Vector(p['origin_offset_m'])+Vector((-6,0,0))
        else:
            from plans import site
            sp=site(seed);sp['building']=p;build_site(sp,SimpleNamespace(root=roots[0]),Vector(p['origin_offset_m']))
        context(101 if row.get('building_only') else seed)
        # Reuse the actual exported frame's recorded light, not an estimate
        # reconstructed from a different version of the presentation script.
        receipt=json.loads(Path('renders/matches',name+'.json').read_text());lighting=receipt['lighting']
        light();sc=bpy.context.scene;sun=bpy.data.objects['Low front raking sun'];sun.rotation_euler=lighting['sun_rotation'];sun.data.energy=lighting['sun_energy'];sun.data.angle=lighting['sun_angle']
        sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=lighting['sky_strength'];sc.view_settings.exposure=receipt['exposure']
        shot=row['shot'];spec=(shot['location'],shot['target'],shot['lens']);cam=camera(spec,1400);cam.rotation_euler.rotate_axis('Z',shot['roll']);sc.render.resolution_y=round(1400/shot['aspect']);sc.cycles.samples=32
        sc.render.image_settings.file_format='PNG';sc.render.filepath=str((out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        result=dict(stage='source; supplementary, never the delivery evidence',source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),camera=spec,width=1400,lighting=lighting,export_pair=str(Path('renders/matches',name+'.png')),context_recipe_sha256=context_signature())
        (out/(name+'.json')).write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
