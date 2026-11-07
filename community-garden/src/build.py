"""Build the reusable family and three distinct seeded form-checkpoint gardens."""
import argparse,sys,json,math,random,hashlib,os
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
import geometry as Q
import plants,pieces,fence
from plan import plan,SEEDS
from kit import tiling

LIB={};PLANTS={}


def descendants(roots):return [o for r in roots for o in [r,*r.children_recursive]]


def export(path,roots):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in descendants(roots):
        ob.select_set(True)
        if ob.type=='MESH':
            for attr in list(ob.data.color_attributes):
                if attr.name=='Wind':attr.name='_WIND'
                elif attr.name!='_WIND':ob.data.color_attributes.remove(attr)
    bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLTF_SEPARATE',use_selection=True,
        export_extras=True,export_animations=False,export_tangents=True,export_attributes=True,
        export_vertex_color='NONE',export_image_format='AUTO',export_texture_dir='cache')
    # Resolve exported copies back to one canonical image identity, shared by
    # family and all seeds. Checkpoint files never touch the native deliveries.
    doc=json.loads(path.read_text());folders=[Path('textures/checkpoint'),Path('build/context/chain'),REPO/'ground/textures/ship']
    known={hashlib.sha256(p.read_bytes()).hexdigest():p.resolve() for f in folders for p in f.glob('*.png')}
    for row in doc.get('images',[]):
        copied=path.parent/row['uri'];target=known.get(hashlib.sha256(copied.read_bytes()).hexdigest())
        if target is None:raise ValueError('Unregistered image '+str(copied))
        row['uri']=os.path.relpath(target,path.parent.resolve());row.pop('mimeType',None)
    path.write_text(json.dumps(doc,separators=(',',':'))+'\n')
    return doc


def remove(rt):
    for o in [*rt.children_recursive,rt]:bpy.data.objects.remove(o,do_unlink=True)


def place(key,name,pos,parent,yaw=0):return Q.instance(LIB[key],name,pos,yaw,parent)


