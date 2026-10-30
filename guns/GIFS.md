# Finished-gun signature GIFs

One loop under each finished gun's README hero, rendered from its exported GLB
with the embedded baked maps. The side-by-side is not included.
Run `make -C guns/<gun> gif`; the shared implementation and configuration
interface are documented in [common/README.md](common/README.md#one-signature-motion-gif).

Every loop uses the member's accepted final studio, Eevee at 64 samples, AgX
Medium High Contrast, fixed sample settings, a flat RGB surround and no text. One discarded warmup
frame initializes Eevee before frame zero; it is not part of the animation. All
clips run at their authored speed. Each loop adds exactly 500 ms to its first
frame; the durations below include that hold. Frames are sampled by time on
half-open clip intervals, so the endpoint is not counted twice.

| GIF | Clip | Pixels | Frames | Hz | Distinct palette entries | Bytes | Loop ms |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [pistol](./pistol/docs/motion.gif) | `ReloadEmpty` | 960×640 | 48 | 20 | 244 | 265,362 | 2,900 |
| [lever](./lever/docs/motion.gif) | `Fire` → `Cycle` | 960×505 | 26 | 20 | 254 | 141,408 | 1,800 |
| [shotgun](./shotgun/docs/motion.gif) | `Fire` | 960×447 | 22 | 20 | 254 | 257,807 | 1,600 |
| [revolver](./revolver/docs/motion.gif) | `Reload` | 576×371 | 67 | 20 | 187 | 433,393 | 3,850 |
| [bolt](./bolt/docs/motion.gif) | `Fire` | 720×351 | 55 | 25 | 254 | 434,764 | 2,700 |
| [ak](./ak/docs/motion.gif) | `ReloadEmpty` | 820×443 | 70 | 20 | 252 | 427,451 | 4,000 |
| [smg](./smg/docs/motion.gif) | `ReloadEmpty` | 960×519 | 70 | 20 | 249 | 300,968 | 4,000 |
| [lmg](./lmg/docs/motion.gif) | `Reload` | 480×384 | 120 | 20 | 189 | 392,971 | 6,500 |

All palettes allocate at most 256 entries, including transparency for unchanged
pixels. ffmpeg uses one palette for the entire clip, no dithering, difference
rectangles and transparent unchanged pixels. Each gun retains its 2048 PBR atlas;
these presentation files add no game geometry, textures or draw calls.

Source frames below use each manifest's 60 Hz clock. GIF indices are zero based;
every sample advances by 50 ms (40 ms for bolt), with the extra 500 ms on index
000 only. None of the clips is slowed down.

| Gun | GIF indices | Sampled source frames |
| --- | --- | --- |
| pistol | 000–047 | ReloadEmpty 0, 3, …, 141 |
| lever | 000–025 | Fire 0, 3, …, 15 → Cycle 0, 3, …, 57 |
| shotgun | 000–021 | Fire 0, 3, …, 63 |
| revolver | 000–066 | Reload 12, 15, …, 210; static margins trimmed |
| bolt | 000–054 | Fire 0, 2.4, …, 129.6 |
| ak | 000–069 | ReloadEmpty 0, 3, …, 207 |
| smg | 000–069 | ReloadEmpty 0, 3, …, 207 |
| lmg | 000–119 | Reload 0, 3, …, 357 |

All renders start at 960 pixels wide. The revolver's complete 960-pixel reload
exceeded 1 MB: after a tighter composition and removal of static margins, it
still needed 576 pixels and a 192-entry allocation. Bolt and AK needed 720 and
820 pixels respectively after larger deliveries exceeded 450,000 bytes. These
retain their full moving spans and full palette allocations. No gun required
reducing its selected frame rate. Fine revolver surface detail is softer at its
smaller delivery size; the extractor, cases and loader remain readable.
The Harrow's full six-second reload ships at 480 pixels with a 192-entry
allocation. A 960-pixel landscape was 1,263,756 bytes, 640 pixels was 708,992,
and a tighter portrait crop increased the animated area to 1,290,055 bytes at
576 pixels. The final landscape keeps every sample and all cover/box travel;
its 189 distinct entries retain dark paint, gray polymer and colored rounds.

Camera coordinates below are meters in the existing gun frame (+Y forward,
+Z up, +X right). All use a 36 mm horizontal sensor and the member's unchanged
final studio/lights. The preceding hero supplies a full silhouette; the manual
action crops spend pixels on the feed/ejection area.

| Gun | Camera location | Target | Lens mm | Aspect | Roll rad | Exposure |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| pistol | (0.37, 0.21, 0.15) | (0, 0.025, -0.008) | 48 | 1.5 | 0 | -0.15 |
| lever | (0.48, -0.05, 0.83) | (0, 0.16, 0.035) | 43 | 1.9 | 0.4 | -0.15 |
| shotgun | (0.87, 0.35, 0.32) | (0, 0.26, 0.005) | 48 | 2.15 | 0 | -0.15 |
| revolver | (-0.42, -0.35, 0.26) | (0, 0.055, 0.02) | 54 | 1.55 | 0 | -0.3 |
| bolt | (0.68, 0.015, 0.29) | (0, 0.135, 0.045) | 48 | 2.05 | 0 | -0.15 |
| ak | (1.12, 0.53, 0.38) | (0, 0.16, -0.04) | 49 | 1.85 | 0 | -0.15 |
| smg | (-0.92, 0.48, 0.35) | (0, 0.08, -0.02) | 50 | 1.85 | 0 | -0.15 |
| lmg | (−1.25, −0.12, 0.68) | (−0.015, 0.16, 0.04) | 43 | 1.25 | 0 | -0.15 |

The pistol's `ReloadEmpty` shows magazine exchange and slide release; its short
Fire would hide most of the mechanism. The revolver's `Reload` shows the crane,
extractor, retained/falling cases, loader and closing cylinder. AK and SMG empty
reloads show their different magazine and charging-handle paths. The pump and
bolt `Fire` include the complete manual cycle, with their corrected visible
feed and ejection. The lever keeps its original separate `Fire` → `Cycle`
sequence: combining the presentation does not alter either exported clip.
The Harrow's complete `Reload` shows cover opening, belt withdrawal, box
exchange, belt placement on the tray and closing. Its .20-second Fire is too
brief to show those relationships as clearly. The hero supplies its complete
silhouette; the GIF frames the cover, belt and box throughout their travel.

Each `src/gif.json` is the camera/sequence source of truth. Each gun's
`build/gif/report.json` records the source GLB hash, every sampled source frame,
decoded GIF delays, actual palette entries, file size and GIF hash.
`build/gif/contact-sheet.jpg`, `review/frames-*.jpg` and the full PNGs provide
frame inspection; `build/gif/playback.html` loads the continuous 1× GIF locally.
Only `docs/motion.gif` is committed. Per-gun [review notes](pistol/REVIEW.md)
record color/value comparison with the existing docs, motion legibility and
palette review; each gun has its own corresponding `REVIEW.md`.

Validation on `wp/docs-gifs`: all seven `make gif` targets passed twice, including
complete Blender renders, with identical delivered GIF bytes. Exact-byte reuse
is an explicit [numeric comparison with the committed GIF](common/README.md#exact-bytes-across-gpu-repeats):
every run creates a fresh candidate, verifies the unchanged recipe/geometry and
compares every decoded pixel before retaining the existing bytes for negligible
GPU rounding. Removing the reference GIF can produce visually equivalent bytes
that differ; raw GPU arithmetic is not claimed to be bit-exact.

Each gun's `make check` was run. Pistol, lever, pump, revolver, bolt and SMG passed;
the interrupted lever run resumed after its already completed verify/atlas
prerequisites. AK fails its existing exact-main-GLB checksum after a fresh bake
(32 bytes smaller than the recorded baseline). Its geometry/UV/rig preservation,
source/finalized/re-imported construction and motion, atlas and retainer-fit
checks pass separately; no baseline or check was relaxed. The full 24-file kit
fixture suite passed sequentially from an empty scratch build, as did the four
shared GIF tests, four repository-policy tests and repository/staged checks.
Detailed local evidence is in `build/docs-gifs/`, including
`verified-thread-gifs.json`, `kit-suite/results.json` and the per-gun check logs.

AK follow-up on `wp/guns-ak-check` (2026-10-30): the failure above is resolved.
Two clean default builds and their separate checks now pass. Only sparse GPU
bake rounding differed; exact non-image GLB data and JSON semantics remain
protected, with decoded texture differences bounded against the historical
accepted bake. The [AK investigation](ak/REVIEW.md#fresh-build-check--2026-10-30)
records the byte/texel measurements, tolerance and full command results.
The accepted docs JPGs and GIF remain unchanged.

Harrow completion on `wp/guns-lmg` (2026-10-30): two full `make gif` runs
deliver identical GIF bytes. All 120 decoded candidate frames match exactly;
the shared tool's explicit canonical-byte comparison retains the first
delivery. Every decoded frame was opened on its native review page. Corner
RGB is constant at 111/114/118, and quantization averages .929 RGB levels on
the object. The compact loop retains the complete six-second reload. The
[LMG review](lmg/REVIEW.md#finals--delivered-gif-frame-and-palette-review)
records compression trials, palette/color inspection and the continuous
visual-playback limitation.

All decoded frames were inspected, with native pages for feed, ejection,
extraction and charging. Background corners remain exactly constant; global
palettes show no objectionable steel bands or dither noise in the reviewed
sequences. Continuous visual playback was unavailable in this headless session;
the authored-speed delays were audited and each local `playback.html` opens
the actual looping GIF for that remaining visual check.
