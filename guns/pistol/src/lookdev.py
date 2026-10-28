"""Original, rest-coordinate PD C9 finishes and causally located carry wear.

No reference image is loaded here. Coordinates and normals are explicit mesh
attributes so rigid-bone projection isolation and source joining preserve masks.
Fine texture and engraving are shader height, not additional game geometry.
"""
import argparse,math,sys,json
from pathlib import Path
import bpy
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT))
from kit.materials import Nodes

def inputs(n):
 a=n.node('ShaderNodeAttribute',attribute_name='FinishPosition')
 normal=n.node('ShaderNodeAttribute',attribute_name='FinishNormal')
 p=a.outputs['Vector'];v=normal.outputs['Vector']
 x,y,z=n.split(p);nx,ny,nz=n.split(v)
 return dict(p=p,normal=v,x=x,y=y,z=z,nx=nx,ny=ny,nz=nz)

def absolute(n,x):return n.math('ABSOLUTE',x)
def sub(n,a,b):return n.math('SUBTRACT',a,b)
def minimum(n,*values):
 result=values[0]
 for v in values[1:]:result=n.math('MINIMUM',result,v)
 return result

def interval(n,x,lo,hi,feather=.0004):
 return n.mul(n.ramp(x,lo-feather,lo),n.ramp(x,hi+feather,hi))

def marking(n,c,name,y0,y1,z0,z1,side):
 u=n.math('DIVIDE',sub(n,c['y'],y0),y1-y0)
 if side<0:u=sub(n,1,u)
 v=n.math('DIVIDE',sub(n,c['z'],z0),z1-z0)
 tex=n.node('ShaderNodeTexImage',extension='CLIP',interpolation='Cubic')
 tex.image=bpy.data.images.load(str(BASE/'build/markings'/f'{name}.png'),check_existing=True)
 tex.image.colorspace_settings.name='Non-Color'
 n.feed(tex.inputs['Vector'],n.combine(u,v,0))
 facing=n.ramp(n.mul(c['nx'],side),.55,.90)
 return n.mul(tex.outputs['Color'],facing)

def scratch(n,c,axis='Y',amount=1):
 # Directional contact scuffs, gated further by each material's causal zone.
 stretch=(15000,180,18000) if axis=='Y' else (15000,15000,150)
 grain=n.noise(n.vec('MULTIPLY',c['p'],stretch),1,2)
 return n.mul(n.ramp(grain,.62,.75),amount)

def finish(n,base,rough,metal,height=0,ao=1):
 n.channel('micro_ao',ao)
 mat=n.finish(base,rough,metal,height,bump=1.0)
 mat.node_tree.nodes['SURFACE'].inputs['Specular IOR Level'].default_value=.28
 return mat

