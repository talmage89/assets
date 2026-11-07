"""Reconstruct the accepted prior checkpoint locally from its tracked scripts."""
from pathlib import Path
import subprocess
root=Path(__file__).resolve().parents[1];dest=root/'build/baseline-src';dest.mkdir(parents=True,exist_ok=True)
for name in ('build.py','spec.py'):
    text=subprocess.check_output(['git','show','8cc0710:skateboard/src/'+name],text=True,cwd=root)
    if name=='build.py':text=text.replace('ROOT=Path(__file__).resolve().parents[2]','ROOT=Path(__file__).resolve().parents[3]')
    (dest/name).write_text(text)
