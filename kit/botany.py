"""Original plant geometry primitives; meters, deterministic input, no external assets.

Growth rules belong to the species/family. This module only sweeps supplied
centerlines and assembles oriented alpha cards, custom normals and wind data.
"""
import math
import bpy
import bmesh
from mathutils import Vector
from kit import model as G


def sweep(name, points, radii, material, sides=8, phase=0, base_lobes=0):
    """Parallel-transport tapered stem with optional buttress lobes at its foot.

    Radii and stations are supplied by growth rules. Root collars swell in the
    first radii; section ellipticity varies gently rather than making straight
    manufactured tubes. Bases/tips are capped to support independent audits.
    """
    points=list(map(Vector,points));loops=[];previous=None
    for i,(p,radius) in enumerate(zip(points,radii)):
        tangent=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized()
        if previous is None:
            seed=Vector((1,0,0)) if abs(tangent.z)>.9 else Vector((0,0,1))
            u=tangent.cross(seed).normalized()
        else:u=(previous-tangent*previous.dot(tangent)).normalized()
        v=tangent.cross(u).normalized();previous=u
        loop=[]
        for k in range(sides):
            a=k*math.tau/sides
            lobe=base_lobes*math.exp(-p.z*4)*(0.5+0.5*math.cos(5*a+phase))
            uneven=1+.035*math.sin(3*a+phase+i*.31)+lobe
            loop.append(p+radius*uneven*(u*math.cos(a)+v*math.sin(a)))
        loops.append(loop)
    return G.smooth(G.loft(name,loops,material),85)


def wind_attribute(ob, values):
    """RGBA = sway weight, hierarchy / 4, stable branch phase, leaf flutter.

    Engine-specific wind conventions differ. This is an explicit normalized
    convention, named Wind, not a color tint and never connected to BaseColor.
    """
    color=ob.data.color_attributes.new(name='Wind',type='FLOAT_COLOR',domain='POINT')
    for item,value in zip(color.data,values):item.color=value
    # Do not implicitly make wind a glTF BaseColor multiplier.
    ob.data.color_attributes.active_color_index=0
    ob['wind_channels']='R sway; G branch level/4; B phase; A flutter'
    return color


class Cards:
    """Accumulate independently oriented cards with outward-bent loop normals."""
    def __init__(self):
        self.vertices=[];self.faces=[];self.uvs=[];self.normals=[];self.wind=[]
        self.centers=[];self.widths=[];self.normal_bends=[];self.clump_blends=[]

    def add(self,center,normal,roll,size,rect,crown_center,wind,normal_bend=.72,
            clump_center=None,clump_blend=0):
        c=Vector(center);n=Vector(normal).normalized()
        seed=Vector((0,0,1)) if abs(n.z)<.95 else Vector((1,0,0))
        u=n.cross(seed).normalized();v=n.cross(u).normalized()
        u,v=u*math.cos(roll)+v*math.sin(roll),-u*math.sin(roll)+v*math.cos(roll)
        start=len(self.vertices);u0,v0,u1,v1=rect
        self.faces.append(tuple(start+i for i in range(4)))
        for x,y in ((-1,-1),(1,-1),(1,1),(-1,1)):
            p=c+(u*x+v*y)*size/2;self.vertices.append(tuple(p))
            outward=(p-Vector(crown_center)).normalized()
            if clump_center is not None:
                local=(p-Vector(clump_center)).normalized()
                outward=(outward*(1-clump_blend)+local*clump_blend).normalized()
            # Keep custom normals in the geometric front hemisphere. Double-sided
            # engines flip the backface normal; no camera-dependent card facing.
            if outward.dot(n)<0:outward=-outward
            self.normals.append(tuple((n*(1-normal_bend)+outward*normal_bend).normalized()))
            self.wind.append(wind)
        self.uvs.extend([(u0,v0),(u1,v0),(u1,v1),(u0,v1)])
        self.centers.append(tuple(c));self.widths.append(size)
        self.normal_bends.append(normal_bend);self.clump_blends.append(clump_blend if clump_center is not None else 0)

    def add_grid(self,grid,rect,wind):
        """Append a supplied curved rectangular alpha patch with physical normals.

        Rows follow texture V; columns follow U. Finite differences retain cup,
        droop or folds without bending every surface toward a crown. Geometry
        shape/species and texture outlines remain caller-owned. Existing flat
        card assembly and its defaults are unchanged.
        """
        rows=len(grid);cols=len(grid[0])
        if rows<2 or cols<2 or any(len(row)!=cols for row in grid):
            raise ValueError('Alpha patch needs a rectangular grid >=2 by 2')
        points=[[Vector(p) for p in row] for row in grid];start=len(self.vertices)
        u0,v0,u1,v1=rect
        for y,row in enumerate(points):
            for x,p in enumerate(row):
                du=row[min(x+1,cols-1)]-row[max(0,x-1)]
                dv=points[min(y+1,rows-1)][x]-points[max(0,y-1)][x]
                n=du.cross(dv)
                if n.length<1e-10:raise ValueError('Degenerate alpha patch tangent')
                self.vertices.append(tuple(p));self.normals.append(tuple(n.normalized()))
                self.uvs.append((u0+(u1-u0)*x/(cols-1),v0+(v1-v0)*y/(rows-1)))
                self.wind.append(wind)
        for y in range(rows-1):
            for x in range(cols-1):
                ids=(start+y*cols+x,start+y*cols+x+1,start+(y+1)*cols+x+1,start+(y+1)*cols+x)
                self.faces.append(ids)
                self.centers.append(tuple(sum((Vector(self.vertices[i]) for i in ids),Vector())/4))
                self.widths.append((points[y][x+1]-points[y][x]).length)
                self.normal_bends.append(0);self.clump_blends.append(0)

    def mesh(self,name,material):
        # Avoid closed-solid normal recalculation: authored winding is intentional.
        me=bpy.data.meshes.new(name);me.from_pydata(self.vertices,[],self.faces);me.update()
        ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob)
        me.materials.append(material);uv=me.uv_layers.new(name='BakeUV')
        for loop in me.loops:uv.data[loop.index].uv=self.uvs[loop.vertex_index]
        for p in me.polygons:p.use_smooth=True
        me.normals_split_custom_set([self.normals[loop.vertex_index] for loop in me.loops])
        wind_attribute(ob,self.wind);ob['allow_boundary']=True
        ob['normal_bend']=self.normal_bends[0]
        ob['clump_blend']=self.clump_blends[0]
        ob['normal_policy']='Authored crown/clump radial blend then card bend, hemisphere-corrected'
        return ob


