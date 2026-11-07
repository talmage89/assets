# School site and look-dev checkpoint report

The accepted room grammar, 30 × 32 ft bay, 10 ft ceiling, construction and
hinged assemblies remain. This revision replaces the detached racetracks,
recomposes the parcels, adds era-specific glazing/roof treatment and binds
shared baked PBR. It stops before documentation images or a README gallery.
Root README and kit are unchanged. No push is made.

## Three places

| Seed | Decades and arrangement | Parcel / entry | Building triangles | Static campus triangles | Views |
| --- | --- | --- | ---: | ---: | --- |
| 101 Cedar Fork | 1956 fingers, 1963 communal/service block, 1984 cross wing | Mid-block / south | 70,055 | 275,916 | [Hero](renders/lookdev/101/hero.png), [above](renders/lookdev/101/above.png), [plan evidence](renders/site-evidence/101-plan.jpg) |
| 102 Briar Court | 1964 four-room courtyard pods, 1988 rear row | Corner / east | 70,585 | 281,641 | [Hero](renders/lookdev/102/hero.png), [above](renders/lookdev/102/above.png), [plan evidence](renders/site-evidence/102-plan.jpg) |
| 103 North Vale | 1976 compact media core, 1991 addition | Park-backed / north | 57,452 | 258,005 | [Hero](renders/lookdev/103/hero.png), [above](renders/lookdev/103/above.png), [plan evidence](renders/site-evidence/103-plan.jpg) |

These are placed export counts, including native parcel foliage and fences.
Buildings have six materials, campuses 22. The compact school stays below
60k rather than adding geometry without a visible purpose.

**Vehicle cost is separate and material.** Two intact library hatchback source
actors add 116,064 triangles. Including them, the occupied parcels cost
391,980 / 397,705 / 374,069 triangles, above the original 300k whole-site
ceiling if that ceiling includes moving vehicle actors. The standalone
static campus packages remain below 300k. I have not hidden that difference
inside a unique-mesh count or altered the cars to recover it. The surrounding
native houses, continuing streets, trees and utility lines are presentation
context as well, outside these package counts. Per-view provenance records
their full placed cost. Their source finishes and the vehicles' period remain
weaker than the school look; period changes belong to the lead.

## Each requested form fix

| Fix | Result and evidence |
| --- | --- |
| Loading drives | Open one-way bus lanes follow long school-side loading curbs, joined to graded entry plazas. Parent curbs use another route and the staff approaches. Real curb openings/aprons meet native streets. [101 plan](renders/lookdev/101/plan.png), [102 plan](renders/lookdev/102/plan.png), [103 plan](renders/lookdev/103/plan.png). Bus places remain sockets. |
| Repeated skeleton | Entry headings, frontage count, staff lot, play/field locations and portable positions differ. The courtyard gym/kitchen/boiler are on the opposite side of its office from 101. Above views in the first table show the complete layouts. |
| Blacktop | Large asphalt yards meet teaching wings, with basketball, four-square, hopscotch, an illustrative state map, perimeter track, tetherballs and hoops. Playground socket/fence beside each; practice field and backstop beyond. [101](renders/lookdev/101/blacktop.png), [102](renders/lookdev/102/blacktop.png), [103](renders/lookdev/103/blacktop.png). |
| Blind early walls | Broad steel sash, low spandrels, hopper bays, sunshades and corridor clerestories distinguish early fingers/pods from 1970s slots. Replacements retain cleaner aluminum and some upper infill. [101](renders/lookdev/101/windows.png), [102](renders/lookdev/102/windows.png), [103](renders/lookdev/103/windows.png), [original steel ribbon pair](renders/look-matches/ribbon-pair.jpg). |
| Repeated roofs | Longitudinal gable, low pod gables, deep overhangs, framed monitors and flat granular cover; equipment size/count follows wing use and age. Curbs seat on actual roof planes; vent bases follow pitch. [101](renders/lookdev/101/roof.png), [102](renders/lookdev/102/roof.png), [103](renders/lookdev/103/roof.png), plus all aerials. |
| Empty grounds / world edge | Five native mature trees and four foundation shrubs per parcel, signs/marquees, racks, lights and yard/field fences. Native colonial/ranch/cape houses, streets, poles on real conductor sockets, slack conductors and surrounding trees give neighborhood context. Park woodland replaces the compact site's rear house row. |
| Repeated flat heroes | Each camera stands along its own drop-off approach, at 1.68m with a 40mm lens. An approximately 18° sun rakes the facade. New heroes are linked above; old-camera comparisons retain the original world camera, lens and direct-light settings. |

The complete [Cycles contact sheet](renders/lookdev/contact.jpg) includes the
window, entry/canopy, gym, hardware, roof, scale, rear and site views. Each
rear view includes the kitchen/service compound and blacktop. Each seed's
`provenance.json` identifies its export including every referenced image hash.

The [before/after contact sheet](renders/before-after/contact.jpg) links twelve
pairs: hero, aerial, rear and window camera for each school. Each panel is
1400px wide. Campus headings change beneath the unchanged world cameras;
this deliberately shows different facades in some old close-up cameras.
The new targeted views remain beside that literal comparison. Original
checkpoint scripts can be rebuilt from repository revision `1fd7b37` under
`build/baseline/`; the isolated rebuild reproduces all six original binaries
byte for byte and the original counts/bounds.

