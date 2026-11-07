"""Reuse host-family construction in a fresh process, writing only here.

The families use plain sibling import names. Process isolation keeps their
modules and globals intact; no source monkey patch survives this invocation.
"""
import argparse
import json
import sys
import os
import math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]


def downtown(out,variant='downtown'):
    out=out.resolve();os.chdir(REPO/'downtown')
    sys.path[:0]=[str(REPO),str(REPO/'downtown/src')]
    from plan import generate
    from graphics import generate as signs
    from geometry import palette
    from building import Building
    from kit.tiling import export
    bpy.ops.wm.read_factory_settings(use_empty=True)
    p=generate(411,'midwest')['lots'][5]
    p.update(id='CoffeeHost_Downtown',index=0,width=9.144,depth=27.432,stories=2,
        floor_first=4.572,upper=3.3528,roof=7.9248,height=8.8392,parapet=.9144,
        style='italianate',cornice='metal',corner=None,chamfer=0,tenant='diner',
        awning=False,storefront='iron',transom='clear',gallery=False,bay_window=False,
        fire_escape=False,brick=(.24,.079,.043),painted=False,neighbor_left=8.8,neighbor_right=9.3)
    class CafeHost(Building):
        def shop_room(self,*args):pass
        def graphic(self,b,key,*args):
            if key==self.p['tenant']:return
            super().graphic(b,key,*args)
    cafe=variant=='downtown'
    if not cafe:
        i={'downtown-left':1,'downtown-right':2,'downtown-opposite':3}[variant]
        p.update(id='CoffeeContext_'+variant,index=i,width=7.3152 if i==1 else 8.5344,tenant=('barber','antiques','pharmacy')[i-1],brick=((.23,.11,.060),(.30,.15,.075),(.25,.23,.18))[i-1],stories=2,awning=i==3)
    sheet,layout=signs(out.parent.parent/'host-signs');b=(CafeHost if cafe else Building)(p,palette(sheet),layout)
    root,obs,doors=b.build();root.location.y=p['depth']/2
    for m in bpy.data.materials:
        if m.use_nodes:
            bs=m.node_tree.nodes.get('Principled BSDF')
            if bs and bs.inputs['Transmission Weight'].default_value>.9:bs.inputs['Roughness'].default_value=.002
    # Bring the host's front line to Y=0. Its own origin remains intact.
    bpy.context.view_layer.update();export(out,[root]+list(root.children_recursive))
    out.with_suffix('.json').write_text(json.dumps(p,indent=2)+'\n')


def commercial_finish(C,kind):
    """Bind original Commercial charts in this private host cache only."""
    from surfaces import pbr,charts,tint_layer
    folder=REPO/'commercial/textures/ship'
    wall=pbr('CommercialEIFS',folder,pair=True);equipment=pbr('CommercialEquipment',folder)
    concrete=pbr('CommercialConcrete',folder);roof=pbr('CommercialRoof',folder,pair=True)
    bpy.context.view_layer.update()
    for ob in [o for o in bpy.context.scene.objects if o.type=='MESH']:
        role=ob.data.materials[0].name.removeprefix('Form_').split('.')[0]
        if role=='Glass' or ob.get('graphic'):continue
        old=ob.data.materials[0].node_tree.nodes.get('Principled BSDF');color=tuple(old.inputs['Base Color'].default_value[:3])
        if ob.get('repaint'):color=(.47,.45,.37)
        material=wall if role=='Wall' else concrete if role=='Concrete' else roof if role=='Roof' else equipment
        ob.data.materials.clear();ob.data.materials.append(material)
        cell={'Trim':'Black','Metal':'Metal','White':'White','Primary':'Primary','Accent':'Primary','Black':'Black'}.get(role,'White')
        charts(ob,role,cell=None if role in ('Wall','Concrete','Roof') else cell,coverage=2.4384 if role=='Wall' else 2)
        tint_layer(ob,[color if role not in ('Concrete','Roof') else (1,1,1) for v in ob.data.vertices])


