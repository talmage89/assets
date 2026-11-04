"""Factory factors, using the family's one-atlas coverage-delta method."""
import runpy
from pathlib import Path
_family=runpy.run_path(str(Path(__file__).with_name("pickup_spec.py")))
FAMILY_COLORS=_family["COLORS"];FAMILY_METAL=_family["PAINT_METAL"]
COLORS=dict(FAMILY_COLORS)
PAINT_METAL=dict(FAMILY_METAL)
# Original cool graphite factory option; no photograph is a material input.
COLORS['Graphite']=(.120,.130,.145)
PAINT_METAL['Graphite']=.55
