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
        for mat in stock:me.materials.append(mat)
        index=next(i for i,mat in enumerate(stock) if mat.name=='House_'+role)
        for p in me.polygons:p.material_index=index
        a=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
        for v in a.data:v.color=(*color,1)
        me.uv_layers.new(name='UVMap')
    if meta['spec']['roof_age']=='tired':
        vs=[];fs=[]
        for sign in (-1,1):
            for row in range(1,10):
                distance=row*4.8768/34/(1+m.pitch*m.pitch)**.5
                y=(m.y0+distance) if sign==-1 else (m.y1-distance)
                for j in range(18):
                    if rng.random()>.13:continue
                    x=m.x0+.35+j*(m.width-.7)/18+rng.uniform(-.05,.05);width=rng.uniform(.13,.22)
                    # Entire tab must belong to the exposed main roof.
                    points=[(xx,yy) for xx in (x-width/2,x+width/2) for yy in (y,y-sign*.14)]
                    if any(max(b.height(xx,yy) for b in roof_parts(plan) if b.covers(xx,yy))>m.height(xx,yy)+.001 for xx,yy in points):continue
                    off=len(vs)
                    for k in range(4):
                        t=k/3;yy=y-sign*t*.14;lift=.002+.014*(1-t)**2
                        for xx in (x-width/2,x+width/2):vs.append((xx,yy,m.height(xx,yy)+lift))
                    for k in range(3):
                        face=(off+2*k,off+2*k+1,off+2*k+3,off+2*k+2)
                        fs.append(face if sign==-1 else face[::-1])
        mesh('Aged_CurledTabs',vs,fs,'Shingles',(.07,.075,.065),'curled_tabs')
    if meta['spec']['siding']=='wood':
        vs=[];fs=[]
        for o in meta['openings']:
            if o['face']!='front' or o['kind']!='window':continue
            b=next(v for v in plan['blocks'] if v.name==o['block'])
            for j in range(10):
                x=b.x0+o['u']+rng.uniform(-o['w']/2,o['w']/2);y=b.y0-.12;z=o['z']+.003
                w=rng.uniform(.007,.023);d=rng.uniform(.007,.026);off=len(vs)
                vs.extend([(x-w,y,z),(x+w*.5,y-.002,z+.0004),(x+w,y-d,z+.0016),(x-w*.7,y-d*.8,z+.0008)])
                fs.append((off,off+1,off+2,off+3))
        mesh('Aged_LiftedPaint',vs,fs,'Trim',meta['spec']['colors']['trim'],'paint_flakes')
