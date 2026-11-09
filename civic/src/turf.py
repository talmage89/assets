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
            # Same July albedo/normal repeat as the garden and trailer park.
            # Moisture, mower turns, walk margins and root competition act at
            # their real locations, rather than a uniform green overlay.
            margin=min([min(abs(x-aa),abs(x-bb)) if cc<y<dd else 99 for aa,bb,cc,dd in cuts]+
                [min(abs(y-cc),abs(y-dd)) if aa<x<bb else 99 for aa,bb,cc,dd in cuts])
            dry=min(.85,dry+.22*math.exp(-(margin/.38)**2)*(.55+.45*math.sin(x*.7+y*.9)**2))
            moisture=.82+.13*math.sin(x*.21+y*.13+sp['seed'])+.05*math.sin(y*.51-x*.32)
            shade=min(.56,sum(.38*math.exp(-((x-tx-1.7)**2+(y-ty-1.2)**2)/22) for tx,ty in trees))
            grain=.94+.04*math.sin(x*2.3+y*.77)+.02*math.sin(y*3.1-x*.9)
            rgb=(.53*(1+dry*.44),.61*(1-dry*.48),.50*(1-dry*.42))
            attr.data[loop.index].color=(*(c*moisture*grain*(1-shade) for c in rgb),1)
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
                    charts.extend([uv[j] for j in (0,1,2,0,2,3)]);colors.extend([(.94,.99,.71,1)]*4)
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
    # A habitual corner cut from the sidewalk to the entry route. Its narrow
    # irregular soil core feathers into drought-stressed grass, rather than a
    # drawn rectangular dirt strip. The accepted path curves stay unchanged.
    from aging import patch
    start,end=((7.7,-28.6),(1.1,-16.3)) if sp['kind']=='downtown' else ((8.7,-28.9),(5.0,-12.3))
    delta=Vector((end[0]-start[0],end[1]-start[1],0));direction=delta.normalized();across=Vector((-direction.y,direction.x,0))
    width=.72;origin=Vector((*start,.021))-across*width/2
    trail=patch(a,'PedestrianCornerCut',origin,across,direction,width,delta.length,(.16,.106,.042),
        lambda s,t:.50*math.sin(t*math.pi)**.35*max(0,1-abs((s-.5)/(.27+.055*math.sin(t*27))))**1.2,nx=6,ny=55)
    for vertex in trail.data.vertices:
        p=vertex.co;t=((p-origin).dot(direction))/delta.length
        vertex.co+=across*(.065*math.sin(t*17)+.025*math.sin(t*49))
        if not grass(p.x,p.y):
            for loop in trail.data.loops:
                if loop.vertex_index==vertex.index:trail.data.color_attributes['Tint'].data[loop.index].color[3]=0


def beds(a,sp):
    """Mulch retained beneath the foundation boxwoods; sparse real wood relief."""
    rng=random.Random(sp['seed']+2501)
    areas=[(-20.7,-11.7,-10.9,-9.02),(.2,6.7,-10.9,-9.02)] if sp['kind']=='downtown' else [(13.2,14.85,-4.8,3.4)]
    for index,(l,r,f,k) in enumerate(areas):
        m=a.mesh('FoundationMulch_'+str(index),kind='FoundationMulch',trim_strip=0,authored_winding=True)
        m.geom([(l,f,.004),(r,f,.004),(r,k,.004),(l,k,.004)],[(0,1,2,3)],'Trim',(.061,.033,.014))
        for j in range(round((r-l)*(k-f)*8)):
            x,y=rng.uniform(l,r),rng.uniform(f,k);theta=rng.uniform(0,math.tau)
            length=rng.uniform(.035,.095);width=rng.uniform(.009,.024);cs,sn=math.cos(theta),math.sin(theta)
            pts=[(x+cs*u-sn*v,y+sn*u+cs*v,z) for u,v,z in [(-length/2,0,.005),(length/2,0,.005),(0,width,.012)]]
            m.geom(pts,[(0,1,2)],'Trim',(.085*rng.uniform(.7,1.2),.043,.019))
        m.finish()
    return areas
