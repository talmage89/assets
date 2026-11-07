"""Construct modules, assemble original seeded sites, export external glTF."""
import argparse,sys,json,math,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import geometry as Q, pieces, bowl, terrain
from plan import plan,SEEDS
from park_site import site

def record(rt):
    bpy.context.view_layer.update()
    points=[rt.matrix_world.inverted()@ob.matrix_world@v.co for ob in [rt,*rt.children_recursive] if ob.type=='MESH' for v in ob.data.vertices]
    return dict(triangles=Q.count(rt),bounds_m=[[float(op(p[k] for p in points)) for k in range(3)] for op in (min,max)] if points else [],
                sockets={o.name.split('__')[-1]:dict(position_m=list(o.location),kind=o['socket_kind']) for o in rt.children_recursive if 'socket_kind' in o},properties={k:(rt[k].to_list() if hasattr(rt[k],'to_list') else rt[k]) for k in rt.keys()})

def export(path,roots):
    path.parent.mkdir(parents=True,exist_ok=True);bpy.ops.object.select_all(action='DESELECT')
    for rt in roots:
        for o in [rt,*rt.children_recursive]:o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLTF_SEPARATE',use_selection=True,
        export_yup=True,export_extras=True,export_animations=False,export_tangents=True,export_texture_dir='shared',export_image_format='AUTO',export_shared_accessors=True,export_all_vertex_colors=False,export_attributes=True,export_vertex_color='MATERIAL')
    embedded=Path('build/embedded')/path.with_suffix('.glb').name;embedded.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=str(embedded.resolve()),export_format='GLB',use_selection=True,
        export_yup=True,export_extras=True,export_animations=False,export_tangents=True,export_image_format='AUTO',export_all_vertex_colors=False,export_attributes=True,export_vertex_color='MATERIAL')
    from export_frames import repair
    repair(path);repair(embedded)
    from external import share_images
    share_images(path)
    return dict(embedded_build_bytes=embedded.stat().st_size,gltf_bytes=path.stat().st_size,bin_bytes=path.with_suffix('.bin').stat().st_size,
                sha256=hashlib.sha256(path.read_bytes()+path.with_suffix('.bin').read_bytes()).hexdigest())

