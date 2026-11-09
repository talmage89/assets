"""Clip pigment films to the actual exported deck's planar surface pieces.

Four corner rays cannot conform a film crossing a crown or a ramp transition.
This projects every clipped vertex, retaining the original continuous chart.
"""
import math
from mathutils import Vector


class Projector:
    def __init__(self,root,surface):
        self.surface=surface;self.triangles=[];self.grid={};self.pitch=4;self.higher={}
        for ob in root.children_recursive:
            if ob.type!='MESH' or not ob.name.startswith(('Flat_','Ramp_','Grade slab','SpeedRamp','North end grade','Inner closure')):continue
            ob.data.calc_loop_triangles()
            for face in ob.data.loop_triangles:
                points=[ob.matrix_world@ob.data.vertices[i].co for i in face.vertices]
                normal=(points[1]-points[0]).cross(points[2]-points[0])
                if normal.length<1e-10 or normal.normalized().z<.7:continue
                index=len(self.triangles);self.triangles.append((points,normal,min(v.z for v in points),max(v.z for v in points)))
                for x in range(math.floor(min(v.x for v in points)/self.pitch),math.floor(max(v.x for v in points)/self.pitch)+1):
                    for y in range(math.floor(min(v.y for v in points)/self.pitch),math.floor(max(v.y for v in points)/self.pitch)+1):self.grid.setdefault((x,y),[]).append(index)

    def polygons(self,points,uv):
        low=min(v[2] for v in points)-.12;high=max(v[2] for v in points)+.12
        candidates=set()
        for x in range(math.floor(min(v[0] for v in points)/self.pitch),math.floor(max(v[0] for v in points)/self.pitch)+1):
            for y in range(math.floor(min(v[1] for v in points)/self.pitch),math.floor(max(v[1] for v in points)/self.pitch)+1):candidates.update(self.grid.get((x,y),[]))
        original=[Vector((p[0],p[1],t[0],t[1])) for p,t in zip(points,uv)]
        result=[]
        for index in sorted(candidates):
            triangle,normal,z0,z1=self.triangles[index]
            if z1<low or z0>high:continue
            poly=original[:]
            for a,b in zip(triangle,triangle[1:]+triangle[:1]):
                if not poly:break
                def distance(p):return (b.x-a.x)*(p.y-a.y)-(b.y-a.y)*(p.x-a.x)
                clipped=[]
                for p,q in zip(poly,poly[1:]+poly[:1]):
                    dp,dq=distance(p),distance(q)
                    if dp>=-1e-8:clipped.append(p)
                    if (dp>=-1e-8)!=(dq>=-1e-8):clipped.append(p.lerp(q,dp/(dp-dq)))
                poly=clipped
            if len(poly)<3:continue
            # Subtract every higher surface in XY, including partial overlaps.
            # A centroid visibility ray alone misses a topping over one corner
            # of an internal flange, or a raised seal crossing a broad film.
            fragments=self.exposed(poly,index,candidates)
            for poly in fragments:
                area=abs(sum(p.x*q.y-q.x*p.y for p,q in zip(poly,poly[1:]+poly[:1])))/2
                if area<1e-8:continue
                vertices=[]
                for p in poly:
                    a=triangle[0];z=a.z-(normal.x*(p.x-a.x)+normal.y*(p.y-a.y))/normal.z
                    vertices.append((p.x,p.y,z))
                unit=normal.normalized();key=tuple(round(v,4) for v in unit)+(round(-unit.dot(triangle[0]),3),)
                result.append(([(x,y,z+.0012) for x,y,z in vertices],[(p.z,p.w) for p in poly],key))
        return self.compact(result)

    @staticmethod
    def clip(poly,distance,positive):
        out=[]
        for p,q in zip(poly,poly[1:]+poly[:1]):
            dp,dq=distance(p),distance(q);a=dp>=0 if positive else dp<=0;b=dq>=0 if positive else dq<=0
            if a:out.append(p)
            if a!=b:out.append(p.lerp(q,dp/(dp-dq)))
        return out

    def exposed(self,poly,index,candidates):
        tri,n,lo,hi=self.triangles[index]
        def coefficients(t,n):
            a,b=-n.x/n.z,-n.y/n.z;c=t[0].z-a*t[0].x-b*t[0].y
            return a,b,c
        a,b,c=coefficients(tri,n);fragments=[poly]
        if index not in self.higher:
            # A floor triangle is reused by many stains. Cache the potential
            # higher surfaces once, rather than rechecking every level/layer.
            possible=set();xs=[v.x for v in tri];ys=[v.y for v in tri]
            for xx in range(math.floor(min(xs)/self.pitch),math.floor(max(xs)/self.pitch)+1):
                for yy in range(math.floor(min(ys)/self.pitch),math.floor(max(ys)/self.pitch)+1):possible.update(self.grid.get((xx,yy),[]))
            higher=[]
            for other in sorted(possible):
                if other==index:continue
                t,nn,z0,z1=self.triangles[other]
                if z1<lo-.001 or z0>hi+.16:continue
                if max(v.x for v in t)<min(xs) or min(v.x for v in t)>max(xs) or max(v.y for v in t)<min(ys) or min(v.y for v in t)>max(ys):continue
                aa,bb,cc=coefficients(t,nn)
                if max((aa-a)*p.x+(bb-b)*p.y+cc-c for p in tri)>1e-5:higher.append(other)
            self.higher[index]=higher
        minx,maxx=min(p.x for p in poly),max(p.x for p in poly);miny,maxy=min(p.y for p in poly),max(p.y for p in poly)
        for other in self.higher[index]:
            if other==index:continue
            t,n,z0,z1=self.triangles[other]
            if z1<lo-.001 or z0>hi+.16:continue
            if max(v.x for v in t)<minx or min(v.x for v in t)>maxx or max(v.y for v in t)<miny or min(v.y for v in t)>maxy:continue
            aa,bb,cc=coefficients(t,n);da,db,dc=aa-a,bb-b,cc-c-1e-5
            if max(da*p.x+db*p.y+dc for p in poly)<=0:continue
            planes=[lambda p,a=a,b=b:(b.x-a.x)*(p.y-a.y)-(b.y-a.y)*(p.x-a.x) for a,b in zip(t,t[1:]+t[:1])]
            planes.append(lambda p,da=da,db=db,dc=dc:da*p.x+db*p.y+dc)
            result=[]
            for fragment in fragments:
                inside=fragment
                for plane in planes:
                    if len(inside)<3:break
                    outside=self.clip(inside,plane,False)
                    if len(outside)>=3:result.append(outside)
                    inside=self.clip(inside,plane,True)
            fragments=result
            if not fragments:break
        return fragments

    def compact(self,polygons):
        # UV-band edges subdivide a perfectly planar deck without changing
        # its surface. Recombine those coplanar film fragments; retain true
        # crowns/transitions and any significant missing floor area.
        groups={}
        for pts,uv,key in polygons:
            groups.setdefault(key,[]).append((pts,uv))
        output=[]
        def area(points):return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(points,points[1:]+points[:1])))/2
        def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        def flat(a,b,c):return cross(a,b,c)<=2e-5*(math.dist(a,b)+math.dist(b,c))
        for group in groups.values():
            if len(group)==1:output.extend(group);continue
            unique={}
            for pts,uv in group:
                for p,t in zip(pts,uv):unique[(round(p[0],6),round(p[1],6))]=(p,t)
            points=sorted(unique);lower=[];upper=[]
            for p in points:
                while len(lower)>1 and flat(lower[-2],lower[-1],p):lower.pop()
                lower.append(p)
            for p in reversed(points):
                while len(upper)>1 and flat(upper[-2],upper[-1],p):upper.pop()
                upper.append(p)
            hull=lower[:-1]+upper[:-1]
            if len(hull)<3:output.extend(group);continue
            full=area(hull);covered=sum(area(pts) for pts,uv in group)
            # Only unite complete coplanar coverage. Raised seals and voids
            # retain their separately clipped surface fragments.
            if abs(full-covered)>max(1e-7,full*1e-5):output.extend(group);continue
            pts=[unique[p][0] for p in hull];uv=[unique[p][1] for p in hull];valid=True
            origin=Vector(pts[0]);best=max(((Vector(pts[i])-origin).cross(Vector(pts[j])-origin) for i in range(1,len(pts)) for j in range(i+1,len(pts))),key=lambda n:n.length)
            normal=best.normalized()
            if any(abs(normal.dot(Vector(p)-origin))>.00015 for poly,coords in group for p in poly):output.extend(group);continue
            for i in range(1,len(pts)-1):
                a,b,c=map(Vector,(pts[0],pts[i],pts[i+1]))
                for weights in ((1/3,1/3,1/3),(.6,.2,.2),(.2,.6,.2),(.2,.2,.6)):
                    q=a*weights[0]+b*weights[1]+c*weights[2]
                    hit=self.surface.ray_cast(q+Vector((0,0,.20)),Vector((0,0,-1)),.40)
                    if hit[0] is None or abs(hit[0].z-q.z)>.003:valid=False;break
                if not valid:break
            output.extend([(pts,uv)] if valid else group)
        return output
