"""Meter-scale authored reflectance inputs; photographic fitting never edits maps.

Black paint is a 2.2% diffuse reflector. Dielectric F0 is controlled through
Blender's specular factor, retained in opaque atlas alpha. These inputs belong
only to Harrow; the family precedents remain read-only.
"""
PAINT=(.022,.023,.024)
PAINT_ROUGH=.28
PAINT_SPEC=.8
PHOSPHATE=(.028,.029,.030)
PHOSPHATE_ROUGH=.57
PHOSPHATE_METAL=.35
POLYMER={
 'handguard':((.006,.0068,.0078),.60,.55),
 'stock':((.009,.0095,.010),.57,.8),
 'grip':((.025,.027,.029),.30,.95),
 'box':((.023,.024,.023),.55,.8),
 'handle':((.006,.0065,.007),.32,.85),
}

SITES=("receiver","cover","cover_top","rivets","handle","flash","regulator","ports","feet","box","butt")