## Sites against published plans

The comparison diagrams describe authored relationships, not surveyed or
traced copies. Exact citations and rights are in [REFERENCE](REFERENCE.md)
and [the source register](refs/SOURCES.md).

- 101 uses the incremental finger/yard relationship in the LAUSD 1956 plan,
  Figure34, and 1960 aerial, Figure36, in Sapphos' 2018 historical assessment.
  Its blacktop lies against the fingers/cross wing, parking beside them and
  field beyond. The original parcel is narrower and more urban than ours.
- 102 uses CDE's 2000 guide, printed p41 / PDF50: a long bus loading approach
  by administration/multipurpose, separate parking access on a second
  frontage and hardcourts beside teaching blocks. McDowell's written
  nomination supplies mature planting/multiple frontages; its missing scanned
  supplementary site plan is not claimed as inspected evidence.
- 103 uses the LAUSD 1974 plan, Figure39, and 1977 aerial, Figure41, for the
  later office/communal growth and shared large yard relationship. The
  compact grammar and park-backed parcel are original design decisions,
  not something inferred to exist in that finger-plan reference.

These sources support planning relationships, not complete vehicle swept
paths, a certified school program or the geometry of an unmeasured curb.

## Materials, age and pairs

No new school image set. Brick is CommercialBrick (101) and native RanchBrick
buff/tan (102/103), 512 triples. Painted CMU and concrete are Commercial1024
triples; equipment/trim is the Commercial2048 atlas. Granular roof cover
reuses the mineral maps at a coarser scale, without the rejected asphalt
binder grid. Glass is stock transmissive PBR. Manufacture comes from original
4096 bakes; shared image files remain unchanged.

Buildings reference twelve images / **25 MiB** each. Campuses reference 33
shared images / **113 MiB** each. The six exports' union is **37 images /
114.33 MiB**, 74,509,897 PNG bytes. Estimates assume 8bpp block compression
and full mips. These are shared loaded costs, not new school texture memory;
presentation context is additional. Exported physical UV densities and
material/image allocations are in `build/delivery-audit.json`.

Splash acts at wall feet; runoff follows actual scuppers and clear masonry
piers; pale repointing/mineral strips stay on mortar beds. Column-base rust,
sash-joint paint history, door-edge handling chips, asphalt trench repairs,
crack sealant, worn lawn shortcuts and faded game/parking paint follow their
causes. Placement-owned corner color carries macro aging; shared baked maps
carry fine manufacture. These are stock exported glTF surfaces.

[Exported photographic pairs](renders/look-matches/contact.jpg) compare Walls
in daily use (2010), McDowell in daily use (1973) and the archival Emerald
covered walk (1958). [Source-scene pairs](renders/source-matches/contact.jpg)
check the same appearance before consolidation/export. Neutrals are the
sunlit concrete curb, white-painted spandrel and pale monochrome fascia.
`build/reference-balance.json` records the assumptions. The ribbon uses a
bounded short-lens fit in a clear courtyard gap; it is not an EXIF recovery.
Camera fits compare original designs by features rather than photographic
replicas. RMS residuals remain explicit in each pair and calibration receipt.

## Proof and limits

`make`, `make check`, `make repeat`, camera verification, the shared-image/UV
audit and repository checks are the acceptance commands. Detailed receipts
and exact geometry-plus-glTF file bytes are under `build/`; README lists the
rebuild entry points. Physical source checks are separate from fresh-import
serialization checks. The audit measures rooms, door/casing/ground clearance,
roof-curb seating, traffic-paving separation and reservation intersections.
It checks 300 grammar seeds and all 772 pre-existing delivery files outside `school/`.

The added critique passes begin with color/value in [REVIEW](REVIEW.md),
including rejected roof bindings, blocked views and camera failures. The
remaining CG tells are broad even lawns, repeated native foliage/context,
simple room backings and regular blinds, sharp door chips, repeating masonry
in close-ups, simple HVAC and subtle roof aggregate. Small mineral repairs
are weaker at full hero framing than the larger drainage/splash shading.
The state-map graphic and practice field are illustrative. The scene is not
a product-photograph match or a complete interior, engineering, vehicle
swept-path or code-compliance model. No requested docs images are committed.

The lead should review the explicit moving-vehicle budget treatment above.
A useful later kit addition would be a general completed-ground door sweep
and a camera-visibility check: numerical landmark projection alone accepted
a camera inside a later addition. No kit change is made here.

The completed command receipts are `build/lookdev-final-make.log`,
`build/final-repeat.log` (49 files identical), `build/final-check.log`,
`build/final-render-audit.json`, `build/baseline-verify.json`,
`build/delivery-audit.json` and `build/tonal-check.json`. Follow-up scale,
gym-light and Eevee renders pass with their logs under `build/final-*.log`.
Repository check: 1,947 source files, zero errors. All 35 rooms pass, 43
exterior leaves clear the completed ground through 903 poses, and 22 actual
roof-curb seats pass. Whole-frame hero highlights have zero all-channel
clipping. The final sheet includes 45 Cycles views and the Eevee preview.

| Package | Geometry + glTF bytes, excluding shared images |
| --- | ---: |
| School-101 / Campus-101 | 9,667,423 / 21,176,867 |
| School-102 / Campus-102 | 9,800,951 / 21,741,690 |
| School-103 / Campus-103 | 7,891,876 / 18,650,644 |
