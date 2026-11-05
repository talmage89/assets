"""Camera-facing, contrast-compensated wire inspection, and engine mesh data."""
import math


def data(points,diameter):
    """Two vertices per station. Engine sets NORMAL=tangent, UV2.x=diameter.

    Raw mesh coordinates use the documented Blender frame; convert (x,y,z)
    to (x,z,-y) for glTF/Godot. Expand the MeshInstance custom AABB by at least
    the largest permitted pixel width in world space to avoid culling it.
    """
    vertices=[];normals=[];uv=[];uv2=[];indices=[]
    for i,p in enumerate(points):
        q=points[max(0,i-1)];r=points[min(len(points)-1,i+1)]
        t=[b-a for a,b in zip(q,r)];ln=math.sqrt(sum(v*v for v in t));t=[v/ln for v in t]
        for side in (0,1):
            vertices.append(p);normals.append(t);uv.append((side,i/(len(points)-1)));uv2.append((diameter,0))
        if i:
            j=2*i;indices.extend((j-2,j-1,j+1,j-2,j+1,j))
    return dict(vertices=vertices,normals=normals,uv=uv,uv2=uv2,indices=indices)


def inspection(meta,camera,width,height):
    """Cycles equivalent of the far policy, evaluated for this one camera.

    Only the distance comparison calls this. Ordinary geometry views render
    the unmodified, physically sized exported tubes.
    """
    import bpy
    from mathutils import Vector
    from kit import model as G
    vertices=[];faces=[];alphas=[];colors=[]
    inv=camera.matrix_world.inverted();metres_per_pixel_at_unit=36/camera.data.lens/width
    for span in meta['spans']:
        pts=span['points'];diam=span['diameter_m']
        for i,p in enumerate(pts):
            p=Vector(p);t=(Vector(pts[min(i+1,len(pts)-1)])-Vector(pts[max(i-1,0)])).normalized()
            direction=(camera.location-p).normalized();side=t.cross(direction).normalized()
            depth=max(.1,-(inv@p).z);mpp=depth*metres_per_pixel_at_unit
            true_px=diam/mpp;display_px=max(.85,true_px);w=display_px*mpp
            for sign in (-1,1):
                vertices.append(p+side*w*.5*sign);alphas.append(min(1,(true_px/display_px)**.55))
                colors.append((.012,.013,.012,1) if span.get('material')=='Aluminum' else (.0015,.0017,.0015,1))
            if i:
                j=len(vertices)-2;faces.append((j-2,j-1,j+1,j))
    m=bpy.data.materials.new('Contrast compensated far-wire inspection');m.use_nodes=True
    ns,ls=m.node_tree.nodes,m.node_tree.links;ns.clear()
    attr=ns.new('ShaderNodeAttribute');attr.attribute_name='Coverage'
    color=ns.new('ShaderNodeAttribute');color.attribute_name='LineColor'
    transparent=ns.new('ShaderNodeBsdfTransparent');surface=ns.new('ShaderNodeEmission');ls.new(color.outputs['Color'],surface.inputs['Color'])
    mix=ns.new('ShaderNodeMixShader');out=ns.new('ShaderNodeOutputMaterial')
    ls.new(attr.outputs['Fac'],mix.inputs[0]);ls.new(transparent.outputs[0],mix.inputs[1]);ls.new(surface.outputs[0],mix.inputs[2]);ls.new(mix.outputs[0],out.inputs['Surface'])
    ob=G.mesh('Camera evaluated far-wire ribbons',vertices,faces,m);a=ob.data.attributes.new('Coverage','FLOAT','POINT')
    for d,v in zip(a.data,alphas):d.value=v
    c=ob.data.color_attributes.new('LineColor','FLOAT_COLOR','POINT')
    for d,v in zip(c.data,colors):d.color=v
    ob.visible_shadow=False
    return ob
