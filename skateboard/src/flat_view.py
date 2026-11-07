"""Axial camera makes the real skid plane legible without posing the wheel."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import render

def axial(s):
    return {'wheel_profile':dict(location=(-.28,-s.axle_y,s.axle_z),target=(-.084,-s.axle_y,s.axle_z),lens=75,aspect=1.3)}
render.shots=axial
if __name__=='__main__':render.main()
