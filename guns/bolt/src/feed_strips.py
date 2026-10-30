"""30-Hz exported close-ups, including the unchanged ReloadEmpty feed window."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),17)

def main():
    out=BASE/'renders/feed';out.mkdir(parents=True,exist_ok=True);report={}
    for clip,start,end,label in [('Fire',40,125,'Fire'),('ReloadEmpty',40,125,'ReloadEmpty'),
                                ('ReloadEmpty',190,245,'ReloadEmpty-feed')]:
        for cut in (False,True):
            name=label+('-cutaway' if cut else '-port');folder=out/name;folder.mkdir(exist_ok=True)
            cmd=[str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1',
                 '--python',str(BASE/'src/cycle_views.py'),'--','--source',str(BASE/'export/bolt.glb'),
                 '--out',str(folder),'--engine','BLENDER_EEVEE','--width','640','--samples','24',
                 '--clip',clip,'--start',str(start),'--end',str(end)]
            if cut:cmd+=['--cutaway']
            with (folder/'render.log').open('w') as log:subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT,cwd=ROOT)
            meta=json.loads((folder/'shots.json').read_text());panels=[];play=[]
            for shot,row in meta.items():
                rgba=Image.open(folder/(shot+'.png')).convert('RGBA')
                bg=Image.new('RGBA',rgba.size,(58,61,65,255));bg.alpha_composite(rgba);raw=bg.convert('RGB');play.append(raw)
                raw.thumbnail((450,254));panel=Image.new('RGB',(450,288),(229,230,226));panel.paste(raw,(0,32))
                ImageDraw.Draw(panel).text((8,6),f'{clip}  f{row["frame"]:g}  {"receiver section" if cut else "port"}',font=FONT,fill=(22,28,25));panels.append(panel)
            sheet=Image.new('RGB',(1800,288*((len(panels)+3)//4)),(229,230,226))
            for i,panel in enumerate(panels):sheet.paste(panel,(450*(i%4),288*(i//4)))
            sheet.save(out/(name+'.jpg'),quality=91,optimize=True)
            times=[round((v['frame']-start)/60*1000) for v in meta.values()]
            durations=[b-a for a,b in zip(times,times[1:])]
            # The inclusive terminal pose belongs in the strip. Playback ends
            # there, with no extra held frame or slowed loop.
            play[0].save(out/(name+'.webp'),save_all=True,append_images=play[1:-1],duration=durations,loop=0,quality=88)
            with Image.open(out/(name+'.webp')) as encoded:
                actual=0
                for i in range(encoded.n_frames):encoded.seek(i);encoded.load();actual+=encoded.info.get('duration',0)
            assert actual==times[-1],(name,actual,times[-1])
            report[name]=dict(clip=clip,start=start,end=end,rate_hz=30,frames=[r['frame'] for r in meta.values()],
                source_sha256=hashlib.sha256((BASE/'export/bolt.glb').read_bytes()).hexdigest(),cutaway=cut,
                decoded_duration_ms=actual)
            print('FEED STRIP',name,len(panels),'frames',flush=True)
    (out/'timing.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
