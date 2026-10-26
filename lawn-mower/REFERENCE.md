# Meadow 21 measurement and construction reference

Original Cinder Works gas push mower. The 21 in class, not a replica of a branded model.
All surfaces, materials and graphics are scripted. Reference pixels are never used in textures.

## Primary sources (accessed 26 October 2026)

- [Troy-Bilt TB120B manufacturer specification](https://www.troybilt.com/en_US/push-mowers/tb120b-push-lawn-mower/11A-A2T2066.html): 21 in (533.4 mm) cutting width, 7 in (177.8 mm) front wheels, 8 in (203.2 mm) rear wheels, 140 cc vertical engine, steel deck, 1.9 US bushel bag (66.96 L nominal), recoil start, 1.25–3.75 in cutting range. The contradictory generic feature text describing nine positions is ignored; the actual specification lists six. Our independent four-lever axle carriers are an original construction choice.
- [MTD operator manual 769-27025](https://apps.mtdproducts.com/manuals/769-27025.pdf): bag channels around a steel frame, hook attachment under the rear door, two-piece handle, cable clips, rope guide, bail and folding sequence. Pages 7–12 (printed numbering) inform the assembly, not exact dimensions.
- [MTD illustrated parts 769-10291](https://apps.mtdproducts.com/manuals/769-10291.pdf): printed pp. 4–11 show deck, blade adapter, shield, individual wheel hardware, lower/upper handle and bag frame as separately manufactured parts. This is an older family drawing, used only for construction.
- [Toro 3440-905 operator manual](https://www.toro.com/getpub/210212): independent confirmation of rear bag hook/frame, vertical-shaft blade stack and released blade-control geometry. No Toro styling or marks reproduced.

## Looking references

- Manufacturer TB120B photographs (`product0.jpg`, `product1.jpg`): wheel-to-deck proportions, engine layering, bag slope and handle joints. Copyright Troy-Bilt, comparison only.
- [Mower in actual use, Famartin, 27 May 2015](https://commons.wikimedia.org/wiki/File:2015-05-27_12_41_21_A_lawn_mower_on_Tranquility_Court_in_the_Franklin_Farm_section_of_Oak_Hill,_Fairfax_County,_Virginia.jpg), CC BY-SA 4.0: full assembly, fabric folds, cable routing, wheel dirt and restrained use wear. Different manufacturer and engine; not a dimensional drawing.
- [2006 Lawn Master, GPS 56, 14 Nov 2016](https://commons.wikimedia.org/wiki/File:2006_Lawn_Master_Mower_(30953866266).jpg), CC BY 2.0: heavier accumulated dry grass, oily crankcase, sun-aged polymer and contact abrasion. It has a rigid catcher, unlike our fabric bag; use only the engine/deck/wheel wear. Our default age lies between the two used examples.

## Authored dimensional schedule

Dimensions lacking published tolerances are explicit design estimates, not claimed manufacturer measurements.

| Feature | Design | Basis / uncertainty |
| --- | --- | --- |
| Blade sweep | 533.4 mm | Published 21 in nominal, exact inch conversion |
| Tire diameters | 177.8 / 203.2 mm | Published 7 / 8 in; measured on scripted surfaces |
| Cutting chamber | 556 mm internal diameter | 10 mm radial blade allowance; authored |
| Deck gauge / rolled hem | 2 mm / 5 mm return | Stamped construction estimate ±0.5 mm |
| Wheelbase / tread | 530 / 538 mm | Image proportions revised after photo comparison, estimate ±20 mm |
| Handle tube | 22 mm OD | Photo/parts construction estimate ±2 mm |
| Handle grip height | about 1.05 m | Ergonomic design estimate ±30 mm |
| Engine shroud | about 280 × 310 × 115 mm | 140 cc class photos, estimate ±15 mm |
| Grass bag | about 430 × 530 × 380 mm envelope | Nominal 1.9 bushel class; tapered/sagged cloth is not an exact capacity certification |
| Bag frame wire | 6 mm OD | Photo construction estimate ±1 mm |

No imported models, textures, scans, traced outlines or downloaded lighting. Direct image/PDF downloads and credits are in `refs/SOURCES.md`; `make refs` restores them.

The final overall width is authored at 608.8 mm (600 mm across wheel hardware, plus the side mulch cover), after narrowing the original 670 mm wheel stance during review. [Toro’s 21 in gas push mower](https://www.toro.com/en/product/21311) publishes 23 in / 58 cm overall width; this independent class check supports the narrower stance. The original design retains about 25 mm more overall width for its individual adjuster hardware. The final 1.551 m length and 1.091 m released-bail height are ergonomic design dimensions, not TB120B published specifications.

## Owner correction dimensions

The accepted mower's follow-up brief specifies a 5–6 mm sheathed control cable
and an 8–10 mm operator-presence rod. The corrected design uses 5.6 mm and 9 mm,
respectively. These are owner-specified design ranges, not manufacturer claims.
The rod is spring-returned forward in its released pose, with molded pivot bosses;
its new held stop is −64.5° about the same X pivot. The handle still folds 135°.
The revised released-bail envelope is about 1056.5 mm high. The used Famartin photo
remains the camera/cloth/cable looking reference; the GPS 56 mower informs the
aged molded catcher top. The hybrid molded-top/fabric design remains original.
