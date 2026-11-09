"""Mown civic turf: native Ground blade cells at real hardscape edges.

No scattered tuft objects or new image allocation. Root competition changes
the existing lawn's corner tint; centimeter crowns break its flat edge.
"""
import math,random
import bpy
from mathutils import Vector


def finish(a,sp,cuts):
    trees=sp['trees'];l,r,f,k=sp['parcel']
    for ob in a.objects:
        if ob.get('module_kind')!='SiteLawn':continue
        for v in ob.data.vertices:
            x,y=v.co[:2]
            edge=min(x-l,r-x,y-f,k-y)
            v.co.z+=max(0,min(1,edge/2))*(.012+.009*math.sin(x*.43)*math.sin(y*.37))
        attr=ob.data.color_attributes['Tint']
        for loop in ob.data.loops:
            x,y=ob.data.vertices[loop.vertex_index].co[:2]
            dry=min(.65,sum(.48*math.exp(-((x-tx)**2+(y-ty)**2)/12) for tx,ty in trees))
            col=attr.data[loop.index].color
            col[0]*=1+.36*dry;col[1]*=1-.14*dry;col[2]*=1-.28*dry
        ob.data.update()
    def grass(x,y):
        return l+.01<x<r-.01 and f+.01<y<k-.01 and not any(aa-.005<x<bb+.005 and cc-.005<y<dd+.005 for aa,bb,cc,dd in cuts)
    rng=random.Random(sp['seed']+803);verts=[];faces=[];charts=[];colors=[]
    # Only boundaries between grass and slabs receive a continuous short fringe.
    # Internal partition edges and edges against buildings receive no fake tuft.
    for aa,bb,cc,dd in cuts[1:]:
        for start,end in [((aa,cc),(bb,cc)),((bb,cc),(bb,dd)),((bb,dd),(aa,dd)),((aa,dd),(aa,cc))]:
            p,q=Vector((*start,0)),Vector((*end,0));length=(q-p).length
            if length<.1:continue
            tangent=(q-p).normalized();normal=Vector((-tangent.y,tangent.x,0))
            for j in range(max(1,round(length/.18))):
                t=(j+rng.uniform(.15,.85))/max(1,round(length/.18));center=p.lerp(q,t)
                left,right=grass(*(center+normal*.035)[:2]),grass(*(center-normal*.035)[:2])
                if left==right:continue
                inward=normal if left else -normal
                center+=inward*.018;center.z=-.014
                width=rng.uniform(.15,.25);height=rng.uniform(.032,.057)
                for axis in (tangent,(tangent*.35+inward*.94).normalized()):
                    top=center+inward*rng.uniform(.005,.016)+Vector((0,0,height))
                    i=len(verts);verts.extend([center-axis*width/2,center+axis*width/2,top+axis*width/2,top-axis*width/2])
                    faces.extend([(i,i+1,i+2),(i,i+2,i+3)])
                    col,row=rng.randrange(4),rng.randrange(2);ua=.25+col*.0625+.00075;ub=ua+.061
                    va=row*.125+.00075;vb=va+.1235;uv=[(ua,va),(ub,va),(ub,vb),(ua,vb)]
                    charts.extend([uv[j] for j in (0,1,2,0,2,3)]);colors.extend([(.68,.73,.52,1)]*4)
    me=bpy.data.meshes.new('NativeGroundMownEdges');me.from_pydata(verts,[],faces);me.update()
    ob=bpy.data.objects.new(a.root.name+'__MownGrassEdges',me);bpy.context.collection.objects.link(ob);ob.parent=a.root
    from wear import decal
    if not bpy.data.materials.get('CivicGround_Decals'):
        stub=decal(a,'MaterialInitialization',(0,0,-5),(.01,.01),'paint');bpy.data.objects.remove(stub,do_unlink=True)
    me.materials.append(bpy.data.materials['CivicGround_Decals'])
    uv=me.uv_layers.new(name='UVMap')
    for li,value in enumerate(charts):uv.data[li].uv=value
    tint=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT');me.color_attributes.active_color=tint
    for i,c in enumerate(colors):tint.data[i].color=c
    ob['module_kind']='NativeGroundMownEdges';ob['cause']='mower leaves short blades at slab margins'
    a.objects.append(ob)
