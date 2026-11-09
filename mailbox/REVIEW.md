# Mailbox review

Pass 1: opened the closed/open source, mechanism and timber details and the
manufacturer pair. The traditional silhouette and hollow/open door read, but
flat roof strips, an accidentally rotated print, very pale wood and a matte
charcoal finish made it look synthetic. Smoothed curved sheet normals, repaired
print-corner UV ownership in the kit, added lengthwise fibers and end grain,
and changed the powder coat to a darker, glossier black. Eagle, branded handle
and approval stamps are deliberately not copied. The camera initially had the
crop origin subtracted twice in the asset landmarks; corrected that error.

Construction sweeps found a crown/catch collision, lower door/pin interference,
and an inboard bracket crossing the swinging face. Bent the catch above the
crown, lowered the hinge axis 0.5 mm, moved the fixed cheeks outboard and joined
them to the shell with anchored tabs. Hinge ears now have real bores. Source
sweeps at one-degree steps pass with a 0.05 mm tolerance, not a relaxed visual
exception. The kit's documented spring and pin contacts stay narrowly named.

Pass 2: opened revised source views and the correctly framed photograph pair.
The address reads, roof reflection is continuous and flag/door poses work.
End grain exposed a shader-vector output error (noise blobs rather than rings);
replaced it with explicit radial arithmetic and softened the ring contrast.
Darkened/glossed the finish to approach the photographed powder coat. Camera
fit is a construction comparison against a slightly larger modern box, not a
claim of reproducing the manufacturer's envelope or hardware.

First GLB review: motion passed, but the address was a black rectangle. The
separate source print sheet shadowed the underlying door during AO baking.
Moved the original print shader/UVs onto the actual stamped front face, removing
the extra print plane entirely. Rebake required. End-grain ring contrast was
softened and its phase varied spatially to avoid perfect target rings.

Final corrected GLB: opened every Cycles view (hero, front/side/back/top,
mechanism/timber details, human scale and open pose), Eevee, contact sheet and
`renders/review4-glb/shell-pair.jpg`. Address 1847 now reads with no black AO
rectangle. Roof curvature, returned door and independent flag survive the bake.
Tiny hardware has stronger/darker contrast and fine fibers soften at 1024; the
wood is deliberately lightly weathered, not deeply split. The larger modern
photograph still has a glossier finish and different latch/flag details. The
final pair includes the real exported support below the reference-only box.

`make all match-final PASS=review4` passes, including all normal `make check`
prerequisites: 1,264 triangles, one material, three 1024 maps, 1,300,792-byte
GLB, 71.15% UV coverage and no overlaps. Reimport position error is zero.
The imported Door/Flag sweeps test 106/91 positions, with zero measured
penetration at 0.05 mm tolerance and no allowed-contact exclusions. Thirteen
support tests pass on actual game surfaces. The isolation report records three
projection groups and eight stationary AO shadows. This uses the merged kit
features, not a manual bake fallback. No continuous-sweep guarantee is claimed.


## Phase 2 combined-kit regression and wear calibration

Clean baseline `make` / `make check` passed: 1,264 triangles, one material,
1,300,792 bytes. Opened committed/new hero and full Cycles/Eevee contact:
construction, framing, open Door/raised Flag and hardware agree. The new-looking
finish is inherited, not an integration regression.

First wear checkpoint: opened `renders/wear-pass1-{source,glb}/used_black_post-pair.jpg`.
Rejected the exaggerated white roof stripe and the yellow-green curtain across
the lower shell. The reference has sparse chips and rubbed folds, not wholesale
crown paint failure or a moss-covered wall. Removed the non-edge crown band,
narrowed lower fold chips and reduced their coverage. Confined seam dirt to a
small lower zone in darker neutral dirt. The kit's weathered pine replaces the
fresh wood, but appeared too pale in the pair: added an age-dependent cooler,
darker tone through OUT_base while preserving grain, checks, knots and causal
ground splash from `materials.weathered_wood()`. Correct grain and grade frames
are separate for the horizontal arm. No geometry or texture-set change.
First export/check passed (2,591,284 bytes); acceptance waits on the correction.

Opened the first full-frame hero and six-side/detail contact as well: the roof
stripe is unmistakably wrong from above, and the post foot is still too clean.
The pine replacement needs more caused dirt near grade, even after darkening
the wood palette. A further local adjustment amplifies the kit
`OUT_splash` mask only on the vertical post and mixes a dark damp-earth tone.
It retains the kit's irregular grade-driven shape; no uniform whole-post grime
or circular stain is introduced. Review the lower post in the final hero.

