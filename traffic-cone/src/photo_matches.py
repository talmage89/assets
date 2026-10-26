from pathlib import Path
P=Path(__file__).resolve().parents[1]
# Body landmarks in the embedded photograph; soft/cropped base corners are
# not reliable calibration anchors. The base retains the independently cited 14-inch size.
MATCHES={'product':dict(photo=str(P/'refs/sheet-004.jpg'),crop=(0,0,182,435),title='28-inch cone / profile and collars',location=(.25,-1.7,1.05),target=(0,0,.35),lens=65,
landmarks=[dict(world=(0,0,.7112),pixel=(91,10)),dict(world=(-.01905,0,.6985),pixel=(79,20)),dict(world=(.01905,0,.6985),pixel=(104,20)),dict(world=(-.108,0,.03),pixel=(34,383)),dict(world=(.108,0,.03),pixel=(151,383))])}
