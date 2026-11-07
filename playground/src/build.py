"""Build the module library and three original installed sites; quick materials.

Checkpoint exports are glTF with two shared original diagnostic images. Existing
library deliveries are read-only; their canonical external images are reused.
"""
import argparse,hashlib,json,math,sys,os
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(HERE)]
import geometry as F,parts as P
from dimensions import *
from plan import site,SEEDS
from kit import model as G


def jobs():
    d=dict(RampHeadBridge=P.ramp_head_bridge,Deck72=lambda r:P.deck(r,1.8288),Barrier72=lambda r:P.barrier(r,False,1.8288),NeckGuard=P.neck_guard,Deck=P.deck,Barrier=P.barrier,InfillPanel=lambda r:P.barrier(r,True),HipRoof=P.roof,Shade=lambda r:P.roof(r,True),Stairs48=P.steps,Transfer24=P.transfer,RampSegment=P.ramp_segment,RampLanding=P.landing,InterdeckSteps=P.interdeck,RoofRiser=P.roof_riser,SlideStraight24=lambda r:P.slide(r,.6096),SlideStraight48=P.slide,SlideWave48=lambda r:P.slide(r,1.2192,'wave'),SlideWave72=lambda r:P.slide(r,1.8288,'wave'),SlideSpiral72=lambda r:P.slide(r,1.8288,'spiral'),SlideTube48=lambda r:P.slide(r,1.2192,'tube'),Arch48=P.arch,Ladder72=lambda r:P.ladder(r,1.8288),VerticalLadder48=P.ladder,ChainNet48=P.net,RockWall48=P.rock,FirePole=P.pole,OverheadLadder=P.overhead,OverheadRings=lambda r:P.overhead(r,True),PanelWheel=P.panel,PanelTic=lambda r:P.panel(r,'tic'),PanelPeriscope=lambda r:P.panel(r,'scope'),SwingArchFrame=lambda r:P.swing_frame(r,True),SwingFrame=P.swing_frame,SwingBelt=P.swing,SwingBucket=lambda r:P.swing(r,True),SpringRider=P.spring,Roundabout=P.spinner)
    for h in (.6096+1.12,1.2192+1.12,1.8288+1.12):d['Post'+str(round(h*1000))]=lambda r,h=h:P.post(r,h)
    return d


def members(root):return [root,*root.children_recursive]

def export(path,obs):
    path.parent.mkdir(parents=True,exist_ok=True);bpy.ops.object.select_all(action='DESELECT')
    for o in obs:o.select_set(True)
    # Derive tangent space on import. Blender's recalculation of one reused
    # tree tangent varies at its four-decimal rounding boundary between runs.
    # The checkpoint preserves normals/UVs; final bake validation revisits this.
    bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLTF_SEPARATE',use_selection=True,export_yup=True,export_extras=True,export_animations=False,export_tangents=False,export_attributes=True,export_all_vertex_colors=False,export_image_format='AUTO',export_texture_dir='images')
    # Canonicalize the generated quick image and any reused library images.
    # Existing image bytes are identified by hash, never re-encoded or overwritten.
    doc=json.loads(path.read_text())
    for mat in doc.get('materials',[]):
        if 'QuickChain' in mat.get('name','') or mat.get('name','') in ('Playground_Deck','Playground_Chain'):mat['alphaMode']='MASK';mat['alphaCutoff']=.45;mat['doubleSided']=True
    for mesh in doc.get('meshes',[]):
        for primitive in mesh['primitives']:
            name=doc['materials'][primitive['material']]['name']
            if 'QuickChain' in name or 'QuickPerforated' in name or doc['materials'][primitive['material']].get('extras',{}).get('tiling_vertex_tint') is False:primitive['attributes'].pop('COLOR_0',None)
    candidates=[p for folder in ('playground','ground','trees','shrubs','fences','street-furniture') for p in (ROOT/folder).glob('**/textures/ship/*.png')]
    known={hashlib.sha256(p.read_bytes()).hexdigest():p for p in candidates}
    for im in doc.get('images',[]):
        p=path.parent/im['uri'];digest=hashlib.sha256(p.read_bytes()).hexdigest()
        if digest in known:im['uri']=os.path.relpath(known[digest],path.parent)
        else:
            dst=path.parent/'images'/p.name;im['uri']='images/'+dst.name
    path.write_text(json.dumps(doc,separators=(',',':'))+'\n')
    return doc


