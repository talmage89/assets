"""Render-only landscaping around the native loading loop, never exported."""
import math,random
import bpy
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
from kit import model as G

def landscaping(campus):
    bpy.context.view_layer.update();vertices=[];faces=[];labels=[]
    for ob in campus:
        if ob.type!='MESH':continue
        ob.data.calc_loop_triangles();offset=len(vertices)
        vertices.extend(ob.matrix_world@v.co for v in ob.data.vertices)
        for t in ob.data.loop_triangles:
            faces.append(tuple(offset+i for i in t.vertices))
            labels.append(ob.data.materials[t.material_index].name)
    tree=BVHTree.FromPolygons(vertices,faces,all_triangles=True)
    ground=bpy.data.objects['Distant school grounds']
    fallback=max((ground.matrix_world@v.co).z for v in ground.data.vertices)
    def ground_at(x,y,radius):
        heights=[]
        for dx,dy in [(0,0),(radius,0),(-radius,0),(0,radius),(0,-radius)]:
            p,_,index,_=tree.ray_cast(Vector((x+dx,y+dy,40)),Vector((0,0,-1)),45)
            if p is None:heights.append(fallback);continue
            if p.z>.10 or any(k in labels[index] for k in ['Asphalt','Concrete','Walk']):return None
            heights.append(p.z)
        return min(heights)
    obs=[];trees=[];shrubs=[]
    masters=[next(o for o in campus if o.name=='Mature_tree_'+str(i)) for i in [0,3]]
    for i,y in enumerate([18,36,60]):
        x=24;z=ground_at(x,y,.7)
        if z is None:continue
        master=masters[i%2];base=master.matrix_world.translation
        xf=Matrix.Translation((x,y,z))@Matrix.Rotation(i*.83,4,'Z')@Matrix.Translation(-base)
        for original in master.children_recursive:
            if original.type!='MESH':continue
            ob=original.copy();ob.name='Loop context tree '+str(i)+' '+original.name
            ob.parent=None;bpy.context.scene.collection.objects.link(ob)
            ob.matrix_world=xf@original.matrix_world;obs.append(ob)
        trees.append(dict(source=master.name,position_m=[x,y,z]))
    # Dense understory closes the low horizon below the mature crowns. Every
    # candidate is rejected if its actual native surface is road, walk or roof.
    mat=bpy.data.materials.new('Loop understory');mat.use_nodes=True
    nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF')
    tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value=36;nt.links.new(tc.outputs['Generated'],noise.inputs[0])
    ramp=nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color=(.010,.020,.005,1)
    ramp.color_ramp.elements[1].color=(.031,.057,.016,1)
    nt.links.new(noise.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value=.91
    bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.018
    nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
    rng=random.Random(6107)
    for i,y in enumerate(range(18,87,4)):
        x=24;z=ground_at(x,y,1.8)
        if z is None:continue
        rings=[]
        for zz,radius in [(0,1.1),(.2,1.5),(.7,1.75),(1.5,1.7),(2.3,1.4),(3.0,.8),(3.5,.05)]:
            ring=[]
            for k in range(18):
                a=math.tau*k/18;r=radius*rng.uniform(.84,1.16)
                ring.append((x+r*math.cos(a),y+r*math.sin(a),z+zz+rng.uniform(-.035,.035)))
            rings.append(ring)
        ob=G.loft('Loop understory '+str(i),rings,mat);G.smooth(ob,65);obs.append(ob)
        shrubs.append([x,y,z])
    return obs,dict(trees=trees,understory=shrubs,
        scope='Native tree data instanced read-only; original procedural distant shrubs. Five actual native ground rays per candidate reject roads/walks/roofs; ground continuation supports outside-parcel roots.')
