"""Delivery-only pavement maintenance and accessible surface markings.

The accepted plan, stall envelopes and every collision surface stay intact.
ADA 502 requires marked access aisles, but specifies no paint color; blue
diagonal lines and a white ISA on blue follow the period reference practice.
"""
import json,random
from pathlib import Path
import bpy,bmesh
import geometry as G
from plan import deck_z


def revise(root,p):
    layout=json.loads(Path('textures/lookdev/layout.json').read_text())
    G.palette(Path('textures/lookdev'))
    spaces=[s for s in p['stalls'] if s['accessible']]
    marks=next(o for o in root.children if o.name.startswith('Parking markings and signs'))
    G.M['Graphics']=next(m for m in marks.data.materials if m and m.name.startswith('GroundParkingTrim'))
    marks.data=marks.data.copy();bm=bmesh.new();bm.from_mesh(marks.data)
    from service_age import floor_surface
    from mathutils import Vector
    surface=floor_surface(root)
    for v in {v for f in bm.faces if f.normal.z>.7 for v in f.verts}:
        hit=surface.ray_cast(v.co+Vector((0,0,.05)),Vector((0,0,-1)),.10)
        if hit[0] is not None:v.co.z=hit[0].z+.0005
    removed=[]
    for f in bm.faces:
        mat=marks.data.materials[f.material_index];center=f.calc_center_median()
        if 'form Blue' in mat.name:
            removed.append(f);continue
        # Only the old access-aisle hatches, not stall edge stripes or numbers.
        if 'GroundTrim' not in mat.name:continue
        for s in spaces:
            a,c=s['access_aisle']
            if a+.09<center.x<c-.09 and abs(center.y-s['y'])<s['depth']/2+.4 and center.z<.2:
                removed.append(f);break
    bmesh.ops.delete(bm,geom=removed,context='FACES')
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bm.to_mesh(marks.data);bm.free();marks.data.update()
    b=G.Mesh('Accessible aisle hatching and ISA',root);done=set()
    for s in spaces:
        x,y=s['x'],s['y']+.25
        def q(corners,mat,rect=None,offset=.0005):
            b.quad([(xx,yy,deck_z(p,0,xx,yy)+offset) for xx,yy in corners],rect,mat)
        q([(x-.48,y-.48),(x+.48,y-.48),(x+.48,y+.48),(x-.48,y+.48)],'Blue')
        q([(x-.43,y-.43),(x+.43,y-.43),(x+.43,y+.43),(x-.43,y+.43)],'Graphics',layout['♿'],.0007)
        left,right=s['access_aisle']
        if (left,right) in done:continue
        done.add((left,right));y0,y1=s['y']-s['depth']/2,s['y']+s['depth']/2
        for j in range(10):
            yy=y0+.12+j*(s['depth']-.85)/10
            q([(left+.06,yy),(left+.14,yy),(right-.06,yy+.65),(right-.14,yy+.65)],'Blue')
    ob=b.finish();ob['allow_boundary']=True
    return dict(removed_floor_triangles=len(removed),accessible_symbols=len(spaces),access_aisles=len(done))
