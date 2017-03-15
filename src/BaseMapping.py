class BaseMapping(object):
    """
    The simplest kind of mapping, which other types depend on.
    Initialise with a data key to map:
    mappings = {
        u'key': BaseMapping('meta:keyname')
    }
    
    then you can evaluate against a Parser instance like this:
    value = mappings['key'].evaluate(parser, default="my default")
    """
    def __init__(self, *args):
        """
        Initialise.
        :param key: key to look up in the Parser
        """
        self.key = args[0]
        
    def evaluate(self, parser_instance, default="(unavailable)"):
        """
        Get the value for the key from the parser instance, or return the default value
        :param parser_instance: parser instance to look up from
        :param default: default value to return if the key does not exist in the Parser's data source
        :return: the value as a String
        """
        return parser_instance.get(self.key,default)