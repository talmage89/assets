"""X220 fascia sculpture: original authored curves on the continuous parent.

No reference data is imported here. End-plan and construction measurements live
in the independent review tools. All mouth guides are projected AFTER the fair
sheet is evaluated; this file never changes an evaluated body vertex.
"""
import math
import bpy,bmesh
from mathutils import Vector
from kit import model as G


def lower_edge(x,front):
    """Painted corners descend past a high central intake surround."""
    from suv_body import smoothstep
    if front:return .615-.210*smoothstep(.52,.81,abs(x))
    return .545-.035*smoothstep(.52,.86,abs(x))


def split_lower(source,names):
    """Split open polygons on a curved molding edge, preserving their planes."""
    vertices=[];faces=[];labels=[]
    for f in source.data.polygons:
        label=names[f.material_index]
        front=label=='Front molded fascia'
        if label not in ['Front molded fascia','Rear molded fascia']:
            pieces=[([source.data.vertices[i].co.copy() for i in f.vertices],f.material_index)]
        else:
            poly=[source.data.vertices[i].co.copy() for i in f.vertices];upper=[];lower=[]
            for a,c in zip(poly,poly[1:]+poly[:1]):
                da=a.z-lower_edge(a.x,front);dc=c.z-lower_edge(c.x,front)
                (upper if da>=0 else lower).append(a)
                if da*dc<0:
                    # Bisection follows the original straight mesh edge exactly.
                    lo,hi=0.,1.
                    for _ in range(32):
                        t=(lo+hi)/2;p=a.lerp(c,t);d=p.z-lower_edge(p.x,front)
                        if d*da>0:lo=t
                        else:hi=t
                    p=a.lerp(c,(lo+hi)/2);upper.append(p);lower.append(p)
            pieces=[(upper,f.material_index),(lower,names.index(('Front' if front else 'Rear')+' lower bumper cladding'))]
        for poly,idx in pieces:
            if len(poly)<3:continue
            offset=len(vertices);vertices.extend(poly);faces.append(tuple(range(offset,len(vertices))));labels.append(idx)
    old=source.data;mesh=bpy.data.meshes.new('Curved molding boundaries');mesh.from_pydata(vertices,[],faces);mesh.update()
    for mat in old.materials:mesh.materials.append(mat)
    for f,i in zip(mesh.polygons,labels):f.material_index=i
    source.data=mesh
    if old.users==0:bpy.data.meshes.remove(old)
    bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
    from suv_body import conform_edges
    conform_edges(bm);bm.to_mesh(mesh);bm.free()


def radial_point(tree,theta,z,front,sign):
    center=Vector((0,-1.37 if front else 1.42,z))
    direction=Vector((sign*math.sin(theta),(-1 if front else 1)*math.cos(theta),0))
    hit,n,_,_=tree.ray_cast(center+direction*2,-direction,2)
    if hit is None:raise ValueError(('Optical guide missed parent',theta,z,front))
    if n.dot(direction)<0:n=-n
    return hit,n


