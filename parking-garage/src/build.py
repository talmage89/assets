"""Form checkpoint: module library, two garages, shared external glTF images."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path[:0]=[str(ROOT),str(HERE)]
import geometry as G
import pieces
from plan import garage,deck_z,ramp_fraction,TEE,SPAN,FLOOR,STALL,DEPTH,AISLE
from graphics import generate
from kit import tiling


def members(r):return [r,*r.children_recursive]


def export(path,obs):
    """Use the existing kit GLB exporter, then split without reencoding images."""
    import copy
    from kit.gltf import GLB
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=Path('build/embedded')/path.with_suffix('.glb').name
    tiling.export(tmp,obs);g=GLB(tmp);doc=g.json;binary=g.binary
    known={hashlib.sha256(p.read_bytes()).hexdigest():p for folder in (ROOT/'ground/textures/ship',ROOT/'street-light/textures/ship',Path('textures/checkpoint')) for p in folder.glob('*.png')}
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
    rows=[];L,W=p['length'],p['width'];municipal=p['system']=='precast';a,b=p['ramp_limits'];joint=p['joint_y']
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
                return lev*FLOOR+(FLOOR*ramp_fraction(x,p) if central else 0)+.01*(width/2-abs(y-cy))
            if not ramp and level==0:
                bay_surface('Grade slab',rt,-L/2,L/2,lo,hi,lambda x,y:deck_z(p,level,x,y),.16)
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
                    xf=lambda v,x=x,cy=cy,central=central,level=level:Vector((v.x,v.y,v.z+height(level,x+v.x,cy+v.y,central)-level*FLOOR))
                    put('DoubleTee' if municipal else 'PTSlab',f'{"Ramp" if ramp else "Flat"}_L{level+1}_T{station:02d}',(x,cy,level*FLOOR),xf=xf)
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
                grid=[-L/2+i*3*TEE for i in range(math.ceil(L/(3*TEE))+1)]
                grid=[min(v,L/2) for v in grid];grid=sorted(set(grid+([a,b] if ramp else [])))
                for x in grid:
                    central=ramp and a+1e-6<x<b-1e-6
                    z=height(level,x,cy+side*width/2,central)
                    if level<p['levels']-(2 if central else 1):
                        xf=lambda v,x=x,yy=yy,central=central:Vector((v.x,v.y,v.z+(FLOOR*ramp_fraction(x,p) if central else 0)))
                        put('ColumnCorbel' if municipal else 'PTColumn',f'Column_{level}_{ramp}_{side}_{x:.2f}',(x,yy,level*FLOOR),xf=xf)
                    # Lowest inclined deck also needs support from grade.
                    if central and level==0 and z>.96:
                        col=G.Mesh(f'Ramp ground pier {side} {x}',rt);col.box((x,yy,(z-.80)/2),(.6096,.6096,z-.80));col.finish()
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
            if not municipal and (level>0 or ramp):
                # Long-span cast PT beams run ACROSS the parking bay. The
                # slab spans the 36ft distance between these transverse beams.
                for i in range(math.ceil(L/(3*TEE))+1):
                    xx=min(-L/2+i*3*TEE,L/2)
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
        # Facade spandrels on front and rear; top deck stays open to sky.
        for side in (-1,1):
            yy=side*W/2
            edges=sorted({-L/2,L/2,a,b,*[min(-L/2+i*3*TEE,L/2) for i in range(math.ceil(L/(3*TEE))+1)]})
            for i,(x0,x1) in enumerate(zip(edges,edges[1:])):
                xx=(x0+x1)/2
                if level==0 and side==-1 and xx>L/2-p['end_length']-3:continue
                ramp=side==1 and a<xx<b
                if ramp and level==p['levels']-1:continue
                def xf(v,xx=xx,x0=x0,x1=x1,ramp=ramp,side=side):
                    vx=v.x*(x1-x0)/(3*TEE)
                    return Vector((vx,v.y,v.z+(FLOOR*ramp_fraction(xx+vx,p) if ramp else 0)))
                put('Spandrel' if municipal else 'CableBarrier',f'Facade_{level}_{side}_{i}',(xx,yy,level*FLOOR),0,xf)
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
                for y0,y1 in ((-W/2+5.6,joint),(joint,W/2)):
                    mb.box((side*L/2,(y0+y1)/2,level*FLOOR+.55),(.24,y1-y0,1.10))
                mb.finish()
        # Expansion line and transverse pour strips at structural grid.
        seals=G.Mesh(f'Pour joints level {level}',rt)
        for x in (-L/2+i*3*TEE for i in range(1,math.ceil(L/(3*TEE)))):
            seals.box((x,p['flat_y'],level*FLOOR+.004),(.023,SPAN,.008),'Seal')
        seals.finish()
    for i,pos in enumerate(p['towers']):
        kind='Tower' if p['levels']==4 else 'Tower3' if p['levels']==3 else 'Tower5'
        put(kind,f'Tower_{i+1}',pos,-90 if i==0 else 90)
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
        x,y,z=s['x'],s['y'],s['z'];row=-1 if s['yaw']==180 else 1
        root=G.root('Stall_'+s['id'],(x,y,z),rt,socket_kind='parked_car',yaw_degrees=s['yaw'],width_m=s['width'],depth_m=s['depth'],occupied=s['occupied'],level=s['level'])
        root.rotation_euler=(math.atan(s['crossfall']),0,math.radians(s['yaw']))
        for xx in (x-s['width']/2,x+s['width']/2):
            y0,y1=y-DEPTH/2,y+DEPTH/2
            marks.quad([(xx-.05,y0,deck_z(p,s['level'],xx,y0,s['ramp'])+.006),(xx+.05,y0,deck_z(p,s['level'],xx,y0,s['ramp'])+.006),(xx+.05,y1,deck_z(p,s['level'],xx,y1,s['ramp'])+.006),(xx-.05,y1,deck_z(p,s['level'],xx,y1,s['ramp'])+.006)])
        wy=y+row*(DEPTH/2-.90)
        put('WheelStop','Stop_'+s['id'],(x,wy,deck_z(p,s['level'],x,wy,s['ramp'])))
        num=f'{index%120+1:03d}';ny=y-row*(DEPTH/2-.45)
        marks.quad([(x-.34,ny-.18,deck_z(p,s['level'],x-.34,ny-.18,s['ramp'])+.008),
                    (x+.34,ny-.18,deck_z(p,s['level'],x+.34,ny-.18,s['ramp'])+.008),
                    (x+.34,ny+.18,deck_z(p,s['level'],x+.34,ny+.18,s['ramp'])+.008),
                    (x-.34,ny+.18,deck_z(p,s['level'],x-.34,ny+.18,s['ramp'])+.008)],layout[num],'Graphics')
        if s['compact']:
            yy=y-row*(DEPTH/2-1.15)
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
            sg=G.Mesh('Accessible sign '+s['id'],rt);sy=y-DEPTH/2+.22
            sg.tube([(x,sy,0),(x,sy,2.10)],.025,'Steel');sg.box((x,sy,1.82),(.34,.035,.48),'Blue')
            circle=[(x+.083*math.cos(t*math.tau/16),sy-.022,1.77+.083*math.sin(t*math.tau/16)) for t in range(17)]
            sg.tube(circle,.009,'White',6);sg.tube([(x-.015,sy-.024,1.92),(x-.015,sy-.024,1.80),(x+.075,sy-.024,1.80),(x+.12,sy-.024,1.71)],.010,'White',6);sg.finish()
    # Arrows are original cut polygons, using Ground's paint chart.
    for level in range(p['levels']):
        for xx in (-L/4,L/4):
            cy=p['flat_y'];zz=deck_z(p,level,xx,cy)+.009
            poly=[(-1.1,-.12),(.3,-.12),(.3,-.40),(1.1,0),(.3,.40),(.3,.12),(-1.1,.12)]
            marks.geom([(xx+x,cy+y,zz) for x,y in poly],[tuple(range(7))],'White')
        for i,x in enumerate((-L/3,0,L/3)):
            for yy in (-W/2+.5,joint-.5):put('Drain',f'Drain_{level}_{i}_{yy:.1f}',(x,yy,deck_z(p,level,x,yy)+.002))
    marks.finish()
    # Entry slots in the end bay keep all queuing on property.
    ex=L/2-p['end_length']/2
    islands=G.Mesh('Entry control islands',rt)
    for i,dx in enumerate((-1.65,1.65)):
        lane=ex+dx;floor=deck_z(p,0,lane-1.8,-W/2+2.5)
        islands.box((lane-1.8,-W/2+2.5,floor+.075),(.65,3.6,.15))
        put('Gate',f'{"Entry" if i==0 else "Exit"}_Gate',(lane-1.57,-W/2+3.7,floor+.15))
        put('Ticket',f'Ticket_{i}',(lane-1.8,-W/2+1.8,floor+.15),90)
    islands.finish()
    put('PayStation','PedestrianPay',(p['towers'][0][0]-1.5,-W/2-1.3,0))
    head=G.Mesh('Entry gantry and signs',rt)
    for x in (ex-3.45,ex+3.45):head.box((x,-W/2-1.0,1.75),(.14,.14,3.5),'Steel')
    head.box((ex,-W/2-1.0,3.40),(7.0,.18,.20),'Steel')
    # Hanging bar lower edge measured at precisely 98in above route grade.
    head.box((ex,-W/2-1.0,2.4892+.06),(6.7,.10,.12),'Yellow')
    for x in (ex-2.7,ex+2.7):head.tube([(x,-W/2-1,2.61),(x,-W/2-1,3.3)],.006,'Steel',6)
    head.quad([(ex-2.7,-W/2-1.10,2.66),(ex+2.7,-W/2-1.10,2.66),(ex+2.7,-W/2-1.10,3.07),(ex-2.7,-W/2-1.10,3.07)],layout['CLEARANCE  8 FT 2 IN'],'Graphics')
    head.quad([(ex-1.3,-W/2-1.11,3.5),(ex+1.3,-W/2-1.11,3.5),(ex+1.3,-W/2-1.11,4.03),(ex-1.3,-W/2-1.11,4.03)],layout['PUBLIC PARKING'],'Graphics')
    # FULL display is installed, off in this weekday partially occupied state.
    head.quad([(ex+3.7,-W/2-.6,2.1),(ex+4.9,-W/2-.6,2.1),(ex+4.9,-W/2-.6,2.5),(ex+3.7,-W/2-.6,2.5)],layout['FULL'],'Graphics')
    head.box((ex+4.3,-W/2-.565,2.3),(1.3,.05,.5),'Steel')
    head.beam((ex+3.45,-W/2-1,2.3),(ex+4.3,-W/2-.565,2.3),.06,.06)
    head.finish()
    signage=G.Mesh('Level and building signs',rt)
    for level in range(p['levels']):
        z=level*FLOOR
        for xx in (-L/2+2,0,L/2-2):
            signage.quad([(xx-.9,-W/2-.14,z+.32),(xx+.9,-W/2-.14,z+.32),(xx+.9,-W/2-.14,z+.82),(xx-.9,-W/2-.14,z+.82)],layout['LEVEL '+str(level+1)],'Graphics')
    label='ALDER QUAY' if municipal else 'BELLWETHER COMMONS';z=(p['levels']-1)*FLOOR+.5
    signage.quad([(-7,-W/2-.16,z-.2),(7,-W/2-.16,z-.2),(7,-W/2-.16,z+.5),(-7,-W/2-.16,z+.5)],layout[label],'Graphics');signage.finish()
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
            for side in (-1,1):G.root('Socket_Bearing_'+str(side),(0,side*(SPAN/2-.29),-.6596),rr,socket_kind='module_connection')
        if name in ('InvertedT','LBeam','PTBeam','Spandrel','CableBarrier'):
            for side in (-1,1):G.root('Socket_End_'+str(side),(side*1.5*TEE,0,0),rr,socket_kind='module_connection')
        if 'Column' in name:
            for z in (0,FLOOR):G.root('Socket_Stack_'+str(z),(0,0,z),rr,socket_kind='module_connection')
        templates[name]=rr;report[name]=export(Path('export/modules')/(name+'.gltf'),members(rr))
        report[name]['bounds_m']=G.bounds(members(rr));assert report[name]['triangles']<=(8000 if name.startswith('Tower') else 2000),(name,report[name]['triangles'])
    for name,count,rise,pt in [('StructuralBay',3,0,False),('EndBay',2,0,False),('RampBay',3,FLOOR/(16*TEE),False),('PTStructuralBay',3,0,True)]:
        rr=G.root(name,module_kind=name);length=count*TEE
        def placed(kind,n,pos,yaw=0,scale=1):
            def xf(v):return Vector((v.x*scale,v.y,v.z+rise*(v.x*scale+pos[0])))
            return G.clone(templates[kind],name+'__'+n,pos,yaw,rr,xf)
        for i in range(count):placed('PTSlab' if pt else 'DoubleTee','Deck'+str(i),((i-(count-1)/2)*TEE,0,FLOOR))
        for side in (-1,1):
            for end in (-1,1):placed('PTColumn' if pt else 'ColumnCorbel',f'Column{side}{end}',(end*length/2,side*SPAN/2,0))
            if pt:placed('PTBeam','Beam'+str(side),(side*length/2,0,FLOOR),90)
            else:placed('LBeam','Beam'+str(side),(0,side*SPAN/2,FLOOR),180 if side==-1 else 0,length/(3*TEE))
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
