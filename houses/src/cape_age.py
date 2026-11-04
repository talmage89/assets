"""Sparse original silhouette wear: lifted paint edges and curled asphalt tabs."""
import random
import bpy
from mathutils import Vector
from cape_plan import generate,roof_parts


def add(meta):
    plan=generate(meta['seed'],meta['spec']);m=plan['blocks'][0];rng=random.Random(8100+meta['seed'])
    owner=next(o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set'))
    stock=list(owner.data.materials)
    def mesh(name,vertices,faces,role,color,component):
        if not faces:return
        me=bpy.data.meshes.new(name);me.from_pydata(vertices,[],faces);me.update()
        ob=bpy.data.objects.new(name,me);bpy.context.scene.collection.objects.link(ob)
        ob.parent=bpy.data.objects.get('House');ob['asset_set']=owner['asset_set'];ob['component']=component;ob['block']='Main'
        ob['allow_boundary']=True
        for mat in stock:me.materials.append(mat)
        index=next(i for i,mat in enumerate(stock) if mat.name=='House_'+role)
        for p in me.polygons:p.material_index=index;p.use_smooth=name=='Aged_LiftedPaint'
        a=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
        for v in a.data:v.color=(*color,1)
        me.uv_layers.new(name='UVMap')
    # Omit isolated roof-tab overlays. The common roof retains granule loss;
    # widespread curl would need a continuous tab surface rather than boxes.
    # Thin parging/form-imprint charts sit 0.2 mm above the actual foundation.
    # They share its material; no decal texture or extra draw call is allocated.
    from plan import wall_frame
    from cape_build import foundation_top
    import math
    for block in plan['blocks']:
        if block.name.startswith('Dormer') or block.name in ('RearShed','Breezeway'):continue
        top=foundation_top(block)
        if top<.2:continue
        vs=[];fs=[]
        for face in ('front','back','left','right'):
            origin,t,n,length=wall_frame(block,face)
            def quad(u0,u1,z0,z1):
                if z1<=z0:return
                off=len(vs)
                vs.extend((origin[0]+t[0]*u+n[0]*(-.0238),origin[1]+t[1]*u+n[1]*(-.0238),z) for u,z in ((u0,z0),(u1,z0),(u1,z1),(u0,z1)))
                fs.append(tuple(range(off,off+4)))
            if meta['spec']['foundation']=='crawlspace':
                for row in range(math.ceil(top/.2032)):
                    z=row*.2032
                    if z>.01:quad(.03,length-.03,z-.0015,z+.0015)
                    for col in range(math.ceil(length/.4064)):
                        u=col*.4064+(row%2)*.2032
                        if .05<u<length-.05:quad(u-.0015,u+.0015,z+.003,min(top-.025,z+.2002))
            else:
                for i in range(1,math.ceil(length/1.2192)):
                    u=i*1.2192
                    if u<length-.04:quad(u-.0008,u+.0008,.025,top-.025)
        mesh(block.name+'_FoundationImprints',vs,fs,'Concrete',(.72,.74,.74),'foundation_marks')
    if meta['spec']['siding']=='wood':
        vs=[];fs=[];bare=[];bare_faces=[];checks=[];check_faces=[]
        for o in meta['openings']:
            if o['face']!='front' or o['kind']!='window':continue
            b=next(v for v in plan['blocks'] if v.name==o['block'])
            for j in range(9):
                x=b.x0+o['u']+rng.uniform(-o['w']/2-.04,o['w']/2+.04)
                w=rng.uniform(.018,.047);d=rng.uniform(.006,.014)
                depth=.174-d-rng.uniform(.002,.006) if j<6 else rng.uniform(.022,.045)
                def point(dx,dy,lift):
                    v=depth+dy
                    return (x+dx,b.y0-v,o['z']+.004-(v-.013)*.016/.161+lift)
                off=len(bare)
                # Ragged, grain-long losses, with broad splintered ends rather
                # than identical knife-shaped trapezoids. Eight-vertex outlines
                # are funded by curling only three of each nine paint losses.
                outline=((-1,.14),(-.55,.02),(.12,.09),(.87,.03),(1,.68),(.48,.96),(-.20,.81),(-.86,.92))
                bare.extend(point(w*xx,d*yy,.00015) for xx,yy in outline)
                bare_faces.append(tuple(range(off,off+8)))
                if j%3==0:
                    off=len(vs);film=d*.40
                    for k,(v,lift) in enumerate(((0,.0002),(.3,.0003),(.8,.0013),(.7,.0019))):
                        width=w*(.90+.10*math.sin(k*1.7+j))
                        vs.extend([point(-width,v*film,lift),point(-width*.05,v*film*.85,lift*.64),point(width*.85,v*film*.9,lift*.88)])
                    for k in range(3):
                        for col in range(2):
                            a=off+3*k+col;fs.append((a,a+3,a+4,a+1))
                off=len(checks)
                check=min(d*1.15,.173-depth)
                checks.extend([point(-w*1.12,check,.00008),point(-w*1.12,check+.00045,.00008),point(w*1.10,check+.00045,.00008),point(w*1.10,check,.00008)])
                check_faces.append((off,off+1,off+2,off+3))
        mesh('Aged_GrayWoodAtSillNoses',bare,bare_faces,'Trim',(.205,.216,.211),'paint_flakes')
        mesh('Aged_GrainChecksAroundPeeling',checks,check_faces,'Trim',(.12,.13,.125),'paint_flakes')
        mesh('Aged_LiftedPaint',vs,fs,'Trim',meta['spec']['colors']['trim'],'paint_flakes')
