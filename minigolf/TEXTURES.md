# Texture plan — pending look approval

The gate uses a 256² color/ORM swatch pair and a 1024² original graphics sheet,
shared through canonical external PNG URIs by both glTFs. They are diagnostic
quick materials: no baked normal, manufactured carpet fiber, final aging or
finished UV density is claimed. Swatch UV overlap is intentional.

After form approval:

| Shared set | Maps / ship size | Compressed GPU with full mips | Purpose |
| --- | --- | ---: | --- |
| New course surface atlas | 2048² BaseColor, +Y Normal, ORM; bake 4096² | 16 MiB | Three carpet hues with repeated fine fiber; stratified faux rock; fixture paint, exposed plywood, metal, rubber, cup aluminum and water ripple regions |
| New original graphics | 1024² RGBA BaseColor | 1⅓ MiB | Numbers/par, fictional business signs, scorecards; measured physical type sizes |
| Reused Ground Concrete | Existing 2048² triple | 16 MiB | Slabs, curb edging, walks, clubhouse foundation; UVs follow meters |
| Reused Ground Asphalt | Existing 2048² triple | 16 MiB | Parking court; local traffic/joint/repair masks without changing shared images |
| Reused Ground Lawn | Existing 2048² triple | 16 MiB | Maintained planted grade; cutout bank/stream construction |
| Reused fence lumber | Existing privacy 2048² triple | 16 MiB | Native perimeter modules where their stock members serve; fixture-specific wood stays on course atlas |
| Reused Shrubs | Existing 2048² triple | 16 MiB | Linked Boxwood landscaping, once for all plants |

New allocation: **17⅓ MiB**. Complete course site using every reused set above:
**97⅓ MiB**, independent of hole/fixture count. Library trees and town context
add their own existing sets only for presentation; they do not ship in the
course checkpoint. A scene already using Ground/fences/shrubs pays only the
17⅓ MiB new allocation. PNG disk bytes are not GPU allocations. Numbers assume
8 bpp per map and 4/3 mip overhead; uncompressed uploads cost more.

Target opaque course palette is one material, with separate graphics and
water/lens transmission states sharing the same images where possible. Three
Ground states, lumber and shrub foliage remain separate for physical scale and
shared identity. Expected complete planted site: eight states, with material
primitives counted per module and moving member. This is a large-site palette,
not one unique set per hole.

Fine wear belongs in maps or vertex-controlled macro tint, never extra dense
geometry: tee and cup traffic, carpet glue seams and stitched patches, edge
paint failure and repaint boundaries, mineral crust/algae at wetted rock and
liner, corner leaves, standing water dirt and golf balls in the pond. Each has
a cause mask. Full-frame used-photo comparison must prove that it survives.
None of those final wear effects is certified at this form gate.
