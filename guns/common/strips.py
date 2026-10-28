"""15-Hz wall-clock frame strips and real-duration playback from imported GLB."""
import os,sys,json,subprocess,struct
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font

def hold_duration(path,size,milliseconds):
 """Retain a static clip's time when libwebp optimizes it to a still image.

 The original VP8/VP8L bitstream is unchanged. Wrap it as one timed frame using
 the WebP container fields: developers.google.com/speed/webp/docs/riff_container.
 No artificial moving pixel or duplicated visual content is introduced.
 """
 data=path.read_bytes();assert data[:4]==b'RIFF' and data[8:12]==b'WEBP'
 frames=[];offset=12
 while offset<len(data):
  tag=data[offset:offset+4];length=struct.unpack_from('<I',data,offset+4)[0]
  end=offset+8+length+(length&1)
  if tag in (b'VP8 ',b'VP8L'):frames.append(data[offset:end])
  offset=end
 assert len(frames)==1,'Only an opaque encoded still may be wrapped'
 def u24(value):return int(value).to_bytes(3,'little')
 def chunk(tag,payload):return tag+struct.pack('<I',len(payload))+payload+b'\0'*(len(payload)&1)
 dimensions=u24(size[0]-1)+u24(size[1]-1)
 body=b'WEBP'+chunk(b'VP8X',b'\x02\0\0\0'+dimensions)
 body+=chunk(b'ANIM',b'\0'*6)
 body+=chunk(b'ANMF',b'\0'*6+dimensions+u24(milliseconds)+b'\x02'+frames[0])
 path.write_bytes(b'RIFF'+struct.pack('<I',len(body))+body)

def main(base,manifest,source='build/weapon.glb',output='renders/checkpoint/strips',*,engine='BLENDER_WORKBENCH',samples=16):
 BASE=Path(base).resolve();CLIPS,FPS=manifest.CLIPS,manifest.FPS
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),17)
 out=BASE/output;out.mkdir(parents=True,exist_ok=True)
 timing={}
 for clip,spec in CLIPS.items():
  folder=out/clip;folder.mkdir(exist_ok=True)
  cmd=['blender','-b','--factory-startup','--python-exit-code','1','--python',str(BASE/'src/render.py'),'--',
       '--source',str(BASE/source),'--out',str(folder),'--engine',engine,
       '--width','400','--samples',str(samples),'--strip',clip]
  if engine!='BLENDER_WORKBENCH':cmd=[str(ROOT/'kit/with_gpu.sh'),*cmd]
  with (folder/'render.log').open('w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True,cwd=ROOT)
  data=json.loads((folder/'shots.json').read_text());panels=[];playback=[]
  for name,s in data.items():
   raw=Image.open(folder/(name+'.png')).convert('RGBA');bg=Image.new('RGBA',raw.size,(58,61,65,255));bg.alpha_composite(raw);raw=bg.convert('RGB')
   p=Image.new('RGB',(400,352),(235,236,233));p.paste(raw,(0,30));d=ImageDraw.Draw(p)
   d.text((8,5),f"{clip} | {s['time_s']:.3f} s / f{s['frame']:g}",font=font,fill=(15,25,20));panels.append(p)
   if s['frame']<spec['frames']:playback.append(raw)
  columns=min(5,len(panels));rows=(len(panels)+columns-1)//columns
  sheet=Image.new('RGB',(columns*400,rows*352),(235,236,233))
  for i,p in enumerate(panels):sheet.paste(p,((i%columns)*400,(i//columns)*352))
  sheet.save(out/(clip+'.jpg'),quality=88,optimize=True)
  # Animated WebP supports millisecond frame durations; preserve the clip's
  # actual duration, including the short Idle endpoint. No slowed key-pose loop.
  duration=round(spec['frames']/FPS*1000);n=max(1,len(playback))
  times=[s['time_s'] for s in data.values()]
  durations=[round(times[i+1]*1000)-round(times[i]*1000) for i in range(n)]
  assert sum(durations)==duration
  timing[clip]=dict(source_fps=FPS,strip_rate_hz=15,duration_ms=duration,playback_frame_durations_ms=durations,samples=[dict(frame=s['frame'],time_s=s['time_s']) for s in data.values()])
  playback[0].save(out/(clip+'.webp'),save_all=True,append_images=playback[1:],duration=durations,loop=0,quality=85)
  path=out/(clip+'.webp')
  with Image.open(path) as encoded:
   encoded.load();single=encoded.n_frames==1
  if single:hold_duration(path,playback[0].size,duration)
  with Image.open(path) as encoded:
   actual=0
   for i in range(encoded.n_frames):
    encoded.seek(i);encoded.load();actual+=encoded.info.get('duration',0)
   assert actual==duration,(clip,actual,duration)
   timing[clip].update(encoded_frame_count=encoded.n_frames,encoded_duration_ms=actual)
  print('STRIP',clip,len(panels),'samples',duration,'ms',flush=True)

 (out/'timing.json').write_text(json.dumps(timing,indent=2))
