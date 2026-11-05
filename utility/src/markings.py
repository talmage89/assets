"""Original temporary diagnostic labels; no photographic pixels."""
from pathlib import Path
import bpy
from kit.fonts import find_font
from kit import model as G


def label(name,text,position,w,h):
    # A single quad carries generated text; fine text never costs mesh triangles.
    import subprocess,sys
    key=text.replace('\n','_').replace(' ','_').replace('/','-')
    path=Path('build/labels')/(key+'.png');path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists():
        subprocess.run(['python3',str(Path(__file__).with_name('label_image.py').resolve()),'--text',text,'--out',str(path)],check=True)
    m=bpy.data.materials.new(name+' diagnostic ink');m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.9
    im=m.node_tree.nodes.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(path.resolve()),check_existing=True)
    m.node_tree.links.new(im.outputs['Color'],p.inputs['Base Color'])
    m.node_tree.links.new(im.outputs['Alpha'],p.inputs['Alpha']);m.surface_render_method='DITHERED'
    x,y,z=position;ob=G.mesh(name,[(x-w/2,y,z-h/2),(x+w/2,y,z-h/2),(x+w/2,y,z+h/2),(x-w/2,y,z+h/2)],[(0,1,2,3)],m)
    uv=ob.data.uv_layers.new()
    for i,p in enumerate(((0,0),(1,0),(1,1),(0,1))):uv.data[i].uv=p
    return ob


if __name__=='__main__':
    # Invoked with system Python; Blender's own Python need not have Pillow.
    pass
