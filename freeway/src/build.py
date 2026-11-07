"""Build the family and both places; export before any image judgment."""
import argparse,sys,json,math,hashlib
from dataclasses import replace
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import geom as Q,pieces,roads,roadside,weather,site as builtin_site
import importlib.util
spec=importlib.util.spec_from_file_location('freeway_site',HERE/'site.py');site=importlib.util.module_from_spec(spec);sys.modules['freeway_site']=site;spec.loader.exec_module(site)
from plan import *
from materials import palette
from external import share,bundle

def export(path,roots):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);bpy.ops.object.select_all(action='DESELECT')
    for rt in roots:
        for ob in [rt,*rt.children_recursive]:
            if ob.type!='CURVE':ob.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLTF_SEPARATE',use_selection=True,
        export_yup=True,export_extras=True,export_animations=False,export_skins=False,export_tangents=False,
        export_texture_dir='staging',export_image_format='AUTO',export_shared_accessors=True,
        export_all_vertex_colors=False,export_vertex_color='NAME',export_vertex_color_name='Tint')
    images=share(path)
    return dict(file=str(path),triangles=sum(Q.count(r) for r in roots),gltf_bytes=path.stat().st_size,bin_bytes=path.with_suffix('.bin').stat().st_size,images=images,bundle_sha256=bundle(path))

def describe(rt):
    bpy.context.view_layer.update();points=[rt.matrix_world.inverted()@ob.matrix_world@v.co for ob in [rt,*rt.children_recursive] if ob.type=='MESH' for v in ob.data.vertices]
    return dict(triangles=Q.count(rt),bounds=[[float(op(p[k] for p in points)) for k in range(3)] for op in (min,max)] if points else [],sockets={o.name:dict(kind=o['socket_kind'],position=list(o.location)) for o in rt.children_recursive if o.get('socket_kind')},kind=rt.get('module_kind'))