def measure(rt):
    bpy.context.view_layer.update();ps=[o.matrix_world@v.co for o in rt.children_recursive if o.type=='MESH' for v in o.data.vertices]
    return [[float(f(p[k] for p in ps)) for k in range(3)] for f in (min,max)]


def surface(rt,plan):
    x0,y0,x1,y1=plan['surface'];N,M=44,36;vs=[];fs=[]
    # Install the border around the connected union of use zones, avoiding a
    # large empty rectangular pad. Small margins connect the neighboring zones.
    regions=[[max(x0,z['rect'][0]-.18),max(y0,z['rect'][1]-.18),min(x1,z['rect'][2]+.18),min(y1,z['rect'][3]+.18)] for z in plan['zones']]
    regions.append([-.95,y0,.95,plan['zones'][0]['rect'][1]+.2])
    xs=sorted(set([x0+(x1-x0)*i/N for i in range(N+1)]+[v for r in regions for v in (r[0],r[2])]))
    ys=sorted(set([y0+(y1-y0)*i/M for i in range(M+1)]+[v for r in regions for v in (r[1],r[3])]))
    N=len(xs)-1;M=len(ys)-1;occupied=set()
    for j in range(M):
        for i in range(N):
            x=(xs[i]+xs[i+1])/2;y=(ys[j]+ys[j+1])/2
            if any(a<=x<=c and b<=y<=d for a,b,c,d in regions):occupied.add((i,j))
    depress=[]
    for m in plan['modules']:
        if m['kind'].startswith('SwingB'):depress.append((m['pos'][0],m['pos'][1],.50,1.05,.075))
        if m['kind'].startswith('Slide'):
            h=1.8288 if '72' in m['kind'] else .6096 if '24' in m['kind'] else 1.2192;kind='spiral' if 'Spiral' in m['kind'] else 'wave' if 'Wave' in m['kind'] else 'straight';p=Vector(P.slide_path(h,kind)[-1]);t=math.radians(m['yaw']);xx=m['pos'][0]+math.cos(t)*p.x-math.sin(t)*p.y;yy=m['pos'][1]+math.sin(t)*p.x+math.cos(t)*p.y;depress.append((xx,yy,.61,.75,.065))
    for j in range(M+1):
        y=ys[j]
        for i in range(N+1):
            x=xs[i];z=-.005
            if not plan['inclusive']:
                z-=sum(d*math.exp(-((x-a)/w)**2-((y-b)/h)**2) for a,b,w,h,d in depress)
                z+=.006*math.sin(2.1*x+plan['seed'])*math.cos(2.8*y)
            vs.append((x,y,z))
    for j in range(M):
        for i in range(N):
            if (i,j) in occupied:
                a=j*(N+1)+i;fs.append((a,a+1,a+N+2,a+N+1))
    from site_surface import build as containment
    containment(rt,plan,depress)


def library():
    roots={};report={}
    for i,(name,fn) in enumerate(jobs().items()):
        rt=F.root(name);fn(rt);report[name]=F.finish(rt);roots[name]=rt
        print('PIECE',name,report[name]['triangles'],flush=True)
    return roots,report


