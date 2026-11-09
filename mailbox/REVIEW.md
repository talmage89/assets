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
