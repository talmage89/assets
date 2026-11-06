"""Rebuild existing library construction locally with quick form finishes.

Each invocation imports one family to avoid its standalone module names
colliding. Writes only skatepark/build/context. No accepted delivery is opened
for writing. Foliage and chain-link use the library's original scripted pixels.
"""
import argparse, sys, math, json, random
from pathlib import Path
import bpy
from mathutils import Vector, Euler
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
sys.path.insert(0,str(REPO));sys.path.insert(0,str(HERE))
import geometry as Q
from kit import model as G

def main():
    p=argparse.ArgumentParser();p.add_argument('family');p.add_argument('--out',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    a.out.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.read_factory_settings(use_empty=True);Q.palette();family=a.family
    if family=='ground':
        sys.path.insert(0,str(REPO/'ground/src'));import build as B
        B.MATS.update({k:Q.M.get(k,Q.M['Joint']) for k in ('Asphalt','Concrete','Lawn','GroundTrim','GroundIron','GroundFoliage')})
        roots=[B.road('Road_Straight_A',0),B.curb('Curb_Straight'),B.curb('Curb_DrivewayCut',cut=True),B.sidewalk('Sidewalk_A')]
        for rt in roots:B.consolidate(rt)
    elif family=='furniture':
        sys.path.insert(0,str(REPO/'street-furniture/src'));import forms as F, pieces as P
        F.LAYOUT={'Aluminum':(0,0,1,1),'litter':(0,0,1,1)}
        def own(o,rt,finish='Paint'):
            o.parent=rt;o['finish']=finish;G.apply(o);o.data.materials.clear();o.data.materials.append(Q.M.get(finish,Q.M['Steel']));return o
        F.own=own
        roots=[]
        for name,fn in [('Bench',P.bench),('Litter',P.receptacle),('BikeRack',P.rack)]:
            rt=Q.root(name,'site');fn(rt);Q.join(rt);roots.append(rt)
    elif family=='chain':
        sys.path.insert(0,str(REPO/'fences/chain-link/src'));import build as B
        from modular import Builder
        from kit.export import atlas_material
        def init(self,high,wear):
            Builder.__init__(self,'ChainLink',False,wear);self.zinc=Q.M['Zinc']
            B.mesh_tile.apply(a.out.parent/'fabric-source')
            self.fabric_mat=atlas_material('ChainLink',(a.out.parent/'fabric-source').resolve(),.5,True)
            for n in self.fabric_mat.node_tree.nodes:
                if hasattr(n,'uv_map'):n.uv_map='BakeUV'
        B.Chain.__init__=init;b=B.Chain(False,.4)
        b.section('Chain_Section');b.posts();b.gate()
        roots=[o for o in bpy.context.scene.objects if not o.parent]
        for rt in roots:rt.location=(0,0,0);Q.join(rt)
    elif family=='tree':
        sys.path.insert(0,str(REPO/'trees/src'))
        from species import MAPLE as S
        from growth import generate
        from leaves import generate as leaf_image
        from leaf_material import material
        from kit import botany
        stems,terminals,centers,assignments,masses,card_masses,tufts=generate(S.SEED,species=S)
        rt=Q.root('RedMaple','site');rng=random.Random(S.SEED+99)
        for i,stem in enumerate(stems):
            if stem.level>2:continue
            points=stem.points;radius=stem.radii
            ob=botany.sweep('Library maple stem',points,radius,Q.M['Composite'],sides=10 if stem.level<1 else 6);ob.parent=rt
        folder=a.out.parent/'leaves';path=leaf_image(folder,1024,species=S)
        leaf=material(bpy.data.images.load(str(path.resolve())),bpy.data.images.load(str((folder/'T_RedMaple_Normal.png').resolve())),bpy.data.images.load(str((folder/'T_RedMaple_ORM.png').resolve())))
        cards=botany.Cards();basis=None
        for i,pos in enumerate(centers):
            if i%3==0:
                rot=Euler((rng.random()*math.tau,rng.random()*math.tau,rng.random()*math.tau)).to_matrix();basis=[rot@Vector(v) for v in ((1,0,0),(0,1,0),(0,0,1))]
            normal=basis[i%3];mc=Vector(masses[card_masses[i]]['center'])
            if normal.dot(pos-mc)<0:normal=-normal
            cards.add(pos,normal,rng.random()*math.tau,S.CARD_SIZE*rng.uniform(.94,1.05),S.LEAF_RECTS[rng.randrange(8)],S.CROWN_CENTER,(0,0,0,0),S.NORMAL_BEND,clump_center=mc,clump_blend=S.MASS_NORMAL_BLEND)
        cards.mesh('Library maple foliage',leaf).parent=rt;Q.join(rt);roots=[rt]
    elif family=='houses':
        sys.path.insert(0,str(REPO/'houses/src'));import build as B
        from plan import load
        b=B.build(load(27,None,'builder_colonial'));roots=[o for o in bpy.context.scene.objects if not o.parent]
    elif family=='light':
        # Run the family's own game-density builder and replace source-only
        # nodes with its uniform form values before context serialization.
        import runpy
        sys.argv=['build.py','--','--quality','game','--wear','.3','--out',str(a.out.with_suffix('.blend'))]
        runpy.run_path(str(REPO/'street-light/src/build.py'),run_name='__main__')
        Q.palette()
        for ob in bpy.context.scene.objects:
            if ob.type=='MESH':
                ob.data.materials.clear();ob.data.materials.append(Q.M['Zinc'])
        roots=[o for o in bpy.context.scene.objects if not o.parent]
        for rt in roots:Q.join(rt)
    else:raise ValueError(family)
    bpy.context.view_layer.update()
    for rt in roots:rt['library_source']=family
    bpy.ops.export_scene.gltf(filepath=str(a.out.resolve()),export_format='GLB',export_extras=True,export_animations=False,export_tangents=True)
    a.out.with_suffix('.json').write_text(json.dumps(dict(family=family,source_geometry='repository scripts; quick material overrides',triangles=sum(Q.count(r) for r in roots)),indent=2))

if __name__=='__main__':main()
