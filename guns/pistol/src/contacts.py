"""Required surface contacts, independent of swept clearance and serialization."""
import bpy
from mathutils import Vector
from kit import weapon,motion,assembly

def measure(arm):
    rows=[]
    def contact(a,b,limit,kind):
        left=bpy.data.objects[a];right=bpy.data.objects[b]
        d,method=assembly.distance(left,right)
        rows.append(dict(kind=kind,parts=[a,b],distance_m=d,limit_m=limit,method=method,passed=d<=limit))
    weapon.pose(arm,'FireLast',15)
    contact('SlideStop_Lug','Slide_Shell',.00015,'stop engagement')
    # Independent opposing-face samples verify overlap at the rear notch wall,
    # rather than mistaking an unrelated closest corner for lock engagement.
    lug=motion.surface(bpy.data.objects['SlideStop_Lug'])
    slide=motion.surface(bpy.data.objects['Slide_Shell'])
    face=[]
    for x,z in [(-.0120,.04135),(-.0116,.04135),(-.0125,.04135)]:
        hit=slide['tree'].ray_cast(Vector((x,.012,z)),Vector((0,1,0)),.003)
        face.append(None if hit[0] is None else dict(point=list(hit[0]),normal=list(hit[1]),
            lug_distance_m=lug['tree'].find_nearest(hit[0])[3]))
    assert all(p and p['normal'][1]>.8 and p['lug_distance_m']<.00016 for p in face),face
    rows.append(dict(kind='opposing stop/notch faces',samples=face,passed=True))
    weapon.pose(arm,'Idle',0)
    for name in ('Magazine_FeedLip','Magazine_FeedLip.001'):
        contact(name,'Magazine_TopRound_Case',.00015,'cartridge retention')
        contact(name,'Magazine_Body',.0002,'curled lip attached to shell')
    # Measured projected nose containment complements solid clearance: a
    # nonintersecting cartridge could still visibly project past the front wall.
    body=motion.surface(bpy.data.objects['Magazine_Body'])
    noses=[motion.surface(bpy.data.objects[n])['hi'].y for n in ('Magazine_TopRound_Bullet','Magazine_SecondRound_Bullet')]
    assert max(noses)<=body['hi'].y
    rows.append(dict(kind='cartridge noses behind body front envelope',nose_y_m=noses,
                     body_front_y_m=body['hi'].y,passed=True))
    contact('Magazine_Follower','Magazine_SecondRound_Case',.00015,'follower support')
    left=motion.surface(bpy.data.objects['Magazine_FeedLip']);right=motion.surface(bpy.data.objects['Magazine_FeedLip.001'])
    gap=min(abs(p.x) for p in left['points'])+min(abs(p.x) for p in right['points'])
    case=motion.surface(bpy.data.objects['Magazine_TopRound_Case']);diameter=case['hi'].x-case['lo'].x
    assert gap<diameter-.001,(gap,diameter)
    rows.append(dict(kind='retention aperture',gap_m=gap,case_diameter_m=diameter,passed=True))
    contact('Frame_Grip','Magazine_Floorplate',.00015,'magazine seating shoulder')
    weapon.pose(arm,'Reload',28)
    d,method=assembly.distance(bpy.data.objects['Frame_Grip'],bpy.data.objects['Magazine_Floorplate'])
    assert d>.03,d
    rows.append(dict(kind='withdrawn magazine leaves seat',distance_m=d,method=method,passed=True))
    weapon.pose(arm,None,0)
    if not all(r['passed'] for r in rows):raise AssertionError(rows)
    return rows
