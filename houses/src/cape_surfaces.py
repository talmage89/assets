"""Cause-driven Cape source materials, with explicit bake channels."""
from kit.materials import Nodes
from cape_shingle_fields import shingle_tile


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
    broad=n.noise(rest,3.5,3);fine=n.channel('fine_noise',n.noise(rest,210,2))
    breakup=n.ramp(broad,.28,.66)
    low=n.ramp(n.math('SUBTRACT',z,bottom),.33,.015)
    under=n.ramp(n.math('SUBTRACT',eave,z),.55,.06)
    height=0;peel=0
    skin=meta['spec']['siding']
    if role=='Concrete':base=n.vec('MULTIPLY',base,(.835,1.,1.185))
    # Walls carry metric U/Z charts; trim keeps its shared eight-strip chart.
    if role=='Siding':
        u,v,_=n.split(n.node('ShaderNodeTexCoord').outputs['UV'])
        if skin=='wood':
            u=n.mul(u,2.4384);v=n.mul(v,2.4384)
            row=n.math('FLOOR',n.math('DIVIDE',v,.1016));course=n.math('FRACT',n.math('DIVIDE',v,.1016))
            phase=n.noise(n.combine(row,0,0),1,0)
            seam=n.math('FRACT',n.add(n.math('DIVIDE',u,2.44),phase))
            joint=n.ramp(seam,.0018,.0005);butt=n.ramp(course,.065,.005)
            base=n.mix(n.mul(joint,.25),base,(.12,.115,.095),color=True)
            height=n.add(n.mul(joint,-.001),n.mul(fine,.000035))
            rough=n.add(.61,n.mul(fine,.14))
        elif skin=='cedar':
            field=next(node for node in n.nt.nodes if node.type=='TEX_IMAGE' and node.image and 'BaseColor' in node.image.name).outputs['Color']
            if meta['spec'].get('cedar_finish','stained')=='painted':
                seam=n.ramp(field,.12,.025);field=n.add(.98,n.mul(seam,-.42));rough=.78
                base=n.vec('MULTIPLY',n.node('ShaderNodeVertexColor',layer_name='Tint').outputs['Color'],field)
            else:
                field=n.vec('MULTIPLY',field,(2.2,2.2,2.2))
                base=n.vec('MULTIPLY',n.node('ShaderNodeVertexColor',layer_name='Tint').outputs['Color'],field)
                # High/sunny wall bleaches silver; sheltered courses stay brown.
                high=n.ramp(n.math('SUBTRACT',z,bottom),.4,2.3)
                exposed=n.mul(n.add(.40,n.mul(sun,.59)),high,n.ramp(n.math('SUBTRACT',eave,z),.18,.75))
                gray=n.vec('MULTIPLY',base,(.90,1.12,1.55))
                base=n.mix(exposed,base,gray,color=True);rough=.88
        elif skin=='cement':rough=.91
        elif skin=='aluminum':
            # Course exposure and sun dull the paint evenly. Rain washes narrow
            # vertical paths beneath sill corners and gutter overflow sites.
            washed=0
            for op in meta['openings']:
                if op['kind']!='window':continue
                b=next(b for b in meta['blocks'] if b['name']==op['block'])
                fb=op['face'] in ('front','back')
                wall=b['y0'] if op['face']=='front' else b['y1'] if op['face']=='back' else b['x0'] if op['face']=='left' else b['x1']
                on_wall=n.ramp(n.math('ABSOLUTE',n.add(y if fb else x,-wall)),.10,.025)
                below=n.mul(n.ramp(z,op['z']+.01,op['z']-.04),n.ramp(z,op['z']-1.9,op['z']-.30))
                for side in (-1,1):
                    cx=b['x0' if fb else 'y0']+op['u']+side*op['w']/2
                    washed=n.maximum(washed,n.mul(on_wall,below,n.ramp(n.math('ABSOLUTE',n.add(x if fb else y,-cx)),.085,.014)))
            washed=n.maximum(washed,attr(n,'CapeWater','Fac'))
            oxide=n.mul(.27,n.add(.38,n.mul(sun,.62)),n.add(1,n.mul(washed,-.88)))
            base=n.mix(oxide,base,(.49,.50,.47),color=True);rough=n.add(.52,n.mul(oxide,.9))
            phase=n.math('FRACT',n.mul(v,24))
            trapped=n.maximum(n.ramp(phase,.20,.01),n.ramp(nz,-.5,-.95))
            dirt=n.mul(trapped,.50,n.add(1,n.mul(washed,-.8)))
            base=n.vec('MULTIPLY',base,n.combine(n.add(1,n.mul(dirt,-.60)),n.add(1,n.mul(dirt,-.64)),n.add(1,n.mul(dirt,-.67))))
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
            wet=attr(n,'CapePeel','Fac')
            flake=n.noise(n.vec('MULTIPLY',rest,(.65,14,35)),22,2)
            low_wet=n.mul(low,n.add(.28,n.mul(site,.72)))
            peel=n.mul(wood,old,n.maximum(n.mul(low_wet,.85),wet),n.ramp(flake,.57,.67))
            # Bare gray wood, with a lighter raised surviving film edge.
            base=n.mix(peel,base,(.205,.216,.211),color=True)
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
        variation=n.channel('manufacture_variation',n.add(.62,n.mul(granule,1.15)))
        base=n.vec('MULTIPLY',base,n.combine(variation,variation,variation))
        mineral=n.ramp(n.noise(rest,550,0),.30,.70)
        mineral=n.channel('manufacture_granule',n.add(.65,n.mul(mineral,.60)))
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
