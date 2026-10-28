"""Explicit native reference patches after independent neutral adaptation."""
import json
from pathlib import Path
from PIL import Image,ImageDraw
from value_review import stats
BASE=Path(__file__).resolve().parents[1]
# Rectangles are picked on the stated preview widths, then scaled to native
# pixels. Missing surfaces are explicitly absent rather than guessed.
PATCHES={
 'left.jpg':(1150,{'steel_barrel':(920,128,1040,144),'steel_receiver':(450,119,480,129),'steel_barrel_highlight':(920,130,1040,140),'scope_visible_bell':(630,64,680,114),'scope_satin_highlight':(630,84,680,94),'scope_dark':(430,91,455,98),'stock_black':(600,145,710,160)}),
 'm24_profile.jpg':(1500,{'steel_barrel':(1200,93,1340,99),'steel_receiver':(610,98,650,104),'scope':(610,59,650,70),'stock_black':(850,125,950,143)}),
 'PEO_M24_SWS-01.jpg':(1500,{'steel_receiver_field_painted':(937,244,960,250),'scope':(700,195,770,210),'stock_gray_camo':(700,270,800,290)}),
 'detail_030.jpg':(1500,{'steel_receiver':(750,100,860,145),'stock_olive':(300,230,450,260)}),
 'detail_029.jpg':(1500,{'steel_receiver':(760,100,860,145),'stock_olive':(300,230,450,260)}),
 'open.jpg':(3008,{'steel_receiver':(1140,985,1310,1010),'scope':(638,550,677,660),'stock_olive_gray':(2110,1080,2260,1120)}),
 'daylight.jpg':(2048,{'steel_barrel':(455,490,510,515),'scope':(650,325,700,342),'stock_black':(895,250,950,268)}),
}
def measure():
 wb=json.loads((BASE/'build/white-balanced/corrections.json').read_text());result={}
 for name,(width,patches) in PATCHES.items():
  im=Image.open(wb[name]['output']).convert('RGB');scale=im.width/width;rows={};marked=im.copy();d=ImageDraw.Draw(marked)
  for role,(x0,y0,x1,y1) in patches.items():
   polygon=[(x0*scale,y0*scale),(x1*scale,y0*scale),(x1*scale,y1*scale),(x0*scale,y1*scale)]
   rows[role]=dict(**stats(im,polygon),polygon_native=polygon);d.line(polygon+[polygon[0]],fill=(255,100,20),width=3);d.text(polygon[0],role,fill=(255,120,20))
  marked.thumbnail((1500,1000));marked.save(BASE/'build/white-balanced'/(Path(name).stem+'-measurements.jpg'),quality=92)
  result[name]=dict(white_balance=wb[name],surfaces=rows,scope_absent=name.startswith('detail_'))
 (BASE/'build/white-balanced/measurements.json').write_text(json.dumps(result,indent=2));return result
if __name__=='__main__':print(json.dumps(measure(),indent=2))
