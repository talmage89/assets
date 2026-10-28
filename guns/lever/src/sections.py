"""Actual triangle/plane section cuts; dimensions are measured from intersections."""
import json
import sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import weapon as W


def extract(ob,y):
    ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh();mesh.calc_loop_triangles()
    points=[ev.matrix_world@v.co for v in mesh.vertices];segments=[]
    for tri in mesh.loop_triangles:
        vs=[points[i] for i in tri.vertices];hits=[]
        for p,q in zip(vs,vs[1:]+vs[:1]):
            if (p.y-y)*(q.y-y)<0:
                v=p+(q-p)*((y-p.y)/(q.y-p.y));hits.append([v.x*1000,v.z*1000])
        if len(hits)==2:segments.append(hits)
    ev.to_mesh_clear();return segments


def main():
    base=Path(__file__).resolve().parents[1];results={}
    definitions=[('Wrist',[-35,-5,25],['Stock','Upper_Tang','Lower_Tang']),
        ('Butt',[-220,-150],['Stock']),('Forend',[250,330,430],['Forend','Magazine_Tube','Barrel']),
        ('Receiver at gate',[148],['Receiver','Loading_Gate','Bolt_Body','Carrier_Cradle']),
        ('Band seats',[432,667],['Forend_Band','Muzzle_Band','Barrel','Magazine_Tube','Forend'])]
    for stage in ('lever','sculpt'):
        bpy.ops.wm.open_mainfile(filepath=str(base/'build'/(stage+'.blend')))
        arm=bpy.data.objects['LeverArmature'];W.pose(arm,'Idle',0);rows=[]
        for region,ys,names in definitions:
            for y in ys:
                outlines={n:extract(bpy.data.objects[n],y*.001) for n in names}
                flat=[p for segs in outlines.values() for line in segs for p in line]
                rows.append(dict(region=region,station_mm=y,parts=outlines,
                    width_mm=max(p[0] for p in flat)-min(p[0] for p in flat),
                    height_mm=max(p[1] for p in flat)-min(p[1] for p in flat)))
        results[stage]=rows
    (base/'build/sections.json').write_text(json.dumps(results,indent=2))
    print('SECTION CUTS',len(results['lever']),'game and dense-source stations')


if __name__=='__main__':main()
