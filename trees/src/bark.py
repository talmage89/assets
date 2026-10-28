"""Original dark maple bark: broad shallow ridges and short lifted plates."""
import math
import bpy
from kit.materials import Nodes
from species import MAPLE
from bark_source import generate


def material(wear=.5,out=None,species=MAPLE):
    n=Nodes(species.BARK_NAME)
    p=n.node('ShaderNodeTexCoord').outputs['Object'];x,y,z=n.split(p)
    old=n.ramp(z,*species.BARK['old_transition'])
    age=n.node('ShaderNodeAttribute',attribute_name='BarkMaturity')
    old=n.mul(old,age.outputs['Fac'])
    angle=n.math('ARCTAN2',y,x)
    uv=n.combine(n.add(n.mul(angle,1/math.tau),.5),n.mul(z,1/species.BARK['field_height']),0)
    texture=n.node('ShaderNodeTexImage');texture.image=bpy.data.images.load(str(generate(out,species=species).resolve()))
    texture.image.colorspace_settings.name='Non-Color';texture.extension='REPEAT'
    n.feed(texture.inputs['Vector'],uv)
    fields=n.node('ShaderNodeSeparateColor');n.feed(fields.inputs[0],texture.outputs['Color'])
    face=n.ramp(fields.outputs['Green'],.12,.80)
    if species.ARCHITECTURE=='excurrent':face=n.math('POWER',face,species.BARK['ridge_contrast'])
    base=n.mix(face,species.BARK['fissure'],species.BARK['flake'],color=True)
    grain=n.noise(p,species.BARK['grain_frequency'],3)
    young=n.mix(n.mul(grain,.15),species.BARK['young'],species.BARK['mature'],color=True)
    base=n.mix(old,young,base,color=True)
    # Rain retained beneath the crotch and in low sheltered cracks.
    track=n.noise(n.combine(n.mul(x,32),n.mul(y,32),n.mul(z,.55)),1,2)
    damp=n.mul(n.maximum(n.mul(n.ramp(track,.48,.70),n.ramp(z,3.2,.3)),
                         n.mul(n.ramp(z,.25,.025),n.ramp(track,.35,.65))),wear)
    base=n.mix(n.mul(damp,.6),base,(.0007,.00055,.0003),color=True)
    north=n.ramp(y,-.04,.15)
    lichen=n.mul(north,n.ramp(z,.15,.65),n.ramp(z,3.,1.1),n.ramp(n.noise(p,84),.71,.81),.14)
    if species.ARCHITECTURE=='excurrent':
        # Small pale colonies on sheltered ridge tops, sparse enough to leave
        # the warm bark visible; separate from rain-darkened fissures.
        lichen=n.mul(n.add(.60,n.mul(north,.40)),n.ramp(z,.18,.6),n.ramp(z,3.8,1.8),n.ramp(n.noise(p,72),.68,.75),face,.85)
    base=n.mix(lichen,base,(.035,.038,.024),color=True)
    if species.ARCHITECTURE=='excurrent':base=n.mix(lichen,base,(.50,.51,.36),color=True)
    if 'dead' in species.BARK:
        dead=n.node('ShaderNodeAttribute',attribute_name='DeadWood')
        base=n.mix(dead.outputs['Fac'],base,species.BARK['dead'],color=True)
    relief=n.add(n.mul(fields.outputs['Red'],species.BARK.get('field_range_m',.005)),species.BARK.get('field_floor_m',-.001))
    height=n.add(n.mul(old,relief),n.mul(grain,.00012))
    n.channel('micro_ao',n.mix(old,1,fields.outputs['Blue']))
    n.channel('rain',damp);n.channel('lichen',lichen)
    mat=n.finish(base,n.add(species.BARK.get('roughness',.84),n.mul(grain,.11),n.mul(damp,.03)),0,height)
    if species.ARCHITECTURE=='excurrent':
        next(node for node in mat.node_tree.nodes if node.type=='BUMP').inputs['Strength'].default_value=species.BARK['bump_strength']
    mat.node_tree.nodes['SURFACE'].inputs['Specular IOR Level'].default_value=species.BARK.get('specular',.12)
    mat.node_tree.nodes['SURFACE'].inputs['IOR'].default_value=1.45
    return mat