def nitride(name,role,wear):
 n=Nodes(name);c=inputs(n);p=c['p'];x,y,z=c['x'],c['y'],c['z'];ax=absolute(n,x)
 grain=n.noise(p,6500,2);patch=n.noise(p,360,3)
 rough=n.add(.52,n.mul(sub(n,grain,.5),.065))
 base=n.mix(n.mul(patch,.045),(.0265,.0263,.0262),(.031,.0308,.0307),True)
 height=n.mul(sub(n,grain,.5),3e-6)
 metal=1.0
 # Perimeter exposure is restricted to holster/racking contact regions.
 shoulder=n.ramp(ax,.0096,.0122)
 edge=n.maximum(n.mul(n.band(z,.0660,.00015,.0009),shoulder),
                n.mul(n.band(z,.0401,.00010,.0006),shoulder),
                n.mul(n.band(y,.1354,.00015,.00065),n.ramp(ax,.009,.012)))
 front=n.ramp(y,.087,.124)
 rear=n.mul(n.ramp(y,-.010,-.032),n.ramp(z,.059,.065))
 contact=n.maximum(front,n.mul(rear,.45))
 breakup=n.ramp(patch,.39,.68)
 rub=n.mul(edge,contact,breakup,wear)
 carbon=n.mul(interval(n,y,.029,.036,.004),interval(n,z,.046,.065,.001),
              n.ramp(c['nx'],.2,.8),n.ramp(patch,.2,.65),wear)
 if role=='slide':
  # The 2 mm rounded shoulder is at Z=64.5..66.5, not the old
  # Z=66 band on the flat. Wear follows its exposed leading half.
  shoulder=n.mul(n.ramp(ax,.0100,.0108),n.ramp(z,.0648,.0655),
                 n.ramp(absolute(n,c['nx']),.10,.45))
  leading=n.ramp(y,.040,.070)
  nose=n.mul(n.ramp(y,.1305,.1350),n.maximum(n.ramp(ax,.0104,.0120),
             n.ramp(z,.0635,.0655),n.ramp(z,.042,.040)))
  # The crests are the outer side land, never the 1 mm-deep groove floors.
  diagonal=sub(n,y,n.mul(sub(n,z,.0417),1.97/25.1))
  phase=n.math('PINGPONG',n.add(diagonal,.030),.0015)
  crests=n.mul(n.ramp(ax,.01232,.01265),n.ramp(phase,.00115,.00140),
              n.maximum(interval(n,y,-.031,.003,.001),interval(n,y,.089,.123,.001)),
              interval(n,z,.043,.065,.001))
  # Fine directional interruption keeps contact lines coherent at 2048.
  drag=n.add(.76,n.mul(n.noise(n.vec('MULTIPLY',p,(2600,180,2200)),1,2),.24))
  rub=n.mul(n.maximum(n.mul(shoulder,leading),nose,n.mul(crests,.60)),drag,wear)
 if role=='hood':
  # Same black nitride as the slide. The old inset bands (up to 5.2 mm
  # wide) and coarse noise made a pale, blocky picture frame in the bake.
  top=n.ramp(c['nz'],.35,.85)
  tracks=n.maximum(n.ramp(x,-.00795,-.00845),n.ramp(x,.00985,.01035),
                   n.ramp(y,.06465,.06525))
  drag=n.add(.86,n.mul(n.noise(n.vec('MULTIPLY',p,(3400,160,2000)),1,2),.14))
  rub=n.mul(top,tracks,drag,wear)
  side_track=n.maximum(n.ramp(y,.0648,.06535),n.ramp(z,.0650,.0656))
  side=n.maximum(n.ramp(x,-.0080,-.0085),n.ramp(x,.00995,.01045))
  rub=n.maximum(rub,n.mul(side,side_track,drag,wear,.85))
  carbon=n.mul(n.ramp(y,.037,.0355),wear)
 elif role=='barrel':
  rub=n.mul(n.band(z,.0604,.0002,.0005),interval(n,y,.067,.133,.003),wear,.65)
  carbon=n.mul(n.ramp(y,.132,.137),n.ramp(patch,.23,.72),wear)
 elif role=='breech':
  carbon=n.mul(n.ramp(y,.028,.033),n.ramp(patch,.12,.66),wear)
  rub=n.mul(n.band(z,.048,.0003,.001),n.ramp(patch,.5,.72),wear)
 elif role=='control':
  # Finger contact polishes the exposed pad/serration crests, not its recess.
  edge=n.maximum(n.band(z,.0343,.00015,.0008),n.band(y,.0048,.0002,.0008),
                  n.band(y,.0162,.0002,.0008),n.band(z,.0044,.0001,.0007))
  rub=n.mul(edge,n.ramp(patch,.31,.63),wear)
 elif role=='release':
  # Exposed steel bevel and pressed upper pad: no cloudy noise in the face.
  perimeter=n.maximum(n.ramp(y,.0128,.01215),n.ramp(y,.0202,.02085),
                       n.ramp(z,.0048,.00415),n.ramp(z,.0152,.01585))
  pad=n.mul(n.ramp(z,.010,.0145),n.ramp(y,.016,.019),.24)
  rub=n.mul(n.maximum(perimeter,pad),n.ramp(x,-.0144,-.0150),wear)
 elif role=='sight':
  edge=n.maximum(n.band(z,.0715,.0001,.0007),n.band(y,.1258,.0002,.0006))
  rub=n.mul(edge,n.ramp(patch,.38,.72),wear,.8)
  if name.startswith('C9_Sight_Front_'):
   rub=n.mul(n.ramp(z,.07125,.07185),wear)
 elif role=='lip':
  rub=n.mul(n.maximum(n.ramp(z,.040,.044),n.band(ax,.005,.0003,.001)),wear)
  carbon=0;rough=n.add(.36,n.mul(grain,.08))
 elif role=='rail':
  rub=n.mul(n.ramp(z,.0384,.0392),wear);carbon=0
 scuff=n.mul(scratch(n,c),contact,wear,.13) if role not in ('hood','release') else 0
 base=n.mix(n.maximum(rub,scuff),base,(.14,.145,.14),True)
 rough=n.mix(rub,rough,.29);metal=n.mix(rub,metal,1)
 base=n.mix(carbon,base,(.0024,.0021,.0018),True)
 rough=n.mix(carbon,rough,.83);metal=n.mix(carbon,metal,.05)
 height=n.add(height,n.mul(scuff,-.000008),n.mul(carbon,.000006))
 if role=='slide':
  marks=n.maximum(marking(n,c,'slide-left',.005,.079,.045,.062,-1),
                  marking(n,c,'slide-right',.006,.028,.045,.062,1))
  height=n.add(height,n.mul(marks,-.00016))
  base=n.mix(n.mul(marks,.55),base,(.012,.012,.0115),True)
  rough=n.mix(marks,rough,.53)
 return finish(n,base,rough,metal,height)

