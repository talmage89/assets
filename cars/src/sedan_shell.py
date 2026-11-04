"""The accepted continuous sheet with physical door/sill partitions for rigging."""
import argparse,json,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from build import Build
import sedan_body,sedan_spec as S,wheels


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--quality',choices=['game','high'],required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True);b=Build(a.quality=='high',0,False)
    b.root.name=S.NAME;b.asset_set=S.ASSET_SET;b.root['asset_set']=S.ASSET_SET;b.physical_doors=True
    sedan_body.build(b);wheels.build(b,S)
    for mat in list(bpy.data.materials):
        if mat.users==0:bpy.data.materials.remove(mat)
    sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
    sc['asset']=S.NAME;sc['quality']=a.quality;sc['stage']='Accepted sheet with physical sill/door partitions';sc['seed']=150
    Path(a.out).parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
    print('S240_RIGGABLE_SHELL',a.quality,flush=True)
if __name__=='__main__':main()
