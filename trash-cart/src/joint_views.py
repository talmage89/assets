"""Close construction views of the delivered hinge through its full range."""
import runpy
from pathlib import Path

globals().update({k: v for k, v in runpy.run_path(
    str(Path(__file__).with_name('config.py'))).items() if not k.startswith('__')})
SHOTS = {
    'closed': dict(location=(.68, .94, 1.35), target=(.235, .395, 1.035),
                   lens=100, aspect=1.4),
    'swing': dict(location=(.68, .94, 1.35), target=(.235, .395, 1.035),
                  lens=100, aspect=1.4, lid=-67),
    'open': dict(location=(.68, .94, 1.35), target=(.235, .395, 1.035),
                 lens=100, aspect=1.4, lid=-110),
}
for shot in SHOTS.values():
    shot['hide_assemblies'] = ['AtlasBlueLid']
