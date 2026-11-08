"""Seeded causal weather skins sharing the existing three-map atlas."""
import math,random
import bpy
from mathutils import Vector
from textures import RECTS


def material():
    name='ManufacturedPatina';ma=bpy.data.materials.get(name)
    if ma:return ma
    from surfaces import palette
    ma=palette()['Metal'].copy();ma.name=name;ma['tiling_vertex_tint']=True
    ns,ls=ma.node_tree.nodes,ma.node_tree.links;bs=next(n for n in ns if n.type=='BSDF_PRINCIPLED')
    color=next(n for n in ns if n.type=='TEX_IMAGE' and 'BaseColor' in n.image.name)
    tint=next(n for n in ns if n.type=='VERTEX_COLOR');alpha=ns.new('ShaderNodeMath');alpha.operation='MULTIPLY'
    ls.new(color.outputs['Alpha'],alpha.inputs[0]);ls.new(tint.outputs['Alpha'],alpha.inputs[1]);ls.new(alpha.outputs[0],bs.inputs['Alpha'])
    ma.surface_render_method='DITHERED';ma.use_backface_culling=True;return ma


def rect(kind,variant=0):
    u0,v0,u1,v1=RECTS[kind]
    if kind=='Rust':step=(u1-u0)/4;u0+=variant%4*step;u1=u0+step
    pad=3/2048;return u0+pad,v0+pad,u1-pad,v1-pad


def quad(parent,name,points,chart,alpha=1,up=False):
    if alpha<.015:return
    me=bpy.data.meshes.new(name);me.from_pydata(points,[],[(0,1,2,3)]);me.materials.append(material());me.update()
    face=me.polygons[0];center=face.center
    if (up and face.normal.z<0) or (not up and face.normal.x*center.x+face.normal.y*center.y<0):face.flip()
    uv=me.uv_layers.new(name='UVMap');u0,v0,u1,v1=chart;corners=((u0,v0),(u1,v0),(u1,v1),(u0,v1))
    for li in face.loop_indices:uv.data[li].uv=corners[me.loops[li].vertex_index]
    tint=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER');me.color_attributes.active_color=tint
    for row in tint.data:row.color=(1,1,1,alpha)
    ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);ob.parent=parent
    ob['asset_set']='Manufactured';ob['component']='weather_patina';ob['cause']=name;return ob


def home(a,p,skirt):
    if p['era']=='1996':return
    from homes import openings
    r=random.Random(p['seed']+51097);L,W,E,F=p['length'],p['width'],p['eave'],p['floor']
    severity={'patched':1.,'faded':.76,'kept':.15}[p['upkeep']]
    for face in ('front','back','left','right'):
        along=face in ('front','back');sign=-1 if face in ('front','left') else 1;length=L if along else W;holes=openings(p,face)
        def xf(u,z,offset=.0026):return (u,sign*(W/2+offset),z) if along else (sign*(L/2+offset),u,z)
        def wall(kind,u,z,w,h,strength):
            if u-w/2< -length/2+.04 or u+w/2>length/2-.04:return
            quad(a.root,'Protected '+kind+' '+face,[xf(u-w/2,z),xf(u+w/2,z),xf(u+w/2,z+h),xf(u-w/2,z+h)],rect(kind,r.randrange(4)),strength)
        north=(face=='back')==(p.get('site_yaw',0)==0) if along else False
        # Microclimate below the eave; sparse fans, rather than a uniform band.
        for u in (-length*.33,length*.04,length*.32):
            width=r.uniform(.48,.9);z=E-r.uniform(.18,.29)
            if any(abs(u-h['u'])<h['w']/2+width/2 and z<h['z']+h['h']+.025 for h in holes):continue
            wall('Damp',u,z,width,E-z,severity*(.85 if north else .48))
        for h in holes:
            if h['kind']!='window':continue
            if r.random()<.60*severity:
                side=r.choice((-1,1));width=r.uniform(.12,.22);u=h['u']+side*(h['w']/2+.14)
                drop=r.uniform(.18,.58);wall('Rust',u,h['z']-.04-drop,width,drop,severity*.95)
            if r.random()<.55*severity:
                side=r.choice((-1,1));u=h['u']+side*(h['w']/2+.22)
                wall('Damp',u,h['z']+.12,.24,h['h']*.73,severity*(.8 if north else .48))
        # A small number of actual outer rail sources beside the end hood.
        if not along and severity>.4:
            u=(-1 if p['seed']%2 else 1)*(holes[0]['w']/2+.20);drop=r.uniform(.30,.72)
            wall('Rust',u,E-.035-drop,.22,drop,severity)
        # Splash follows grade. Keep real missing/cracked openings unobscured:
        # each weather skin stays inside one existing intact skirt panel.
        count=math.ceil(length/.4064)
        for j in range(count):
            if p['missing_skirt'] and (face=='front' and j==count//2+3 or not along and j==1):continue
            if face=='back' and j in (count//2-1,count//2):continue
            if p['era']=='1972' and face=='front' and (p['seed']%4==0 and j==count//3 or p['seed']%2==0 and j==count//4):continue
            if r.random()>.44*severity:continue
            u=-length/2+(j+.5)*length/count;w=length/count-.012;z=.046;ht=r.uniform(.29,.40)
            points=[xf(u-w/2,z,.014),xf(u+w/2,z,.014),xf(u+w/2,z+ht,.014),xf(u-w/2,z+ht,.014)]
            quad(skirt,'Grade splash '+face,points,rect('Splash'),severity*.95)


def awning(a,p,face,h,xf):
    if p['era']!='1972':return
    r=random.Random(p['seed']+round(h['u']*100)+sum(map(ord,face))*13)
    severity={'patched':1.,'faded':.75,'kept':.12}[p['upkeep']]
    top=h['z']+h['h']+.18;u=h['u']
    for side in (-1,1):
        if r.random()>.55*severity:continue
        x=u+side*h['w']*.36;width=r.uniform(.10,.17);drop=r.uniform(.17,.39);d=.026
        points=[xf((x-width/2,d+drop,top-.19*(d+drop)/.62+.002)),xf((x+width/2,d+drop,top-.19*(d+drop)/.62+.002)),
                xf((x+width/2,d,top-.19*d/.62+.002)),xf((x-width/2,d,top-.19*d/.62+.002))]
        quad(a.root,'Awning screw runoff',points,rect('Rust',r.randrange(4)),severity,up=True)
