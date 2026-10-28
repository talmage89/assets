"""Shotgun entry point for the shared presentation renderer."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]));sys.path.insert(0,str(Path(__file__).parent))
from guns.common.render import main
import final_shots as shots,interface
if __name__=='__main__':main(shots,interface)
