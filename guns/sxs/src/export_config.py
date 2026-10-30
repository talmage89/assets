"""Export-only standalone subsets; the main atlas/UV/rig is unchanged."""
from pathlib import Path
import runpy
settings=runpy.run_path(str(Path(__file__).with_name('config.py')))
globals().update({k:v for k,v in settings.items() if k.isupper()})
DETACHABLES=[dict(armature='SXSArmature',bone=bone,bones=[bone],name=name,
 filename=file,clip=clip,frame=0,texture_size=512,texture_clusters=True)
 for bone,name,file,clip in [('LiveR','CoveyShell','shell.glb','Idle'),
                           ('HullR','CoveyHull','hull.glb','IdleSpent')]]
