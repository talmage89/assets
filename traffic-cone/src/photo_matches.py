from pathlib import Path
P=Path(__file__).resolve().parents[1]
# Body landmarks in the embedded photograph; soft/cropped base corners are
# not reliable calibration anchors. The base retains the independently cited 14-inch size.
MATCHES={'product':dict(photo=str(P/'refs/sheet-004.jpg'),crop=(0,0,182,435),title='28-inch cone / profile and collars',location=(.25,-1.7,1.05),target=(0,0,.35),lens=65,
landmarks=[dict(world=(0,0,.7112),pixel=(91,10)),dict(world=(-.01905,0,.6985),pixel=(79,20)),dict(world=(.01905,0,.6985),pixel=(104,20)),dict(world=(-.108,0,.03),pixel=(34,383)),dict(world=(.108,0,.03),pixel=(151,383))])}

# Road-used cone has one-piece orange foot, different sleeve widths and a slimmer neck.
# The 28-inch design stays fixed; the fit measures the common cone envelope.
MATCHES['used_roadside']=dict(photo=str(P/'refs/used-roadside.jpg'),crop=(550,330,1080,1420),title='Road-used PVC / scuffs, rubber transfer and worn collar',location=(.35,-2,1.05),target=(0,0,.36),lens=65,exposure=-.10,landmarks=[
 dict(world=(0,0,.7112),pixel=(809,356)),dict(world=(-.01905,0,.6985),pixel=(773,370)),dict(world=(.01905,0,.6985),pixel=(846,370)),
 dict(world=(-.108,0,.03),pixel=(607,1282)),dict(world=(.108,0,.03),pixel=(1015,1268)),dict(world=(0,-.108,.03),pixel=(831,1340))])


# The moderate-use campus cone has a double foot and a taped neck. Exclude
# those different constructions from the four-landmark body-envelope fit.
MATCHES['used_campus']=dict(photo=str(P/'refs/used-campus.jpg'),crop=(150,180,1350,3530),title='Installed used PVC / moderate sleeve abrasion and scuffed foot',
 location=(-.011103,-.818585,.523087),target=(.015186,.154448,.293922),lens=96.861955,exposure=-.10,landmarks=[
 dict(world=(0,0,.7112),pixel=(672,264)),dict(world=(-.108,0,.03),pixel=(355,2900)),
 dict(world=(.108,0,.03),pixel=(1093,2900)),dict(world=(0,-.108,.03),pixel=(750,3120))])
