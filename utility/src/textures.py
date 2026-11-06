"""Original measured-scale age fields; no photographic pixels are read.

The atlas contains two treated round-pine charts, sawn fir, zinc, dielectric
hardware, ANSI-70 paint, guards and original lettering. Checks follow grain;
wetting follows grade/shade; runoff starts under a fastener or a tank seam.
The field planes are baked by Cycles at their physical dimensions, then the
kit filters the 4096 maps to 2048 in the correct channel domains.
"""
import argparse,json,math,sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from atlas import RECTS,PHYSICAL,GUARD
from kit.image_io import write_png,linear_to_srgb


def smooth(x,a,b):
    t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)


def mix(color,target,mask):return color*(1-mask[...,None])+np.asarray(target)*mask[...,None]


def coherent(rng,w,h,cols,rows):
    """Own anisotropic fibre field; continuous across many texels."""
    from PIL import Image
    data=rng.uniform(-1,1,(rows,cols)).astype(np.float32)
    return np.asarray(Image.fromarray(data).resize((w,h),Image.Resampling.BICUBIC)).copy()


def field(role,w,h,wear=1):
    rng=np.random.default_rng(277+list(RECTS).index(role)*131)
    U,V=np.meshgrid((np.arange(w)+.5)/w,1-(np.arange(h)+.5)/h)
    W,H=PHYSICAL[role];X=U*W;Z=V*H
    grain=np.zeros((h,w),np.float32);broad=grain.copy()
    for k in range(6):
        broad+=np.sin(U*(k+1)*13+np.sin(V*8+k)*.8+rng.random()*6)*(.5**k)
    broad/=2
    fine=rng.normal(0,1,(h,w)).astype(np.float32)
    height=np.zeros((h,w),np.float32);ao=np.ones((h,w),np.float32)
    rough=np.full((h,w),.8,np.float32);metal=np.zeros((h,w),np.float32)
    if role.startswith('Pole') or role in ('Crossarm','Molding'):
        if role=='Crossarm':
            U,V=V,U
            broad=.28*np.sin(V*13+np.sin(U*8)*.4)
        # Long annual bands deflect around sparse branch-whorl knots.
        q=U.copy();knots=np.zeros_like(U)
        if role=='Crossarm':
            q+=.045*coherent(rng,w,h,16,5)+.008*coherent(rng,w,h,100,20)
        else:
            q+=.018*coherent(rng,w,h,13,25)+.003*coherent(rng,w,h,70,180)
            q+=.17*V # gentle spiral grain around the round timber
        for _ in range(7 if role.startswith('Pole') else 3):
            ku,kv=rng.uniform(.08,.92),rng.uniform(.08,.95)
            dx=(U-ku)/rng.uniform(.10,.22) if role=='Crossarm' else (U-ku)/rng.uniform(.026,.055)
            dz=(V-kv)/rng.uniform(.008,.020) if role=='Crossarm' else (V-kv)/rng.uniform(.012,.030)
            knot=np.exp(-(dx*dx+dz*dz)*.5)
            q+=(.10 if role=='Crossarm' else .030)*np.tanh(dx)*np.exp(-abs(dz)*.6-abs(dx)*.35)
            knots=np.maximum(knots,knot)
        for k in range(5):
            grain+=np.sin(q*(95+71*k)+.5*np.sin(V*(8+k*3))+k*2)*(.5**k)
        grain*=.5*(.65+.35*coherent(rng,w,h,45,20 if role=='Crossarm' else 85))
        # Silvered, neutral gray-brown fibers; fir keeps a warmer cut grain.
        base=(.170,.158,.150) if role.startswith('Pole') else (.145,.125,.092)
        color=np.broadcast_to(np.asarray(base),(h,w,3)).copy()
        color*=np.clip(1+grain[...,None]*.13+broad[...,None]*.13+fine[...,None]*.025,.5,1.5)
        # Millimetre-scale longitudinal fibres, separate from annual bands.
        fibres=coherent(rng,w,h,220,85 if role.startswith('Pole') else 35)
        color*=1+fibres[...,None]*.12
        color=mix(color,(.076,.069,.053),knots*.53)
        height=(.000055 if role=='Crossarm' else .000025 if role=='Molding' else .000075)*grain+.000016*fine+.00022*fibres-knots*.00018
        cracks=np.zeros_like(U)
        for j in range(72 if role.startswith('Pole') else 35):
            u,v=rng.uniform(.01,.99),rng.uniform(.02,.99);length=rng.uniform(.025,.15)
            # Radial drying opens the exposed side most; long tapered splits
            # follow the same slow spiral as the fibres, rather than ruled bars.
            exposure=.35+.65*(.5+.5*np.cos((u-.31)*math.tau))
            width=rng.uniform(.0013,.0058)*exposure
            if j%9==0:width*=1.6;length*=1.3
            path=u+(.17 if role.startswith('Pole') else .022)*(V-v)+.0018*np.sin(V*51+rng.random()*6)
            envelope=smooth(V,v-length,v-length*.45)*(1-smooth(V,v+length*.45,v+length))
            slit=np.exp(-((U-path)/(width*(.12+.88*envelope)+1e-6))**2)*envelope
            cracks=np.maximum(cracks,slit)
        color=mix(color,(.014,.012,.009),cracks*.94*wear)
        height-=cracks*.0055*wear;ao-=cracks*.55*wear
        if role.startswith('Pole'):
            # Uneven capillary rise, enhanced on the shaded half, never a band.
            wet_top=.64+.18*np.sin(U*19)+.085*np.sin(U*51)
            wet=(1-smooth(Z,wet_top-.15,wet_top+.18))*(.87+.10*np.sin(U*math.tau+1))
            green=(1-smooth(Z,.25,.72))*(.65+.35*np.cos((U-.23)*math.tau))**4
            color=mix(color,(.037,.045,.026),wet*.92*wear)
            color=mix(color,(.055,.080,.027),green*.79*wear)
            # String-trimmer impacts at the accessible ground-line bark.
            scuff=np.zeros_like(U)
            for _ in range(65):
                u,z=rng.uniform(0,1),rng.uniform(.13,.34)
                dx=(U-u)/rng.uniform(.009,.026)
                scratch=np.exp(-dx**6-((Z-z-.012*(U-u))/.005)**2)
                scuff=np.maximum(scuff,scratch)
            color=mix(color,(.22,.170,.095),scuff*.65*wear);height-=scuff*.0015
            # Exposed cut end leaches; long fibers remain the same material.
            top=smooth(V,.94,.995)*(.45+.3*broad)
            color=mix(color,(.24,.235,.212),top*.65*wear)
            # Fastener drips are located at actual pole equipment datums.
            for u,z,ln in ((.25,9.0,.7),(.75,9.0,.5),(.25,7.85,.65),(.25,6.60,.45),(.25,1.8,.13)):
                zz=z/H;below=np.maximum(0,zz-V)
                streak=np.exp(-((U-u)/(.008+below*.015))**2)*smooth(V,zz-ln/H,zz)* (V<zz)
                color=mix(color,(.105,.057,.025),streak*.62*wear)
            # Removed sign: lighter protected wood around dark nail punctures.
            for u,z in ((.22,.96),(.32,1.27),(.19,1.46),(.29,1.58),(.39,1.05),(.40,1.52),(.33,2.1),(.18,2.24)):
                pin=np.exp(-((U-u)/.005)**2-((Z-z)/.014)**2)
                halo=np.exp(-((U-u)/.017)**2-((Z-z)/.045)**2)
                runoff=np.exp(-((U-u)/.009)**2)*np.exp(-np.maximum(0,z-Z)/.16)*(Z<z)*(Z>z-.55)
                color=mix(color,(.125,.052,.017),np.maximum(halo*.75,runoff*.8)*wear)
                color=mix(color,(.018,.014,.010),pin*.95*wear);height-=pin*.0025
            scar=np.exp(-((U-.32)/.11)**8-((Z-1.30)/.35)**8)
            scar*=.6+.4*coherent(rng,w,h,45,90)
            color=mix(color,(.115,.095,.061),scar*.51*wear)
        else:
            # Through-bolt runoff at the arm centre and brace connections.
            for u in (.18,.5,.82):
                track=(np.exp(-((V-u)/.006)**2)*(1-U)**.45 if role=='Crossarm' else np.exp(-((U-u)/.006)**2)*(1-V)**.45)
                color=mix(color,(.085,.045,.021),track*.7*wear)
        rough=.83+.10*cracks+.025*broad
    elif role=='Tank':
        color=np.broadcast_to((.235,.247,.238),(h,w,3)).copy()
        chalk=smooth(V,.15,.95)*(.75+.15*broad)
        color=mix(color,(.29,.30,.285),chalk*.45*wear)
        color*=1+.025*coherent(rng,w,h,110,90)[...,None]
        bottom=(1-smooth(V,.015,.16+.05*np.sin(U*19)+.025*np.sin(U*37)))*(.64+.18*broad)
        color=mix(color,(.066,.064,.043),bottom*.83*wear)
        # Lift-eye weld roots and isolated failures of the rolled lid seam.
        for u,v,ln in ((.022,.87,.43),(.478,.87,.51),(.522,.87,.43),(.978,.87,.33),(.26,.985,.54),(.17,.74,.61),(.25,.74,.52),(.33,.74,.63),(.08,.985,.7),(.43,.985,.55)):
            down=np.maximum(0,v-V)
            track=np.exp(-((U-u-.0015*np.sin(V*24))/(.004+down*.016))**2)*smooth(V,v-ln,v)*(V<v)
            color=mix(color,(.079,.068,.046),track*.86*wear)
            root=np.exp(-((U-u)/.010)**2-((V-v)/.022)**2)
            color=mix(color,(.16,.063,.018),root*.85*wear)
        # Narrow failure of paint at the rolled lower seam, no pasted rust.
        seam=np.exp(-((V-.027)/.009)**2)*smooth(broad,-.1,.42)
        color=mix(color,(.13,.058,.020),seam*.85*wear)
        height=.000035*fine-seam*.0002;rough=.68+.16*chalk+.04*fine
    elif role=='Steel':
        # Irregular zinc crystals, later darkened at cut edges and bolt seats.
        cell=np.zeros_like(U)
        for _ in range(52):
            x,y=rng.random(2);cell=np.maximum(cell,np.exp(-((U-x)**2+(V-y)**2)/rng.uniform(.0003,.002)))
        shade=.25+.085*cell+.012*fine
        color=np.stack((shade*.95,shade,shade*.985),axis=-1)
        edge=np.exp(-np.minimum.reduce([U,1-U,V,1-V])*85)*smooth(broad,.15,.5)
        color=mix(color,(.115,.067,.025),edge*.72*wear)
        metal[:]=.88;metal*=1-edge*.7;rough=.58+.12*broad;height=.000025*fine
    elif role=='Guard':
        color=np.broadcast_to((.61,.398,.035),(h,w,3)).copy()
        sun=(.5+.5*np.cos(U*math.tau))*.45*wear
        color=mix(color,(.68,.53,.15),sun)
        dirt=(1-smooth(V,0,.15))*(.7+.2*broad)
        color=mix(color,(.13,.105,.043),dirt*.62*wear)
        scuffs=np.zeros_like(U)
        for _ in range(22):
            u,v=rng.uniform(.05,.95),rng.uniform(.08,.65)
            scuffs=np.maximum(scuffs,np.exp(-((U-u)/.026)**2-((V-v)/.003)**2))
        color=mix(color,(.23,.21,.13),scuffs*.6*wear);height=-scuffs*.0002;rough=.8+.04*fine
    elif role=='Endgrain':
        r=np.sqrt((U-.44)**2+(V-.53)**2)
        rings=np.sin(r*220+np.sin(U*16)*.7)
        color=np.broadcast_to((.15,.128,.091),(h,w,3)).copy()*(1+rings[...,None]*.14)
        angle=np.arctan2(V-.53,U-.44)
        split=(np.cos(angle*7+1.3)>.993)*smooth(r,.1,.35)
        color=mix(color,(.023,.020,.013),split*.8);height=.0002*rings-split*.0015
    elif role in ('Tag','Brand','Rating'):
        from PIL import Image,ImageDraw,ImageFont
        from kit.fonts import find_font
        text={'Tag':'RV0123456789','Brand':'RILL TIMBER\nSP CCA 1992\nCLASS 4','Rating':'RILL ELECTRIC\n50 kVA\n7200 / 120-240'}[role]
        bg={'Tag':(166,157,128),'Brand':(100,93,79),'Rating':(160,164,151)}[role]
        font_path=str(find_font('DejaVu Sans','Book'))
        if role=='Tag':
            im=Image.new('RGB',(w,h),bg)
            for i,char in enumerate(text):
                glyph=Image.new('RGB',(192,300),bg);d=ImageDraw.Draw(glyph);font=ImageFont.truetype(font_path,225)
                box=d.textbbox((0,0),char,font=font);d.text(((192-box[2]+box[0])/2-box[0],(300-box[3]+box[1])/2-box[1]),char,font=font,fill=(33,32,24))
                x0,x1=round(i*w/len(text)),round((i+1)*w/len(text));im.paste(glyph.resize((x1-x0,h),Image.Resampling.LANCZOS),(x0,0))
        else:
            canvas_h=768;canvas_w=round(canvas_h*W/H);im=Image.new('RGB',(canvas_w,canvas_h),bg);d=ImageDraw.Draw(im)
            size=round(canvas_h/4)
            while True:
                font=ImageFont.truetype(font_path,size);box=d.multiline_textbbox((0,0),text,font=font,align='center',spacing=18)
                if box[2]-box[0]<canvas_w*.92:break
                size-=1
            d.multiline_text(((canvas_w-box[2]+box[0])/2-box[0],(canvas_h-box[3]+box[1])/2-box[1]),text,font=font,fill=(33,32,24),align='center',spacing=18)
            im=im.resize((w,h),Image.Resampling.LANCZOS)
        from kit.image_io import srgb_to_linear
        color=srgb_to_linear(np.asarray(im,dtype=np.float32)/255)
        if role=='Brand':
            # Burned/stamped wood, not a pale foil rectangle.
            ink=np.clip((.112-color.mean(axis=2))/.095,0,1)
            fibres=coherent(rng,w,h,30,3)
            wood=np.broadcast_to((.170,.158,.150),(h,w,3)).copy()*(1+fibres[...,None]*.13)
            color=wood*(1-ink[...,None])+color*ink[...,None]
        scratches=(fine>1.4)*.08; color*=1-scratches[...,None]*wear
        height=-((color.mean(axis=2)<.05)*.00007);rough[:]=.85
    else:
        base={'Porcelain':(.36,.375,.35),'Polymer':(.27,.285,.265),
              'Cable':(.008,.0085,.008),'Vine':(.055,.082,.018),'Recess':(.019,.014,.010)}[role]
        color=np.broadcast_to(base,(h,w,3)).copy()*(1+broad[...,None]*.09)
        if role in ('Porcelain','Polymer'):
            # Dust lives underneath shed lips; UV repeats over each shed.
            collar=(1-smooth(V,.0,.2))*.35*wear;color=mix(color,(.12,.115,.09),collar)
            rough[:]=.28 if role=='Porcelain' else .7
        height=.00002*fine
    return np.clip(color,0,1),height,np.stack([np.clip(ao,.2,1),np.clip(rough,.12,1),np.clip(metal,0,1)],axis=-1)


