"""Rebuild existing library construction locally with quick form finishes.

Each invocation imports one family to avoid its standalone module names
colliding. Writes only skatepark/build/context. No accepted delivery is opened
for writing. Foliage and chain-link use the library's original scripted pixels.
"""
import argparse, sys, math, json, random,hashlib
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
        F.LAYOUT={'Aluminum':(0,0,1,1),'litter':(0,0,1,1)};F.M=Q.M['Paint']
        def own(o,rt,finish='Paint'):
            o.parent=rt;o['finish']=finish;G.apply(o);o.data.materials.clear();o.data.materials.append(Q.M.get({'Inside':'Black','Aluminum':'Zinc'}.get(finish,finish),Q.M['Steel']))
            for face in o.data.polygons:face.material_index=0
            return o
        F.own=own
        roots=[]
        for name,fn in [('Bench',P.bench),('Litter',P.receptacle),('BikeRack',P.rack)]:
            rt=Q.root(name,'site');fn(rt);Q.join(rt);roots.append(rt)
    elif family=='chain':
        sys.path.insert(0,str(REPO/'fences/chain-link/src'))
        import dimensions as D
        # Build at municipal height; never stretch the 4ft alpha fabric/mesh.
        for key in ('HEIGHT','RAIL_Z','LINE_TOP','TERM_TOP','CAP_TOP'):
            setattr(D,key,getattr(D,key)+.6096)
        D.LATCH_Z=.9144
        import build as B
        from modular import Builder
        from kit.export import atlas_material
        def init(self,high,wear):
            Builder.__init__(self,'ChainLink',False,wear);self.zinc=Q.M['Zinc']
            # Canonical fence atlas is built by its own unchanged pipeline.
            self.fabric_mat=atlas_material('ChainLink',(REPO/'fences/chain-link/textures/ship').resolve(),.5,True)
            for n in self.fabric_mat.node_tree.nodes:
                if hasattr(n,'uv_map'):n.uv_map='BakeUV'
        B.Chain.__init__=init;b=B.Chain(False,.4)
        b.section('Chain_Section');b.posts();b.gate()
        # Redistribute the tall gate's hardware; only the tube/fabric heights
        # change dimensionally. Wire diamonds and fitting gauges stay native.
        for ob in list(bpy.context.scene.objects):
            if ob.name.startswith('Chain hinge 1') and ob.type=='MESH':ob.location.z+=.6096
        gate=bpy.data.objects['Chain_GateBay'];leaf=bpy.data.objects['Chain_Gate']
        for s in (-1,1):
            for z in (1.50,1.75):
                ob=b.wire_tie(gate,'Municipal upper gate tie',s*(D.LEAF/2-D.RAIL_OD/2),z,False);b.reparent([ob],leaf)
        ob=b.cyl(gate,'Municipal gate middle cross rail',(-D.LEAF/2,0,.9652),(D.LEAF/2,0,.9652),D.RAIL_OD/2,12);b.reparent([ob],leaf)
        line=bpy.data.objects['Chain_Line']
        for z in (1.5,1.8):b.wire_tie(line,'Municipal high line tie',0,z,False)
        for label,opening in (('Wide',6.096),('Short',3.048)):
            length=(opening-D.GATE_PITCH)/2;rt=b.root('Chain_Infill'+label,(0,0,0))
            b.fabric(rt,'Native pitch gate infill',-length/2,length/2)
            b.cyl(rt,'Gate infill top rail',(-length/2,0,D.RAIL_Z),(length/2,0,D.RAIL_Z),D.RAIL_OD/2,12)
        roots=[o for o in bpy.context.scene.objects if not o.parent]
        for rt in roots:rt.location=(0,0,0);Q.join(rt)
    elif family=='tree':
        roots=[]
        for name in ('RedMaple','PinOak'):
            canonical=REPO/'trees/export'/f'{name}.glb'
            before=set(bpy.context.scene.objects)
            bpy.ops.import_scene.gltf(filepath=str(canonical.resolve()))
            added=set(bpy.context.scene.objects)-before
            owner=Q.root(name,'site')
            owner['stage']='imported canonical baked GLB';owner['canonical_source']=str(canonical.relative_to(REPO));owner['canonical_sha256']=hashlib.sha256(canonical.read_bytes()).hexdigest()
            for ob in added:
                if ob.parent not in added:ob.parent=owner
            roots.append(owner)
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
    bpy.ops.export_scene.gltf(filepath=str(a.out.resolve()),export_format='GLB',export_extras=True,export_animations=False,export_tangents=True,export_attributes=True,
        **(dict(export_vertex_color='NONE') if family=='tree' else {}))
    a.out.with_suffix('.json').write_text(json.dumps(dict(family=family,source_geometry='canonical delivered GLBs, including alpha-cut cards and baked maps' if family=='tree' else 'repository scripts; local context adaptation',triangles=sum(Q.count(r) for r in roots)),indent=2))

if __name__=='__main__':main()
