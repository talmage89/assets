"""Reuse family coordinate preparation, preserving S240 dielectric road film.

The family decoder multiplies ORM blue by the factory metallic factor. Store
clean paint coverage in that channel so dust does not become metallic when a
factory option changes. The pickup preparation and shader remain unchanged.
"""
import argparse,sys
from pathlib import Path
import bpy
sys.path[:0]=[str(Path(__file__).resolve().parent),str(Path(__file__).resolve().parents[2])]
import prepare_bake

def main():
    p=argparse.ArgumentParser(add_help=False);p.add_argument('--out',required=True)
    a,_=p.parse_known_args(sys.argv[sys.argv.index('--')+1:]);prepare_bake.main()
    for m in bpy.data.materials:
        if not m.get('vehicle_paint'):continue
        nt=m.node_tree;nt.links.new(nt.nodes['OUT_paint_coverage'].outputs[0],nt.nodes['OUT_metal'].inputs[0])
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
if __name__=='__main__':main()
