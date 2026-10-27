"""Small vehicle construction primitives. Meters, wheel spindle along X.

No reference pixels enter this module. Surfaces are authored functions; all
separate panels may evaluate the same function to preserve cross-seam normals.
"""
import math
import bpy
from mathutils import Vector
from kit import model as G


def panel(name, surface, us, vs, material, outward, gauge=.0009, return_depth=.012):
    """Sample an analytic skin with edge returns, then close its sheet gauge.

    us/vs are explicit knot lists so silhouettes and styling creases can receive
    more samples. Returns run inward along the local normal. Each edge ends in
    a closed gauge, rather than pretending the sheet is a zero-thickness plane.
    """
    nu,nv=len(us),len(vs)
    verts=[tuple(surface(u,v)) for v in vs for u in us]
    faces=[(j*nu+i,j*nu+i+1,(j+1)*nu+i+1,(j+1)*nu+i)
           for j in range(nv-1) for i in range(nu-1)]
    a,b,c=(Vector(verts[k]) for k in faces[0][:3])
    if (b-a).cross(c-a).dot(Vector(outward))<0:
        faces=[tuple(reversed(f)) for f in faces]
    # Consistent perimeter winding from the face edges, independent of grid direction.
    boundary={}
    for face in faces:
        for a,b in zip(face,face[1:]+face[:1]):
            key=tuple(sorted((a,b)))
            if key in boundary:del boundary[key]
            else:boundary[key]=(a,b)
    if return_depth:
        normals={i:Vector((0,0,0)) for edge in boundary.values() for i in edge}
        for face in faces:
            a,b,c=(Vector(verts[k]) for k in face[:3]);n=(b-a).cross(c-a).normalized()
            for i in face:
                if i in normals:normals[i]+=n
        inner={}
        for i,n in normals.items():
            inner[i]=len(verts);verts.append(tuple(Vector(verts[i])-n.normalized()*return_depth))
        faces.extend((b,a,inner[a],inner[b]) for a,b in boundary.values())
    ob=G.mesh(name,verts,faces,material)
    mod=ob.modifiers.new('Closed sheet gauge','SOLIDIFY');mod.thickness=gauge;mod.offset=-1
    mod.use_even_offset=True
    G.smooth(ob,35)
    ob['sheet_gauge_m']=gauge;ob['edge_return_m']=return_depth
    return ob


def loaded_tire(name, center, width, aspect, rim_inches, material, segments=96,
                loaded_radius=None):
    """Closed radial carcass, crowned tread, bulged shoulders, smooth contact load.

    ISO size defines nominal radius. A local C1 ground-contact flattening leaves
    the upper carcass unchanged; this is a parked mesh, not a rolling simulation.
    Fine tread and lettering belong to the eventual normal bake.
    """
    rim=rim_inches*.0254/2;radius=rim+width*aspect
    # Axial/radial stations: inward bead -> sidewall -> shoulder -> tread -> outward bead.
    profile=[(-.36*width,rim),(-.45*width,rim+.018),(-.495*width,rim+.075),
             (-.5*width,radius-.057),(-.45*width,radius-.019),(-.37*width,radius-.004),
             (-.25*width,radius-.001),(0,radius),(.25*width,radius-.001),
             (.37*width,radius-.004),(.45*width,radius-.019),(.5*width,radius-.057),
             (.495*width,rim+.075),(.45*width,rim+.018),(.36*width,rim)]
    ob=G.lathe(name,profile,material,segments,axis='X',closed=True)
    h=radius if loaded_radius is None else loaded_radius
    for vertex in ob.data.vertices:
        z=vertex.co.z
        # Smooth maximum(z,-h): exact flat ground below transition; untouched above.
        d=z+h;k=.004
        vertex.co.z=-h+(0 if d<=-k else (d if d>=k else (d+k)**2/(4*k)))
    ob.location=center
    ob['nominal_radius_m']=radius;ob['loaded_radius_m']=h
    ob['tire_size']=f'{round(width*1000)}/{round(aspect*100)}R{rim_inches:g}'
    return ob


def samples(count):
    return [i/count for i in range(count+1)]
