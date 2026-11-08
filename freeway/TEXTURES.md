# Freeway materials

The civil delivery uses stock external glTF PBR, shared images and ordinary vertex
color. Every pixel is scripted. Reference photographs only inform the visual
review; none is sampled by a material generator.

Ground Asphalt, Concrete, Lawn and GroundTrim remain byte-identical inputs.
The freeway's seasonal lawn derivative changes only the original scripted
Lawn BaseColor pigment and clump-scale value contrast; its canonical blade
normal and ORM stay shared. This
2048 color map adds 5⅓ MiB when a scene also loads the native commercial lawn.
Dry straw pigment lives in that image, with normalized vertex colors at or
below one; glTF cannot retain an HDR multiplier in its normalized COLOR_0.
Broad dry/mown/unmown fields follow exposure and drainage on the actual graded
earth. There are no overlapping opaque mowing skins. Dense crossed-card tiles
sample the maintenance atlas's original rooted fan of blades/seed heads and
belong to the optional context budget. Eight linked tile meshes carry the
near-field parallax; density falls toward the textured base at distance. Tiles
follow actual earth normals and reject paved footprints. Mown cards are short;
unmown drifts past the maintenance line are taller. The card material is stock
double-sided glTF MASK and allocates no extra image. Each linked tile has 16
clumps, two crossed quads per clump and 64 triangles, on a .65m placement pitch.
The smaller footprint fits terrain creases with less whole-patch burial.
Stratified roots and
upward blade normals keep the sward continuous. The atlas fan has 90
thin blades and two seed heads. Alternating shoulder strips select subtly
lighter/darker card patterns; unmown tiles vary height in drifts. Grass-card
normal strength is .10 so the atlas's shared repair relief does not make
individual blades look corrugated. Source-height comparisons apply that same
strength. The base retains the native baked blade normal at its own scale.
Four narrow linked tile rows taper the curved median's sward toward paving.
Placement density and blade height both fade toward the distant base. Its
aggregate under-blade value and faint 1.524m mowing swaths keep distant turf
from becoming a lighter blank sheet. ROW UVs follow station/lateral meters,
including the curved alignment. Additional near-detail zones cover guides
and rails; all cards and their scales are present in the actual export.
Bare soil/gravel reuses the native Asphalt mineral grain with brown vertex
pigment; its image bytes stay canonical. The irregular median-edge skin is
sampled against the actual terrain, retaining the original supporting mesh.
World/meter tile UVs intentionally repeat. Existing manufacture remains in
those maps; broad traffic causes belong to lane-space vertex colors and
placement-owned maintenance charts. Wheel-polish materials share Ground
Concrete's or Asphalt's three images and reduce roughness in the wheel paths.
Explicit lane-center sample vertices retain the narrow oil field rather than
interpolating between its two edges.

| New shared set | Shipped maps | Full-mip BC7/BC5-equivalent memory | Reason |
| --- | --- | ---: | --- |
| FreewayConcrete | 2048 BaseColor / Normal / ORM | 16 MiB | Cast bridge, barriers, wall panels and drainage; sand, pores and surface response at a physical 3.048m repeat |
| FreewayZinc | 1024 BaseColor / Normal / ORM | 4 MiB | Large unpainted guide/rail/light structures need dulled zinc and hydroxide response absent from the paving atlas |
| FreewaySigns | 2048 BaseColor / Normal / ORM | 16 MiB | Thirteen original guide/regulatory/trailblazer legends, guarded chart regions and aged sheeting; fictional state marker |
| FreewayMaintenance | 1024 RGBA BaseColor / Normal / ORM | 4 MiB | Additional caused repairs, broken old paint, joint spalls, crack sealant, drips, drain salts, tire traces, silt and small trapped debris |

The new allocation is **40 MiB**, shared across both scenes and all 17 pieces.
The sign triple replaces the form gate's temporary single sign image. The
small ROW fabric field is reused from the original fence recipe. Town and
traffic load their own native library sets, outside the freeway-only cost.
Disk PNG bytes and the actual unique-image union are measured in
`build/look-audit.json`, rather than inferred from this allocation table.

