"""Tessellate the remeshed machined roof into an integral R0.60 recess lip.

The top shares its exact boundary vertices with the lip. No tangent Boolean
intersection is involved. A constrained 2-D triangulation chooses topology
only; every roof height comes from the original signed-distance zero set.
"""
import math
from mathutils import Vector
from mathutils.geometry import delaunay_2d_cdt
from head_surface import height

def bezier(a,b,c,d,n):
    return [tuple((1-t)**3*a[k]+3*t*(1-t)**2*b[k]+3*t*t*(1-t)*c[k]+t**3*d[k] for k in range(2))
            for t in (i/n for i in range(n+1))]

def inside(p, polygon):
    x,y=p; result=False
    for a,b in zip(polygon,polygon[1:]+polygon[:1]):
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]: result=not result
    return result

def recess_profiles():
    r=5.9
    outline=[(r*math.cos(t),94+r*math.sin(t)) for t in (math.pi*i/256 for i in range(257))]
    outline+=bezier((-r,94),(-r,92),(-6.2,90),(-6.7,88.5),64)[1:]
    outline+=bezier((-6.7,88.5),(-7.2,86.7),(-3.0,86.3),(0,86.3),64)[1:]
    outline+=bezier((0,86.3),(3.8,86.3),(10.5,86.7),(9.2,88.5),128)[1:]
    outline+=bezier((9.2,88.5),(7.4,91),(r,92),(r,94),80)[1:-1]
    profiles=[]
    for i,(x,y) in enumerate(outline):
        tangent=Vector(outline[(i+1)%len(outline)])-Vector(outline[i-1])
        n=Vector((tangent.y,-tangent.x)).normalized(); radius=.6
        roof=lambda d:height(x+n.x*d,y+n.y*d)
        derivative=lambda d:(roof(d+.002)-roof(d-.002))/.004
        lo=0.; hi=radius*2
        for _ in range(30):
            d=(lo+hi)*.5; q=derivative(d)
            if d-radius+radius*q/math.sqrt(1+q*q)>0:hi=d
            else:lo=d
        d=(lo+hi)*.5;q=derivative(d)
        zc=roof(d)-radius/math.sqrt(1+q*q); end=math.atan2(1,-q)
        arc=[]
        for j in range(25):
            angle=end+(math.pi-end)*j/24
            offset=radius*(1+math.cos(angle))
            arc.append((x+n.x*offset,y+n.y*offset,zc+radius*math.sin(angle)))
        # Floor is below the full lip even at the shallow rear heel. Its
        # fore half remains Z48 around the unchanged boss/spindle.
        floor=48+.4*min(0,y-94)
        assert floor<zc-.1,(x,y,zc,floor)
        profiles.append([*arc,(x,y,floor)])
    return profiles

def upper_mesh(roofloops):
    """Return roof/lip/floor vertices and faces; outer boundary stays exact."""
    outer=[*roofloops[0],*[row[-1] for row in roofloops[1:]],
        *roofloops[-1][-2::-1],*[row[0] for row in roofloops[-2:0:-1]]]
    outer_xy=[tuple(p[:2]) for p in outer]
    profiles=recess_profiles(); hole=[p[0][:2] for p in profiles]
    assert all(inside(p,outer_xy) for p in hole),'Recess lip must be wholly within the upper head'
    points=[]; edges=[]
    # Insert constraints first so their exact coordinates own coincident
    # dense-grid samples. Grid samples inside the opening are omitted.
    for polygon in (outer_xy,hole):
        start=len(points);points.extend(polygon)
        edges.extend((start+i,start+(i+1)%len(polygon)) for i in range(len(polygon)))
    for row in roofloops[1:-1]:
        points.extend(p[:2] for p in row[1:-1] if not inside(p[:2],hole))
    vs,_,triangles,_,_,_=delaunay_2d_cdt([Vector(p) for p in points],edges,[],0,.000001,False)
    vertices=[(p.x,p.y,height(p.x,p.y)) for p in vs]
    faces=[];regions=[]
    for triangle in triangles:
        c=tuple(sum(vs[i][k] for i in triangle)/len(triangle) for k in (0,1))
        if inside(c,outer_xy) and not inside(c,hole): faces.append(tuple(triangle));regions.append(1)
    # The triangulator can split a boundary segment at an existing roof
    # sample. Recover those points in perimeter order, then interpolate the
    # arc profiles to the same fractions. This creates no T-junctions.
    boundary={}
    for face in faces:
        for a,b in zip(face,face[1:]+face[:1]):
            key=tuple(sorted((a,b)));boundary[key]=boundary.get(key,0)+1
    ids={i for edge,count in boundary.items() if count==1 for i in edge}
    ring=[]
    for j,(a,b) in enumerate(zip(hole,hole[1:]+hole[:1])):
        a,b=Vector(a),Vector(b);delta=b-a;length=delta.length_squared;candidates=[]
        for i in ids:
            t=(vs[i]-a).dot(delta)/length
            if -.00001<=t<.99999 and (vs[i]-(a+delta*t)).length<.00003:
                candidates.append((max(0,t),i))
        for t,i in sorted(candidates):
            profile=[]
            for p,q in zip(profiles[j],profiles[(j+1)%len(profiles)]):
                profile.append(tuple(p[k]*(1-t)+q[k]*t for k in range(3)))
            # Use the actual shared top point. Its deviation from the
            # circular sample is only the constrained segment chord error.
            profile[0]=vertices[i];ring.append((i,profile))
    assert len(ring)>=len(profiles),(len(ring),len(profiles))
    previous=[i for i,p in ring]
    for row in range(1,len(profiles[0])):
        current=[]
        for i,profile in ring:
            current.append(len(vertices));vertices.append(profile[row])
        faces.extend((previous[i],previous[(i+1)%len(ring)],current[(i+1)%len(ring)],current[i]) for i in range(len(ring)))
        regions.extend([2]*len(ring))
        previous=current
    center=len(vertices);vertices.append((0,94,48))
    faces.extend((center,previous[i],previous[(i+1)%len(ring)]) for i in range(len(ring)))
    regions.extend([3]*len(ring))
    return vertices,faces,regions