def planted(plot,bed,site):
    rng=random.Random(plot['seed']);w,d=plot['width'],plot['depth'];sp=plot['crop'];soil=bed['soil_surface_m']+.003
    stage=0 if plot['state']=='new' else 2
    plot['soil_z_world']=float(bed.location.z+bed['soil_surface_m'])
    plot['plants']=[]
    def add(species,x,y,st=None,yaw=None,variant=None):
        j=stage if st is None else st;v=(rng.randrange(2) if variant is None else variant) if j==2 else 0;key=f'{species}_{j}_{v}'
        rt=Q.instance(PLANTS[key],f'Plot{plot["id"]:02}_{species}',(x,y,soil),rng.random()*360 if yaw is None else yaw,bed)
        plot['plants'].append(dict(species=species,local=[x,y,soil],prototype=key))
        return rt
    if plot['state']=='fallow':
        # Straw is actual scattered short stalks at the soil surface, held off
        # the board edge. Local decomposition/wet patches remain quick values.
        for i in range(90 if w<2 else 160):
            x=rng.uniform(-w/2+.10,w/2-.10);y=rng.uniform(-d/2+.10,d/2-.10);a=rng.random()*math.tau;l=rng.uniform(.035,.09)
            Q.beam('Fallow straw stalk',(x,y,soil+.006),(x+l*math.cos(a),y+l*math.sin(a),soil+.008),.002,bed,'Straw',.002)
    else:
        # Crop-spacing choices intentionally sit at the generous home-garden
        # end of Extension's production ranges, rather than filling by noise.
        if sp=='tomato':
            xs=[0] if w<2 else [-.72,.72];ys=[-.76,0,.76] if d<3 else [-2.1,-.7,.7,2.1]
            for x in xs:
                for y in ys:
                    add(sp,x,y)
                    if plot['id']%2:place('TomatoCage','Cage', (x,y,soil-.04),bed)
                    else:
                        Q.box('Tomato 1x2 wood stake',(x+.07,y,soil+.82),(.01905,.0381,1.72),bed,'Wood')
                        for z in (.45,.85,1.20):Q.ring('Loose cloth tomato tie',soil+z,.065,bed,'Straw',.003,center=(x+.025,y),segments=10)
        elif sp=='bean':
            if plot['id']%2:
                support=place('BeanTeepee','Bean teepee',(0,0,soil),bed)
                for k in range(5):
                    a=k*math.tau/5;rt=add(sp,.52*math.cos(a),.52*math.sin(a),yaw=0,variant=0)
                    # Vine follows the pole from planted foot to its apex.
                    rt.rotation_euler=Vector((-.52*math.cos(a),-.52*math.sin(a),2.12)).to_track_quat('Z','Y').to_euler()
            else:
                yaw=90 if w<2 else 0;place('BeanTrellis','Bean trellis',(0,0,soil),bed,yaw)
                for j in range(6):
                    t=-.75+j*.30;add(sp,0 if yaw else t,t if yaw else 0,yaw=yaw,variant=1)
        else:
            if sp=='squash':
                xs=[0] if w<2 else [-.65,.65];ys=[-.57,.60] if d<3 else [-1.7,0,1.7]
            else:
                spacing={'pepper':.55,'corn':.38,'lettuce':.31,'kale':.52,'herb':.42}[sp]
                nx=min(3,max(1,int((w-.38)/spacing)));ny=min(6,max(1,int((d-.38)/spacing)))
                xs=[(i-(nx-1)/2)*spacing for i in range(nx)];ys=[(i-(ny-1)/2)*spacing for i in range(ny)]
            for x in xs:
                for y in ys:
                    if plot['state']=='weedy' and rng.random()<.20:continue
                    add(sp,x,y)
        # Straw stays concentrated beneath vegetables, never a whole-site wash.
        for i in range(24 if w<2 else 50):
            x=rng.uniform(-w/2+.13,w/2-.13);y=rng.uniform(-d/2+.13,d/2-.13);a=rng.random()*6.28
            Q.beam('Plant straw mulch',(x,y,soil+.008),(x+.055*math.cos(a),y+.055*math.sin(a),soil+.009),.002,bed,'Straw',.002)
    if plot['state']=='weedy':
        for i in range(12):add('weed',rng.uniform(-w*.48,w*.48),rng.uniform(-d*.48,d*.48),2)
    # Edge flowers, with sparse sunflowers on north ends rather than every bed.
    if plot['id']%3==0 and plot['state']!='fallow':
        add('marigold',-w/2+.16,-d/2+.15,2)
        if plot['id']%2==0:add('sunflower',w/2-.22,d/2-.22,2)
    if plot['id']==3:place('Pinwheel','Garden pinwheel',(-w/2+.1,d/2-.12,soil),bed)
    # Damp, irregular soil around watered planting zones: geometry only at this
    # checkpoint, no uncaused all-over grime or final painted wear.
    if plot['state'] in ('tidy','lush'):
        for i in range(3):
            cx=rng.uniform(-w*.25,w*.25);cy=rng.uniform(-d*.35,d*.35);rad=.18
            v=[(cx,cy,soil+.012)]+[(cx+rad*rng.uniform(.65,1.15)*math.cos(j*math.tau/9),cy+rad*rng.uniform(.65,1.15)*math.sin(j*math.tau/9),soil+.012) for j in range(9)]
            Q.mesh('Watered soil around roots',v,[(0,j+1,(j+1)%9+1) for j in range(9)],bed,'WetSoil')
    Q.join(bed)


