"""Reference selection keeps clean checks independent of unrelated remote files."""
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from kit.fetch_refs import fetch
ROOT=Path(__file__).resolve().parents[1]

class Response(io.BytesIO):
    headers={'Content-Type':'image/png'}

class FetchReferences(unittest.TestCase):
    def setUp(self):
        (ROOT/'build/tmp').mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'build/tmp')
        self.addCleanup(self.temp.cleanup);self.folder=Path(self.temp.name)
        (self.folder/'SOURCES.md').write_text('| a.png | https://example.invalid/a.png | original fixture |\n| b.png | https://example.invalid/b.png | original fixture |\n')
    def test_legacy_downloads_all_and_preserves_existing(self):
        (self.folder/'a.png').write_bytes(b'existing')
        with patch('kit.fetch_refs.urllib.request.urlopen',return_value=Response(b'fixture')) as request:
            fetch(self.folder)
        self.assertEqual(request.call_count,1)
        self.assertEqual((self.folder/'a.png').read_bytes(),b'existing')
        self.assertEqual((self.folder/'b.png').read_bytes(),b'fixture')
    def test_only_registered_subset(self):
        with patch('kit.fetch_refs.urllib.request.urlopen',return_value=Response(b'fixture')) as request:
            fetch(self.folder,['b.png'])
        self.assertEqual(request.call_args.args[0].full_url,'https://example.invalid/b.png')
        self.assertFalse((self.folder/'a.png').exists())
    def test_unknown_selection_makes_no_request(self):
        with patch('kit.fetch_refs.urllib.request.urlopen') as request:
            with self.assertRaisesRegex(ValueError,'Unregistered'):fetch(self.folder,['missing.png'])
        request.assert_not_called()
    def test_non_image_and_unsafe_names_rejected(self):
        response=Response(b'html');response.headers={'Content-Type':'text/html'}
        with patch('kit.fetch_refs.urllib.request.urlopen',return_value=response):
            with self.assertRaisesRegex(ValueError,'not image/PDF'):fetch(self.folder,['a.png'])
        self.assertFalse((self.folder/'a.png').exists())
        (self.folder/'SOURCES.md').write_text('| ../bad.png | https://example.invalid/bad.png | fixture |\n')
        with patch('kit.fetch_refs.urllib.request.urlopen') as request:
            with self.assertRaises(ValueError):fetch(self.folder)
        request.assert_not_called()

if __name__=='__main__':unittest.main()
