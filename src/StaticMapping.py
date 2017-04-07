from BaseMapping import BaseMapping


class StaticMapping(BaseMapping):
    def __init__(self,value,*args,**kwargs):
        super(StaticMapping, self).__init__(*args,**kwargs)
        self.value = value

    def evaluate(self, parser_instance, default="(unavailable)"):
        return self.value