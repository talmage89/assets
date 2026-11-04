"""Independent H120 checkpoint measures, separate from serialization checks."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from hatch_check import bounds,mesh_tree
from hatch_lookdev import supports
import hatch_spec as S


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--coupled-struts',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve();bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.view_layer.update()
    parts={};categories={};pivots={};errors=[];stroke=[]
    for ob in bpy.context.scene.objects:
        if ob.type=='MESH' and ob.get('asset_set')==S.ASSET_SET:
            ob.data.calc_loop_triangles();n=len(ob.data.loop_triangles);parts[ob.name]=n
            cat=ob['part_category'];categories[cat]=categories.get(cat,0)+n
        if ob.name in ['Door_'+c for c in ['FL','FR','RL','RR']]+['Hood','Liftgate']:
            pivots[ob.name]=dict(position_m=list(ob.matrix_world.translation),axis=list(ob['hinge_axis_vehicle']) if 'hinge_axis_vehicle' in ob else ob.get('pivot_axis'),range_degrees=list(ob['range_degrees']))
    for name in ['Hood','Liftgate']:
        ob=bpy.data.objects[name];rest=ob.matrix_basis.copy();values=[]
        lo,hi=ob['range_degrees']
        for k in range(round(hi-lo)+1):
            angle=lo+k;ob.matrix_basis=rest@Matrix.Rotation(math.radians(angle),4,'X');bpy.context.view_layer.update();supports()
            for member in bpy.context.scene.objects:
                if 'support_target' not in member or not member.name.endswith('sleeve'):continue
                if ('hood' in member.name)!=(name=='Hood'):continue
                d=(bpy.data.objects[member['support_target']].matrix_world.translation-member.matrix_world.translation).length
                length=member['member_length_m'];overlap=2*length-d;bottom=d-length-.020
                values.append(dict(angle=angle,member=member.name,pin_distance_m=d,overlap_m=overlap,bottom_clearance_m=bottom))
        ob.matrix_basis=rest;bpy.context.view_layer.update()
        min_overlap=min(v['overlap_m'] for v in values);min_bottom=min(v['bottom_clearance_m'] for v in values)
        stroke.append(dict(node=name,min_overlap_m=min_overlap,min_bottom_clearance_m=min_bottom,samples=values))
        if min_overlap<.015 or min_bottom<.005:errors.append(name+' gas spring stroke outside physical members')
    underside=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('part_category')=='underbody']
    minimum=min((o.matrix_world@v.co).z for o in underside for v in o.data.vertices)
    if minimum<.139:errors.append('Underbody below 139 mm minimum')
    if bpy.context.scene['quality']=='game' and sum(parts.values())>60000:errors.append('Triangle budget')
    contacts=[]
    def contact(first,second):
        a,b=bpy.data.objects[first],bpy.data.objects[second]
        ta,tb=mesh_tree([a]),mesh_tree([b]);crossings=len(ta.overlap(tb))
        distance=min([tb.find_nearest(a.matrix_world@v.co)[3] for v in a.data.vertices]+[ta.find_nearest(b.matrix_world@v.co)[3] for v in b.data.vertices])
        passed=bool(crossings) or distance<=.0008
        contacts.append(dict(first=first,second=second,triangle_crossings=crossings,nearest_vertex_to_surface_m=distance,passed=passed))
        if not passed:errors.append('Unsupported joint: '+first+' / '+second)
    for code in ['FL','FR','RL','RR']:
        for z in [.60,.85]:
            label=code+str(z)
            contact('H120 moving hinge leaf '+label,'H120 welded hinge reinforcement '+label)
            contact('H120 welded hinge reinforcement '+label,'Door '+code[0]+'_'+code[1])
            contact('H120 fixed hinge leaf '+label,'H120 hinge jamb '+code)
            contact('H120 hinge pin '+label,'H120 fixed hinge leaf '+label)
    for side in ['L','R']:
        contact('H120 hood support '+side+' moving ball bracket','Hood outer')
        contact('H120 hood pedestal '+side,'Wheelwell_F'+side)
        contact('H120 gate support '+side+' moving ball bracket','H120 bonded seal Backlight')
        contact('H120 gate strut jamb '+side,'H120 trunk tub')
        contact('H120 roof hinge pin '+side,'H120 roof hinge bearing ear '+side+str(.027))
    coupled=None
    if a.coupled_struts:
        from hatch_coupled_motion import sweep
        coupled=sweep()
        if not coupled['passed']:errors.append('Coupled gas-spring motion')
    supports();report=dict(stage='source detail/look checkpoint; no UV, bake or GLB certification',passed=not errors,errors=errors,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),triangles=sum(parts.values()),categories=categories,meshes=parts,pivots=pivots,
        min_underbody_clearance_m=minimum,strut_stroke=stroke,contacts=contacts,coupled_springs=coupled,
        wheel_axes={c:dict(axle_world_m=list(bpy.data.objects['Wheel_'+c].matrix_world.translation),spin_axis='local X',range_degrees=[0,360],
            kingpin_axis_vehicle=list(bpy.data.objects['Steer_'+c]['kingpin_axis_vehicle']) if c.startswith('F') else None) for c in ['FL','FR','RL','RR']},
        surface_refinements={o.name:dict(new_samples=o['detail_reflection_samples'],max_projection_m=o['detail_reflection_max_projection_m']) for o in bpy.context.scene.objects if 'detail_reflection_samples' in o},
        texture_plan=dict(size=2048,maps=['BaseColor RGBA','OpenGL +Y Normal','ORM'],compressed_full_mip_MiB=16,allocation='planned, no textures allocated at source checkpoint'))
    Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ['passed','errors','triangles','min_underbody_clearance_m']},indent=2))
    if errors:raise AssertionError(errors)
if __name__=='__main__':main()
