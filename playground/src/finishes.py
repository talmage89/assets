"""Period tints and causal surface allocation. No photographic pixels.

Tint values are linear reflectances. The same stock glTF maps are shared by
all periods; corner colors carry sun exposure and per-installation variation.
"""
import math
import numpy as np
PALETTES={
1996:dict(steel=(.018,.070,.27,1),rail=(.73,.49,.018,1),red=(.55,.028,.018,1),green=(.72,.45,.016,1),blue=(.020,.095,.35,1),yellow=(.78,.54,.025,1)),
2005:dict(steel=(.020,.105,.065,1),rail=(.43,.31,.15,1),red=(.22,.026,.040,1),green=(.035,.17,.10,1),blue=(.30,.22,.13,1),yellow=(.48,.34,.17,1)),
2013:dict(steel=(.020,.22,.20,1),rail=(.43,.50,.070,1),red=(.70,.17,.025,1),green=(.43,.50,.070,1),blue=(.028,.31,.36,1),yellow=(.61,.48,.24,1))}

def placed(ob,plan):
    import geometry as F
    codes=ob.data.attributes.get('FinishCode');tint=ob.data.color_attributes.get('Tint')
    if codes is None or tint is None:return
    age={1996:1.,2005:.55,2013:.13}[plan['year']]
    palette=PALETTES[plan['year']]
    # Parent-local positions are retained until the installed hierarchy updates.
    from uv_finish import CELLS,METAL,PLASTIC,rect_uv
    charts=ob.data.attributes.get('ChartKind');uv=ob.data.uv_layers.active
    module=str(ob.parent.get('module','')) if ob.parent else ''
    repainted=module.startswith('Post') and age>.75 and (plan['seed']+round(ob.parent.location.x*100)+round(ob.parent.location.y*100))%5==0
    if repainted:ob.parent['maintenance_repaint']=True
    mat=ob.matrix_basis
    for face in ob.data.polygons:
        key=F.FINISHES[codes.data[face.index].value];color=palette.get(key,F.COLORS.get(key,(.3,.3,.3,1)))
        chart=CELLS[charts.data[face.index].value] if charts else None
        target=chart
        q=mat@face.center
        if F.LOOK and age>.35:
            if chart=='Cast':target='Worn'
            if chart=='Coat' and module.startswith('Post') and q.z<.12:target='Worn'
            if chart=='Coat' and key=='rail' and q.z>.60 and face.normal.z>.25:target='Worn'
            if chart=='Deck' and module in ('Deck','Deck72') and face.normal.z>.9:
                root=ob.parent;world=root.matrix_basis@q
                for event in plan['modules']:
                    if not event['kind'].startswith(('Slide','Stairs','Transfer','Interdeck')):continue
                    x,y,z=event['pos']
                    eh=1.8288 if '72' in event['kind'] else .6096 if '24' in event['kind'] else 1.2192
                    if abs(world.z-eh)<.08 and math.hypot(world.x-x,world.y-y)<.43:target='WornDeck'
            if chart=='Deck' and module in ('Stairs48','Transfer24') and q.z>.38 and abs(q.x)<.25:target='WornDeck'
            if chart=='Coat' and age>.75 and not repainted and q.z>.28 and max(0,.7*face.normal.x-.5*face.normal.y+.5*face.normal.z)>.4:target='ChalkCoat'
            if chart=='Slide' and age>.75:target='OldSlide'
            if chart=='Clean' and age>.75:target='Chalk'
        if target and target!=chart:
            old=METAL.get(chart,PLASTIC.get(chart));new=METAL.get(target,PLASTIC.get(target))
            for li in face.loop_indices:
                u,v=uv.data[li].uv;u=(u-old[0])/(old[2]-old[0]);v=(v-old[1])/(old[3]-old[1]);rect_uv(uv.data[li],new,u,v)
            charts.data[face.index].value=CELLS.index(target)
        for li in face.loop_indices:
            p=mat@ob.data.vertices[ob.data.loops[li].vertex_index].co
            n=ob.data.loops[li].normal
            sun=max(0,.7*n.x-.5*n.y+.5*n.z)
            fade=age*(.035+.14*sun) if key in palette else 0
            if key in ('red','green','blue','yellow') and age>.75:fade=age*(.06+.35*sun)
            if repainted and key=='steel':fade*=.25
            c=np.array(color[:3]);c=c*(1-fade)+np.array((.34,.32,.28))*fade
            # Low splashed bases remain local; do not paint a uniform dirt band.
            if key=='steel' and ob.parent and str(ob.parent.get('module','')).startswith('Post'):
                streak=max(0,math.sin(math.atan2(p.y,p.x)*7+plan['seed']+ob.parent.location.x*3+ob.parent.location.y*7)*.6+.25)
                rust=age*math.exp(-max(0,p.z)*14)*streak*(.25 if repainted else 1)
                c=c*(1-rust)+np.array((.19,.062,.017))*rust
            if key=='zinc':c=np.ones(3)
            if target=='WornDeck':c=np.ones(3)*(.82 if age>.75 else .55)
            variation=1+.025*math.sin(p.x*13+p.y*9+plan['seed'])
            tint.data[li].color=(*np.clip(c*variation,0,1),1)
