"""PBR filtering preserves linear energy, independent masks and vector frames."""
import unittest
import subprocess
import tempfile
import hashlib
from pathlib import Path
import numpy as np
from kit.downsample import filter_pixels
from kit.image_io import linear_to_srgb,write_png,read_png

ROOT=Path(__file__).resolve().parents[1]


class PBRFilterTests(unittest.TestCase):
    def test_existing_three_map_cli_is_read_only(self):
        (ROOT/'build').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'build') as temp:
            folder=Path(temp);source=folder/'bake';out=folder/'ship'
            for name,value in [('BaseColor',[.3,.5,.7,.4]),('Normal',[.5,.5,1]),('ORM',[1,.6,.8])]:
                write_png(source/f'T_Fixture_{name}.png',np.tile(value,(4,4,1)))
            before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.iterdir()}
            subprocess.run(['python3',str(ROOT/'kit/downsample.py'),'--source',str(source),'--out',str(out),
                            '--asset','Fixture','--size','2','--alpha-mode','independent'],check=True,capture_output=True)
            self.assertEqual(before,{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.iterdir()})
            for name in ['BaseColor','Normal','ORM']:
                self.assertTrue(np.allclose(read_png(out/f'T_Fixture_{name}.png')[0,0],read_png(source/f'T_Fixture_{name}.png')[0,0],atol=1/255))

    def test_color_energy_and_two_alpha_meanings(self):
        a=np.zeros((2,2,4),float);a[:,1]=1
        independent=filter_pixels(a,1,'BaseColor','independent')[0,0]
        coverage=filter_pixels(a,1,'BaseColor','coverage')[0,0]
        self.assertTrue(np.allclose(independent[:3],linear_to_srgb(np.array([.5]*3))))
        self.assertTrue(np.allclose(coverage,[1,1,1,.5]))
        self.assertAlmostEqual(independent[3],.5)
        self.assertTrue(np.allclose(filter_pixels(a[:,:,:3],1,'Emission')[0,0],independent[:3]))
        self.assertTrue(np.array_equal(a[:,0],np.zeros((2,4))))

    def test_normal_directions_and_roughness_energy(self):
        a=np.tile([1.,.5,.5],(2,2,1));a[:,1]=[.5,.5,1]
        expected=np.array([1.,0,1])/np.sqrt(2)
        for name in ['Normal','CoatNormal']:
            actual=filter_pixels(a,1,name)[0,0]*2-1
            self.assertTrue(np.allclose(actual,expected))
        a=np.zeros((2,2,3),float);a[:,1]=1
        for name in ['ORM','Clearcoat']:
            self.assertTrue(np.allclose(filter_pixels(a,1,name)[0,0],[.5,np.sqrt(.5),.5]))
        self.assertTrue(np.allclose(filter_pixels(a,1,'Transmission'),.5))
        for args in [(3,'ORM'),(0,'ORM'),(1,'unknown')]:
            with self.assertRaises(ValueError):filter_pixels(a,*args)


if __name__=='__main__':unittest.main()
