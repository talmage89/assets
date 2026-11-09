"""Drafting diagnostic from the serialized site manifests, not a Cycles view."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def main():
    fig,axes=plt.subplots(2,2,figsize=(18,10),layout='constrained')
    for col,seed in enumerate((101,202)):
        p=json.loads(Path(f'build/garage-{seed}.json').read_text());L,W=p['length'],p['width']
        for row,level in enumerate((0,p['levels']-1)):
            ax=axes[row,col];ax.set_aspect('equal');ax.set_facecolor('#f4f3ed')
            ax.add_patch(Rectangle((-L/2,-W/2),L,W,facecolor='#dddcd2',edgecolor='#515955',lw=1.2))
            if level==p['levels']-1:
                a,b=p['ramp_limits'];ax.add_patch(Rectangle((a,p['joint_y']),b-a,p['ramp_width'],facecolor='#b8b4a5',hatch='//',edgecolor='#858579',lw=.5))
            for s in p['stalls']:
                if s['level']!=level:continue
                if s['accessible']:color='#9ec7dc'
                else:color='#fbfaf5'
                ax.add_patch(Rectangle((s['x']-s['width']/2,s['y']-s['depth']/2),s['width'],s['depth'],facecolor=color,edgecolor='#777a74',lw=.45))
                if s['occupied']:ax.add_patch(Rectangle((s['x']-.92,s['y']-2.25),1.84,4.5,facecolor='#4e686c',edgecolor='none'))
            for route in p['paths']:
                if 'Down' in route['name']:continue
                z=[v[2] for v in route['points']]
                if min(z)>level*3.3528+.2 or max(z)<level*3.3528-.2:continue
                pts=route['points'];ax.plot([v[0] for v in pts],[v[1] for v in pts],color='#168aaf',lw=1.3,alpha=.8)
            for i,pos in enumerate(p['towers']):
                ax.add_patch(Rectangle((pos[0]-2.7,pos[1]-2.8),5.4,5.6,facecolor='#d3c28e',edgecolor='#5b604d',lw=.8))
                ax.text(pos[0],pos[1],f'S{i+1}',ha='center',va='center',size=8)
            ax.set_xlim(-L/2-8,L/2+8);ax.set_ylim(-W/2-8,W/2+5)
            ax.set_title(f"{seed} / {p['system']} / level {level+1} / {L:.2f} × {W:.2f} m",loc='left',size=11)
            ax.set_xlabel('Blender X / m');ax.set_ylabel('Blender Y / m');ax.grid(alpha=.15)
    fig.suptitle('Serialized form plans — dark rectangles are occupied car reservations; hatched area is the lower sloping roof',size=13)
    out=Path('build/plans.png');fig.savefig(out,dpi=120);plt.close(fig);print(out)


if __name__=='__main__':main()
