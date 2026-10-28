"""Original inert 7.62×39 visual silhouettes for game props.

Millimeter exterior approximations only. No chamber, projectile interior,
primer pocket, loading specification, working cartridge or tolerance model.
The caller owns materials, mesh registration and its scene's scale conversion.
"""
def cartridge(lathe,name,position,bone,*,fired=False,sides=32):
 x,y,z=position
 # Sparse silhouette stations; the covered base is a solid visual cap.
 case=[(0,0),(0,5.5),(.4,5.65),(1.2,5.65),(1.6,5.15),
       (3.0,5.15),(3.4,5.5),(27.5,5.0),(31.3,4.2),(38.6,4.0)]
 if fired:case += [(38.6,3.5),(36.8,3.5),(36.8,0)]
 else:case += [(38.6,0)]
 objects=[lathe(name+'_Case',[(y+h,r) for h,r in case],
                'case',bone,center=(x,z),n=sides)]
 if not fired:
  jacket=[(37.8,0),(37.8,3.9),(41.5,3.9),(46.5,3.3),
          (51.2,2.1),(55.2,.85),(55.8,.2),(55.8,0)]
  objects.append(lathe(name+'_Jacket',[(y+h,r) for h,r in jacket],
                       'copper',bone,center=(x,z),n=sides))
 return objects
