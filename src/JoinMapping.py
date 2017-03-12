from CompositeMapping import BaseMapping


class JoinMapping(BaseMapping):
    def __init__(self, *args, **kwargs):
        """
        Create a new mapping that joins multiple fields together
        :param joinchar:
        :param args:
        """
        super(JoinMapping,self).__init__(*args)
        self.joinchar = kwargs.get('joinchar',u'-')
        self.keylist = list(args)
        
    def evaluate(self, parser_instance, default="(unavailable)"):
        mappedlist = map(lambda key_entry: parser_instance.get(key_entry, default=default), self.keylist)
        return self.joinchar.join(mappedlist)