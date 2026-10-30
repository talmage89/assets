"""Dimensioned actual triangle-plane cuts: imported game and dense wood cages."""
import json,sys,math,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from kit import weapon as W,weapon_verify as V
BASE=Path(__file__).resolve().parents[1]
CUTS=[('Head 3 mm behind breech',1,.112,(0,2),('Action_Body',)),
 ('Head 8 mm behind breech',1,.107,(0,2),('Action_Body',)),
 ('Head 15 mm behind breech',1,.100,(0,2),('Action_Body',)),
 ('Right bore axis',3,.0126,(1,2),('Action_Body','Top_Strap')),
 ('Left bore axis',3,-.0126,(1,2),('Action_Body','Top_Strap')),
 ('Centerline Y94 to Y115',0,.0000005,(1,2),('Action_Body','Top_Strap')),
 ('Concentric fence rolls',1,.108,(0,2),('Action_Body',)),
 ('Shoulder and head',1,.096,(0,2),('Action_Body','Stock_Walnut','Top_Strap','Top_Lever')),
 ('Barrels at breech',1,.117,(0,2),('Barrel_R','Barrel_L','Solid_TopRib','Extractor_Rim_R','Extractor_Rim_L')),
 ('Barrels at muzzle',1,.7749,(0,2),('Barrel_R','Barrel_L','Solid_TopRib','Bottom_Rib')),
 ('Action at knuckle',1,.1703,(0,2),('Action_Body','Hinge_Pin','Barrel_Hook','Forend_IronCup_R','Forend_IronCup_L')),
 ('Action at bar',1,.145,(0,2),('Action_Body','Breech_Lumps','Bottom_Rib')),
 ('Flush plate seam',1,.1005,(0,2),('Action_Body','Trigger_Plate')),
 ('Front trigger slot',1,.064,(0,2),('Trigger_Plate','Front_Trigger')),
 ('Rear trigger slot',1,.031,(0,2),('Trigger_Plate','Rear_Trigger')),
 ('Knuckle side section',0,.014,(1,2),('Action_Body','Forend_IronCup_R','Forend_Iron')),
 ('Standing breech',1,.1146,(0,2),('Action_Body','Bushing_R','Bushing_L','PinFace_R','PinFace_L')),
 ('Forend rear',1,.211,(0,2),('Forend_Walnut','Barrel_R','Barrel_L','Forend_Iron','Bottom_Rib')),
 ('Forend front',1,.320,(0,2),('Forend_Walnut','Barrel_R','Barrel_L','Bottom_Rib')),
 ('Butt stock rear',1,-.245,(0,2),('Stock_Walnut',)),
 ('Butt stock front',1,-.150,(0,2),('Stock_Walnut',)),
 ('Wrist',1,-.015,(0,2),('Stock_Walnut','Top_Strap','Trigger_Plate')),
 ('Tang inlet',1,.005,(0,2),('Stock_Walnut','Top_Strap','Tang_Safety','Safety_Guide')),
 ('Action floor and lumps',0,.0000005,(1,2),('Action_Body','Breech_Lumps','Barrel_Hook','Hook_Web','Locking_Shoe','Locking_Shoe_Upper','Hinge_Pin'))]
def capture(path,dense=False):
 if path.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(path))
 else:V.import_glb(path)
 arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE');W.pose(arm,'Idle',0)
 rows=[];dg=bpy.context.evaluated_depsgraph_get()
 for title,axis,station,projection,names in CUTS:
  parts={}
  for name in names:
   target='HIGH_'+name if dense and name in ('Stock_Walnut','Forend_Walnut','Action_Body','Top_Lever') else name
   ob=next(o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('part_name',o.name)==target) if not dense else bpy.data.objects[target]
   ev=ob.evaluated_get(dg);mesh=ev.to_mesh();mesh.calc_loop_triangles();segments=[]
   for tri in mesh.loop_triangles:
    vs=[ev.matrix_world@mesh.vertices[i].co for i in tri.vertices];hits=[]
    for a,b in zip(vs,vs[1:]+vs[:1]):
     if axis==3:
      sign=1 if station>0 else -1
      da=a.x-sign*(.0126-(a.y-.115)*1.7/660.4)
      db=b.x-sign*(.0126-(b.y-.115)*1.7/660.4)
     else:da=a[axis]-station;db=b[axis]-station
     if da*db<0:hits.append(a+(b-a)*(-da)/(db-da))
    if len(hits)==2:
     if title=='Centerline Y94 to Y115':
      # Clip the actual triangle intersection to the named datum interval.
      a,b=hits;delta=b-a;lo=0.;hi=1.
      if abs(delta.y)<1e-12:
       if not .094<=a.y<=.115:continue
      else:
       bounds=sorted(((.094-a.y)/delta.y,(.115-a.y)/delta.y))
       lo=max(lo,bounds[0]);hi=min(hi,bounds[1])
       if hi<=lo:continue
      hits=[a+delta*lo,a+delta*hi]
     segments.append([[p[k]*1000 for k in projection] for p in hits])
   ev.to_mesh_clear()
   if segments:parts[name]=segments
  assert parts,title
  pts=[p for ss in parts.values() for seg in ss for p in seg];b=[[min(p[k] for p in pts),max(p[k] for p in pts)] for k in (0,1)]
  rows.append(dict(title=title,plane=('bore-axis vertical' if axis==3 else 'XYZ'[axis]),station_mm=station*1000,axes=['XYZ'[k] for k in projection],parts=parts,part_sizes_mm={name:[max(p[k] for seg in ss for p in seg)-min(p[k] for seg in ss for p in seg) for k in (0,1)] for name,ss in parts.items()},bounds_mm=b,size_mm=[hi-lo for lo,hi in b]))
 return rows
