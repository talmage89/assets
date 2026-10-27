"""Parameterized decurrent tree, botanical branchlets and procedural bark."""
import argparse,sys,random,math,json
from pathlib import Path
import bpy
from mathutils import Vector,Euler
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import model as G,botany
from kit.studio import studio_mat
from species import MAPLE,get
from growth import generate
from leaves import generate as make
from leaf_material import material
from bark import material as bark_material


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--quality',default='game');p.add_argument('--wear',type=float,default=.5);p.add_argument('--seed',type=int,default=None);p.add_argument('--species',choices=('maple','oak'),default='maple')
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);species=get(args.species);args.seed=species.SEED if args.seed is None else args.seed;out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True);sc=bpy.context.scene
    sc.unit_settings.system='METRIC';sc['quality']=args.quality;sc['stage']='summer maple / final look development' if args.species=='maple' else 'pin oak / summer look development'
    root=G.pivot(species.ASSET,(0,0,0));root['static_root']=True
    bark=bark_material(args.wear,out.parent/'bark-source',species=species)
    alpha=bpy.data.images.load(str(make(out.parent/'leaf-source',2048 if species.PLACEHOLDER else 4096,species=species).resolve()));leaf=material(alpha,bpy.data.images.load(str((out.parent/('leaf-source/T_'+species.ASSET+'_Normal.png')).resolve())),bpy.data.images.load(str((out.parent/('leaf-source/T_'+species.ASSET+'_ORM.png')).resolve())),**species.LEAF_SHADER)
    (out.parent/'branchlet-atlas.json').write_text((out.parent/'leaf-source/branchlet-atlas.json').read_text())
    stems,terminals,centers,assignments,masses,card_masses,card_tufts=generate(args.seed,species=species);woody=[];geometric_stems=[];geometric_by_index={};rng=random.Random(args.seed+99)
    for k,stem in enumerate(stems):
        if species.ARCHITECTURE=='excurrent' and stem.level<0:continue
        dead=getattr(stem,'kind','live')=='dead'
        minimum=(species.DEAD_WOOD_RADIUS if dead else species.MIN_WOOD_RADIUS) if species.ARCHITECTURE=='excurrent' else .0105
        if stem.level==4 or (stem.level>0 and stem.nominal_radius<minimum):continue
        if stem.level>=3:
            retained=[i for i,r in enumerate(stem.radii) if r>=minimum]
            end=max(retained) if retained else 0
            if end<1:continue
            points=stem.points[:end+1];radii=stem.radii[:end+1]
        else:points=stem.points;radii=[max(minimum,r) for r in stem.radii] if stem.level>0 else stem.radii
        sides=stem.sides
        if stem.level>0:
            # Curvature, not remeshed zig-zags; keep the round cross-sections.
            count,sides=(species.WOOD_RESOLUTION if species.ARCHITECTURE=='excurrent' else {1:(12,10),2:(7,6),3:(4,4)})[stem.level]
            if species.ARCHITECTURE=='excurrent' and stem.level==2 and points[0].z<7.1:count,sides=10,4
            if species.ARCHITECTURE=='excurrent' and stem.level==2 and (points[-1]-points[0]).length<1.8:count,sides=4,4
            if dead:count,sides=(5,4) if stem.parent==0 else (3,3)
            source_points=points;source_radii=radii;points=[];radii=[]
            for n in range(count):
                x=n/(count-1)*(len(source_points)-1);i=min(int(x),len(source_points)-2);t=x-i
                points.append(source_points[i].lerp(source_points[i+1],t))
                radii.append(source_radii[i]*(1-t)+source_radii[i+1]*t)
        # Anchor to the parent's retained sweep, rather than its denser
        # design curve: a few cm error can otherwise leave a 2 cm limb loose.
        if stem.level>0:
            parent=geometric_by_index[stem.parent]['points'];x=stem.attach*(len(parent)-1);j=min(int(x),len(parent)-2)
            anchor=Vector(parent[j]).lerp(Vector(parent[j+1]),x-j);delta=anchor-points[0]
            points=[p+delta*(1-i/(len(points)-1))**2 for i,p in enumerate(points)]
        record=dict(index=k,points=[list(p) for p in points],radii=radii)
        geometric_stems.append(record);geometric_by_index[k]=record
        ob=botany.sweep('Stem_%03d'%k,points,radii,bark,sides=sides,phase=stem.phase,base_lobes=getattr(species,"ROOT_LOBES",.07) if k==0 else 0)
        if k==0:
            for v in ob.data.vertices:
                if v.co.z<.001:v.co.z=0
        owner=ob.data.attributes.new(name='GrowthOwner',type='INT',domain='FACE')
        for value in owner.data:value.value=k
        ob['asset_set']=species.ASSET;ob['growth_index']=k;ob.parent=root;woody.append(ob)
    # Union all retained >2 cm wood. No wire meshes or disconnected twig caps.
    # Authored flared sweeps retain their curved cross-sections; manifold
    # unions remove interior caps. Fine alpha twigs complete the last order.
    from wood import living_union
    wood=living_union(woody,stems,bark)
    wood.name='Trunk and branches';wood['coarse_union']=True
    from wood_uv import seams
    seams(wood,geometric_stems,stems,species=species)
    wood.parent=root;wood['asset_set']=species.ASSET;wood['export_part']='Trunk and branches'
    for attr in list(wood.data.color_attributes):wood.data.color_attributes.remove(attr)
    stations=[(p,max(0,stem.level)/4,stem.phase) for stem in stems for p in stem.points]
    radii=[r for stem in stems for r in stem.radii]
    from mathutils.kdtree import KDTree
    tree=KDTree(len(stations))
    for i,(p,_,_) in enumerate(stations):tree.insert(p,i)
    tree.balance();values=[]
    maturity=wood.data.attributes.new(name='BarkMaturity',type='FLOAT',domain='POINT')
    dead_attr=wood.data.attributes.new(name='DeadWood',type='FLOAT',domain='POINT') if species.ARCHITECTURE=='excurrent' else None
    dead_stations=[getattr(s,'kind','live')=='dead' for s in stems for p in s.points]
    for v in wood.data.vertices:
        _,index,_=tree.find(v.co);_,level,phase=stations[index]
        values.append((max(0,min(1,v.co.z/species.HEIGHT))*.65,level,phase,0))
        maturity.data[v.index].value=max(0,min(1,(radii[index]-.05)/.05))
        if dead_attr:dead_attr.data[v.index].value=float(dead_stations[index])
    botany.wind_attribute(wood,values)
    owners={ci:ti for ti in terminals for ci in assignments[ti]}
    cards=botany.Cards();groups=[];basis=None
    for i,pos in enumerate(centers):
        if i%3==0:
            rotation=Euler((rng.random()*math.tau,rng.random()*math.tau,rng.random()*math.tau)).to_matrix()
            basis=[rotation@Vector(axis) for axis in [(1,0,0),(0,1,0),(0,0,1)]]
            groups.append(dict(first=i,count=3,orthogonal=True))
        stem=stems[owners[i]];normal=basis[i%3]
        mass_center=Vector(masses[card_masses[i]]['center'])
        radial=(pos-mass_center).normalized()
        if normal.dot(radial)<0:normal=-normal
        wind=(min(1,pos.z/species.HEIGHT),1.,stem.phase,rng.uniform(.65,1.))
        size=species.CARD_SIZE*rng.uniform(*getattr(species,"CARD_SCALE",(.94,1.05)))
        normal_center=mass_center
        if species.ARCHITECTURE=='excurrent':
            # Elliptical tier normals: a shallow bough has a lit upper surface
            # and shaded underside, not the shading of a spherical pompon.
            d=pos-mass_center;az=math.radians(masses[card_masses[i]]['azimuth'])
            out_axis=Vector((math.cos(az),math.sin(az),0));side_axis=Vector((-out_axis.y,out_axis.x,0))
            rx,ry,rz=masses[card_masses[i]]['radii']
            field=out_axis*d.dot(out_axis)/rx+side_axis*d.dot(side_axis)/ry+Vector((0,0,d.z/rz))
            normal_center=pos-field
        mass_blend=species.NORMAL_MASS_BLEND_UPPER if species.ARCHITECTURE=='excurrent' and pos.z>9 else species.MASS_NORMAL_BLEND
        cards.add(pos,normal,rng.random()*math.tau,size,species.LEAF_RECTS[rng.randrange(len(species.LEAF_RECTS))],species.CROWN_CENTER,wind,species.NORMAL_BEND,clump_center=normal_center,clump_blend=mass_blend)
    foliage=cards.mesh('Summer leaf cards',leaf);foliage.parent=root;foliage['asset_set']=species.ASSET;foliage['export_part']='Summer leaf cards';foliage['placeholder']=species.PLACEHOLDER
    foliage['normal_policy']=f'{species.NORMAL_BEND:.0%} bent; radial direction {1-species.MASS_NORMAL_BLEND:.0%} whole crown / {species.MASS_NORMAL_BLEND:.0%} branch mass; front oriented outward'
    graph=dict(seed=args.seed,stems=[dict(points=[list(p) for p in s.points],radii=s.radii,level=s.level,parent=s.parent,attach=s.attach,phase=s.phase,sides=s.sides,load=s.load,nominal_radius=s.nominal_radius) for s in stems],
               terminals=terminals,card_centers=cards.centers,card_widths=cards.widths,card_owners=[owners[i] for i in range(len(centers))],groups=groups,
               geometric_stems=geometric_stems,masses=masses,card_masses=card_masses,card_tufts=card_tufts,fork_height=species.FORK_HEIGHT,placeholder=species.PLACEHOLDER)
    if species.ARCHITECTURE=='excurrent':graph['stem_kinds']=[getattr(s,'kind','live') for s in stems]
    (out.parent/'growth.json').write_text(json.dumps(graph,indent=2))
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()))
    for ob in [wood,foliage]:ob.data.calc_loop_triangles()
    print('BOTANICAL_MODEL',json.dumps({o.name:len(o.data.loop_triangles) for o in [wood,foliage]}),'cards',len(cards.faces))

if __name__=='__main__':main()
