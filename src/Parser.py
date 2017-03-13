import xml.etree.cElementTree as ET


class Parser(object):
    def __init__(self,datacontent):
        super(Parser,self).__init__()
        self._data = ET.fromstring(datacontent)
        
    def get(self,key,default=None):
        keyparts = key.split(':')
        if len(keyparts)==1:
            searchpath = "meta[@value='inmeta']/meta[@name='{0}']".format(key)
        elif len(keyparts)==2:
            section=keyparts[0]
            if section=="meta": section="meta-source"
            searchpath = "meta[@name='{0}']/meta[@name='{1}']".format(section,keyparts[1])
        elif len(keyparts)==3:
            section=keyparts[0]
            subsection=keyparts[1]
            searchpath = "meta[@name='{0}']/meta[@name='type'][@value='{1}']/../meta[@name='{2}']".format(section,subsection,keyparts[2])
        else:
            raise KeyError("too many : in key!")
        
        elem = self._data.find(searchpath)
        if elem is None:
            if default is None:
                raise KeyError(key)
            else:
                return default
        return elem.get('value')
    
    def dump(self):
        from bs4 import BeautifulSoup
        
        print BeautifulSoup(ET.tostring(self._data), "xml").prettify(encoding="UTF-8")
        