Second source pair: the crown stripe and moss curtain are gone, and the pine
now reads silver-gray. Noticed vertical dirt streaks on the red flag: the lower
shell-height mask had been evaluated in the flag's hinge-local coordinates.
Removed that deposit layer from the red signal finish and gave the Door paint
its actual rest-height offset, so lower-fold deposits remain attached to the
correct manufactured region. The third bake includes this coordinate correction
and the already identified stronger road-splashed post foot.

Third checkpoint: opened both refreshed source/exported used-photo pairs and
all eight hero/orthographic/detail/open-pose probes in `renders/wear-pass3-*`.
Accepted the sparse fold wear, clear crown, unstriped red flag, silver-gray
pine and irregular dark splash at the grade contact. The foot now reads at
full hero size; broad post faces retain gray wood instead of a uniform dirt
wash. Fine checks/fibers soften in the atlas, and the photographed post has
more knots; these are explicit close-view limits. `make export check` passed:
1,264 triangles / one material / 2,082,780 bytes, with three 1024 maps
BaseColor / Normal / ORM 645,381 / 638,621 / 703,649 bytes. Source/imported motion
and actual-surface support checks pass. Final docs follow this acceptance.

Final `make` passed (`../build/polish/mailbox-final.log`). Opened the complete
final contact and all three generated docs JPGs: the silvered post and dirty
foot read in the full hero, the crown stays clear and the flag has no misplaced
streaks. All nine Cycles views and the Eevee view record the final GLB hash.
The accepted JPGs are held for the single end-of-pass image commit.

## LOD rollout — 2026-11-09

Merged current main (already up to date). Frozen tool revision `c18eff8` and
103 literal hashes are in `build/lod-rollout/mailbox/freeze*`. Original
`make -C mailbox check -o build/lookdev.blend -o build/game-audit.blend
-o build/finalized.blend -o export/Mailbox.glb` passes before adoption;
`original-before.{json,log}` records the exact command and result. Those
accepted generated inputs are frozen to prevent source regeneration. The
small-prop starting chain requests .4 at .25 and .15 at .09; Door/Flag frames
and independent meshes must remain through both. No original export/map or
docs image is changed. A build or numeric result alone is not acceptance.

### LOD critique 1: reject a pointed near crown

Opened all six native strips, all three construction views and the contact.
Black coating, silvered pine, bottom splash and red flag values hold. But the
570-triangle near candidate has a visibly pointed front crown at .25 / 4.40m;
the rounded shell is a defining silhouette. Reject that level despite every
image gate and the independent UV/frame/raw audit passing. The 224-triangle
far level at .09 / 12.22m keeps recognizable post, shell and flag coverage;
its close view exposes a much coarser mouth and rear silhouette. Neither
meets the original 506/190 count targets. Full original config, outputs,
checks, hashes and every image are archived in `build/lod-rollout/mailbox/pass1/`.
Next try more near silhouette geometry and a lower far request at the same
switches; preserve the original goals and image gates. Door/Flag remain separate.

### LOD critique 2: rest appearance passes, door sweep fails

The next .6/.12 requests reach 766/202 triangles, still above 506/190.
Opened all six new native strips, all three construction views and contact.
The near crown now rounds more convincingly; coating, wood and flag values
hold. The far close view exposes angular shell/flag shapes, but native switch
coverage holds. Every generic image/raw/normal/UV check passes. A session ended
with observed exit 143 during the first build; no own process remained, and
the identical directly monitored retry completed with exit 0. Exact receipts
are `build/lod-rollout/mailbox/pass2{,-retry}.json`.

**Stop: no mailbox adoption.** The physical imported-LOD sweep fails:
LOD1 DoorMesh penetrates LOD_Static .000247644m at 74 degrees; LOD2 penetrates
.000893887m at 2 degrees. Both exceed the unchanged .00005m tolerance.
Flag clears both levels. Each sweep tests the actual one moving mesh against
two fixed meshes at 1-degree steps (106 door, 91 flag samples). The original
imported-GLB sweep passes with measured zero penetration. Mere serialized
pivot equality and separate meshes cannot approve these altered hinge surfaces.

`src/check_lod_motion.py` includes every imported mesh: generic static
consolidation does not carry the source asset_set tag onto LOD_Static, so
reusing the source's tag filter unchanged would silently omit the shell.
The checker asserts mesh ownership/count before calling the existing kit sweep.
The first manual invocation used the repository working directory and failed
to find its input; the corrected Make target runs in the family directory and
records the actual physical failure, not a missing-file result. Full
`make check-lod` now includes this physical audit and must fail. No geometry,
tolerance, original source or frozen tool is patched to conceal the failure.

