"""Substitute the accepted dense carved furniture; author original finishes."""
import argparse,sys,json,shutil,hashlib
from pathlib import Path
import bpy
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
import lookdev

def main():
 p=argparse.ArgumentParser();p.add_argument('--wear',type=float,default=.85)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
 with bpy.data.libraries.load(str(BASE/'build/shotgun.blend'),link=False) as (source,destination):
  destination.objects=['HIGH_Stock','HIGH_Forend_Wood']
 for dense in destination.objects:
  target=bpy.data.objects[dense['low_target']];target.data=dense.data.copy()
  target.vertex_groups.clear();group=target.vertex_groups.new(name=target['bone'])
  group.add(list(range(len(target.data.vertices))),1,'REPLACE')
  bpy.data.objects.remove(dense,do_unlink=True)
 records=lookdev.assign(a.wear)
 snapshot=BASE/'build/delivery/high-sources';snapshot.mkdir(exist_ok=True)
 for file in ('lookdev.py','build_high.py'):
  shutil.copy2(BASE/'src'/file,snapshot/file)
 records['_source_sha256']={file:hashlib.sha256((snapshot/file).read_bytes()).hexdigest() for file in ('lookdev.py','build_high.py')}
 bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'build/delivery/high.blend'))
 (BASE/'build/delivery/finishes.json').write_text(json.dumps(records,indent=2))
 print('HEARTH HIGH FINISHES',len(records),flush=True)
if __name__=='__main__':main()
