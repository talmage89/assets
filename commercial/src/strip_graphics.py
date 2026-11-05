"""Original tenant/sign/window artwork. No photographic inputs.

Every tenant uses the same sign and window quad geometry; only atlas UVs change.
This form sheet reserves the eventual 2K single-color sign-sheet allocation.
"""
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from PIL import Image, ImageDraw, ImageFont
from kit.fonts import find_font
from strip_plan import TENANTS


def generate(out=Path('build/strip/signs')):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    size=2048;im=Image.new('RGBA',(size,size),(0,0,0,0));dr=ImageDraw.Draw(im);records={}
    keys=list(TENANTS)
    def cell(index):
        col,row=index%4,index//4
        return col*512+12,row*204+12,col*512+500,row*204+192
    def font(family,style,size):return ImageFont.truetype(str(find_font(family,style)),size)
    def label(string,rect,face,color,fraction=.88,y=.5,height=.42):
        x0,y0,x1,y1=rect;ff=font(face,'Bold',60)
        while dr.textbbox((0,0),string,font=ff)[2]>fraction*(x1-x0) or dr.textbbox((0,0),string,font=ff)[3]-dr.textbbox((0,0),string,font=ff)[1]>(y1-y0)*height:ff=font(face,'Bold',ff.size-1)
        bb=dr.textbbox((0,0),string,font=ff)
        dr.text(((x0+x1)/2-(bb[2]+bb[0])/2,y0+(y1-y0)*y-(bb[3]+bb[1])/2),string,font=ff,fill=color)
    for i,(key,t) in enumerate(TENANTS.items()):
        rr=cell(i);r=(rr[0],rr[1],rr[2],rr[1]+74);face='DejaVu Serif' if t['font']=='serif' else 'DejaVu Sans'
        # Channel-letter cells keep transparent fields over a physical raceway.
        if t['style']!='channel':
            dr.rectangle(r,fill=t['field'])
            if t['style']=='panel':dr.rectangle((r[0]+5,r[1]+5,r[2]-5,r[3]-5),outline=t['ink'],width=3)
        label(t['name'],r,face,t['ink'],y=.30,height=.43)
        sub=(r[0]+8,r[1]+45,r[2]-8,r[3]-3)
        label(t['subtitle'],sub,'DejaVu Sans',t['ink'],y=.51,height=.55)
        # A small authored motif changes the silhouette of the ink, not a logo
        # traced from a chain. Type choices avoid distinctive chain wordmarks.
        dr.line((r[0]+45,r[1]+43,r[2]-45,r[1]+43),fill=t['ink'],width=1)
        records[key]={'sign':r,'style':t['style']}
        r=cell(i+9)
        dr.rectangle((r[0]+5,r[1]+5,r[2]-5,r[3]-5),fill='#E6DFCC' if key=='vacant' else '#1D282B')
        if key=='vacant':
            label('FOR LEASE',r,'DejaVu Sans','#753C32',y=.30)
            label('INQUIRE AT OFFICE',r,'DejaVu Sans','#34413C',y=.69)
        else:
            label('OPEN',r,'DejaVu Sans','#D9B079',y=.24)
            label('MON - SAT   9 - 7',r,'DejaVu Sans','#EEE9D8',y=.53)
            label(t['subtitle'],r,'DejaVu Sans','#EEE9D8',y=.80)
        records[key]['window']=r
    for j,name in enumerate(('ALDER RILL SHOPS','CROSSBEND COURT','LOWBANK COMMONS','WILLOW SPAN SHOPS')):
        rr=cell(18+j);r=(rr[0],rr[1],rr[2],rr[1]+132);dr.rectangle(r,fill='#343C37');label(name,r,'DejaVu Serif','#E6D9BC',y=.34,height=.28)
        label('NEIGHBORHOOD SHOPS',r,'DejaVu Sans','#E6D9BC',y=.75,height=.16);records[name]={'sign':r}
    for j,address in enumerate(str(110+2*i) for i in range(12)):
        rr=cell(22+j);r=(rr[0],rr[1],rr[2],rr[1]+74);dr.rectangle(r,fill='#22282A');label(address,r,'DejaVu Sans','#EEEBDC',height=.70);records[address]={'sign':r}
    for j,string in enumerate(('RESERVED','VAN ACCESSIBLE')):
        rr=cell(34+j);r=(rr[0],rr[1],rr[2],rr[1]+74);dr.rectangle(r,fill='#EAE9DF');label(string,r,'DejaVu Sans','#294539',height=.68);records[string]={'sign':r}
    # Short tower faces have their own correctly proportioned layout. Do not
    # squeeze a six-to-one fascia wordmark onto a three-to-one entry panel.
    for j,(key,t) in enumerate(TENANTS.items()):
        col,row=j%8,j//8;r=(col*250+6,1840+row*90,col*250+244,1920+row*90)
        dr.rectangle(r,fill=t['field']);face='DejaVu Serif' if t['font']=='serif' else 'DejaVu Sans'
        parts=t['name'].split(' ')
        if len(parts)>1:
            for line,word in enumerate((' '.join(parts[:-1]),parts[-1])):
                area=(r[0],r[1]+line*27,r[2],r[1]+(line+1)*27)
                label(word,area,face,t['ink'],height=.80)
        else:label(t['name'],(r[0],r[1]+2,r[2],r[1]+55),face,t['ink'],height=.66)
        label(t['subtitle'],(r[0]+2,r[1]+58,r[2]-2,r[3]-2),'DejaVu Sans',t['ink'],height=.65)
        records[key]['tower']=r
    im.save(out/'T_StripSigns_BaseColor.png')
    for data in records.values():
        for kind in ('sign','window','tower'):
            if kind in data:
                a,b,c,d=data[kind];data[kind]=(a/size,1-d/size,c/size,1-b/size)
    (out/'layout.json').write_text(json.dumps(records,indent=2)+'\n')
    return out


def install(folder=Path('build/strip/signs')):
    import bpy
    folder=Path(folder);ma=bpy.data.materials.new('StripTenantInks');ma.use_nodes=True
    ns,ls=ma.node_tree.nodes,ma.node_tree.links;p=ns.get('Principled BSDF')
    tex=ns.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str((folder/'T_StripSigns_BaseColor.png').resolve()),check_existing=True)
    ls.new(tex.outputs['Color'],p.inputs['Base Color']);ls.new(tex.outputs['Alpha'],p.inputs['Alpha'])
    p.inputs['Roughness'].default_value=.55;ma.surface_render_method='DITHERED';ma.use_backface_culling=True
    return ma,json.loads((folder/'layout.json').read_text())


def quad(name,tenant,kind,x,y,z,w,h,parent,mat,layout):
    from geometry import mesh
    ob=mesh(name,[(x-w/2,y,z-h/2),(x+w/2,y,z-h/2),(x+w/2,y,z+h/2),(x-w/2,y,z+h/2)],[(0,1,2,3)],mat,parent,False)
    uv=ob.data.uv_layers.new(name='UVMap');a,b,c,d=layout[tenant][kind]
    assert 0<=a<c<=1 and 0<=b<d<=1,('Invalid ink rectangle',tenant,kind,(a,b,c,d))
    tc=((a,b),(c,b),(c,d),(a,d))
    for li in ob.data.loops:uv.data[li.index].uv=tc[li.vertex_index]
    ob['tenant']=tenant;ob['graphic']=True;return ob


if __name__=='__main__':generate()
