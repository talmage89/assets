"""Additional final feed-tray view; presentation only, exported baked GLB."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(Path(__file__).parent)]
import final_shots as shots
# Keep the entire raised cover and the laid belt in the same frame.
shots.SHOTS['belt_laid'] = dict(location=(-.70, -.08, .58), target=(-.015, .14, .24),
    lens=48, aspect=1.35, action='Reload', frame=264, exposure=-.15)
# Reuse the accepted entry point's imported-axis-aware pose composition.
import runpy
runpy.run_path(str(Path(__file__).with_name('final_render.py')), run_name='__main__')
