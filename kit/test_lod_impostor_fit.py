"""CPU regression for a render-derived fixed-plane impostor fit."""
import unittest
import numpy as np
from kit.lod_impostor_fit import fit


class ImpostorFit(unittest.TestCase):
    def test_joint_coverage_and_radiance(self):
        yy,xx=np.mgrid[-1:1:32j,-1:1:32j];frames=[]
        for i in range(8):
            theta=i*2*np.pi/8;radius=np.hypot(.65*np.cos(theta),.5*np.sin(theta))
            alpha=np.clip((1-(xx/radius)**2-(yy/.85)**2)*8,0,1)
            rgb=np.zeros((32,32,3));rgb[:]=[.12+.02*np.cos(theta),.23,.08]
            frames.append(np.uint8(np.concatenate([rgb,alpha[:,:,None]],axis=2)*255+.5))
        before=np.array(frames);result,report=fit(before,size=16,iterations=30)
        self.assertEqual(result.shape,(4,16,16,4))
        self.assertLess(report['alpha_mse_after'],report['alpha_mse_before']*.8)
        self.assertLess(report['premultiplied_linear_rgb_mse_after'],report['premultiplied_linear_rgb_mse_before'])
        again,_=fit(before,size=16,iterations=30)
        self.assertTrue(np.array_equal(result,again))
        self.assertTrue(np.array_equal(before,frames))
        self.assertGreater(result[:,:,:,3].max(),100)
        self.assertEqual(result.dtype,np.uint8)
        self.assertTrue(np.all(result[:,0,:,3]==0),'exterior visual hull grew opaque specks')
        # Low-opacity fit residuals must not invent saturated bright colors.
        self.assertLess(result[:,:,:,:3].max(),100)

    def test_bad_capture_shape(self):
        with self.assertRaises(ValueError):fit(np.zeros((8,31,32,4),np.uint8),size=16)


if __name__=='__main__':unittest.main()
