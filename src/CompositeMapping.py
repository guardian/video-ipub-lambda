class BaseMapping(object):
    def __init__(self, *args):
        self.key = args[0]
        
    def evaluate(self, parser_instance, default="(unavailable)"):
        return parser_instance.get(self.key,default)