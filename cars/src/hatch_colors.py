"""Factory factors, using the family's one-atlas coverage-delta method."""
import runpy
from pathlib import Path
_family=runpy.run_path(str(Path(__file__).with_name("pickup_spec.py")))
FAMILY_COLORS=_family["COLORS"];FAMILY_METAL=_family["PAINT_METAL"]
COLORS=dict(FAMILY_COLORS)
PAINT_METAL=dict(FAMILY_METAL)
# Neutral graphite corrected in matched sunlight; no photo enters materials.
COLORS['Graphite']=(.130,.125,.126)
PAINT_METAL['Graphite']=.55
