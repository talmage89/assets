"""Original manufacture and causal age for the Cape source checkpoint.

Six roles only. Existing family images are read-only. These source nodes expose
bake channels; translating their fine wear to the shared delivery fields is a
later gate. No photographic pixels are read here.
"""
import math
import random
import json
import numpy as np
from kit.materials import Nodes
from kit.image_io import write_png,linear_to_srgb


def shingle_tile(folder):
    folder.mkdir(parents=True,exist_ok=True);size=512
    yy,xx=np.mgrid[:256,:512];x=xx/512*1.2192
    colors=[];heights=[];units=[]
    for kind in ('cedar','cement'):
        exposure=.1524 if kind=='cedar' else .3048
        z=yy/256*(.762 if kind=='cedar' else .6096)
        row=np.floor(z/exposure).astype(int);height=np.zeros_like(x);color=np.ones_like(x)
        for r in range(5 if kind=='cedar' else 2):
            rng=random.Random(417+r*97)
            if kind=='cedar':
                count=rng.choice((7,8,9));remaining=1.2192;widths=[]
                for j in range(count):
                    left=count-j-1;lo=max(.0762,remaining-.254*left);hi=min(.254,remaining-.0762*left)
                    width=rng.uniform(lo,hi);widths.append(width);remaining-=width
                shift=rng.uniform(0,1.2192);edges=np.r_[0,np.cumsum(widths)]-shift
            else:widths=[.6096,.6096];edges=np.array([0,.6096,1.2192])-.3048*(r%2)
            for j,(a,b) in enumerate(zip(edges,edges[1:])):
                butt=rng.uniform(-.003,.003) if kind=='cedar' else 0
                v=np.mod(z+butt,exposure)/exposure;key=np.minimum(x-a,b-x)
                tone=rng.uniform(.90,1.07) if kind=='cedar' else rng.uniform(.91,1.01)
                units.append(dict(kind=kind,row=r,width_m=float(b-a),exposure_m=exposure,butt_offset_m=butt))
                for period in (-1.2192,0,1.2192):
                    aa,bb=a+period,b+period;select=(row==r)&(x>=aa)&(x<bb);key=np.minimum(x-aa,bb-x)
                    grain=np.sin(x*2791+np.sin(z*38)*.7)+.5*np.sin(x*5731+z*27)
                    relief=(.006 if kind=='cedar' else .004)*(1-v)-np.exp(-(key/.0018)**2)*.0025+grain*(.00023 if kind=='cedar' else .00013)
                    # The thin upper end is shaded by the next course's butt.
                    # Contrast belongs within every shingle, not in alternating
                    # nearly black and pale units across the whole elevation.
                    shadow_span=.30+.035*np.sin(x*37+np.sin(z*23)) if kind=='cedar' else .045
                    shade=1-(.92 if kind=='cedar' else .34)*np.exp(-(1-v)/shadow_span)-.30*np.exp(-(key/.0018)**2)
                    color[select]=(shade*tone*(1+grain*.018))[select];height[select]=relief[select]
        colors.append(np.stack([color]*3,2));heights.append(height)
    # Image rows run down; UV V runs up. Cedar is the lower half of the atlas.
    rgb=np.concatenate([np.flipud(a) for a in colors[::-1]])
    # Each half is a metric chart, with independent vertical derivative scale.
    normal=[]
    for hi,span in zip(heights,(.762,.6096)):
        dx=(np.roll(hi,-1,1)-np.roll(hi,1,1))/(2*1.2192/512)
        dy=(np.roll(hi,-1,0)-np.roll(hi,1,0))/(2*span/256)
        n=np.stack((-dx,-dy,np.ones_like(hi)),2);n/=np.linalg.norm(n,axis=2,keepdims=True);normal.append(n)
    write_png(folder/'T_CapeShingle_BaseColor.png',np.clip(linear_to_srgb(rgb),0,1))
    write_png(folder/'T_CapeShingle_Normal.png',np.concatenate([np.flipud(a) for a in normal[::-1]])*.5+.5)
    orm=np.zeros((512,512,3));orm[:,:,0]=1;orm[:256,:,1]=.92;orm[256:,:,1]=.86
    write_png(folder/'T_CapeShingle_ORM.png',orm)
    (folder/'manufacture.json').write_text(json.dumps(dict(units=units),indent=2))


