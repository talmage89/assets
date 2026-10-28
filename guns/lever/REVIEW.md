# Bracken L20 — form and motion review

This is the requested stop **before look-dev**. Inspection colors are constant;
the walnut has no grain or dings and the steel has no wear. This review does
not accept their final appearance. The source is an original visual game asset
with deliberately incomplete internals, rather than a mechanically functional
reproduction. Published dimensions and authored animation estimates are kept
separate in [README.md](README.md) and [refs/SOURCES.md](refs/SOURCES.md).

## Reference treatment

The lower carbine in Hmaag's CC0 right photo is the main straight-grip .30-30
proportion reference. The upper long rifle is excluded. Cjp24's sharp left
profile/close-up is a different .375 variant; it constrains construction and
viewing angle, not its checkering, finish or exact stock contour. Hmaag's
`receiver.jpg` really shows the action open. `open.jpg` and `open2.jpg` are
closed oblique action views despite their cache names. No photo is mirrored.

Every paired photo is adapted in linear RGB before composition. The right
photo uses unclipped white paper below the lower gun. The left profile uses
a bright bare screw-slot facet; the open-action photo uses a polished pivot
screw facet. The oblique left uses a polished cross-pin highlight, and the
right/top reference uses a broad bare bolt flat. Native rectangles, gains,
valid pixel counts and marked originals are in
`build/white-balanced/corrections.json` and `*-neutral.jpg`.

The small silver facets reflect their surroundings. They are estimated
neutrals, with remaining cast visible in the photographs, not measured gray
cards. No albedo is recovered from them at this gate. In particular the old
steel's residual blue is not copied into our steel. Later finish acceptance
needs additional neutrals and used-surface value measurements.

`kit/photo_match.py` fits comparison cameras from manually selected anatomical
landmarks, without supplying geometry to the model generator. A narrow prior
on estimated camera height prevents the planar side landmarks from inventing
a very low right camera or an overly elevated open-action view. These are
estimated views, not recovered EXIF. Lens, residuals, projection overlays and
height assumptions are retained in `build/cameras.json` and the calibration
JPGs beside the pairs. Different original contours prevent exact registration.

## Image critique history

The early previews remain ignored under `renders/pass1/` through `pass6/`.
They document rejected iterations, not final delivery. Each pass began by
looking at value/color before construction and silhouette.

1. **Initial form.** Against the native Commons references, the furniture
   looked pale and the steel too uniformly bright. Quick colors were darkened
   and the lighting kept neutral. The first assembly exceeded the triangle
   ceiling and had unsupported/overlapping linkage and feed parts. Those were
   rejected. Hidden tube rounds were simplified, screws budgeted, and cavities,
   real bearing bores, lock seats and supported linkage built before proceeding.
   Inspection sheet: `build/lever-pass1-sheet.jpg`.
2. **Machined planes and proportions.** Value remained provisional. The
   receiver's large flat faces showed triangular highlight fans; the body was
   too long and the forend too short beside the photos. Broad plane normals
   were corrected, the receiver rear moved to its current shorter envelope,
   and the compound forend lengthened. A box-like butt return was replaced by
   a genuinely curved steel plate seated against the wood. Inspection sheet:
   `build/lever-pass2-sheet.jpg`.
3. **Construction at first-person scale.** The dark cavity/readable edge
   balance was improved, but the stock head still read as an open wooden
   trough, and the upper tang was too broad behind the wrist. The tang was
   narrowed aft, the unnecessary deep mortise removed and clearance cut from
   an envelope of our own moving hammer. Bands were fitted to actual sections,
   rather than merely placed around nominal radii. Native images are in
   `renders/pass3/`.
4. **Rejected forward-hammer trial.** Quick values were stable. Moving the
   hammer forward reduced the opening but made its base clash with the carrier
   bearing and sear arm. The sweep rejected that trial even though the static
   contact assertions passed. The image still showed an oversized spur and
   exposed trough. It was not accepted. `renders/pass4/hammer.png` and
   `stock.png` show the trial.
5. **Shorter forged hammer.** The thumb pad remained too bright/plain for a
   finished gun, which is deferred. The shape was shortened and the internal
   pivot raised; the sear support was rerouted. The stock slot became smaller,
   but the tang lay below the head's surface. Its forward path was raised to
   follow that surface. A real bolt passage and broader front rails replaced
   the interpenetrating front. `build/lever-pass5-sheet.jpg` and
   `renders/pass6/hammer.png` expose the difference.
