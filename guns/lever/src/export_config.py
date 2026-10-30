"""Delivery policy for the corrected source and its new atlas layout."""
from pathlib import Path
import runpy
_settings=runpy.run_path(str(Path(__file__).with_name("config.py")))
globals().update({k:v for k,v in _settings.items() if k.isupper()})
EXPORT_TANGENT_ROUNDING=[]