def main():
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--game',default=str(BASE/'export/sxs.glb'));parser.add_argument('--source',default=str(BASE/'build/sxs.blend'));parser.add_argument('--out',default=str(BASE/'renders/checkpoint/sections'))
 args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
 game=Path(args.game).resolve();source=Path(args.source).resolve();out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=True)
 result=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),glb_sha256=hashlib.sha256(game.read_bytes()).hexdigest(),dense=capture(source,True),game=capture(game))
 (out/'sections.json').write_text(json.dumps(result,indent=2))
 from PIL import Image,ImageDraw,ImageFont
 from kit.fonts import find_font
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),21);small=ImageFont.truetype(find_font('Noto Sans','Regular'),17)
 panels=[]
 for g,h in zip(result['game'],result['dense']):
  im=Image.new('RGB',(700,650),(239,240,235));d=ImageDraw.Draw(im);b=g['bounds_mm'];cx=sum(b[0])/2;cy=sum(b[1])/2
  scale=min(600/(b[0][1]-b[0][0]),470/(b[1][1]-b[1][0]));xy=lambda p:(350+(p[0]-cx)*scale,325-(p[1]-cy)*scale)
  d.text((16,12),g['title'],font=font,fill=(25,36,31));d.text((16,45),f"{g['plane']} = {g['station_mm']:g} mm / {' x '.join(f'{v:.2f}' for v in g['size_mm'])} mm",font=small,fill=(25,36,31))
  for name,values in g['part_sizes_mm'].items():
   if name in ('Forend_Walnut','Stock_Walnut'):d.text((16,76),name+': '+' x '.join(f'{v:.2f}' for v in values)+' mm',font=small,fill=(25,36,31))
  for row,color,width in [(h,(29,145,144),4),(g,(142,63,35),1)]:
   for ss in row['parts'].values():
    for seg in ss:d.line([xy(p) for p in seg],fill=color,width=width)
  # Review-only arrows identify construction landmarks on the measured
  # sections. They do not enter the geometry or its acceptance probes.
  notes={
   'Head 3 mm behind breech': [('R13.35 front / R6 side',(24,50)),('centerline',(0,55.59))],
   'Head 8 mm behind breech': [('degree-5 return',(19,51)),('centerline',(0,55.59))],
   'Head 15 mm behind breech': [('6 mm side return',(24,47)),('centerline',(0,55.59))],
   'Right bore axis': [('18.5 mm axial roll',(105,55)),('head to strap',(87,47))],
   'Left bore axis': [('18.5 mm axial roll',(105,55)),('head to strap',(87,47))],
   'Centerline Y94 to Y115': [('front floor',(111,55.59)),('lever recess',(96,48))],
   'Concentric fence rolls': [('bore axis',(12.618,44)),('bore axis',(-12.618,44))],
   'Action at bar': [('ground side',(25.95,20)),('rounded lower arris',(-23,5.8))],
   'Flush plate seam': [('shared lower skin',(20,1.6))],
   'Front trigger slot': [('6.0 mm slot / 5.4 mm blade',(5.6,6.5))],
   'Rear trigger slot': [('6.0 mm slot / 5.4 mm blade',(-5.6,2.8))]}
  from landmarks import arrow
  for i,(label,point) in enumerate(notes.get(g['title'],[])):
   start=(22,111+i*34);d.text(start,label,font=small,fill=(25,75,70))
   if label!='bore axis':
    from mathutils import Vector
    target=Vector(point);nearest=[]
    for values in g['parts'].values():
     for a,b in values:
      a,b=Vector(a),Vector(b);delta=b-a
      t=max(0,min(1,(target-a).dot(delta)/max(delta.length_squared,1e-20)))
      nearest.append(a+delta*t)
    point=min(nearest,key=lambda p:(p-target).length_squared)
   arrow(d,(220,123+i*34),xy(point),color=(20,115,105))
  d.text((16,598),'teal: dense/source / brown: imported GLB',font=small,fill=(25,36,31))
  d.text((16,625),' / '.join(g['parts']),font=small,fill=(25,36,31));panels.append(im)
  im.save(out/(g['title'].lower().replace(' ','-')+'.jpg'),quality=92,optimize=True)
 sheet=Image.new('RGB',(2100,650*math.ceil(len(panels)/3)),(239,240,235))
 for i,im in enumerate(panels):sheet.paste(im,(i%3*700,i//3*650))
 sheet.save(out/'sections.jpg',quality=92,optimize=True);print('SECTIONS',len(panels),out/'sections.jpg')
if __name__=='__main__':main()