6. **Calibrated photographic review.** The paired right/left/open images
   exposed the trigger's overly hooked toe and heavy blade. Its curve was
   softened and width/thickness reduced while retaining the muzzle-facing
   concavity. The first camera solution showed too much top surface in the
   open view; camera-height priors now keep the comparisons closer to the
   photographs. The lower link, original lock relief and demonstration feed
   remain visibly simpler than the class's hidden mechanism; they are recorded
   as visual design limitations below. The hammer now has separately supported
   full-cock and half-cock lands. Its bolt-overtravel pose remains depressed
   until the returning bolt is clear, rather than intersecting the pin tail.
7. **Ammunition macros and inspection contrast.** The standalone white floor
   and exposure washed out brass, so the macros now use a transparent surround
   and lower exposure; the sheets composite them onto neutral gray. Large
   triangular case highlights revealed that registration discarded the
   analytic revolution normals. Those normals are now applied after
   registration. The head face also concealed the struck primer: a round
   shallow seat and a denser primer face expose its actual dent. Independent
   imported-surface rays measure a 0.22 mm dent with 0.07 mm axial thickness
   behind its center. The visible case-seat rings were increased without
   changing the eight-sided occluded tube variants. The finished checkpoint
   remains below 40k triangles. Workbench strips now have enough contrast to
   read the complete gun and flying case against their gray surround.

8. **Empty-cycle dependency.** Final clip inspection caught that the empty
   branch skipped the carrier lift. It now follows the same cam stroke as a
   loaded cycle, including the last-case and empty demonstration clips. An
   independent pose assertion checks the raised carrier even with no round.

9. **Tang seating from the final sections.** The earlier wide tongue was
   supported at its center but overhung the round wrist at its edges. The aft
   tongue is now narrower and nearly flush, broadening only into the head; a
   changing carved crown supplies its actual inlet land. Eight underside-land
   surface probes check both edges through the wrist/head instead of inferring
   support from one minimum distance. A buried fork connects the narrow rear
   tongue to both receiver cheeks below the race; a slotted retention screw
   seats on the tongue. Every disconnected tang component must independently
   meet the receiver, so a decorative floating rear plate cannot pass. The
   stock remains a compound cage.
10. **Closed cuts and normal-field polish.** The inlet now uses our unrelieved
    tang solid with a 0.03 mm outward normal offset, rather than scaling a
    hollow part and enlarging its voids. Distinct stock/steel race floors avoid
    coplanar cuts. Concave Boolean polygons are ear-clipped before reduction;
    only zero-volume triangle fins with two boundary edges and one overfull
    edge are pruned. Source and reduced stock/tang remain closed at each stage.
    The reduced wood receives the retained cage's smooth vertex-normal field,
    without adding triangles or textures. The tang's machined horizontal cap
    has a flat normal field. These remove the triangular highlight fans visible
    in `renders/pass10/`; `renders/pass11/` shows the correction.

Final checkpoint inspection, region acceptance and measured proof follow below.

## Form acceptance list

These are form judgments from the native views and paired photographs, with
remaining differences stated explicitly. They accept the original construction
for this checkpoint, not the provisional surfaces as finished hunting wear.
Paths below are generated, ignored files relative to this folder.

