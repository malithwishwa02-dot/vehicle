"""
Unit Tests for Artifact Pipeline
"""
import unittest
import shutil
import json
import tempfile
import os
from pathlib import Path
from core.pipeline import ArtifactPipeline

class TestArtifactPipeline(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.pipeline = ArtifactPipeline(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_proxy_validation(self):
        # Valid user:pass
        valid_auth = "user:pass@127.0.0.1:8080"
        res = self.pipeline.process_proxy(valid_auth)
        self.assertTrue(res['valid'])
        self.assertEqual(res['host'], '127.0.0.1')
        self.assertEqual(res['user'], 'user')

        # Valid no auth
        valid_no_auth = "127.0.0.1:8080"
        res = self.pipeline.process_proxy(valid_no_auth)
        self.assertTrue(res['valid'])
        self.assertEqual(res['host'], '127.0.0.1')

        # Invalid
        invalid = "broken_proxy_string"
        res = self.pipeline.process_proxy(invalid)
        self.assertFalse(res['valid'])

    def test_fullz_validation(self):
        valid_fullz = {
            "name": "John Doe",
            "address": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "cc_number": "4111111111111111",
            "cc_exp": "12/25",
            "cc_cvv": "123"
        }
        res = self.pipeline.process_fullz(valid_fullz)
        self.assertTrue(res['valid'])

        invalid_fullz = {"name": "Jane Doe"} # Missing fields
        res = self.pipeline.process_fullz(invalid_fullz)
        self.assertFalse(res['valid'])

    def test_cookie_ingest(self):
        # Create dummy JSON cookie
        cookie_file = Path(self.test_dir) / "cookies.json"
        with open(cookie_file, 'w') as f:
            json.dump([{"name": "session", "value": "123"}], f)
        
        res = self.pipeline.ingest_cookie_jar(str(cookie_file))
        self.assertTrue(res['valid'])
        self.assertEqual(res['format'], 'JSON')

if __name__ == '__main__':
    unittest.main()
