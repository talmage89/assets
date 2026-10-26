from pathlib import Path
import math
P=Path(__file__).resolve().parents[1]
a=.381;b=a*(math.sqrt(2)-1);s=5.367
# Photo is a historical urban assembly; compare its stop plate, not its black names or round post.
pts=[((-b,a),(225,224)),((b,a),(332,173)),((a,b),(397,247)),((a,-b),(477,447)),((-a,b),(170,410))]
MATCHES={'stop_photo':dict(photo=str(P/'refs/installed.jpg'),crop=(600,650,2750,3485),title='30-inch stop / plate and sheeting comparison',location=(-.7,-1.4,1.4),target=(0,-.03,2.5),lens=45,landmarks=[dict(world=(x,-.0294,2.5146+z),pixel=(u*s,v*s)) for ((x,z),(u,v)) in pts])}
