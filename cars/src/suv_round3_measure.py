"""Independent finite sections of the built round-three meshes, in meters."""
import math
import numpy as np
from mathutils import Vector
from suv_fairness import field
from suv_measure import mesh_tree,points,bounds


def measure(obs):
    by={o.name:o for o in obs};body=[o for o in obs if o.get('part_category') in ['body','doors','fascia','pillars']]
    ray=field(body);tree=mesh_tree(body);lines=[]
    for y in [-.390,.215,.720]:
        row={'station_y_m':y}
        for name,guess,window in [('shoulder',1.047+.022*y,.030),('lower',.56+.023*y,.080)]:
            samples=[]
            for z in np.linspace(guess-.075,guess+.075,301):
                hit=ray((2,y,z),(-1,0,0))
                if hit is None:continue
                p,n,part=hit;samples.append(dict(z_m=float(z),point_m=list(p),normal=list(n),angle_degrees=math.degrees(math.atan2(n.z,n.x))))
            # Locate the strongest turn inside the measured neighborhood; no
            # design normal or prescribed angle is substituted for a ray hit.
            candidates=[]
            for a in samples:
                b=min(samples,key=lambda q:abs(q['z_m']-a['z_m']-window))
                if abs(b['z_m']-a['z_m']-window)<.0006 and abs((a['z_m']+b['z_m'])/2-guess)<.035:
                    candidates.append((abs(b['angle_degrees']-a['angle_degrees']),a,b))
            turn,a,b=max(candidates,key=lambda q:q[0]);n0=Vector(a['normal']);n1=Vector(b['normal'])
            central=[s for s in samples if abs(s['z_m']-guess)<.040]
            low,high=central[0]['angle_degrees'],central[-1]['angle_degrees']
            edges=[min(central,key=lambda q:abs(q['angle_degrees']-(low+(high-low)*f))) for f in [.1,.9]]
            row[name]=dict(turn_10_90_width_z_m=edges[1]['z_m']-edges[0]['z_m'],width_z_m=b['z_m']-a['z_m'],surface_chord_m=Vector(a['point_m']).__sub__(Vector(b['point_m'])).length,
                normal_turn_degrees=math.degrees(n0.angle(n1)),endpoints_m=[a['point_m'],b['point_m']],samples=samples)
        lines.append(row)
    spoiler=by['Liftgate spoiler'];ss=points(spoiler);st=mesh_tree([spoiler]);roof=mesh_tree([by['Roof']]);sections=[]
    for x in [0,.40,.60,.70,.745]:
        # Trace the actual outer roof and lower return at a fixed rear chord.
        strip=[p for p in ss if abs(abs(p.x)-x)<.012]
        y=max(p.y for p in strip)-.020 if strip else 2.005
        top=st.ray_cast(Vector((x,y,3)),Vector((0,0,-1)),3)[0];bottom=st.ray_cast(Vector((x,y,1.0)),Vector((0,0,1)),2)[0]
        if top is not None and bottom is not None:sections.append(dict(x_m=x,y_m=y,top_m=list(top),bottom_m=list(bottom),thickness_z_m=top.z-bottom.z))
    # Closed-section roots and deep return are actual vertices, not constants.
    n=int(spoiler['section_vertices']);roots=[];ends=[]
    for i in range(0,len(ss),n):
        section=ss[i:i+n];q=section[0];h=roof.ray_cast(Vector((q.x,q.y,3)),Vector((0,0,-1)),3)[0]
        if h is not None:roots.append(q.z-h.z)
        if abs(q.x)>.69:ends.append(max(p.z for p in section)-min(p.z for p in section))
    pocket=by['Plate pocket opening'];pt=mesh_tree([pocket]);bed=[]
    for x in np.linspace(-.13,.13,7):
        for z in np.linspace(.865,.995,7):
            p=pt.ray_cast(Vector((x,3,z)),Vector((0,-1,0)),2)[0]
            if p is not None:bed.append(list(p))
    bed=np.asarray(bed);center=bed.mean(axis=0);_,_,vv=np.linalg.svd(bed-center);residual=(bed-center)@vv[-1]
    normal=vv[-1] if vv[-1][1]>0 else -vv[-1]
    # Actual skin/rim intersections, not the optical guide (which stands 4 mm
    # proud of the skin). A planar bed under a convex gate has varying edge
    # depths. Report that variation instead of calling the design depth a test.
    gate_ob=by['Liftgate outer'];role=gate_ob.data.attributes['skin_face_role'];uses={}
    for face in gate_ob.data.polygons:
        for vi in face.vertices:uses.setdefault(vi,set()).add(role.data[face.index].value)
    lip=[]
    for v in gate_ob.data.vertices:
        p=gate_ob.matrix_world@v.co
        if {0,2}.issubset(uses[v.index]) and abs(p.x)<.19 and .81<p.z<1.05:lip.append(list(p))
    lip=np.asarray(lip);depths=(lip-center)@normal
    pocket_rim=dict(samples_m=lip.tolist(),width_m=float(np.ptp(lip[:,0])),height_m=float(np.ptp(lip[:,2])),
        edge_depth_min_m=float(depths.min()),edge_depth_max_m=float(depths.max()),
        scope='Actual shared vertices of exposed skin and aperture gauge rim; perpendicular distances to independently fitted actual bed plane. Includes aperture clearance; no missing center skin is invented.')
    gate=mesh_tree([by['Liftgate outer']]);gate_sections=[]
    for z in [.77,.81,1.035,1.09]:
        ps=[]
        for x in [-.60,-.40,-.20,0,.20,.40,.60]:
            h=gate.ray_cast(Vector((x,3,z)),Vector((0,-1,0)),2)[0]
            if h is not None:ps.append(list(h))
        gate_sections.append(dict(z_m=z,points_m=ps))
    mirror={o.name:len(o.data.loop_triangles) for o in obs if o.name.startswith('Mirror housing')}
    return dict(lines=lines,spoiler=dict(sections=sections,end_wrap_heights_m=ends,root_signed_gaps_m=roots,bounds_m=bounds([spoiler])),
        gate=dict(sections=gate_sections,pocket_bed_plane_max_residual_m=float(np.max(np.abs(residual))),pocket_bed_samples=len(bed),pocket_bed_normal=vv[-1].tolist(),pocket_actual_rim=pocket_rim,garnish_bounds_m=bounds([by['Liftgate sculpted garnish']])),mirror_housing_triangles=mirror)
