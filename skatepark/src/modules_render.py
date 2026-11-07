"""Baked external-module sheet, including assembled bowl sector sets."""
import sys,math,json
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from render import setup
from external import bundle

def main():
    source=Path('export/final/SkateparkPieces.gltf');bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
    roots=[o for o in bpy.context.scene.objects if not o.parent];singles=[r for r in roots if 'Bowl_' not in r.name]
    for i,rt in enumerate(singles):rt.location=(i%5*12,i//5*13,0)
    for rt in roots:
        if rt.name.startswith('Bowl_'):rt.location=(10,58,0)
        elif rt.name.startswith('SteelBowl_'):rt.location=(37,58,0)
    cam=setup(40);cam.location=(50,-40,80);cam.rotation_euler=(Vector((24,28,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=42
    sc=bpy.context.scene;sc.view_settings.exposure=-.25;sc.render.resolution_x=1600;sc.render.resolution_y=1400;sc.render.resolution_percentage=100
    out=Path('renders/final/modules.png');out.parent.mkdir(parents=True,exist_ok=True);sc.render.filepath=str(out.resolve());bpy.ops.render.render(write_still=True)
    out.with_suffix('.json').write_text(json.dumps(dict(source=str(source),bundle_sha256=bundle(source),roots=len(roots),engine='CYCLES',scope='Fresh imported external modules; layout offsets for inspection only'),indent=2))
if __name__=='__main__':main()
