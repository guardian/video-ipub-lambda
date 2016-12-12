from __future__ import absolute_import
import unittest
import os


class TestParser(unittest.TestCase):
    def test_invalid_filename_raise(self):
        from xml.etree.cElementTree import ParseError
        from Parser import Parser
        
        with self.assertRaises(ParseError):
            p = Parser("<somethingNOTXML")
        
    def test_get_metadata(self):
        from Parser import Parser
        
        path = os.path.join(os.path.dirname(__file__),"testdata/160615ClericInterview.meta.xml")
        with open(path) as f:
            p = Parser(f.read())
        self.assertEqual(p.get('gnm_master_website_headline'),"150616 Clare Aus")
        self.assertEqual(p.get('meta:gnm_master_website_headline'), "150616 Clare Aus")
        self.assertEqual(p.get('movie:container'), "mp4")
        self.assertEqual(p.get('track:vide:index'), "1")
        self.assertEqual(p.get('meta:invalid-key-with-default', default="boo!"), "boo!")
        
    def test_invalid_metadata_raise(self):
        from Parser import Parser
        path = os.path.join(os.path.dirname(__file__),"testdata/160615ClericInterview.meta.xml")
        with open(path) as f:
            p = Parser(f.read())
        
        with self.assertRaises(KeyError):
            p.get('flobadobadob')
            
        with self.assertRaises(KeyError):
            p.get("one:too:many:")