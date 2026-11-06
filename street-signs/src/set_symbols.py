"""Original primitives measured against SHS 2004 Appendix grids 6-10/6-58.

Grid units, hand-entered construction points and cubic control points. No PDF
path, raster, trace or downloaded font is consumed by this module.
"""
import math
from PIL import Image,ImageDraw

def curve(start,segments):
    points=[start];p=start
    for c1,c2,end in segments:
        for j in range(1,17):
            t=j/16;u=1-t;points.append(tuple(u**3*p[k]+3*u*u*t*c1[k]+3*u*t*t*c2[k]+t**3*end[k] for k in (0,1)))
        p=end
    return points

def draw(kind,width=720):
    im=Image.new('L',(width,round(width*48/36)));d=ImageDraw.Draw(im);s=width/36
    def poly(points):d.polygon([(x*s,y*s) for x,y in points],fill=255)
    def head(x,y,r):d.ellipse(((x-r)*s,(y-r)*s,(x+r)*s,(y+r)*s),fill=255)
    if kind=='pedestrian':
        head(17.5,5.2,3.25)
        p=curve((18.5,9.1),[((21,8.3),(27,12),(30.9,14.6)),((30.9,18),(30.9,21.7),(30.9,24.8))])
        p += [(28.8,24.4),(27.9,16.2),(25.6,15.8)]
        p += curve((25.6,15.8),[((26.7,19.3),(28,23.1),(27,27.1))])[1:]
        p += [(31.1,44.2),(28.3,46.2),(22.3,30.7),(19.6,33.6),(15.8,45.3),(12.1,44),(15.4,31.6),(19.2,24.6),(17.7,19.5),(16.2,21.5),(8.9,23.9),(7.8,22.2),(14.5,17.7)]
        p += curve((14.5,17.7),[((15.5,13.1),(16.5,10),(18.5,9.1))])[1:];poly(p)
    else:
        # Child on the left, adult on the right, distinct skirt and satchels.
        head(9.4,11.1,3.22);head(23.05,5.0,3.4)
        poly([(8.6,14.7),(10,14.9),(11.1,14.4),(14,16),(15.7,19.9),(19,18.5),(21.1,11.2),(22.9,9.6),(23,8.9),(24.3,8.9),(25.8,8.2),(26.2,9.1),(28.5,10.1),(32.7,18.2),(32.2,20.9),(33.6,20.7),(35,25.8),(28.6,27.4),(28.5,36),(31.8,44.6),(28.6,46.2),(25,37.2),(24.7,32.1),(22.9,36.2),(22.1,46.3),(19,46.3),(19.9,33.7),(22.6,25.2),(21.1,19.2),(20.2,20.9),(15.5,21.9),(16.6,27.7),(12.4,28.7),(14.1,33.8),(12.3,34.5),(15.5,44.8),(12.5,45.8),(9.8,38.1),(9.7,34.4),(7.5,34.3),(3.4,45.3),(1.8,44.8),(3.8,34.0),(3.7,33.8),(6.6,25.0),(5.9,22.8),(5.4,25.0),(.9,28.0),(0,27.0),(3.7,23.4),(5.6,17.0),(7.5,15.1)])
        # Negative air gaps at the elbows remain measured, open shapes.
        d.polygon([(27.2*s,15.9*s),(29.4*s,19.3*s),(28.9*s,21.4*s),(28.2*s,21.6*s)],fill=0)
        d.polygon([(12.3*s,21*s),(12.9*s,23.8*s),(11.7*s,24*s)],fill=0)
    bbox=im.getbbox();return im.crop(bbox)

def place(image,kind,box,color):
    mask=draw(kind,1440);mask.thumbnail((round(box[2]-box[0]),round(box[3]-box[1])),Image.Resampling.LANCZOS)
    image.paste(color,(round((box[0]+box[2]-mask.width)/2),round(box[1])),mask)
