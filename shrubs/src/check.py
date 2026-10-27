"""Measure actual source geometry, botanical organization, UVs and Wind data.

Checkpoint audit only: no bake, final UV pack or GLB serialization is certified.
"""
import argparse,sys,json,hashlib
from pathlib import Path
import bpy,bmesh,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))


def parity(bvh,point,direction):
    origin=Vector(point);direction=Vector(direction).normalized();count=0
    for _ in range(100):
        hit,normal,index,distance=bvh.ray_cast(origin,direction,5)
        if hit is None:return count%2==1
        count+=1;origin=hit+direction*1e-6
    raise AssertionError('Unresolved stem parity')


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--species',choices=['Boxwood','Hydrangea'],default='Boxwood');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()));bpy.context.view_layer.update()
    species=a.species;obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')==species];counts={};digest=hashlib.sha256();positions=[]
    for o in sorted(obs,key=lambda x:x.name):
        m=o.data;m.calc_loop_triangles();counts[o.name]=len(m.loop_triangles);wind=m.color_attributes.get('Wind')
        assert wind and len(wind.data)==len(m.vertices)
        vals=np.array([c.color[:] for c in wind.data]);assert np.isfinite(vals).all() and vals.min()>=0 and vals.max()<=1
        for v in m.vertices:positions.append(o.matrix_world@v.co);digest.update(np.array(v.co[:],'<f4').tobytes())
        for c in wind.data:digest.update(np.array(c.color[:],'<f4').tobytes())
        for n in m.corner_normals:digest.update(np.array(n.vector[:],'<f4').tobytes());assert abs(n.vector.length-1)<1e-4
        assert m.uv_layers
        for t in m.loop_triangles:assert t.area>1e-12
    wood=bpy.data.objects[species+' wood'];me=wood.data;part=me.attributes['GrowthPart'];vs=[tuple(v.co) for v in me.vertices]
    graph=json.loads((a.source.parent/'growth.json').read_text());solids=[];attachments=[];rooted=0
    for i,stem in enumerate(graph['stems']):
        bm=bmesh.new();bm.from_mesh(me);layer=bm.faces.layers.int['GrowthPart'];bmesh.ops.delete(bm,geom=[f for f in bm.faces if f[layer]!=i],context='FACES')
        assert bm.faces and all(e.is_manifold for e in bm.edges if e.link_faces)
        volume=bm.calc_volume(signed=True);assert volume>0,(i,volume);bm.free()
        ids={v for f in me.polygons if part.data[f.index].value==i for v in f.vertices};actual=np.array([vs[v] for v in ids]);minimum=float(actual[:,2].min())
        solids.append(dict(stem=i,volume_m3=volume,minimum_z_m=minimum))
        if stem['parent']<0:
            assert abs(minimum)<1e-5,(i,minimum);rooted+=1
        else:
            design=np.array(stem['points'][0]);sides=stem['sides'];ring=actual[np.argsort(np.linalg.norm(actual-design,axis=1))[:sides]];center=ring.mean(0)
            faces=[tuple(f.vertices) for f in me.polygons if part.data[f.index].value==stem['parent']];bvh=BVHTree.FromPolygons(vs,faces,all_triangles=False)
            votes=sum(parity(bvh,center,d) for d in [(1,.319,.177),(.271,1,.119),(.191,.279,1)])
            assert votes>=2,(i,center,votes)
            attachments.append(dict(stem=i,parent=stem['parent'],measured_base_m=center.tolist(),inside_parent_votes=votes,nearest_parent_surface_m=bvh.find_nearest(Vector(center))[3]))
    assert rooted>=20
    assert 2000<=sum(counts.values())<=6000
    materials={s.material for o in obs for s in o.material_slots};assert len(materials)<=2
    assert list(bpy.data.objects[species].location)==[0,0,0]
    lo=np.min(positions,axis=0);hi=np.max(positions,axis=0);assert abs(lo[2])<1e-5
    leaf=bpy.data.objects['Boxwood leaf cards' if species=='Boxwood' else 'Hydrangea leaf and flower cards'];me=leaf.data
    image=next(n.image for n in leaf.data.materials[0].node_tree.nodes if n.type=='TEX_IMAGE' and 'BaseColor' in n.image.name)
    w,h=image.size;assert (w,h)==(2048,2048);pixels=np.empty(w*h*4,np.float32);image.pixels.foreach_get(pixels);alpha=pixels.reshape(h,w,4)[:,:,3]
    uv=me.uv_layers[0];support=[];densities=[];byband=[[] for _ in range(12)];per_face={};zmax=.95 if species=='Boxwood' else 1.3
    for poly in me.polygons:
        uvs=[uv.data[i].uv for i in poly.loop_indices];u0,v0=uvs[0];u1,v1=uvs[2]
        assert len(uvs)==4 and 0<=u0<u1<=1 and (0<=v0<v1<=.5 if species=='Boxwood' else .5<=v0<v1<=1)
        xa,xb=round(u0*w),round(u1*w);ya,yb=round(v0*h),round(v1*h);ys,xs=np.nonzero(alpha[ya:yb,xa:xb]>.45)
        if not len(xs):continue
        xx=(xs+.5)/(xb-xa);yy=(ys+.5)/(yb-ya)
        verts=np.array([me.vertices[me.loops[i].vertex_index].co[:] for i in poly.loop_indices]);assert np.allclose(verts[2],verts[1]+verts[3]-verts[0],atol=1e-6)
        pts=verts[0]+xx[:,None]*(verts[1]-verts[0])+yy[:,None]*(verts[3]-verts[0])
        bounds=np.array([pts.min(0),pts.max(0)]);support.append(bounds);per_face[poly.index]=bounds
        densities.append((xb-xa)/np.linalg.norm(verts[1]-verts[0]))
        for j in range(12):
            selected=pts[(pts[:,2]>=j*zmax/12)&(pts[:,2]<(j+1)*zmax/12)]
            if len(selected):byband[j].append(np.array([selected.min(0),selected.max(0)]))
    supp=np.concatenate(support);leaflo=supp.min(0);leafhi=supp.max(0);bands=[]
    for j,band in enumerate(byband):
        if band:
            pts=np.concatenate(band);size=pts.max(0)-pts.min(0);bands.append(dict(z_interval_m=(j*zmax/12,(j+1)*zmax/12),x_width_m=float(size[0]),y_width_m=float(size[1])))
    rep=dict(passed=True,species=species,scope='source geometry/Wind/normals/tile/plant construction, no bake/GLB proof',triangles=counts,total=sum(counts.values()),materials=len(materials),meshes=len(obs),rooted_stems=rooted,wood_solids=solids,measured_daughter_attachments=attachments,mesh_bounds_m=dict(min=lo.tolist(),max=hi.tolist(),size=(hi-lo).tolist()),retained_foliage_bounds_m=dict(min=leaflo.tolist(),max=leafhi.tolist(),size=(leafhi-leaflo).tolist()),width_by_height_bands=bands,card_density_px_m=dict(min=min(densities),max=max(densities)),geometry_normals_wind_sha256=digest.hexdigest(),source_bytes=a.source.stat().st_size,texture_bytes={c:(ROOT/'shrubs/textures/ship'/f'T_Shrubs_{c}.png').stat().st_size for c in ('BaseColor','Normal','ORM')},texture_memory_MiB_full_mip_BC7_BC5_8bpp_ORM=16)
    if species=='Hydrangea':
        heads=[]
        for head in graph['heads']:
            bounds=np.concatenate([per_face[i] for i in range(head['first_face'],head['first_face']+head['faces'])]);heads.append(dict(stem=head['stem'],nodding=head['nodding'],actual_alpha_bounds_m=(bounds.max(0)-bounds.min(0)).tolist()))
        assert all(.15<max(h['actual_alpha_bounds_m'])<.21 for h in heads),heads
        # Opposite pairs use the same measured parent station before petioles.
        for i in range(0,len(graph['leaves']),2):assert graph['leaves'][i]['anchor_m']==graph['leaves'][i+1]['anchor_m']
        rep['measured_heads']=heads;rep['opposite_leaf_pairs']=len(graph['leaves'])//2
        parent_bvhs={};petiole_votes=[]
        for i,record in enumerate(graph['leaves']):
            parent=record['stem']
            if parent not in parent_bvhs:
                wme=wood.data;wpart=wme.attributes['GrowthPart']
                faces=[tuple(f.vertices) for f in wme.polygons if wpart.data[f.index].value==parent]
                parent_bvhs[parent]=BVHTree.FromPolygons([tuple(v.co) for v in wme.vertices],faces,all_triangles=False)
            actual=me.vertices[i*6+1].co
            assert (actual-Vector(record['anchor_m'])).length<1e-6
            votes=sum(parity(parent_bvhs[parent],actual,d) for d in [(1,.319,.177),(.271,1,.119),(.191,.279,1)])
            assert votes>=2,(i,parent,actual,votes)
            petiole_votes.append(votes)
        rep['measured_petiole_bases_inside_parent']=len(petiole_votes)
        rep['minimum_petiole_parity_votes']=min(petiole_votes)
    source_audit=a.source.parent/'lookdev-audit.json';game_audit=a.source.parent/'game-audit.json'
    if source_audit.exists() and game_audit.exists():
        sd=json.loads(source_audit.read_text())['sets'][species]['geometry_sha256'];gd=json.loads(game_audit.read_text())['sets'][species]['geometry_sha256'];assert sd==gd;rep['independent_source_game_geometry_sha256']=sd
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(rep,indent=2));print(json.dumps(rep,indent=2))

if __name__=='__main__':main()
