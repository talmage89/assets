"""Published cable envelopes, distinct from a screen-space width policy.

Sources and construction assumptions are recorded in refs/SOURCES.md. The
fiber line is a maintained two-cable bundle, not a 32 mm individual fiber.
All dimensions are metres. No manufacturer marking is reproduced.
"""
PRIMARY = .398 * .0254                 # Raven 1/0 6/1 ACSR
NEUTRAL = .316 * .0254                 # Sparrow #2 6/1 ACSR
SERVICE_HOT = .303 * .0254             # #4 XLPE, 45 mil insulation
SERVICE_MESSENGER = .250 * .0254       # #4 6/1 ACSR
SERVICE_MASS = 153 * .45359237 / 304.8 # published lb / 1,000 ft -> kg/m
SERVICE_TENSION = 300 * SERVICE_MASS / .153 # retain accepted self-weight sag
STRAND = .00635
PHONE = .037                          # GR-421 200-pair .63 mm air-core cable
CATV = .960 * .0254                   # QR860 JCA jacket, excluding strand
FIBER = .0158                         # 144-fiber loose-tube envelope


def communications(count=3):
    """Two to four separately supported cable routes, highest first.

    A fiber bundle contains two touching jackets; its own upper messenger
    remains a separate tube. Coax also has a real strand, rather than a
    fictional enlarged cable. The fourth route is retained copper plant.
    """
    rows = [dict(key='Telephone', diameter=PHONE, offset=-.36, mass=1.771, tension=4500),
            dict(key='CATV', diameter=CATV, offset=-.64, mass=.43, tension=1500)]
    if count >= 3:
        rows.insert(0,dict(key='LashedFiber',diameter=FIBER,offset=-.035,mass=.36,tension=1350,bundle=2))
    if count >= 4:
        rows.append(dict(key='LegacyCopper',diameter=.028,offset=-.90,mass=1.135,tension=4300))
    return rows