Final proof: `final-check.json` records `make check-lod` exit 2 for motion;
`pass2-check.json` separately records the generic check/normal audit exit 0.
Original check before/after both exit 0 with the explicit frozen inputs above.
Final trial is archived in `build/lod-rollout/mailbox/pass2/`, including
physical motion JSON; original standalone PNGs are content-addressed copies
with identical bytes. The reporter ran with `--write-readmes --allow-failed`,
and its complete contact was opened; its generic PASS label does not audit
physical motion. All 103 frozen hashes match. Repository check reports 2553
files, zero errors. The session-wide immutable receipt still reports all
1200 original files unchanged. No accepted source/map/docs or kit code changed.

Mesh-count receipt follow-up: the physical wrapper now rejects any
boundary-excluded fixture and records counts computed from actual imported
ownership instead of a fixed count field. `final-count-check.json` still exits
2 with the same door depths. Each motion measures one moving and two fixed
meshes; no previously omitted surface or new geometry is involved. The rejected
status, maps and payloads remain unchanged.

## Archived rejected LOD reports — round 1

These reports are rejected evidence, not delivered chains.

## LOD rollout checkpoint: rejected motion

No mailbox chain is adopted. The measured trial below passes generic image,
geometry and normal checks, but `make check-lod LOD_THREADS=4` returns 2 on
the added imported-surface motion check. The reduced door penetrates the shell
by .248/.894 mm at LOD1/2, versus the original zero and .05 mm tolerance.
Separate Door/Flag meshes and unchanged pivots do not prove physical clearance.
See [both LOD critiques](REVIEW.md). `make lod` reproduces the rejected trial;
do not deploy it. Target misses remain 766/506 and 202/190, without claiming
an accepted target exception. Comparisons are `renders/lod/`; complete configs,
payload hashes, checks and images are archived in
`build/lod-rollout/mailbox/pass1/` and `pass2/`.

The reporter's generic PASS labels below cover its own image/raw/field gates;
they do not include or overrule the failed physical sweep. Its measured stored
cost is 2232 triangles, one canonical material, nine primitive placements,
4155897 physical bytes and 4.160 MiB resident. All three original 1024 maps
remain one 4.000 MiB allocation; added mesh buffers .07352 MiB, new images 0.
An instance would draw one level (1264/766/202 triangles and three draws),
not all nine stored placements. Both original `make check` runs pass.

<!-- LOD checkpoint: begin -->
## Additional LODs

`make lod` builds additional core glTF/BIN files and a manifest under `export/lod/`; `make check-lod` checks them. The existing delivery is immutable LOD0. Default `make` and `make check` retain their original build graph.

| Level | Triangles / target | Materials / draw calls | Geometry bytes | PNG bytes | Total load bytes | GPU unique textures + mesh, MiB | Switch height / distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LOD0 | 1,264 / — | 1 / 3 | 95,129 | 1,987,651 | 2,082,780 | 4.000 + 0.0864 | near |
| LOD1 | 766 / 506 | 1 / 3 | 63,756 | 1,987,651 | 2,051,407 | 4.000 + 0.0568 | 25.0% / 4.40 m |
| LOD2 | 202 / 190 | 1 / 3 | 21,710 | 1,987,651 | 2,009,361 | 4.000 + 0.0167 | 9.0% / 12.22 m |

Chain check: True; image check: True; normal check: True.


Whole-chain resident GPU estimate: **4.160 MiB**, versus LOD0 alone **4.087 MiB**. Unique textures 4.000 MiB = 4.000 MiB original + 0.000 MiB proxy/impostor; all meshes 0.1599 MiB. Increase over LOD0 0.074 MiB = 0.000 MiB far maps + 0.0735 MiB additional mesh buffers. Intermediate new images: 0. Bind intermediate primitives to the canonical LOD0 material resources; the manifest records full image hashes and source image indices. Identical embedded/external PNG bytes require this resource binding to share GPU allocations, including duplicate original image entries. GPU columns deduplicate complete image hashes within each row; PNG/dependency bytes retain physical payload copies. Optional camera-facing impostor is a separate alternative; engine overhead is excluded.

Distances are to the bound center at 60° vertical FOV / 1080p. GPU figures estimate 8-bpp block-compressed textures with full mips plus raw accessor mesh bytes, before engine overhead. Per-level map bytes describe dependencies, including reused originals. The whole-chain estimate deduplicates canonical image resources. Targets and achieved counts are reported separately; a count alone does not establish visual acceptance.

Load these files as alternatives and configure Godot visibility ranges, Unity LODGroup renderers, or Unreal mesh/component LODs. Keep matching near pivots in the same pose during switching. [Engine sources, pixel thresholds and texture policy](../kit/LOD.md).

Near levels consolidate static parts by material and simplify moving parts while retaining names, pivots, sockets and animation data. Intermediate levels preserve original charts, attributes and LOD0 materials. Only the proxy receives new charts baked from the immutable delivered maps and shaders. Intermediate levels allocate no additional images.