`textures.py` generates original 4096 fields; `bake.py` calls the kit's GPU
flat-tile baker, with physical height ranges and color round-trip checks.
`filter_textures.py` uses the kit's linear-light color, vector normal and
roughness RMS reduction. BaseColor is sRGB, normals are OpenGL +Y, ORM is
linear R occlusion / G roughness / B metallic. Coverage is independent of
color during baking and is restored before premultiplied delivery filtering.

The 4×4 maintenance atlas has eight shipped-pixel chart insets. Charts repeat
only when their cause recurs; location, orientation, extent and phase belong
to the seeded scene. This is deliberate atlas reuse, not a unique lightmap
unwrap. Normal maps use the same chart orientation as their color. The source
material comparison replaces shipped maps with the 4096 fields and evaluates
the physical source height; its metadata explicitly labels that inspection.

Pavement is divided at measured lane/wheel offsets. Smooth wheel contact and
narrow engine-line darkening follow the driving direction, with interrupted
station history rather than a uniform noise wash. Slab repairs stay between
joints and sample native paving grain instead of an atlas patch stamp;
spalls follow seals, shoulder crack sealants stay on asphalt, and the
later overlay is confined to a maintained stretch. Old dashes are offset from
the restripe and raised markers are omitted by a deterministic seed.

Bridge deposits begin at joints, scuppers and bearing locations. Seven separate
cap concentrations follow the actual bearing lines, with variable width,
opacity and run length. Broad damp film remains below the bearing shelf.
Girder drips
follow the actual flange/web profile and camber. Column repairs follow the
cylinder; no flat patch floats in front of it. Additional column height
stations carry broad head-connected dampness and low spray deposits.
The existing runoff chart supplies fine channels on skins following each
32-sided shaft, .6mm above its actual surface, from below the cap to the foot.
The old opaque decorative column-repair skins are removed so they cannot
interrupt that flow with pale rectangular cutouts.
Barrier toes retain
road film, and open assembly ends concentrate joint staining. A few ramp-rail bays are bent,
with neighboring replacements brighter than the older zinc. Litter and rooted
volunteers accumulate at barrier drainage and fence traps.

Traffic uses the three original native car bodies. The car family's own
coverage-alpha/factory-color data produces ordinary local paint RGB variants;
original bodies, maps and deliveries are unchanged. Native near bodies retain
all geometry and maps; distant context bodies retain the prior coherent local
LOD normals and omit the high-mesh normal bake. Brake emission is retained for
queues and disabled for flowing daytime traffic. These static scene actors do
not replace the working native vehicle deliveries.

`context_colors.py` decodes the canonical GLB's embedded PNG explicitly from
sRGB, applies the native factory-reference delta through its coverage alpha,
filters in linear light and encodes once. Twenty-one 1024 RGB variants serve
seven additional colors on three bodies; Atlantic reuses the native reference
map. Porcelain, Carbon, Aluminum, Graphite and Atlantic are native car-family
presets. Garnet, Spruce and Sand are original local tints. The exported ORM
metallic factor follows each factory preset, rather than retaining Atlantic's
factor for every finish. The fleet weights are 22/16/22/12/12/10/4/2 percent
for silver/gray/black/white/blue/red/green/tan; seeds select individual actors.
The inverse audit follows actual exported material bindings and recovers the
filtered native reference within 8-bit quantization on unclipped pixels. This
guards against the pale-fleet conversion error rejected in review pass 4.

The town export preserves native house CORNER color through its import/export
boundary. COLOR_0 is required wherever a native tiling material declares
vertex tint. Tree finals use the tree family's documented two-sided thin-leaf
response with the actual exported baked images. Stock glTF MASK is the portable
fallback; an engine needs the corresponding foliage shader for that response.
No new foliage image or procedural leaf field is substituted in final renders.
Cycles uses 128 transparent bounces, following the native oak's overlapping
cards; the default eight made mature crowns artificially black. Larger mature
yard crowns and smaller freeway-front trees are recorded instance transforms,
not additional unique foliage meshes or new image allocations.
