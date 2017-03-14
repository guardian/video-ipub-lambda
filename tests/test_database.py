from __future__ import absolute_import
import unittest
import os
import logging


class TestDatabase(unittest.TestCase):
    def __init__(self,*args,**kwargs):
        super(TestDatabase,self).__init__(*args,**kwargs)
        self._cached_id = None
        
    def test_remove_extension(self):
        from Database import Database
        str = "filename.xyz"
        self.assertEqual(Database._remove_extension(str),"filename")
        
        str = "barefilename"
        self.assertEqual(Database._remove_extension(str),"barefilename")
        
        str = "/path/to/filename.xyz"
        self.assertEqual(Database._remove_extension(str), "/path/to/filename")
        
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
            
    def test_add_encoding(self):
        from Database import Database, NotFound
        
        d = Database(make_connection=True)
        
        fake_id = 9999
        testmeta = {u'abitrate'    : '128000',
                  u'acodec'      : 'aac',
                  u'aspect'      : '16x9',
                  u'duration'    : 123.45,
                  u'fcs_id'      : 'KP-123456-1',
                  u'file_size'   : 234125,
                  u'format'      : 'mp4',
                  u'frame_height': '720',
                  u'frame_width' : '1280',
                  u'mobile'      : '0',
                  u'multirate'   : '0',
                  u'octopus_id'  : '23455',
                  u'url'         : 'http://path/to/rendition.mp4',
                  u'vbitrate'    : '768000',
                  u'vcodec'      : 'h264'
                  }
        expectedmeta = {u'abitrate'    : 128000,
                    u'acodec'      : 'aac',
                    u'aspect'      : '16x9',
                    u'duration'    : 123.45,
                    u'fcs_id'      : 'KP-123456-1',
                    u'file_size'   : 234125,
                    u'format'      : 'mp4',
                    u'frame_height': 720,
                    u'frame_width' : 1280,
                    u'mobile'      : 0,
                    u'multirate'   : 0,
                    u'octopus_id'  : 23455,
                    u'url'         : 'http://path/to/rendition.mp4',
                    u'vbitrate'    : 768000,
                    u'vcodec'      : 'h264'
                    }

        encid = d.add_encoding(fake_id,testmeta)
        self.assertIsNotNone(encid)
        
        fetched_row = d.get_encoding(fake_id,limit=1)
        self.assertDictContainsSubset(expectedmeta,fetched_row[0])