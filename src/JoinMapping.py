from BaseMapping import BaseMapping


class JoinMapping(BaseMapping):
    """
    Mapping that allows multiple keys to be joined together by a delimiter.
    Use like this:
    
    mappings = {
        u'key': JoinMapping('meta:keyone', 'media:keytwo', joinchar=',')
    }
    
    then you get the value:
    value = mappings['key'].evaluate(parser, default="none")
    
    #should return "valueone,valuetwo"
    """
    def __init__(self, *args, **kwargs):
        """
        Create a new mapping that joins multiple fields together.
        :param args: each argument is  key name to look up.
        :param joinchar: demlimiter to join the results together
        """
        super(JoinMapping,self).__init__(*args)
        self.joinchar = kwargs.get('joinchar',u'-')
        self.keylist = list(args)
        
    def evaluate(self, parser_instance, default="(unavailable)"):
        """
        Get the value for the key from the parser instance, or return the default value
        :param parser_instance: parser instance to look up from
        :param default: default value to return if the key does not exist in the Parser's data source
        :return: the value as a String
        """
        mappedlist = map(lambda key_entry: parser_instance.get(key_entry, default=default), self.keylist)
        return self.joinchar.join(mappedlist)