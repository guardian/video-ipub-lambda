from BaseMapping import BaseMapping


class FormatMapping(BaseMapping):
    """
    Mapping that works like the .format() method on a string.

    Use like this:
    mappings = {
        u'key': FormatMapping('formatstring_with_{0}_or_{something}', 'media:keytwo', something={'meta:something'})
    }

    then you get the value:
    value = mappings['key'].evaluate(parser, default="none")

    #should return formatstring_with_valueone_or_valuetwo
    """

    def __init__(self, *args, **kwargs):
        super(FormatMapping,self).__init__(*args)

        self.formatstring = args[0]
        self.format_args = args[1:]
        self.format_kwargs = kwargs

    def __str__(self):
        return "FormatMapping: {0} [{1}], {{ {2} }}".format(self.formatstring, self.format_args, self.format_kwargs)

    def evaluate(self, parser_instance, default="(unavailable)"):
        mappedargs = map(lambda key_entry: parser_instance.get(key_entry, default=default), self.format_args)
        mappedkwargs = dict(
            map(
                lambda (k, v): (k, parser_instance.get(v, default=default)),
                self.format_kwargs.items()
            )
        )

        return self.formatstring.format(*mappedargs,**mappedkwargs)
