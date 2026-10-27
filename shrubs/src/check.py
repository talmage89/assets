"""Independent checkpoint geometry/atlas/Wind checks. Does not certify a GLB."""
import argparse,sys,json,math,hashlib
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()));bpy.context.view_layer.update()
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')=='Boxwood'];errors=[];counts={};digest=hashlib.sha256();positions=[]
    for o in sorted(obs,key=lambda x:x.name):
        m=o.data;m.calc_loop_triangles();counts[o.name]=len(m.loop_triangles);wind=m.color_attributes.get('Wind')
        assert wind and len(wind.data)==len(m.vertices)
        vals=np.array([c.color[:] for c in wind.data]);assert np.isfinite(vals).all() and vals.min()>=0 and vals.max()<=1
        for v in m.vertices:
            positions.append(o.matrix_world@v.co);digest.update(np.array(v.co[:],'<f4').tobytes())
        for c in wind.data:digest.update(np.array(c.color[:],'<f4').tobytes())
        assert len(m.uv_layers)>0
        for t in m.loop_triangles:assert t.area>1e-12
        assert all(abs(n.vector.length-1)<1e-4 for n in m.corner_normals)
    assert 2000<=sum(counts.values())<=6000
    assert len({s.material for o in obs for s in o.material_slots})<=2
    assert list(bpy.data.objects['Boxwood'].location)==[0,0,0]
    lo=[min(p[i] for p in positions) for i in range(3)];hi=[max(p[i] for p in positions) for i in range(3)]
    assert abs(lo[2])<1e-5
    leaf=bpy.data.objects['Boxwood leaf cards'];me=leaf.data
    # Retained alpha support measured on actual quad positions at tile texel
    # centers, rather than reporting the configured envelope as a measurement.
    image=next(n.image for n in leaf.data.materials[0].node_tree.nodes if n.type=='TEX_IMAGE' and 'BaseColor' in n.image.name)
    w,h=image.size;pixels=np.empty(w*h*4,np.float32);image.pixels.foreach_get(pixels);alpha=pixels.reshape(h,w,4)[:,:,3]
    uv=me.uv_layers[0];support=[];densities=[]
    for poly in me.polygons:
        ids=[me.loops[i].vertex_index for i in poly.loop_indices];vs=[me.vertices[i].co for i in ids];uvs=[uv.data[i].uv for i in poly.loop_indices]
        u0,v0=uvs[0];u1,v1=uvs[2];xa,xb=round(u0*w),round(u1*w);ya,yb=round(v0*h),round(v1*h)
        ys,xs=np.nonzero(alpha[ya:yb,xa:xb]>.45)
        if not len(xs):continue
        xx=(xs+.5)/(xb-xa);yy=(ys+.5)/(yb-ya)
        verts=np.array([v[:] for v in vs]);pts=verts[0]+xx[:,None]*(verts[1]-verts[0])+yy[:,None]*(verts[3]-verts[0]);support.append(np.array([pts.min(0),pts.max(0)]))
        densities.append((xb-xa)/(vs[1]-vs[0]).length)
    supp=np.concatenate(support);leaflo=supp.min(0);leafhi=supp.max(0)
    rep=dict(passed=True,scope='source checkpoint geometry/Wind/authored tile bounds; no finalized UV/bake/GLB proof',triangles=counts,total=sum(counts.values()),materials=2,meshes=len(obs),mesh_bounds_m=dict(min=lo,max=hi,size=[b-a for a,b in zip(lo,hi)]),retained_foliage_bounds_m=dict(min=leaflo.tolist(),max=leafhi.tolist(),size=(leafhi-leaflo).tolist()),card_density_px_m=dict(min=min(densities),max=max(densities)),geometry_wind_sha256=digest.hexdigest(),source_bytes=a.source.stat().st_size,texture_bytes={c:(ROOT/'shrubs/textures/ship'/f'T_Shrubs_{c}.png').stat().st_size for c in ('BaseColor','Normal','ORM')},texture_memory_MiB_full_mip_BC7_BC5_8bpp_ORM=16)
    a.out.write_text(json.dumps(rep,indent=2));print(json.dumps(rep,indent=2))

if __name__=='__main__':main()
