"""Pistol clip-strip entry point."""
import sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE.parents[1]));sys.path.insert(0,str(BASE/'src'))
from guns.common.strips import main
import interface
if __name__=='__main__':main(BASE,interface,source="export/pistol.glb",output="renders/final/strips",engine='BLENDER_EEVEE',samples=16)