def scene(p,lib):
    roots=[]
    # All authored pieces retain their construction-frame ends for chaining.
    stations=roads.seq(-p.length/2,p.length/2,JOINT*8)
    for i,(a,c) in enumerate(zip(stations,stations[1:])):
        roots.append(roads.road(p,'Road_%03d'%i,a,c))
    roots.extend([roads.terrain(p),roads.placement_wear(p)])
    paths=Q.root('DrivingPaths',module_kind='sockets');roots.append(paths)
    for side in (-1,1):
        for lane in range(2):
            pts=[p.xyz(s,p.lane(side,lane),.02) for s in roads.seq(-p.length/2,p.length/2,6.)]
            if side<0:pts.reverse()
            Q.curve(paths,'Lane_'+str(side)+'_'+str(lane),pts)
    # Median. Two F rails protect the pier footprint, with tapered split noses.
    if p.kind=='diamond':
        median=Q.root('PavedMedian',module_kind='terrain');b=Q.Batch('Median floor',median)
        for aa,cc in zip(stations,stations[1:]):
            b.face([p.xyz(aa,-p.median/2,-.006),p.xyz(aa,p.median/2,-.006),p.xyz(cc,p.median/2,-.006),p.xyz(cc,-p.median/2,-.006)],'Concrete')
        b.finish();roots.append(median)
        for i,s in enumerate(roads.seq(-p.length/2+3.048,p.length/2-3.048,6.104)):
            if abs(s)<16:
                for side in (-1,1):roots.append(site.along(lib['MedianF'],'PierProtection_%s_%03d'%(side,i),p,s,side*.85))
            else:roots.append(site.along(lib['MedianF'],'Median_%03d'%i,p,s,0))
        roots.append(site.clone(lib['Overpass'],'JuniperOverpass'))
        roots.append(roads.arterial(p));roots.append(site.terminal_signals(p));roots.append(roadside.terminal(p))
        for side in (-1,1):
            for entry in (False,True):
                roots.append(roads.ramp(p,'Ramp_%s_%s'%(side,'On' if entry else 'Off'),side,entry))
                pts=ramp_points(p,side,entry)
                roots.extend(site.rail_run(lib,'RampRail_%s_%s'%(side,entry),pts))
                # Physical nose in the widening gore, behind painted chevrons.
                if not entry:
                    roots.append(site.clone(lib['GoreAttenuator'],'GoreNose_'+str(side),(side*14.2,-side*224.,-.07),0 if side>0 else 180))
                    b=Q.Batch('Gore chevrons '+str(side));rt=Q.root('GorePaint_'+str(side),module_kind='gore');b.rt=rt
                    def point(s,u,lift=0):
                        t=(280-abs(s))/264;q=t*t*(3-2*t)
                        low=p.edge-RIGHT+LANE/2;edge=low+(p.terminal-low)*q-3.6576
                        v=max(0,min(1,(t-.1)/.9));v=v*v*(3-2*v)
                        center=low+(p.terminal-low)*q
                        hz=-.02*(center-p.median/2)+(BRIDGE_Z+.02*(p.terminal-p.median/2))*v+.073152
                        main=-.02*(p.edge-p.median/2)
                        h=main+(hz-main)*max(0,min(1,(u-p.edge)/max(.01,edge-p.edge)))
                        return (side*u,s,h+lift),edge
                    for a,c in zip(roads.seq(190,232,3),roads.seq(190,232,3)[1:]):
                        aa,ae=point(-side*a,0);cc,ce=point(-side*c,0)
                        b.surface([point(-side*a,p.edge)[0],point(-side*a,ae)[0],point(-side*c,ce)[0],point(-side*c,p.edge)[0]],'Asphalt')
                    for j in range(9):
                        s=-side*(218-j*2.2);outer=15.5+j*.40
                        b.surface([point(s,12.9,.007)[0],point(s+side*.65,12.9,.007)[0],point(s+side*1.8,outer,.007)[0],point(s+side*1.15,outer,.007)[0]],'White')
                    b.box((side*14.2,-side*224,-.12),(1.2,6.,.10),'Bridge')
                    b.finish();roots.append(rt)
        for side in (-1,1):
            guide=site.planted_truss('GuideTruss_'+str(side),p,-side*360,0 if side>0 else 180)
            # Both panels face the same-direction carriageway. The advance
            # structure stands upstream of the gore, within the added lane.
            for panel in guide.children:
                if panel.get('replaceable_panel'):
                    panel.location.x=6.1 if panel.get('legend')=='through' else 14.0 if panel.get('legend')=='exitSmall' else 12.5
                    if side<0 and panel.get('legend')=='through':pieces.change_legend(panel,'through_south')
            roots.append(guide)
        roots.append(site.row_fence(p))
    else:
        # Wide, grassy median and cable system are a visibly different section.
        median=Q.root('WideMedian',module_kind='terrain');b=Q.Batch('WideMedian__Mesh',median)
        for a,c in zip(roads.seq(-p.length/2,p.length/2,12.),roads.seq(-p.length/2,p.length/2,12.)[1:]):
            for side in (-1,1):
                b.surface([p.xyz(a,side*p.median/2,-.02),p.xyz(a,0,-.50),p.xyz(c,0,-.50),p.xyz(c,side*p.median/2,-.02)],'Lawn')
        b.finish();roots.append(median)
        for i,s in enumerate(roads.seq(-p.length/2+3.048,p.length/2-3.048,6.096)):roots.append(site.along(lib['CableBay'],'MedianCable_%03d'%i,p,s,0,-.50))
        for side in (-1,1):
            for i,s in enumerate(roads.seq(-p.length/2+3.048,p.length/2-3.048,6.096)):
                point=list(p.xyz(s,side*31));point[2]=0
                a=math.degrees(math.atan2(p.frame(s)[1][0],p.frame(s)[1][1]))
                roots.append(site.clone(lib['SoundPanel'],'SoundWall_%s_%03d'%(side,i),point,-a))
        guide=site.planted_truss('CedarGuide',p,75)
        for panel in list(guide.children):
            if not panel.get('replaceable_panel'):continue
            if panel.get('legend')=='through':panel.location.x=(p.lane(1,0)+p.lane(1,1))/2
            else:site.delete(panel)
        roots.append(guide)
        roots.append(site.row_fence(p))
    # Davits, drainage inlets, delineators, mile and speed signs.
    furniture=Q.root('RoadFurniture',module_kind='roadside');b=Q.Batch('Drainage and delineators',furniture)
    for side in (-1,1):
        for i,s in enumerate(roads.seq(-p.length/2+40,p.length/2-40,100)):
            if p.kind=='diamond' and abs(s)<40:continue
            roots.append(site.along(lib['DavitLight'],'Davit_%s_%02d'%(side,i),p,s,side*(p.edge+3.2),0,90 if side>0 else -90))
        for s in roads.seq(-p.length/2+30,p.length/2-30,60.96):
            u=side*(p.edge+1.6);point=p.xyz(s,u,-.34)
            b.box(point,(.60,.90,.12),'Bridge')
            for j in range(7):b.box((point[0]-.25+j*.08,point[1],point[2]+.065),(.025,.75,.012),'DarkSteel')
            point=p.xyz(s,side*(p.edge+.9))
            b.beam(point,(point[0],point[1],point[2]+1.05),.045,'White',.02)
            b.box((point[0],point[1]-.025,point[2]+.95),(.07,.025,.15),'Yellow')
        for s,legend,w,h in [(-65.,'speed',.9144,1.2192),(180.,'mile',.3048,1.2192)]:
            if side<0 and legend=='mile':legend='mile_south'
            point=p.xyz(s*side,side*(p.edge+2.0));rr=Q.root('RoadSign_'+str(side)+'_'+legend,point,furniture)
            bb=Q.Batch(rr.name+'__Post',rr);bb.beam((0,0,0),(0,0,3.2),.055,'Steel',.055);bb.finish()
            pieces.sign_face(rr.name+'__Panel',w,h,legend,rr,(0,-.04,2.4));rr.rotation_euler.z=0 if side>0 else math.pi
        if p.kind=='diamond':
            for offset in (-4.9,4.9):
                rr=Q.root('TerminalDoNotEnter_'+str(side)+'_'+str(offset),(side*p.terminal+offset,-side*22,7.35),furniture)
                bb=Q.Batch(rr.name+'__Post',rr);bb.beam((0,0,-.15),(0,0,3.0),.055,'Steel',.055);bb.box((0,0,-.075),(.30,.30,.15),'Bridge');bb.finish()
                pieces.sign_face(rr.name+'__Panel',.9144,.9144,'wrong',rr,(0,-.04,2.65));rr.rotation_euler.z=math.pi if side>0 else 0
            rr=Q.root('GroundExit_'+str(side),(side*16.,-side*211.,.07),furniture)
            bb=Q.Batch(rr.name+'__Posts',rr)
            for x in (-.50,.50):bb.beam((x,0,-.10),(x,0,3.0),.065,'Steel',.065)
            bb.finish();pieces.sign_face(rr.name+'__Panel',1.524,1.2192,'gore_exit',rr,(0,-.04,2.5));rr.rotation_euler.z=0 if side>0 else math.pi
    b.finish();roots.append(furniture)
    bpy.context.view_layer.update()
    soil=roadside.soil_tree();support=[]
    for rt in roots:
        if rt.get('module_kind') in ('roadway','ramp','arterial'):support.extend(roadside.seat(rt,soil))
    Path('build/edge-support-'+str(p.seed)+'.json').write_text(json.dumps(support,indent=2))
    roots.append(roadside.landscape(p))
    if getattr(Q,'LOOKDEV',False):
        roots.append(weather.paving(p))
        for rt in roots:weather.construction(rt)
    # Context and actors are delivered separately so civil cost is independently
    # measurable. Every review still imports all three exported packages.
    return roots

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seeds',nargs='+',type=int,default=[101,202]);ap.add_argument('--out',default='build/Freeway.blend');ap.add_argument('--stage',choices=('form','look'),default='look');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True);palette(a.stage);lib={r.name:r for r in pieces.library()}
    # Standalone road modules demonstrate straight, curve and bank transition.
    for name,p in [('RoadStraight',plan(101)),('RoadCurve',replace(plan(202),grade=0.))]:lib[name]=roads.road(p,name,-18.288,18.288)
    lib['RoadBankTransition']=roads.road(replace(plan(202),grade=0.),'RoadBankTransition',-18.288,18.288,bank=(-.02,-.025))
    lib['RampBranch']=roads.ramp(plan(101),'RampBranch',1,False)
    if Q.LOOKDEV:
        for r in lib.values():weather.construction(r)
    rows={n:describe(r) for n,r in lib.items()}
    for n,r in lib.items():export('export/modules/'+n+'.gltf',[r])
    for i,r in enumerate(lib.values()):r.location=(i%4*65,i//4*70,0)
    export('export/FreewayModules.gltf',list(lib.values()))
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
    # Library templates retain zero transforms when cloning into a scene.
    for r in lib.values():r.location=(0,0,0)
    for seed in a.seeds:
        p=plan(seed);roots=scene(p,lib);report=export('export/Freeway-'+str(seed)+'.gltf',roots)
        report.update(plan=p.data(),parts={r.name:describe(r) for r in roots})
        context=site.town(p);traffic=site.traffic(p)
        report['context']=export('export/Town-'+str(seed)+'.gltf',[context])
        report['traffic']=export('export/Traffic-'+str(seed)+'.gltf',[traffic])
        report['traffic']['placements']=json.loads(traffic['placements_json'])
        report['context']['placements']=json.loads(context['placements_json'])
        Path('build/scene-'+str(seed)+'.json').write_text(json.dumps(report,indent=2))
        # Native Blender curves survive in a rebuildable per-scene source.
        # Only the reusable construction library is hidden in that source.
        templates={ob:(ob.hide_render,ob.hide_viewport) for r in lib.values() for ob in [r,*r.children_recursive]}
        for ob in templates:ob.hide_render=True;ob.hide_viewport=True
        bpy.ops.wm.save_as_mainfile(filepath=str(Path('build/Freeway-'+str(seed)+'.blend').resolve()))
        for ob,(render_hidden,viewport_hidden) in templates.items():ob.hide_render=render_hidden;ob.hide_viewport=viewport_hidden
        print('FREEWAY SCENE',seed,report['triangles'],'triangles',flush=True)
        for r in [*roots,context,traffic]:site.delete(r)
    Path('build/modules.json').write_text(json.dumps(rows,indent=2))
    print('FREEWAY MODULES',len(lib),sum(r['triangles'] for r in rows.values()))
if __name__=='__main__':main()