def polymer(name,role,wear):
 n=Nodes(name);c=inputs(n);x,y,z=c['x'],c['y'],c['z'];ax=absolute(n,x)
 grain=n.noise(c['p'],5200,2);patch=n.noise(c['p'],170,3)
 base=(.0067,.0060,.0053)
 rough=n.add(.57,n.mul(sub(n,grain,.5),.12))
 height=n.mul(sub(n,grain,.5),8e-6)
 panel=0;lint=0;shine=0;ao=1
 if role=='frame':
  center=n.add(.0012,n.mul(sub(n,z,.008),math.tan(math.radians(22))))
  u=n.add(sub(n,y,center),.001)
  qx=sub(n,absolute(n,u),.012);qz=sub(n,absolute(n,n.add(z,.023)),.019)
  distance=sub(n,n.add(n.math('SQRT',n.add(n.mul(n.maximum(qx,0),n.maximum(qx,0)),
                n.mul(n.maximum(qz,0),n.maximum(qz,0)))),minimum(n,n.maximum(qx,qz),0)),.0028)
  panel=n.mul(n.ramp(distance,-.00055,-.0014),n.ramp(ax,.0108,.0131),
              interval(n,z,-.0475,.002,.0008))
  pattern=n.combine(u,z,0)
  warp=n.mul(sub(n,n.noise(pattern,240,2),.5),.00030)
  pattern=n.combine(n.add(u,warp),z,0)
  cells=n.voronoi(pattern,880,'DISTANCE_TO_EDGE')
  tops=n.ramp(cells,.055,.21)
  texture=n.mul(panel,tops,.00022)
  height=n.add(height,texture)
  ao=n.mix(panel,1,n.mix(tops,.88,1))
  base=n.mix(panel,base,(.0210,.0192,.0172),True)
  # Broad hand contact leaves polished pebble crowns and smooth thumb areas.
  hand=n.mul(interval(n,z,-.042,.003,.006),n.maximum(n.ramp(absolute(n,u),.005,.018),.30))
  shine=n.mul(hand,n.ramp(patch,.20,.71),wear)
  rough=n.mix(panel,rough,.76)
  rough=n.mix(n.mul(shine,n.mix(panel,1,tops)),rough,.34)
  base=n.mix(n.mul(shine,.18),base,(.0125,.0113,.0097),True)
  thumb=n.mul(interval(n,z,.003,.026,.006),interval(n,u,-.024,-.004,.006),
              n.ramp(ax,.0125,.0140),n.ramp(absolute(n,c['nx']),.45,.85),wear)
  rough=n.mix(n.mul(thumb,.72),rough,.32)
  # Palm-bearing web crowns polish along their curved surface. Keep value
  # change below 5%; the visible effect is sheen, not a pale round patch.
  web=n.mul(interval(n,y,-.040,-.012,.005),interval(n,z,.012,.034,.005),
            n.ramp(ax,.007,.012),n.ramp(absolute(n,c['nx']),.35,.80),wear)
  rough=n.mix(n.mul(web,.66),rough,.35)
  base=n.mix(n.mul(web,.045),base,(.0125,.0113,.0097),True)
  chafe=n.mul(interval(n,z,-.051,-.046,.002),n.ramp(absolute(n,u),.014,.024),
              n.ramp(patch,.40,.75),wear)
  base=n.mix(n.mul(chafe,.22),base,(.019,.016,.012),True)
  height=n.add(height,n.mul(scratch(n,c),chafe,-.000008))
  # Sparse light fibers/dust remain in sheltered texture valleys near the rim.
  valley=n.mul(panel,sub(n,1,tops),n.ramp(distance,-.010,-.002))
  fiber=n.ramp(n.noise(n.vec('MULTIPLY',pattern,(280,2600,1)),1,2),.68,.79)
  strand=n.mul(n.band(n.add(z,n.mul(n.math('SINE',n.mul(u,1500)),.00024)),
                      -.0065,.000035,.00010),interval(n,u,.007,.012,.0005))
  fiber=n.maximum(fiber,strand)
  lint=n.mul(valley,fiber,n.ramp(patch,.48,.72),wear,.75)
  base=n.mix(lint,base,(.065,.057,.044),True)
  rough=n.mix(lint,rough,.89)
  marks=n.maximum(marking(n,c,'frame-left',.052,.096,.025,.033,-1),
                  marking(n,c,'frame-right',.047,.084,.025,.032,1))
  height=n.add(height,n.mul(marks,.00014))
  base=n.mix(n.mul(marks,.23),base,(.017,.015,.012),True)
  seam=n.mul(n.band(x,0,.00003,.00009),interval(n,z,-.047,.034,.002))
  height=n.add(height,n.mul(seam,.000028))
 elif role=='magazine':
  base=(.006,.0062,.0058);rough=.53
  contact=n.maximum(n.ramp(z,.010,.037),n.ramp(z,-.042,-.053))
  scuff=n.mul(scratch(n,c,'Z'),contact,n.ramp(patch,.35,.73),wear)
  base=n.mix(n.mul(scuff,.45),base,(.038,.035,.028),True)
  rough=n.mix(n.mul(contact,wear),rough,.36)
  height=n.add(height,n.mul(scuff,-.000010))
  marks=n.maximum(marking(n,c,'magazine',-.0115,.0115,.003,.013,1),
                  marking(n,c,'magazine',-.0115,.0115,.003,.013,-1))
  height=n.add(height,n.mul(marks,-.00008))
  base=n.mix(n.mul(marks,.32),base,(.025,.026,.023),True)
 elif role=='follower':
  base=(.19,.042,.008);rough=.59
  rough=n.mix(n.ramp(z,.024,.027),rough,.43)
 elif role=='sight_dot':base=(.64,.61,.52);rough=.60
 elif role=='trigger':
  shine=n.mul(n.ramp(y,.046,.050),wear)
  rough=n.mix(shine,rough,.30)
  # Fine horizontal molded ridges carry in the normal map only.
  waves=n.math('SINE',n.mul(z,math.tau/.00115))
  height=n.add(height,n.mul(waves,.000025,n.ramp(c['ny'],.5,.9)))
 else:rough=n.mix(n.mul(patch,wear,.25),rough,.34)
 return finish(n,base,rough,0,height,ao)

