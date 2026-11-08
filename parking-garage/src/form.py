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
from plan import FLOOR,TEE,SPAN


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
            if side<0:pts.reverse()
            b.quad(pts,layout[key],'Graphics')
        plaque(1.75,3.05,1.5,.31,label)
        plaque(1.75,2.70,1.5,.22,'OPEN  6 AM - MIDNIGHT')
        for lev in range(levels):plaque(-1.78,lev*FLOOR+1.60,.72,.65,'LEVEL '+str(lev+1))
    b.finish()


def upgrade(rt,p,layout):
    for ob in list(rt.children_recursive):remove_paint(ob)
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
                    b.box(((a+c)/2,yy,z-.20),(c-a-.07,.006,.012),'Seal')
                    for zz in (1.25,1.47):b.tube([(a+.10,yy+.15,z+zz),(c-.10,yy+.15,z+zz)],.012,'Steel')
                    for xx in (a+.10,(a+c)/2,c-.10):b.beam((xx,yy+.15,z+1.02),(xx,yy+.15,z+1.49),.045,.045)
                else:b.box(((a+c)/2,yy+.04,z+.13),(c-a-.08,.008,.012),'Seal')
        # Hazard paint is restricted to turn-facing corner guards, never a
        # blue film repeated at every column foot.
        for xx in (p['ramp_limits'][0]-.65,p['ramp_limits'][1]+.65):
            for yy in (p['flat_y']-SPAN/2+.55,p['flat_y']+SPAN/2-.55):
                for j in range(6):
                    x=xx+(j-2.5)*.105
                    b.quad([(x-.05,yy,z+.10),(x+.05,yy,z+.10),(x+.28,yy,z+.90),(x+.18,yy,z+.90)],None,'Yellow' if j%2 else 'Steel')
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
