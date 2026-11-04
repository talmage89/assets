# Planned shared commercial maps — no delivery bake at the form checkpoint

All fields will be generated at 4096 and filtered to the sizes below, following
houses' shared external-image delivery. Repeat UV overlap is deliberate on
building tiles; trim/graphic faces stay within guarded finish cells. Source
photo pairs will be repeated on the actual final glTF after the eventual bake.

| Set | Ship maps / size | Physical use and reason | BC7 / BC5 + full mips |
| --- | --- | --- | ---: |
| CommercialCMU | Color / Normal / ORM, 1024² | 2.4384 m repeat, 8 × 16 in construction; normal strength distinguishes smooth/split faces. Broad store and future tenant/end walls need repeat density. | 4 MiB |
| CommercialBrick | Color / Normal / ORM, 512² | 1.2192 m repeat; neutral mortar and per-unit kiln tones, shared by station and strip mall. | 1 MiB |
| CommercialEIFS | Color / Normal, 512² | Fine aggregate finish; scalar .88 roughness / 0 metal avoids a redundant ORM. | ⅔ MiB |
| CommercialRoof | Color / Normal, 512² | Large low-detail membrane behind parapets; scalar .93 roughness / 0 metal. | ⅔ MiB |
| CommercialTrim | Color / Normal / ORM, 2048² | Storefront extrusions, coping/hem, painted/bare metal, RTU louvers, soffit folds, door hardware and service gear. One sheet serves both building types and their fixtures. | 16 MiB |
| CommercialEquipment | Color / Normal / ORM, 2048² | One shared dispenser/prop atlas: close card reader, nozzles, cabinet seams, air machine, ice cabinet, cage, refuse and guards. Shared repeated pumps justify 2K; no per-pump sets. | 16 MiB |
| CommercialGraphics | RGBA BaseColor, 1024² | Both fictional brands, 0–9 digits, grade labels, posters and safety graphics. Guarded equal-size cells let brands and prices swap through UV selection. Glass/emission use scalar state and the same pixels. | 1⅓ MiB |
| **New commercial allocation** | **17 images** | Reused once across all seeds and the later strip mall. | **39⅔ MiB** |
| Ground asphalt + concrete | Existing two 2048² triples | Canonical ground-family original fields; 6.096 / 3.048 m repeats. No new commercial paving maps. | **32 MiB already allocated when ground is loaded** |
| **Whole commercial family with required paving** | **23 unique images** | Includes all wall variants; a CMU-only station need not load brick/EIFS. | **71⅔ MiB** |

These are allocation estimates, assuming 8-bpp BC7 color/ORM and BC5 normals,
with complete mip chains. A 2048 triple is 16 MiB, a 1024 triple 4 MiB, a 512
triple 1 MiB; a single 1024 RGBA image is 1⅓ MiB. PNG sizes are unrelated.
Canonical ground URIs or an importer texture-ID cache must be retained so the
road and station do not upload identical paving images twice. A standalone
commercial package still needs those two triples once. Loading the entire
64 MiB ground family plus commercial adds only 39⅔ MiB: 103⅔ MiB combined.

At this checkpoint, **one generated 2048² transparent lettering sheet per station
and scalar quick materials** support form review. It is not a finished atlas or baked
texture delivery; current material slots and its preview PNG are not final GPU
claims. Every pixel is generated from our strings and installed open DejaVu
fonts. Photos never become texture inputs. Raised logo placeholders will become
fixed graphic panels; geometry identity across brand swaps remains a delivery
check, not a claim of this prototype.

Future wear remains cause-driven: parked-engine and fueling drips, turning tire
paths, repaired trench/cracks, joint deposits, door/base gum/grime, low bollard
scuffs and rust, coping/fascia runoff, low masonry salts and south-facing fading.
Broad fields can use ordinary RGBA8 vertex tint as houses do; microstructure
stays in tiles/trim. No uniform noise wash, scattered wall peeling or extra
whole-station unique atlas is planned. Full-frame and used-photo checks must
judge the strength after baking.
