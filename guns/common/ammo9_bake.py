"""Dense bake-only 9 mm exteriors from the accepted family visual profiles.

The existing game builder remains unchanged. A dense, regular quad revolution
avoids baking triangulated game-mesh smoothing fans into polished jackets and
case mouths. Coordinates enter as millimeters; returned mesh data is meters.
No source object is bound, exported or assigned an asset family here.
"""
from mathutils import Matrix
from kit import model as M
from guns.common.ammo9_visual import cartridge

def parts(name,base,*,materials,bone='Root',fired=False,segments=128):
 result=[]
 def lathe(part,profile,material,owner,*,center,n=32,closed=False):
  ob=M.lathe(part+'_Bake',profile,materials[material],segments=segments,
             axis='Y',center=center,closed=closed)
  ob.data.transform(Matrix.Scale(.001,4));ob['low_target']=part;ob['bone']=owner
  result.append(ob);return ob
 cartridge(lathe,name,base,bone,fired=fired,sides=segments)
 return result
