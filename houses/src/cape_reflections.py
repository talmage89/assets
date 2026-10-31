"""Original modeled reflection luminance proxies, never exported with assets."""
import random
import bpy
from mathutils import Vector
from ranch_render import reflection_scenery
from render import simple
from kit.materials import Nodes
DEFAULT_PHASE=(-.06,0.,0.)


def scenery(meta,phase=None):
    reflection_scenery(meta);m=meta['blocks'][0];r=random.Random(9281)
    n=Nodes('Cape reflection leaves');tc=n.node('ShaderNodeTexCoord')
    position=n.vec('ADD',tc.outputs['Object'],phase if phase is not None else DEFAULT_PHASE)
    tone=n.ramp(n.noise(position,4,2),.35,.65)
    level=n.mix(tone,.038,.30)
    level=n.math('MAXIMUM',n.math('DIVIDE',n.math('POWER',level,4),.027),.070)
    field=n.combine(n.mul(level,1.04),level,n.mul(level,1.03))
    leaf=n.finish(field,.87,0)
    # A modeled lighting proxy, analogous to a studio reflection card. Its
    # prescribed radiance represents a daylit neighboring crown; it avoids
    # baking a particular reflection into the window material.
    emission=n.node('ShaderNodeEmission');n.feed(emission.inputs['Color'],field);emission.inputs['Strength'].default_value=1.84
    transparent=n.node('ShaderNodeBsdfTransparent');path=n.node('ShaderNodeLightPath');mix=n.node('ShaderNodeMixShader')
    n.feed(mix.inputs[0],path.outputs['Is Glossy Ray']);n.feed(mix.inputs[1],transparent.outputs[0]);n.feed(mix.inputs[2],emission.outputs[0])
    n.feed(n.nt.nodes['OUT'].inputs['Surface'],mix.outputs[0])
    for f in (.25,.75):
        center=Vector((m['x0']+(m['x1']-m['x0'])*f,m['y0']-8.5,2.0))
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3,radius=1,location=center)
        ob=bpy.context.object;ob.name='Cape presentation low leafy crown';ob.data.materials.append(leaf)
        for v in ob.data.vertices:
            v.co*=r.uniform(.89,1.10);v.co.x*=1.7;v.co.y*=1.2;v.co.z*=1.55
        # Ray gating is in the shader, including paths behind a storm pane.
        ob.visible_camera=False;ob.visible_shadow=False;ob.visible_diffuse=False;ob.visible_transmission=True
        vertices=[];faces=[]
        for j in range(1700):
            p=Vector(tuple(r.uniform(-1,1) for _ in range(3))).normalized();c=center+Vector((p.x*1.74,p.y*1.24,p.z*1.58))
            a=Vector(tuple(r.uniform(-1,1) for _ in range(3))).normalized()*r.uniform(.045,.09);b=a.cross(p).normalized()*a.length*.55
            i=len(vertices);vertices.extend((c-a,c+b,c+a,c-b,c+p*.008));faces.extend((i+k,i+(k+1)%4,i+4) for k in range(4))
        me=bpy.data.meshes.new('Original low leaf facets');me.from_pydata(vertices,[],faces);me.update();me.materials.append(leaf)
        ob=bpy.data.objects.new('Cape presentation low leaf facets',me);bpy.context.collection.objects.link(ob)
        ob.visible_camera=False;ob.visible_shadow=False;ob.visible_diffuse=False;ob.visible_transmission=True
