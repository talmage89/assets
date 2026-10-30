"""Native photographic wear observations, used only by comparison code.

Values classify apparent exposed finish inside independently outlined parts.
Specular reflections can mimic exposed steel, so the report includes threshold
sensitivity and the actual 2-D classification overlay. No observation is read
by the modeling, material, bake or export stages.
"""
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
from look_review import polygon_mask,REGIONS

def ellipse_mask(shape,ellipses):
 im=Image.new('L',shape,0);d=ImageDraw.Draw(im)
 for x,y,rx,ry in ellipses:d.ellipse((x-rx,y-ry,x+rx,y+ry),fill=255)
 return np.asarray(im)>0

def receiver_parts(shape):
 receiver=polygon_mask(shape,[[(414,446),(469,450),(485,509),(807,512),(814,448),(1452,448),(1456,414),(1604,414),(1611,637),(1550,681),(1510,710),(1448,709),(1457,647),(1374,645),(1360,710),(910,723),(841,721),(835,646),(809,646),(797,670),(552,676),(518,645),(514,551),(451,551),(440,656),(423,683),(416,624),(400,541),(359,506)]])
 heads=ellipse_mask(shape,[(410,493,27,20),(476,509,28,22),(446,620,29,20),(901,476,27,17),(1162,473,31,18),(1414,478,30,17),(1474,474,28,22),(1435,565,30,24),(1417,604,29,22),(1461,628,29,24)])
 return receiver,heads

def observed(base,site,offset=0):
 name='used_receiver' if site in ('receiver','cover','cover_top','rivets','handle') else 'used_right' if site in ('flash','regulator','ports','feet') else 'used_box' if site=='box' else 'used_stock'
 image=np.asarray(Image.open(base/'build/white-balanced'/(name+'.jpg')).convert('RGB'));h,w=image.shape[:2];v=image.max(2).astype(float);y,x=np.mgrid[:h,:w];shape=(w,h)
 receiver,heads=receiver_parts(shape) if name=='used_receiver' else (None,None)
 threshold=0;note='';mode='bright'
 if site=='receiver':
  part=receiver&~heads
  # Only exposed rails/returns, not the olive receiver's unpainted flats.
  roi=polygon_mask(shape,[[(512,510),(805,510),(816,551),(516,560)],[(514,632),(814,630),(817,680),(538,680)],[(807,406),(1452,405),(1454,453),(812,451)],[(804,628),(1448,625),(1451,654),(811,657)],[(1490,405),(1640,407),(1640,690),(1550,700)]])
  threshold=112;wear=part&roi&(v>threshold+offset)
  note='Exposed silver/gray returns and port rims only; olive phosphate flats excluded from wear classification.'
 elif site in ('cover','cover_top'):
  part=polygon_mask(shape,REGIONS['paint_cover'][1]);med=np.asarray(Image.fromarray(np.uint8(v)).filter(ImageFilter.MedianFilter(15)),float)
  if site=='cover':
   roi=((abs(y-(327-(x-790)*.012))<5)&(x>790))|((abs(y-400)<5)&(x>790))|((x>490)&(x<800)&(y>364)&(y<391))|((x>1498)&(y>350))
   threshold=126;wear=part&roi&(v>threshold+offset)
   note='Bright exposed crest/return chips. Broad cylindrical light-card reflection is excluded; threshold sensitivity is retained.'
  else:
   roi=(x>798)&(x<1450)&(y>334)&(y<393)
   threshold=13;wear=part&roi&((v-med)>threshold+offset)&(v>48)
   note='Positive fine scratch contrast on visible cover working face; narrow crown and dark scratches remain censored by this view.'
 elif site=='rivets':
  part=heads;threshold=87;wear=part&(v>threshold+offset)
  note='Whole ten visible head/contact lands; apparent exposed finish, not a paint BRDF recovery.'
 elif site=='handle':
  part=polygon_mask(shape,REGIONS['handle_polymer'][1]);threshold=70;wear=part&(v>threshold+offset)
  note='Bright handled polish footprint; specular response and wear are not uniquely separable in one photograph.'
 elif site=='flash':
  part=polygon_mask(shape,[[(51,145),(121,154),(124,170),(55,166)]]);threshold=45;mode='dark';wear=part&(v<threshold+offset)
  note='Apparent dark muzzle deposit, including shaded slot interiors: upper bound on carbon coverage.'
 elif site=='regulator':
  part=polygon_mask(shape,[[(397,270),(429,274),(435,300),(400,298)]]);threshold=48;mode='dark';wear=part&(v<threshold+offset)
  note='Apparent dark discharge zone; recess shadow limits independent soot segmentation.'
 elif site=='ports':
  part=polygon_mask(shape,[[(845,341),(1017,365),(1007,410),(853,395)]]);threshold=32;mode='dark';wear=part&(v<threshold+offset)
  note='Dark port neighborhood; shadow is inseparable from carbon. Not an absolute carbon-fraction acceptance.'
 elif site=='feet':
  part=polygon_mask(shape,[[(254,695),(273,698),(303,710),(332,706),(334,721),(325,732),(300,734),(278,726),(260,715)],[(385,621),(411,625),(428,632),(438,637),(438,649),(430,656),(411,646),(390,635)]]);threshold=135;wear=part&(v>threshold+offset)
  note='Bright exposed pad pressure/lip lands. Photographed pad shape differs from the accepted original.'
 elif site=='box':
  part=polygon_mask(shape,REGIONS['molded_box'][1]);threshold=82
  wear=part&(x<580)&(y>760)&(v>threshold+offset)
  note='Bottom-impact end/corner scuff, excluding the lid and paper. Broad flank remains the molding color.'
 else:
  part=polygon_mask(shape,REGIONS['molded_stock'][1]);med=np.asarray(Image.fromarray(np.uint8(v)).filter(ImageFilter.MedianFilter(21)),float);threshold=11
  # Native butt is at upper-right in this loose-stock photograph.
  roi=(x>1180)|(y<440);wear=part&roi&((v-med)>threshold+offset)
  note='Fine rubbed heel/toe contrast on butt-end returns; broad old field scuffs are outside this named shoulder-contact site.'
 assert part.sum()>20,(site,'bad photographic observation')
 return image,part,wear,dict(photo=name,threshold=threshold,threshold_offset=offset,classification=mode,limit=note)
