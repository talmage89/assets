"""Family 9 mm exterior game meshes, based on the accepted C9 profile, retessellated for macro views.

No firearm internals or ammunition construction are modeled. A caller supplies
its own lathe(name, profile, material, bone, center=..., n=..., closed=...).
Coordinates are visual-asset millimeters, +Y toward the bullet/mouth. The
pistol's existing builder is unchanged and can adopt this module separately.
"""
def cartridge(lathe,name,base,bone='Root',*,fired=False,sides=20):
    x,y,z=base
    if fired:
        # Dense circumference, sparse axial stations: round macro silhouettes
        # under 700 triangles. The bottom/primer are separate exterior surfaces.
        profile=[(0,0),(0,4.86),(.12,4.96),(1.05,4.96),(1.25,4.15),
                 (2.1,4.15),(2.35,4.91),(18.85,4.74),(19.15,4.72),
                 (19.15,4.38),(1.6,4.38),(1.6,0)]
        case=lathe(name+'_Case',[(y+a,r) for a,r in profile],'brass',bone,center=(x,z),n=32)
        # Open mouth / extractor groove get the circumference budget. Primer
        # center is a smooth disc rather than hidden concentric geometry.
        lathe(name+'_Primer',[(y-.01,0),(y-.01,1.7),(y+.04,1.7),(y+.04,0)],
              'primer',bone,center=(x,z),n=12)
    else:
        profile=[(0,0),(0,4.96),(1.1,4.96),(1.3,4.15),(2.1,4.15),(2.4,4.91),(19.15,4.72),(19.15,0)]
        case=lathe(name+'_Case',[(y+a,r) for a,r in profile],'brass',bone,center=(x,z),n=sides)
        lathe(name+'_Primer',[(y-.01,0),(y-.01,1.7),(y+.08,1.7),(y+.08,0)],'primer',bone,center=(x,z),n=12)
        bullet=[(18.8,0),(18.8,4.5),(23,4.5),(25.3,3.9),(27.5,2.7),(29.5,0)]
        lathe(name+'_Bullet',[(y+a,r) for a,r in bullet],'copper',bone,center=(x,z),n=sides)
    return case
