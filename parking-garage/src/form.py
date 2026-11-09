"""Refine construction without changing the accepted stalls, ramps or paths.

The original form deliveries remain immutable. This additive checkpoint
loads their script-built source and writes export/form/ independently.
"""
import json,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
import geometry as G
import pieces
from plan import FLOOR,TEE,SPAN,ramp_fraction


def remove_paint(ob):
    if ob.type!='MESH' or not ('Column' in ob.name):return
    ob.data=ob.data.copy();bm=bmesh.new();bm.from_mesh(ob.data)
    doomed=[f for f in bm.faces if 'form Blue' in ob.data.materials[f.material_index].name]
    bmesh.ops.delete(bm,geom=doomed,context='FACES');bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bm.to_mesh(ob.data);bm.free();ob.data.update()


def tower_signs(r,levels,layout,label):
    b=G.Mesh(r.name+'__Wayfinding',r)
    # Sign faces on both public sides, mounted to the opaque shaft piers.
    for side in (-1,1):
        x=side*2.844
        def plaque(y,z,w,h,key):
            b.box((x-side*.023,y,z),(.028,w+.06,h+.06),'Steel')
            pts=[(x,y-w/2,z-h/2),(x,y+w/2,z-h/2),(x,y+w/2,z+h/2),(x,y-w/2,z+h/2)]
            if side<0:pts=[pts[1],pts[0],pts[3],pts[2]]
            b.quad(pts,layout[key],'Graphics')
        plaque(1.75,3.05,1.5,.31,label)
        plaque(1.75,2.70,1.5,.22,'OPEN  6 AM - MIDNIGHT')
        for lev in range(levels):plaque(-1.78,lev*FLOOR+1.60,.72,.65,'TOWER '+str(lev+1))
    for lev in range(levels):
        for xx,key in ((-1.45,'STAIRS'),(1.30,'ELEVATOR')):
            z=lev*FLOOR+2.48;b.box((xx,2.704,z),(1.25,.01,.24),'Steel')
            b.quad([(xx+.60,2.711,z-.10),(xx-.60,2.711,z-.10),(xx-.60,2.711,z+.10),(xx+.60,2.711,z+.10)],layout[key],'Graphics')
    b.finish()


def refine_fixture(rr,strap=.40):
    old=next((ob.name for ob in rr.children if ob.get('socket_kind')=='light_emitter'),None)
    for ob in reversed(list(rr.children_recursive)):bpy.data.objects.remove(ob,do_unlink=True)
    pieces.fixture(rr,refined=True,strap=strap)
    if old:next(ob for ob in rr.children if ob.get('socket_kind')=='light_emitter').name=old


def upgrade(rt,p,layout):
    for ob in list(rt.children_recursive):remove_paint(ob)
    if p['system']=='precast':
        from tee_detail import deepen
        p['deepened_tee_count']=deepen(rt,p)
        for rr in list(rt.children):
            if rr.get('module_kind')!='Spandrel':continue
            for ob in list(rr.children):
                if ob.type=='MESH':bpy.data.objects.remove(ob,do_unlink=True)
            pieces.spandrel(rr,refined=True)
            a,c=next((a,c) for a,c in zip(p['structural_stations'],p['structural_stations'][1:]) if a-1e-5<rr.location.x<c+1e-5)
            ramp=rr.location.y>0 and p['ramp_limits'][0]<rr.location.x<p['ramp_limits'][1]
            for ob in rr.children:
                if ob.type!='MESH':continue
                for v in ob.data.vertices:
                    v.co.x*=(c-a)/(3*TEE)
                    if ramp:v.co.z+=FLOOR*ramp_fraction(rr.location.x+v.co.x,p)
                bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free();ob.data.update()
    for rr in list(rt.children):
        if rr.get('module_kind')!='Fixture':continue
        refine_fixture(rr,.5524 if p['system']=='precast' else .10)
    towers=[o for o in rt.children if o.name.startswith('Tower_') and o.get('module_kind')]
    for old in towers:
        matrix=old.matrix_basis.copy();name=old.name;kind=old['module_kind']
        for ob in reversed([old,*old.children_recursive]):bpy.data.objects.remove(ob,do_unlink=True)
        rr=G.root(name,parent=rt,module_kind=kind);rr.matrix_basis=matrix
        pieces.tower(rr,p['levels'],refined=True)
        tower_signs(rr,p['levels'],layout,'ALDER QUAY' if p['system']=='precast' else 'BELLWETHER COMMONS')
    b=G.Mesh('Facade construction and turn protection',rt)
    W,L=p['width'],p['length'];municipal=p['system']=='precast'
    for lev in range(p['levels']):
        z=lev*FLOOR
        for side in (-1,1):
            if side==1:continue # inclined rear panels retain their actual grade
            yy=side*(W/2+.132)
            for i,(a,c) in enumerate(zip(p['structural_stations'],p['structural_stations'][1:])):
                if lev==0 and (a+c)/2>L/2-p['end_length']-3:continue
                if municipal:
                    # Express the 12ft subpanel rhythm with scored joints and
                    # a drip chase. These are 8mm, bounded to the panel face.
                    for xx in (a+TEE,c-TEE):
                        if a+.1<xx<c-.1:b.box((xx,yy,z+.34),(.009,.006,1.15),'Seal')
                    for zz in (1.25,1.47):b.tube([(a+.10,yy+.15,z+zz),(c-.10,yy+.15,z+zz)],.012,'Steel')
                    for xx in (a+.10,(a+c)/2,c-.10):b.beam((xx,yy+.15,z+1.02),(xx,yy+.15,z+1.49),.045,.045)
                else:b.box(((a+c)/2,yy+.04,z+.13),(c-a-.08,.008,.012),'Seal')
        # Hazard paint is restricted to turn-facing corner guards, never a
        # blue film repeated at every column foot.
        for xx in p['ramp_limits'] if lev<p['levels']-1 else ():
            for cy,sign in ((p['flat_y']-SPAN/2,1),(p['flat_y']+SPAN/2,-1)):
                yy=cy+sign*.386
                b.box((xx,cy+sign*.383,z+.55),(.72,.004,.95),'Steel')
                for j in range(6):
                    x=xx+(j-2.5)*.105
                    pts=[Vector(v) for v in [(x-.05,yy,z+.10),(x+.05,yy,z+.10),(x+.28,yy,z+.90),(x+.18,yy,z+.90)]]
                    for cut,above in ((xx-.345,True),(xx+.345,False)):
                        clipped=[]
                        for a,c in zip(pts,pts[1:]+pts[:1]):
                            ia=a.x>=cut if above else a.x<=cut;ic=c.x>=cut if above else c.x<=cut
                            if ia:clipped.append(a)
                            if ia!=ic:clipped.append(a.lerp(c,(cut-a.x)/(c.x-a.x)))
                        pts=clipped
                    if len(pts)>=3:b.geom(pts,[tuple(range(len(pts)))],'Yellow' if j%2 else 'Steel')
    b.finish()
    # Current graphics are the additional family page, with individual level
    # colors and hours. The accepted original page is never overwritten.
    for ob in rt.children_recursive:
        if ob.type!='MESH':continue
        for i,m in enumerate(ob.data.materials):
            if m and m.name.startswith('GroundParkingTrim'):ob.data.materials[i]=G.M['Graphics']
    bpy.context.view_layer.update()
    p['garage_triangles']=G.triangles([rt,*rt.children_recursive]);p['bounds_m']=G.bounds([rt,*rt.children_recursive])
    rt['stage']='REFINED FORM / LOOK-DEV CHECKPOINT'
    return rt
