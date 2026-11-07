"""Branch-first vegetables using the library's shared botanical sweeps/cards.

Each blade has its own petiole, cup and droop. Crop rules are family-local;
seed, stage and morphology are explicit. No external geometry or texture.
"""
import math,random
import bpy
from mathutils import Vector
from kit import botany,tiling
import geometry as Q
from atlas import rect,SPECIES,flower_rect

LEAF=None


def along(axis,t):
    """Centreline attachment, shared by every daughter/leaf/fruit on that axis."""
    t=max(0,min(1,t))*(len(axis)-1);j=min(len(axis)-2,int(t))
    return Vector(axis[j]).lerp(Vector(axis[j+1]),t-j)


def material(folder):
    global LEAF
    LEAF=tiling.material('GardenPlants',folder,alpha=True)
    LEAF.use_backface_culling=False
    LEAF.alpha_threshold=.45
    bs=LEAF.node_tree.nodes.get('Principled BSDF');bs.inputs['Specular IOR Level'].default_value=.18
    bs.inputs['Transmission Weight'].default_value=.12;bs.inputs['IOR'].default_value=1.35
    LEAF['leaf_response']='two-sided rough thin sheet; glTF transmission .12, no painted lighting'
    return LEAF


class Plant:
    def __init__(self,species,stage,seed,support_radius=.0125,field=False):
        self.sp=species;self.stage=stage;self.rng=random.Random(seed);self.cards=botany.Cards()
        self.field=field
        self.support_radius=support_radius
        self.root=Q.root(f'{species}_{stage:.2f}_{seed}','plant')
        self.root['species']=species;self.root['stage_fraction']=stage;self.root['seed']=seed
        self.attachments=[];self.blades=[]

    def stem(self,pts,r=.004,sides=5):
        pts=list(map(Vector,pts))
        if self.field:
            sides=min(sides,4 if r>.008 else 3)
            if len(pts)==3 and r<.005:pts=[pts[0],pts[-1]]
        ob=botany.sweep('Rooted '+self.sp+' axis',pts,[r*(1-.7*i/(len(pts)-1)) for i in range(len(pts))],Q.M['Stem'],sides)
        Q.own(ob,self.root);return pts

    def leaf(self,base,direction,length,width,cup=.06,droop=.24,rows=3,cols=2):
        if self.field:
            if self.sp=='corn':rows=6;cols=2
            elif self.sp=='squash':rows=4;cols=3
            elif self.sp in ('lettuce','kale'):rows=3;cols=2
            else:rows=2;cols=2
        length*=self.rng.uniform(.90,1.08);width*=self.rng.uniform(.86,1.08)
        cup*=self.rng.uniform(.8,1.2);droop*=self.rng.uniform(.85,1.15)
        base=Vector(base);axis=Vector(direction).normalized()
        # Continue the petiole into the retained-alpha margin. A transparent
        # card border must not leave the visible blade floating off its stalk.
        # The rachis enters the retained alpha; fine petiole relief is in the tile.
        side=axis.cross(Vector((0,0,1)))
        if side.length<.01:side=Vector((1,0,0))
        side.normalize();normal=side.cross(axis).normalized()
        if normal.z<0:normal=-normal
        roll=self.rng.uniform(-.65,.65) if self.sp not in ('corn','weed') else self.rng.uniform(-.42,.42)
        side,normal=side*math.cos(roll)+normal*math.sin(roll),normal*math.cos(roll)-side*math.sin(roll)
        grid=[]
        # Texture outline begins 2.5% above grid base. Rooted petiole extends
        # into that margin, so retained alpha begins on the stalk surface.
        for j in range(rows):
            t=j/(rows-1);row=[]
            for k in range(cols):
                x=k/(cols-1)*2-1
                corr=.012*math.sin(t*31+x*4) if self.sp in ('kale','lettuce') else 0
                p=base+axis*(length*t)+side*(x*width/2)+normal*(length*cup*x*x*math.sin(math.pi*t)+corr)
                p.z-=length*droop*t*t
                row.append(p)
            grid.append(row)
        old=base.z<.30 and self.rng.random()<.35
        # The new heart of a lettuce remains green; senescence belongs to
        # the older outside whorl. Keep the seed stream independent of this mask.
        old=old and (self.sp!='lettuce' or base.z<.044*self.stage**1.25)
        self.cards.add_grid(grid,rect(self.sp,old=old),(min(1,max(0,base.z/2)),.75,self.rng.random(),.8))
        self.blades.append(dict(base=list(base),length_m=length,width_m=width))

    def stalk_leaf(self,start,az,reach,z,length,width,**kw):
        start=Vector(start);d=Vector((math.cos(az),math.sin(az),z))
        end=start if self.field else start+d*reach
        if not self.field:self.stem([start,start.lerp(end,.5)+Vector((0,0,.012)),end],.0025*self.stage,4)
        self.leaf(end,d,length,width,**kw)
        return end

    def tomato(self):
        s=self.stage;h=1.72*s**1.25;axis=self.stem([(0,0,0),(.025*s,-.01*s,h*.3),(-.03*s,.025*s,h*.65),(.04*s,.01*s,h)],.009*s,7)
        leaders=[axis]
        if s>.7:
            for j in range(4):
                base=along(axis,.12+j*.09);a=j*2.399+.5;tip=Vector((math.cos(a)*.31*s,math.sin(a)*.31*s,h*self.rng.uniform(.75,.98)))
                leaders.append(self.stem([base,base.lerp(tip,.4)+Vector((0,0,.025)),tip],.006*s,6))
        nodes=max(3,round(36*s))
        for j in range(nodes):
            axis=leaders[j%len(leaders)];n=math.ceil((nodes-j%len(leaders))/len(leaders))
            t=.15+.76*(j//len(leaders))/max(1,n-1)+self.rng.uniform(-.025,.025)*s;base=along(axis,t);az=j*2.399+.4+self.rng.uniform(-.25,.25)
            out=Vector((math.cos(az),math.sin(az),.30));reach=(.29+.18*math.sin(t*math.pi))*s
            tip=base+out*reach;rachis=self.stem([base,base.lerp(tip,.5)+Vector((0,0,.025*s)),tip],.0035*s,4)
            side=Vector((-out.y,out.x,0))
            for k in range(4):
                tt=.16+k*.21;node=along(rachis,tt)
                for sign in (-1,1):
                    v=(out*.4+side*sign+Vector((0,0,self.rng.uniform(-.10,.9)))).normalized()
                    end=node;# Leaflet petiole is the connected base of the blade.
                    self.leaf(end,v,(.19-.018*k)*s,.095*s,droop=.48,rows=3)
            self.leaf(tip,out,.20*s,.095*s,droop=.42,rows=3)
            if s>.7 and j%2==0:
                # Supplemental daughter compound: nine original atlas leaflets
                # overlap the modeled compound and screen the leader's interior.
                az2=az+.8;v=Vector((math.cos(az2),math.sin(az2),.12));side2=Vector((-v.y,v.x,0))
                base2=base;rows=3 if self.field else 4;cols=2 if self.field else 3;grid=[]
                for jj in range(rows):
                    tt=jj/(rows-1);row=[]
                    for kk in range(cols):
                        u=kk/(cols-1)*2-1
                        p=base2+v*(.52*s*tt)+side2*(u*.58*s/2)+Vector((0,0,-.16*s*tt*tt+.02*s*u*u*math.sin(math.pi*tt)))
                        row.append(p)
                    grid.append(row)
                self.cards.add_grid(grid,(.753,.503,.997,.747),(.5,.8,self.rng.random(),.8))
            if s>.7 and j in (2,4,7,10,13,16):
                fruitstem=base+out*.12*s-Vector((0,0,.07*s));self.stem([base,fruitstem],.002*s,4)
                for k in range(3):
                    p=fruitstem+side*(k-.5)*.075*s-Vector((0,0,.045*s));self.stem([fruitstem,p],.0016,4)
                    Q.sphere('Hanging tomato berry',p,.037*s,self.root,('Fruit' if (j+k)%3==0 else 'Turning' if (j+k)%3==1 else 'Unripe'),scale=(1,1,.85),segments=8 if self.field else 10,rings=4)
        if s>.7:
            for j,axis in enumerate(leaders):
                at=along(axis,.97);az=j*2.399;v=Vector((math.cos(az),math.sin(az),.6))
                for sign in (-1,0,1):self.leaf(at,v+Vector((-.45*sign,.32*sign,.15)),.12*s,.065*s,droop=.3,rows=3)
        self.root['architecture']='five leaders; 36 modeled nine-leaflet compounds plus 18 overlapping nine-leaflet branchlet cards; terminal leaves and six green-to-red trusses'

    def pepper(self):
        s=self.stage;h=.76*s**1.25;self.stem([(0,0,0),(0,0,h*.47)],.007*s,6)
        for b in range(max(1,round(3*s))):
            az=b*2.1;d=Vector((math.cos(az),math.sin(az),0));base=Vector((0,0,h*.38));tip=d*.22*s+Vector((0,0,h))
            self.stem([base,base.lerp(tip,.55),tip],.0045*s,5)
            nodes=max(2,round(6*s))
            for j in range(nodes):
                node=base.lerp(tip,.2+.7*j/max(1,nodes-1))
                for sign in (-1,1):self.stalk_leaf(node,az+sign*1.4,.025*s,.4,.17*s,.075*s,droop=.22)
                if s>.7 and j==1:
                    p=node+d*.045-Vector((0,0,.07*s));self.stem([node,p],.002,4)
                    for k in range(1 if self.field else 4):
                        a=k*math.tau/(1 if self.field else 4)
                        Q.sphere('Four-lobed bell pepper',(p.x+.017*s*math.cos(a),p.y+.017*s*math.sin(a),p.z-.028*s),.025*s,self.root,'Green' if b%2 else 'Red',scale=(1,1,1.8),segments=5 if self.field else 7,rings=3 if self.field else 4)
        self.root['architecture']='forked stem; paired entire blades; pendent lobed peppers'

    def squash(self):
        s=self.stage;self.stem([(0,0,0),(.04*s,.02*s,.09*s)],.018*s,7)
        for j in range(max(5,round(24*s))):
            az=j*2.399;reach=self.rng.uniform(.10,.44)*s;z=self.rng.uniform(.22,.50)*s
            tip=Vector((math.cos(az)*reach,math.sin(az)*reach,z))
            self.stem([(.03*s,.01*s,.05*s),tip*.65+Vector((0,0,.075*s)),tip],.008*s,5)
            self.leaf(tip,(math.cos(az),math.sin(az),.08),self.rng.uniform(.36,.46)*s,self.rng.uniform(.36,.46)*s,cup=.15,droop=.40,rows=5,cols=5)
        if s>.7:
            for j in range(2):
                a=j*2.4;p=Vector((math.cos(a)*.16,math.sin(a)*.16,.06))*s
                Q.sphere('Zucchini beneath crown',p,.043*s,self.root,'Green',scale=(2.8,1,.8),segments=9,rings=5)
                self.bloom(Vector((p.x-.10*s,p.y,.16*s)),.055*s,5,'Yellow')
        self.root['architecture']='short basal crown; hollow long radial petioles; large lobed palmate blades; low fruit'

    def bean(self):
        s=self.stage;h=1.95*s**1.25;pts=[]
        for j in range(15):
            z=h*j/14;r=self.support_radius+.82*.0035*s*(1-.7*j/14)
            bow=.014*math.sin(math.pi*z/2.08) if self.support_radius<.003 else 0
            pts.append((r*math.cos(j*.7),bow+r*math.sin(j*.7),z))
        axis=self.stem(pts,.0035*s,5)
        for j in range(max(4,round(28*s))):
            z=.13*s+j*(h-.20*s)/(max(4,round(28*s)))+self.rng.uniform(-.018,.018)*s;az=j*2.4+self.rng.uniform(-.3,.3)
            d=Vector((math.cos(az),math.sin(az),.2));base=along(axis,z/h);end=base+d*self.rng.uniform(.11,.20)*s
            if self.field:
                side=Vector((-d.y,d.x,0)).normalized()*.001
                Q.mesh('Fine bean petiole ribbon',[base-side,base+side,end+side,end-side],[(0,1,2,3)],self.root,'Stem',upward=True)
            else:self.stem([base,end],.002*s,4)
            for k in (-1,0,1):
                a=az+k*.95;v=Vector((math.cos(a),math.sin(a),self.rng.uniform(.05,1.0)));e=end
                self.leaf(e,v,.25*s,.18*s,droop=.36)
            if s>.7 and j%3==1:
                for k in range(1 if self.field else 2):
                    p=end+Vector((k*.028,0,0))
                    if k:self.stem([end,p],.0015*s,3)
                    self.stem([p,p+Vector((.01,0,-.075)),p+Vector((.005,0,-.15))],.005,5)
        self.root['architecture']='twining leader; trifoliate leaves at alternate nodes; pendant pods'
        self.root['support_radius_m']=self.support_radius

    def corn(self):
        s=self.stage;h=2.24*s**1.25;axis=self.stem([(0,0,0),(.012*s,0,h*.45),(0,.015*s,h)],.014*s,7)
        for j in range(max(4,round(13*s))):
            t=.13+.72*j/max(1,round(13*s)-1);az=(j%2)*math.pi+.18+self.rng.uniform(-.30,.30)
            node=along(axis,t)
            if not self.field:Q.cyl('Corn sheathing node',node-Vector((0,0,.018*s)),node+Vector((0,0,.018*s)),.015*s,self.root,'Stem',7)
            self.leaf(node,(math.cos(az),math.sin(az),.62),(.95-.20*t)*s,.10*s,cup=.16,droop=.79,rows=9,cols=2)
        if s>.7:
            for z,a in ((h*.53,0),(h*.64,math.pi)):
                node=along(axis,z/h);p=node+Vector((.045*s*math.cos(a),.045*s*math.sin(a),.035*s))
                self.stem([node-Vector((0,0,.06*s)),p-Vector((0,0,.075*s))],.006*s,5)
                Q.sphere('Husked sweet corn ear',p,.035*s,self.root,'Unripe',scale=(1,1,3),segments=7,rings=4)
            for j in range(7 if self.field else 9):
                a=j*2.4;tip=Vector((.12*s*math.cos(a),.12*s*math.sin(a),h+.14*s));self.stem([(0,.015*s,h*.93),tip],.002*s,3)
                for k in range(1 if self.field else 3):
                    p=Vector((0,.015*s,h*.93)).lerp(tip,.52 if self.field else .35+k*.24)
                    Q.mesh('Tassel anthers',[p+Vector((-.003,0,-.009))*s,p+Vector((.003,0,-.009))*s,p+Vector((0,.003,.009))*s],[(0,1,2)],self.root,'Straw')
            for j in range(7):
                p=Vector((.045*s,0,h*.53+.105*s));end=p+Vector((.03+.009*math.sin(j*1.8),-.045-.014*j/7,.005-.004*math.cos(j)));mid=p+Vector((.02*math.sin(j),-.025*j/7,.025))
                if self.field:
                    side=Vector((.0007,0,0));Q.mesh('Brown silk filament ribbon',[p-side,p+side,end+side,end-side],[(0,1,2,3)],self.root,'Spent',upward=True)
                else:Q.tube('Brown silk filament',[p,mid,end],.0007*s,self.root,'Spent',3)
        self.root['architecture']='jointed culm; alternate distichous strap leaves; ears at upper axils; terminal tassel'

    def rosette(self):
        s=self.stage;sp=self.sp;kale=sp=='kale';h=(.36 if kale else .11)*s**1.25
        self.stem([(0,0,0),(0,0,h)],.012*s,6)
        n=max(6,round((35 if self.field else 36)*s))
        for j in range(n):
            az=j*2.399;f=j/n;base=Vector((0,0,h*f));v=(math.cos(az),math.sin(az),.08+f*1.7)
            self.leaf(base,v,(.32 if kale else .24)*s*(1-.35*f),(.15 if kale else .17)*s,cup=.20,droop=.15,rows=5,cols=5)
        self.root['architecture']='spiral rosette; cupped overlapping blades' if not kale else 'short stalk; spiral ruffled leaves'

    def herb(self):
        s=self.stage
        self.stem([(0,0,0),(0,0,.08*s)],.005*s,5)
        for k in range(max(2,round(6*s))):
            a=k*2.4;base=Vector((0,0,.025*s));tip=Vector((math.cos(a)*.13*s,math.sin(a)*.13*s,.40*s))
            self.stem([base,tip],.003*s,5)
            nodes=max(2,round(6*s))
            for j in range(nodes):
                p=base.lerp(tip,.2+j*.66/max(1,nodes-1))
                for side in (-1,1):self.stalk_leaf(p,a+j*math.pi/2+side*math.pi/2,.012*s,.35,.11*s,.065*s,droop=.12,rows=3)
        self.root['architecture']='basil-like opposite decussate leaf pairs on branching stems'

    def bloom(self,center,r,n=9,mat='Flower'):
        if self.field or self.sp=='marigold':
            grid=[[center+Vector(((i-1)*r,(j-1)*r,.004*(1-((i-1)**2+(j-1)**2)/2))) for i in range(3)] for j in range(3)]
            self.cards.add_grid(grid,flower_rect(mat),(.4,.8,self.rng.random(),.8))
            return
        Q.sphere('Flower receptacle',center,r*.37,self.root,'Spent',scale=(1,1,.55),segments=7,rings=2)
        # Folded radial petals, connected to the receptacle, face upward.
        for j in range(n):
            a=j*math.tau/n;d=Vector((math.cos(a),math.sin(a),0));v=Vector((-d.y,d.x,0));c=center+d*r*.22
            Q.mesh('Cupped corolla petal',[c-v*r*.17,c+d*r*.70-v*r*.30+Vector((0,0,r*.24)),c+d*r,c+d*r*.70+v*r*.30+Vector((0,0,r*.24)),c+v*r*.17],[(0,1,2),(0,2,3),(0,3,4)],self.root,mat,upward=True)

    def flower(self):
        s=self.stage;sun=self.sp=='sunflower';h=(1.90 if sun else .28)*s**1.25
        axis=self.stem([(0,0,0),(.018*s,0,h)],(.012 if sun else .004)*s,6)
        if sun:
            for j in range(max(3,round(12*s))):
                a=j*2.399;node=along(axis,.10+j*.77/max(1,round(12*s)-1))
                self.stalk_leaf(node,a,.07*s,.6,.30*s,.22*s,droop=.30,rows=3)
            if s>.55:
                center=Vector((.018*s,-.065*s,h-.025*s));self.stem([axis[-1],center],.006*s,5)
                Q.sphere('Sunflower seed disc',center,.080*s,self.root,'Spent',scale=(1,.30,1),segments=14,rings=4)
                for j in range(22):
                    a=j*math.tau/22;d=Vector((math.cos(a),-.04,math.sin(a)));p=center+d*.074*s
                    ob=Q.sphere('Ray floret',p+d*.035*s,.021*s,self.root,'Yellow',scale=(.5,.2,2),segments=4,rings=2)
                    ob.data.transform(MatrixAround(p+d*.035*s,d.to_track_quat('Z','Y').to_matrix().to_4x4()))
        else:
            for b in range(max(2,round(9*s))):
                a=b*2.399;base=along(axis,.08);tip=Vector((math.cos(a)*.14*s,math.sin(a)*.14*s,h*self.rng.uniform(.7,1.15)))
                branch=self.stem([base,base.lerp(tip,.65),tip],.0025*s,4)
                for j in range(4 if self.field else 6):
                    node=along(branch,.12+j*(.69/(3 if self.field else 5)))
                    for sign in (-1,1):self.stalk_leaf(node,a+sign*1.3,.016*s,.35,.11*s,.065*s,rows=3)
                if s>.55:
                    self.bloom(tip,.037*s,10,'Flower' if b%4 else 'Yellow')
                    self.bloom(tip+Vector((0,0,.010*s)),.022*s,8,'Yellow' if b%4 else 'Flower')
            if s>.7:self.bloom(Vector((-.06*s,.04*s,h*.55)),.016*s,7,'Spent')
        self.root['architecture']='alternate broad leaves and drooping sunflower head' if sun else 'compact seven-branch mound; pinnate foliage; double flowering heads and one spent flower'

    def weed(self):
        s=self.stage
        for j in range(9):
            a=j*2.4;self.leaf((0,0,.008),(math.cos(a),math.sin(a),.6),.19*s,.026*s,droop=.3,rows=4)
        self.stem([(0,0,0),(.02*s,0,.27*s)],.002*s,4)

    def finish(self):
        core=Q.join(self.root)
        if core:
            height=max(.05,max(v.co.z for v in core.data.vertices));phase=self.rng.random()
            botany.wind_attribute(core,[(max(0,min(1,v.co.z/height))*.38,.25,phase,0) for v in core.data.vertices])
        if self.cards.vertices:
            ob=self.cards.mesh(self.root.name+'__Leaves',LEAF);ob.parent=self.root
            # This stage uses outline alpha only. Physical normals come from
            # shared curved cards, not painted crown illumination.
            tr=ob.modifiers.new('Leaf triangles','TRIANGULATE');tr.keep_custom_normals=True;Q.G.apply(ob)
        extra=162 if self.sp=='tomato' and self.stage>.7 else 0
        self.root['atlas_leaflet_count']=extra
        self.root['blade_count']=len(self.blades)+extra
        self.root['blade_lengths_m']=[b['length_m'] for b in self.blades]
        self.root['blade_widths_m']=[b['width_m'] for b in self.blades]
        self.root['triangles']=Q.count(self.root)
        return self.root


def MatrixAround(p,m):
    from mathutils import Matrix
    return Matrix.Translation(p)@m@Matrix.Translation(-p)


def build(species,stage=1,seed=1,support_radius=.0125,field=False):
    p=Plant(species,stage,seed,support_radius,field)
    if species in ('lettuce','kale'):p.rosette()
    elif species in ('sunflower','marigold'):p.flower()
    else:getattr(p,species)()
    return p.finish()


def library():
    out={}
    for sp in SPECIES:
        for j,stage in enumerate((.28,.64,1.0)):
            for variant in range(2 if stage==1 else 1):
                name=f'{sp}_{j}_{variant}';rt=build(sp,stage,713+SPECIES.index(sp)*29+variant*167,support_radius=.00125 if sp=='bean' and variant==1 else .0125)
                rt.name=name;out[name]=rt
                if stage==1:
                    ft=build(sp,stage,713+SPECIES.index(sp)*29+variant*167,support_radius=.00125 if sp=='bean' and variant==1 else .0125,field=True)
                    ft.name=name+'_field';out[ft.name]=ft
    return out
