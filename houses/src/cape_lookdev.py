"""Quick source fields for the form gate; no bake or delivery-map writes.

All accepted shared maps remain read-only. Cedar and cement use an original
small two-region preview tile, planned as one additional 512-square set.
"""
import json
import math
from pathlib import Path
import bpy
import bmesh
import numpy as np
from mathutils import Vector
from kit import tiling
from kit.image_io import write_png,linear_to_srgb
from lookdev import materials
from textures import SETS


def shingle_preview(folder):
    folder.mkdir(parents=True,exist_ok=True);size=512
    if (folder/'T_CapeShingle_BaseColor.png').exists():return
    yy,xx=np.mgrid[:size,:size];u=xx/size;v=yy/size
    h=np.zeros((size,size));value=np.ones_like(h)*.8
    for low,kind in ((0,'cedar'),(.5,'cement')):
        rows=5 if kind=='cedar' else 2
        r=np.floor((v-low)*2*rows).astype(int);inside=(v>=low)&(v<low+.5)
        phase=(r%2)*.5;count=7 if kind=='cedar' else 2
        unit=np.floor(u*count+phase);local=(u*count+phase)%1;fy=((v-low)*2*rows)%1
        rng=.5+.5*np.sin(unit*127.1+r*311.7)
        height=.003*(1-fy)-.001*(local<.035)
        grain=np.sin(u*2*math.pi*119+np.sin(v*19)*.55)*.06 if kind=='cedar' else np.sin(u*2*math.pi*117)*.015
        col=(.91+rng*.09+grain)*(1-.17*np.exp(-fy/.07))
        h[inside]=height[inside];value[inside]=col[inside]
    dx=(np.roll(h,-1,1)-np.roll(h,1,1))/(2*1.2192/size);dy=(np.roll(h,-1,0)-np.roll(h,1,0))/(2*1.2192/size)
    n=np.stack((-dx,-dy,np.ones_like(h)),2);n/=np.linalg.norm(n,axis=2,keepdims=True)
    rgb=np.stack([value]*3,2)
    write_png(folder/'T_CapeShingle_BaseColor.png',np.rint(np.clip(linear_to_srgb(rgb),0,1)*255).astype(np.uint8))
    write_png(folder/'T_CapeShingle_Normal.png',np.rint((n*.5+.5)*255).astype(np.uint8))
    orm=np.zeros((size,size,3),np.uint8);orm[:,:,0]=255;orm[:,:,1]=212;write_png(folder/'T_CapeShingle_ORM.png',orm)


