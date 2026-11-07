"""R5 measurements on constructed game surfaces, not design constants."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from sedan_check import bounds,points,mesh_tree,plane_cut


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.source).resolve();bpy.ops.wm.open_mainfile(filepath=str(src));bpy.context.view_layer.update()
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')=='Sedan']
    skin=[o for o in obs if o.get('part_category') in ['body','doors','glass','pillars','fascia']];tree=mesh_tree(skin+[o for o in obs if o.get('part_category')=='openings'])
    backlight=bpy.data.objects['Backlight'];roles=backlight.data.attributes['sheet_role']
    outer={i for face in backlight.data.polygons if roles.data[face.index].value==0 for i in face.vertices}
    glass=[backlight.matrix_world@backlight.data.vertices[i].co for i in sorted(outer)];corners={}
    top_y=min(p.y for p in glass);base_y=max(p.y for p in glass)
    for name,sign in [('L',-1),('R',1)]:
        # Find corners from the actual outer sheet extrema, independently of
        # the authored glass-cut equation and the inward laminate.
        corners[name]={key:max((p for p in glass if abs(p.y-y)<.015),key=lambda p:sign*p.x)
                       for key,y in [('top',top_y),('base',base_y)]}
    widths={key:corners['R'][key].x-corners['L'][key].x for key in ['top','base']}
    sails=[]
    for name,sign in [('L',-1),('R',1)]:
        q=corners[name]['base'];z=q.z-.080
        hip=tree.ray_cast(Vector((sign*2,q.y,z)),Vector((-sign,0,0)),4)[0]
        sails.append(dict(side=name,glass_base_m=list(q),hip_m=list(hip),transverse_width_m=abs(hip.x-q.x),beltline_z_m=z))
    lamps={}
    for o in obs:
        if not o.name.startswith('Taillamp opening') or o.get('lamp_piece')!='quarter':continue
        raw=list(o['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];nu,nv=o['form_columns'],o['form_rows']
        columns=[(ps[i],ps[(nv-1)*nu+i]) for i in range(nu)]
        corner=[(b-a).length for a,b in columns if .78<=abs((a.x+b.x)/2)<=.88]
        mid=ps[(nv//2)*nu:(nv//2+1)*nu]
        lamps[o.name]=dict(corner_max_height_m=max(corner),corner_min_height_m=min(corner),forward_taper_height_m=(columns[-1][1]-columns[-1][0]).length,quarter_return_m=max(p.y for p in mid if abs(p.x)>.78)-mid[-1].y)
    pocket=bpy.data.objects['Plate pocket opening'];raw=list(pocket['well_mouth_samples']);mouth=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    plate_ob=bpy.data.objects['Plate blank 12x6 inch'];plate=bounds([plate_ob]);mouth_center=sum(mouth,Vector())/len(mouth)
    # Attachment applies the plate's tilt to its vertices. Measure its actual
    # straight box edges, rather than mistaking the tilted AABB for its size.
    edge_lengths=sorted((plate_ob.matrix_world.to_3x3()@(plate_ob.data.vertices[e.vertices[1]].co-plate_ob.data.vertices[e.vertices[0]].co)).length for e in plate_ob.data.edges)
    normal_matrix=plate_ob.matrix_world.to_3x3().inverted().transposed()
    n=max((normal_matrix@f.normal for f in plate_ob.data.polygons),key=lambda n:n.y).normalized()
    pp,_,_,distance=mesh_tree([plate_ob]).ray_cast(mouth_center+n*.020,-n,.100)
    plate_record=dict(mouth_width_m=max(p.x for p in mouth)-min(p.x for p in mouth),mouth_height_m=max(p.z for p in mouth)-min(p.z for p in mouth),mouth_to_plate_depth_m=distance-.020 if pp is not None else None,plate_depth_ray_m=[list(mouth_center),list(pp) if pp is not None else None],plate_bounds_m=plate,plate_edge_dimensions_m=dict(width=edge_lengths[-1],height=edge_lengths[len(edge_lengths)//2],thickness=edge_lengths[0]),top_lamp_bounds_m=bounds([bpy.data.objects['Plate illumination housing']]))
    mirrors={o.name:bounds([o]) for o in obs if o.name.startswith('Mirror housing')};panes={o.name:bounds([o]) for o in obs if o.name.startswith('Mirror pane')}
    mirror_profile=[]
    canopy=mesh_tree(skin)
    for o in obs:
        if not o.name.startswith('Mirror housing'):continue
        differences=[]
        for p0 in points(o):
            top=canopy.ray_cast(Vector((0,p0.y,3)),Vector((0,0,-1)),4)[0]
            if top is not None:differences.append(p0.z-top.z)
        mirror_profile.append(dict(name=o.name,maximum_above_centerline_canopy_m=max(differences)))
    closures={}
    for o in obs:
        if o.get('part_category')!='closure' or o.name=='Form cavity closure':continue
        bb=bounds([o]);tires=[bounds([t]) for t in obs if t.name.startswith('Tire_')]
        sep=min(max(t['min'][1]-bb['max'][1],bb['min'][1]-t['max'][1]) for t in tires)
        closures[o.name]=dict(bounds_m=bb,minimum_tire_y_separation_m=sep)
    end_tree=mesh_tree(skin+[o for o in obs if o.get('part_category')=='openings' or o.name=='Rear form underbody closure'])
    def rear(x,z):return end_tree.ray_cast(Vector((x,4,z)),Vector((0,-1,0)),5)[0]
    profile=[]
    for z in [.220,.270,.320,.370,.390,.420]:
        q=rear(0,z);profile.append(dict(z_m=z,surface_m=list(q) if q is not None else None))
    bottom=[]
    for x in [0,.2,.4,.6,.8]:
        cut=plane_cut([bpy.data.objects['Rear molded fascia']],x,axis=0)
        candidates=[p for segment in cut for p in segment if p[0]>2.05]
        q=min(candidates,key=lambda p:p[1])
        bottom.append(dict(x_m=x,lowest_painted_surface_yz_m=q))
    bumper=dict(plan_at_450mm_m=[list(rear(x,.450)) for x in [0,.2,.4,.6,.8]],lower_center_profile=profile,
        lower_turn_over_150mm_m=rear(0,.420).y-rear(0,.270).y,
        lower_painted_edge_sections=bottom,
        lower_scope='Actual silhouette, including the rolled black cavity closure below the painted sheet. Null rays preserve physical reveal gaps; underbody detail remains deferred.')
    report=dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),glass_widths_m=widths,glass_corners_m={n:{k:list(v) for k,v in r.items()} for n,r in corners.items()},sails=sails,taillamps=lamps,plate=plate_record,mirrors=mirrors,mirror_panes=panes,mirror_profile=mirror_profile,underbody_end_closures=closures,bumper=bumper)
    errors=[]
    if not 1.1<=widths['base']<=1.3:errors.append('Backlight base width')
    if not 1.1<=widths['top']<=1.35:errors.append('Backlight top width')
    for name,r in lamps.items():
        if not .120<=r['corner_max_height_m']<=.180:errors.append(name+' corner height')
        if not .250<=r['quarter_return_m']<=.450:errors.append(name+' quarter return')
    if abs(plate_record['mouth_width_m']-.320)>.008 or abs(plate_record['mouth_height_m']-.170)>.005:errors.append('Plate mouth')
    if plate_record['mouth_to_plate_depth_m'] is None or not .020<=plate_record['mouth_to_plate_depth_m']<=.030:errors.append('Plate depth')
    if abs(plate_record['plate_edge_dimensions_m']['width']-.3048)>.00001 or abs(plate_record['plate_edge_dimensions_m']['height']-.1524)>.00001:errors.append('12 by 6 inch plate geometry')
    for n,r in mirrors.items():
        if not all(lo<=v<=hi for v,lo,hi in zip(r['size'],[.230,.100,.140],[.270,.130,.170])):errors.append(n+' size')
        if not .90<=r['min'][2]<=.97:errors.append(n+' beltline position')
    if any(r['size'][1]>.0041 for r in panes.values()):errors.append('Mirror glass rear face not planar')
    if any(r['maximum_above_centerline_canopy_m']>0 for r in mirror_profile):errors.append('Mirror projects above canopy silhouette')
    if any(r['minimum_tire_y_separation_m']<=0 for r in closures.values()):errors.append('Underbody closure overlaps wheel Y bounds')
    if not all(a[1]>b[1] for a,b in zip(bumper['plan_at_450mm_m'],bumper['plan_at_450mm_m'][1:])):errors.append('Bumper not convex across')
    plan=bumper['plan_at_450mm_m'];slopes=[b[1]-a[1] for a,b in zip(plan,plan[1:])]
    if not all(a>b for a,b in zip(slopes,slopes[1:])):errors.append('Bumper plan curvature reverses')
    if bumper['lower_turn_over_150mm_m']<=0:errors.append('Lower bumper does not turn under')
    if sum(r['surface_m'] is not None for r in profile)<4:errors.append('Insufficient lower bumper profile coverage')
    report.update(passed=not errors,errors=errors);Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
    if errors:raise AssertionError(errors)
if __name__=='__main__':main()