def garden(p):
    rng=random.Random(p['seed']);W,D=p['size'];rt=Q.root('Garden_'+str(p['seed']),'garden')
    rt['seed']=p['seed'];rt['archetype']=p['archetype'];rt['year']=p['year'];rt['footprint_m']=[W,D]
    ground=Q.root('GardenGround','ground',rt)
    # An aged chip surface belongs to the city lot; broad grass alleys frame
    # park/newer plots. Compacted fines form the shared accessible route.
    ma='Chip' if p['archetype']=='city' else 'Lawn'
    Q.box('Garden base',(0,0,-.035),(W,D,.07),ground,ma)
    for i,a in enumerate(p['paths']):
        x,y=a['center'];w,d=a['size'];Q.box('Main route '+str(i),(x,y,.007),(w,d,.014),ground,a['surface'])
        # Compacted path edges feather into grade rather than forming an
        # inaccessible sharp lip. The measured flat clear width stays intact.
        for side in (-1,1):
            Q.mesh('Feathered path shoulder',[(x+side*w/2,y-d/2,.014),(x+side*(w/2+.10),y-d/2,0),(x+side*(w/2+.10),y+d/2,0),(x+side*w/2,y+d/2,.014)],[(0,1,2,3)],ground,a['surface'])
    Q.join(ground)
    for plot in p['plots']:
        x,y=plot['center'];w,d=plot['width'],plot['depth']
        bed=pieces.bed(f'Plot{plot["id"]:02}',w,d,plot['board_height'],plot['edge'],plot['seed']);bed.parent=rt;bed.location=(x,y,.014)
        bed['plot_id']=plot['id'];bed['care_state']=plot['state'];bed['crop']=plot['crop']
        planted(plot,bed,rt)
        # A reachable marker, with real stake, at the front end of each plot.
        Q.box('Number marker stake',(-w/2+.15,-d/2+.07,.37),(.020,.020,.58),bed,'Wood')
        Q.box('Plot number board',(-w/2+.15,-d/2+.05,.60),(.18,.018,.12),bed,'White')
        Q.text(bed,f'{plot["id"]:02}',(-w/2+.15,-d/2+.039,.566),.073,'Steel')
        Q.socket(bed,f'Socket_Plot{plot["id"]:02}',(0,-d/2-.47,-.014))
        if plot['id']%4==0:
            # Weed cloth shows only in a narrow torn patch beside a bed.
            Q.mesh('Worn weed cloth edge',[(w/2,-.35,.009),(w/2+.12,-.28,.012),(w/2+.07,.14,.01),(w/2,.26,.009)],[(0,1,2,3)],bed,'Cloth')
        Q.join(bed)
    infrastructure=[]
    sx,sy=p['service'];shed=place('NativeShed','ToolShed',(sx,sy,0),rt);infrastructure.append(shed)
    cx,cy=p['compost'];infrastructure.append(place('CompostThreeBay','Compost',(cx,cy,0),rt))
    wx,wy=p['water'];infrastructure.append(place('Standpipe','Water',(wx,wy,0),rt,180 if wx<0 else 0))
    bx,by=p['bench'];infrastructure.append(place('ShadeBench','Bench',(bx,by,0),rt,180))
    place('RainBarrel','Rain barrel',(sx-1.65,sy,0),rt)
    # Continuous gutter/downpipe routes roof runoff into the barrel lid.
    pipe=Q.root('RainCapture','infrastructure',rt)
    Q.tube('Shed gutter and downpipe',[(sx-1.43,sy+1.5,2.30),(sx-1.43,sy,2.30),(sx-1.64,sy,2.27),(sx-1.65,sy,1.02),(sx-1.65,sy,.89)],.035,pipe,'Zinc',8);Q.join(pipe)
    place('BulletinBoard','Noticeboard',(-2,-D/2+1.0,0),rt)
    place('Bucket','Bucket',(wx-.6,wy+.25,0),rt)
    place('WateringCan','Watering can',(wx+.5,wy+.4,0),rt,35)
    place('Wheelbarrow','Wheelbarrow',(cx-1.0,cy-1.9,0),rt,-25)
    # One short row-cover is over a freshly planted plot; it never crosses a route.
    fresh=next(q for q in p['plots'] if q['state']=='new' and min(q['width'],q['depth'])<2)
    x,y=fresh['center'];place('RowCover','Row cover',(x,y,fresh['soil_z_world']-.025),rt,90 if fresh['width']>fresh['depth'] else 0)
    # Netting over a separate low crop, tied to four actual stakes. The sag
    # follows the unsupported span, and shares an otherwise unused leaf tile.
    netplot=next(q for q in p['plots'] if q['crop'] in ('lettuce','herb','kale') and q['state']!='fallow')
    nx,ny=netplot['center'];net=Q.root('BirdNet','tool',rt);net.location=(nx,ny,0)
    nw=min(netplot['width']-.12,1.0);nd=min(netplot['depth']-.12,1.85)
    for xx in (-nw/2,nw/2):
        for yy in (-nd/2,nd/2):Q.box('Net support stake',(xx,yy,.45),(.019,.019,.90),net,'Wood')
    v=[];faces=[];uv=[]
    for j in range(9):
        for i in range(7):
            u=i/6;t=j/8;z=.90-.11*math.sin(math.pi*u)*math.sin(math.pi*t)
            v.append(((u-.5)*nw,(t-.5)*nd,z));uv.append((u*nw/.48/4,.75+t*nd/.48/4))
    # Subdivide into native .48m tiles, so repeat stays in its reserved region.
    # The net is a single swatch at this checkpoint: UVs are explicitly clamped
    # to its tile below; later look-dev may allocate a metric repeat sampler.
    for j in range(8):
        for i in range(6):k=j*7+i;faces.append((k,k+1,k+8,k+7))
    me=bpy.data.meshes.new('Bird net sag');me.from_pydata(v,[],faces);me.update();ob=bpy.data.objects.new('Bird net curved alpha',me);bpy.context.collection.objects.link(ob);ob.parent=net;me.materials.append(plants.LEAF)
    layer=me.uv_layers.new(name='UVMap')
    for face in me.polygons:
        for li,(u,t) in zip(face.loop_indices,((0,0),(1,0),(1,1),(0,1))):layer.data[li].uv=(.003+u*(nw/6/.48)*.244,.753+t*(nd/8/.48)*.244)
    Q.join(net)
    fence.perimeter(p,rt)
    Q.socket(rt,'Socket_StreetEntry',(0,-D/2,0),'site_entry')
    sign=Q.root('GardenSign','infrastructure',rt)
    compact=p['archetype']=='park';span=1.05 if compact else 2.35;height=.66 if compact else .58
    for x in (3.4-span*.42,3.4+span*.42):Q.box('Garden sign ground post',(x,-D/2+.25,.95),(.0889,.0889,1.90),sign,'OldWood')
    Q.box('Garden sign boards',(3.4,-D/2+.24,1.45),(span,.0381,height),sign,'OldWood' if compact else 'Green')
    Q.text(sign,'MEADOW\nCOMMONS' if compact else p['name'],(3.4,-D/2+.218,1.49 if compact else 1.50),.105 if compact else .118,'Steel' if compact else 'White')
    Q.text(sign,'GARDEN' if compact else 'COMMUNITY GARDEN',(3.4,-D/2+.218,1.23 if compact else 1.29),.095,'Steel' if compact else 'White');Q.join(sign)
    # Give the margins living weeds: rooted clumps under posts and in corners.
    for j in range(20):
        x=(-1 if j%2 else 1)*(W/2-.16);y=rng.uniform(-D/2+.3,D/2-.4)
        Q.instance(PLANTS['weed_2_0'],'Fence foot weeds',(x,y,0),rng.random()*360,rt)
    bpy.context.view_layer.update();return rt


