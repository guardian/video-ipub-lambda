from __future__ import absolute_import
import unittest
import os
from mock import MagicMock
import logging


class TestDatabase(unittest.TestCase):
    def __init__(self,*args,**kwargs):
        super(TestDatabase,self).__init__(*args,**kwargs)
        self._cached_id = None
        
    def test_get_filename(self):
        from Database import Database
        
        d = Database(make_connection=False)
        
        testmeta = {'filename': 'thisisafile', 'originalFilename': 'wrongfile', 'otherdata':'other'}
        self.assertEqual(d._get_filename(testmeta),"thisisafile")

        testmeta = {'originalFilename': 'thisisafile', 'otherdata': 'other'}
        self.assertEqual(d._get_filename(testmeta), "thisisafile")
        
        testmeta = {'otherdata':'other','random stuff': 'yadayada','rhubarb': 'custard','spam':'eggs'}
        self.assertIsNone(d._get_filename(testmeta))
        
    def test_make_filebase(self):
        from Database import Database
        d = Database(make_connection=False)
        
        self.assertEqual(d._make_filebase("file.extension"),"file")
        self.assertEqual(d._make_filebase("file.ext.something"),"file.ext")
        self.assertEqual(d._make_filebase("file"),"file")
        
    def test_make_new_record(self):
        from Database import Database
        d = Database(make_connection=True)
        
        self._cached_id = d._make_new_record("testfilebase",1234567,"KP-345")
        logging.info("cached id {0}".format(self._cached_id))
        self.assertIsNotNone(self._cached_id)
        
    def test_find_in_database(self):
        from Database import Database, NotFound, InvalidData
        d = Database(make_connection=True)
        
        self._cached_id = d._make_new_record("testfilebase2", 1234568, "KP-347")
        print "cached id {0}".format(self._cached_id)
        self.assertEqual(d._find_in_database("testfilebase2"),self._cached_id)
        
        with self.assertRaises(NotFound):
            d._find_in_database("some_invalid pathname!")
            
    