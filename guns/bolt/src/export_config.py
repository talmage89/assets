"""Standalone texture policy; changing it never invalidates the gun bake."""
from pathlib import Path
import runpy
_settings=runpy.run_path(str(Path(__file__).with_name("config.py")))
globals().update({k:v for k,v in _settings.items() if k.isupper()})
DETACHABLES=[dict(spec,texture_size=1024,texture_clusters=True) for spec in DETACHABLES]
