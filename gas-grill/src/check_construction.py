"""Measured header alignment, wheel planes, cup supports, drain and open envelope."""
import argparse,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.motion import owned,surface


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));bpy.context.view_layer.update()
    objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o]
    def named(prefix):return next(o for o in objects if o.name.startswith(prefix))
    def bbox(obs):
        points=[o.matrix_world@v.co for o in obs for v in o.data.vertices]
        lo=[min(v[k] for v in points) for k in range(3)];hi=[max(v[k] for v in points) for k in range(3)]
        return dict(min=lo,max=hi,size=[hi[k]-lo[k] for k in range(3)])
    lid=bpy.data.objects['Lid'];center=lid.matrix_world.translation.x
    badge=bbox([named('Badge stamped backing')]);gauge=bbox([named('Thermometer rolled bezel')])
    header={name:dict(center_x_m=(box['min'][0]+box['max'][0])/2,lid_center_error_m=abs((box['min'][0]+box['max'][0])/2-center)) for name,box in [('badge',badge),('thermometer',gauge)]}
    header['vertical_gap_m']=gauge['min'][2]-badge['max'][2]
    assert max(header[k]['lid_center_error_m'] for k in ('badge','thermometer'))<1e-6
    assert header['vertical_gap_m']>.005,'Header elements overlap in front projection'
    legs=bbox([o for o in objects if o.name.startswith('Formed cart leg')]);wheels={}
    for name in ('Wheel_Front','Wheel_Back'):
        box=bbox([o for o in objects if owned(o,bpy.data.objects[name])]);front=name.endswith('Front')
        gap=legs['min'][1]-box['max'][1] if front else box['min'][1]-legs['max'][1]
        assert gap>.001
        wheels[name]=dict(bounds_m=box,leg_axial_clearance_m=gap,rotation_invariant='Y rotation preserves every axial coordinate')
    tray=named('Removable stamped grease tray');cup=named('Foil grease catch cup');tray_surface=surface(tray);cup_surface=surface(cup)
    supports={}
    for ob in objects:
        if not ob.name.startswith('Catch cup folded hanger'):continue
        points=surface(ob)['points'];samples=list(points)
        ob.data.calc_loop_triangles()
        for tri in ob.data.loop_triangles:
            v0,v1,v2=[ob.matrix_world@ob.data.vertices[i].co for i in tri.vertices]
            for i in range(9):
                for j in range(9-i):samples.append(v0+(v1-v0)*(i/8)+(v2-v0)*(j/8))
        top=min(tray_surface['tree'].find_nearest(v)[3] for v in samples)
        lower=min(cup_surface['tree'].find_nearest(v)[3] for v in samples)
        print('SUPPORT_GAPS',ob.name,top,lower,flush=True)
        assert top<.0005 and lower<.0005,'Cup hanger does not bridge tray and cup'
        supports[ob.name]=dict(tray_surface_gap_m=top,cup_surface_gap_m=lower)
    assert len(supports)==2
    origin=bpy.data.objects['Grill'].matrix_world@Vector((0,-.030,.675))
    assert tray_surface['tree'].ray_cast(origin,Vector((0,0,-1)),.06)[0] is None,'Drain opening is capped'
    closed=bbox(objects);rest=lid.matrix_basis.copy();lid.matrix_basis=rest@Matrix.Rotation(math.radians(-104),4,'X');bpy.context.view_layer.update()
    opened=bbox(objects);lid.matrix_basis=rest;bpy.context.view_layer.update()
    result=dict(passed=True,header=header,lid_center_x_m=center,wheels=wheels,cup_supports=supports,drain_clear=True,closed_bounds_m=closed,open_bounds_m=opened)
    Path(a.out).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':main()
