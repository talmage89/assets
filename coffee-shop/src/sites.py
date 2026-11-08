"""Three seeded contexts using read-only library deliveries and host builders.

Sites are separate, reviewable exports; shop counts exclude the surrounding
town. All positions use the cafe front-center datum, meters, -Y street front.
"""
import argparse,json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
import bpy
from mathutils import Vector
from kit import model,tiling
import geometry as G
from package import externalize,bundle
from plan import PROOFS
CACHE={};M={}

def instance(path,name,loc,yaw=0,scale=1):
    path=Path(path).resolve();key=str(path)
    if key not in CACHE:
        before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=key);obs=set(bpy.context.scene.objects)-before
        rt=G.root('TemplateContext_'+path.stem)
        for o in obs:
            if o.parent not in obs:o.parent=rt
        CACHE[key]=rt
    ob=G.clone(CACHE[key],name,loc,yaw=yaw);ob.scale=(scale,)*3;return ob

def slab(name,rect,z,role='Concrete',thick=.12):
    x0,x1,y0,y1=rect;ob=model.box(name,((x0+x1)/2,(y0+y1)/2,z-thick/2),(x1-x0,y1-y0,thick),M[role],0);tiling.world_uv(ob,6.096 if role=='Asphalt' else 3.048);return ob

def paint(a,b,width=.09,center=False):
    a,b=Vector(a),Vector(b);ob=model.box('Worn parking paint',(a+b)/2,(width,.002,(b-a).length),M['YellowPaint'] if center else M['Paint'],0);ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();tiling.world_uv(ob,1);return ob

def island(x,y,w,d,z):
    slab('Island concrete curb',(x-w/2,x+w/2,y-d/2,y+d/2),z+.14)
    slab('Island soil',(x-w/2+.15,x+w/2-.15,y-d/2+.15,y+d/2-.15),z+.148,'Lawn',.03)
    instance(REPO/'trees/export/RedMaple.glb','Island maple',(x,y,z+.15),31,.46)

def car(i,x,y,z,yaw=0):
    key=('AlderH120','AlderC150','AlderX220')[i%3]
    rt=instance(REPO/f'cars/export/{key}.glb','Parked '+key,(x,y,z),yaw)
    colors=((.18,.025,.018),(.055,.07,.065),(.42,.38,.26),(.024,.07,.09))
    for ob in rt.children_recursive:
        if ob.type!='MESH':continue
        for slot in ob.material_slots:
            m=slot.material
            if not m or not m.use_nodes:continue
            bs=m.node_tree.nodes.get('Principled BSDF')
            if not bs:continue
            if 'Lamp' in m.name or 'lamp' in m.name:
                bs.inputs['Emission Strength'].default_value=0
            if 'Paint' in m.name:
                name='Parked_'+key+'_Paint_'+str(i%4);ma=bpy.data.materials.get(name)
                if ma is None:
                    ma=m.copy();ma.name=name;p=ma.node_tree.nodes.get('Principled BSDF')
                    for link in list(p.inputs['Base Color'].links):ma.node_tree.links.remove(link)
                    p.inputs['Base Color'].default_value=(*colors[i%4],1)
                slot.link='OBJECT';slot.material=ma
    return rt

def street(y,z,length=180,entries=(),width=10):
    slab('Public two-way street',(-length/2,length/2,y-width,y),z,'Asphalt')
    slab('Far public walk',(-length/2,length/2,y-width-3,y-width),z+.1524)
    for x in range(-80,81,6):paint((x,y-width/2,z+.002),(x+2.8,y-width/2,z+.002),.09,True)
    for yy in (y,y-width):
        cuts=sorted({-length/2,length/2,*[x+s*3.048 for x in entries for s in (-1,1)]}) if yy==y else [-length/2,length/2]
        for a,b in zip(cuts,cuts[1:]):
            if yy==y and any(abs((a+b)/2-x)<3.048 for x in entries):continue
            slab('Public curb',(a,b,yy-.08,yy+.08),z+.1524)

