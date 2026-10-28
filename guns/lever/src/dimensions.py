"""Original visual asset landmarks, millimeters. +Y muzzle, +Z up, +X right.

These are animation/art parameters, not manufacturing drawings. Published
external dimensions and photo-derived estimates are distinguished in README.
"""
BORE = 48.0
BREECH = 200.0
MUZZLE = 708.0
TUBE = 20.0
TUBE_PITCH = 64.77
CAPACITY = 6
SIGHT = 66.0
HEADS = {
    'Root': (0, 0, 0), 'Lever': (0, 124, -1),
    'Link': (0, 195, 5), 'Bolt': (0, 140, 48),
    'LockingBlock': (0, 180, 30), 'Carrier': (0, 85, 7),
    'Hammer': (0, 70, 30), 'Trigger': (0, 83, 0), 'Sear':(0,83,0),
    'LoadingGate': (15.2, 122, 20),
    'Follower': (0, 210 + CAPACITY*TUBE_PITCH, 20),
    'Magazine': (0, 210, 20), 'CarrierRound': (0, 85, 7),
    'ChamberRound': (0, 200, 48), 'FiredCase': (0, 200, 48),
    'FiredGuide': (0, 200, 48), 'CarrierGuide': (0,85,7),
    'InsertGuide': (25, 113, 20), 'InsertRound': (25, 113, 20),
    'LeverHand': (0, 0, -29),
    **{'Tube'+str(i+1): (0, 210+i*TUBE_PITCH, 20) for i in range(CAPACITY)},
}
PARENTS = {'Lever':'Link', 'Sear':'Trigger', 'FiredGuide':'Bolt', 'FiredCase':'FiredGuide', 'CarrierRound':'CarrierGuide',
           'InsertRound': 'InsertGuide', 'LeverHand': 'Lever'}
SOCKETS = {
    'Socket_Muzzle': (0, MUZZLE, BORE),
    'Socket_Foregrip': (-18, 307, 13),
    'Socket_Butt': (0, -253.5, -50),
    'Socket_Eye': (0, -85, SIGHT),
    'Socket_Ejection': (0, 114, 68),
    'Socket_MagWell': (16, 147, 20),
    'Socket_Magazine': HEADS['Magazine'],
    'Socket_SupportHand': (-18, 307, 13),
    'Socket_Shell': HEADS['InsertGuide'],
    'Socket_LeverHand': HEADS['LeverHand'],
}
RIDING = {'Socket_Magazine':'Magazine', 'Socket_SupportHand':'Root',
          'Socket_Shell':'InsertGuide', 'Socket_LeverHand':'LeverHand'}
