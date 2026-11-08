"""Actual transverse triangle intersections, independently plotted for review."""
import argparse,json,sys
from pathlib import Path
STATIONS=[-5.88,-5.48,-4.953,-4.42,-4.035]

def capture(source):
    import bpy
    from mathutils import Vector
    if source.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(source.resolve()))
    else:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
    bpy.context.view_layer.update();groups={}
    if source.suffix=='.blend':
        groups={'game':[bpy.data.objects['Compound hood shell']]}
        high=bpy.data.objects.get('Dense front mold')
        if high:groups['dense source']=[high]
    else:groups={'export':[o for o in bpy.context.scene.objects if o.type=='MESH']}
    result={}
    for name,obs in groups.items():
        sections=[]
        for yy in STATIONS:
            lines=[]
            for ob in obs:
                me=ob.data;me.calc_loop_triangles()
                points=[ob.matrix_world@v.co for v in me.vertices]
                for tri in me.loop_triangles:
                    if source.suffix!='.blend' and 'Paint' not in me.materials[me.polygons[tri.polygon_index].material_index].name:continue
                    ps=[points[i] for i in tri.vertices]
                    if max(p.z for p in ps)<.81 or min(p.y for p in ps)>yy or max(p.y for p in ps)<yy:continue
                    hits=[]
                    for a,c in zip(ps,ps[1:]+ps[:1]):
                        if abs(c.y-a.y)<1e-10:continue
                        t=(yy-a.y)/(c.y-a.y)
                        if 0<=t<=1:
                            p=a.lerp(c,t);hits.append([p.x,p.z])
                    if len(hits)==2:lines.append(hits)
            sections.append(dict(y_m=yy,segments=lines))
        result[name]=sections
    return dict(source=str(source),sections=result,
                scope='Actual evaluated triangle-plane intersections; no reference contours or target constants reported as measurements')

def plot(path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    data=json.loads(path.read_text());fig,axes=plt.subplots(2,3,figsize=(15,8),layout='constrained')
    for i,yy in enumerate(STATIONS):
        ax=axes.flat[i]
        for j,(name,rows) in enumerate(data['sections'].items()):
            ax.add_collection(LineCollection(rows[i]['segments'],colors=['#bd7100','#164559'][j%2],linewidths=1,label=name))
        ax.set(xlim=(-1.3,1.3),ylim=(.65,2.02),title=f'Actual section Y = {yy:.3f} m',xlabel='X (m)',ylabel='Z (m)')
        ax.set_aspect('equal');ax.grid(alpha=.2);ax.legend(fontsize=8)
    axes.flat[-1].axis('off');axes.flat[-1].text(0,.7,'Original compound mold\nNose / swept fender / axle / cowl\nActual low and dense surfaces',fontsize=13)
    fig.savefig(path.with_suffix('.png'),dpi=130);plt.close(fig)

def main():
    p=argparse.ArgumentParser();p.add_argument('--source');p.add_argument('--out',required=True);p.add_argument('--plot',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None);out=Path(a.out)
    if a.plot:plot(out)
    else:out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(capture(Path(a.source)),indent=2))
if __name__=='__main__':main()
