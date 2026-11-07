"""Native shed construction in a private checkpoint cache; accepted files read-only."""
import sys,argparse,json
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
sys.path[:0]=[str(REPO),str(HERE)]
import geometry as Q


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True);Q.palette()
    sys.path.insert(0,str(REPO/'shed/src'))
    import build as B
    from types import SimpleNamespace
    b=B.Shed(SimpleNamespace(quality='game',wear=.6))
    B.floor(b);B.walls(b);B.doors(b);B.roof(b)
    # Tab cuts belong in the later normal bake. Keep full gauged, overlapping
    # courses at the checkpoint instead of paying for every interior tab end.
    for ob in list(bpy.context.scene.objects):
        if ob.name.startswith('Shingle tab'):bpy.data.objects.remove(ob,do_unlink=True)
    for sign in (-1,1):
        for row in range(12):
            xa=B.RX-row*B.RX/12;xb=max(0,xa-B.RX/12-.016);base=.017+row*.001
            pts=[(sign*xb,B.RIDGE-xb*B.PITCH+base),(sign*xa,B.RIDGE-xa*B.PITCH+base),
                 (sign*xa,B.RIDGE-xa*B.PITCH+base-.003),(sign*xb,B.RIDGE-xb*B.PITCH+base-.003)]
            b.add(Q.G.profile('Checkpoint lapped shingle course',pts,-B.RY,B.RY,b.roof,'Y'))
    # Keep all native thicknesses, framing, fasteners, shingles and pivots;
    # replace only the not-yet-baked procedural source finishes.
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH':continue
        names=[ma.name.lower() if ma else '' for ma in ob.data.materials]
        mapped=[]
        for n in names:
            mat='OldWood'
            if 'shingle' in n or 'felt' in n:mat='Roof'
            elif 'white' in n:mat='White'
            elif 'sage' in n or 'door' in n:mat='Green'
            elif 'zinc' in n or 'galv' in n:mat='Zinc'
            elif 'hardware' in n:mat='Steel'
            elif 'glass' in n:mat='Glass'
            mapped.append(Q.M[mat])
        ids=[p.material_index for p in ob.data.polygons];ob.data.materials.clear()
        for ma in mapped:ob.data.materials.append(ma)
        for p,i in zip(ob.data.polygons,ids):p.material_index=i
        Q.own(ob,ob.parent)
    for rt in [b.root]+[o for o in b.root.children_recursive if o.get('pivot_axis')]:Q.join(rt)
    b.root.name='NativeShed';b.root['library_source']='shed/src/build.py; game-density construction'
    bpy.context.view_layer.update()
    p=Path('build/context');p.mkdir(parents=True,exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=str((p/'shed.glb').resolve()),export_format='GLB',export_extras=True,export_animations=False)
    (p/'shed.json').write_text(json.dumps(dict(triangles=Q.count(b.root),source='shed/src/build.py'),indent=2))


if __name__=='__main__':main()
