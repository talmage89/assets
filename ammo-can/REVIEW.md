# Ammo can review

## References and working construction

Read the military specification's cover, gasket and hasp/latch functioning requirements and the manufacturer dimensions. Opened the manufacturer's three product photographs, opened-cover photograph, two dimension drawings and the downloaded dimensional sheet. The envelope is exactly 305.6 × 154.8 × 190.5 mm to float precision. Main walls/cover use the published 0.8/1.2 mm gauges. Hardware estimates remain explicitly authored, not claimed dimensions from the separately controlled government drawing.

Initial assembly sweeps found a sleeve touching the cover skirt and carrying wire touching its feet. Reduced sleeve wall to the appropriate rolled-sheet section, moved its axis clear of the skirt, and thinned the handle feet while retaining their support. Initial lid sweeps then found filled rectangular hinge mounts crossing the gasket, pin and rear skirt. Replaced them with actual bent-sheet leaves and relieved the rear cover skirt. The lid has open C hooks so it can withdraw from the secured body pin, rather than impossible closed sleeves. Tested both high/game sources: cam release 54 samples, closed-lid handle 46; then lid opening 111 samples at 1°, withdrawal 101 samples at 0.25 mm, and open-lid handle 46. All have zero measured solid penetration. Only explicitly named working sleeve/shaft bearings have intended-contact declarations; pin crossings are included in the cover-removal sweep.

The integrated `kit/assembly.py` independently measures actual surfaces at 22 support/contact pairs in high/game: contact is measured at gasket, retainer, hasp, hinge leaves, mounting feet and pull bail; the pin/wire radial clearances measure approximately 0.300 mm. These are physical source checks. Later GLB equality checks prove serialization separately.

## Photo critique, first source pass

Individually opened seven Cycles views in `renders/pass1/`: hero, cam released, cam close-up, rear hinge, raised handle, closed photo match and front latch photo match. Opened both photographic pairs. The dimensions and folded side reinforcement read as the M2A1 class, and fictional stencils are legible. Weaknesses: the lid folds were too sharp, two horizontal pressed ribs were missing on the cam neck, and handling wear spread too broadly over the cam face. The nominal open-lid studio view only released the cam: the legacy `lid` setting reset the generic part rotation. Corrected the view to use that explicit lid setting, rather than claiming an open cover from metadata alone.

Added a restrained 0.35 mm cover-fold bevel, the two supported stamped cam ribs, and restricted handling wear to grip and pull regions. Increased the procedural backdrop width to keep the low matched camera inside the seamless. All motion/contact checks pass again after these changes. Game mesh 2,784 triangles. Finalized atlas: 53.17% coverage, zero measured overlap/outside/degenerate triangles, p5/median/p95 887/976/980 px/m at 1024.

Photo calibration estimates: closed view 60.0 mm lens / 5.22 px RMS at 640×480; front closure 123.7 mm / 2.59 px RMS in the 310×360 crop. Independent Blender projection agrees within 0.00032 px. These fits support proportions and construction, not an exact product replica or a known EXIF lens. Final GLB comparison remains required.

## Revised source and delivery probe

Opened all five revised source images and both refreshed photo pairs in `renders/pass2/`. The folded cover and cam ribs now catch light as sheet steel, and rubbing is limited to handling/edge regions. Opened both 1024/8-sample baked GLB Cycles probes: geometry, paint, gasket and fictional lot transfer cleanly; there is no thin-wall projection band. The stencil softens at 1024 as expected. This early exported probe checks the actual delivery material before the full bake, not just source shading.

The corrected open-lid pose exposed a framing problem: the top of the lid extended beyond the original camera. Reframed it around the complete open assembly. Kept the broad cam face flat shaded after the inspection-hole Boolean to remove a triangular highlight. Opened the revised source open-lid and cam close-up in `renders/framing-final/`. The lid fit, but the released latch still exceeded the frame. Measured all posed mesh vertices: the complete assembly reaches 610.282 mm high. Refit the camera from those vertices to retain at least 8% frame margin, with a 45 mm lens aimed at 305 mm height. The final exported render must confirm that framing. The matched reference is newer/darker under different illumination; our finish is an original, mildly used olive drab, with fictional stencils absent from that specific manufacturer photo.

