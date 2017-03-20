from BaseMapping import BaseMapping


class MIMEFormatMapping(BaseMapping):
    """
    Special mapping for the format field.  Mostly this is the mime-type; but detection of m3u8 comes through as
    text/plain so we must over-ride it.
    Usage:

    m = MIMEFormatMapping(u'meta:mime-type',u'meta:fall-back',prepend='video/')
    prepend/append are only used for the fallback field, if it does not contain a /
    """

    def __init__(self, *args, **kwargs):
        super(MIMEFormatMapping, self).__init__(*args)

        self.primary_field = args[0]
        self.fallback_field = args[1]
        self.prepend = kwargs['prepend'] if 'prepend' in kwargs else ""
        self.append = kwargs['append'] if 'append' in kwargs else ""

    def evaluate(self, parser_instance, default="text/plain"):
        primary = parser_instance.get(self.primary_field, default=default)
        if primary!="text/plain":
            return primary
        fallback = parser_instance.get(self.fallback_field, default=default)

        if '/' in fallback:
            return fallback
        else:
            return u"{0}{1}{2}".format(self.prepend,fallback,self.append)