def paving(p,lib):
    W,D=p['skating'];rt=Q.root('SkatingFlatwork');hole=None
    if p['bowl']:
        x,y,_=p['bowl']['location'];hole=[x-bowl.BX,x+bowl.BX,y-bowl.BY,y+bowl.BY]
    xs=sorted(set([-W/2,W/2]+[i*3.048 for i in range(-round(W/6.096),round(W/6.096)+1) if -W/2<i*3.048<W/2]+(hole[:2] if hole else [])))
    ys=sorted(set([-D/2,D/2]+[i*3.048 for i in range(-round(D/6.096),round(D/6.096)+1) if -D/2<i*3.048<D/2]+(hole[2:] if hole else [])))
    mat='Asphalt' if p['type']=='prefab' else 'Concrete'
    cuts=([hole] if hole else [])+p.get('terrain_cuts',[])+p.get('landscape_cuts',[])
    if p['type']=='poured':
        for item in p['placements']:
            if item['piece']=='FlatBar':continue
            source=lib[item['piece']]
            a=math.radians(item['yaw']);c,s=math.cos(a),math.sin(a);x,y,_=item['location']
            for x0,x1,y0,y1 in json.loads(source.get('ground_cut_json','[]')):
                xx=[x+vx*c-vy*s for vx,vy in ((x0,y0),(x1,y0),(x1,y1),(x0,y1))]
                yy=[y+vx*s+vy*c for vx,vy in ((x0,y0),(x1,y0),(x1,y1),(x0,y1))]
                cuts.append([min(xx),max(xx),min(yy),max(yy)])
    def remaining(rect):
        parts=[rect]
        for cut in cuts:
            new=[];hx0,hx1,hy0,hy1=cut
            for x0,x1,y0,y1 in parts:
                a,b=max(x0,hx0),min(x1,hx1);c,d=max(y0,hy0),min(y1,hy1)
                if a>=b or c>=d:new.append((x0,x1,y0,y1));continue
                new += [(x0,a,y0,y1),(b,x1,y0,y1),(a,b,y0,c),(a,b,d,y1)]
            parts=[r for r in new if r[1]-r[0]>1e-5 and r[3]-r[2]>1e-5]
        return parts
    for xa,xb in zip(xs,xs[1:]):
        for ya,yb in zip(ys,ys[1:]):
            if hole and hole[0]<(xa+xb)/2<hole[1] and hole[2]<(ya+yb)/2<hole[3]:continue
            gap=0 if mat=='Asphalt' else .0015
            if mat=='Asphalt':Q.box('Independent pad pour',((xa+xb)/2,(ya+yb)/2,-.075),(xb-xa,yb-ya,.15),rt,mat,0)
            else:
                for x0,x1,y0,y1 in remaining((xa+gap,xb-gap,ya+gap,yb-gap)):
                    Q.mesh('Exposed troweled slab skin',[(x0,y0,0),(x1,y0,0),(x1,y1,0),(x0,y1,0)],[(0,1,2,3)],rt,mat)
    # Beneath 3mm sawn joints only, never across the bowl opening.
    for xa,xb in zip(xs,xs[1:]):
        for ya,yb in zip(ys,ys[1:]):
            if hole and hole[0]<(xa+xb)/2<hole[1] and hole[2]<(ya+yb)/2<hole[3]:continue
            if mat=='Concrete':
                # Only strips beneath saw cuts, with no duplicate hidden floor.
                for rect in ((xa,xb,ya,ya+.0015),(xa,xa+.0015,ya,yb)):
                    for x0,x1,y0,y1 in remaining(rect):Q.mesh('Recessed joint backing',[(x0,y0,-.006),(x1,y0,-.006),(x1,y1,-.006),(x0,y1,-.006)],[(0,1,2,3)],rt,'Joint')
    edge_mat='GroundConcrete' if 'GroundConcrete' in Q.M else 'Concrete'
    # Concrete-valued thickened slab edge meets a narrow mow strip, then lawn.
    for x in (-W/2,W/2):
        Q.box('Thickened slab edge',(x+(.045 if x>0 else -.045),0,-.09),(.09,D,.18),rt,edge_mat,.004)
        Q.box('Concrete mow strip',(x+(.27 if x>0 else -.27),0,-.05),(.36,D+.90,.10),rt,edge_mat,.004)
    for y in (-D/2,D/2):
        Q.box('Thickened slab edge',(0,y+(.045 if y>0 else -.045),-.09),(W+.18,.09,.18),rt,edge_mat,.004)
        Q.box('Concrete mow strip',(0,y+(.27 if y>0 else -.27),-.05),(W+.18,.36,.10),rt,edge_mat,.004)
    return rt

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('build/Skatepark.blend'));ap.add_argument('--seeds',type=int,nargs='+',default=SEEDS);ap.add_argument('--look',action='store_true');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True);Q.palette();bpy.context.scene.unit_settings.system='METRIC'
    if a.look:
        import finishes
        finishes.materials()
    lib={o.name:o for o in pieces.library()}
    for n in (4,5):
        ob=pieces.bank('PlazaBank_'+str(n),h=n*.1524,rail=True);lib[ob.name]=ob
    bowl_lib=bowl.build(True);steel_bowl=bowl.build(False)
    # Blender's automatic suffixes must not become the public module identifiers.
    for i,rt in enumerate(steel_bowl):rt.name='SteelBowl_Sector_%02d'%i if i<16 else 'SteelBowl_Floor_'+str(i-16)
    if a.look:finishes.prepare([*lib.values(),*bowl_lib,*steel_bowl])
    for rt in [*lib.values(),*bowl_lib,*steel_bowl]:Q.join(rt)
    # A grid reservation surrounds each physical footprint. Curved profile
    # connections retain their exact analytic coordinates beside these ports;
    # a scene's flatwork fills the reservation, as it does in this generator.
    for rt in [*lib.values(),*bowl_lib,*steel_bowl]:
        if a.look:rt['stage']='baked look-dev checkpoint'
        bounds=record(rt)['bounds_m'];lo=[math.floor(bounds[0][k]/.1524)*.1524 for k in (0,1)];hi=[math.ceil(bounds[1][k]/.1524)*.1524 for k in (0,1)]
        rt['grid_bounds_json']=json.dumps([lo,hi])
        Q.socket(rt,'Grid_SW',(*lo,0),kind='layout_grid');Q.socket(rt,'Grid_NE',(*hi,0),kind='layout_grid')
    records={o.name:record(o) for o in [*lib.values(),*bowl_lib,*steel_bowl]}
    ex=Path('export/final' if a.look else 'export/connected-form');delivery=export(ex/'SkateparkPieces.gltf',[*lib.values(),*bowl_lib,*steel_bowl]);parks={}
    for seed in a.seeds:
        p=plan(seed);connections,cuts=terrain.build(p,lib);p['terrain_cuts']=cuts
        roots=list(connections);skating=list(connections)+[paving(p,lib)];roots.append(skating[-1])
        if p['bowl']:
            for source in bowl_lib if p['bowl']['pool'] else steel_bowl:
                rt=Q.instance(source,source.name+'_placed',p['bowl']['location']);skating.append(rt);roots.append(rt)
        for i,item in enumerate(p['placements']):
            rt=Q.instance(lib[item['piece']],item['piece']+'_'+str(i),item['location'],item['yaw']);roots.append(rt);skating.append(rt)
            terrain.bury_seams(rt,item,p)
        site_roots=site(p);roots+=site_roots
        if a.look:
            finishes.prepare(connections+[skating[len(connections)] ]+site_roots)
            for rt in skating:finishes.weather(rt,p)
            import placed_wear
            placed_wear.bowl_contacts(skating,p)
            finishes.basin_deposits(skating,p)
        guard_check=terrain.guard_contacts(roots)
        mark_check=finishes.surface_mark_contacts(skating) if a.look else None
        if a.look:
            for rt in roots:rt['stage']='baked look-dev checkpoint'
        for rt in roots:Q.join(rt)
        if p.get('terrain_yaw'):
            from mathutils import Matrix
            transform=Matrix.Rotation(math.radians(p['terrain_yaw']),4,'Z')
            for rt in skating:rt.matrix_world=transform@rt.matrix_world
        bpy.context.view_layer.update()
        info=dict(plan=p,placed_wear=placed_wear.report(skating) if a.look else None,guard_contacts=guard_check,surface_mark_contacts=mark_check,skating_triangles=sum(Q.count(r) for r in skating),whole_site_triangles=sum(Q.count(r) for r in roots),
                  parts={r.name:record(r) for r in roots})
        # Detailed wear receipts belong in the build report, rather than in
        # every runtime node's extras. Keep construction sockets/pivots.
        for rt in roots:
            if 'placed_wear_json' in rt:del rt['placed_wear_json']
        path=ex/('Park_'+str(seed)+'.gltf');info['delivery']=export(path,roots);parks[str(seed)]=info
        Path('build/park-'+str(seed)+'.json').write_text(json.dumps(info,indent=2))
        for rt in roots:
            for o in [*rt.children_recursive,rt]:
                if o.name in bpy.data.objects:bpy.data.objects.remove(o,do_unlink=True)
    # Only current external glTF references own the generated shared images.
    # Remove stale iteration images so a clean rebuild has the same file set.
    used={image['uri'] for path in ex.glob('*.gltf') for image in json.loads(path.read_text()).get('images',[]) if 'uri' in image}
    for old in ex.glob('*.glb'):old.unlink()
    for image in (ex/'shared').glob('*.png'):
        if image.relative_to(ex).as_posix() not in used:image.unlink()
    # Source module inspection layout, independent from placed exports.
    for i,rt in enumerate(lib.values()):rt.location=(i%4*12,i//4*12,0)
    for i,rt in enumerate(bowl_lib):rt.location=(0,62,0)
    for rt in steel_bowl:rt.location=(24,62,0)
    a.out.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(a.out.resolve()))
    report=dict(stage='baked look-dev' if a.look else 'connected form checkpoint',pieces=records,parks=parks,library_delivery=delivery)
    a.out.with_suffix('.json').write_text(json.dumps(report,indent=2));print('CHECKPOINT',json.dumps({s:{k:v for k,v in info.items() if k.endswith('triangles')} for s,info in parks.items()}))

if __name__=='__main__':main()
