from pathlib import Path
P=Path(__file__).resolve().parents[1]
b=1.04775;r=.08255;y=.2413;s=b+.13335
MATCHES={'shell':dict(photo=str(P/'refs/product.jpg'),crop=(100,230,920,750),title='Historic size-1 / modern stamped-shell construction comparison',location=(.8,-1.45,1.45),target=(0,-.20,1.16),lens=70,hide=['Wood','Timber','Mounting'],landmarks=[dict(world=(w[0],w[1]-.20,w[2]),pixel=(u,v)) for w,u,v in [((-r,-y,b),180,687),((r,-y,b),408,703),((r,y,b),852,613),((0,-y,s+r),297,288),((0,y,s+r),785,310) ]])}

# In-service galvanized mailbox: color/design differ; judge the weathered surface response,
# handling/fastener deposits and nearby checked wood. No photo pixels enter materials.
MATCHES['used_installed']=dict(photo=str(P/'refs/used-post.jpg'),crop=(250,0,1350,1067),title='Installed mailbox / wet seams, handling and gray checked timber',location=(.8,-1.55,1.5),target=(0,-.20,1.16),lens=65,exposure=-.50,landmarks=[
 dict(world=(-r,-y-.20,b),pixel=(337,907)),dict(world=(r,-y-.20,b),pixel=(893,941)),
 dict(world=(0,-y-.20,s+r),pixel=(604,111)),dict(world=(r,y-.20,b),pixel=(1237,917)),dict(world=(0,y-.20,s+r),pixel=(1048,270))])

# Black in-service finish and a silvered timber support; cropping hides the grade.
MATCHES['used_black_post']=dict(photo=str(P/'refs/used-black-post.jpg'),crop=(100,0,1200,900),title='Used black enamel / handled edges and silvered checked post',location=(1.3,-.55,1.4),target=(0,-.20,1.16),lens=65,exposure=-.65,landmarks=[
 dict(world=(r,-y-.20,b),pixel=(201,540)),dict(world=(r,y-.20,b),pixel=(1130,555)),
 dict(world=(0,-y-.20,s+r),pixel=(269,70)),dict(world=(0,y-.20,s+r),pixel=(1144,78)),
 dict(world=(r,-y-.20,s),pixel=(182,313)),dict(world=(r,y-.20,s),pixel=(1080,320))])
