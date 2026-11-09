"""Fresh-import construction, motion and resource checks under one lock."""
from pathlib import Path
import runpy
import sys

for name in ('parameter_check.py','check.py','motion_check.py','site_check.py'):
    script=Path(__file__).resolve().parent/name
    sys.argv=[str(script),'--']
    runpy.run_path(str(script),run_name='__main__')