def prepare(source,out):
    bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));bpy.context.view_layer.update()
    meta=json.loads(source.with_suffix('.json').read_text());mats=materials(Path('textures/source'))
    skin=meta['spec']['siding'];preview=out.parent/'materials'/'shingles'
    if skin in ('cedar','cement'):
        shingle_preview(preview);mats['Siding']=tiling.material('CapeShingle',preview,tint=True)
        ns=mats['Siding'].node_tree.nodes;ls=mats['Siding'].node_tree.links
        coord=ns.new('ShaderNodeTexCoord');sep=ns.new('ShaderNodeSeparateXYZ');ls.new(coord.outputs['UV'],sep.inputs[0])
        fract=ns.new('ShaderNodeMath');fract.operation='FRACT';ls.new(sep.outputs['Y'],fract.inputs[0])
        scale=ns.new('ShaderNodeMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=.5;ls.new(fract.outputs[0],scale.inputs[0])
        offset=ns.new('ShaderNodeMath');offset.operation='ADD';offset.inputs[1].default_value=.5 if skin=='cement' else 0;ls.new(scale.outputs[0],offset.inputs[0])
        uvout=ns.new('ShaderNodeCombineXYZ');ls.new(sep.outputs['X'],uvout.inputs[0]);ls.new(offset.outputs[0],uvout.inputs[1])
        for node in ns:
            if node.type=='TEX_IMAGE':ls.new(uvout.outputs[0],node.inputs['Vector'])
    p=mats['Glass'].node_tree.nodes.get('Principled BSDF');nodes=mats['Glass'].node_tree
    for socket in ('Base Color','Roughness'):
        for link in list(p.inputs[socket].links):nodes.links.remove(link)
    p.inputs['Base Color'].default_value=(.95,.97,.95,1);p.inputs['Roughness'].default_value=.035
    total=0;before_total=0;weathered=0;added=0
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH' or not ob.get('asset_set'):continue
        me=ob.data;me.calc_loop_triangles();before_total+=len(me.loop_triangles)
        # Only causal low-wall and upper-roof sample rows. No dense all-face grid.
        if ob.get('component') in ('wall','foundation','roof'):
            bm=bmesh.new();bm.from_mesh(me);block=next((v for v in meta['blocks'] if v['name']==ob.get('block')),meta['blocks'][0])
            levels=[block['floor']-.12,block['floor']+.06,block['floor']+.24,block['floor']+.40] if ob.get('component')!='roof' else [block['eave']+.35,block['eave']+.90,block['eave']+1.7,block['eave']+2.4]
            for z in levels:bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,plane_co=(0,0,z),plane_no=(0,0,1))
            bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
        roles=[m.name.replace('House_','') for m in me.materials]
        for i,role in enumerate(roles):me.materials[i]=mats[role]
        attr=me.color_attributes['Tint'];uv=me.uv_layers.active;world=[ob.matrix_world@v.co for v in me.vertices]
        comp=ob.get('component');block=next((v for v in meta['blocks'] if v['name']==ob.get('block')),meta['blocks'][0]);vr={};normal={}
        for poly in me.polygons:
            role=roles[poly.material_index];n=(ob.matrix_world.to_3x3()@poly.normal).normalized()
            for vi in poly.vertices:
                vr[vi]=role
                if vi not in normal or n.z>.4 or abs(n.z)<.3:normal[vi]=n
            axis=max(range(3),key=lambda k:abs(n[k]));axes=[k for k in range(3) if k!=axis];pts=[world[i] for i in poly.vertices]
            if role=='Trim':axes.sort(key=lambda k:max(p[k] for p in pts)-min(p[k] for p in pts),reverse=True)
            lo=min(p[axes[1]] for p in pts);hi=max(p[axes[1]] for p in pts)
            strip=6 if role=='Glass' else (5 if comp in ('flashing','valley','roof_vent','storm_window') else (2 if comp=='eave_rake_soffit' and n.z<-.6 else 0))
            for li in poly.loop_indices:
                p=world[me.loops[li].vertex_index]
                if role in ('Trim','Glass'):
                    u=p[axes[0]]/4
                    if strip==5:u=.78+.20*(p[axes[0]]%4)/4
                    uv.data[li].uv=(u,(strip+.04+(p[axes[1]]-lo)/max(.5,(hi-lo)/.92))/8)
                elif role=='Shingles' and abs(n.z)>.3:
                    xy=(p.x,p.y/max(.2,abs(n.z))) if abs(n.y)>=abs(n.x) else (p.y,p.x/max(.2,abs(n.z)))
                    uv.data[li].uv=(xy[0]/4.8768,xy[1]/4.8768)
                elif role=='Siding' and skin in ('cedar','cement'):
                    # Preview uses half-tile addressing; ordinary split charts wait
                    # for delivery, just as the ranch's source roof did.
                    uv.data[li].uv=(p[axes[0]]/1.2192, p[axes[1]]/.6096)
                else:uv.data[li].uv=(p[axes[0]]/SETS.get(role,SETS['Trim'])[1],p[axes[1]]/SETS.get(role,SETS['Trim'])[1])
        for v in me.vertices:
            role=vr[v.index];p=world[v.index];n=normal[v.index];c=Vector(attr.data[v.index].color[:3]);amount=0;algae=0
            if role in ('Glass','Veneer'):c=Vector((1,1,1))
            if role=='Concrete':c=Vector((.82,.81,.78))
            if role=='Shingles':c=Vector(dict(warm_charcoal=(.82,.79,.70),weathered_wood=(1.,.86,.65),dark_brown=(.76,.63,.48))[meta['spec']['shingle_color']])
            if role in ('Siding','Concrete'):
                low=max(0,block['floor']-.205) if role=='Siding' else 0
                ripple=.05*math.sin(p.x*8.7+p.y*4.9)+.025*math.sin(p.x*21.3-p.y*7.1)
                amount=.32*max(0,min(1,(low+.32+ripple-p.z)/.25))
                algae=max(0,n.y)*.17*max(0,1-abs(p.z-low-.14)/.5)
            if role=='Shingles' and comp=='roof' and meta['spec']['roof_age']=='tired':
                algae=max(0,n.y)*.30*(.3+.7*(.5+.5*math.sin(p.x*4.7+.3*math.sin(p.y*3)))**4)
            factor=Vector((1-amount*.55-algae*.55,1-amount*.65-algae*.4,1-amount*.77-algae*.65));c*=factor
            attr.data[v.index].color=(*c,1);weathered+=amount>.02 or algae>.02
        me.calc_loop_triangles();total+=len(me.loop_triangles)
    meta.update(triangles=total,stage='Cape form checkpoint / original quick fields / no bake',source_triangles=before_total,weathered_vertices=weathered,preview_siding_set=skin in ('cedar','cement'))
    out.parent.mkdir(parents=True,exist_ok=True);out.with_suffix('.json').write_text(json.dumps(meta,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()))
    print('CAPE_SOURCE',meta['seed'],total,weathered);return meta
