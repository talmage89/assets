"""Photographic acceptance bounds include zero tails and highlight chroma."""
import copy
import unittest
from guns.common.paint_review import comparison


class PaintBoundsTests(unittest.TestCase):
    def setUp(self):
        self.photo=dict(value_p10_p50_p90=[0,50,100],highlight_rgb=[100,100,100],
                        highlight_value=100,highlight_color=[1,1,1])

    def test_exact_zero_is_required(self):
        self.assertTrue(comparison(self.photo,self.photo)[1])
        changed=copy.deepcopy(self.photo);changed['value_p10_p50_p90'][0]=1
        self.assertFalse(comparison(changed,self.photo)[1])

    def test_median_and_tail_have_different_bounds(self):
        changed=copy.deepcopy(self.photo);changed['value_p10_p50_p90'][1]=56
        self.assertFalse(comparison(changed,self.photo)[1])
        changed=copy.deepcopy(self.photo);changed['value_p10_p50_p90'][2]=114
        self.assertTrue(comparison(changed,self.photo)[1])
        changed['value_p10_p50_p90'][2]=116
        self.assertFalse(comparison(changed,self.photo)[1])

    def test_rgb_agreement_does_not_waive_highlight_color(self):
        changed=copy.deepcopy(self.photo);changed.update(highlight_rgb=[110,90,100],
            highlight_value=110,highlight_color=[1,90/110,100/110])
        self.assertFalse(comparison(changed,self.photo)[1])


if __name__=='__main__':unittest.main()
