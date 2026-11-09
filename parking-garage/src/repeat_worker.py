"""Clean independent garage and site rebuild, in one serialized worker."""
from pathlib import Path
import runpy
import sys

for name in ('build.py','site.py'):
    script=Path('src')/name
    sys.argv=[str(script),'--']
    runpy.run_path(str(script),run_name='__main__')
