from pathlib import Path
P=Path(__file__).resolve().parents[1]
b=1.04775;r=.08255;y=.2413;s=b+.13335
MATCHES={'shell':dict(photo=str(P/'refs/product.jpg'),crop=(100,230,920,750),title='Historic size-1 / modern stamped-shell construction comparison',location=(.8,-1.45,1.45),target=(0,-.20,1.16),lens=70,hide=['Wood','Timber','Mounting'],landmarks=[dict(world=(w[0],w[1]-.20,w[2]),pixel=(u,v)) for w,u,v in [((-r,-y,b),180,687),((r,-y,b),408,703),((r,y,b),852,613),((0,-y,s+r),297,288),((0,y,s+r),785,310) ]])}
