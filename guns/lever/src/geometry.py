"""Original compound surfaces and manufactured visual parts, authored in mm.

No reference pixels, foreign meshes or external material assets are read here.
The retained dense furniture is a sculpt source; only its reduced copy ships.
"""
import math
import bpy
import bmesh
from mathutils import Matrix, Vector
from kit import model as M

PARTS = []
HIGH = {}
NORMAL_HIGH = {}
MAT = {}


def palette():
    for key, color, metallic, rough in [
        ('blue', (.010, .0105, .011), .8, .38),
        ('wood', (.018, .0075, .0025), 0, .53),
        ('steel', (.24, .25, .26), 1, .32),
        ('dark', (.025, .026, .027), 1, .43),
        ('brass', (.46, .29, .085), 1, .30),
        ('copper', (.39, .145, .055), 1, .32),
        ('lead', (.13, .135, .14), .85, .50),
        ('stamp', (.025, .021, .014), 1, .48),
    ]:
        mat = bpy.data.materials.new('CP_'+key)
        mat.use_nodes = True
        bs = mat.node_tree.nodes['Principled BSDF']
        bs.inputs['Base Color'].default_value = (*color, 1)
        bs.inputs['Metallic'].default_value = metallic
        bs.inputs['Roughness'].default_value = rough
        if key=='wood':bs.inputs['Specular IOR Level'].default_value=.3
        mat.diffuse_color = (*color, 1)
        MAT[key] = mat


def freeze(ob):
    M.apply(ob)
    ob.data.transform(ob.matrix_world)
    ob.matrix_world = Matrix.Identity(4)
    return ob


def reg(ob, bone='Root', radius=0, segments=2):
    freeze(ob)
    if radius:
        M.bevel(ob, radius, segments)
        n = ob.modifiers.new('Machined area normals', 'WEIGHTED_NORMAL')
        n.keep_sharp = True
    M.apply(ob)
    bm = bmesh.new(); bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(ob.data); bm.free()
    M.smooth(ob, 42)
    ob['bone'] = bone
    ob['asset_set'] = 'Lever'
    ob['part_name'] = ob.name
    PARTS.append(ob)
    return ob


def box(name, lo, hi, mat='blue', bone='Root', r=.3, raw=False):
    lo, hi = Vector(lo), Vector(hi)
    ob = M.box(name, (lo+hi)/2, hi-lo, MAT[mat], 0)
    freeze(ob)
    return ob if raw else reg(ob, bone, r)


def profile(name, points, lo, hi, mat='blue', bone='Root', axis='X', r=.3, raw=False):
    ob = M.profile(name, points, lo, hi, MAT[mat], axis=axis)
    return ob if raw else reg(ob, bone, r)


def lathe(name, points, mat='blue', bone='Root', axis='Y', center=(0,48), n=48, closed=False, raw=False):
    ob = M.lathe(name, points, MAT[mat], segments=n, axis=axis, center=center, closed=closed)
    return ob if raw else reg(ob, bone)


def cut(ob, tool, operation='DIFFERENCE'):
    mat = ob.data.materials[0]
    tool.data.materials.clear(); tool.data.materials.append(mat)
    mod = ob.modifiers.new('Machined cavity', 'BOOLEAN')
    mod.operation = operation; mod.solver = ob.get('boolean_solver','MANIFOLD'); mod.object = tool
    M.apply(ob); bpy.data.objects.remove(tool, do_unlink=True)
    ob.data.materials.clear(); ob.data.materials.append(mat)
    for f in ob.data.polygons: f.material_index = 0
    return ob


def cutbox(ob, lo, hi, r=0):
    tool = box('tool', lo, hi, raw=True)
    if r: M.bevel(tool, r, 4); M.apply(tool)
    return cut(ob, tool)


def subdivide(ob, levels):
    mod = ob.modifiers.new('Carved compound cage', 'SUBSURF')
    mod.levels = mod.render_levels = levels
    M.apply(ob)
    return ob


