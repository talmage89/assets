"""Alder C150 body-form checkpoint, from a clean Blender 5.2 scene."""
import argparse,json,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import model as G
from kit.vehicle import panel,samples
import pickup_spec as S
import body,wheels


class Build:
    def __init__(self,high):
        self.high=high;self.root=G.pivot('AlderC150',(0,0,0));self.root['static_root']=True
        self.root['asset_set']='Pickup'
        self.m={}
        for key,color in dict(body=(.39,.405,.41),glass=(.065,.086,.095),rubber=(.027,.029,.032),
                              wheel=(.34,.35,.36),bed=(.12,.13,.14),bumper=(.20,.21,.22)).items():
            m=bpy.data.materials.new('Clay '+key);m.diffuse_color=(*color,1);m.use_nodes=True
            bs=m.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=(*color,1)
            bs.inputs['Roughness'].default_value=.43 if key=='body' else .65
            self.m[key]=m
    def add(self,ob,parent=None,category='body'):
        ob['part_category']=category
        ob=G.attach(ob,parent or self.root,asset_set='Pickup')
        if not ob.data.has_custom_normals:G.smooth(ob,35)
        return ob
    def skin(self,name,fn,nu,nv,mat,outward,parent=None,category='body',**kw):
        factor=1.5 if self.high else .6
        # Flat floors/inner walls and glass need no dense redundant sheet grid.
        if not self.high and (name in ['Cab floor','Pickup bed floor','Cab rear lower','Pickup box front'] or category=='glass'):
            factor=.3
        ob=panel(name,fn,samples(max(2,round(nu*factor))),samples(max(2,round(nv*factor))),mat,outward,**kw)
        return self.add(ob,parent,category)


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--quality',default='high',choices=['game','high']);p.add_argument('--wear',type=float,default=.65)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    b=Build(args.quality=='high');body.build(b);wheels.build(b,S)
    sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
    sc['asset']='AlderC150';sc['quality']=args.quality;sc['stage']='body-form checkpoint';sc['seed']=150
    sc['reference_dimensions']=json.dumps(dict(length=S.LENGTH,width=S.WIDTH,height=S.HEIGHT,wheelbase=S.WHEELBASE,track=S.TRACK))
    bpy.context.view_layer.update();Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(args.out).resolve()))
    counts={}
    for ob in sc.objects:
        if ob.type=='MESH':
            ob.data.calc_loop_triangles();cat=ob['part_category'];counts[cat]=counts.get(cat,0)+len(ob.data.loop_triangles)
    print('CHECKPOINT_TRIANGLES',json.dumps(counts),sum(counts.values()),flush=True)


if __name__=='__main__':main()
