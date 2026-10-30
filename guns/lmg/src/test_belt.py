"""Regression for observed branch popping, count masking and visible continuity."""
import unittest,math
from belt import solve,transforms,game_pose,PITCH,COUNT
class BeltTests(unittest.TestCase):
 def test_chords_and_no_branch_jump(self):
  before=None
  for k in range(301):
   p=solve(k/100)
   self.assertLess(max(abs(math.dist(a,b)-PITCH) for a,b in zip(p,p[1:])),1e-6)
   if before:self.assertLess(max(math.dist(a,b) for a,b in zip(p,before)),.8)
   before=p
 def test_count_end(self):
  for count in range(COUNT+1):
   p=transforms(0,count)
   self.assertEqual(sum(p[f'BeltRound{i:02d}']['scale'][0]>0 for i in range(COUNT)),count)
 def test_streaming_visible_slots(self):
  for count in (1,4,199):
   a=game_pose(count,1,200);b=game_pose(count+1,0,200)
   # The outgoing owner recycles only at the hidden ends. Every other slot
   # retains its position rather than popping back one display spacing.
   outgoing=count%COUNT
   for i in range(COUNT):
    if i!=outgoing:self.assertLess(math.dist(a[f'BeltLink{i:02d}']['loc'],b[f'BeltLink{i:02d}']['loc']),1e-7)
if __name__=='__main__':unittest.main()
