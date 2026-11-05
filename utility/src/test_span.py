"""Independent mathematical and clearance controls for the generator."""
import math,unittest
from span import catenary,sample,screen_width,sag_from_tension
from ribbon import data


class CatenaryTests(unittest.TestCase):
    def test_tension(self):
        p,q=(0,0,10),(0,48,12)
        sag=sag_from_tension(p,q,.2158,550)
        c=catenary(p,q,sag)
        self.assertAlmostEqual(c['a']*.2158*9.80665,550,places=8)
        self.assertGreater(sag,sag_from_tension(p,q,.2158,1100))
    def test_unequal_supports(self):
        for rise in (-3,0,3):
            p,q=(2,3,9),(26,35,9+rise)
            curve=catenary(p,q,.9)
            self.assertLess(math.dist(curve['point'](0),p),1e-9)
            self.assertLess(math.dist(curve['point'](1),q),1e-9)
            self.assertAlmostEqual((p[2]+q[2])/2-curve['point'](.5)[2],.9,places=10)
            # A catenary's second derivative obeys z'' = sqrt(1+z'^2)/a.
            t=.43;dt=1e-4;L=40;dz=(curve['point'](t+dt)[2]-curve['point'](t-dt)[2])/(2*dt*L)
            ddz=(curve['point'](t+dt)[2]-2*curve['point'](t)[2]+curve['point'](t-dt)[2])/(dt*L)**2
            self.assertAlmostEqual(ddz,math.sqrt(1+dz*dz)/curve['a'],places=7)
    def test_polyline_error(self):
        p,q=(0,0,10),(0,60,12);pts,report=sample(p,q,1.6,.008)
        truth=catenary(p,q,1.6)['point']
        for a,b in zip(pts,pts[1:]):
            for k in range(1,10):
                t=k/10;z=a[2]*(1-t)+b[2]*t;y=a[1]*(1-t)+b[1]*t
                self.assertLess(abs(z-truth(y/60)[2]),.0081)
        self.assertGreater(report['arc_m'],math.dist(p,q))
    def test_invalid(self):
        for end,sag in [((0,0,20),1),((0,40,10),0),((0,40,10),-1),((0,40,10),20)]:
            with self.assertRaises(ValueError):catenary((0,0,10),end,sag)
    def test_far_coverage(self):
        for depth in (20,50,100,200):
            w=screen_width(.01,depth)
            self.assertAlmostEqual(w['width_px']*w['coverage'],w['actual_px'])
            self.assertGreaterEqual(w['width_px'],.85)
        r=data([(0,0,1),(0,5,0),(0,10,1)],.01)
        self.assertEqual(len(r['indices'])//3,4)
        self.assertTrue(all(abs(math.sqrt(sum(x*x for x in n))-1)<1e-8 for n in r['normals']))


if __name__=='__main__':unittest.main()