def fuse_stems(objects, name='Fused branch unions', voxel_size=.018, triangle_target=4500, connected_only=False):
    """Fuse coarse woody forks/roots; retain finer twigs as separate components.

    A voxel union removes hidden intersecting branch walls. Gentle relaxation
    rounds living collars, followed by silhouette-conscious decimation. Callers
    must restore attributes on the regenerated surface and measure the result.
    No UVs or custom normals survive; run this before final UV/baking.
    """
    bpy.ops.object.select_all(action='DESELECT')
    for ob in objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join()
    ob=objects[0];ob.name=name
    remesh=ob.modifiers.new('Living wood union','REMESH');remesh.mode='VOXEL'
    remesh.voxel_size=voxel_size;remesh.use_smooth_shade=True;G.apply(ob)
    if connected_only:
        # A rooted plant is one coarse solid. Sub-voxel twig remnants can form
        # disconnected crumbs; retain the rooted (largest) surface explicitly.
        bm=bmesh.new();bm.from_mesh(ob.data);remaining=set(bm.verts);components=[]
        while remaining:
            start=remaining.pop();component={start};stack=[start]
            while stack:
                vertex=stack.pop()
                for edge in vertex.link_edges:
                    other=edge.other_vert(vertex)
                    if other in remaining:remaining.remove(other);component.add(other);stack.append(other)
            components.append(component)
        keep=max(components,key=len)
        bmesh.ops.delete(bm,geom=[v for component in components if component is not keep for v in component],context='VERTS')
        bm.to_mesh(ob.data);bm.free();ob.data.update()
    relax=ob.modifiers.new('Collar relaxation','SMOOTH');relax.factor=.6;relax.iterations=4;G.apply(ob)
    ob.data.calc_loop_triangles();count=len(ob.data.loop_triangles)
    if count>triangle_target:
        dec=ob.modifiers.new('Wood silhouette budget','DECIMATE');dec.ratio=triangle_target/count
        dec.use_collapse_triangulate=True;G.apply(ob)
    # Voxel grids can leave coincident vertices / submicron collapse slivers at
    # narrow tips. Weld/dissolve before the independent manifold/area audit.
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-5)
    bmesh.ops.delete(bm,geom=[e for e in bm.edges if not e.link_faces],context='EDGES')
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_edges],context='VERTS')
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(ob.data);bm.free();ob.data.update()
    G.smooth(ob,85)
    return ob
