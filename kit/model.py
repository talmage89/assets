"""Small deterministic modeling vocabulary, in meters. No asset-specific globals.

Profiles are authored coordinates, never sampled from reference imagery.
Objects carry `asset_set` and `assembly` for independent budgets and pivots.
"""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix


def mesh(name, vertices, faces, material=None):
    data = bpy.data.meshes.new(name)
    data.from_pydata(vertices, [], faces)
    data.update()
    ob = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(ob)
    if material:
        data.materials.append(material)
    bm = bmesh.new(); bm.from_mesh(data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(data); bm.free()
    return ob


def bevel(ob, radius=0.001, segments=2):
    if radius:
        m = ob.modifiers.new('Manufacturing edge radius', 'BEVEL')
        m.width = radius; m.segments = segments
        m.harden_normals = True
        m.miter_outer = 'MITER_ARC'
    return ob


def smooth(ob, angle=40):
    ob.data.shade_smooth()
    ob.data.set_sharp_from_angle(angle=math.radians(angle))
    return ob


def apply(ob):
    dg = bpy.context.evaluated_depsgraph_get()
    old = ob.data
    ob.data = bpy.data.meshes.new_from_object(ob.evaluated_get(dg), depsgraph=dg,
                                            preserve_all_data_layers=True)
    ob.modifiers.clear()
    if old.users == 0:
        bpy.data.meshes.remove(old)
    return ob


def box(name, center, size, material, radius=0.001, segments=2):
    x,y,z = (v/2 for v in size)
    vs = [(a*x,b*y,c*z) for a,b,c in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),
                                     (1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
    fs = [(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)]
    ob = mesh(name,vs,fs,material); ob.location=center
    return bevel(ob, min(radius,min(size)*.45), segments)


def rounded_rectangle(w,h,r,n=4):
    out=[]
    for x,y,a in [(w/2-r,-h/2+r,-90),(w/2-r,h/2-r,0),
                  (-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180)]:
        out += [(x+r*math.cos(math.radians(a+90*i/n)),
                 y+r*math.sin(math.radians(a+90*i/n))) for i in range(n+1)]
    return out


def profile(name, points, lo, hi, material, axis='X', radius=0, segments=2):
    """Extruded closed polygon. Concave caps use Blender's ngon triangulator."""
    def p(u,v,h):
        return (h,u,v) if axis=='X' else ((u,h,v) if axis=='Y' else (u,v,h))
    n=len(points)
    vs=[p(u,v,h) for h in (lo,hi) for u,v in points]
    fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]
    fs += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    return bevel(mesh(name,vs,fs,material),min(radius,abs(hi-lo)*.45),segments)


def loft(name, loops, material, caps=True, closed=True):
    n=len(loops[0]); vs=[tuple(p) for loop in loops for p in loop]
    fs=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i)
        for j in range(len(loops)-1) for i in range(n if closed else n-1)]
    if caps and closed:
        fs += [tuple(reversed(range(n))),tuple(range(len(vs)-n,len(vs)))]
    return mesh(name,vs,fs,material)


def lathe(name, points, material, segments=48, axis='Z', center=(0,0), closed=False):
    """Revolve (axial position, radius); axis points weld to one vertex."""
    def p(h,a,b):
        c,d=center
        return (h,c+a,d+b) if axis=='X' else ((c+a,h,d+b) if axis=='Y' else (c+a,d+b,h))
    vs=[]; rings=[]
    for h,r in points:
        ring=[]
        for i in range(1 if r==0 else segments):
            t=i*math.tau/segments; ring.append(len(vs)); vs.append(p(h,r*math.cos(t),r*math.sin(t)))
        rings.append(ring)
    fs=[]
    for j in range(len(rings) if closed else len(rings)-1):
        a,b=rings[j],rings[(j+1)%len(rings)]
        if len(a)==len(b)==1:continue
        for i in range(segments):
            k=(i+1)%segments
            fs.append((a[0],b[i],b[k]) if len(a)==1 else
                      ((a[i],b[0],a[k]) if len(b)==1 else (a[i],b[i],b[k],a[k])))
    if not closed:
        if len(rings[0])>1:fs.append(tuple(reversed(rings[0])))
        if len(rings[-1])>1:fs.append(tuple(rings[-1]))
    return smooth(mesh(name,vs,fs,material))