def downtown(p):
    z=-.1524;curb=-p['walk']-.15;street(curb,z,width=14)
    # Contiguous party walls on both sides, with occupied ground-floor rooms.
    left=4.572;right=4.572
    for j in range(4):
        wl=7.3152;wr=8.5344
        instance('build/hosts/downtown-left.glb',f'West party-wall tenant {j}',(-left-wl/2,0,0));left+=wl
        instance('build/hosts/downtown-right.glb',f'East party-wall tenant {j}',(right+wr/2,0,0));right+=wr
    for j in range(-5,6):
        instance('build/hosts/downtown-opposite.glb',f'Across Main Street tenant {j}',(j*8.5344,curb-17,0),180)
    # Continue the accepted slab's pours laterally, without buried duplicates.
    pits=(-21,-12,13,24);py=curb+1
    for a,b in ((-80,-p['width']/2-2.3),(p['width']/2+2.8,80)):
        xs=sorted({a,b,*[x+s*.69 for x in pits for s in (-1,1) if a<x+s*.69<b]});ys=(-p['walk'],py-.69,py+.69,0)
        for xa,xb in zip(xs,xs[1:]):
            for ya,yb in zip(ys,ys[1:]):
                if any(abs((xa+xb)/2-x)<.69 and abs((ya+yb)/2-py)<.69 for x in pits):continue
                slab('Main Street continuous walk',(xa,xb,ya,yb),0)
    for i,x in enumerate((-21,-12,13,24)):
        instance(REPO/'street-furniture/export/MeterTwin.gltf','Curb meter',(x,curb+.55,0))
        instance(REPO/'street-light/export/StreetLight.glb','Main Street light',(x+2,curb+.75,0),0)
        # Original grate geometry surrounds the actual trunk opening.
        b=G.Batch('Tree grate '+str(i));b.box((x,curb+1,-.06),(1.38,1.38,.04),'soil')
        for k in range(12):
            for s in (-1,1):b.box((x+s*(.28+k*.035),curb+1.0,-.008),(.018,1.32,.016),'black')
        b.finish();instance(REPO/'trees/export/RedMaple.glb','Main Street tree',(x,curb+1.0,0),i*67,.37)
        instance('build/hosts/downtown-opposite.glb','Rear block tenant '+str(i),(x,44,0))
    for i,x in enumerate((-21,-5.8,8.0,25)):
        car(i,x,curb-1.32,z,90)
        for xx in (x-3.2,x+3.2):paint((xx,curb-.20,z+.003),(xx,curb-2.35,z+.003),.07)
    for i,x in enumerate((-18,-4,18)):car(i+1,x,curb-12.5,z,-90)
    instance(REPO/'street-furniture/export/Bench.gltf','Main Street bench',(-10,-3.5,0))
    instance(REPO/'street-furniture/export/NewsDaily.gltf','Daily newspaper box',(9,-4.4,0),-8)
    return dict(type='mid-block Main Street',street_width_m=14,party_wall_neighbors=8,opposite_storefronts=11)

