"""Remove current delivery/cache outputs; retain original correction history."""
from pathlib import Path
import shutil

def remove(p):
    if p.is_dir() and not p.is_symlink():shutil.rmtree(p)
    elif p.exists() or p.is_symlink():p.unlink()

keep={'preservation.json','before-delivery','delivery-baseline-source'}
for p in Path('build').glob('*'):
    if p.name not in keep:remove(p)
for p in Path('renders').glob('*'):
    if not p.name.startswith('delivery-'):remove(p)
for p in (Path('export'),Path('textures')):
    if p.exists():remove(p)
