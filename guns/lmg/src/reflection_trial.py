"""Rejected physical reflection-profile trial, rebuilt on the canonical GLB.

This rig never changes the accepted finish or the canonical comparison rig.
It exposes the local-profile/whole-part tradeoff in the final surface evidence.
"""
from pathlib import Path
import runpy,sys
TRIAL={'color': [0.815339648499324, 0.971246432490335, 1.0],
 'lights': [{'position': [-0.65, 0.12, -0.35], 'power': 0.456255877, 'size': [0.7, 1.2]},
            {'position': [-0.65, 0.12, 0.75], 'power': 0.917246703, 'size': [0.7, 1.2]},
            {'position': [0, -0.8, -0.25], 'power': 3.645221421, 'size': [0.6, 0.7]},
            {'position': [0, 0.95, -0.25], 'power': 6.754541736, 'size': [0.6, 0.7]},
            {'position': [0, 0.95, 0.15], 'power': 2.26143791, 'size': [0.6, 0.7]},
            {'position': [-0.25, 0.15, 0.8], 'power': 0.294797909, 'size': [0.04, 0.65]},
            {'position': [0.25, 0.15, 0.38], 'power': 0.217718335, 'size': [0.04, 0.65]},
            {'position': [0.25, 0.15, 0.8], 'power': 0.880879368, 'size': [0.04, 0.65]},
            {'position': [-0.12, -0.02, -0.065], 'power': 6.4339e-05, 'size': [0.12, 0.15]},
            {'position': [0.6, 0.15, 0.2], 'power': 0.971980353, 'size': [0.07, 0.8]},
            {'position': [-0.65, 0.15, 0.4], 'power': 0.005766229, 'size': [0.8, 0.025]},
            {'position': [-0.32, 0.15, 1.0], 'power': 9.426758525, 'size': [0.8, 0.025]},
            {'position': [-0.08, 0.2, 0.32], 'power': 0.402743746, 'size': [0.16, 0.025]},
            {'position': [-0.15, 0.04, -0.19], 'power': 0.550097747, 'size': [0.35, 0.3]},
            {'position': [-0.18, 0.5, -0.2],
             'power': 0.307745687,
             'size': [0.35, 0.3],
             'target': [0, 0.5, 0.1]},
            {'position': [0.18, 0.5, -0.2],
             'power': 1.277004861,
             'size': [0.35, 0.3],
             'target': [0, 0.5, 0.1]},
            {'position': [-0.12, 0.62, 0.23],
             'power': 0.522267469,
             'size': [0.15, 0.04],
             'target': [0, 0.62, 0.1]}],
 'world': 0.0}

def main():
 base=Path(__file__).resolve().parents[1];sys.path[:0]=[str(base.parents[1]),str(base/'src')]
 from light_fits import FITS
 FITS['cover_profile_trial']=TRIAL
 import final_shots
 final_shots.PHOTO_POSES['used_photo']['light_fit']='cover_profile_trial'
 final_shots.RENDER_STAGE='Rejected physical reflection-profile trial / actual canonical GLB'
 runpy.run_path(str(base/'src/final_render.py'),run_name='__main__')
if __name__=='__main__':main()
