"""Independent module export and side-by-side generator demonstration."""
import json,math
from pathlib import Path
import bpy
from mathutils import Vector
from geo import Assembly,root,text
from parts import wall_bay,window,cornice,column,front_door,steps
from station import overhead
from services import equipment,bollard,gear,drains
from delivery import counts,publish,consolidate


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True);objects=[];rows=[]
    specs=[('WallBay',lambda a:wall_bay(a,'WallBay',(0,0,0),4.18,3.9624)),
        ('TallSash',lambda a:window(a,'TallSash',(0,0,0))),
        ('AluminumSash',lambda a:window(a,'AluminumSash',(0,0,0),1.65,1.7,modern=True)),
        ('Cornice',lambda a:cornice(a,'Cornice',(0,0,2),4.18)),
        ('TuscanColumn',lambda a:column(a,'Tuscan',(0,0,0),7.3748,.878)),
        ('Pilaster',lambda a:column(a,'Pilaster',(0,0,0),3.4,.48,True)),
        ('FrontDoor',lambda a:front_door(a,'Door',(0,0,0))),
        ('StoneSteps',lambda a:steps(a,(0,0,0),4.2)),
        ('OverheadDoor',lambda a:overhead(a,'Overhead',0,0,0)),
        ('RoofHVAC',lambda a:equipment(a,(0,0,0))),
        ('TurnoutRack',lambda a:gear(a,'Gear',(0,0,0))),
        ('Bollard',lambda a:bollard(a,(0,0,0))),
        ('Drainage',lambda a:drains(a,(-1.5,1.5,0,2),4)),
        ('PlainFascia',lambda a:cornice(a,'ModernCap',(0,0,2),4.18,plain=True))]
    for j,(name,fn) in enumerate(specs):
        a=Assembly('Module_'+name);fn(a);meta=counts(a.root.children_recursive)
        rows.append(dict(name=name,**meta));consolidate(a);a.root.location=((j%4-1.5)*9,(j//4)*9,0)
        objects += [a.root]+list(a.root.children_recursive)
    report=publish('CivicPieces',objects);report['modules']=rows
    Path('build/modules.json').write_text(json.dumps(report,indent=2)+'\n')


def render(out,width,samples):
    from render import light,camera
    from library import place,clear
    for name in ('modules','range'):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        if name=='modules':
            source=Path('build/review/CivicPieces.glb');bpy.ops.import_scene.gltf(filepath=str(source.resolve()));target=(0,12,1);loc=(38,-43,43);lens=48
        else:
            for j,seed in enumerate((101,202,303,404)):
                place(Path('build/review')/f'Civic-{seed}.glb','Generator_'+str(seed),((j-1.5)*41,0,0))
            clear();target=(0,0,3);loc=(79,-143,63);lens=45
        light();sc=bpy.context.scene;sc.cycles.samples=samples;camera((loc,target,lens),width)
        # A physical review ground catches all module contacts, keeping the
        # same procedural sunlight and exported material response.
        from sites import ground
        a=Assembly('ReviewGround');ground(a,'ReviewConcrete',(-160,160,-130,110),'Concrete',-.035)
        sc.render.image_settings.file_format='PNG';sc.render.filepath=str((out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
