# Look-dev allocation, planned after this checkpoint

No final skatepark textures are baked this round. Current glTFs use quick
uniform form materials plus the library's original scripted fence/leaf images.
Source photographs are excluded from every material and image generator.

| Set | Shipped size / maps | Estimated GPU memory, BC7/BC5 + full mips | Purpose |
| --- | --- | ---: | --- |
| Ground Concrete, reused | 2048² BaseColor / +Y Normal / ORM | 16MiB | Riding concrete with reduced broom normal/roughness response; native walk response on pedestrian slabs. Construction joints are geometric seams with a sealant strip. |
| Ground Asphalt, reused | 2048² triple | 16MiB | Prefab pad and parking. Local repair/traffic changes belong to this family, not an edit to ground's accepted maps. |
| Ground Lawn, reused | 2048² triple | 16MiB | Turf and planting interfaces. Native lawn fringes/grass, not a uniform green plate, in the look pass. |
| Skatepark trim + decals, new | 2048² RGBA BaseColor / Normal / ORM | 16MiB | Pipe and block coping, ceramic/grout, steel armor/rails, wax and polished grind lanes, scrapes, concrete repairs, sparse fictional tags and municipal rules. Opaque and alpha states share identical images. |
| Prefab surface/frame, new | 1024² triple | 4MiB | Phenolic laminate, galvanized skin/frame, panel seams, recessed screw impressions and local worn riding lanes. The four-foot panel width retains physical metric density. |

**20MiB new, 48MiB reused ground; 68MiB for all skating/paving/grass sets
loaded together.** A poured-only skating section needs concrete + trim,
32MiB; a prefab skating section needs asphalt + trim + prefab, 36MiB.
These are compressed GPU estimates, independent of PNG disk bytes. Each family
loads a map once across all pieces and seeds. There is no unique whole-park atlas.

Canonical tree, chain-link, furniture and light deliveries add their own shared
library sets. The form checkpoint's reduced source context is not their final
delivery or its texture-memory receipt. Town houses, the extra trees and roads
beyond the lot are presentation only and do not ship in the park glTF.

The age pass must remain visible at player distance: wax darkens and polishes
the actual grind edges; loss of coping paint follows the top contact lane,
oxide the sheltered sides and welded ends. Wheel/board tracks follow ridden
lines and transition lips. Joint cracks/patches occur at actual pours. Water,
leaf fragments and grit collect at the waterfall drain, rather than around
every perimeter uniformly. Tags are original and moderate, confined mainly
to non-riding sides. Prefab wear follows wheel lanes, plate edges and screw
seats. Board impact bends only the lower fence fabric. None of this is claimed
complete by a quick uniform gray form render.

Bake at 4096 and ship at the sizes above, using the kit's channel-correct
filtering. Rejudge every requested photo pair on the baked external glTF;
the form-only UV charts do not prove final texel density or bake quality.
