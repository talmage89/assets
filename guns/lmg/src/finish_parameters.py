"""Meter-scale authored reflectance inputs; photographic fitting never edits maps.

Black paint is a 2.2% diffuse reflector. Dielectric F0 is controlled through
Blender's specular factor, retained in opaque atlas alpha. These inputs belong
only to Harrow; the family precedents remain read-only.
"""
PAINT=(.022,.023,.024)
PAINT_ROUGH=.42
PAINT_SPEC=.8
PHOSPHATE=(.028,.029,.030)
BIPOD_PHOSPHATE=(.044,.045,.042)
PHOSPHATE_ROUGH=.57
PHOSPHATE_METAL=.35
POLYMER={
 'handguard':((.006,.0068,.0078),.60,.55),
 'stock':((.009,.0095,.010),.57,.8),
 'grip':((.032,.034,.036),.40,.95),
 'box':((.023,.024,.023),.55,.8),
 'handle':((.009,.0095,.010),.24,1.0),
}

# Fine molding skin: cycles/m, relief in meters, roughness span. These are
# distinct manufacturing finishes, not one exaggerated grain on every molding.
POLYMER_GRAIN={
 'handguard':(1000,20e-6,.10),
 'stock':(1200,16e-6,.06),
 'grip':(1400,10e-6,.06),
 'box':(1000,25e-6,.10),
 'handle':(1800,6e-6,.04),
}

SITES=("receiver","cover","cover_top","rivets","handle","flash","regulator","ports","feet","box","butt")