def parking(p,pad=False):
    z=0;edge=-p['walk']-.15
    lot=(-18,39,-32,25) if not pad else (-20,19,-29,20)
    # Front parking + aisle, west side drive, rear service court. Paving ends
    # at the building/walk interfaces, rather than running through the room.
    slab('Customer lot front',(lot[0],lot[1],lot[2],edge),z,'Asphalt')
    slab('West side drive',(lot[0],-p['width']/2-2.3,edge,lot[3]),z,'Asphalt')
    slab('Rear service court',(-p['width']/2-2.3,lot[1],p['depth'],lot[3]),z,'Asphalt')
    if pad:slab('East service drive',(11.2,lot[1],edge,lot[3]),z,'Asphalt')
    else:
        instance('build/hosts/strip-neighbors.glb','Occupied strip tenants',(0,0,0))
        slab('Continuous tenant walk',(p['width']/2+2.8,39,edge,0),.1524)
    stalls=[]
    for row,cy in enumerate((edge-3.0,edge-16.3)):
        for j in range(6 if pad else 13):
            x=-5+j*2.74
            if row==0 and (-3<x<2):continue  # pedestrian crossing/accessible approach
            if pad and x>6.3:continue
            stalls.append((x,cy))
            for xx in (x-1.37,x+1.37):paint((xx,cy-2.7,.003),(xx,cy+2.7,.003))
            slab('Wheel stop',(x-.85,x+.85,cy+(1.9 if row==0 else -1.9),cy+(2.06 if row==0 else -1.74)),.11)
            if (j+row)%3!=1:car(j+row,x,cy,0,0 if row==0 else 180)
    # Drive aisle and a clear raised pedestrian landing connect to the street.
    for yy in (edge-5.9,edge-10.5):paint((-2.3,yy,.003),(.3,yy,.003),.30)
    for xx in ((-16,35) if not pad else (-17,16.5)):
        # The pad's east island sits by the walk approach, clear of the
        # cross-lot photographic sight line and the accepted side patio.
        iy=edge-10.5 if not pad else (-6.5 if xx>0 else -11.0)
        island(xx,iy,2.5,6,0)
        instance(REPO/'street-light/export/StreetLight.glb','Parking light',(xx,iy,.15),90)
    if pad:
        # Walk-up use, no vehicle queue through the accepted side patio.
        b=G.Batch('Walkup menu carrier');b.box((6.0,4.62,1.30),(.16,.055,.7),'black');b.panel(6.,4.584,1.30,.60,.62,'menu0');b.finish()
    # Original service enclosure, blocked CMU walls and slatted gate leaves.
    ex=-10.5;ey=14.5 if pad else 22.0;b=G.Batch('Service dumpster enclosure')
    for xx in (ex-1.8,ex+1.8):b.box((xx,ey,1.0),(.16,3.2,2.0),'wall')
    b.box((ex,ey+1.52,1.0),(3.6,.16,2.0),'wall')
    for j in range(20):b.box((ex-1.7+j*.18,ey-1.56,1.0),(.14,.04,1.80),'forest')
    b.box((ex,ey,.70),(2.3,1.5,1.35),'forest');b.box((ex,ey,1.42),(2.40,1.6,.09),'black');b.finish()
    entries=(lot[0]+3.5,lot[1]-3.5);street(lot[2]-3.0,0,entries=entries)
    xs=sorted({lot[0],lot[1],*[x+s*3.048 for x in entries for s in (-1,1)]})
    for a,b in zip(xs,xs[1:]):
        if any(abs((a+b)/2-x)<3.048 for x in entries):
            slab('Open public driveway apron',(a,b,lot[2]-3,lot[2]),0,'Concrete')
        else:slab('Public frontage sidewalk',(a,b,lot[2]-3,lot[2]),.1524)
    # 1:12 approach from parking to the accepted raised cafe through walk.
    vs=[(-2.15,edge-1.8288,0),(-.55,edge-1.8288,0),(-.55,edge,.1524),(-2.15,edge,.1524)]
    ob=model.mesh('Cafe parking approach ramp',vs,[(0,1,2,3)],M['Concrete']);tiling.world_uv(ob,3.048)
    # Houses beyond the opposite curb give the lot a town address.
    for i in range(5):
        instance(REPO/'houses/export/HearthfieldRanch-11.gltf','Beyond frontage house '+str(i),(-35+i*20,lot[2]-26,0),180)
        instance(REPO/'trees/export/RedMaple.glb','Frontage tree '+str(i),(-31+i*20,lot[2]-16,0),i*77,.65)
    for i in range(5):instance(REPO/'trees/export/RedMaple.glb','Rear landscape tree '+str(i),(-22+i*14,lot[3]+5,0),i*49,.70)
    # Close the view beyond the parcel with a neighborhood street and the
    # library's houses. A flat lawn horizon is not a believable town edge.
    back=lot[3]+13
    slab('Rear neighborhood street',(-100,100,back,back+7),0,'Asphalt')
    slab('Rear neighborhood walk',(-100,100,back+7,back+9),.1524)
    for i in range(6):
        filename='HearthfieldRanch-11.gltf' if i%2 else 'HearthfieldCape-34.gltf'
        instance(REPO/'houses/export'/filename,'Rear neighborhood house '+str(i),(-44+i*19,back+16,0))
    if pad:
        # The oblique east hero looks northwest past the west drive. Close
        # that sightline with a real side street, walks and facing neighbors.
        slab('West neighborhood street',(-38,-30,-120,150),0,'Asphalt')
        slab('West street near walk',(-30,-27.5,-120,150),.1524)
        slab('West street far walk',(-40.5,-38,-120,150),.1524)
        for yy in range(-100,130,6):paint((-34,yy,.003),(-34,yy+2.8,.003),.09,True)
        for i,yy in enumerate(range(-75,140,18)):
            filename='HearthfieldRanch-11.gltf' if i%2 else 'HearthfieldCape-34.gltf'
            instance(REPO/'houses/export'/filename,'West street neighbor '+str(i),(-49,yy,0),90)
            instance(REPO/'trees/export/RedMaple.glb','West street tree '+str(i),(-42,yy+6,0),i*43,.49)
    return dict(type='converted bank pad / walk-up' if pad else 'strip-center end cap',lot_bounds_m=lot,stall_count=len(stalls),minimum_design_aisle_m=6.096,drive_through=False)

