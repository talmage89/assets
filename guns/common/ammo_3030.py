"""Original .30-30 flat-nose visual cartridge and fired case, in millimeters.

Visual exterior only: shallow primer seat, no charge or manufacturing internals.
Callers supply their palette and registration, retaining their own atlas policy.
The origin is the center of the head, +Y toward the mouth. All texels/letters
are authored; reference photographs are never accepted by this module.
"""
import math
import bpy
import bmesh
from mathutils import Matrix, Vector
from kit import model as M
from kit.fonts import find_font

CASE_LENGTH = 51.8
OVERALL_LENGTH = 64.77
RIM_DIAMETER = 12.85


def revolved(name, profile, counts, material, base):
    """Manifold angular zipper; dense visible lips and economical hidden rings."""
    x,y,z=base;verts=[];rings=[];faces=[]
    for (h,r),n in zip(profile,counts):
        rings.append(list(range(len(verts),len(verts)+n)))
        verts.extend((x+r*math.cos(math.tau*i/n),y+h,z+r*math.sin(math.tau*i/n)) for i in range(n))
    for j,a in enumerate(rings):
        b=rings[(j+1)%len(rings)];i=k=0
        while i<len(a) or k<len(b):
            if k==len(b) or (i<len(a) and (i+1)/len(a)<=(k+1)/len(b)):
                faces.append((a[i%len(a)],b[k%len(b)],a[(i+1)%len(a)]));i+=1
            else:
                faces.append((a[i%len(a)],b[k%len(b)],b[(k+1)%len(b)]));k+=1
    ob=M.mesh(name,verts,faces,material)
    bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    return ob


def revolution_normals(ob,profile,counts,base):
    # Analytic revolution normals: unequal-count joins must not weight the
    # mouth or shoulder into the octagonal shading rejected on previous guns.
    owner={};offset=0
    for j,n in enumerate(counts):
        owner.update({v:j for v in range(offset,offset+n)});offset+=n
    x,y,z=base
    section=[]
    for j,(h,r) in enumerate(profile):
        hh,rr=profile[(j+1)%len(profile)]
        section.append(Vector((-(rr-r),hh-h)).normalized())
    normals=[None]*len(ob.data.loops)
    for face in ob.data.polygons:
        ids={owner[v] for v in face.vertices};segment=next(j for j in ids if (j+1)%len(profile) in ids)
        for loop in face.loop_indices:
            vi=ob.data.loops[loop].vertex_index;j=owner[vi]
            prev=section[(j-1)%len(profile)];nex=section[j]
            # The long straight body must not interpolate toward the cone's
            # normal over its entire 33.5 mm length. That fictitious bend made
            # a dent-like wave in the fired-case macro. Each straight exterior
            # segment keeps its own analytic cone normal at both ends.
            straight_transition=j in (6,7,8,9)
            normal=(prev+nex).normalized() if not straight_transition and prev.dot(nex)>math.cos(math.radians(38)) else section[segment]
            co=ob.data.vertices[vi].co;dx,dz=co.x-x,co.z-z;radius=math.hypot(dx,dz)
            normals[loop]=(normal.y*dx/radius,normal.x,normal.y*dz/radius)
        face.use_smooth=True
    ob.data.normals_split_custom_set(normals)
    return ob


def build(name, base, palette, register, bone='Root', *, fired=False, hidden=False, headstamp=False):
    """Return named case, primer and (live only) flat-nose bullet objects."""
    # CIP exterior envelope, rounded/relieved for a game prop. The reduced
    # occluded tube variants intentionally spend less than the display version.
    n=8 if hidden else (32 if headstamp else 24)
    profile=[(0,2.08),(0,6.2),(.18,6.425),(1.5,6.425),(1.63,5.35),
             (2.2,5.05),(3.1,5.355),(36.6,5.095),(39.69,4.23),(51.8,4.19),
             (51.8,3.88),(50.8,3.87),(4.0,4.85),(3.8,2.08)]
    counts=[n,n,n,n,8 if hidden else 16,8 if hidden else 16,n,n,n,40 if fired and not hidden else n,
            40 if fired and not hidden else n,24 if not hidden else 8,8 if hidden else 16,n]
    case=revolved(name+'_Case',profile,counts,palette['brass'],base);register(case,bone)
    revolution_normals(case,profile,counts,base)
    x,y,z=base
    face=[(-.01,0)]+([(-.01,.45),(-.01,.85),(-.01,1.2)] if fired else [])+[(-.01,1.95),(.12,2.05),(.28,2.05),(.28,0)]
    primer=M.lathe(name+'_Primer',face,palette['steel'],segments=24,axis='Y',center=(x,z))
    for v in primer.data.vertices:v.co.y+=y
    if fired:
        # Actual shallow struck depression in the exterior, no primer internals.
        for v in primer.data.vertices:
            r=math.hypot(v.co.x-x,v.co.z-z)
            if v.co.y<y+.13:v.co.y+=.22*max(0,1-(r/.9)**2)**2
    result=[case]
    if hidden:bpy.data.objects.remove(primer,do_unlink=True)
    else:register(primer,bone);result.append(primer)
    if not fired:
        bullet=M.lathe(name+'_Jacket',[(47,0),(47,3.90),(55.5,3.91),(59.0,3.78),(62.8,2.95),(64.0,2.35),(64.0,0)],palette['copper'],segments=n,axis='Y',center=(x,z))
        for v in bullet.data.vertices:v.co.y+=y
        register(bullet,bone);result.append(bullet)
        nose=M.lathe(name+'_FlatNose',[(63.7,0),(63.7,2.4),(64.77,2.23),(64.77,0)],palette['lead'],segments=n,axis='Y',center=(x,z))
        for v in nose.data.vertices:v.co.y+=y
        register(nose,bone);result.append(nose)
    if headstamp:
        font=bpy.data.fonts.load(find_font('DejaVu Sans','Bold'))
        for text,offset in [('PD',3.5),('30-30',-3.55)]:
            curve=bpy.data.curves.new(name+' fictional headstamp','FONT');curve.body=text;curve.font=font
            curve.size=1.7 if text=='PD' else 1.5;curve.align_x='CENTER';curve.align_y='CENTER';curve.resolution_u=2
            ob=bpy.data.objects.new(name+'_Headstamp',curve);bpy.context.collection.objects.link(ob)
            ob.location=(x,y-.025,z+offset);ob.rotation_euler=(math.pi/2,0,0)
            ob.data.materials.append(palette['stamp'])
            bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
            bpy.ops.object.convert(target='MESH');M.apply(ob);ob.data.transform(ob.matrix_world);ob.matrix_world=Matrix.Identity(4)
            ob['allow_boundary']=True;register(ob,bone);result.append(ob)
    return result
