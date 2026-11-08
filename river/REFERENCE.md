# River / bridge form basis

Original visual constructions for a 1995–2015 town. Published references guide
the construction vocabulary; the crossings are authored places, not surveyed
replicas or engineered hydraulic/structural designs. Photos are viewed only.

| Feature | Source / authored interpretation |
| --- | --- |
| Normal-flow channel | Brief's 60–150ft range; nominal 100ft / 30.480m downtown, 120ft / 36.576m edge. Width varies along each reach. USGS SIR 2005-5153 distinguishes normal water from bankfull width, measured at riffles. Do not equate the two. |
| Bed / floodplain | About 1.05m run depth; 0.37m riffle center; outside pool about 2.1m, with 2.04m exported vertex-depth maximum. USGS Circular 1246, riffle formation pp36–37, for outside-bend scour and inside-bar deposition. Values are original within the brief, not a measured USGS station. |
| Banks | Natural floodplain about 2.15m above local water; outer bank rises over about 3m, inner about 8m, with local variation and road fill. These are authored stable/eroding profiles. MDT Chapter 17 describes 2H:1V riprapped abutment slopes; the unarmored bank is not assumed to follow that slope. |
| Scour / riprap | FHWA HEC-18 (2012), Chapters 3/7/8: contraction, local scour, debris loading. HEC-23 volume 2 (2009), DG11/14: toe and pier aprons, filter and buried edges. Stones span roughly 0.3–0.8m at the bridge; exposed toe/apron, buried filter not exported. No design-flow or stone-sizing calculation is claimed. |
| Main structure | FDOT 2010 index 20130, drawing revised 2005: standard AASHTO Type III, 45in / 1.143m deep, 16in / .4064m top flange, 22in / .5588m bottom flange, 7in / .1778m web. Bottom-to-top vertical zones 7 / 7.5 / 19 / 4.5 / 7in; ¾in bottom-foot chamfers. Traditional AASHTO section retained in the period; the current publication does not date our fictional bridge. |
| Spans | Downtown 3 × 60ft / 18.288m; edge 2 × 80ft / 24.384m. Five girders per span, elastomer pads on concrete plinths/steel seating plates, chamfered caps, three 1.2m columns or a 1.3m wall with rounded upstream/downstream noses. Authored arrangement within the standard girder class. |
| Deck | Downtown 39ft / 11.8872m; edge 35ft / 10.668m. Two 11ft / 3.3528m lanes, 2% crown, 193–260mm concrete deck, 60mm asphalt, 152.4mm raised walks at the road edge. Five girders give 2.497 / 2.192m spacing and .95m deck overhang to exterior girder centerlines. Widths are art choices; Ground's measured materials and paint charts are reused. |
| Bearing stack | Bottom to top: .20m plinth, .02m steel seating plate, .064m elastomer with two visible laminations, .016m sole plate. Plinth .56 × .70m; seat plate .4964 × .6103m; pad .4327 × .5205m. Added keeper angles, four anchors and nuts retain the accepted .30m stack height. Adapted from the landed freeway's native layers; fresh-import rays measure actual girder/sole and plinth/support contact. No load rating is implied. |
| Other bridge construction | Expansion gaps, joint seals/steel retainers, diaphragms, approach slabs, backwalls, flared wingwalls, curb-mounted 32in parapets, W-beam approach rail/terminals, scuppers and supported utility conduits. FDOT indexes 20500, 20900, 21100 and 21210 establish the construction vocabulary. |
| Period assembly drawing | Tennessee DOT STD-4-4: designed 1989, issued 1992, revised 1996. Interior/exterior I-beam deck interfaces, overhang and end diaphragm construction. Our permanent concrete silhouette retains the haunch and diaphragms; hidden reinforcing and temporary erection supports are omitted. |
| Inventory / era | FHWA 1995 Recording and Coding Guide, Items 42/43: highway/pedestrian over waterway; prestressed concrete, stringer/multi-beam/girder. Fictional 1974 downtown and 1968 county bridges, maintained in 2010. |

The two plans change bend, normal width, bar/riffle stations, span arrangement,
pier type, street width and the town's land use. They do not share a plan with
different decoration. Floodplain maples come from `trees/`; no new tree species
are introduced. Willow is omitted under the owner's no-new-species rule.

Current photo neutral patches: FHWA's exposed concrete cap,
Raisin's gray bridge parapet and the 2008 Huron bank photograph's
weathered gray dock decking. Earlier rejected studies used Morrison's pale
concrete trail wall and Stockport's gray asphalt. These are assumed neutrals,
not color cards. Photo comparison reports retain fit residuals and
construction/class differences.

Shared construction now calls `freeway/src/pieces.py` from merged main, through
`src/freeway_bridge.py`; no source was copied from its unmerged branch. Native
factories supply the girder topology, column bent, F-parapet, W-beam terminal
and bearing layer geometry. The Type III section remains the independently
cited FDOT profile above; the native Type IV is not silently substituted.
Concrete and Zinc are the freeway's unchanged shared image sets. See its
`REFERENCE.md` and texture documentation for their own construction basis.
