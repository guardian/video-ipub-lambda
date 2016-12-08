from __future__ import absolute_import
import unittest
import os


class TestParser(unittest.TestCase):
    def test_get_metadata(self):
        from Parser import Parser
        path = os.path.join(os.path.dirname(__file__),"testdata/160615ClericInterview.meta.xml")
        p = Parser(path)
        self.assertEqual(p.get('gnm_master_website_headline'),"150616 Clare Aus")
        
    def test_invalid_metadata_raise(self):
        from Parser import Parser
        path = os.path.join(os.path.dirname(__file__),"testdata/160615ClericInterview.meta.xml")
        p = Parser(path)
        with self.assertRaises(KeyError):
            p.get('flobadobadob')