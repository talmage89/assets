"""Sampled checkpoint motions; simplified steering bearing contacts are explicit."""
MOTIONS=[]
for name,axis,lo,hi,step in [
    ('Entrance_front','Z',0,98,2),('Entrance_rear','Z',-98,0,2),
    ('Emergency_rear','Z',0,105,3),('Emergency_side','Z',-105,0,3),
    ('Roof_hatch_front','X',-80,0,4),('Roof_hatch_rear','X',-80,0,4),
    ('Stop_arm','Z',-90,0,3),('Crossing_arm','Z',-90,0,3),
    ('Steer_FL','Z',-40,40,2),('Steer_FR','Z',-40,40,2),
    *[(f'Wheel_{code}','X',0,360,15) for code in ['FL','FR','RL_outer','RL_inner','RR_outer','RR_inner']]]:
    allow=[]
    if name.startswith('Steer_'):
        allow=[dict(moving='Front spindle',fixed='Front axle',reason='Simplified coaxial spindle/axle steering-bearing interface; chassis is an exterior visual approximation')]
    MOTIONS.append(dict(node=name,axis=axis,range=[lo,hi],step=step,tolerance_m=.0005,allow=allow))
