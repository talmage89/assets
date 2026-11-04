"""Metric lap relief from horizontal unions of the clipped wall skin.

A sweep through envelope vertices and course datums unions their horizontal
intervals. Source triangulation diagonals add no repeated course geometry.
"""
import math
import bpy
from mathutils import Vector


def courses(ob,skin,meta=None,exposure_m=None):
    if ob.get('component')!='wall' or skin not in ('wood','vinyl','aluminum','cement'):return
    me=ob.data;face=ob.get('face')
    outward=Vector(dict(front=(0,-1,0),back=(0,1,0),left=(-1,0,0),right=(1,0,0))[face])
    axis=0 if face in ('front','back') else 1;fixed=1-axis
    exposure=(.2794 if skin=='cement' else .1016) if exposure_m is None else exposure_m
    projection=.00437 if skin=='cement' else .014 if skin=='wood' else .0105
    vs=[];fs=[];cs=[];mis=[];external=[];tint=me.color_attributes['Tint']
    def emit(points,colors,mi,normal=None):
        if len(points)<3:return
        if normal is not None and (points[1]-points[0]).cross(points[2]-points[0]).dot(normal)<0:
            points=points[::-1];colors=colors[::-1]
        start=len(vs);vs.extend(points);cs.extend(colors);fs.append(tuple(range(start,len(vs))));mis.append(mi)
    for p in me.polygons:
        points=[me.vertices[i].co.copy() for i in p.vertices];colors=[Vector(tint.data[i].color) for i in p.vertices]
        if p.normal.dot(outward)>.99:external.append((points,colors[0],p.material_index))
        else:emit(points,colors,p.material_index)
    if not external:return
    lo=min(p.z for poly,c,mi in external for p in poly);hi=max(p.z for poly,c,mi in external for p in poly)
    levels={round(p.z,6) for poly,c,mi in external for p in poly}
    levels.update(round(i*exposure,6) for i in range(math.ceil(lo/exposure),math.floor(hi/exposure)+1))
    if skin=='aluminum':
        levels.update(round(i*exposure+exposure-.0203,6) for i in range(math.floor(lo/exposure),math.ceil(hi/exposure)) if lo<i*exposure+exposure-.0203<hi)
    levels=sorted(levels);base=external[0][0][0][fixed]
    for z0,z1 in zip(levels,levels[1:]):
        if z1-z0<1e-6:continue
        mid=(z0+z1)/2;intervals=[]
        for poly,c,mi in external:
            edges=[]
            for a,b in zip(poly,poly[1:]+poly[:1]):
                if min(a.z,b.z)<mid<max(a.z,b.z):
                    slope=(b[axis]-a[axis])/(b.z-a.z);offset=a[axis]-slope*a.z
                    edges.append((slope*mid+offset,slope,offset))
            if len(edges)>=2:
                edges.sort();intervals.append((edges[0],edges[-1],c,mi))
        intervals.sort(key=lambda v:v[0][0]);unions=[]
        for left,right,c,mi in intervals:
            if unions and left[0]<unions[-1][1][0]+2e-5:
                if right[0]>unions[-1][1][0]:unions[-1]=(unions[-1][0],right,c,mi)
            else:unions.append((left,right,c,mi))
        row=math.floor(mid/exposure)
        def point(edge,z,relief=True):
            p=Vector((0,0,z));p[axis]=edge[1]*z+edge[2];p[fixed]=base
            return p+outward*(projection*(1-min(1,max(0,z/exposure-row)))) if relief else p
        for left,right,c,mi in unions:
            pieces=[(left,right)]
            if skin=='aluminum' and meta:
                block=next(b for b in meta['blocks'] if b['name']==ob.get('block'))
                cuts=[]
                for op in meta['openings']:
                    if op['kind']!='window' or op['block']!=block['name'] or op['face']!=face or not op['z']-1.9<mid<op['z']:continue
                    for side in (-1,1):
                        center=block['x0' if axis==0 else 'y0']+op['u']+side*op['w']/2
                        cuts.extend(center+d for d in (-.08,0,.08) if left[0]+1e-5<center+d<right[0]-1e-5)
                edges=[left]+[(v,0,v) for v in sorted(set(cuts))]+[right]
                pieces=list(zip(edges,edges[1:]))
            for left,right in pieces:
                points=[point(left,z0),point(right,z0),point(right,z1),point(left,z1)]
                if (points[1]-points[0]).length+(points[2]-points[3]).length<1e-6:continue
                clean=[]
                for p in points:
                    if not clean or (p-clean[-1]).length>1e-7:clean.append(p)
                if len(clean)>2 and (clean[0]-clean[-1]).length<1e-7:clean.pop()
                emit(clean,[c]*len(clean),mi,outward)
                if abs(z0-row*exposure)<2e-6:
                    butt=[point(left,z0,False),point(right,z0,False),point(right,z0),point(left,z0)]
                    if (butt[1]-butt[0]).length>1e-6:emit(butt,[c]*4,mi,Vector((0,0,-1)))
    mesh=bpy.data.meshes.new(me.name+'_Lapped');mesh.from_pydata(vs,[],fs);mesh.update()
    for m in me.materials:mesh.materials.append(m)
    color=mesh.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
    for dst,c in zip(color.data,cs):dst.color=c
    for p,mi in zip(mesh.polygons,mis):p.material_index=mi
    mesh.uv_layers.new(name='UVMap');ob.data=mesh
    ob['course_exposure_m']=exposure;ob['butt_projection_m']=projection