def commercial(kind,out):
    sys.path[:0]=[str(REPO),str(REPO/'commercial/src')]
    import geometry as C
    import strip_building as S
    import building as B
    from kit.tiling import export
    bpy.ops.wm.read_factory_settings(use_empty=True)
    C.palette(dict(primary=(.055,.09,.085),accent=(.32,.16,.08),light=(.65,.62,.52)),(.34,.30,.22) if kind=='strip' else (.42,.40,.32))
    if kind in ('strip','strip-neighbors'):
        w=12.8016;d=19.5072
        p=dict(building=dict(width=w,depth=d,front=0,roof=4.2672,parapet=5.1816),
            style='flat',walk=3.048,endcaps=['wrap','plain'],look=False,modules=[])
        neighbors=kind=='strip-neighbors'
        ink=None;layout={}
        if neighbors:
            from strip_graphics import generate as tenant_graphics,install
            tenant_graphics(Path('build/strip-signs'));ink,layout=install(Path('build/strip-signs'))
        else:S.interior=lambda *args:None;S.quad=lambda *args,**kwargs:None
        for i in range(4 if neighbors else 2):
            m=dict(id=f'CoffeeHost_Bay_{i+1}',width=w/2,depth=d,origin=[(-.25+i*.5)*w,0],
                yaw=0,tenant=('cleaner','hair','pizza','tax')[i] if neighbors else 'vacant',lease_group='other' if neighbors else 'cafe',partition=neighbors,open_left=i>0 and not neighbors,
                address=str(110+2*i) if neighbors else '16',end_column=i==(3 if neighbors else 1),hosted_sign=not neighbors)
            if neighbors:m['origin'][0]+=w
            p['modules'].append(m);S.bay(m,p,ink,layout)
        if not neighbors:S.endcap('CoffeeHost_Endcap',-w/2+.1016,p,outward=-1)
        S.endcap('CoffeeHost_PartyClosure',w/2+(2*w if neighbors else 0)-.1016,p,outward=1)
    else:
        w=10.9728;d=9.144;h=3.66
        p=dict(width=w,depth=d,roof=3.10,parapet=h,construction='commercial wall/storefront helpers, original pad envelope')
        r=C.root('CoffeeHost_Pad',kind='CoffeeHost');r['reusable_module']=True
        C.box('Pad slab',(0,d/2,.0762),(w,d,.1524),'Concrete',r,.005)
        B.wall_with_openings('Pad front masonry',w,h,[(0,w-1.10,.20,2.68),(-1.35,1.0544,.1524,2.73)],r,y=.1016)
        B.glazed_leaf('CoffeeHost_Pad_Entry',-1.35,-.06,.158,.9144,2.03,r)
        for a,c in ((-w/2+.55,-1.89),(-.82,w/2-.55)):
            n=max(1,round((c-a)/1.48))
            for i in range(n):B.storefront('Pad display',a+(i+.5)*(c-a)/n,-.04,(c-a)/n-.035,r)
        C.frame('Pad entry jamb',-1.35,-.06,1.46,1.0544,2.60,'Trim',r,.055,.12)
        C.panel('Pad entry transom',-1.35,-.06,2.475,.91,.43,'Glass',r,.006)
        C.box('Pad threshold',(-1.35,0,.1524),(1.08,.25,.014),'Metal',r,.002)
        for side in (-1,1):
            rr=C.root('Pad side '+str(side),(side*(w/2-.1016),d/2,0),90 if side>0 else -90,parent=r)
            B.wall_with_openings('Pad side masonry',d,h,[(2.8-d/2,1.83,.9652,1.10)] if side>0 else [],rr)
            if side>0:
                x=2.8-d/2;C.frame('Walkup window frame',x,-.12,1.5152,1.83,1.10,'Trim',rr,.055,.12)
                C.panel('Walkup fixed pane',x-.46,-.12,1.5152,.86,.98,'Glass',rr,.006)
                slide=C.root('Walkup_SlidingPane',(x+.46,-.12,1.5152),parent=rr);slide['slide_axis']='X';slide['range_m']=[-.86,0]
                C.panel('Walkup sliding pane',0,0,0,.86,.98,'Glass',slide,.006)
                C.box('Walkup serving shelf',(x,-.26,.9652),(2.05,.55,.045),'Metal',rr,.004)
                for s in (-1,1):C.beam('Walkup shelf bracket',(x+s*.65,-.02,.64),(x+s*.65,-.44,.94),.035,.035,'Trim',rr)
        rr=C.root('Pad rear',(0,d-.1016,0),180,parent=r)
        B.wall_with_openings('Pad rear masonry',w,h,[(w*.28,1.016,.1524,2.134)],rr)
        dp=C.hinge('CoffeeHost_Pad_ServiceDoor',(w*.28-.495,-.13,.158),rr,(-100,0))
        C.box('Pad steel service leaf',(.495,0,1.055),(.984,.045,2.10),'Trim',dp,.004)
        C.box('Pad service landing',(w*.28,-.65,.0762),(1.6,1.10,.1524),'Concrete',rr,.004)
        C.box('Pad membrane',(0,d/2,3.10),(w-.40,d-.40,.045),'Roof',r,0)
        for yy in (.1016,d-.1016):S.coping('Pad coping',w,yy,h,r)
        for s in (-1,1):
            cc=C.root('Pad side coping',(s*(w/2-.1016),d/2,0),90,parent=r);S.coping('Pad side cap',d,0,h,cc)
        # 1997 bank-branch conversion: a broad standing-seam hip with deep
        # eaves, rather than an unexplained flat-parapet cube. Roof panels
        # carry 19 mm standing locks at 406 mm pitch and folded hip caps.
        eave=3.70;peak=5.16;ex=w/2+.46;ey=.46
        corners=[(-ex,-ey,eave),(ex,-ey,eave),(ex,d+ey,eave),(-ex,d+ey,eave)]
        ridge=[(-1.1,d/2,peak),(1.1,d/2,peak)]
        C.mesh('Converted bank hip roof',corners+ridge,[(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4)],'Primary',r,False)
        for a,b in ((0,1),(1,2),(2,3),(3,0)):
            C.beam('Folded eave fascia',corners[a],corners[b],.055,.17,'Primary',r)
            C.beam('Bank roof soffit',tuple(v-.10 if j==2 else v for j,v in enumerate(corners[a])),tuple(v-.10 if j==2 else v for j,v in enumerate(corners[b])),.32,.035,'White',r)
        for corner,rp in zip(corners,(ridge[0],ridge[1],ridge[1],ridge[0])):C.beam('Folded hip lock',corner,rp,.035,.035,'Primary',r)
        C.beam('Folded ridge cap',ridge[0],ridge[1],.09,.04,'Primary',r)
        for side in (-1,1):
            for j in range(-13,14):
                x=j*.4064
                if abs(x)>ex:continue
                frac=max(0,(abs(x)-1.1)/(ex-1.1));end_y=d/2*(1-frac) if side<0 else d-d/2*(1-frac)
                C.beam('Standing roof seam',(x,-ey if side<0 else d+ey,eave+.013),(x,end_y,peak-(peak-eave)*frac+.013),.016,.019,'Primary',r)
        for side in (-1,1):
            for j in range(1,24):
                yy=-ey+j*.4064
                if yy>=d+ey:continue
                t=min(yy+ey,d+ey-yy)/(d/2+ey)
                C.beam('Standing hip panel seam',(side*ex,yy,eave+.013),(side*(ex-(ex-1.1)*t),yy,eave+(peak-eave)*t+.013),.016,.019,'Primary',r)
        patch=C.mesh('Bank stucco local repaint',[(w/2+.001,5.1,.34),(w/2+.001,6.8,.34),(w/2+.001,6.84,1.65),(w/2+.001,6.55,1.77),(w/2+.001,5.15,1.71)],[(0,1,2,3,4)],'Wall',r,False);patch['repaint']=True
        # A cantilevered walk-up cover leaves the accepted side route clear.
        C.box('Walkup shelter soffit',(w/2+.48,2.8,2.66),(1.30,2.9,.11),'White',r,.005)
        for yy in (1.53,4.07):C.beam('Walkup cantilever bracket',(w/2-.04,yy,2.14),(w/2+.94,yy,2.61),.045,.045,'Trim',r)
        C.box('Pad patched infill',(-3.8,-.005,.91),(1.03,.018,1.16),'Concrete',r,0)
        C.box('Pad replaced window sill',(-3.8,-.05,.31),(1.10,.15,.055),'Trim',r,0)
    world=C.root('Host_'+kind,kind='Host');world['reusable_module']=True
    for o in list(bpy.context.scene.objects):
        if o!=world and o.parent is None:o.parent=world
    for ob in bpy.context.scene.objects:
        for mod in list(ob.modifiers):
            if mod.type=='BEVEL' and mod.width<=.0041:ob.modifiers.remove(mod)
    C.M['Glass'].node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.002
    commercial_finish(C,kind);C.finalize();export(out);out.with_suffix('.json').write_text(json.dumps(p,indent=2)+'\n')


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--kind',choices=['downtown','downtown-left','downtown-right','downtown-opposite','strip','strip-neighbors','pad'],required=True);a.add_argument('--out',type=Path,required=True);a=a.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.parent.mkdir(parents=True,exist_ok=True)
    downtown(a.out,a.kind) if a.kind.startswith('downtown') else commercial(a.kind,a.out)
