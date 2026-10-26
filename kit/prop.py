"""Small-prop construction helpers: authored plates, rest frames, and manifests."""
import argparse,json,sys,math
from pathlib import Path
import bpy
from mathutils import Vector
from kit import model as G,materials as M

class Build:
    def __init__(self,asset,quality,wear):
        self.asset=asset;self.high=quality=='high';self.wear=wear
        self.root=G.pivot(asset,(0,0,0));self.root['static_root']=True
    def add(self,ob,parent=None):return G.attach(ob,parent or self.root,self.asset)
    def metal(self,name='Weathered zinc',color=(.36,.39,.40)):
        return M.surface(name,'stainless',self.wear,color=color,roughness=.60,dust=.28,grime=.25)
    def bolt(self,name,point,direction,mat,r=.004):
        return [self.add(o) for o in G.fastener(name,point,direction,mat,r,self.high)]
    def plate(self,name,points,depth,mat,front=None,back=None,center=(0,0,0),rotation=0):
        ob=G.profile(name,points,-depth/2,depth/2,mat,axis='Y',radius=.0003 if self.high else 0,segments=2)
        G.apply(ob)
        if front or back:
            if front:ob.data.materials.append(front)
            if back:ob.data.materials.append(back)
            uv=ob.data.uv_layers.new(name='PrintUV')
            xs=[p[0] for p in points];zs=[p[1] for p in points];w=max(xs)-min(xs);h=max(zs)-min(zs)
            for p in ob.data.polygons:
                p.material_index=1 if front and p.normal.y<-.9 else (2 if front and back and p.normal.y>.9 else 0)
                for i in p.loop_indices:
                    v=ob.data.vertices[ob.data.loops[i].vertex_index].co
                    u=(v.x-min(xs))/w
                    uv.data[i].uv=(1-u if p.normal.y>.9 else u,(v.z-min(zs))/h)
        ob.rotation_euler.z=rotation;ob.location=center
        return self.add(ob)
    def save(self,path,quality):
        sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
        sc['asset']=self.asset;sc['quality']=quality;sc['wear']=self.wear;sc['stage']='lookdev';sc['seed']=73
        bpy.context.view_layer.update();bpy.ops.file.pack_all();Path(path).parent.mkdir(parents=True,exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(Path(path).resolve()))
        counts={'installed':0,'atlas_templates':0}
        for ob in sc.objects:
            if ob.type=='MESH':
                ob.data.calc_loop_triangles();counts['atlas_templates' if ob.get('bake_only') else 'installed']+=len(ob.data.loop_triangles)
        print('BUILD_COUNTS',json.dumps(counts),flush=True)

def arguments():
    p=argparse.ArgumentParser();p.add_argument('--quality',choices=['high','game'],default='high');p.add_argument('--wear',type=float,default=.35);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    if not 0<=a.wear<=2:raise ValueError('wear must be in [0,2]')
    bpy.ops.wm.read_factory_settings(use_empty=True)
    return a