def lamps(b,front,sign,material,tree):
    """Monotone polar guides cannot jump from a lamp to the hood or backlight.

    Vertically ruled front units grow toward the outside corner then taper into
    the fender. The rear wrap is one shape split on the exact gate plane.
    """
    from suv_body import smoothstep
    from suv_spec import PANEL_GAP
    n=32 if b.high else 24
    rows=[];nv=5 if b.high else 3
    for j in range(nv):
        v=j/(nv-1);row=[]
        for i in range(n+1):
            u=i/n
            if front:
                theta=math.radians(36+39*u)
                # Find the outside hood roll at this azimuth, then seat the
                # optical upper edge 18 mm below it. A prescribed Z ramp can
                # jump inward over a raised hood ridge, making a torn corner.
                from suv_body import hood_height
                probe,_=radial_point(tree,theta,.90,True,sign)
                for _ in range(5):
                    top=hood_height(probe.x,probe.y)-.018
                    probe,_=radial_point(tree,theta,top,True,sign)
                height=(.078+.080*smoothstep(0,.55,u))*(1-.87*smoothstep(.75,1,u))
            else:
                theta=math.radians(21+55*u)
                top=1.166+.023*math.sin(math.pi*u)-.060*smoothstep(.78,1,u)
                height=(.074+.103*smoothstep(0,.55,u))*(1-.87*smoothstep(.78,1,u))
            hit,normal=radial_point(tree,theta,top-height*(1-v),front,sign)
            row.append(hit+normal*.004)
        rows.append(row)
    if front:groups=[('',rows)]
    else:
        groups=[]
        for inner in [True,False]:
            subset=[];xx=.745+(-1 if inner else 1)*PANEL_GAP/2
            for row in rows:
                pair=next((a,c) for a,c in zip(row,row[1:]) if abs(a.x)<=xx<=abs(c.x))
                a,c=pair;t=(xx-abs(a.x))/(abs(c.x)-abs(a.x));p=a.lerp(c,t)
                keep=[q for q in row if (abs(q.x)<xx if inner else abs(q.x)>xx)]
                subset.append(keep+[p] if inner else [p]+keep)
            # A fixed angular station count would otherwise change across the
            # seam with height; reparameterize each side by its own arc length.
            count=17 if inner else 13;regular=[]
            for row in subset:
                ds=[0.]
                for a,c in zip(row,row[1:]):ds.append(ds[-1]+(c-a).length)
                regular_row=[]
                for i in range(count):
                    d=ds[-1]*i/(count-1);k=next((k for k in range(len(ds)-1) if ds[k+1]>=d),len(ds)-2)
                    regular_row.append(row[k].lerp(row[k+1],(d-ds[k])/max(1e-9,ds[k+1]-ds[k])))
                regular.append(regular_row)
            groups.append((' gate' if inner else ' quarter',regular))
    result=[]
    for suffix,rows in groups:
        verts=[p for row in rows for p in row];nu=len(rows[0]);nv=len(rows)
        ob=G.mesh(('Headlamp' if front else 'Taillamp')+' opening'+str(sign)+suffix,verts,[(j*nu+i,j*nu+i+1,(j+1)*nu+i+1,(j+1)*nu+i) for j in range(nv-1) for i in range(nu-1)],material)
        ob['form_rows']=nv;ob['form_columns']=nu;ob['aperture_samples']=[q for p in verts for q in p]
        ob['polar_optical_guide']=True
        if not front:ob['lamp_piece']=suffix.strip()
        result.append(ob)
    return result


def grille_lip(b,blank,surface):
    """A 16 mm folded surround follows the actual mouth and stands 7 mm proud."""
    from suv_apertures import surface_uv,boundary_indices
    raw=list(blank['well_mouth_samples']);loop=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    center=sum(loop,Vector())/len(loop);rings=[]
    for width,height in [(0,.001),(.003,.007),(.014,.007),(.018,.001)]:
        ring=[]
        for p in loop:
            _,n=surface_uv(p,surface);radial=p-center;radial-=n*radial.dot(n);radial.normalize()
            q=p+radial*width;hit,_,_,_=surface['tree'].find_nearest(q);_,nn=surface_uv(hit,surface)
            ring.append(hit+nn*height)
        rings.append(ring)
    ob=G.loft('Grille folded surround',rings,b.m['bumper'],caps=False)
    sol=ob.modifiers.new('Surround molded gauge','SOLIDIFY');sol.thickness=.002;sol.offset=-1;G.apply(ob)
    b.add(ob,category='openings')


def rear_garnish(b,tree):
    """The parent gate carries the transverse crease; add its badge seat."""
    # The earlier separate narrow bridge read as a tube in grazing light.
    # Keep the stamped shoulder itself as Alder's lamp-to-lamp treatment.
    badge_land(b,tree)


def badge_land(b,tree):
    """Small unmarked medallion seat in the garnish; no borrowed identity."""
    outline=[(.039*math.cos(math.tau*i/20),1.129+.027*math.sin(math.tau*i/20)) for i in range(20)]
    rings=[]
    for depth in [.006,.009]:
        ring=[]
        for x,z in outline:
            p,n,_,_=tree.ray_cast(Vector((x,3,z)),Vector((0,-1,0)),2)
            ring.append(p+n*depth)
        rings.append(ring)
    ob=G.loft('Liftgate badge mounting land',rings,b.m['body'])
    b.add(ob,bpy.data.objects['Liftgate'],category='openings')
