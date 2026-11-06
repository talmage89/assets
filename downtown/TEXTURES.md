# Shared texture allocation proposed for look-dev

No final texture bake is part of this checkpoint. The current geometry has
meter staging UVs, vertex quick colors, and one original 2048² sign image.
That image is shared by all 28 individual glTFs through one canonical URI.

The proposed delivery follows the houses' stock glTF plus shared external
images, with no custom runtime shader and at most six materials per building.
Do not allocate one atlas per building.

| Shared allocation | Ship / maps | Purpose and physical organization | GPU MiB |
| --- | --- | --- | ---: |
| Masonry | 2048² BaseColor / Normal / ORM | Original common/running bond, measured brick/mortar module; guarded kiln-color and painted-brick variants. Mortar remains neutral in baked texels | 16 |
| Mineral + roofing | 1024² BaseColor / Normal / ORM | Guarded tiling regions for limestone, terra cotta and falling membrane roof. Copings/stone returns use the mineral region, roofs use the membrane region | 4 |
| Finish + trim/ornament | 2048² BaseColor / Normal / ORM | Painted wood grain, painted iron, aluminum/bronze, galvanized metal, dentil/frieze relief, flutes and small ornament. Broad finishes tile in U within guarded strips; formed silhouette remains geometry | 16 |
| Signs | 2048² RGBA BaseColor | Fictional sign-band, blade and glass lettering, old ghost-paint variants. Swap names using atlas UV rectangles; no new lettering geometry | 5.333 |
| Interior | 1024² RGBA BaseColor | Original drawn shelf/office/apartment backings and light masks. Depth comes from the existing shallow geometry; alpha supports curtain/light coverage | 1.333 |
| Glass | Reuses finish/trim clear region | Uniform IOR/transmission state, with authored pane thickness and ordinary glTF material extensions | 0 |
| **All towns, loaded once** | **11 canonical images** | **Six material states maximum: masonry, mineral/roof, finish/trim, signs, interior, glass** | **42.667** |

Estimates assume BC7 color/ORM, BC5 normal, 8 bpp per image and complete mip
chains. PNG disk bytes do not imply compression or GPU allocation. Uncompressed
RGBA8 uploads with mipmaps would be about 170.667 MiB. A scene loading every
building still shares these same resources, if its importer caches canonical
image URIs as the houses' delivery does. This is a planned allocation, not a
measured engine memory claim.

Bake original source fields at 4096, then use the existing channel-correct kit
filters to the stated ship sizes. Brick module, guarded strip coverage and
physical texel densities must be independently measured after final UV mapping.
Current meter UVs are not those finished charts; repeated UVs are deliberate.

Wear must follow causes: mortar repair patches, low splash and spalls, damp
below scuppers/downspouts and sills, escape-anchor rust, upward fading,
peeling folded-metal paint at seams and edges, and threshold contact. Large
patches need subdivided weather vertices or UV-addressed regions; a global noise
wash or broad uniform dirt band is unacceptable. A used reference, white-balanced
on a stated neutral, must calibrate those effects on exported textured geometry.

Night response remains a next-gate feature. Interior lights should occupy
selected apartment/office cells and supported shop fixtures. The form checkpoint
contains the room geometry, curtains, blinds, window air conditioners, diner
booths/counter/stools, shelves, barber chairs and vacant paper; no night-light
or physically calibrated illumination claim is made here.
