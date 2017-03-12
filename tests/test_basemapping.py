from __future__ import absolute_import
import unittest
import os
from mock import MagicMock


class TestBaseMapping(unittest.TestCase):
    TESTDATA = {
        u'testkey': u'testvalue'
    }
    TESTMAPPED = {}
    
    def _return_datakey(self, k, default=None):
        if k in self.TESTDATA:
            return self.TESTDATA[k]
        else:
            if default is not None:
                return default
            else:
                raise KeyError
    
    def test_evaluate(self):
        from BaseMapping import BaseMapping
        from Parser import Parser
        from pprint import pprint

        p = Parser("<?xml version=\"1.0\"?><meta-data></meta-data>")
        p.get = MagicMock(side_effect=self._return_datakey)
        
        m = BaseMapping('testkey')
        self.assertEqual(m.evaluate(p),u"testvalue")
        

class TestJoinMapping(unittest.TestCase):
    TESTDATA = {
        u'testkey': u'testvalue',
        u'testotherkey': u'testtwo'
    }
    
    TESTMAPPED = {}
    
    def _return_datakey(self, k, default=None):
        if k in self.TESTDATA:
            return self.TESTDATA[k]
        else:
            if default is not None:
                return default
            else:
                raise KeyError
    
    def test_evaluate(self):
        from JoinMapping import JoinMapping
        from Parser import Parser
        from pprint import pprint
        
        p = Parser("<?xml version=\"1.0\"?><meta-data></meta-data>")
        p.get = MagicMock(side_effect=self._return_datakey)
        
        m = JoinMapping('testkey','testotherkey', joinchar='-')
        self.assertEqual(m.evaluate(p), u"testvalue-testtwo")