def main():
    a=argparse.ArgumentParser();a.add_argument('--out',default='build/gardens.blend');a.add_argument('--seeds',type=int,nargs='+',default=list(SEEDS));a.add_argument('--archetype',choices=('city','park','accessible'));args=a.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.unit_settings.system='METRIC';Q.palette()
    plants.material('textures/checkpoint');fence.material('build/context/chain')
    # Reuse native tiling sets in surface-only checkpoint roles; all three seeds
    # reference the same files. No existing map is rebaked or overwritten.
    for name in ('Lawn',):Q.M[name]=tiling.material(name,REPO/'ground/textures/ship')
    LIB.update(pieces.library());PLANTS.update(plants.library())
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(Path('build/context/shed.glb').resolve()))
    added=set(bpy.context.scene.objects)-before;root=next(o for o in added if o.parent not in added);root.name='NativeShed';LIB[root.name]=root
    modules=[*LIB.values(),*PLANTS.values()]
    counts={o.name:dict(kind=o['kind'] if 'kind' in o else 'shed',triangles=Q.count(o)) for o in modules}
    export('export/checkpoint/CommunityGardenPieces.gltf',modules)
    # Save prototypes separately to support an exported-pieces sheet.
    Path('build').mkdir(exist_ok=True);Path('build/pieces.json').write_text(json.dumps(counts,indent=2))
    for seed in args.seeds:
        p=plan(seed,args.archetype);rt=garden(p);count=Q.count(rt)
        export(f'export/checkpoint/Garden_{seed}.gltf',[rt])
        info=dict(plan=p,triangles=count,modules=counts,stage='form and construction; quick materials, no final bake')
        Path(f'build/garden-{seed}.json').write_text(json.dumps(info,indent=2));print('GARDEN',seed,count,flush=True)
        remove(rt)
    for rt in modules:remove(rt)
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(args.out).resolve()))


if __name__=='__main__':main()
