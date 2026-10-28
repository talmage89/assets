"""Relay 9 entry point for the stable family presentation tool."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]));sys.path.insert(0,str(Path(__file__).parent))
from guns.common.render import main
import interface
if any('export/' in arg for arg in sys.argv):
 import final_shots as shots
else:import shots
from kit import weapon_presentation as presentation
base_samples=presentation.strip_samples
def member_samples(duration_frames,*,fps=60,rate=15):
 # A 720-rpm cycle needs native 60-Hz samples to expose its maximum bolt pose.
 # Longer hand motions retain the family's economical uniform 15-Hz review.
 return base_samples(duration_frames,fps=fps,rate=60 if duration_frames<=15 else rate)
presentation.strip_samples=member_samples
if __name__=='__main__':main(shots,interface)