## Final delivery checks: PASS

`make -C ammo-can` and `make -C ammo-can check` both exited 0 in `build/ammo-final-resumed.log`. High/game geometry and scale audits, independent UV/normal checks, fresh GLB re-import, photographic camera projection, repository checks, both motion sweeps, both 22-pair surface-contact reports and the two release/open/remove sequence reports pass. All sampled solid sweeps measure zero penetration. Rebuilt the game source independently into `build/ammo-repeat.blend` and audited it: geometry SHA-256 matches exactly, `ab50c299e6363e0cac4bb210b15b669d0a481f20351b94c488c0e8003c1a5c54`.

Delivery: 2,784 triangles, one material, four mesh objects, 1,869,928-byte GLB. SHA-256 `5a1263c761643ab7e0b9453250a5c82c90d2a075aef0ea3c8cf4c4a0ddecebf8`. All maps are 1024²: BaseColor 423,548 bytes, Normal 376,937, ORM 847,777. Approximately 4 MB block-compressed texture residency including mipmaps. Re-imported rest-vertex and pivot-matrix errors measure 0; maximum vertex-normal unit error is 1.1921e-7. Delivered UV coverage 53.17%, overlap/outside/degenerate counts 0, density p5/median/p95 887/976/980 px/m.

Full 4096/32-sample OptiX bake: all five channels have zero missed interior samples over 8,617,697 checked texels; BaseColor also has zero black interior texels. Isolation uses four coordinate frames and 24 stationary AO occluders. No texture repair or external image enters the material. Detailed evidence is in `textures/bake/bake-report.json` and `build/`.

Individually opened the ten final Cycles views, Eevee hero, both exported photo renders/pairs, all three docs and the complete contact sheet. The open cover, released cam and bail now fit completely within the image; all close-ups show the retained bearing and folded construction. The broad cam face no longer has the first pass's triangular highlight. The 1024 stencil remains readable at normal viewing distance but softens in close-up. Paint is lighter under this studio than the manufacturer's differently lit new can. The low photo camera revealed a dark background patch. Hiding the negative-fill cards and widening the seamless did not fix it. Actual camera ray casts showed the patch hits the seamless 17–26 m away, where the main studio lights no longer illuminate it. Added a broad wash facing the far backdrop, with the asset behind the light. This is a comparison-only procedural studio change. No kit or delivered surface changes are involved.

All 13 final metadata entries identify the current GLB hash. Final contact: `renders/final/contact.jpg`; photo pairs: `renders/photo-final-glb/match_closed-pair.jpg` and `match_latch-pair.jpg`. Docs: hero 1600×750 / 71,097 bytes; turnaround 1600×1700 / 104,403; details 1600×2795 / 182,286. Three JPGs only. The weakest areas are softened small pressed edges/stencils, simpler formed corners and cam edges, and authored hardware estimates beyond the published dimensions/gauges. There is no unresolved assembly or budget failure, and no lead input is needed.

Opened both refreshed matched PNGs and photographic pairs after the backdrop wash: the black patch is gone. A faint lighting transition remains on the comparison backdrop; it does not affect the object or the clean portfolio studio images. The original assembly, calibrated viewpoints and delivered atlas are unchanged. Final render provenance still matches all 13 records. The updated default build and check also run after this presentation-only Makefile change; see `build/ammo-complete.log`.

## Phase 2 combined-kit regression

On `wp/polish`, `make clean`, `make`, and a separate `make check` exited 0
against the combined kit. The new exported hero and all turnaround, pivot,
close-up, scale and Eevee views were opened alongside the committed hero;
there is no visible integration regression. Both original construction photo
pairs were also opened. Delivery remained 2,784 triangles / 1 material /
1,869,928 bytes, exactly the README baseline. Logs and the preserved baseline
hero/contact/GLB are under `../build/polish/`.

