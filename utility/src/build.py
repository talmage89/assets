"""Build reusable utility parts and four runs. Stop at the form checkpoint."""
import argparse,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit import model as G
from kit.tiling import export
from plan import SEEDS,pole_spec,street
from construction import Assembly,palette,pole,guy,crossarm,transformer,conductor,pin,M
from span import sag_from_tension,catenary


def mesh_report(objects):
    rows={}
    for ob in objects:
        if ob.type!='MESH':continue
        ob.data.calc_loop_triangles()
        rows[ob.name]=dict(triangles=len(ob.data.loop_triangles),vertices=len(ob.data.vertices),
          materials=len(set(p.material_index for p in ob.data.polygons)),
          bounds=[[min((ob.matrix_world@v.co)[k] for v in ob.data.vertices) for k in range(3)],
                  [max((ob.matrix_world@v.co)[k] for v in ob.data.vertices) for k in range(3)]])
    return rows


def save(path,metadata):
    bpy.context.view_layer.update();path.parent.mkdir(parents=True,exist_ok=True)
    import bmesh
    for ob in bpy.context.scene.objects:
        if ob.type=='MESH':
            bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.triangulate(bm,faces=bm.faces[:]);bm.to_mesh(ob.data);bm.free()
    bpy.ops.wm.save_as_mainfile(filepath=str(path.resolve()))
    rows=mesh_report(list(bpy.context.scene.objects));metadata.update(meshes=rows,total_triangles=sum(x['triangles'] for x in rows.values()))
    export(path.with_suffix('.glb'))
    metadata['glb_bytes']=path.with_suffix('.glb').stat().st_size
    path.with_suffix('.json').write_text(json.dumps(metadata,indent=2))


def parts(out):
    bpy.ops.wm.read_factory_settings(use_empty=True);palette();rows={}
    for i,kind in enumerate(('tangent','angle','deadend','transformer','riser','streetlight')):
        s=pole_spec(kind='tangent' if kind=='streetlight' else kind,seed=10+i)
        s['light']=kind=='streetlight';s['bank']=1
        a=pole(kind.title(),s)
        rows[kind]=dict(spec=s,sockets={k:list(ob.location) for k,ob in a.sockets.items()})
        a.root.location=(i*6,0,0)
    a=Assembly('CrossarmAssembly');crossarm(a,pole_spec(),0)
    for x in (-.97536,.97536):
        pin(a,x,.205,.24);a.socket('Conductor_'+('Left' if x<0 else 'Right'),(x,.205,.24),diameter=.0101)
    a.finish();a.root.location=(0,8,0)
    a=Assembly('Transformer50kVA');s=pole_spec(kind='transformer');a.socket('Primary_A',(0,-.1,10.1));transformer(a,s);a.finish()
    # Rebase the standalone transformer so its bottom-footprint is the origin.
    for ob in a.root.children:
        if ob.type=='MESH':
            for v in ob.data.vertices:v.co.z-=s['neutral']+.23
        else:ob.location.z-=s['neutral']+.23
    a.root.location=(6,8,0)
    a=guy('GuyAssembly',(0,0,8.8),(0,-6.3,.1));a.root.location=(12,8,0)
    save(out,dict(stage='FORM CHECKPOINT / quick materials / unbaked',parts=rows))