def alloy(name,kind,fired,wear):
 n=Nodes(name);c=inputs(n)
 grain=n.noise(c['p'],6500,2);patch=n.noise(c['p'],550,3)
 color={'brass':(.48,.285,.075),'copper':(.46,.175,.073),'primer':(.42,.39,.31),
        'steel':(.24,.25,.25)}[kind]
 tarnish=n.mul(n.ramp(patch,.52,.77),wear,.28)
 base=n.mix(tarnish,color,tuple(v*.40 for v in color),True)
 rough=n.add(.30,n.mul(grain,.09),n.mul(tarnish,.15))
 height=n.mul(sub(n,grain,.5),2e-6)
 if fired:
  # Case coordinates run +Y from head to mouth, unchanged accepted geometry.
  soot=n.mul(n.ramp(c['y'],.0158,.0191),n.ramp(patch,.15,.69),wear)
  base=n.mix(soot,base,(.013,.010,.006),True);rough=n.mix(soot,rough,.76)
  extractor=n.mul(n.band(c['y'],.0011,.00020,.00035),n.ramp(c['nx'],.55,.85),wear)
  base=n.mix(extractor,base,(.59,.37,.12),True)
 return finish(n,base,rough,1,height)

def assign(wear):
 records={}
 for ob in [o for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o]:
  # Corner normal attribute keeps masks stable on hard bevels after joining.
  attr=ob.data.attributes.new('FinishPosition','FLOAT_VECTOR','POINT')
  attr.data.foreach_set('vector',[a for v in ob.data.vertices for a in v.co])
  normals=ob.data.attributes.new('FinishNormal','FLOAT_VECTOR','CORNER')
  normals.data.foreach_set('vector',[a for v in ob.data.corner_normals for a in v.vector])
  slots=list(ob.data.materials);roles=[]
  for index,original in enumerate(slots):
   key=original.name.removeprefix('CP_').split('.')[0]
   role=''
   if ob.name=='Frame_Grip':role='frame'
   elif ob.name.startswith('Barrel_Hood'):role='hood'
   elif ob.name.startswith(('Barrel_Tube','Crown_Land')):role='barrel'
   elif ob.name.startswith('Slide_Shell'):role='slide'
   elif ob.name.startswith('Slide_BreechFace'):role='breech'
   elif ob.name.startswith('Frame_RailInsert'):role='rail'
   elif ob.name.startswith('MagRelease'):role='release'
   elif ob.name.startswith(('SlideStop','Takedown')):role='control'
   elif ob.name.startswith('Magazine_FeedLip'):role='lip'
   elif ob.name.startswith('Magazine_Body'):role='magazine'
   elif ob.name=='Magazine_Follower':role='follower'
   elif ob.name=='Sight_FrontDot':role='sight_dot'
   elif ob.name.startswith('Sight_'):role='sight'
   elif ob.name.startswith('Trigger_Shoe'):role='trigger'
   name='C9_'+ob.name+'_'+str(index)
   if role in ('slide','hood','barrel','breech','rail','control','release','lip','sight') or key in ('nitride','darksteel'):
    mat=nitride(name,role or 'steel',wear)
   elif key in ('brass','copper','primer','steel'):mat=alloy(name,key,ob.name.startswith('Case_'),wear)
   else:mat=polymer(name,role or key,wear)
   ob.data.materials[index]=mat;roles.append(role or key)
  records[ob.name]=roles
 bpy.context.scene['finish_wear']=wear
 return records

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--source',required=True);parser.add_argument('--out',required=True);parser.add_argument('--wear',type=float,default=.72)
 a=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
 bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
 records=assign(a.wear);out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()))
 out.with_suffix('.json').write_text(json.dumps(dict(wear=a.wear,roles=records,
  coordinates='explicit rest-position and corner-normal attributes; original generated markings only'),indent=2))
 print('C9 LOOKDEV',len(records),'original material assignments',flush=True)

if __name__=='__main__':main()
