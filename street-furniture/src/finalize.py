"""Use kit finalization, then give thin folded charts disjoint rectangles.

The native smart projection can fold disconnected thin returns into a chart.
Only self-overlapping charts are split; the independent kit UV audit gates the
result. No tolerance is relaxed. All other finalized geometry stays intact.
"""
import json,math,runpy,sys
from pathlib import Path
import bpy,numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import uv
from mathutils import Vector

def main():
    try:runpy.run_path(str(ROOT/'kit/finalize.py'),run_name='__main__')
    except RuntimeError as e:
        if not str(e).startswith('UV validation failed:'):raise
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o];charts=[];split=0
    for ob in obs:
        me=ob.data;me.calc_loop_triangles();groups=[list(g) for g in uv.islands(ob)];owner={li:i for i,g in enumerate(groups) for li in g};audit=uv.report([ob],2048)
        bad=set()
        for a,b,area in audit['overlap_examples']:
            ia=owner[me.loop_triangles[a].loops[0]];ib=owner[me.loop_triangles[b].loops[0]]
            if ia==ib:bad.add(ia)
        # Check every same-chart triangle pair, since examples are capped.
        per={i:[] for i in range(len(groups))}
        for t in me.loop_triangles:per[owner[t.loops[0]]].append(t)
        data=me.uv_layers['BakeUV'].data
        for i,tris in per.items():
            if i in bad:continue
            for j,a in enumerate(tris):
                aa=[tuple(data[k].uv) for k in a.loops]
                for b in tris[j+1:]:
                    bb=[tuple(data[k].uv) for k in b.loops]
                    if uv.intersection_area(aa,bb)>1e-10:bad.add(i);break
                if i in bad:break
        for i,g in enumerate(groups):
            if i in bad:
                split+=1
                for t in per[i]:
                    loops=list(t.loops);points=[data[k].uv.copy() for k in loops];charts.append((ob,loops,points))
            else:charts.append((ob,g,[data[k].uv.copy() for k in g]))
    # Greedy rows of bounding rectangles, sorted by height. Each gets a two
    # delivered-pixel guard. Shape and per-surface priority remain unchanged.
    rows=[]
    for ob,loops,pts in charts:
        lo=Vector((min(p.x for p in pts),min(p.y for p in pts)));hi=Vector((max(p.x for p in pts),max(p.y for p in pts)));span=hi-lo
        rotate=span.x>span.y
        xy=[Vector((p.y-lo.y,p.x-lo.x)) if rotate else p-lo for p in pts]
        w,h=(span.y,span.x) if rotate else (span.x,span.y)
        rows.append(dict(ob=ob,loops=loops,points=xy,w=w,h=h))
    order=sorted(range(len(rows)),key=lambda i:(-rows[i]['h'],-rows[i]['w'],i))
    def pack(factor):
        x=y=line=0;result={}
        for i in order:
            row=rows[i];w=max(1,math.ceil(row['w']*factor))+4;h=max(1,math.ceil(row['h']*factor))+4
            if w>2040:return None
            if x+w>2040:x=0;y+=line;line=0
            if y+h>1980:return None
            result[i]=(x+4,y+4);x+=w;line=max(line,h)
        return result
    low,high=0,4096
    for _ in range(28):
        mid=(low+high)/2
        if pack(mid) is None:high=mid
        else:low=mid
    positions=pack(low);assert positions
    for i,row in enumerate(rows):
        x,y=positions[i];data=row['ob'].data.uv_layers['BakeUV'].data
        for li,p in zip(row['loops'],row['points']):data[li].uv=((x+p.x*low)/2048,(y+p.y*low)/2048)
    report=uv.report(obs,2048);assert report['degenerate_uv_triangles']==0 and report['outside_triangles']==0 and report['overlap_fraction']<1e-5,report
    assert report['density_px_m']['5']>55 and report['density_px_m']['50']>75,report['density_px_m']
    report.update(repaired_folded_charts=split,rectangle_charts=len(rows),guard_pixels=2,scope=__doc__)
    Path('build/uv.json').write_text(json.dumps(report,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(Path('build/finalized.blend').resolve()))
    print('FAMILY UV',report['coverage'],report['density_px_m'],'overlap',report['overlap_fraction'],flush=True)
if __name__=='__main__':main()
