"""Round-two measurements of built triangles, independent of design inputs.

Plan setbacks are envelope samples through actual meshes at 5 mm height steps,
so they can be compared with a reference top view. They are not the section
function or its prescribed turn radius. Closed/recessed optical forms remain
included in that envelope, while wheels and mirror housings are excluded.
"""
import math
from mathutils import Vector
from mathutils.kdtree import KDTree
from suv_measure import points,bounds,mesh_tree,plane_cut


def measure(obs):
    by_name={o.name:o for o in obs};result={}
    exterior=[o for o in obs if o.get('part_category') in ['body','doors','fascia','cladding','openings']]
    tree=mesh_tree(exterior);plans={}
    for front in [True,False]:
        samples=[]
        for x in [0,.40,.65,.70,.75,.80,.85]:
            hits=[tree.ray_cast(Vector((x,-4 if front else 4,.25+.005*i)),Vector((0,1 if front else -1,0)),5)[0] for i in range(220)]
            hits=[q for q in hits if q is not None]
            p=(min if front else max)(hits,key=lambda q:q.y);samples.append(p)
        center=samples[0];rows=[dict(halfwidth_m=p.x,point_m=list(p),setback_m=abs(p.y-center.y)) for p in samples]
        aa,bb,cc=[Vector((p.x,p.y,0)) for p in samples[2:5]];area=(bb-aa).cross(cc-aa).length/2
        radius=(bb-aa).length*(cc-bb).length*(aa-cc).length/(4*area)
        plans['front' if front else 'rear']=dict(samples=rows,corner_setback_at_800mm_m=rows[5]['setback_m'],three_point_xy_envelope_radius_m=radius,
            method='First outward hit at each height; most forward/aft hit over Z 0.250..1.345 m, every 5 mm; physical source meshes, not a prescribed radius')
    result['plan']=plans
    lowers={}
    for end in ['Front','Rear']:
        ob=by_name[end+' lower bumper cladding'];rows=[]
        for x in [0,.40,.70,.78]:
            band=[Vector((x,y,z)) for segment in plane_cut([ob],x,axis=0) for y,z in segment]
            if not band:continue
            lo=min(band,key=lambda p:p.z);hi=max(band,key=lambda p:p.z)
            rows.append(dict(halfwidth_m=x,bottom_m=list(lo),top_m=list(hi),height_m=hi.z-lo.z))
        lowers[end.lower()]=rows
    hood=points(by_name['Hood outer']);lead=min((p for p in hood if abs(p.x)<.025),key=lambda p:p.y)
    lowers['front_center_share_hood_to_ground']=lowers['front'][0]['height_m']/lead.z
    result['lower_fascias']=lowers
    hood_tree=mesh_tree([by_name['Hood outer']]);hood_sections=[]
    for y in [-2.,-1.7,-1.4]:
        row=[]
        for x in [0,.3,.5,.6,.7,.78,.83]:
            p=hood_tree.ray_cast(Vector((x,y,2)),Vector((0,0,-1)),2)[0]
            if p is not None:row.append(list(p))
        hood_sections.append(dict(y_m=y,points_m=row))
    result['hood_cross_sections']=hood_sections

    mirror={}
    for side in ['L','R']:
        housing=by_name['Mirror housing_'+side];pane=by_name['Mirror pane_'+side];sail=by_name['Mirror sail_'+side]
        hh=bounds([housing]);pp=points(pane)
        mirror[side]=dict(housing_m=hh,center_m=[(a+b)/2 for a,b in zip(hh['min'],hh['max'])],pane_y_span_m=max(p.y for p in pp)-min(p.y for p in pp),sail_m=bounds([sail]),parent=housing.parent.name)
    mirror['width_across_both_m']=bounds([by_name['Mirror housing_'+s] for s in ['L','R']])['size'][0]
    result['mirrors']=mirror
    lamps={}
    for ob in obs:
        if not ob.name.startswith(('Headlamp opening','Taillamp opening')) or 'aperture_samples' not in ob:continue
        raw=list(ob['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];nu,nv=ob['form_columns'],ob['form_rows']
        columns=[]
        for i in range(nu):
            a,c=ps[i],ps[(nv-1)*nu+i];columns.append(dict(x_m=(a.x+c.x)/2,height_z_m=abs(c.z-a.z),height_surface_m=(c-a).length))
        lamps[ob.name]=dict(columns=columns,maximum_z_height_m=max(r['height_z_m'] for r in columns),corner_height_at_800mm_m=min(columns,key=lambda r:abs(abs(r['x_m'])-.8))['height_z_m'])
    result['lamps']=lamps
    raw=list(by_name['Upper grille opening']['well_mouth_samples']);mouth=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    kd=KDTree(len(mouth))
    for i,p in enumerate(mouth):kd.insert(p,i)
    kd.balance();gaps={}
    for side in [-1,1]:
        ob=by_name['Headlamp opening'+str(side)];ps=points(ob)
        gap,p,q=min((kd.find(p)[2],p,kd.find(p)[0]) for p in ps)
        gaps[str(side)]=dict(gap_m=gap,points_m=[list(p),list(q)],scope='Shortest actual lens-to-grille-mouth vertex distance; surrounding lip further occupies the painted interval')
    result['lamp_grille_gap']=gaps
    roof=mesh_tree([by_name['Roof']]);rails={}
    for side in ['L','R']:
        ps=points(by_name['Roof rail_'+side]);samples=[]
        for y in [.40,.70,1.05,1.35]:
            near=sorted(ps,key=lambda p:abs(p.y-y))[:8];top=max(near,key=lambda p:p.z);hit=roof.ray_cast(Vector((top.x,top.y,3)),Vector((0,0,-1)),3)[0]
            if hit is not None:samples.append(dict(rail_top_m=list(top),roof_m=list(hit),top_above_roof_m=top.z-hit.z))
        rails[side]=samples
    result['rails']=rails
    spoiler=by_name['Liftgate spoiler'];ss=points(spoiler);roots=[]
    for i in range(0,len(ss),6):
        q=ss[i];hit=roof.ray_cast(Vector((q.x,q.y,3)),Vector((0,0,-1)),3)[0]
        if hit is not None:roots.append(q.z-hit.z)
    result['spoiler_root']=dict(minimum_signed_gap_m=min(roots),maximum_signed_gap_m=max(roots),samples=len(roots),scope='Actual first vertices of the authored closed cross sections against the roof; negative means seated overlap')
    return result
