"""Separate source comparison entry point; final renderer only accepts GLB."""
import sys
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
sys.path.insert(0,str(Path(__file__).resolve().parent))
import final_shots,interface
from guns.common.render import main
config=SimpleNamespace(**{k:v for k,v in vars(final_shots).items() if not k.startswith('_')})
config.FINAL_STAGE=False;config.RENDER_STAGE='original dense procedural source comparison'
main(config,interface)
