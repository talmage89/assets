"""Portable font discovery: exact faces, aliases and actionable failures."""
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kit.fonts import find_font


class Fonts(unittest.TestCase):
    def tearDown(self):
        find_font.cache_clear()

    def test_installed_faces(self):
        for family,style in [('Noto Sans','Regular'),('Noto Sans','Bold'),
                             ('DejaVu Sans','Book'),('DejaVu Sans','Bold'),
                             ('DejaVu Sans','Condensed Bold')]:
            self.assertTrue(Path(find_font(family,style)).is_file())

    def test_missing_family_and_style(self):
        for family,style in [('Assets Missing Font','Regular'),('Noto Sans','Missing Style')]:
            with self.assertRaisesRegex(RuntimeError,f'{family}.*{style}'):
                find_font(family,style)

    def test_missing_fontconfig(self):
        with patch('kit.fonts.subprocess.run',side_effect=FileNotFoundError):
            with self.assertRaisesRegex(RuntimeError,'Noto Sans.*Bold.*fontconfig'):
                find_font('Noto Sans','Bold')

    def test_failed_fontconfig(self):
        with patch('kit.fonts.subprocess.run',side_effect=subprocess.CalledProcessError(1,'fc-match')):
            with self.assertRaisesRegex(RuntimeError,'Noto Sans.*Bold'):
                find_font('Noto Sans','Bold')


if __name__=='__main__':unittest.main(argv=[__file__])