def context(site_root,plan):
    """Reuse existing original library scripts/deliveries without editing them."""
    # Street furniture modules through their own construction functions and palette
    # adapter; no new bench/receptacle design and no unrelated family rebuild.
    import importlib.util
    def module(name,path):
        sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
    sf=module('sf_forms',ROOT/'street-furniture/src/forms.py')
    original=sys.modules.get('forms');sys.modules['forms']=sf
    pp=module('sf_pieces',ROOT/'street-furniture/src/pieces.py')
    sf.M=F.M['Frame'];sf.LAYOUT={k:[.1,.1,.9,.9] for k in ('Paint','Zinc','Rubber','Inside','Aluminum','litter')}
    def own(o,parent,finish='Paint'):
        c={'Paint':'steel','Zinc':'zinc','Aluminum':'zinc','Rubber':'rubber','Inside':'rubber'}.get(finish,'steel');return F.own(o,parent,c)
    sf.own=own
    sf.quad=lambda *args,**kwargs:None;pp.quad=sf.quad
    for name,fn,pos in [('LibraryBench',pp.bench,(-2.8,plan['walk_y']+1.22,0)),('LibraryLitter',pp.receptacle,(-4.2,plan['walk_y']+1.22,0))]:
        rt=F.root(name);rt.parent=site_root;fn(rt);F.finish(rt);rt.location=pos;rt['library_source']='street-furniture/src/pieces.py'
    if original:sys.modules['forms']=original
    else:sys.modules.pop('forms',None)
    # Existing delivered tree, including its correct alpha-cut cards. Two species.
    x0,y0,x1,y1=plan['surface'];treefiles=['PinOak','RedMaple']
    for i,(name,pos) in enumerate(zip(treefiles[:1] if plan['inclusive'] else treefiles,[(x0-2.7,y1-2,0),(x1+2.9,y1+1,0)])):
        before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(ROOT/'trees/export'/f'{name}.glb'));added=set(bpy.context.scene.objects)-before
        holder=F.root('Library_'+name);holder.parent=site_root;holder.location=pos
        for ob in sorted(added,key=lambda o:o.name):
            if ob.parent not in added:ob.parent=holder
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(ROOT/'shrubs/export/Shrubs.glb'));added=set(bpy.context.scene.objects)-before
    bush=next(o for o in added if o.name.split('.')[0]=='Boxwood');keep=set(members(bush))
    for o in added-keep:bpy.data.objects.remove(o,do_unlink=True)
    bush.parent=site_root;bush.location=(x0-1.1,plan['walk_y']+.8,0)
    # Ground is presentation geometry, yet delivered with site and shared canonical
    # tiling images. Original family shader, never its entire inspection library.
    from kit.tiling import material,world_uv
    folder=ROOT/'ground/textures/ship';base=folder/'T_Grass_BaseColor.png'
    choices=list(folder.glob('*BaseColor.png'))
    grass=next((p for p in choices if 'lawn' in p.name.lower()),None)
    mat=None
    if grass:
        key=grass.stem[2:-10];mat=material(key,folder)
    if mat is None:mat=F.M['Site']
    o=G.box('Library Ground lawn',(2,1,-.115 if plan['inclusive'] else -.20),(240,240,.20),mat,0);o.parent=site_root
    if grass:world_uv(o,4)
    else:F.own(o,site_root,(.07,.12,.027,1),'Site')
    import context as library_context
    library_context.fences(site_root,plan,F)
    library_context.light(site_root,plan,F)


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('build/Playground.blend'));p.add_argument('--seeds',default='101,202,303');p.add_argument('--lookdev',action='store_true');p.add_argument('--no-context',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.unit_settings.system='METRIC';F.init(a.lookdev);roots,report=library();out=Path('export');out.mkdir(exist_ok=True)
    # Standalone modules have ground-centered footprint origins, except explicit
    # mating interfaces (deck top / slide entrance / ramp high end / hanger axis).
    for name,rt in roots.items():export(out/(name+'.gltf'),members(rt))
    for label,names in [('ComparisonDeck',[('Deck',(0,0,.6096)),('Post1730',(-HALF,-HALF,0)),('Post1730',(HALF,-HALF,0)),('Post1730',(-HALF,HALF,0)),('Post1730',(HALF,HALF,0)),('Barrier',(0,-HALF,.6096))]),('ComparisonSwings',[('SwingFrame',(0,0,0)),('SwingBelt',(-SWING_BAY/2-SWING_SEAT_OFFSET,0,SWING_H)),('SwingBelt',(-SWING_BAY/2+SWING_SEAT_OFFSET,0,SWING_H))])]:
        rr=F.root(label)
        for i,(name,pos) in enumerate(names):c=F.clone(roots[name],label+'_'+str(i),pos);c.parent=rr
        export(out/(label+'.gltf'),members(rr))
        for o in members(rr):bpy.data.objects.remove(o,do_unlink=True)
    for i,(name,rt) in enumerate(roots.items()):
        z=SWING_H if name in ('SwingBelt','SwingBucket') else .6 if name.startswith('Deck') or name=='RampSegment' else 1.0 if name in ('HipRoof','Shade') else 0
        rt.location=((i%7)*7,(i//7)*7,z)
    export(out/'PlaygroundPieces.gltf',[o for rt in roots.values() for o in members(rt)])
    a.out.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(a.out.resolve()))
    # Templates stay offstage; each site is independently selected for export.
    manifests=[]
    for seed in map(int,a.seeds.split(',')):
        plan=site(seed);rt=F.root('Playground'+str(seed));placed=[]
        for i,m in enumerate(plan['modules']):
            c=F.clone(roots[m['kind']],f'{m["kind"]}_{i:03}',m['pos'],m['yaw'],tint=plan);c.parent=rt;c['zone_group']=m['group'];placed.append(c)
        bpy.context.view_layer.update()
        composite=[o for o in placed if o['zone_group']=='composite'];pts=[o.matrix_world@v.co for r in composite for o in r.children_recursive if o.type=='MESH' for v in o.data.vertices]
        bb=[min(p.x for p in pts),min(p.y for p in pts),max(p.x for p in pts),max(p.y for p in pts)]
        plan['zones'].insert(0,dict(name='Connected composite 6ft envelope',group='composite',rect=[bb[0]-USE,bb[1]-USE,bb[2]+USE,bb[3]+USE],rule='CPSC 5.3.9; conservative bounding envelope'))
        ground=F.root('Siteworks');ground.parent=rt;surface(ground,plan);F.finish(ground)
        if a.lookdev:
            from labels import build as labels
            labels(rt,plan)
        if not a.no_context:context(rt,plan)
        if plan['year']==1996:
            F.empty(rt,'SchoolBuildingEdgeSocket',(0,plan['surface'][3]+16,0),'school_building_edge')
        bpy.context.view_layer.update()
        # Export only each site, never offstage templates or prior seeds.
        doc=export(out/f'Playground-{seed}.gltf',members(rt));plan['equipment_triangles']=sum(report[m['kind']]['triangles'] for m in plan['modules']);plan['total_triangles']=sum(len(o.data.loop_triangles) for o in rt.children_recursive if o.type=='MESH' and not o.data.calc_loop_triangles())
        plan['parts']=[dict(**m,triangles=report[m['kind']]['triangles']) for m in plan['modules']];plan['materials']=len(doc.get('materials',[]));plan['images']=[im['uri'] for im in doc.get('images',[])];plan['bounds_m']=measure(rt)
        manifests.append(plan);(out/f'Playground-{seed}.json').write_text(json.dumps(plan,indent=2));print('SITE',seed,plan['equipment_triangles'],plan['total_triangles'],flush=True)
        for o in members(rt):bpy.data.objects.remove(o,do_unlink=True)
    # Remove exporter staging copies of maps whose URI is canonical elsewhere.
    used={(p.parent/im['uri']).resolve() for p in out.glob('*.gltf') for im in json.loads(p.read_text()).get('images',[])}
    for p in (out/'images').glob('*.png'):
        if p.resolve() not in used:p.unlink()
    (Path('build')/'manifest.json').write_text(json.dumps(dict(stage='baked shared manufacture charts / look-dev checkpoint' if a.lookdev else 'form and construction checkpoint; no bake',pieces=report,sites=manifests),indent=2))

if __name__=='__main__':main()
