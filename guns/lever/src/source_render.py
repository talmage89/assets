"""Separately labeled dense-source comparison, never a final image."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from guns.common.render import main
import final_shots,interface
final_shots.FINAL_STAGE=False
final_shots.RENDER_STAGE='dense procedural source comparison, before baking'
if __name__=='__main__':main(final_shots,interface)
