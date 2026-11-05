# Shared signals surfaces

The family uses five original images, referenced by the same external URI
from every assembly and reusable part. There are no copied maps per seed.
Stock glTF PBR handles every finish and lens state.

| Image | Delivery | Purpose |
| --- | --- | --- |
| T_Signals_BaseColor | 2048², sRGB | 32 guarded manufacturing/age trims, equipment fronts, signs and maintenance records |
| T_Signals_Normal | 2048², OpenGL +Y | Meter-scale manufactured relief; Cycles bake at 4096, vector-filtered to 2048 |
| T_Signals_ORM | 2048², non-color | R occlusion, G roughness, B metallic; dielectric paint and concrete remain nonmetallic |
| T_Signals_Emissive | 1024², sRGB + coverage alpha | Original LED arrays, arrows, hand/person and digit source; full opaque vehicle-lens circles with radial emissive packages inside |
| T_Signals_Names | 512 × 256, sRGB | Eight fictional swappable street names |

At 8 bits per pixel block compression with complete mip chains, the family
costs **17.5 MiB**: 16 MiB atlas, 1⅓ MiB indications and ⅙ MiB names. This is
an engine compression estimate, not the PNG file size or measured VRAM.
A runtime uploading everything as RGBA8 with full mips would use about 70 MiB.

## Materials and why

| Part | Material references | Reason |
| --- | --- | --- |
| Mast assembly | Signals_Atlas; SharedLens_Off / SharedLens_Lit; SharedNames or SharedNames_Lit | One PBR finish across steel, concrete, hardware, cases and camera; separate swappable lens states; one swappable name face |
| Vehicle / pedestrian head | Atlas + the two lens states | Named state meshes remain independently controllable |
| Pedestal | Atlas + the two lens states | Shared case, post, button and instruction-sign trims |
| Push-button attachment / short post | Atlas | Instructions, service sticker, scuffed button and coatings are in the atlas |
| Cabinet, door and service | Atlas | Natural aluminum, rack fronts, breakers, harness and document pocket share one material |
| Span assembly | Atlas + the two lens states | Clamps, steel/copper cable sheaths and head cases reuse the same trims |

The family has four material references at most in one intersection; a span
installation uses three. Lit/dark instances share the same image and UV tile; dark packages retain a
small reflectance factor. Each vehicle cover has an authored 6 mm crown.
An illuminated name uses the existing name image, with no additional texture.
The Rill fixture is mapped into these same manufacturing trims; its original
library file is read only and remains byte-identical.

## Age and sampling

Paint keeps its hue as the exposed top chalks and roughens. Dirt tracks begin
under retained ledges and extend down. Zinc crystallization is restrained;
water retained low on the support leaves zinc oxide, and crevices/cut edges at
the base and nuts carry interrupted oxidation. Upward arm/case faces receive
perch deposits. Concrete has form lines. Cabinet splash stays on the lower
leaf; the service label and document sheet stay attached to their door.
The accessible button has polished contact and short abrasion strokes, with a
small maintenance sticker on its station.

These are shared trims, not a unique island for every repeated bolt or pole.
Intentional chart reuse is checked inside each guarded cell; accidental cell
crossings, outside UVs and zero-area charts fail. The seven-segment digits
intentionally sample a known opaque LED texel, checked in the exported image.
Actual per-primitive density is in build/delivery-check.json. Tall poles have
less density than cases and buttons. This is the main close-range compromise.

The linear BaseColor and ORM fields and meter-valued heights are generated at
4096. The kit's locked GPU flat baker produces PBR maps; channel-correct
filtering produces the 2048 delivery. No photograph enters any field, shader,
normal, label or baked pixel. Noto/DejaVu installed open fonts provide text.

Presentation imports cap only surrounding library image buffers to 512–1024
in memory. Signal delivery images retain the sizes above; source photo pairs
use the original 4096 generated fields. No delivered library image is rewritten.