| Region | Image acceptance and difference from the photograph |
| --- | --- |
| Receiver and loading gate | [x] `views/receiver.png`, `receiver_left.png`, `gate_open.png`; right/left pairs. The cheeks read as thick machined steel, with actual top/bottom openings, screw seats and an inset spring cover. Our cover is longer and more rounded, the screw pattern original, and the rear opening/tang broader than Hmaag's older carbine. The absent fine surface variation remains obvious at this stage. |
| Lever | [x] `views/lever_open.png`, both raking views, `pairs/open_photo-pair.jpg`. It reads as a forged flat bar with two apertures and a supported pin on the dropping link. Our finger loop is more oval, slightly thicker and shorter than the photographed historic loop. Its rear latch neck and the open link have simpler original contours. |
| Bolt, locking block and carrier | [x] `views/open.png`, `open_left.png`, open pair and Cycle strip. The bolt remains supported while withdrawn; the top opening exposes the carrier and its round. Our underside race and extractor provide construction, but the forked lock, exposed lower link and carrier web are simplified visual internals. The photo does not verify the hidden fork or cam paths; that limitation is retained. |
| Hammer | [x] `views/hammer.png`, `aimed.png`, both source/export pairs. The shorter forged body and broad spur replace the oversized early trial. Our pad remains more angular and wider than the old photograph. Dense crossed cuts exist but are not yet baked into the game surface. Full-cock and half-cock supports are separately measured. |
| Trigger | [x] `views/trigger.png`, `trigger_quarter_view.png`, both trigger pairs. The concavity faces the photographed muzzle, with a restrained forward toe; three actual surface rays independently check that direction. Our blade is shorter and has a somewhat fuller toe than the historic photographed blade. It is a radiused flat section, not a rod. |
| Sights | [x] `views/sights.png`, `front_sight.png`, `aimed.png`. Dovetail, leaf, stepped elevator, open buckhorn, ramp, blade and bead read as separate construction. Our horn tips are broader and more open than the tiny sights in the whole-gun reference. The exact eye view shows the bead centered in the notch with its top level with the shoulders; receiver/barrel surfaces remain below. |
| Barrel, magazine and bands | [x] right/top/front orthographic views, `forend.png`, front-sight view and side pairs. The round barrel has an open crown and taper; the full-length tube ends just behind it. Both bands fit actual surfaces. Our front band has simpler clamp detail, and the forend band sits nearer the wood's nose than the older primary right photo, closer to the later left reference's layout. |
| Butt stock and butt plate | [x] `views/stock.png`, `butt_plate.png`, both raking views, `sections.jpg`, side pairs. Changing sections show rounded compound wood, a straight wrist, comb and belly; the plate is curved across its face and seated. Our comb/wrist transition is fuller and our crescent shallower than the older right photo. The later checkered photo has a different stock and is not copied. |
| Forend | [x] `views/forend.png`, side pairs and three section stations. The wood wraps a rounded barrel channel with broad lands, varying belly and a shaped nose, without knife lips. Our nose is fuller, and its plain uncheckered surface differs from the later .375 reference. Grain, dings and hand oil are intentionally absent until look-dev. |
| Ammunition | [x] `cartridge/cartridge.png`, `cartridge/headstamp.png`, `case/case.png`, `case/mouth.png`, `case/headstamp.png`; C.I.P. exterior table and the center cartridge in Barowski's photo. The rim, long neck, jacket/lead distinction, hollow fired mouth, struck primer and fictional headstamp read clearly. Our required flat nose differs from that photo's rounded soft point. The smooth brass lacks the photographed axial scratches and oxidation; those belong to the later atlas. |

All view paths in the table are under `renders/checkpoint/`. Additional source
pairs are under `renders/checkpoint/source-pairs/`. Form acceptance retains the
listed original contour differences; it does not claim photographic identity.

## Round-trip correction

The first complete source sweep passed while fresh imported Cycle/Chamber
failed at f49.5. glTF sampled a zero-scale CarrierRound at f50 as an identity
rotation, so interpolation prematurely tipped the still-visible cartridge into
the barrel and forend. FiredCase similarly lost rotation just before f34.
STEP visibility itself was correct. Motion now belongs to nonscaling
CarrierGuide/FiredGuide bones, while their children control display alone.
Targeted half-frame source/import comparisons and the imported Chamber sweep
confirmed the correction before repeating the complete checks.

The initial Makefile also expanded BP/PYTHON before the kit defined them.
Recursive expansion fixes both commands. That initial failed run is not counted
as a passing build. The final reported make run uses the corrected graph.

## Planned hunting wear, after this gate

| Named site | Finished appearance and cause |
| --- | --- |
| Receiver corner rubs | Narrow broken bright-gray steel along handled/projecting corners; dark bluing retained in recesses |
| Receiver bottom rubs | Directional gray contact streaks below the action, confined to exposed bearing/handling areas |
| Receiver plum flats | Uneven thin bluing with a restrained plum/brown cast on exposed flats, not a uniform noise wash |
| Lever hand arcs | Smooth polished-gray bands on the lower and inner finger loop where fingers ride |
| Gate lips | Thin bright steel at the spring cover's mouth and handled edge |
| Band shoulders | Small edge rubs on projecting steel, no dirty halo on adjoining wood |
| Muzzle rim | Fine radial and axial scuffs at the accessible crown rim, bore kept dark |
| Toe/heel crush marks | Small directional compressed/darkened walnut dings at exposed corners |
| Forend edge dings | Sparse broken dents on grasped and bumped wood shoulders |
| Wrist hand oil | Darker, smoother walnut around the palm contact, following carved fiber |

No finish effect is accepted from a close-up alone. The later baked hero must
show the localized use at full frame without washing out steel or walnut.


## Recorded verification

The checkpoint `make` graph runs the source construction/state sweep, fresh
GLB verification, repository check, imported geometric topology check and all
presentation stages. `make repeat` performs a second independent build.
The final inspection uses the exported game GLB, including its provisional
materials; high-source pairs are supplementary and explicitly labeled.

Recorded successful commands:

