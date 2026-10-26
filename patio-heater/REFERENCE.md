# Evening 89: measurement and construction basis

Original Cinder Works design, researched 26 October 2026. Photos and manuals
are comparison inputs only. Nothing from them enters mesh or texture generation.

| Feature | Published reference | Original asset |
| --- | --- | --- |
| Overall height | Fire Sense 61436: 89 in | 2.2606 m nominal, fastener top within 1 mm |
| Reflector diameter | 33 in, five-piece hood | .8382 m, three petals plus crown |
| Ground base diameter | 18 in | .4572 m |
| Post OD | 3 in one-piece post | .0762 m, 1.2 mm wall |
| Fuel | 20 or 30 lb LP cylinder | owner's 20 lb only; cylinder excluded |
| Cabinet | photos: rolled sheet and vented shoulder | .4064 m OD, .71 m wall height, 1.5 mm sheet, hinged door |
| Head proportions | photo calibrated by 89 in envelope | emitter .264 m OD × .224 m clear height |
| Reflector fabrication | manuals: petals, crown, three studs | .9 mm aluminum, lap seams, hemmed rim |

Primary source: [Balkene Home / Fire Sense 61436](https://balkenehome.com/products/61436).
Manufacturer [2023 Pro/Lux assembly manual](https://cdn.shopify.com/s/files/1/0979/8032/files/61436_63253_63670_64927_FS_Manual_2023_a91f3e20-68e5-4b1f-804a-3be24a5ec90f.pdf),
pp. 4–7: post, hose, regulator, reflector studs and assembly.
[AZ Patio Heaters door model manual](https://azpatioheaters.com/HLDS01-WHDK.pdf),
pp. 2, 7–10: hinged cabinet, regulator and three-petal reflector.
Its wicker finish and table are not used. The 61436 itself uses a lift cover.

Only the published overall dimensions are exact source dimensions. Housing
height, emitter height, gauges, fastener placement and internal spider are
original engineering choices informed by visible construction. Camera fit
residuals report the differences instead of claiming silhouette identity.

The optional owner cylinder fit checker measures the read-only GLB: 312.2 mm
diameter, 468.0 mm tall, foot-ring bottom origin, +Z up, valve −Y at local
(0, −41.9, 423.5) mm. Modeling never loads it. The socket places its foot ring
on the actual .064 m floor. Housing, door, supports and hose are checked against
imported triangle surfaces. See refs/SOURCES.md for credits and licenses.


Wear review uses [Terrassenstrahler.jpg](https://commons.wikimedia.org/wiki/File:Terrassenstrahler.jpg),
3268zauber, 12 February 2009, CC BY-SA 3.0. It shows heaters in outdoor
restaurant service, including stained metal, oxidized shoulders and scuffed
bases. Their age is unknown. The foreground stainless lift-cover heater supplies
the review camera and outdoor-use comparison, not our paint color or geometry.
Our powder-coat chalking, drag damage, trapped-moisture corrosion and rain
residue are procedural material responses to those causes. The comparison
crop and credit are reproducible from src/photo_matches.py and refs/SOURCES.md.
