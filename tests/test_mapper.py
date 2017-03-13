from __future__ import absolute_import
import unittest
import os
from mock import MagicMock


class TestRealData(unittest.TestCase):
    def test_realdata_elastic(self):
        from Parser import Parser
        from Mapper import Mapper
        from pprint import pprint
        
        with open(os.path.join(os.path.dirname(__file__),'testdata/realdata_elastic.xml')) as f:
            p = Parser(f.read())
            
        m = Mapper()
        mapped_data = m.map_metadata(p)
        
        pprint(mapped_data)
        
class TestMapperCore(object):
    """
    Mixin class that implements the actual test methods
    """
    TESTDATA = {}
    TESTMAPPED = {}
    
    def _return_datakey(self, k, default=None):
        if k in self.TESTDATA:
            return self.TESTDATA[k]
        else:
            if default is not None:
                return default
            else:
                raise KeyError
        
    def test_get_metadata(self):
        from Mapper import Mapper
        from Parser import Parser
        from pprint import pprint

        p = Parser("<?xml version=\"1.0\"?><meta-data></meta-data>")
        p.get = MagicMock(side_effect=self._return_datakey)
        m = Mapper()
        mapped_data = m.map_metadata(p)
        pprint(mapped_data)
        self.assertDictEqual(mapped_data, self.TESTMAPPED)


class TestMappingOne(unittest.TestCase, TestMapperCore):
    TESTDATA = {
        u'track:audi:bitrate': "128",
        u'track:audi:format' : "aac",
        u'meta:aspect_ratio' : "16x9",
        u'movie:duration'    : 123.45,
        u'meta:FCS asset ID' : "KP-1234-2",
        u'movie:size'        : 53234,
        u'movie:format'      : "mp4",
        u'track:vide:height' : "720",
        u'track:vide:width'  : "1280",
        u'meta:for_mobile'   : "0",
        u'meta:is_multirate' : "0",
        u'meta:octopus ID'   : "12345678",
        u'meta:cdn_url'      : "http://path/to/rendition.mp4",
        u'track:vide:bitrate': "768",
        u'track:vide:format' : "h264",
        u'filename': "some_filename.mxf"
    }
    
    TESTMAPPED = {
        u'abitrate'    : 128.0,
        u'acodec'      : 'aac',
        u'aspect'      : '16x9',
        u'duration'    : 123.45,
        u'fcs_id'      : 'KP-1234-2',
        u'file_size'   : 53234,
        u'format'      : 'mp4',
        u'frame_height': '720',
        u'frame_width' : '1280',
        u'mobile'      : '0',
        u'multirate'   : '0',
        u'octopus_id'  : '12345678',
        u'url'         : 'http://path/to/rendition.mp4',
        u'vbitrate'    : 768.0,
        u'vcodec'      : 'h264',
        u'filename': "some_filename.mxf"
    }


class TestMappingTwo(unittest.TestCase, TestMapperCore):
    TESTDATA = {
        u'track:audi:aac_settings_bitrate': "128000",
        u'track:audi:codec'               : "aac",
        u'meta:aspect_ratio'               : "16x9",
        u'meta:durationSeconds'            : 123.45,
        u'meta:itemId'                     : "KP-123456-1",
        u'movie:size'                      : 234125,
        u'movie:extension'                 : "mp4",
        u'track:vide:height'               : "720",
        u'track:vide:width'                : "1280",
        u'meta:for_mobile'                 : "0",
        u'meta:is_multirate'               : "0",
        u'meta:gnm_master_generic_titleid' : "23455",
        u'meta:cdn_url'                    : "http://path/to/rendition.mp4",
        u'track:vide:h264_settings_bitrate': "768000",
        u'track:vide:codec'                : "h264",
        u'originalFilename': "some_filename.mxf",
        u'__collection': "VX-1234"
    }
    
    TESTMAPPED = {u'abitrate'    : 128.0,
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
                  u'vbitrate'    : 768.0,
                  u'vcodec'      : 'h264',
                  u'originalFilename': "some_filename.mxf",
                  u'project': "VX-1234"
                  }


class TestMappingIncomplete(unittest.TestCase, TestMapperCore):
    TESTDATA = {
        u'track:audi:bitrate': "128",
        u'track:audi:format' : "aac",
        u'meta:aspect_ratio' : "16x9",
        u'movie:duration'    : 123.45,
        u'meta:FCS asset ID' : "KP-1234-2",
        u'movie:size'        : 53234,
        u'movie:format'      : "mp4",
        u'track:vide:height' : "720",
        u'track:vide:width'  : "1280",
        u'meta:octopus ID'   : "12345678",
        u'meta:cdn_url'      : "http://path/to/rendition.mp4",
        u'track:vide:bitrate': "768",
        u'track:vide:format' : "h264",
        u'filename': "rendition.mxf"
    }
    
    TESTMAPPED = {
        u'abitrate'    : 128.0,
        u'acodec'      : 'aac',
        u'aspect'      : '16x9',
        u'duration'    : 123.45,
        u'fcs_id'      : 'KP-1234-2',
        u'file_size'   : 53234,
        u'format'      : 'mp4',
        u'frame_height': '720',
        u'frame_width' : '1280',
        u'mobile'      : '0',
        u'multirate'   : '0',
        u'octopus_id'  : '12345678',
        u'url'         : 'http://path/to/rendition.mp4',
        u'vbitrate'    : 768.0,
        u'vcodec'      : 'h264',
        u'filename': "rendition.mxf"
    }