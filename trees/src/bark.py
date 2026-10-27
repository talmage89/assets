"""Original dark maple bark: broad shallow ridges and short lifted plates."""
import math
import bpy
from kit.materials import Nodes
from settings import BARK
from bark_source import generate


def material(wear=.5,out=None):
    n=Nodes('Maple bark / dark gray-brown flaky ridges')
    p=n.node('ShaderNodeTexCoord').outputs['Object'];x,y,z=n.split(p)
    old=n.ramp(z,*BARK['old_transition'])
    age=n.node('ShaderNodeAttribute',attribute_name='BarkMaturity')
    old=n.mul(old,age.outputs['Fac'])
    angle=n.math('ARCTAN2',y,x)
    uv=n.combine(n.add(n.mul(angle,1/math.tau),.5),n.mul(z,1/BARK['field_height']),0)
    texture=n.node('ShaderNodeTexImage');texture.image=bpy.data.images.load(str(generate(out).resolve()))
    texture.image.colorspace_settings.name='Non-Color';texture.extension='REPEAT'
    n.feed(texture.inputs['Vector'],uv)
    fields=n.node('ShaderNodeSeparateColor');n.feed(fields.inputs[0],texture.outputs['Color'])
    face=n.ramp(fields.outputs['Green'],.12,.80)
    base=n.mix(face,BARK['fissure'],BARK['flake'],color=True)
    grain=n.noise(p,BARK['grain_frequency'],3)
    young=n.mix(n.mul(grain,.15),BARK['young'],BARK['mature'],color=True)
    base=n.mix(old,young,base,color=True)
    # Rain retained beneath the crotch and in low sheltered cracks.
    track=n.noise(n.combine(n.mul(x,32),n.mul(y,32),n.mul(z,.55)),1,2)
    damp=n.mul(n.maximum(n.mul(n.ramp(track,.48,.70),n.ramp(z,3.2,.3)),
                         n.mul(n.ramp(z,.25,.025),n.ramp(track,.35,.65))),wear)
    base=n.mix(n.mul(damp,.6),base,(.0007,.00055,.0003),color=True)
    north=n.ramp(y,-.04,.15)
    lichen=n.mul(north,n.ramp(z,.15,.65),n.ramp(z,3.,1.1),n.ramp(n.noise(p,84),.71,.81),.14)
    base=n.mix(lichen,base,(.035,.038,.024),color=True)
    relief=n.add(n.mul(fields.outputs['Red'],.005),-.001)
    height=n.add(n.mul(old,relief),n.mul(grain,.00012))
    n.channel('micro_ao',n.mix(old,1,fields.outputs['Blue']))
    n.channel('rain',damp);n.channel('lichen',lichen)
    mat=n.finish(base,n.add(.84,n.mul(grain,.11),n.mul(damp,.03)),0,height)
    mat.node_tree.nodes['SURFACE'].inputs['Specular IOR Level'].default_value=.12
    mat.node_tree.nodes['SURFACE'].inputs['IOR'].default_value=1.45
    return mat
