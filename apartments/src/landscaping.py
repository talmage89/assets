"""Seeded period foundation beds using the shrubs' original exported species.

Boxwood (native growth seed 419) and Hydrangea (815) keep their shared baked
atlas. Placement, size, grouping and maintenance are seeded per building;
these presentation instances are never added to the architectural package.
"""
import math
import random
from mathutils import Vector
from kit import model as G
from plans import transform


def mulch_material():
    import bpy
    ma=bpy.data.materials.get('Presentation aged bark mulch')
    if ma:return ma
    ma=bpy.data.materials.new('Presentation aged bark mulch');ma.use_nodes=True
    n,l=ma.node_tree.nodes,ma.node_tree.links;bs=n.get('Principled BSDF')
    bs.inputs['Roughness'].default_value=.99
    tc=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=64
    l.new(tc.outputs['Object'],noise.inputs['Vector'])
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.016,.010,.006,1);ramp.color_ramp.elements[1].color=(.085,.047,.021,1)
    l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],bs.inputs['Base Color'])
    bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.025;bump.inputs['Strength'].default_value=.6
    l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],bs.inputs['Normal']);return ma


def bed(lib,root_path,tree_path,name,x0,x1,y,side,seed,place=lambda q:q,corner=False):
    """A broken mixed border, kept clear of the central door/walk reservation."""
    rng=random.Random(seed);length=x1-x0
    if length<.55:return
    edge=[]
    for i in range(max(3,math.ceil(length/.8))+1):
        t=i/max(3,math.ceil(length/.8));x=x0+length*t
        edge.append(place((x,y+side*(.89+.09*math.sin(x*1.4+seed)),.018)))
    inner=[place((x,y-side*.68,.018)) for x in (x1,x0)]
    vertices=edge+inner
    # Top fan, independent of surface winding in a rotated/rear bed.
    center=sum((Vector(q) for q in vertices),Vector())/len(vertices)
    ob=G.mesh(name+' mulch',[tuple(center),*vertices],[(0,j+1,(j+1)%len(vertices)+1) for j in range(len(vertices))],mulch_material())
    for f in ob.data.polygons:
        if f.normal.z<0:f.flip()
    # A low bent steel edge is nearly buried; its top follows the bed's arc.
    import bpy
    steel=bpy.data.materials.get('Presentation bed edging') or bpy.data.materials.new('Presentation bed edging')
    steel.diffuse_color=(.048,.044,.031,1);steel.use_nodes=True
    bs=steel.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=steel.diffuse_color;bs.inputs['Roughness'].default_value=.88
    for j,(a,b) in enumerate(zip(edge,edge[1:])):
        G.mesh(name+' edge '+str(j),[(a[0],a[1],-.005),(b[0],b[1],-.005),(b[0],b[1],.06),(a[0],a[1],.06)],[(0,1,2,3)],steel)
    x=x0+.5;index=0
    while x<x1-.20:
        # Drifts of like plants rather than alternating colors at one spacing.
        species='Hydrangea' if index in ((0,1) if seed%2 else (3,4)) else 'Boxwood'
        spread=rng.uniform(.80,1.19) if species=='Hydrangea' else rng.uniform(.67,1.47)
        if (index+seed)%7==0:spread*=1.19
        missing=(index+seed)%11==3
        if not missing:
            q=place((x+rng.uniform(-.14,.14),y+rng.uniform(-.27,.22),.02))
            shape=(spread*rng.uniform(.94,1.14),spread*rng.uniform(.86,1.1),spread*rng.uniform(.78,1.19))
            rt=lib.place(root_path,name+' '+species,q,rng.randrange(360),select=species,scale=shape)
            rt['native_growth_seed']=815 if species=='Hydrangea' else 419;rt['placement_seed']=seed
        x+=rng.uniform(1.12,1.65) if species=='Boxwood' else rng.uniform(1.45,1.85);index+=1
    if corner:
        lib.place(tree_path,name+' young corner maple',place((x0-.25,y+side*.25,0)),seed%360,scale=(.32,.32,.36))


def foundations(lib,p,root,stem):
    shrubs=root/'shrubs/export/Shrubs.glb';tree=root/'trees/export/RedMaple.glb'
    if stem.startswith(('Complex','Building')):
        b=p.get('building',p)
        buildings=p.get('buildings',[dict(origin=(0,0,0),yaw=0)])
        for bi,bb in enumerate(buildings):
            for mi,module in enumerate(b['modules']):
                def place(q):return transform(transform(q,module['origin'],module['yaw']),bb['origin'],bb['yaw'])
                for sy in (-1,1):
                    # Front flight mouths and the common entry stay clear.
                    margin=3.8 if b['access']=='breezeway' and sy<0 else .4
                    for half,(l,r) in enumerate(((-b['width']/2+margin,-2.65),(2.65,b['width']/2-margin))):
                        bed(lib,shrubs,tree,f'Bed {bi} {mi} {sy} {half}',l,r,sy*(b['depth']/2+1.85),sy,p['seed']*19+bi*41+mi*79+half*7+sy,place,corner=sy<0 and half==0 and mi==0)
    else:
        for u in p['units']:
            w=p['width'];y=-p['depth']/2+u['y']-1.75;x=u['x']
            spans=[(x-w*.49,x-w*.33),(x+w*.43,x+w*.51)] if p['garage'] else [(x-w*.49,x-w*.29-.85),(x-w*.29+.90,x+w*.48)]
            for i,(l,r) in enumerate(spans):
                bed(lib,shrubs,tree,f'Row bed {u["index"]} {i}',l,r,y,-1,p['seed']*23+u['index']*13+i,corner=u['index']==0 and i==0)
