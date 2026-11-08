"""Form checkpoint: module library, two garages, shared external glTF images."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import bpy
import bmesh
from mathutils import Vector,Quaternion
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path[:0]=[str(ROOT),str(HERE)]
import geometry as G
import pieces
from plan import garage,deck_z,ramp_fraction,end_fade,ground_lane_offset,TEE,SPAN,FLOOR,STALL,DEPTH,AISLE
from graphics import generate
from kit import tiling


def members(r):return [r,*r.children_recursive]


def export(path,obs,extra_images=()):
    """Use the existing kit GLB exporter, then split without reencoding images."""
    import copy
    from kit.gltf import GLB
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=Path('build/embedded')/path.with_suffix('.glb').name
    tiling.export(tmp,obs);g=GLB(tmp);doc=g.json;binary=g.binary
    known={hashlib.sha256(p.read_bytes()).hexdigest():p for folder in (ROOT/'ground/textures/ship',ROOT/'street-light/textures/ship',ROOT/'cars/textures/sedan/ship',ROOT/'trees/textures/ship',ROOT/'trees/textures/oak/ship') for p in folder.glob('*.png')}
    known.update({hashlib.sha256(p.read_bytes()).hexdigest():p for p in Path('textures/checkpoint').rglob('*.png')})
    known.update({hashlib.sha256(p.read_bytes()).hexdigest():p for p in extra_images})
    for im in doc.get('images',[]):
        v=doc['bufferViews'][im.pop('bufferView')];a=v.get('byteOffset',0);payload=binary[a:a+v['byteLength']]
        h=hashlib.sha256(payload).hexdigest();assert h in known,im
        im['uri']=os.path.relpath(known[h],path.parent);im.pop('mimeType',None)
    used=sorted({a['bufferView'] for a in doc.get('accessors',[])});output=bytearray();remap={};views=[]
    for i in used:
        output.extend(b'\0'*(-len(output)%4));v=copy.deepcopy(doc['bufferViews'][i]);a=v.get('byteOffset',0)
        payload=binary[a:a+v['byteLength']];v.update(buffer=0,byteOffset=len(output));output.extend(payload);remap[i]=len(views);views.append(v)
    for a in doc.get('accessors',[]):a['bufferView']=remap[a['bufferView']]
    doc['bufferViews']=views;doc['buffers']=[dict(uri=path.with_suffix('.bin').name,byteLength=len(output))]
    path.with_suffix('.bin').write_bytes(output);path.write_text(json.dumps(doc,separators=(',',':'))+'\n')
    return dict(triangles=G.triangles(obs),materials=len(doc.get('materials',[])),
                gltf_bytes=path.stat().st_size,bin_bytes=len(output),glb_bytes=tmp.stat().st_size,
                images=[i['uri'] for i in doc.get('images',[])])


def bay_surface(name,r,x0,x1,y0,y1,z,thickness=.22,mat='Deck'):
    b=G.Mesh(name,r);ys=[y0,(y0+y1)/2,y1]
    for a,c in zip(ys,ys[1:]):
        top=[(x0,a,z(x0,a)),(x1,a,z(x1,a)),(x1,c,z(x1,c)),(x0,c,z(x0,c))]
        b.prism([(x,y,zz-thickness) for x,y,zz in top],(0,0,thickness),mat)
    return b.finish()


def make_garage(p,templates,layout):
    rt=G.root('Garage_'+str(p['seed']),system=p['system'],stage='FORM CHECKPOINT / QUICK MATERIALS')
    rows=[];L,W=p['length'],p['width'];municipal=p['system']=='precast';a,b=p['ramp_limits'];joint=p['joint_y'];shafts=set();supports={}
    def put(kind,name,pos=(0,0,0),yaw=0,xf=None):
        rr=G.clone(templates[kind],name,pos,yaw,rt,xf);rr['module_kind']=kind
        rows.append(dict(name=name,kind=kind,position=list(pos),yaw=yaw,triangles=G.triangles(members(rr))))
        return rr
    # Exposed grade slab is only under the flat parking bay, not under the
    # dedicated ramp void. End platforms provide the actual level connections.
    for level in range(p['levels']):
        for ramp in (False,True):
            cy=p['ramp_y'] if ramp else p['flat_y'];width=p['ramp_width'] if ramp else SPAN
            lo,hi=cy-width/2,cy+width/2
            def height(lev,x,y,central=False):
                return lev*FLOOR+(FLOOR*ramp_fraction(x,p) if central else 0)+.01*(width/2-abs(y-cy))*end_fade(p,x)
            if not ramp and level==0:
                for k,(g0,g1) in enumerate(zip((-L/2,a,b),(a,b,L/2))):
                    bay_surface('Grade slab '+str(k),rt,g0,g1,lo,hi,lambda x,y:deck_z(p,level,x,y),.16)
            # Each 12ft station is a real placed module. Slopes and drainage
            # are transformed into owned vertices, with unchanged UV charts.
            for station in range(p['tee_count']):
                x=-L/2+(station+.5)*TEE
                central=ramp and a<x<b
                if central and level==p['levels']-1:continue
                if ramp and not municipal:
                    # Narrow speed-ramp strips retain 24ft clear two-way width.
                    z=lambda xx,yy:height(level,xx,yy,central)
                    cuts=sorted({x-TEE/2,x+TEE/2,*[v for v in (a+p['transition'],b-p['transition']) if x-TEE/2<v<x+TEE/2]})
                    for k,(c0,c1) in enumerate(zip(cuts,cuts[1:])):
                        ob=bay_surface(f'SpeedRamp_L{level}_{station}_{k}',rt,c0,c1,lo,hi,z,.25)
                        rows.append(dict(name=ob.name,kind='SpeedRamp',position=[x,cy,level*FLOOR],yaw=0,triangles=G.triangles([ob])))
                elif level>0 or central:
                    def xf(v,x=x,cy=cy,central=central,level=level,ramp=ramp):
                        vy=v.y;zz=v.z+height(level,x+v.x,cy+v.y,central)-level*FLOOR
                        # The inner L girder is inboard of the nominal 60ft
                        # parking line. Shorten the tee body to its seat while
                        # a real thick closure pour completes the deck edge.
                        if municipal and v.z<=-.049 and ((not ramp and v.y>0) or (ramp and v.y<0)):
                            vy-=math.copysign(.43*abs(v.y)/(SPAN/2-.22),v.y)
                        # Flat pad bottom on the sloping ledge; retain its
                        # slightly compressed/graded top under the tee stem.
                        if municipal and v.z<-.67:
                            zz-=.0004+.01*(SPAN/2-abs(v.y))*end_fade(p,x+v.x)
                        return Vector((v.x,vy,zz))
                    put('DoubleTee' if municipal else 'PTSlab',f'{"Ramp" if ramp else "Flat"}_L{level+1}_T{station:02d}',(x,cy,level*FLOOR),xf=xf)
                    if municipal:
                        y0,y1=(joint+.025,joint+.74) if ramp else (joint-.74,joint-.025)
                        bay_surface(f'Inner closure pour {level} {ramp} {station}',rt,x-TEE/2,x+TEE/2,y0,y1,lambda xx,yy:height(level,xx,yy,central),.15)
                elif ramp:
                    bay_surface(f'North end grade {station}',rt,x-TEE/2,x+TEE/2,lo,hi,lambda xx,yy:height(0,xx,yy),.16)
                # Fixtures live between stem rows; their mounting backs touch
                # the slab underside, and protected conduit follows a beam.
                if level<p['levels']-(2 if central else 1) and station%2==0:
                    for yy in (cy-2.5,cy+2.5) if municipal or not ramp else (cy,):
                        zz=height(level+1,x,yy,central)-(.55 if municipal else .32)
                        put('Fixture',f'Fixture_{level}_{ramp}_{station}_{yy:.1f}',(x,yy,zz))
            # Beams/columns along each independent span edge, paired about
            # the center expansion gap when flat and sloping decks diverge.
            for side in (-1,1):
                yy=cy+side*width/2
                if municipal and abs(yy-joint)<1e-5:yy+=(-.43 if not ramp else .43)
                edge_yaw=0
                grid=p['structural_stations']
                for x in grid:
                    # The central column is shared, with two differently
                    # elevated corbel rows; duplicated offset shafts would
                    # project through the parked cars' bumper envelopes.
                    shafts.add((x,cy+side*width/2))
                if not municipal:continue
                for i,(x0,x1) in enumerate(zip(grid,grid[1:])):
                    if x1-x0<1:continue
                    x=(x0+x1)/2
                    central=ramp and a<x<b
                    if (level==0 and not central) or (central and level==p['levels']-1):continue
                    # Length is scaled only along beam axis; slopes remain
                    # real placement geometry rather than object transforms.
                    def xf(v,x=x,x0=x0,x1=x1,central=central,cy=cy,side=side):
                        xx=v.x*(x1-x0-.82)/(3*TEE-.82)
                        return Vector((xx,-v.y if side==-1 else v.y,v.z+height(level,x+xx,cy+side*width/2,central)-level*FLOOR))
                    put('LBeam' if municipal else 'PTBeam',f'Girder_{level}_{ramp}_{side}_{i}',(x,yy,level*FLOOR),edge_yaw,xf)
                    for endx in (x0,x1):
                        elevation=level*FLOOR+(FLOOR*ramp_fraction(endx,p) if central else 0)
                        key=(round(endx,5),round(yy,5),round(elevation,5))
                        if key not in supports or central:
                            supports[key]=dict(x=endx,y=yy,level=level,ramp=central)
            if not municipal and (level>0 or ramp):
                # Long-span cast PT beams run ACROSS the parking bay. The
                # slab spans the 36ft distance between these transverse beams.
                for i,xx in enumerate(p['structural_stations']):
                    central=ramp and a<xx<b
                    if (level==0 and not central) or (central and level==p['levels']-1):continue
                    def xf(v,xx=xx,cy=cy,width=width,central=central):
                        localx=v.x*width/SPAN
                        return Vector((localx,v.y,v.z+height(level,xx,cy+localx,central)-level*FLOOR))
                    put('PTBeam',f'PT transverse beam {level} {ramp} {i}',(xx,cy,level*FLOOR),90,xf)
        # The end decks above are the same tees as the main bay. Guard the
        # unused high-level north-west landing instead of leaving an edge drop.
        if level==p['levels']-1:
            gb=G.Mesh('Roof west ramp termination guard',rt)
            gb.box((a,p['ramp_y'],level*FLOOR+.55),(.22,p['ramp_width'],1.10));gb.finish()
        joint_cover=G.Mesh(f'End expansion covers {level}',rt)
        for x0,x1 in ((-L/2,a),(b,L/2)):
            joint_cover.box(((x0+x1)/2,joint,level*FLOOR-.001),(x1-x0,.12,.006),'Seal')
        joint_cover.finish()
        if level<p['levels']-1:
            for xx,landing in ((a,level),(b,level+1)):
                def seam_z(x,y,landing=landing):
                    return landing*FLOOR+.01*(p['ramp_width']/2-abs(y-p['ramp_y']))*end_fade(p,x)+.002
                bay_surface(f'Ramp landing seal {level} {xx}',rt,xx-.02,xx+.02,joint,W/2,seam_z,.012,'Seal')
        # Facade spandrels on front and rear; top deck stays open to sky.
        for side in (-1,1):
            yy=side*W/2
            extra=[a+p['transition'],b-p['transition']] if side==1 and not municipal else []
            edges=sorted({*p['structural_stations'],*extra})
            for i,(x0,x1) in enumerate(zip(edges,edges[1:])):
                xx=(x0+x1)/2
                if level==0 and side==-1 and xx>L/2-p['end_length']-3:continue
                ramp=side==1 and a<xx<b
                if ramp and level==p['levels']-1:continue
                def xf(v,xx=xx,x0=x0,x1=x1,ramp=ramp,side=side):
                    vx=v.x*(x1-x0)/(3*TEE)
                    return Vector((vx,v.y,v.z+(FLOOR*ramp_fraction(xx+vx,p) if ramp else 0)))
                put('Spandrel' if municipal else 'PTGuard',f'Facade_{level}_{side}_{i}',(xx,yy,level*FLOOR),0,xf)
        # End guards leave street entry at grade and stair thresholds clear.
        for ramp_side in (False,True):
            if ramp_side and level==p['levels']-1:continue
            for i,(x0,x1) in enumerate(zip(edges,edges[1:])):
                xx=(x0+x1)/2
                if not a<xx<b:continue
                def xf(v,xx=xx,x0=x0,x1=x1,ramp_side=ramp_side):
                    vx=v.x*(x1-x0)/(3*TEE)
                    return Vector((vx,v.y,v.z+(FLOOR*ramp_fraction(xx+vx,p) if ramp_side else 0)))
                put('CableBarrier',f'Center guard {level} {ramp_side} {i}',(xx,joint+(.25 if ramp_side else -.25),level*FLOOR),xf=xf)
        if level>0:
            for side in (-1,1):
                mb=G.Mesh(f'End guard {level} {side}',rt)
                tower_y=p['towers'][0 if side==-1 else 1][1]
                for y0,y1 in ((-W/2,tower_y-2.85),(tower_y+2.85,joint),(joint,W/2)):
                    mb.box((side*L/2,(y0+y1)/2,level*FLOOR+.55),(.24,y1-y0,1.10))
                mb.finish()
        # Expansion line and transverse pour strips at structural grid.
        for x in p['structural_stations'][1:-1]:
            bay_surface(f'Pour joint {level} {x}',rt,x-.0115,x+.0115,-W/2,joint,lambda xx,yy:deck_z(p,level,xx,yy)+.003,.006,'Seal')
    for i,(xx,yy) in enumerate(sorted(shafts)):
        h=(p['levels']-1)*FLOOR
        if abs(yy-W/2)<1e-4 and a<xx<b:h=(p['levels']-2)*FLOOR+FLOOR*ramp_fraction(xx,p)
        rr=G.root(f'ColumnShaft_{i:03d}',parent=rt,module_kind='ColumnShaft')
        pieces.column_body(rr,h).finish();rr.location=(xx,yy,0)
        rows.append(dict(name=rr.name,kind='ColumnShaft',position=[xx,yy,0],yaw=0,triangles=G.triangles(members(rr))))
    for i,support in enumerate(supports.values()):
        xx,yy= support['x'],support['y'];lev=support['level'];ramped=support['ramp']
        def xf(v,xx=xx,ramped=ramped):return Vector((v.x,v.y,v.z+(FLOOR*ramp_fraction(xx+v.x,p) if ramped else 0)))
        rr=put('CorbelPair',f'BearingCorbels_{i:03d}',(xx,yy,(lev-1)*FLOOR),xf=xf)
        # The lowest ramp enters retained grade. Remove buried bearing faces
        # rather than shipping a second invisible foundation under the ramp.
        cut=-rr.location.z
        for ob in list(rr.children_recursive):
            if ob.type!='MESH':continue
            if max(v.co.z for v in ob.data.vertices)<=cut:
                bpy.data.objects.remove(ob,do_unlink=True);continue
            if min(v.co.z for v in ob.data.vertices)>=cut:continue
            bm=bmesh.new();bm.from_mesh(ob.data)
            bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=(0,0,cut),plane_no=(0,0,1),clear_inner=True)
            bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0)
            bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));uv=bm.loops.layers.uv.verify()
            for face in bm.faces:
                if all(abs(v.co.z-cut)<1e-6 for v in face.verts):
                    for loop in face.loops:loop[uv].uv=(loop.vert.co.x/3.048,loop.vert.co.y/3.048)
            bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free();ob.data.update()
        rows[-1]['triangles']=G.triangles(members(rr))
        if not rows[-1]['triangles']:
            rows.pop();bpy.data.objects.remove(rr,do_unlink=True)
    for i,pos in enumerate(p['towers']):
        kind='Tower' if p['levels']==4 else 'Tower'+str(p['levels'])
        put(kind,f'Tower_{i+1}',pos,-90 if i==0 else 90)
        # Diaphragm collector plates into the concrete stair/lift cores.
        # The precast beam seats are pinned; the cores provide the authored
        # lateral system rather than pretending these joints are moment frames.
        ties=G.Mesh(f'Tower {i+1} diaphragm keys',rt);side=-1 if i==0 else 1
        for lev in range(1,p['levels']):
            for yy in (pos[1]-2.38,pos[1]+2.38):
                ties.box((side*(L/2-.10),yy,lev*FLOOR-.016),(.42,.24,.032),'Steel')
                ties.box((side*(L/2-.10),yy,lev*FLOOR-.14),(.032,.24,.25),'Steel')
        ties.finish()
    # Native roof luminaires ship with the garage, sharing their original maps.
    before=set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=str(ROOT/'street-light/export/StreetLight.glb'))
    added=set(bpy.context.scene.objects)-before
    lr=G.root('Roof pole template')
    for ob in added:
        if ob.parent not in added:ob.parent=lr
    for i,x in enumerate((-L/3,L/3)):
        G.clone(lr,'NativeRoofLight_'+str(i),(x,-W/2+.5,(p['levels']-1)*FLOOR),0,rt)
    for ob in members(lr):bpy.data.objects.remove(ob,do_unlink=True)
    # Every stall retains an engine socket; cars are separate actors.
    marks=G.Mesh('Parking markings and signs',rt)
    for index,s in enumerate(p['stalls']):
        x,y,z=s['x'],s['y'],s['z'];row=-1 if s['yaw']==180 else 1;dep=s['depth']
        root=G.root('Stall_'+s['id'],(x,y,z),rt,socket_kind='parked_car',yaw_degrees=s['yaw'],width_m=s['width'],depth_m=s['depth'],occupied=s['occupied'],level=s['level'],paint_number=s['paint_number'])
        root.rotation_mode='QUATERNION'
        normal=Vector((-s['slope_x'],-s['crossfall'],1)).normalized()
        root.rotation_quaternion=Vector((0,0,1)).rotation_difference(normal)@Quaternion((0,0,1),math.radians(s['yaw']))
        for xx in (x-s['width']/2,x+s['width']/2):
            y0,y1=y-dep/2,y+dep/2
            marks.quad([(xx-.05,y0,deck_z(p,s['level'],xx,y0,s['ramp'])+.006),(xx+.05,y0,deck_z(p,s['level'],xx,y0,s['ramp'])+.006),(xx+.05,y1,deck_z(p,s['level'],xx,y1,s['ramp'])+.006),(xx-.05,y1,deck_z(p,s['level'],xx,y1,s['ramp'])+.006)])
        wy=y+row*(dep/2-.90)
        stop=put('WheelStop','Stop_'+s['id'],(x,wy,deck_z(p,s['level'],x,wy,s['ramp'])))
        stop.rotation_mode='QUATERNION';stop.rotation_quaternion=Vector((0,0,1)).rotation_difference(normal)
        rows[-1]['rotation_quaternion']=list(stop.rotation_quaternion)
        num=s['paint_number'];ny=y-row*(dep/2-.45)
        number_vertices=[(x-.34,ny-.18,deck_z(p,s['level'],x-.34,ny-.18,s['ramp'])+.008),
                    (x+.34,ny-.18,deck_z(p,s['level'],x+.34,ny-.18,s['ramp'])+.008),
                    (x+.34,ny+.18,deck_z(p,s['level'],x+.34,ny+.18,s['ramp'])+.008),
                    (x-.34,ny+.18,deck_z(p,s['level'],x-.34,ny+.18,s['ramp'])+.008)]
        if row<0:number_vertices=number_vertices[2:]+number_vertices[:2]
        marks.quad(number_vertices,layout[num],'Graphics')
        if s['compact']:
            yy=y-row*(dep/2-1.15)
            marks.quad([(x-.8,yy-.19,deck_z(p,s['level'],x-.8,yy-.19)+.009),(x+.8,yy-.19,deck_z(p,s['level'],x+.8,yy-.19)+.009),(x+.8,yy+.19,deck_z(p,s['level'],x+.8,yy+.19)+.009),(x-.8,yy+.19,deck_z(p,s['level'],x-.8,yy+.19)+.009)],layout['COMPACT'],'Graphics')
        if s['accessible']:
            marks.geom([(x+u,y+v,deck_z(p,0,x+u,y+v)+.009) for u,v in ((-.65,-.65),(.65,-.65),(.65,.65),(-.65,.65))],[(0,1,2,3)],'Blue')
            # Shared 60in aisles: hatch once per pair.
            if s['id'].endswith(('1','3','5')):
                left,right=s['access_aisle']
                for j in range(13):
                    yy=y-DEPTH/2+j*DEPTH/13
                    marks.quad([(xx,yyy,deck_z(p,0,xx,yyy)+.010) for xx,yyy in ((left,yy),(left+.08,yy),(right,yy+.85),(right-.08,yy+.85))])
            # Standard blue sign with an original geometric wheelchair glyph.
            sg=G.Mesh('Accessible sign '+s['id'],rt);sy=y-dep/2-.20
            sx=s['access_aisle'][0]-.10 if int(s['id'].split('-')[-1])%2 else s['access_aisle'][1]+.10
            sg.tube([(sx,sy,0),(sx,sy,2.35)],.025,'Steel');sg.box((sx,sy,2.07),(.34,.035,.48),'Blue')
            sg.quad([(sx-.13,sy-.0185,1.94),(sx+.13,sy-.0185,1.94),(sx+.13,sy-.0185,2.20),(sx-.13,sy-.0185,2.20)],layout['♿'],'Graphics')
            if s.get('van'):
                sg.box((sx,sy,1.70),(.60,.035,.20),'Blue')
                sg.quad([(sx-.29,sy-.0185,1.61),(sx+.29,sy-.0185,1.61),(sx+.29,sy-.0185,1.79),(sx-.29,sy-.0185,1.79)],layout['VAN ACCESSIBLE'],'Graphics')
            sg.finish()
    # Arrows are original cut polygons, using Ground's paint chart.
    for level in range(p['levels']):
        for xx in (-L/4,L/4):
            poly=[(-1.1,-.12),(.3,-.12),(.3,-.40),(1.1,0),(.3,.40),(.3,.12),(-1.1,.12)]
            for ramped in (False,True):
                if ramped and level==p['levels']-1:continue
                cy=p['ramp_y'] if ramped else p['flat_y']+(ground_lane_offset(p,xx) if level==0 else 0)
                for lane in (-1,1):
                    direction=-lane;yy=cy+lane*AISLE/4
                    vs=[(xx+direction*x,yy+direction*y,deck_z(p,level,xx+direction*x,yy+direction*y,ramped)+.009) for x,y in poly]
                    uv=[(.04+(x+1.1)/2.2*.42,.81+(y+.4)/.8*.14) for x,y in poly]
                    marks.geom(vs,[tuple(range(7))],'GroundTrim',uv)
        for i,x in enumerate((-L/3,0,L/3)):
            for yy in (-W/2+.5,joint-.5):put('Drain',f'Drain_{level}_{i}_{yy:.1f}',(x,yy,deck_z(p,level,x,yy)+.002))
    marks.finish()
    # Entry slots in the end bay keep all queuing on property.
    ex=L/2-p['end_length']/2
    apron=G.Mesh('Private entry and accessible street walk',rt)
    if municipal:
        inner=6.1-1.8288
        apron.box((0,-W/2-inner/2,-.08),(L+10,inner,.16),'GroundConcrete')
        for x0,x1 in ((-L/2-5,ex-4.9),(ex+4.9,L/2+5)):
            apron.box(((x0+x1)/2,-W/2-(6.1+inner)/2,-.08),(x1-x0,1.8288,.16),'GroundConcrete')
        for x0,x1,z0,z1 in ((ex-4.9,ex-3.9,0,-.14605),(ex-3.9,ex+3.9,-.14605,-.14605),(ex+3.9,ex+4.9,-.14605,0)):
            apron.prism([(x0,-W/2-6.1,z0-.16),(x1,-W/2-6.1,z1-.16),(x1,-W/2-inner,-.16),(x0,-W/2-inner,-.16)],(0,0,.16),'GroundConcrete')
    else:apron.box((0,-W/2-3.05,-.08),(L+10,6.1,.16),'GroundConcrete')
    for side in (-1,1):apron.box((side*(L/2+2.7),-W/2+5,-.08),(5.4,10,.16),'GroundConcrete')
    apron.finish()
    islands=G.Mesh('Entry control islands',rt)
    for i,dx in enumerate((-1.65,1.65)):
        lane=ex+dx;floor=0;side=-1 if i==0 else 1
        islands.box((lane+side*1.8,-W/2-1.75,floor+.075),(.65,6.3,.15))
        # Full-length arms open in the uncovered apron, not through a deck.
        put('Gate',f'{"Entry" if i==0 else "Exit"}_Gate',(lane+side*1.57,-W/2-.8,floor+.15),0 if i==0 else 180)
        put('Ticket',f'Ticket_{i}',(lane+side*1.8,-W/2+(-2.7 if i==0 else 1.1),floor+.15),90 if i==0 else -90)
    islands.box((ex,-W/2-1.75,.075),(.40,5.3,.15))
    islands.finish()
    put('PayStation','PedestrianPay',(p['towers'][0][0]-1.5,-W/2-1.3,0))
    gy=-W/2-5.3
    gantry_grade=-.14605*(5.3-(6.1-1.8288))/1.8288 if municipal else 0
    head=G.Mesh('Entry gantry and signs',rt,xf=lambda v:Vector((v[0],v[1],v[2]+gantry_grade)))
    for x in (ex-3.45,ex+3.45):head.box((x,gy,1.75),(.14,.14,3.5),'Steel')
    head.box((ex,gy,3.40),(7.0,.18,.20),'Steel')
    # Hanging bar lower edge measured at precisely 98in above route grade.
    head.box((ex,gy,2.4892+.06),(6.7,.10,.12),'Yellow')
    for x in (ex-2.7,ex+2.7):head.tube([(x,gy,2.61),(x,gy,3.3)],.006,'Steel',6)
    head.quad([(ex-2.7,gy-.096,2.66),(ex+2.7,gy-.096,2.66),(ex+2.7,gy-.096,3.07),(ex-2.7,gy-.096,3.07)],layout['CLEARANCE  8 FT 2 IN'],'Graphics')
    head.box((ex,gy-.07,2.865),(5.5,.05,.45),'Steel')
    for x in (ex-2.7,ex+2.7):head.beam((x,gy,2.85),(x,gy-.05,2.85),.025,.025)
    head.quad([(ex-1.3,gy-.096,3.5),(ex+1.3,gy-.096,3.5),(ex+1.3,gy-.096,4.03),(ex-1.3,gy-.096,4.03)],layout['PUBLIC PARKING'],'Graphics')
    head.box((ex,gy-.07,3.765),(2.7,.05,.58),'Steel')
    # FULL display is installed, off in this weekday partially occupied state.
    head.quad([(ex+3.7,gy+.409,2.1),(ex+4.9,gy+.409,2.1),(ex+4.9,gy+.409,2.5),(ex+3.7,gy+.409,2.5)],layout['FULL'],'Graphics')
    head.box((ex+4.3,gy+.435,2.3),(1.3,.05,.5),'Steel')
    head.beam((ex+3.45,gy,2.3),(ex+4.3,gy+.435,2.3),.06,.06)
    head.finish()
    signage=G.Mesh('Level and building signs',rt)
    for level in range(p['levels']):
        z=level*FLOOR
        for xx in (-L/2+2,0,L/2-2):
            if level==0 and xx>L/2-p['end_length']-3:continue
            if level==p['levels']-1 and xx==0:continue
            signage.box((xx,-W/2-.128,z+.57),(1.85,.006,.54),'Steel')
            if not municipal:
                for dx in (-.7,.7):signage.beam((xx+dx,-W/2-.125,z+.4),(xx+dx,-W/2-.087,z+.4),.025,.025)
            signage.quad([(xx-.9,-W/2-.132,z+.32),(xx+.9,-W/2-.132,z+.32),(xx+.9,-W/2-.132,z+.82),(xx-.9,-W/2-.132,z+.82)],layout['LEVEL '+str(level+1)],'Graphics')
    label='ALDER QUAY' if municipal else 'BELLWETHER COMMONS';z=(p['levels']-1)*FLOOR+.5
    name_x=-TEE/2
    signage.box((name_x,-W/2-.128,z+.15),(7.1,.006,.75),'Steel')
    if not municipal:
        for xx in (-3,-1.5,0,1.5,3):signage.beam((name_x+xx,-W/2-.125,z-.1),(name_x+xx,-W/2-.087,z-.1),.03,.03)
    signage.quad([(name_x-3.5,-W/2-.133,z-.2),(name_x+3.5,-W/2-.133,z-.2),(name_x+3.5,-W/2-.133,z+.5),(name_x-3.5,-W/2-.133,z+.5)],layout[label],'Graphics');signage.finish()
    # Conform sampled routes to the triangles the engine actually drives.
    # The tapered end crossfall is bilinear; its triangulated interpolation
    # differs from the ideal formula by up to a few centimetres at turns.
    vs=[];faces=[]
    bpy.context.view_layer.update()
    for ob in members(rt):
        if ob.type!='MESH':continue
        ob.data.calc_loop_triangles();offset=len(vs)
        vs.extend(ob.matrix_world@v.co for v in ob.data.vertices)
        for tri in ob.data.loop_triangles:
            mat=ob.data.materials[tri.material_index].name
            if ('form Deck' in mat or 'form Seal' in mat or mat.split('.')[0]=='Concrete') and (ob.matrix_world.to_3x3()@tri.normal).z>.7:
                faces.append(tuple(offset+i for i in tri.vertices))
    surface=BVHTree.FromPolygons(vs,faces,all_triangles=True);corrections=[];unsupported=[];probed=0
    for row in p['paths']+p['pedestrian_paths']:
        for pt in row['points']:
            heights=[]
            for dx,dy in ((0,0),(0,.001),(0,-.001),(.001,.001),(-.001,-.001)):
                hit=surface.ray_cast(Vector((pt[0]+dx,pt[1]+dy,pt[2]+.15)),Vector((0,0,-1)),.30)
                if hit[0] is None:continue
                # Probe every side before selecting the uppermost plane:
                # overlapping 2mm tee seals and 3mm pour covers both count.
                z=hit[0].z-(hit[1].x*(pt[0]-hit[0].x)+hit[1].y*(pt[1]-hit[0].y))/hit[1].z
                heights.append(z)
            if not heights:
                unsupported.append(dict(path=row['name'],point=list(pt)))
                continue
            z=max(heights);probed+=1
            corrections.append(abs(z-pt[2]));pt[2]=float(z)
    p['route_surface_projection']=dict(samples=len(corrections),max_correction_m=max(corrections),
        unsupported_samples=unsupported,offset_probe_queries=probed,method='Source upward floor planes; edge probes ≤1.5mm extrapolate to original XY. Independent imported float64 barycentric check.')
    # Curves are engine-authoritative metadata, not exported render tubes.
    # Their point samples also travel as JSON extras because glTF has no curves.
    for row in p['paths']+p['pedestrian_paths']:
        cu=bpy.data.curves.new(row['name'],'CURVE');cu.dimensions='3D';sp=cu.splines.new('POLY');sp.points.add(len(row['points'])-1)
        for pt,co in zip(sp.points,row['points']):pt.co=(*co,1)
        ob=bpy.data.objects.new(row['name']+'_Curve',cu);bpy.context.collection.objects.link(ob);ob.parent=rt
        G.root(row['name'],parent=rt,socket_kind='drive_path' if row in p['paths'] else 'pedestrian_path',path_points_json=json.dumps(row['points']),clear_width_m=row['width'])
    p['pieces']=rows;p['garage_triangles']=G.triangles(members(rt));p['bounds_m']=G.bounds(members(rt));p['occupied']=sum(s['occupied'] for s in p['stalls'])
    return rt


def main():
    pa=argparse.ArgumentParser();pa.add_argument('--seeds',default='101,202');pa.add_argument('--out',type=Path,default=Path('build/ParkingGarage.blend'));pa.add_argument('--system');pa.add_argument('--levels',type=int);pa.add_argument('--tee-count',type=int);a=pa.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.unit_settings.system='METRIC'
    layout=generate();G.palette();templates={};report={};alljobs=pieces.jobs()
    alljobs['Tower3']=lambda r:pieces.tower(r,3);alljobs['Tower5']=lambda r:pieces.tower(r,5)
    for name,fn in alljobs.items():
        rr=G.root(name,module_kind=name);fn(rr)
        # Source connection frames survive glTF extras and engine placement.
        if name=='DoubleTee':
            for side in (-1,1):G.root('Socket_Bearing_'+str(side),(0,side*(SPAN/2-.34),-.6846),rr,socket_kind='module_connection')
        if name in ('InvertedT','LBeam','PTBeam','Spandrel','CableBarrier'):
            half_span=SPAN/2 if name=='PTBeam' else 1.5*TEE
            for side in (-1,1):G.root('Socket_End_'+str(side),(side*half_span,0,0),rr,socket_kind='module_connection')
        if 'Column' in name:
            for z in (0,FLOOR):G.root('Socket_Stack_'+str(z),(0,0,z),rr,socket_kind='module_connection')
        templates[name]=rr;report[name]=export(Path('export/modules')/(name+'.gltf'),members(rr))
        report[name]['bounds_m']=G.bounds(members(rr));assert report[name]['triangles']<=(8000 if name.startswith('Tower') else 2000),(name,report[name]['triangles'])
    for name,count,rise,pt in [('StructuralBay',3,0,False),('EndBay',3,0,False),('RampBay',3,FLOOR/(16*TEE),False),('PTStructuralBay',3,0,True)]:
        rr=G.root(name,module_kind=name);length=count*TEE
        def placed(kind,n,pos,yaw=0,scale=1):
            angle=math.radians(yaw)
            def xf(v):
                xx=v.x*scale;world_x=pos[0]+math.cos(angle)*xx-math.sin(angle)*v.y
                # Grade is evaluated after yaw, so the front L girder does
                # not acquire the opposite slope. Column feet stay flat;
                # the shaft extends vertically and the corbel seats incline.
                grade=rise*world_x
                if 'Column' in kind:
                    grade=0 if v.z<1.3 else rise*pos[0] if v.z>FLOOR-.01 else grade
                return Vector((xx,v.y,v.z+grade))
            return G.clone(templates[kind],name+'__'+n,pos,yaw,rr,xf)
        for i in range(count):placed('PTSlab' if pt else 'DoubleTee','Deck'+str(i),((i-(count-1)/2)*TEE,0,FLOOR))
        for side in (-1,1):
            for end in (-1,1):placed('PTColumn' if pt else 'ColumnCorbel',f'Column{side}{end}',(end*length/2,side*SPAN/2,0))
            if pt:placed('PTBeam','Beam'+str(side),(side*length/2,0,FLOOR),90)
            else:placed('LBeam','Beam'+str(side),(0,side*SPAN/2,FLOOR),180 if side==-1 else 0,(length-.82)/(3*TEE-.82))
        for side in (-1,1):G.root('Socket_Bay_'+str(side),(side*length/2,0,FLOOR+rise*side*length/2),rr,socket_kind='structural_bay')
        templates[name]=rr;report[name]=export(Path('export/modules')/(name+'.gltf'),members(rr));report[name]['bounds_m']=G.bounds(members(rr));assert report[name]['triangles']<=2000,(name,report[name]['triangles'])
    # Display sheet keeps meaningful mating-origin templates in individual files.
    for i,(name,rr) in enumerate(templates.items()):rr.location=((i%5)*25,(i//5)*25,1 if name in ('DoubleTee','PTSlab','InvertedT','LBeam','PTBeam') else 0)
    export(Path('export/ParkingGaragePieces.gltf'),[o for r in templates.values() for o in members(r)])
    a.out.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(a.out.resolve()))
    for rr in templates.values():rr.hide_render=True
    # Reset template transforms before copying into individual sites.
    for rr in templates.values():rr.location=(0,0,0);rr.hide_render=False
    plans=[]
    for seed in map(int,a.seeds.split(',')):
        p=garage(seed,a.system,a.levels,a.tee_count);rt=make_garage(p,templates,layout)
        p['delivery']=export(Path('export')/f'ParkingGarage-{seed}.gltf',[o for o in members(rt) if o.type!='CURVE'])
        assert p['garage_triangles']<300000,p['garage_triangles']
        Path(f'build/garage-{seed}.json').write_text(json.dumps(p,indent=2)+'\n')
        # Keep authoring curves in a per-seed blend, with only that garage.
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.wm.save_as_mainfile(filepath=str(Path(f'build/garage-{seed}.blend').resolve()))
        for o in members(rt):bpy.data.objects.remove(o,do_unlink=True)
        plans.append(p)
        print('GARAGE',seed,p['garage_triangles'],len(p['stalls']),p['occupied'],flush=True)
    Path('build/modules.json').write_text(json.dumps(report,indent=2)+'\n')
    Path('build/manifest.json').write_text(json.dumps(dict(stage='form checkpoint; quick materials, no look-dev',garages=plans,modules=report),indent=2)+'\n')


if __name__=='__main__':main()