def source(size=4096,wear=1):
    folder=Path('build/fields');folder.mkdir(parents=True,exist_ok=True);rows={}
    for role,r in RECTS.items():
        x0,y0,x1,y1=r;w=round((x1-x0-2*GUARD)*size/2048);h=round((y1-y0-2*GUARD)*size/2048)
        color,height,orm=field(role,w,h,wear)
        low=float(height.min());span=max(.00001,float(height.max()-low))
        for channel,array in dict(BaseColor=linear_to_srgb(color),Height=((height-low)/span)[...,None],ORM=orm).items():
            write_png(folder/f'{role}_{channel}.png',array,bits=16 if channel=='Height' else 8)
        rows[role]=dict(rect=r,physical_m=PHYSICAL[role],pixels=[w,h],height_distance_m=span,height_offset_m=low,
                        linear_base_median=np.median(color.reshape(-1,3),axis=0).tolist())
    (folder/'fields.json').write_text(json.dumps(dict(size=size,wear=wear,charts=rows),indent=2))
    print('ORIGINAL UTILITY FIELDS',len(rows),size)


def bake(size=4096,samples=4):
    import bpy
    from kit import gpu,model as G
    from atlas import rect
    bpy.ops.wm.read_factory_settings(use_empty=True);sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable()
    sc.cycles.samples=samples;sc.render.bake.margin=0;sc.render.bake.use_clear=True
    config=json.loads(Path('build/fields/fields.json').read_text());objects=[];materials=[]
    for i,(role,row) in enumerate(config['charts'].items()):
        W,H=row['physical_m'];m=bpy.data.materials.new(role);m.use_nodes=True
        ns=m.node_tree.nodes;ns.clear();out=ns.new('ShaderNodeOutputMaterial');target=ns.new('ShaderNodeTexImage');target.name='BAKE_TARGET'
        # Shader source UV is tile-local, target UV is its guarded atlas rect.
        uv=ns.new('ShaderNodeUVMap');uv.uv_map='FieldUV';channels={}
        for channel in ('BaseColor','ORM','Height'):
            n=ns.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(Path(f'build/fields/{role}_{channel}.png').resolve()))
            n.image.colorspace_settings.name='sRGB' if channel=='BaseColor' else 'Non-Color'
            n.extension='EXTEND';m.node_tree.links.new(uv.outputs['UV'],n.inputs['Vector']);channels[channel]=n
        ob=G.mesh(role,[(i*4,0,0),(i*4+W,0,0),(i*4+W,H,0),(i*4,H,0)],[(0,1,2,3)],m)
        src=ob.data.uv_layers.new(name='FieldUV');dst=ob.data.uv_layers.new(name='AtlasUV');a,b,c,d=rect(role)
        for n,(u,v) in enumerate(((0,0),(1,0),(1,1),(0,1))):src.data[n].uv=(u,v);dst.data[n].uv=(a+(c-a)*u,b+(d-b)*v)
        ob.data.uv_layers.active=dst;dst.active_render=True
        materials.append((m,out,target,channels,row));objects.append(ob)
    bpy.ops.object.select_all(action='SELECT');bpy.context.view_layer.objects.active=objects[0]
    # One disjoint physical bake surface, sixteen material charts. Baking
    # separate planes would rescan the 4096 target sixteen times per channel.
    bpy.ops.object.join()
    report={};folder=Path('textures/bake');folder.mkdir(parents=True,exist_ok=True)
    for channel in ('BaseColor','ORM','Normal'):
        im=bpy.data.images.new('UtilityBake'+channel,width=size,height=size,float_buffer=True,alpha=False);im.colorspace_settings.name='Non-Color'
        for m,out,target,channels,row in materials:
            ns,ls=m.node_tree.nodes,m.node_tree.links
            target.image=im;ns.active=target
            if channel=='Normal':
                shader=ns.new('ShaderNodeBsdfPrincipled');bump=ns.new('ShaderNodeBump');bump.inputs['Distance'].default_value=row['height_distance_m'];bump.invert=False
                ls.new(channels['Height'].outputs['Color'],bump.inputs['Height']);ls.new(bump.outputs['Normal'],shader.inputs['Normal'])
            else:
                shader=ns.new('ShaderNodeEmission');ls.new(channels[channel].outputs['Color'],shader.inputs['Color'])
            ls.new(shader.outputs[0],out.inputs['Surface'])
        bpy.ops.object.bake(type='NORMAL' if channel=='Normal' else 'EMIT',normal_space='TANGENT',normal_r='POS_X',normal_g='POS_Y',normal_b='POS_Z')
        pixels=np.empty(size*size*4,np.float32);im.pixels.foreach_get(pixels);array=pixels.reshape(size,size,4)[::-1,:,:3].copy()
        # Fill each chart's 8 delivered-pixel guard from its own boundary.
        for role,row in config['charts'].items():
            x0,y0,x1,y1=[round(v*size/2048) for v in row['rect']];g=round(GUARD*size/2048)
            sy0,sy1=size-y1,size-y0
            interior=array[sy0+g:sy1-g,x0+g:x1-g].copy()
            array[sy0:sy1,x0:x1]=np.pad(interior,((g,g),(g,g),(0,0)),mode='edge')
        if channel=='BaseColor':array=linear_to_srgb(array)
        write_png(folder/f'T_Utility_{channel}.png',array,bits=16 if channel=='Normal' else 8)
        report[channel]=dict(size=size,bytes=(folder/f'T_Utility_{channel}.png').stat().st_size)
        bpy.data.images.remove(im)
    Path('build/bake.json').write_text(json.dumps(dict(engine='Cycles GPU',samples=samples,charts=config,channels=report),indent=2))
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(Path('build/bake-source.blend').resolve()))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=('source','bake'));p.add_argument('--size',type=int,default=4096);p.add_argument('--samples',type=int,default=4);p.add_argument('--wear',type=float,default=1)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    source(a.size,a.wear) if a.stage=='source' else bake(a.size,a.samples)
