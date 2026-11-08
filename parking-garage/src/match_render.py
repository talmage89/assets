"""Render comparison specimens, before/after finishes on the same exports."""
import argparse,json,sys
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
from kit import photo_match
from render import render_shot
from light_review import lighting


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stage',default='form');ap.add_argument('--out',type=Path,default=Path('renders/form-matches'));ap.add_argument('--width',type=int,default=1200);ap.add_argument('--samples',type=int,default=24);ap.add_argument('--source-finish',action='store_true');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    calibration=Path('build/lookdev/matches/calibration.json');photo_match.verify(calibration);receipts=[]
    for name,fit in json.loads(calibration.read_text()).items():
        bpy.ops.wm.read_factory_settings(use_empty=True);path=Path(fit['source_form'])
        if a.stage=='lookdev':
            path=Path(f'export/lookdev/comparison-{name}.gltf') if name!='pleasant' else Path('export/lookdev/sites/ParkingGarageLookSite-101.gltf')
        bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
        from mathutils import Vector
        eye=Vector(fit['shot']['location']);hidden=[]
        for root in list(bpy.context.scene.objects):
            if not root.name.startswith(('Parked ','Street parked ')):continue
            if root.parent and root.parent.name.startswith(('Parked ','Street parked ')):continue
            if (root.matrix_world.translation-eye).xy.length<3.5:
                hidden.append(root.name)
                for ob in [root,*root.children_recursive]:ob.hide_render=True
        if a.source_finish:
            from atlas_binding import source_finish
            source_finish()
        lighting(elevation=36 if name!='precast' else 20,azimuth=-120 if name!='pleasant' else 145,interior=name=='precast')
        if name=='precast':bpy.context.scene.view_settings.exposure=1.0
        shot=fit['shot'];shot['aspect']=(fit['crop'][2]-fit['crop'][0])/(fit['crop'][3]-fit['crop'][1]);shot['max_bounces']=12
        r=render_shot(a.out/(name+'.png'),shot,a.width,a.samples,'CYCLES',path)
        r.update(name=name,stage=a.stage,source_finish=a.source_finish,native_rms_px=fit['residual_rms_pixels'],camera_clearance_hidden_context_cars=hidden);receipts.append(r)
        (a.out/'views.json').write_text(json.dumps(receipts,indent=2)+'\n')
    photo_match.compose(calibration,a.out,a.out)
    from kit.contact import review_sheet
    review_sheet([[p] for p in sorted(a.out.glob('*-pair.jpg'))],a.out/'contact.jpg',width=2400,title='Concrete-balanced photographic comparisons / exported geometry')


if __name__=='__main__':main()
