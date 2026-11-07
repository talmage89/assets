"""Build the family and both places; export before any image judgment."""
import argparse,sys,json,math,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import geom as Q,pieces,roads,site as builtin_site
import importlib.util
spec=importlib.util.spec_from_file_location('freeway_site',HERE/'site.py');site=importlib.util.module_from_spec(spec);spec.loader.exec_module(site)
from plan import *
from materials import palette
from external import share,bundle

def export(path,roots):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);bpy.ops.object.select_all(action='DESELECT')
    for rt in roots:
        for ob in [rt,*rt.children_recursive]:
            if ob.type!='CURVE':ob.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLTF_SEPARATE',use_selection=True,
        export_yup=True,export_extras=True,export_animations=False,export_skins=False,export_tangents=True,
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
        roots.append(roads.arterial(p));roots.append(site.terminal_signals(p))
        for side in (-1,1):
            for entry in (False,True):
                roots.append(roads.ramp(p,'Ramp_%s_%s'%(side,'On' if entry else 'Off'),side,entry))
                pts=ramp_points(p,side,entry)
                for j in range(1,len(pts)-1,3):
                    point=Vector(pts[j]);d=Vector(pts[j+1])-Vector(pts[j-1]);n=Vector((d.y,-d.x,0)).normalized()
                    point+=n*4.9;point.z-=.08
                    roots.append(site.clone(lib['WBeam'],'RampRail_%s_%s_%03d'%(side,entry,j),point,math.degrees(math.atan2(-d.x,d.y))))
                # Physical nose in the widening gore, behind painted chevrons.
                if not entry:
                    roots.append(site.clone(lib['GoreAttenuator'],'GoreNose_'+str(side),(side*15.5,-side*241.,-.12),0 if side>0 else 180))
                    b=Q.Batch('Gore chevrons '+str(side));rt=Q.root('GorePaint_'+str(side),module_kind='gore');b.rt=rt
                    for j in range(9):
                        s=-side*(246-j*2.2);outer=15.0+j*.40
                        b.face([p.xyz(s,side*12.9,.009),p.xyz(s+.65,side*12.9,.009),p.xyz(s+1.8,side*outer,.009),p.xyz(s+1.15,side*outer,.009)],'White')
                    b.finish();roots.append(rt)
        for side in (-1,1):
            roots.append(site.clone(lib['SignTruss'],'GuideTruss_'+str(side),(0,-side*155,0),0 if side>0 else 180))
            roots.append(site.clone(lib['GuardrailEnd'],'ShoulderEnd_'+str(side),(side*14.0,-side*80,-.24),0 if side>0 else 180))
        roots.append(site.row_fence(p))
    else:
        # Wide, grassy median and cable system are a visibly different section.
        median=Q.root('WideMedian',module_kind='terrain');b=Q.Batch('WideMedian__Mesh',median)
        for a,c in zip(roads.seq(-p.length/2,p.length/2,12.),roads.seq(-p.length/2,p.length/2,12.)[1:]):
            b.face([p.xyz(a,-p.median/2,-.02),p.xyz(a,p.median/2,-.02),p.xyz(c,p.median/2,-.02),p.xyz(c,-p.median/2,-.02)],'Lawn')
        b.finish();roots.append(median)
        for i,s in enumerate(roads.seq(-p.length/2+3.048,p.length/2-3.048,6.096)):roots.append(site.along(lib['CableBay'],'MedianCable_%03d'%i,p,s,0))
        for side in (-1,1):
            for i,s in enumerate(roads.seq(-p.length/2+3.048,p.length/2-3.048,6.096)):
                point=list(p.xyz(s,side*31));point[2]=0
                a=math.degrees(math.atan2(p.frame(s)[1][0],p.frame(s)[1][1]))
                roots.append(site.clone(lib['SoundPanel'],'SoundWall_%s_%03d'%(side,i),point,-a))
        roots.append(site.clone(lib['SignTruss'],'CedarGuide',p.xyz(75,0),-math.degrees(75/p.radius)))
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
            point=p.xyz(s*side,side*(p.edge+2.0));rr=Q.root('RoadSign_'+str(side)+'_'+legend,point,furniture)
            bb=Q.Batch(rr.name+'__Post',rr);bb.beam((0,0,0),(0,0,3.2),.055,'Steel',.055);bb.finish()
            pieces.sign_face(rr.name+'__Panel',w,h,legend,rr,(0,-.04,2.4));rr.rotation_euler.z=0 if side>0 else math.pi
    b.finish();roots.append(furniture)
    roots.extend([site.town(p),site.traffic(p)])
    return roots

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seeds',nargs='+',type=int,default=[101,202]);ap.add_argument('--out',default='build/Freeway.blend');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True);palette();lib={r.name:r for r in pieces.library()}
    # Standalone road modules demonstrate straight, curve and bank transition.
    for name,p in [('RoadStraight',plan(101)),('RoadCurve',plan(202))]:lib[name]=roads.road(p,name,-18.288,18.288)
    lib['RoadBankTransition']=roads.road(plan(202),'RoadBankTransition',-18.288,18.288,bank=(-.02,-.04))
    lib['RampBranch']=roads.ramp(plan(101),'RampBranch',1,False)
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
        Path('build/scene-'+str(seed)+'.json').write_text(json.dumps(report,indent=2))
        print('FREEWAY SCENE',seed,report['triangles'],'triangles',flush=True)
        for r in roots:site.delete(r)
    Path('build/modules.json').write_text(json.dumps(rows,indent=2))
    print('FREEWAY MODULES',len(lib),sum(r['triangles'] for r in rows.values()))
if __name__=='__main__':main()
