"""Parameterized decurrent tree, botanical branchlets and procedural bark."""
import argparse,sys,random,math,json
from pathlib import Path
import bpy
from mathutils import Vector,Euler
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import model as G,botany
from kit.studio import studio_mat
from settings import *
from growth import generate
from leaves import generate as make
from leaf_material import material
from bark import material as bark_material


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--quality',default='game');p.add_argument('--wear',type=float,default=.5);p.add_argument('--seed',type=int,default=SEED)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True);sc=bpy.context.scene
    sc.unit_settings.system='METRIC';sc['quality']=args.quality;sc['stage']='summer maple / final look development'
    root=G.pivot('RedMaple',(0,0,0));root['static_root']=True
    bark=bark_material(args.wear,out.parent/'bark-source')
    alpha=bpy.data.images.load(str(make(out.parent/'leaf-source',4096).resolve()));leaf=material(alpha,bpy.data.images.load(str((out.parent/'leaf-source/T_RedMaple_Normal.png').resolve())),bpy.data.images.load(str((out.parent/'leaf-source/T_RedMaple_ORM.png').resolve())))
    (out.parent/'branchlet-atlas.json').write_text((out.parent/'leaf-source/branchlet-atlas.json').read_text())
    stems,terminals,centers,assignments,masses,card_masses,card_tufts=generate(args.seed);woody=[];geometric_stems=[];geometric_by_index={};rng=random.Random(args.seed+99)
    for k,stem in enumerate(stems):
        if stem.level==4 or (stem.level>0 and stem.nominal_radius<.0105):continue
        if stem.level>=3:
            retained=[i for i,r in enumerate(stem.radii) if r>=.0105]
            end=max(retained) if retained else 0
            if end<1:continue
            points=stem.points[:end+1];radii=stem.radii[:end+1]
        else:points=stem.points;radii=[max(.0105,r) for r in stem.radii] if stem.level>0 else stem.radii
        sides=stem.sides
        if stem.level>0:
            # Curvature, not remeshed zig-zags; keep the round cross-sections.
            count,sides={1:(12,10),2:(7,6),3:(4,4)}[stem.level]
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
        ob=botany.sweep('Stem_%03d'%k,points,radii,bark,sides=sides,phase=stem.phase,base_lobes=.07 if k==0 else 0)
        if k==0:
            for v in ob.data.vertices:
                if v.co.z<.001:v.co.z=0
        owner=ob.data.attributes.new(name='GrowthOwner',type='INT',domain='FACE')
        for value in owner.data:value.value=k
        ob['asset_set']='RedMaple';ob['growth_index']=k;ob.parent=root;woody.append(ob)
    # Union all retained >2 cm wood. No wire meshes or disconnected twig caps.
    # Authored flared sweeps retain their curved cross-sections; manifold
    # unions remove interior caps. Fine alpha twigs complete the last order.
    from wood import living_union
    wood=living_union(woody,stems,bark)
    wood.name='Trunk and branches';wood['coarse_union']=True
    from wood_uv import seams
    seams(wood,geometric_stems,stems)
    wood.parent=root;wood['asset_set']='RedMaple';wood['export_part']='Trunk and branches'
    for attr in list(wood.data.color_attributes):wood.data.color_attributes.remove(attr)
    stations=[(p,max(0,stem.level)/4,stem.phase) for stem in stems for p in stem.points]
    radii=[r for stem in stems for r in stem.radii]
    from mathutils.kdtree import KDTree
    tree=KDTree(len(stations))
    for i,(p,_,_) in enumerate(stations):tree.insert(p,i)
    tree.balance();values=[]
    maturity=wood.data.attributes.new(name='BarkMaturity',type='FLOAT',domain='POINT')
    for v in wood.data.vertices:
        _,index,_=tree.find(v.co);_,level,phase=stations[index]
        values.append((max(0,min(1,v.co.z/HEIGHT))*.65,level,phase,0))
        maturity.data[v.index].value=max(0,min(1,(radii[index]-.05)/.05))
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
        wind=(min(1,pos.z/HEIGHT),1.,stem.phase,rng.uniform(.65,1.))
        size=CARD_SIZE*rng.uniform(.94,1.05)
        cards.add(pos,normal,rng.random()*math.tau,size,LEAF_RECTS[rng.randrange(8)],CROWN_CENTER,wind,NORMAL_BEND,clump_center=mass_center,clump_blend=MASS_NORMAL_BLEND)
    foliage=cards.mesh('Summer leaf cards',leaf);foliage.parent=root;foliage['asset_set']='RedMaple';foliage['export_part']='Summer leaf cards';foliage['placeholder']=False
    foliage['normal_policy']=f'{NORMAL_BEND:.0%} bent; radial direction {1-MASS_NORMAL_BLEND:.0%} whole crown / {MASS_NORMAL_BLEND:.0%} branch mass; front oriented outward'
    graph=dict(seed=args.seed,stems=[dict(points=[list(p) for p in s.points],radii=s.radii,level=s.level,parent=s.parent,attach=s.attach,phase=s.phase,sides=s.sides,load=s.load,nominal_radius=s.nominal_radius) for s in stems],
               terminals=terminals,card_centers=cards.centers,card_widths=cards.widths,card_owners=[owners[i] for i in range(len(centers))],groups=groups,
               geometric_stems=geometric_stems,masses=masses,card_masses=card_masses,card_tufts=card_tufts,fork_height=FORK_HEIGHT,placeholder=False)
    (out.parent/'growth.json').write_text(json.dumps(graph,indent=2))
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()))
    for ob in [wood,foliage]:ob.data.calc_loop_triangles()
    print('BOTANICAL_MODEL',json.dumps({o.name:len(o.data.loop_triangles) for o in [wood,foliage]}),'cards',len(cards.faces))

if __name__=='__main__':main()
