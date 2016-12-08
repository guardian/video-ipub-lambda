import xml.etree.cElementTree as ET


class Parser(object):
    def __init__(self,filename):
        super(Parser,self).__init__()
        self._data = ET.parse(filename)
        
    def get(self,key,default=None):
        elem = self._data.find("meta[@value='inmeta']/meta[@name='{0}']".format(key))
        if elem is None:
            if default is None:
                raise KeyError
            else:
                return default
        return elem.get('value')