def house_attachment(row,source_pole,source_comm=None):
    """Optional mast and metadata outside the unchanged house delivery.

    A front-wall mast stands outside the roof overhang. Its lower elbow enters
    the wall, reserving an internal route to the original meter. Interior
    conduit is outside these exterior-shell houses' scope. No second meter.
    """
    meta=json.loads(Path('build/context',row['type']+'.json').read_text())
    block=min(meta['blocks'],key=lambda b:b['y0'])
    angle=math.radians(row['yaw']);rot=Matrix.Rotation(angle,4,'Z');inv=rot.inverted()
    local_source=inv@(Vector(source_pole)-Vector(row['location']))
    side=-1 if local_source.x<0 else 1
    # The corner jamb avoids entry-porch roofs and the garage/window openings.
    xx=block['x0']+.32 if side<0 else block['x1']-.32
    wall_y=block['y0'];yy=wall_y-.80
    x=xx
    from mathutils.bvhtree import BVHTree
    with bpy.data.libraries.load(str(Path('build/context',row['type']+'.blend').resolve()),link=False) as (src,dst):
        dst.objects=[n for n in src.objects if 'Roof' in n or 'roof' in n]
    roof_objects=[o for o in dst.objects if o and o.type=='MESH'];vs=[];fs=[]
    for o in roof_objects:
        o.data.calc_loop_triangles();offset=len(vs);vs.extend([o.matrix_world@v.co for v in o.data.vertices]);fs.extend([tuple(offset+i for i in t.vertices) for t in o.data.loop_triangles])
    bvh=BVHTree.FromPolygons(vs,fs,all_triangles=True);anchor_records=[]
    for sign in (-1,1):
        rx=max(block['x0']+.4,min(block['x1']-.4,x+sign*1.3));ry=wall_y+1.6
        hit=bvh.ray_cast(Vector((rx,ry,20)),Vector((0,0,-1)),30)[0]
        if hit is None:raise ValueError('Missing actual roof anchor')
        anchor_records.append(list(hit))
    for o in dst.objects:
        if o:bpy.data.objects.remove(o,do_unlink=True)
    top=max(5.2,max(p[2] for p in anchor_records)+.75)
    # Size each mast for its own crossing, rather than applying an 18-ft road
    # criterion to the entire private yard. Independent exported checks repeat
    # the classification on actual wire vertices. Private service stays above
    # the general 16-ft Type-A driveway criterion; comm yards retain 12 ft.
    for _ in range(60):
        valid=True
        for source,dz,mass,H,kind in [(source_pole,0,.153,300,'service')]+([(source_comm,-.8,.045,160,'comm_drop')] if source_comm is not None else []):
            end=rot@Vector((x,yy-.32,top+dz))+Vector(row['location'])
            curve=catenary(source,end,sag_from_tension(source,end,mass,H))['point']
            for k in range(201):
                p=curve(k/200);road=abs(p[0])<=4.2672
                minimum=(5.4864 if road else 4.8768) if kind=='service' else (4.7244 if road else 3.6576)
                if p[2]-.16764-.009<minimum+.02:valid=False;break
            if not valid:break
        if valid:break
        top+=.05
    else:raise ValueError('No valid service attachment height')
    a=Assembly(row['name']+'_ServiceMast')
    a.rod('2 inch rigid service mast',(x,yy,2.30),(x,yy,top+.23),.03015,'Steel',10,'house_service')
    a.tube('Service entrance wall elbow',G.bezier((x,yy,2.4),(x,yy,2.12),(x,wall_y-.25,2.15),(x,wall_y+.03,2.15),12),.03015,'Steel',8,'house_service')
    for z in (2.1,2.65):
        a.rod('Mast wall standoff',(xx,wall_y,z),(x,yy,z),.018,'Steel',8,'house_service')
        a.rod('Mast diagonal wall brace',(xx,wall_y,z-.45),(x,yy,z),.012,'Steel',6,'house_service')
        a.box('Mast bracket wall pad',(xx,wall_y-.01,z),(.14,.025,.18),'Steel',0,'house_service')
    # Head points down; separate neutral/hot drip loops remain outside the roof.
    a.tube('Weatherhead entrance',G.bezier((x,yy,top+.23),(x,yy,top+.38),(x,yy-.12,top+.35),(x,yy-.14,top+.24),10),.034,'Paint',8,'house_service')
    for j in range(3):
        off=(j-1)*.027
        a.tube('Service weatherhead drip loop',G.bezier((x+off,yy-.13,top+.24),(x+off,yy-.4,top-.46),(x+off,yy-.58,top-.32),(x+off,yy-.32,top),14),.0045,'Cable',6,'house_service')
    a.rod('Porcelain service attachment',(x,yy,top),(x,yy-.32,top),.024,'Porcelain',10,'house_service')
    # Roof guys attach to actual source roof triangles, rather than guessed
    # roof constants. This supports the tall service mast above the low eave.
    for anchor in anchor_records:
        hit=Vector(anchor)
        a.rod('Mast roof guy',(x,yy,top-.55),hit+Vector((0,0,.035)),.0024,'Steel',6,'house_service')
        a.box('Roof guy flashed anchor',hit+Vector((0,0,.016)),(.10,.08,.027),'Steel',0,'house_service')
    a.socket('ServiceDrop',(x,yy-.32,top),'house_service',.022)
    a.socket('CommunicationDrop',(x,yy-.27,top-.8),'house_communications',.006)
    a.rod('Communication attachment eye',(x,yy,top-.8),(x,yy-.27,top-.8),.008,'Steel',6,'house_service')
    a.finish();a.root.location=row['location'];a.root.rotation_euler.z=angle
    bpy.context.view_layer.update()
    sockets={k:list(o.matrix_world.translation) for k,o in a.sockets.items()}
    return a,sockets,dict(house_type=row['type'],seed=row['seed'],local={k:list(o.location) for k,o in a.sockets.items()},
        frame='Blender metres, +Z up, -Y house front',attachment_height_above_house_grade_m=top,roof_anchors=anchor_records,optional_hardware=True,house_bytes_modified=False)


