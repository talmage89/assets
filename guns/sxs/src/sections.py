"""Dimensioned actual triangle-plane cuts: imported game and dense wood cages."""
import json,sys,math,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from kit import weapon as W,weapon_verify as V
BASE=Path(__file__).resolve().parents[1]
CUTS=[('Barrels at breech',1,.117,(0,2),('Barrel_R','Barrel_L','Solid_TopRib','Extractor_Rim_R','Extractor_Rim_L')),
 ('Barrels at muzzle',1,.7749,(0,2),('Barrel_R','Barrel_L','Solid_TopRib','Bottom_Rib')),
 ('Action at knuckle',1,.1703,(0,2),('Action_Body','Knuckle_R','Knuckle_L','Hinge_Pin','Barrel_Hook','Forend_IronCup_R','Forend_IronCup_L')),
 ('Standing breech',1,.1146,(0,2),('Action_Body','Bushing_R','Bushing_L','PinFace_R','PinFace_L')),
 ('Forend rear',1,.211,(0,2),('Forend_Walnut','Barrel_R','Barrel_L','Forend_Iron','Bottom_Rib')),
 ('Forend front',1,.320,(0,2),('Forend_Walnut','Barrel_R','Barrel_L','Bottom_Rib')),
 ('Butt stock rear',1,-.245,(0,2),('Stock_Walnut',)),
 ('Butt stock front',1,-.150,(0,2),('Stock_Walnut',)),
 ('Wrist',1,-.015,(0,2),('Stock_Walnut','Top_Strap','Trigger_Plate')),
 ('Tang inlet',1,.005,(0,2),('Stock_Walnut','Top_Strap','Tang_Safety','Safety_Guide')),
 ('Action floor and lumps',0,0,(1,2),('Action_Body','Breech_Lumps','Barrel_Hook','Hook_Web','Locking_Shoe','Locking_Shoe_Upper','Hinge_Pin'))]
def capture(path,dense=False):
 if path.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(path))
 else:V.import_glb(path)
 arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE');W.pose(arm,'Idle',0)
 rows=[];dg=bpy.context.evaluated_depsgraph_get()
 for title,axis,station,projection,names in CUTS:
  parts={}
  for name in names:
   target='HIGH_'+name if dense and name in ('Stock_Walnut','Forend_Walnut') else name
   ob=next(o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('part_name',o.name)==target) if not dense else bpy.data.objects[target]
   ev=ob.evaluated_get(dg);mesh=ev.to_mesh();mesh.calc_loop_triangles();segments=[]
   for tri in mesh.loop_triangles:
    vs=[ev.matrix_world@mesh.vertices[i].co for i in tri.vertices];hits=[]
    for a,b in zip(vs,vs[1:]+vs[:1]):
     if (a[axis]-station)*(b[axis]-station)<0:hits.append(a+(b-a)*(station-a[axis])/(b[axis]-a[axis]))
    if len(hits)==2:segments.append([[p[k]*1000 for k in projection] for p in hits])
   ev.to_mesh_clear()
   if segments:parts[name]=segments
  assert parts,title
  pts=[p for ss in parts.values() for seg in ss for p in seg];b=[[min(p[k] for p in pts),max(p[k] for p in pts)] for k in (0,1)]
  rows.append(dict(title=title,plane='XYZ'[axis],station_mm=station*1000,axes=['XYZ'[k] for k in projection],parts=parts,bounds_mm=b,size_mm=[hi-lo for lo,hi in b]))
 return rows
def main():
 game=BASE/'build/sxs.glb';source=BASE/'build/sxs.blend';out=BASE/'renders/checkpoint/sections';out.mkdir(parents=True,exist_ok=True)
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
  for row,color,width in [(h,(29,145,144),4),(g,(142,63,35),1)]:
   for ss in row['parts'].values():
    for seg in ss:d.line([xy(p) for p in seg],fill=color,width=width)
  d.text((16,598),'teal: dense/source / brown: imported GLB',font=small,fill=(25,36,31))
  d.text((16,625),' / '.join(g['parts']),font=small,fill=(25,36,31));panels.append(im)
  im.save(out/(g['title'].lower().replace(' ','-')+'.jpg'),quality=92,optimize=True)
 sheet=Image.new('RGB',(2100,650*math.ceil(len(panels)/3)),(239,240,235))
 for i,im in enumerate(panels):sheet.paste(im,(i%3*700,i//3*650))
 sheet.save(out/'sections.jpg',quality=92,optimize=True);print('SECTIONS',len(panels),out/'sections.jpg')
if __name__=='__main__':main()
