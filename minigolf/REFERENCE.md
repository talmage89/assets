# Construction and look-development references

The source register is [refs/SOURCES.md](refs/SOURCES.md). Published construction
sections are comparators; no builder's routing, theme, branded architecture or
course plan is reproduced.

| Component | Published anchor | Original implementation, meters |
| --- | --- | --- |
| Playing base | Harris detail sheets: outdoor carpet over concrete no less than 4 in; compacted subgrade | 0.1016 m slab, 4.8 mm nominal carpet skin; authored slopes and breaks |
| Course scale | Harris published 18-hole example: 22,000 sq ft / 2044 m² course area | Classic 49 × 56 m parcel including lot/hut; adventure 64 × 65 m including lot/hut; original holes 5.2–8.6 m long, 2.0–3.6576 m wide; the short welcome bowl uses the published 12 ft width comparator |
| Carpet | Wittek: high UV olefin, 3/16 in pile, 12 ft roll; Verde alternative: UV-stabilized 9.5 mm polypropylene loop | 4.8 mm top skin; original loop-nap normal, traffic flattening and roll/repair seams; no modeled fibers |
| Tee mat | Wittek commercial jumbo 24 × 36 in, 1/8 in thick (2018 catalogue; some later PDF OCR incorrectly reads 1⅛) | .9144 × .6096 × .003175, recessed ball-start pocket |
| Cup | TNT Turf builder: standard 4¼ in golf opening; Wittek aluminum liner class; Harris cup/drain detail | .10795 m clear opening; .1016 m deep, .002 m wall; open carpet/slab cut, recessed bottom, drain opening |
| Edging | Builder's brick paver, concrete border, and commercial timber systems | .1524 m concrete curb, .2032 × .1016 m brick units, .0889 × .1397 m treated timbers; original details |
| Walk | US 5 ft walk size already used in ground family | 1.524 m connected route plus tee/cup approaches; geometry check, not accessibility certification |
| Faux rock | Henderson's rebar framework / shotcrete / waterproofing / plaster | Original asymmetric ledged formations; closed exterior skins describe the shell envelope; hidden frame and inner wall omitted from game geometry |
| Pond | Henderson and Winnipeg specification: protective geotextile, 45 mil EPDM, rock protection, concealed liner at banks | .001143 m liner reference gauge; sloped basin and restrained folds; water .40 m above local basin bottom; .185 m freeboard at low grade, rising with the bank; separate submerged rocks |
| Waterfall | Winnipeg stainless weir; builder pump / return practice | three exposed spill lips at 2.48 / 1.63 / .72 m, 1.15 / 1.55 / 1.90 m wide; receiving ledges, splash pool, screened intake and routed 63 mm return; animated flow deferred |
| Footbridge | Harris plan details use 2 × 6 joists, 42 in guarding | Original 1.524 m clear deck, 3.6 m span, .0381 × .1397 joists and 1.067 m rails |
| Fixtures | Period Commons photos show human-scale lighthouse, windmill and bridges | Original 3.20 m windmill, 4.7 m lighthouse, 6.0 m castle gatehouse, 2.30 m covered bridge; complete ball routes and thickness |

Photo dates: Sunnyvale 2007, Michigan 2011, Castro Valley 2011. No photograph is
used as surveyed dimension data. Pose fits use stated approximate landmark
correspondences between different original designs. The matched images compare the shipped baked GLBs in a complete course setting.
Native-pixel residuals and neutral balancing are reported with each pair; they
are evidence of approximate framing, not surveyed reconstructions.


Middletown's published layout and grading plan gives 22,000 ft² (2,043.87 m²)
and contours roughly 66–73 ft (2.13 m of relief). Oak Island's municipal
packet page 40 shows a second winding, water-crossing course; its memo gives
18,590 ft² (1,727.07 m²). Their densities are 8.81 and 10.42 holes per
1,000 m² of enclosed play area. Our actual post-mesh centroid extrema measure
**1,948.55 m² classic / 2,033.50 m² adventure**, or **9.24 / 8.85 holes per
1,000 m²**. All actual playing-face vertices are checked inside those fences.
Parking and the clubhouse are excluded from all these enclosure comparisons.

The classic common-bed polygon is separately 1,220.92 m² and the adventure
routing window is 1,840 m²; neither is substituted for the fenced enclosure.
`build/routing.json` records those area definitions, sampled green area and
actual source playing-face elevation ranges: .129–.610 m classic and
.130–2.590 m adventure. Thus the adventure's actual playing relief is 2.460 m,
compared with the plan's roughly 2.13 m contour span. These dimensions establish
comparable density and relief, not a traced routing or surveyed reconstruction.

The adventure outer circuit and inner crossings follow a 6.5% rising bank.
Concrete walk decks over the water have actual continuous girders, abutments,
elastomer seats, intermediate piers and outer guards; solid support skins
seat the other raised walks. Source BVH contact distances and exported ball
passage/motion tests distinguish construction checks from serialization.

The lighthouse's revised proportions are measured against the 2007 photograph,
not recalled from a generic lighthouse: gallery / shaft-base width is about
59 / 97 pixels (.61), and finial-to-gallery / gallery-to-painted-base height
is about 76 / 129 (.59). The original fixture uses 1.04 / 1.70 m (.61) and
1.51 / 2.58 m (.59), retaining its authored 4.73 m overall height and unchanged
masonry tunnel footprint. Pixel picks have several pixels of uncertainty;
these ratios do not establish the reference structure's absolute dimensions.
The gallery is decorative course construction, not a public platform.

| Course photograph | Source camera / native-pixel RMS | Declared correspondence |
| --- | --- | --- |
| Sunnyvale 2007, central crop (950,650)–(1750,1900) | 42 mm fixed / 6.58 px | Five actual lighthouse silhouette points; camera 1.824 m above imported upper crossing |
| Michigan 2011, crop (180,760)–(3072,2048) | 36.8 mm fitted / 13.34 px | Four concrete curb-top corners, not carpet-level points |
| Castro Valley 2011, crop (0,900)–(4000,3000) | 55.9 mm fitted / 4.39 px | Front roof tips and cap-axis/eave-plane centers inferred from visible roof outlines |

The first source lens is chosen for a supported course viewpoint, not inferred
from reference EXIF. The original full-frame equivalents are 35 mm for Michigan
and 60 mm for Castro Valley; cropping and differences between original designs
limit interpretation of a fitted focal length. The castle's inferred eave
centers are not surveyed surface points. Independent Blender projection agrees
with the solver within .002 px; opaque-core rays and direct image inspection
check visibility separately. No geometry is hidden, isolated or rescaled for
these pairs. Different surrounding hole/water routing remains visible and is
not covered by the landmark error. Neutral ROI/gains are in
`build/reference-balance.json`; the source photos never enter the materials.