def attr(n,name,output='Vector'):
    return n.node('ShaderNodeAttribute',attribute_name=name).outputs[output]


def layer(mat,role,meta):
    n=Nodes.__new__(Nodes);n.mat=mat;n.nt=mat.node_tree;p=n.nt.nodes.get('Principled BSDF')
    def input_value(key):
        s=p.inputs[key];return s.links[0].from_socket if s.is_linked else s.default_value
    base=input_value('Base Color');rough=input_value('Roughness');normal=input_value('Normal');metal=input_value('Metallic')
    rest=attr(n,'CapeRest');x,y,z=n.split(rest);bottom,eave,old=n.split(attr(n,'CapeContext'))
    geom=n.node('ShaderNodeNewGeometry');nx,ny,nz=n.split(geom.outputs['True Normal'])
    north=n.ramp(ny,-.1,.6);shade=n.maximum(north,n.mul(n.ramp(nx,0,.8),.65))
    sun=n.maximum(n.ramp(ny,.25,-.8),n.mul(n.ramp(nx,.25,-.8),.6))
    broad=n.noise(rest,3.5,3);fine=n.noise(rest,210,2)
    breakup=n.ramp(broad,.28,.66)
    low=n.ramp(n.math('SUBTRACT',z,bottom),.33,.015)
    under=n.ramp(n.math('SUBTRACT',eave,z),.55,.06)
    height=0;peel=0
    skin=meta['spec']['siding']
    if role=='Veneer':
        cr,cg,cb=n.split(base);value=n.add(n.mul(cr,.3),n.mul(cg,.6),n.mul(cb,.1))
        aged=n.combine(n.mul(value,1.10),value,n.mul(value,.96))
        base=n.mix(.72,base,aged,color=True)
    # Walls carry metric U/Z charts; trim keeps its shared eight-strip chart.
    if role=='Siding':
        u,v,_=n.split(n.node('ShaderNodeTexCoord').outputs['UV'])
        if skin=='wood':
            base=n.node('ShaderNodeVertexColor',layer_name='Tint').outputs['Color'];normal=None
            row=n.math('FLOOR',n.math('DIVIDE',v,.1016));course=n.math('FRACT',n.math('DIVIDE',v,.1016))
            phase=n.noise(n.combine(row,0,0),1,0)
            seam=n.math('FRACT',n.add(n.math('DIVIDE',u,2.44),phase))
            joint=n.ramp(seam,.0018,.0005);butt=n.ramp(course,.065,.005)
            shade=n.add(.34,n.mul(.66,n.ramp(course,0,.15)))
            base=n.vec('MULTIPLY',base,n.combine(shade,shade,shade))
            base=n.mix(n.mul(joint,.25),base,(.12,.115,.095),color=True)
            height=n.add(n.mul(course,.007),n.mul(joint,-.001),n.mul(fine,.000035))
            rough=n.add(.61,n.mul(fine,.14))
        elif skin=='cedar':
            field=next(node for node in n.nt.nodes if node.type=='TEX_IMAGE' and node.image and 'BaseColor' in node.image.name).outputs['Color']
            if meta['spec'].get('cedar_finish','stained')=='painted':
                seam=n.ramp(field,.12,.025);field=n.add(.98,n.mul(seam,-.42));rough=.78
                base=n.vec('MULTIPLY',n.node('ShaderNodeVertexColor',layer_name='Tint').outputs['Color'],field)
            else:
                field=n.vec('MAXIMUM',n.vec('ADD',n.vec('MULTIPLY',field,(1.65,1.65,1.65)),(-.32,-.32,-.32)),(.025,.025,.025))
                field=n.math('MAXIMUM',n.math('POWER',field,1.75),.065)
                field=n.math('MAXIMUM',n.math('DIVIDE',n.math('POWER',field,2),1.58),.10)
                field=n.math('MINIMUM',field,1.45)
                base=n.vec('MULTIPLY',n.node('ShaderNodeVertexColor',layer_name='Tint').outputs['Color'],field)
                # High/sunny wall bleaches silver; sheltered courses stay brown.
                high=n.ramp(n.math('SUBTRACT',z,bottom),.4,2.3)
                exposed=n.mul(n.add(.40,n.mul(sun,.59)),high,n.ramp(n.math('SUBTRACT',eave,z),.18,.75))
                gray=n.vec('MULTIPLY',base,(.90,1.12,1.55))
                base=n.mix(exposed,base,gray,color=True);rough=.88
        elif skin=='cement':rough=.91
        elif skin=='aluminum':
            oxide=n.mul(.21,n.add(.25,n.mul(sun,.55)),breakup)
            base=n.mix(oxide,base,(.49,.50,.47),color=True);rough=n.add(.52,n.mul(oxide,.9))
        else:rough=.49
    if role in ('Siding','Concrete','Trim'):
        # Rain splash is irregular, concentrated at grade and beside landing/drains.
        site=attr(n,'CapeWater','Fac');xy=n.combine(x,y,0)
        m=meta['blocks'][0];wet_points=[(meta['door_x'],m['y0'],0)]+[(d['centerline'][3][0],d['centerline'][3][1],0) for d in meta['drains']]
        for q in wet_points:site=n.maximum(site,n.ramp(n.vec('DISTANCE',xy,q),.9,.04))
        soil=n.mul(low,n.add(.22,n.mul(site,.62)),n.add(.36,n.mul(breakup,.64)))
        if role=='Concrete':soil=n.mul(n.ramp(z,.30,.015),n.add(.45,n.mul(site,.54)),n.add(.45,n.mul(breakup,.55)))
        base=n.vec('MULTIPLY',base,n.combine(n.add(1,n.mul(soil,-.48)),n.add(1,n.mul(soil,-.56)),n.add(1,n.mul(soil,-.66))))
        mildew=n.mul(shade,n.maximum(n.mul(low,.46),n.mul(under,.38)),breakup)
        base=n.vec('MULTIPLY',base,n.combine(n.add(1,n.mul(mildew,-.65)),n.add(1,n.mul(mildew,-.46)),n.add(1,n.mul(mildew,-.60))))
        if role in ('Siding','Trim'):
            wood=1 if role=='Siding' and (skin=='wood' or skin=='cedar' and meta['spec'].get('cedar_finish')=='painted') else attr(n,'CapeWood','Fac') if role=='Trim' else 0
            wet=n.ramp(n.math('ABSOLUTE',n.math('SUBTRACT',z,attr(n,'CapeWet','Fac'))),.13,.018)
            flake=n.noise(n.vec('MULTIPLY',rest,(1,1,1.7)),22,2)
            low_wet=n.mul(low,n.add(.28,n.mul(site,.72)))
            peel=n.mul(wood,old,n.maximum(n.mul(low_wet,.85),wet),n.ramp(flake,.57,.67))
            # Bare gray wood, with a lighter raised surviving film edge.
            base=n.mix(peel,base,(.245,.231,.194),color=True)
            rim=n.mul(wood,old,n.maximum(low_wet,wet),n.band(flake,.615,.024,.008))
            base=n.mix(n.mul(rim,.43),base,(.61,.59,.52),color=True)
            height=n.add(height,n.mul(peel,-.0006),n.mul(rim,.00065))
            chalk=n.mul(sun,.17,breakup,wood)
            base=n.mix(chalk,base,n.vec('ADD',n.vec('MULTIPLY',base,(.72,.72,.72)),(.15,.15,.14)),color=True)
        if role=='Trim':
            storm=attr(n,'CapeOxide','Fac');oxide=n.mul(storm,n.add(.25,n.mul(breakup,.50)))
            base=n.mix(oxide,base,(.51,.53,.50),color=True);rough=n.mix(oxide,rough,.88)
            metal=n.mix(oxide,metal,.06)
            center,half,top=n.split(attr(n,'CapeFasteners'))
            u=n.mix(n.ramp(n.math('ABSOLUTE',ny),.25,.75),y,x)
            screw=n.ramp(n.math('ABSOLUTE',n.math('SUBTRACT',n.math('ABSOLUTE',n.math('SUBTRACT',u,center)),half)),.025,.004)
            screw=n.mul(storm,screw,n.ramp(n.math('SUBTRACT',top,z),.16,.01),n.ramp(n.math('SUBTRACT',top,z),-.01,.015))
            hanger=n.ramp(n.math('FRACT',n.math('DIVIDE',u,.9144)),.025,.003)
            gutter_face=n.mix(attr(n,'CapeGutterAxis','Fac'),n.math('ABSOLUTE',nx),n.math('ABSOLUTE',ny))
            hanger=n.mul(attr(n,'CapeRust','Fac'),hanger,n.ramp(n.math('SUBTRACT',eave,z),.32,.035),n.ramp(n.math('SUBTRACT',eave,z),-.02,.015),n.ramp(gutter_face,.5,.9),n.ramp(n.math('ABSOLUTE',nz),.7,.15))
            rust=n.mul(old,n.maximum(screw,hanger),n.ramp(broad,.25,.7),.67)
            base=n.mix(rust,base,(.18,.065,.025),color=True)
    if role=='Shingles':
        uv=n.node('ShaderNodeTexCoord').outputs['UV'];ru,rv,_=n.split(uv)
        row=n.math('FLOOR',n.mul(rv,17));tab=n.math('FLOOR',n.add(n.mul(ru,24),n.mul(row,.37)))
        granule=n.noise(n.combine(tab,row,0),1,0)
        variation=n.add(.62,n.mul(granule,1.15))
        base=n.vec('MULTIPLY',base,n.combine(variation,variation,variation))
        mineral=n.ramp(n.noise(rest,550,0),.30,.70)
        mineral=n.add(.65,n.mul(mineral,.60))
        base=n.vec('MULTIPLY',base,n.combine(mineral,mineral,mineral))
        streak=n.noise(n.combine(n.add(n.mul(x,.7),meta['seed']*.173),n.mul(y,.08),n.mul(z,.025)),2,3)
        streak=n.ramp(streak,.43,.68)
        # Broad granule depletion follows water paths, exposing dark asphalt.
        depleted=n.mul(old,n.ramp(streak,.55,.9),.28)
        base=n.mix(depleted,base,(.008,.007,.005),color=True)
        algae=n.mul(old,north,n.add(.18,n.mul(streak,.69)))
        base=n.vec('MULTIPLY',base,n.combine(n.add(1,n.mul(algae,-.75)),n.add(1,n.mul(algae,-.72)),n.add(1,n.mul(algae,-.66))))
        loss=n.mul(old,n.ramp(streak,.10,.75),n.ramp(fine,.43,.60))
        base=n.mix(loss,base,(.012,.011,.009),color=True)
        cheek=0
        for d in meta['blocks']:
            if not d['name'].startswith('Dormer'):continue
            near=n.maximum(n.mul(n.ramp(n.math('ABSOLUTE',n.add(x,-d['x0'])),.13,.015),.35),n.ramp(n.math('ABSOLUTE',n.add(x,-d['x1'])),.17,.015))
            near=n.mul(near,n.ramp(y,d['y0']-.12,d['y0']+.05),n.ramp(y,d['y1']+.15,d['y1']-.05))
            cheek=n.maximum(cheek,near)
        moss=n.mul(old,n.maximum(n.mul(north,n.ramp(n.math('SUBTRACT',z,eave),.7,.1),.9),n.mul(cheek,.85)),n.ramp(broad,.46,.66))
        base=n.mix(n.mul(moss,.67),base,(.055,.076,.021),color=True)
        height=n.mul(moss,.0035);rough=.93
    if role=='Glass':
        p.inputs['Base Color'].default_value=(.96,.98,.96,1);p.inputs['Roughness'].default_value=.010
        p.inputs['IOR'].default_value=1.52;p.inputs['Transmission Weight'].default_value=1
        return
    n.feed(p.inputs['Base Color'],n.channel('base',base));n.feed(p.inputs['Roughness'],n.channel('rough',rough))
    n.feed(p.inputs['Metallic'],n.channel('metal',metal))
    n.channel('peel',peel)
    bump=n.node('ShaderNodeBump');bump.inputs['Strength'].default_value=.7;bump.inputs['Distance'].default_value=1
    n.feed(bump.inputs['Height'],n.channel('height',height))
    if hasattr(normal,'is_output'):n.feed(bump.inputs['Normal'],normal)
    n.feed(p.inputs['Normal'],bump.outputs[0])
