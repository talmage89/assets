"""Archived delivery in the new hero camera, using the original presentation.

This optional historical comparison consumes the round's preserved delivery;
it never changes it. The production build has no dependency on that archive.
"""
import argparse,subprocess
from pathlib import Path

def render(width,samples):
    here=Path(__file__).resolve().parent;root=here.parents[1]
    archive=root/'build/bus-round2/before-export/C75-101.gltf'
    if not archive.exists():return
    old=subprocess.run(['git','show','75eef44:school-bus/src/render.py'],cwd=root,
                       check=True,capture_output=True,text=True).stdout
    namespace={'__name__':'bus_historical_presentation','__file__':str(here/'render.py')}
    exec(compile(old,'original bus presentation','exec'),namespace)
    namespace['render'](argparse.Namespace(source=str(archive),
        out=str(here.parent/'renders/round2-before/new-hero-camera'),
        shots='hero',width=width,samples=samples,engine='CYCLES',
        school=str(root/'school/export/Campus-101.gltf'),calibration=None))