Native-pixel LOD0/adjacent strips, amplified differences, close views and measured image status: `renders/lod/` (`contact.jpg`, `metrics.json`). Raw checks: `export/lod/check.json` and `export/lod/normals-vs-lod0.json`; per-level construction/pruning decisions: `build/lod/<source stem>/simplification.json` and manifest assembly receipts. [Critique, target misses and known failures](../kit/LOD_REVIEW.md).

Shipped PNG dimensions: LOD0: 3 × 1024×1024; LOD1: 3 × 1024×1024; LOD2: 3 × 1024×1024.

LOD1 separate moving meshes: `DoorMesh`, `FlagMesh`.

LOD2 separate moving meshes: `DoorMesh`, `FlagMesh`.

Whole default chain:

| Stored mesh triangles | Material resources | Stored primitive placements | Distinct payload bytes | Resident GPU, MiB |
| ---: | ---: | ---: | ---: | ---: |
| 2,232 | 1 | 9 | 4,155,897 | 4.1600 |

Stored counts include the full immutable source container once and every default level; optional impostor alternatives are excluded. Near materials use their canonical source bindings. Physical payload files are counted once by path. Only one level is drawn per instance: active draw calls range from 3 to 3 across these kinds/levels. Stored primitive placements are not simultaneous runtime draw calls.

<!-- LOD checkpoint: end -->
# LOD round 2 — closed-door levels with an original interaction hold

The accepted 1264-triangle, 2082780-byte original is present and matches the
README exactly. Its family make check passes with existing accepted scenes and
the GLB explicitly frozen. A separate clean source/bake/export/check rebuild
runs under build/lod-round2/mailbox/rebuild/ without overwriting the accepted
delivery or docs. Tool revision 773822c and 103 literal hashes are frozen before
the new proof; source-frozen.json hashes the immutable original.

The new proof distinguishes permitted poses: LOD0 supplies the full 0–105-degree
door sweep; reduced doors may draw only at rest. All levels still require the
flag's complete 0–90-degree sweep with no contact exceptions. The interaction
controller must select LOD0 before changing the door angle and keep it until
the door returns to rest. This addresses round 1's reduced open-door failures
without pretending every reduced door must animate safely. The updated
src/check_lod_motion.py measures those actual imported surfaces and verifies
that translating Mailbox moves every mesh by the same amount. include_nodes
keeps the merged static shell under that placement root.

Start with a .3 near / .08 far target witness at the established .25/.09
switches. Keep the previous .6/.12 payloads, config and native comparisons in
build/lod-round2/mailbox/prior/. No public LOD hook is added until the chain
passes its own images, normals, permitted poses, original check and receipts.

### Round 2 critique 1 — cheaper count witness fails at rest

The clean scratch original rebuild exits 0 and measures 1264 triangles,
2082784 GLB bytes (+4). All expanded POSITION/NORMAL/UV/TANGENT arrays match
the accepted original exactly; maps differ by at most one byte, RMSE at most
.001128, within the kit's GPU rebake limits. The accepted GLB is unchanged.
original-rebuild-{confirmation,difference}.json records the separate facts.

The .3/.08 trial reaches 494/196 triangles, goals 506/190, without new maps.
Opened all six native strips and all construction views. Color/value first:
black coating, red flag, silvered pine and the dirty foot hold. The near front
crown is visibly pointed, repeating the rejected round-1 tell; the distant
flag is angular in construction view. All image/raw/normal checks pass, but
that cannot approve the crown. More decisively, actual closed-door penetration
is 1.592/.234 mm, exceeding .05 mm. The original full door and every flag sweep
pass at zero; placement errors are .000119 mm. The interaction hold therefore
cannot approve these *rest* geometries. Archive all payloads, hashes, native
views and motion results under build/lod-round2/mailbox/target-pass1/. Retry
the conservative .6/.12 chain with the same switches, goals and hold policy.

### Round 2 critique 2 — conservative rest clearance still fails

Opened all refreshed switch strips and construction views. Color/value holds;
the near crown rounds properly, and far coverage remains recognizable. Native
image checks pass. However the 766/202 trial still measures .174/.234 mm of
closed-door penetration, above .05 mm. Every flag sweep and the original door
again pass at zero. Archive this separate failure under pass2/; neither this
result nor round 1's open-door failure approves a reduced closed door.

Use the kit's existing source_geometry_nodes option to retain the original
Door and Flag geometry, as well as their pivots and material routing. Try one
.09 level: retaining these already small moving surfaces makes a weak near
reduction poor value. Keep the original far goal of 190, so any necessary
exception remains measurable. No source geometry or kit code is modified.