The baseline still looks almost unused: broad enamel and especially the cover
have almost no visible abrasion at hero distance. New references are an actual
used M2A1 photographed for a surplus sale and Douglas Muth's used ammunition
box. Their lid lips, corners and carrying attachments lose paint, while broad
panels carry longer, sparse rack scuffs. The fictional lot stencil should be
less opaque where those same scuffs cross it. Geometry and pivot surfaces were
independently compared before/after the material edit and match exactly.

First wear checkpoint: opened `renders/wear-pass1-hero/hero_closed.png` and
both `renders/wear-pass1-{source,glb}/used_surplus-pair.jpg`. Rejected this pass:
the lid had chalky noise across half its face, the lower body looked evenly
corroded, and too many parallel hairlines covered the broad panel. The source
pair proved these were authored-shader problems rather than projection loss.
The lid's coordinates are hinge-local, so its Y center is −149.8 mm; the first
analytic fold mask incorrectly treated Y=0 as its center. Corrected that rest
frame, narrowed the bottom chip band from 23 to 10 mm, kept paint on the broad
cam face, and replaced the broad scratch field with three located rack-contact
tracks and three cover scrapes. The used reference has concentrated edge loss
and sparse long scrapes, not a white mottled coating. The new camera fit is
4.84 px RMS at 900×600; the independent projection check passes.

Second wear checkpoint: opened the new hero and both source/shipped pairs in
`renders/wear-pass2-*`. Accepted the concentrated edge loss and a few legible
rack scrapes: the lid no longer carries the rejected half-face mottling, the
bottom band is narrower, and the cam face retains its coating. The fictional
stencil is faded and locally interrupted. Against the used M2A1 photograph,
wear now follows the same folds and contact zones. The original olive palette
is lighter than the photographed dark surplus finish under different lighting;
this is a wear calibration rather than a paint-color replica. Small chip shapes
soften after the 1024 filter; edge loss and larger scrapes remain visible in the
full hero, without allocating geometry or another map.

`make export check` passed after the correction (log
`../build/polish/ammo-can-wear-pass2-build.log`). Export: 2,784
triangles, 1 material, 2,467,520 bytes; BaseColor / Normal / ORM
729,791 / 418,654 / 1,097,409 bytes at 1024².
The same source contacts, motion sequences, independent UV/normal checks and
fresh GLB re-import passed. Final docs are generated only after this acceptance.

The complete final turnaround revealed a defect hidden by the accepted hero:
the earlier body handling ellipse had become a circular mottled patch on the
rear wall when amplified for wear. Rejected that patch on the full-view review.
A rear mid-panel circle is not a defensible handling zone on a can carried by
its top handle. Removed body handling entirely; broad body abrasion now comes
only from the authored rack tracks, manufactured edges and ground-contact band.
The cam/handle retain their own local contact masks. The first docs generation
was held uncommitted; it cannot be accepted with that rear artifact.

Third wear checkpoint: opened the complete front/rear/top/controls/hero probe
in `renders/wear-pass3-hero/contact.jpg`, and both refreshed used-photo pairs.
The circular rear patch is gone. The rear panel retains its coating with only
fold and bottom wear; lid, cam contact and sparse side scuffs still read at hero
distance. `make export check` exited 0 after this final material correction;
log: `../build/polish/ammo-can-wear-pass3-build.log`. Delivery is 2,398,092
bytes / 2,784 triangles / 1 material; maps BaseColor / Normal / ORM are
693,539 / 418,129 / 1,064,760 bytes at 1024². The revised
source/GLB pair paths are `renders/wear-pass3-source/used_surplus-pair.jpg`
and `renders/wear-pass3-glb/used_surplus-pair.jpg`.

Final corrected `make` passed (log `../build/polish/ammo-can-final-corrected.log`).
Opened the completed final contact, turnaround and details after the rear-mask
correction. All ten Cycles views, the Eevee view and all three exported photo
comparisons name the final GLB SHA-256 in their shot metadata. Independent raw
accessor comparison to the preserved regression GLB measured zero differences
in vertices, indices, normals, UVs, tangents and node/pivot transforms. The three
accepted docs JPGs are held for the single end-of-pass image commit.