def cylinder(name, a, b, radius, material, segments=16):
    a,b=Vector(a),Vector(b)
    ob=lathe(name,[(0,0),(0,radius),((b-a).length,radius),((b-a).length,0)],material,segments)
    ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); ob.location=a
    return ob


def tube(name, points, radius, material, sides=10, caps=True):
    """Parallel-transported circular section along an authored polyline."""
    pts=list(map(Vector,points)); loops=[]; prev=None
    for i,p in enumerate(pts):
        tangent=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized()
        if prev is None:
            seed=Vector((0,0,1)) if abs(tangent.z)<.9 else Vector((1,0,0))
            u=tangent.cross(seed).normalized()
        else:
            u=(prev-tangent*prev.dot(tangent)).normalized()
        v=tangent.cross(u).normalized(); prev=u
        loops.append([p+radius*(u*math.cos(k*math.tau/sides)+v*math.sin(k*math.tau/sides)) for k in range(sides)])
    return smooth(loft(name,loops,material,caps),max(40,360/sides+2))


def bezier(a,b,c,d,steps=12):
    return [tuple((1-t)**3*a[k]+3*(1-t)**2*t*b[k]+3*(1-t)*t*t*c[k]+t**3*d[k]
                  for k in range(len(a))) for t in [i/steps for i in range(steps+1)]]


def sheet(name, points, width, thickness, material, inner=None):
    """An open bent sheet profile in YZ, extruded in X and solidified inward."""
    ob=loft(name, [[(-width/2,y,z),(width/2,y,z)] for y,z in points],material,caps=False,closed=False)
    mod=ob.modifiers.new('Sheet gauge','SOLIDIFY'); mod.thickness=thickness
    mod.offset=-1; mod.use_even_offset=True
    if inner:
        ob.data.materials.append(inner); mod.material_offset=1; mod.material_offset_rim=1
    return smooth(ob)


def boolean(ob, cutter, operation='DIFFERENCE'):
    mod=ob.modifiers.new('Fabricated cutout','BOOLEAN')
    mod.object=cutter; mod.operation=operation; mod.solver='EXACT'
    apply(ob); bpy.data.objects.remove(cutter,do_unlink=True)
    return ob


def pivot(name, position, axis=None, limits=None):
    ob=bpy.data.objects.new(name,None); bpy.context.collection.objects.link(ob)
    ob.location=position; ob.empty_display_type='ARROWS'; ob.empty_display_size=.07
    if axis: ob['pivot_axis']=axis
    if limits: ob['range_degrees']=list(limits)
    return ob


def attach(ob, parent, asset_set='Grill', inherit_asset_set=False):
    """Bake geometry into the pivot's local frame; leave all child origins on it."""
    apply(ob)
    bpy.context.view_layer.update()
    xf=parent.matrix_world.inverted() @ ob.matrix_world
    ob.data.transform(xf); ob.parent=parent; ob.matrix_parent_inverse=Matrix.Identity(4)
    ob.matrix_basis=Matrix.Identity(4)
    ob['asset_set']=parent.get('asset_set',asset_set) if inherit_asset_set else asset_set; ob['assembly']=parent.name
    return ob


def plane_uv(name, corners, material):
    ob=mesh(name,corners,[(0,1,2,3)],material)
    uv=ob.data.uv_layers.new(name='PrintUV')
    corners_uv=[(0,0),(1,0),(1,1),(0,1)]
    for face in ob.data.polygons:
        for loop in face.loop_indices:
            uv.data[loop].uv=corners_uv[ob.data.loops[loop].vertex_index]
    ob['allow_boundary']=True
    return ob


