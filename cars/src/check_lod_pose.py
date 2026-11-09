"""Same-camera near LOD poses, using the delivered pivots and family supports.

This is sampled appearance/membership evidence, not a swept-clearance test.
Run serially in Blender through kit/with_gpu.sh, with --config and --body.
"""
import argparse
import importlib
import json
import math
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Matrix
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.lod import configuration,image_limits
from kit.lod_io import Document,digest
from kit.lod_render import setup,compare


def pose(body):
    changes={}
    for ob in bpy.context.scene.objects:
        if not (ob.name.startswith(('Door_','Steer_','Wheel_')) or
                ob.name in ('Hood','Trunk','Liftgate')):
            continue
        if 'pivot_axis' not in ob or 'range_degrees' not in ob:
            continue
        axis=ob['pivot_axis']
        if axis=='CUSTOM':axis=tuple(ob['hinge_axis_vehicle'])
        bounds=list(ob['range_degrees'])
        angle=max(bounds,key=abs)*.8
        if ob.name.startswith('Wheel_'):angle=55
        ob.matrix_basis=ob.matrix_basis@Matrix.Rotation(math.radians(angle),4,axis)
        changes[ob.name]=dict(axis=list(axis) if not isinstance(axis,str) else axis,degrees=angle)
    required={'Door_'+c for c in ('FL','FR','RL','RR')} | {'Wheel_'+c for c in ('FL','FR','RL','RR')}
    required |= {'Hood','Steer_FL','Steer_FR','Trunk' if body=='sedan' else 'Liftgate'}
    if not required<=changes.keys():raise ValueError('Missing posed pivots: '+str(required-changes.keys()))
    if body=='suv':
        importlib.import_module('suv_mechanics').update_supports()
    else:
        importlib.import_module(body+'_lookdev').supports()
    bpy.context.view_layer.update()
    return changes


def check(config,body):
    cfg,root,source,out=configuration(config)
    manifest=json.loads((out/'manifest.json').read_text())
    before=Document(source).dependencies()
    dest=root/cfg.get('renders','renders/lod')/'posed'
    dest.mkdir(parents=True,exist_ok=True)
    bounds=Document(source).bounds()
    rows=[]
    for level in manifest['levels'][1:]:
        if level.get('proxy'):continue
        path=out/level['path']
        for azimuth in (55,145):
            images=[];poses=[]
            for label,model in [('reference',source),('level',path)]:
                sc=setup(model,bounds,azimuth,level['distance_m'],samples=cfg.get('render_samples',512),
                         elevation=15,factory_paint=cfg.get('factory_paint',False))
                poses.append(pose(body))
                png=dest/f'LOD{level["level"]}-{azimuth}-{label}.png'
                sc.render.filepath=str(png)
                bpy.ops.render.render(write_still=True)
                images.append(np.asarray(Image.open(png).convert('RGBA'),dtype=np.float32)/255)
            if poses[0]!=poses[1]:raise ValueError('Posed pivot membership changed')
            metrics,delta=compare(*images)
            limits=image_limits(cfg,level['level'])
            passed=all(metrics[k]<=v for k,v in limits.items())
            x0,y0,x1,y1=metrics['bbox'];padding=8
            box=(max(0,x0-padding),max(0,y0-padding),min(1920,x1+padding),min(1080,y1+padding))
            panels=[]
            for pixels in [*images,np.concatenate([np.clip(delta*4,0,1),np.ones((*delta.shape[:2],1))],axis=2)]:
                rgba=Image.fromarray(np.uint8(np.clip(pixels*255+.5,0,255)),'RGBA')
                backdrop=Image.new('RGBA',rgba.size,(46,46,46,255));backdrop.alpha_composite(rgba)
                panels.append(backdrop.convert('RGB').crop(box))
            sheet=Image.new('RGB',(sum(p.width for p in panels),panels[0].height),(46,46,46))
            x=0
            for panel in panels:sheet.paste(panel,(x,0));x+=panel.width
            sheet.save(dest/f'LOD{level["level"]}-{azimuth}-native.jpg',quality=94)
            rows.append(dict(level=level['level'],azimuth=azimuth,passed=passed,limits=limits,
                             metrics=metrics,poses=poses[0]))
    if not rows:raise ValueError('Posed evidence requires at least one near level')
    files={p.name:digest(p) for p in dest.iterdir() if p.suffix in ('.png','.jpg')}
    report=dict(passed=all(r['passed'] for r in rows),comparisons=rows,files=files,
                source_dependencies=before,manifest_sha256=digest(out/'manifest.json'),
                script_sha256=digest(Path(__file__)),
                scope='Sampled posed appearance and matching articulation; not swept clearance')
    helper='suv_mechanics' if body=='suv' else body+'_lookdev'
    report['support_helper_sha256']=digest(Path(sys.modules[helper].__file__))
    (dest/'metrics.json').write_text(json.dumps(report,indent=2)+'\n')
    if Document(source).dependencies()!=before:raise ValueError('Immutable source changed')
    print('POSED LOD',report['passed'],[(r['level'],r['azimuth'],r['metrics']) for r in rows],flush=True)
    if not report['passed']:raise SystemExit(2)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config',required=True)
    p.add_argument('--body',choices=['sedan','suv','hatch'],required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    check(a.config,a.body)
