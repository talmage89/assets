"""Numerical camera fitting: a known eye height must not drift underground."""
import math,unittest
import numpy as np
from kit.photo_match import project,calibrate

class CameraPrior(unittest.TestCase):
    def test_height_prior_and_lens_bounds(self):
        params=np.array([math.pi/2,.15,0,-25,1.7,math.log(45),0])
        points=np.array([(0,0,0),(0,0,12),(-4.5,0,6),(4.5,0,6),(0,0,3)])
        pixels=project(params,points,900,1000)[0]
        match=dict(location=(0,-24,1.7),target=(0,0,5),lens=45,crop=(0,0,900,1000),photo='unused',title='fixture',
                   camera_height_m=(1.7,.12),lens_bounds_mm=(28,80),
                   landmarks=[dict(world=p.tolist(),pixel=q.tolist()) for p,q in zip(points,pixels)])
        result=calibrate(match)
        self.assertAlmostEqual(result['shot']['location'][2],1.7,places=3)
        self.assertLess(result['residual_rms_pixels'],.05)
        self.assertTrue(28<=result['shot']['lens']<=80)
        self.assertEqual(result['camera_height_prior_m'],(1.7,.12))

if __name__=='__main__':unittest.main()