def offset_profile(points, distance):
    """Offset an open 2D profile to its left normal; useful for inner ribs/seams.

    End tangents use their neighboring segment. This is a centerline offset;
    tightly concave sheet corners should use a fillet or a manufacturing radius.
    """
    result=[]
    for i,p in enumerate(points):
        tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)])
        tangent.normalize()
        result.append((p[0]-tangent.y*distance,p[1]+tangent.x*distance))
    return result


def ring_loft(name, loops, material):
    """Skin a closed path of equal-size loops, useful for cast vessels and rolled rims."""
    n=len(loops[0]);m=len(loops)
    vertices=[tuple(v) for loop in loops for v in loop]
    faces=[(j*n+i,j*n+(i+1)%n,((j+1)%m)*n+(i+1)%n,((j+1)%m)*n+i)
           for j in range(m) for i in range(n)]
    return mesh(name,vertices,faces,material)


def hollow_section(name, path, section, material):
    """Loft a closed, thin-wall section through authored (x,y,z) stations."""
    return loft(name,[[(x+u,y+v,z) for u,v in section] for x,y,z in path],material)


def fastener(name, position, direction, material, radius=.0045, high=True,
             kind='hex', washer=True):
    """Source recesses use explicit manifold radial topology; game heads are simple.

    Washers, drive recesses and sub-millimeter radii are normal-map detail in the
    game version. No fragile overlapping Boolean cuts are needed for a Phillips head.
    """
    direction=Vector(direction).normalized();p=Vector(position)
    q=direction.to_track_quat('Z','Y').to_matrix().to_4x4();q.translation=p
    if not high:
        head=lathe(name+' head',[(0,0),(0,radius),(.003,radius),(.003,0)],material,6)
        head.matrix_world=q
        return [head]
    parts=[]
    if washer:
        w=lathe(name+' washer',[(0,radius*.54),(0,radius*1.38),(.0008,radius*1.38),
                                (.0008,radius*.54)],material,24,closed=True)
        w.matrix_world=q;parts.append(w)
    z=.0008 if washer else 0
    if kind=='hex':
        head=lathe(name+' head',[(z,0),(z,radius*.90),(z+.0003,radius),
                   (z+.0025,radius),(z+.003,radius*.88),(z+.003,0)],material,6)
    else:
        count=64;loops=[]
        for zz,rr in [(z,radius*.90),(z+.0003,radius),(z+.0024,radius),(z+.003,radius*.88)]:
            loops.append([(rr*math.cos(i*math.tau/count),rr*math.sin(i*math.tau/count),zz) for i in range(count)])
        drive=[]
        for i in range(count):
            t=i*math.tau/count;co=abs(math.cos(t));si=abs(math.sin(t))
            if kind=='cross':
                a=min(radius*.64/max(co,1e-9),radius*.15/max(si,1e-9))
                b=min(radius*.15/max(co,1e-9),radius*.64/max(si,1e-9))
                r=max(a,b)
            else:r=radius*.46/math.cos((t+math.pi/6)%(math.pi/3)-math.pi/6)
            drive.append((r*math.cos(t),r*math.sin(t)))
        loops.append([(x,y,z+.003) for x,y in drive])
        loops.append([(x,y,z+.0011) for x,y in drive])
        head=loft(name+' head',loops,material)
        # A drive floor is star-shaped. An explicit center fan avoids sliver
        # triangles from triangulating its many collinear concave outline points.
        bm=bmesh.new();bm.from_mesh(head.data);bm.faces.ensure_lookup_table()
        floor=bm.faces[-1]
        bmesh.ops.poke(bm,faces=[floor],center_mode='MEAN_WEIGHTED')
        bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
        bm.to_mesh(head.data);bm.free();smooth(head,35)
    head.matrix_world=q;parts.append(head)
    return parts


def weld(name, points, radius, material, high=True):
    """Small authored seam with a restrained rippled bead in the source mesh."""
    ob=tube(name,points,radius,material,8 if high else 5)
    if high:
        for v in ob.data.vertices:
            ripple=1+.10*math.sin(v.co.length*math.tau/.0017)
            # Small transverse variation; never distort the structural path.
            v.co.z+=radius*.10*(ripple-1)
    return ob