def build(seed,kind):
    bpy.ops.wm.read_factory_settings(use_empty=True);CACHE.clear();M.clear();G.palette()
    p=json.loads(Path(f'build/shops/{seed}.json').read_text())
    for role in ('Concrete','Asphalt','Lawn'):M[role]=tiling.material(role,REPO/'ground/textures/ship')
    M['Paint']=M['Concrete']
    M['YellowPaint']=bpy.data.materials.new('Faded road center paint');M['YellowPaint'].use_nodes=True;bs=M['YellowPaint'].node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.55,.32,.025,1);bs.inputs['Roughness'].default_value=.90
    # Original asphalt stays byte-identical; a stock scalar tint represents
    # this darker wearing course and retains its roughness/microstructure.
    mat=M['Asphalt'];nodes=mat.node_tree.nodes;links=mat.node_tree.links;bs=nodes.get('Principled BSDF');mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(.40,.41,.42,1)
    src=bs.inputs['Base Color'].links[0].from_socket;links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bs.inputs['Base Color'])
    # Keep the cafe's authored node names/sockets intact inside the site.
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(Path(f'export/CoffeeShop-{seed}.gltf').resolve()));obs=set(bpy.context.scene.objects)-before
    for ob in obs:
        if ob.parent not in obs:ob.location.y+=p['depth']/2
    # Soil reaches the paving, rather than leaving a light/air gap beneath
    # the finite road boxes. Main Street's roadway is 152.4 mm below its walk.
    land_z=-.1574 if kind=='downtown' else -.005
    slab('District ground',(-1000,1000,-1000,1000),land_z,'Lawn')
    info=downtown(p) if kind=='downtown' else parking(p,kind=='pad')
    for rt in CACHE.values():
        for ob in reversed(G.descendants(rt)):bpy.data.objects.remove(ob,do_unlink=True)
    bpy.context.view_layer.update();tri=sum(sum(len(f.vertices)-2 for f in ob.data.polygons) for ob in bpy.context.scene.objects if ob.type=='MESH')
    root=G.root('CoffeeSite_'+str(seed),seed=seed,front_datum=True)
    for ob in list(bpy.context.scene.objects):
        if ob!=root and ob.parent is None:ob.parent=root
    path=Path(f'build/sites/{seed}.glb');path.parent.mkdir(parents=True,exist_ok=True);tiling.export(path)
    # MikkTSpace can straddle the final four-decimal rounding boundary at
    # three imported car corners. Preserve accepted values only after exact
    # position/normal/UV guards and the kit's one-rounding-step limit.
    from kit.gltf import stabilize_tangents,GLB
    import numpy as np
    raw=GLB(path);anchors=[]
    for old in json.loads((HERE/'context_tangents.json').read_text())[str(seed)]:
        found=[]
        for mi,mesh in enumerate(raw.json['meshes']):
            if old['primitive']>=len(mesh['primitives']):continue
            pr=mesh['primitives'][old['primitive']];attrs=pr['attributes'];vi=old['vertex']
            if raw.json['accessors'][attrs['POSITION']]['count']<=vi:continue
            if all(np.array_equal(raw.accessor(attrs[key])[vi],np.asarray(old[field],dtype=np.float32)) for field,key in (('position','POSITION'),('normal','NORMAL'),('uv','TEXCOORD_0'))):found.append(dict(old,mesh=mi))
        assert found,('Missing unchanged context tangent signature',seed,old)
        anchors.extend(found)
    stabilize_tangents(path,anchors)
    meta=externalize(path,Path(f'export/sites/CoffeeSite-{seed}.gltf'))
    info.update(seed=seed,triangles=tri,shop_triangles=p['triangles'],**meta);info['bundle_sha256']=bundle(f'export/sites/CoffeeSite-{seed}.gltf');path.with_suffix('.json').write_text(json.dumps(info,indent=2)+'\n');print('SITE',seed,tri,flush=True)

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--seeds',default='117,228,339');a=a.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    for seed,kind in PROOFS:
        if str(seed) in a.seeds.split(','):build(seed,kind)
    # Old extracted aliases are rebuildable and must not become a second
    # resource allocation beside the canonical read-only shipping files.
    used=set()
    for docpath in Path('export').rglob('*.gltf'):
        doc=json.loads(docpath.read_text())
        used.update((docpath.parent/im['uri']).resolve() for im in doc.get('images',[]) if 'uri' in im)
    for path in Path('export/textures').glob('*.png'):
        if path.resolve() not in used:path.unlink()