def triangulate_cuts(ob):
    if ob.get('boolean_solver')!='EXACT':return ob
    if any(len(p.vertices)>3 for p in ob.data.polygons):
        mod=ob.modifiers.new('Concave cut tessellation','TRIANGULATE')
        mod.ngon_method='CLIP';mod.keep_custom_normals=True;M.apply(ob)
    bm=bmesh.new();bm.from_mesh(ob.data);removed=0
    while True:
        # Concave Boolean n-gons occasionally tessellate a dangling triangle
        # fin: two free edges and one edge with three incident faces. A fin
        # has no enclosed volume. Remove only this exact topology, never a
        # boundary of the intended solid or a nontrivial surface patch.
        fins=[f for f in bm.faces if len(f.verts)==3
              and sum(e.is_boundary for e in f.edges)==2
              and any(len(e.link_faces)>2 for e in f.edges)]
        if not fins:break
        removed+=len(fins);bmesh.ops.delete(bm,geom=fins,context='FACES')
    if removed:
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data)
        ob['numerical_triangle_fins_removed']=ob.get('numerical_triangle_fins_removed',0)+removed
    bm.free()
    return ob


def dense(ob):
    triangulate_cuts(ob)
    HIGH[ob.name] = ob.data.copy()
    ob['sculpt_method'] = 'subdivision cage with independent width, comb, belly and section curvature'


def reduce(ob, budget):
    triangulate_cuts(ob)
    count = sum(len(p.vertices)-2 for p in ob.data.polygons)
    if count > budget:
        mod = ob.modifiers.new('Silhouette budget', 'DECIMATE')
        mod.ratio = budget/count
        mod.use_collapse_triangulate=ob.get('boolean_solver')=='EXACT'
        M.apply(ob)
        triangulate_cuts(ob)
    return ob


def screw(name, pos, radius=2.6, axis='X', direction=1, bone='Root'):
    x, y, z = pos
    h = {'X':x, 'Y':y, 'Z':z}[axis]
    center = (y,z) if axis=='X' else ((x,z) if axis=='Y' else (x,y))
    ob = lathe(name, [(h-.8,0),(h-.8,radius*.85),(h-.1,radius),
                     (h+.55,radius),(h+.75,radius*.87),(h+.75,0)],
               'blue', bone, axis, center, n=16, raw=True)
    if axis=='X': tool=box('tool',(h+.22,y-radius-1,z-.42),(h+2,y+radius+1,z+.42),raw=True)
    elif axis=='Z': tool=box('tool',(x-radius-1,y-.42,h+.22),(x+radius+1,y+.42,h+2),raw=True)
    else: tool=box('tool',(x-radius-1,h+.22,z-.42),(x+radius+1,h+2,z+.42),raw=True)
    cut(ob, tool)
    if direction<0:
        k='XYZ'.index(axis)
        for v in ob.data.vertices: v.co[k]=2*h-v.co[k]
    return reg(ob, bone)


def sweep(name, path, width, depth, mat='blue', bone='Root', closed=False, section_segments=3):
    """Forged flat bar: a rounded rectangular section, never a circular wire."""
    loops=[]
    for i,(y,z) in enumerate(path):
        prev=Vector(path[(i-1)%len(path)] if closed else path[max(0,i-1)])
        nex=Vector(path[(i+1)%len(path)] if closed else path[min(len(path)-1,i+1)])
        tangent=(nex-prev).normalized(); normal=Vector((-tangent.y,tangent.x))
        section=M.rounded_rectangle(width,depth,min(.6,depth*.28),section_segments)
        loops.append([(x,y+d*normal.x,z+d*normal.y) for x,d in section])
    if closed:loops.append(loops[0])
    ob=M.loft(name,loops,MAT[mat],caps=not closed)
    if closed:
        bm=bmesh.new();bm.from_mesh(ob.data)
        bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001)
        bm.to_mesh(ob.data);bm.free()
    return reg(ob,bone)


def circle_path(y,z,ry,rz,count=56,tilt=0):
    a=math.radians(tilt);out=[]
    for i in range(count):
        t=math.tau*i/count;u=ry*math.cos(t);v=rz*math.sin(t)
        out.append((y+u*math.cos(a)-v*math.sin(a),z+u*math.sin(a)+v*math.cos(a)))
    return out


def rotate_points(ob, pivot, degrees, axis='X'):
    transform=Matrix.Translation(Vector(pivot)) @ Matrix.Rotation(math.radians(degrees),4,axis) @ Matrix.Translation(-Vector(pivot))
    ob.data.transform(transform)
    return ob
