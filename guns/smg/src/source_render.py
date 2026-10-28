"""Explicit dense-source companion to the exported comparisons."""
import sys
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parents[3]),str(Path(__file__).parent)]
from guns.common.render import main
import final_shots,interface
final_shots.FINAL_STAGE=False;final_shots.RENDER_STAGE='dense source comparison / original procedural finish'
if __name__=='__main__':main(final_shots,interface)
