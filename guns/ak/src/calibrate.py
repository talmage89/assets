"""Asset camera policy: constrain side/rear frames, reuse kit projection/verify.

The free kit fit remains appropriate for independent receiver and oblique
anchors. A nominal side/axial photograph may not invent yaw or elevation to
lower its residual: those directions are held at the observed view. Only
camera translation and roll are fitted, at a long fixed lens. Residuals are
retained honestly; this is framing, not shape acceptance.
"""
import json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit.photo_match import calibrate,project
from photo_matches import MATCHES

from guns.common.photo_matches import constrained

def main():
 results={n:(constrained(m) if m.get('fixed_view') else calibrate(m)) for n,m in MATCHES.items()}
 out=Path(__file__).resolve().parents[1]/'build/cameras.json';out.write_text(json.dumps(results,indent=2))
 for n,r in results.items():print(n,round(r['residual_rms_pixels'],2),'px',r.get('framing_policy','free oblique fit'))
if __name__=='__main__':main()
