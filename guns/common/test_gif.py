"""Wall-clock sampling, palette encoding, first hold and lossless repeatability."""
import json
import hashlib
from pathlib import Path
import tempfile
import unittest
from PIL import Image, ImageDraw
from guns.common.gif import timeline, encode
ROOT = Path(__file__).resolve().parents[2]


class MotionGIF(unittest.TestCase):
    def test_uniform_time_and_segment_boundary(self):
        rows = timeline(dict(fps=20, sequence=[dict(clip='Fire'),dict(clip='Cycle')]),
                        dict(Fire=dict(frames=18),Cycle=dict(frames=60)),60)
        self.assertEqual(len(rows),26)
        self.assertEqual(rows[6],dict(action='Cycle',frame=0,time_s=.3))
        self.assertEqual(rows[-1]['frame'],57)
        for a,b in zip(rows,rows[1:]):
            self.assertAlmostEqual(b['time_s']-a['time_s'],.05)
        self.assertEqual(len(timeline(dict(fps=25,sequence=[dict(clip='Fire')]),
                                     dict(Fire=dict(frames=132)),60)),55)

    def test_invalid_rate_and_trim(self):
        for spec in (dict(fps=30,sequence=[dict(clip='Fire')]),
                     dict(fps=25,sequence=[dict(clip='Fire',end=18)])):
            with self.assertRaises(ValueError):
                timeline(spec,dict(Fire=dict(frames=60)),60)

    def test_encode_decoded_duration_and_repeat(self):
        folder=ROOT/'build/gif-tests';folder.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=folder) as tmp:
            base=Path(tmp);out=base/'build/gif';(out/'raw').mkdir(parents=True)
            (base/'export').mkdir();(base/'export/test.glb').write_bytes(b'fixture source identity')
            rows=timeline(dict(fps=20,sequence=[dict(clip='Cycle')]),dict(Cycle=dict(frames=12)),60)
            (out/'timeline.json').write_text(json.dumps(rows))
            digest=hashlib.sha256((base/'export/test.glb').read_bytes()).hexdigest()
            (out/'raw/shots.json').write_text(json.dumps({f'f{i:04d}': dict(row,engine='CYCLES',sha256=digest) for i,row in enumerate(rows)}))
            for i in range(len(rows)):
                im=Image.new('RGBA',(120,80),(0,0,0,0));d=ImageDraw.Draw(im)
                d.rectangle((10+i*12,20,35+i*12,50),fill=(115,92,71,255));im.save(out/'raw'/f'f{i:04d}.png')
            spec=dict(fps=20,colors=256,background=[67,70,73],source='export/test.glb',
                      output='docs/motion.gif',sequence=[dict(clip='Cycle')],camera={},samples=64)
            encode(base,spec,out);before=(base/'docs/motion.gif').read_bytes()
            report=json.loads((out/'report.json').read_text())
            self.assertEqual(report['frame_durations_ms'],[550,50,50,50])
            self.assertEqual(report['duration_ms'],700)
            with Image.open(base/'docs/motion.gif') as im:
                for i in range(im.n_frames):
                    im.seek(i);self.assertEqual(im.convert('RGB').getpixel((119,79)),(67,70,73))
            encode(base,spec,out)
            self.assertEqual(before,(base/'docs/motion.gif').read_bytes())


if __name__=='__main__':
    unittest.main()
