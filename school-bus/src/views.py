"""All views retain meter scale. Hero is eye-height with a 40mm lens."""
SHOTS=dict(
    hero=dict(location=(-9.4,-13.8,1.68),target=(0,-.3,1.64),lens=40,aspect=1.78),
    front=dict(location=(0,-22,1.60),target=(0,-.2,1.60),lens=48,aspect=1.1,ortho=4.2),
    side=dict(location=(-25,0,1.60),target=(0,0,1.60),lens=50,aspect=2.8,ortho=14.0),
    rear=dict(location=(0,23,1.65),target=(0,0,1.65),lens=48,aspect=1.1,ortho=4.2),
    top=dict(location=(0,0,30),target=(0,0,0),lens=50,aspect=2.8,ortho=14.0,roll=1.570796326795),
    rear_three_quarter=dict(location=(10.5,16,2.4),target=(0,1,1.6),lens=45,aspect=1.78),
    front_detail=dict(location=(-4.7,-10.0,1.72),target=(0,-4.85,1.72),lens=48,aspect=1.5),
    entrance=dict(location=(-4.9,-5.75,1.62),target=(-.75,-3.25,1.49),lens=45,aspect=1.3,pose='entrance'),
    interior=dict(location=(-3.7,-4.0,1.80),target=(.55,-3.30,1.92),lens=34,aspect=1.35,pose='entrance',dome=True,exposure=.75),
    aisle=dict(location=(0,-2.95,2.08),target=(0,4.8,1.95),lens=24,aspect=1.6,pose='entrance',dome=True,exposure=2.1),
    warning=dict(location=(6.2,-11.8,2.12),target=(.15,-4.70,1.50),lens=40,aspect=1.5,pose='warning',lit=True),
    emergency=dict(location=(3.4,10.6,1.72),target=(0,5.9,1.83),lens=48,aspect=1.3,pose='rear_exit',dome=True,exposure=.25),
    roof=dict(location=(5,7,8),target=(0,1.3,2.9),lens=45,aspect=1.6,pose='hatches'),
    scale=dict(location=(-12.2,-17,1.68),target=(-.4,-.2,1.45),lens=40,aspect=1.78,human=True),
    fleet=dict(location=(-19,-23,7.0),target=(-.5,0,1.35),lens=42,aspect=1.78,fleet=True),
)
