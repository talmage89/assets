"""Actual source construction measurements, distinct from GLB serialization proof."""
import argparse,sys,json,math,hashlib
from pathlib import Path
import bpy,bmesh
import numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.atlas import tile_report
import runpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from settings import LEAF_RECTS
from crown_measure import retained_bounds


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()))
    cfg=runpy.run_path(str(Path(__file__).with_name('config.py')))
    graph=json.loads((a.source.parent/'growth.json').read_text());obs=[ob for ob in bpy.context.scene.objects if ob.type=='MESH' and ob.get('asset_set')=='RedMaple']
    errors=[];vertices=[ob.matrix_world@v.co for ob in obs for v in ob.data.vertices]
    size=[max(v[k] for v in vertices)-min(v[k] for v in vertices) for k in range(3)]
    if not (11<=size[2]<=13 and 8<=size[0]<=11.3 and 8<=size[1]<=11.3):errors.append('Tree envelope outside brief')
    wood=bpy.data.objects['Trunk and branches'];wood.data.calc_loop_triangles();sections=[]
    # Intersect actual woody triangles with the chest-height plane. Only trunk
    # crosses here. This measures its polygonal surface, not the DBH constant.
    for tri in wood.data.loop_triangles:
        ps=[wood.matrix_world@wood.data.vertices[i].co for i in tri.vertices]
        for A,B in zip(ps,ps[1:]+ps[:1]):
            if (A.z-1.35)*(B.z-1.35)<0:
                t=(1.35-A.z)/(B.z-A.z);sections.append((A.lerp(B,t).x,A.lerp(B,t).y))
    xy=np.unique(np.round(np.array(sections),7),axis=0)
    coeff=np.linalg.lstsq(np.c_[2*xy[:,0],2*xy[:,1],np.ones(len(xy))],(xy*xy).sum(axis=1),rcond=None)[0]
    diameter=2*math.sqrt(coeff[2]+coeff[0]**2+coeff[1]**2)
    if not .30<=diameter<=.40:errors.append('Measured chest-height diameter outside brief')
    # Parent-child centerline attachment is a graph/placement check only.
    # It explicitly does not certify fused branch topology or bark unions.
    attachment=[]
    for i,s in enumerate(graph['stems']):
        if s['parent']<0 or s['level']<0:continue
        par=graph['stems'][s['parent']];x=s['attach']*(len(par['points'])-1);j=min(int(x),len(par['points'])-2);t=x-j
        q=Vector(par['points'][j]).lerp(Vector(par['points'][j+1]),t)
        attachment.append((Vector(s['points'][0])-q).length)
    if max(attachment)>1e-5:errors.append('Disconnected branch centerline')
    co=[s for s in graph['stems'] if s['level']==1]
    forks=[s['points'][0][2] for s in co]
    trunk=next(s for s in graph['stems'] if s['parent']<0)
    if len(co)!=4 or not all(2<=h<=3 for h in forks) or trunk['points'][-1][2]>3:
        errors.append('Main trunk must end in four co-dominants at 2–3 m')
    co_angles=[]
    for s in co:
        delta=np.array(s['points'][1])-s['points'][0]
        co_angles.append(math.degrees(math.acos(delta[2]/np.linalg.norm(delta))))
    hierarchy={str(level):sum(s['level']==level for s in graph['stems']) for level in range(-1,5)}
    wind={}
    for ob in obs:
        attr=ob.data.color_attributes['Wind'];values=np.array([c.color for c in attr.data])
        wind[ob.name]=dict(count=len(values),minimum=values.min(axis=0).tolist(),maximum=values.max(axis=0).tolist())
        if not np.isfinite(values).all() or values.min()<0 or values.max()>1:errors.append('Invalid wind channels')
        if ob.location.length>1e-6 or any(abs(x-1)>1e-6 for x in ob.scale):errors.append('Unapplied object transform')
    leaf=bpy.data.objects['Summer leaf cards'];normals=np.array([n.vector for n in leaf.data.corner_normals])
    normal_error=float(np.max(np.abs(np.linalg.norm(normals,axis=1)-1)))
    if normal_error>1e-5:errors.append('Foliage normals are not normalized')
    tile=tile_report([leaf],cfg)
    errors+=tile['errors']
    total=0
    for ob in obs:ob.data.calc_loop_triangles();total+=len(ob.data.loop_triangles)
    foliage_triangles=len(leaf.data.loop_triangles)
    if foliage_triangles/total<.64:errors.append('Less than approximately two thirds of triangles in foliage')
    if not 10000<=total<=25000:errors.append('Triangle count outside brief')
    materials=sorted({m.name for ob in obs for m in ob.data.materials})
    if len(materials)!=2:errors.append('Expected exactly bark and foliage materials')
    root=bpy.data.objects['RedMaple']
    if root.location.length>1e-8:errors.append('Root origin off ground origin')
    # Area conservation is checked on the authored pipe profiles, separately
    # from surface measurements on the voxel-unioned mesh.
    pipes=[]
    for i,stem in enumerate(graph['stems']):
        children=[s for s in graph['stems'] if s['parent']==i and s['level']>=1]
        if not children or stem['level']<0:continue
        incoming=stem['nominal_radius']**2
        outgoing=sum(s['nominal_radius']**2 for s in children)
        pipes.append(abs(incoming-outgoing)/incoming)
    if max(pipes)>1e-5:errors.append('Conserved pipe areas disagree')
    # All three planes in each group are independent, orthogonal branchlets.
    # Their shader rejects |view dot true_normal| below .13, reaches full
    # coverage at .32, and has no emission. Every view has a companion >.577.
    pair_errors=[]
    for i in range(0,len(leaf.data.polygons),3):
        normals=[leaf.data.polygons[i+j].normal for j in range(3)]
        pair_errors.extend(abs(normals[j].dot(normals[k])) for j,k in [(0,1),(1,2),(0,2)])
    if max(pair_errors)>1e-5:errors.append('Branchlet companions not orthogonal')
    variants=json.loads((a.source.parent/'branchlet-atlas.json').read_text())
    if any(not 15<=v['leaves']<=30 for v in variants):errors.append('Branchlet leaf count outside 15–30')
    alpha=bpy.data.images.get('T_RedMaple_BaseColor.png')
    crown=retained_bounds(leaf,Path(bpy.path.abspath(alpha.filepath)),LEAF_RECTS)
    if not 1.75<=crown['base_m']<=2.15:errors.append('Retained foliage base outside lawn-tree target')
    if not .90<=crown['width_height_x']<=1.12:errors.append('Crown ratio outside broad oval target')
    bm=bmesh.new();bm.from_mesh(wood.data)
    unseen=set(bm.verts);components=[]
    while unseen:
        start=unseen.pop();component={start};stack=[start]
        while stack:
            v=stack.pop()
            for edge in v.link_edges:
                other=edge.other_vert(v)
                if other in unseen:unseen.remove(other);component.add(other);stack.append(other)
        components.append(len(component))
    nonmanifold=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True);bm.free()
    if len(components)!=1 or nonmanifold or volume<=0:errors.append('Wood must be one sealed connected solid')
    min_diameter=min(2*r for s in graph['geometric_stems'] if graph['stems'][s['index']]['level']>0 for r in s['radii'])
    if min_diameter<.02:errors.append('Wire twig below 2 cm retained as geometry')
    if len(graph['masses'])<12:errors.append('Missing scaffold-supported foliage masses')
    if any(graph['stems'][m['scaffold']]['level']!=2 for m in graph['masses']):errors.append('Mass not supported by scaffold')
    if set(graph['card_masses'])!=set(range(len(graph['masses']))):errors.append('Mass/card ownership incomplete')
    clearance=min(p[2]-w/math.sqrt(2) for p,w in zip(graph['card_centers'],graph['card_widths']) if math.hypot(p[0],p[1])-w/math.sqrt(2)<1)
    if clearance<2.2:errors.append('Foliage enters 2.2 m walk clearance near bole')
    root_reach=max(math.hypot(v.co.x,v.co.y) for v in wood.data.vertices if v.co.z<.08)
    if root_reach>.56:errors.append('Root flare extends beyond modest buttress target')
    flare=[]
    for height in [.01,.05,.25,.50,.70,1.35]:
        segments=set();coordinates={}
        for tri in wood.data.loop_triangles:
            cuts=[];indices=list(tri.vertices)
            for ia,ib in zip(indices,indices[1:]+indices[:1]):
                A=wood.data.vertices[ia].co;B=wood.data.vertices[ib].co
                if (A.z-height)*(B.z-height)<0:
                    key=tuple(sorted((ia,ib)));cuts.append(key)
                    if key not in coordinates:
                        q=A.lerp(B,(height-A.z)/(B.z-A.z));coordinates[key]=(float(q.x),float(q.y))
            if len(set(cuts))==2:segments.add(tuple(sorted(cuts)))
        adjacency={}
        for A,B in segments:
            adjacency.setdefault(A,[]).append(B);adjacency.setdefault(B,[]).append(A)
        if any(len(v)!=2 for v in adjacency.values()):raise RuntimeError('Trunk section is not a closed loop')
        unseen=set(adjacency);area=0.
        while unseen:
            start=next(iter(unseen));loop=[start];previous=None;current=start
            while True:
                unseen.discard(current)
                nxt=next(v for v in adjacency[current] if v!=previous)
                if nxt==start:break
                loop.append(nxt);previous,current=current,nxt
            points=[coordinates[key] for key in loop]
            area+=abs(sum(A[0]*B[1]-A[1]*B[0] for A,B in zip(points,points[1:]+points[:1])))*.5
        equivalent=2*math.sqrt(area/math.pi)
        flare.append(dict(height_m=height,area_m2=area,area_equivalent_diameter_m=equivalent,ratio_to_measured_dbh=equivalent/diameter))
    if not 1.5<=flare[0]['ratio_to_measured_dbh']<=1.8:errors.append('Actual grade flare outside 1.5–1.8 DBH')
    report=dict(stage='source construction / final botanical model',flare_sections=flare,passed=not errors,errors=errors,
        wood_connected_components=components,wood_nonmanifold_edges=nonmanifold,wood_volume_m3=volume,
        authored_minimum_branch_diameter_m=min_diameter,root_reach_below_8cm_m=root_reach,conservative_card_clearance_within_1m_of_bole_m=clearance,foliage_mass_count=len(graph['masses']),
        triangles=total,foliage_triangles=foliage_triangles,foliage_triangle_fraction=foliage_triangles/total,
        pipe_junctions=len(pipes),pipe_area_relative_error_max=max(pipes),pipe_scope='Authored nominal load-bearing profiles before collar swelling and voxel union',
        branchlet_companion_dot_error_max=max(pair_errors),branchlet_variants=variants,
        crown=crown,materials=materials,meshes=len(obs),bounds_m=size,
        lowest_vertex_z_m=min(v.z for v in vertices),measured_dbh_circle_fit_m=diameter,
        dbh_section_samples=len(xy),branch_attachment_max_m=max(attachment),
        branch_attachment_scope='centerline placement; not fused surface validation',
        stem_count=len(graph['stems']),hierarchy_counts=hierarchy,co_dominant_start_heights_m=forks,co_dominant_initial_angles_from_vertical_degrees=co_angles,main_trunk_end_z_m=trunk['points'][-1][2],terminal_count=len(graph['terminals']),leaf_cards=len(leaf.data.polygons),
        wind=wind,normal_unit_error_max=normal_error,tiles=tile,
        leaf_source_image_size=list(alpha.size),leaf_source_image_bytes=Path(bpy.path.abspath(alpha.filepath)).stat().st_size,
        source_bytes=a.source.stat().st_size,source_sha256=hashlib.sha256(a.source.read_bytes()).hexdigest(),
        delivery_scope='This source check does not certify delivery. See delivery-check.json, botanical-delivery-check.json and the final GLB photo pairs.')
    a.out.write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
    if errors:raise RuntimeError('Structure check failed')

if __name__=='__main__':main()