```text
make -C guns/lever                 exit 0, including check and fresh-import sweep
make -C guns/lever repeat          exit 0, independent rebuild comparison passed
python3 kit/repo_check.py          exit 0, 781 source files, 0 errors
python3 -m compileall -q guns/lever/src guns/common/ammo_3030.py guns/common/interface_v1_5.py
                                  exit 0
git diff --check HEAD              exit 0
```

- **39,768 gun triangles**, including all ammunition representations; 118 named
  inspection meshes, seven constant material classes, zero texture images.
  Gun GLB **2,649,528 bytes**. The standalone live round is **1,598 triangles /
  58,656 bytes / five materials**; the fired case **1,326 / 47,052 / three**.
- **67 required contacts/support probes** pass in the source and fresh import.
  The worst measured gap is **0.11815 mm**, inside its stated limit. All eight
  tang bearing-land gaps are at most **0.05892 mm**. Each tang component has
  an actual triangle intersection with the receiver. This establishes stated
  construction, separately from serialization agreement.
- **232 intended event/state checks**, the complete count chain, insertion
  interruptions, standalone origins/scale, visible fired-primer dent and its
  remaining thickness pass. Carrier travel is checked on empty cycles too.
- All **37 clips** pass the kit's half-frame clearance sweep: **5,271 source /
  5,304 imported samples**. There are no violations of the declared policy.
  Explicit chamber/bearing contacts and connected hand-envelope overlap retain
  finite bounds in `src/check.py`; this is not a continuous collision proof or
  an anatomical hand simulation.
- **5,271 full affine samples** compare every bone and all ten socket frames.
  Maximum position difference **1.975 micrometers**, maximum linear-component
  difference **0.00000781**. **185 event/end-frame surface comparisons** have
  maximum distance **0.121 micrometers**. These establish serialization.
- Raw exported normals are finite/unit and face outward relative to winding;
  skin weights are rigid and sum to one. All **118 imported geometric solids**
  are closed after check-only welding of duplicated normal/attribute seams at
  **0.01 micrometers**. Unwelded raw seam edges are retained in the geometry
  record for transparency; delivered meshes/normals are not welded by the test.
- The repeat build has identical vertex/normal/skin/animation accessors,
  metadata and oriented triangle sets. Only identical bead triangles can be
  serialized in a different order. Both ammunition GLBs reproduce byte-for-byte.

The dimensional sheet records **965.20 mm overall, 508.00 mm barrel, 340.18 mm
pull, 42.54 mm width and 183.92 mm height**. The section labels describe the
combined section envelope where barrel/tube/bands are included; the flat at
Y=330 mm is the actual rear-sight dovetail seat. The high/low outlines coincide
closely while retaining the varying stock and forend sections.

Camera RMS residuals are **14.10 / 23.08 / 10.46 pixels** for right/left/open,
**3.97 / 3.40 pixels** for trigger side/oblique. These estimated photographic
fits are distinct from the kit's subpixel camera-projection implementation
check. They are not claims of exact contour identity.

`build/check.json`, `serialization.json`, `topology.json`, `determinism.json`
and `provenance.json` retain the complete measurements. `renders/checkpoint/`
contains the contact sheet, regions, dimensions, sections, both photo-pair
sheets, whole-gun strips and eleven action-detail strips. The 37 whole-gun
and eleven detail WebPs retain their encoded real durations; static holds
retain their duration as well.

The final visual audit opened the regenerated contact sheet, region views,
dimension sheet, actual section cuts and both sets of photographic pairs.
All 1,025 whole-gun/detail clip samples were accounted for by decoded-pixel
hashes; their 132 distinct images were opened in six inspection sheets. Exact
duplicate holds share that inspection, rather than being mistaken for missing
poses. Together with the 38 still/pair renders, provenance records **1,063
current-source images**. The audit confirms the smoother stock highlights and
seated tang visible in the last correction, while retaining the region-by-region
photographic differences above. It does not accept the inspection materials as
finished surfaces.

## Remaining limits and next gate

The original loop, stock/crescent, gate and horn contours still differ from the
photos as itemized above. Lock/carrier/fire-control internals are incomplete
visual constructions; feeding contains declared occluded representation
handoffs. The eye's 368 mm placement is an authored ergonomic estimate with a
qualitative cheek-weld reference, not a published dimension. The 3.1 kg mass is
only a class target. Inspect supplies an internal hammer-touch presentation;
the consumer supplies whole-instance turns and hand IK.

Finish, wear, grain, UV/density checks, the 4096-to-2048 bake, final atlas
consolidation and textured delivery remain after lead form review, as requested.
No docs JPGs or generated binaries are committed at this gate. No kit or
existing common/gun file changed. A future kit guide/display helper and a
hide-boundary fixture would make the zero-scale export pitfall harder to repeat.
