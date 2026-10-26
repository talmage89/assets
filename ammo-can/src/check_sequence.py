"""Check actual lid opening/removal after release, using the kit's solid-surface sweeps."""
import argparse,json,sys,runpy,math
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.motion import sweep

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));cfg=runpy.run_path(str(ROOT/'ammo-can/src/config.py'))
 latch=bpy.data.objects['Latch'];lid=bpy.data.objects['Lid'];handle=bpy.data.objects['Handle']
 latch.rotation_euler.x=math.radians(-105);bpy.context.view_layer.update()
 opening=sweep({'MOTIONS':[dict(node='Lid',axis='X',range=[0,-110],step=1,tolerance_m=.00025)]})
 lid.rotation_euler.x=math.radians(-110);bpy.context.view_layer.update()
 # At this angle local +Z translates back and slightly down, out through the
 # C hooks' open mouths. The secured body pin remains in the physical check.
 removal=sweep({'MOTIONS':[dict(node='Lid',kind='translation',axis='Z',range=[0,.025],step=.00025,tolerance_m=.00015)]})
 open_handle=sweep({'MOTIONS':[cfg['MOTIONS'][1]]})
 result=dict(passed=opening['passed'] and removal['passed'] and open_handle['passed'],sequence='Release cam -105 degrees, open lid to -110, withdraw cover 25 mm along its local +Z through C hooks',opening=opening,removal=removal,handle_with_open_lid=open_handle,proof='Actual evaluated solid surfaces; exported serialization is a separate check')
 Path(a.out).write_text(json.dumps(result,indent=2));assert result['passed'],'Sequence clearance failure: '+a.out
if __name__=='__main__':main()
