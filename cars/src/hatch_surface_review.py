"""Same-framing, native-region comparisons with the earlier exported checkpoint."""
import argparse,json,hashlib,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from hatch_detail_review import sheet
REGIONS={
 'lens':('lamp_unlit',(.34,.38,1,.98)),
 'hood':('hood_detail',(0,0,1,1)),
 'rear-quarter':('rear_quarter',(0,0,1,1)),
 'front-arch':('wheel',(0,0,.36,.86)),
 'tire':('wheel',(.12,.06,.88,.95)),
 'grille':('grille',(0,0,1,1)),
 'fog-pocket':('fog_detail',(0,0,1,1)),
 'face':('face',(0,0,1,1)),
 'rear-glass':('Graphite_rear',(.15,.18,.62,.61)),
}


def main():
 p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',required=True);a=p.parse_args();before=Path(a.before);after=Path(a.after)
 bm=json.loads((before/'shots.json').read_text());am=json.loads((after/'shots.json').read_text());font=ImageFont.truetype(find_font('Noto Sans','Regular'),21)
 records={}
 for region,(shot,rect) in REGIONS.items():
  panels=[]
  for folder,meta in [(before,bm),(after,am)]:
   im=Image.open(folder/(shot+'.png')).convert('RGB');crop=tuple(round(v*(im.width if i%2==0 else im.height)) for i,v in enumerate(rect));im=im.crop(crop)
   im.thumbnail((900,760),Image.Resampling.LANCZOS);panels.append((im,crop))
  height=max(im.height for im,_ in panels);canvas=Image.new('RGB',(1800,height+50),(228,231,234));draw=ImageDraw.Draw(canvas)
  for k,((im,crop),meta) in enumerate(zip(panels,[bm,am])):
   draw.text((k*900+15,12),('Earlier / ' if k==0 else 'Corrected / ')+region,font=font,fill=(20,30,35));canvas.paste(im,(k*900+(900-im.width)//2,50))
  canvas.save(after/('compare-'+region+'.jpg'),quality=93,optimize=True)
  records[region]=dict(shot=shot,crops=[q[1] for q in panels],before_sha256=bm[shot]['source_sha256'],after_sha256=am[shot]['source_sha256'])
 colors=[color+'_'+view for color in ['Porcelain','Carbon','Graphite','Aluminum','Atlantic'] for view in ['front','rear']]
 sheet(after,colors,after/'five-colors.jpg',2,(800,525))
 # The old sheet remains at its original rendering resolution.
 old=Image.open(before/'five-colors.jpg');new=Image.open(after/'five-colors.jpg');old.thumbnail((1200,3200));new.thumbnail((1200,3200))
 canvas=Image.new('RGB',(old.width+new.width,max(old.height,new.height)+40),(228,231,234));draw=ImageDraw.Draw(canvas);draw.text((12,10),'Earlier',font=font,fill=(20,30,35));draw.text((old.width+12,10),'Corrected',font=font,fill=(20,30,35));canvas.paste(old,(0,40));canvas.paste(new,(old.width,40));canvas.save(after/'compare-five-colors.jpg',quality=91,optimize=True)
 (after/'surface-comparisons.json').write_text(json.dumps(records,indent=2))
 print('H120_SURFACE_COMPARISONS',len(records),'regions')
if __name__=='__main__':main()