def run(seed,out):
    bpy.ops.wm.read_factory_settings(use_empty=True);palette();plan=street(seed);poles=[];spans=[];homes=[]
    for s in plan['poles']:
        a=pole(s['name'],s);a.root.location=s['location'];poles.append(a)
    bpy.context.view_layer.update()
    def point(a,key):return a.sockets[key].matrix_world.translation.copy()
    def wire(name,p,q,sag,dia,kind,mat='Aluminum',**extra):
        mass,H={'primary':(.2158,550),'neutral':(.1354,450),'communication':(.24,900),
                'service':(.153,300),'comm_drop':(.045,160)}[kind]
        sag=sag_from_tension(p,q,mass,H)
        ob,report=conductor(name,p,q,sag,dia,mat)
        report.update(kind=kind,mass_kg_m=mass,horizontal_tension_n=H,**extra);spans.append(report);return ob
    for i,(a,b) in enumerate(zip(poles,poles[1:])):
        L=(a.root.location-b.root.location).length;psag=L/44;nsag=L/51;csag=L/63
        for key in a.sockets:
            if key.startswith('Primary_'):
                wire(f'Span_{i}_{key}',point(a,key),point(b,key),psag,.0101,'primary',source_socket=a.sockets[key].name,end_socket=b.sockets[key].name)
        wire(f'Span_{i}_Neutral',point(a,'Neutral'),point(b,'Neutral'),nsag,.008,'neutral')
        if plan['profile']['comm']:
            for key,dia,offset in [('CommStrand',.00635,0),('LashedFiber',.020,0),('Telephone',.028,.03)]:
                wire(f'Span_{i}_{key}',point(a,key),point(b,key),csag+offset,dia,'communication','Cable')
            # Wide-pitch lashing is omitted from long-span geometry; planned normal detail.
    for i in (0,2,4):
        a=poles[i];p=point(a,'GuyUpper')
        q=a.root.location+Vector((0,-6.5 if i==0 else 6.5,.1)) if i!=2 else a.root.location+Vector((-6.5,0,.1))
        guy('Guy_'+str(i),p,q)
    transformers=[1,3]
    for row in plan['houses']:
        index=min(transformers,key=lambda i:abs(plan['poles'][i]['location'][1]-row['location'][1]))
        a=poles[index];mast,sockets,sidecar=house_attachment(row,point(a,'Service'),point(a,'CommDrop') if plan['profile']['comm'] else None)
        p=point(a,'Service');q=Vector(sockets['ServiceDrop']);length=(p-q).length
        sag=min(.5,length*.011)
        # Three true conductors, smooth central axes; the lay is a normal-map
        # detail except in the detachable close-up demonstrator.
        for j in range(3):
            off=Vector(((j-1)*.009,0,.006 if j==1 else -.003))
            wire(f'Drop_{row["name"]}_{j}',p+off,q+off,sag,.0062 if j==1 else .0085,'service','Aluminum' if j==1 else 'Cable',house=row['name'],source_pole=index)
        if plan['profile']['comm']:
            wire(f'PhoneDrop_{row["name"]}',point(a,'CommDrop'),sockets['CommunicationDrop'],min(.26,length*.005),.006,'comm_drop','Cable',house=row['name'])
        homes.append(dict(**row,sockets=sockets,attachment=sidecar,transformer=index))
    # Consolidate spans by system for efficient static inspection/export.
    for system in ('primary','neutral','communication','service','comm_drop'):
        names={r['name'] for r in spans if r['kind']==system};obs=[o for o in bpy.context.scene.objects if o.name in names]
        if obs:
            bpy.ops.object.select_all(action='DESELECT')
            for ob in obs:ob.select_set(True)
            bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();obs[0].name='Conductors_'+system
    report=dict(stage='FORM CHECKPOINT / quick materials / unbaked',plan=plan,spans=spans,houses=homes,
      sockets={a.root.name:{k:list(o.matrix_world.translation) for k,o in a.sockets.items()} for a in poles})
    save(out,report)
    Path('build/house-attachments-'+str(seed)+'.json').write_text(json.dumps(homes,indent=2))


def main(a):
    parts(a.out)
    for seed in SEEDS:run(seed,a.out.parent/f'street-{seed}.blend')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('build/utility.blend'));main(p.parse_args(sys.argv[sys.argv.index('--')+1:]))
