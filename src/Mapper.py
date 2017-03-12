from BaseMapping import BaseMapping
from JoinMapping import JoinMapping


class NoMappingFound(StandardError):
    pass


class Mapper(object):
    FIELD_MULTIPLIERS = [
        {
            u'abitrate': 1,
            u'vbitrate': 1
        },
        {
            u'abitrate': 0.001,
            u'vbitrate': 0.001
        }
    ]
    
    FIELD_MAPPINGS = [
        {
            u'abitrate'    : BaseMapping(u'track:audi:bitrate'),
            u'acodec'      : BaseMapping(u'track:audi:format'),
            u'aspect'      : BaseMapping(u'meta:aspect_ratio'),
            u'duration'    : BaseMapping(u'movie:duration'),
            u'fcs_id'      : BaseMapping(u'meta:FCS asset ID'),
            u'file_size'   : BaseMapping(u'movie:size'),
            u'format'      : BaseMapping(u'movie:format'),
            u'frame_height': BaseMapping(u'track:vide:height'),
            u'frame_width' : BaseMapping(u'track:vide:width'),
            u'mobile'      : BaseMapping(u'meta:for_mobile'),
            u'multirate'   : BaseMapping(u'meta:is_multirate'),
            u'octopus_id'  : BaseMapping(u'meta:octopus ID'),
            u'url'         : BaseMapping(u'meta:cdn_url'),
            u'vbitrate'    : BaseMapping(u'track:vide:bitrate'),
            u'vcodec'      : BaseMapping(u'track:vide:format')
        },
        {
            u'abitrate'    : BaseMapping(u'tracks:audi:aac_settings_bitrate'),
            u'acodec'      : BaseMapping(u'tracks:audi:codec'),
            u'aspect'      : BaseMapping(u'meta:aspect_ratio'),
            u'duration'    : BaseMapping(u'meta:durationSeconds'),
            u'fcs_id'      : JoinMapping(u'meta:itemId',u'meta:__version'),
            u'file_size'   : BaseMapping(u'movie:size'),
            u'format'      : BaseMapping(u'movie:extension'),
            u'frame_height': BaseMapping(u'track:vide:height'),
            u'frame_width' : BaseMapping(u'track:vide:width'),
            u'mobile'      : BaseMapping(u'meta:for_mobile'),
            u'multirate'   : BaseMapping(u'meta:is_multirate'),
            u'octopus_id'  : BaseMapping(u'meta:gnm_master_generic_titleid'),
            u'url'         : BaseMapping(u'meta:cdn_url'),
            u'vbitrate'    : BaseMapping(u'track:vide:h264_settings_bitrate'),
            u'vcodec'      : BaseMapping(u'track:vide:codec')
        }
    ]

    FIELD_DEFAULTS = {
        u'mobile': '0',
        u'multirate': '0',
        u'aspect': '16x9'
    }
    
    def _do_mapping(self, mappingdict, parser_instance):
        return dict(map(lambda mappingentry: (
            mappingentry[0],
            mappingentry[1].evaluate(parser_instance,
                                    default=self.FIELD_DEFAULTS[mappingentry[0]] if mappingentry[0] in self.FIELD_DEFAULTS else None)
        ), mappingdict.items()))
        
    def map_metadata(self, parser_instance):
        applied_mapping=0
        failed_mappings = []
        for mappingdict in self.FIELD_MAPPINGS:
            try:
                mapped_data = self._do_mapping(mappingdict,parser_instance)
                for k,v in mapped_data.items():
                    if k in self.FIELD_MULTIPLIERS[applied_mapping]:
                        mapped_data[k] = float(mapped_data[k]) * self.FIELD_MULTIPLIERS[applied_mapping][k]
                return mapped_data
            except KeyError as e:
                applied_mapping +=1
                failed_mappings.append(str(e))
                pass
        #if we got here then all of the mappings failed
        raise NoMappingFound("No mapping matched the provided metadata.  Failed mappings were: {0}".format(failed_mappings))
    
if __name__ == "__main__":
    from sys import argv
    from Parser import Parser
    from pprint import pprint
    
    print "Testing mappings from source file {0}".format(argv[1])
    with open(argv[1]) as f:
        p = Parser(f.read())
        m = Mapper()
        print "Mapping results:"
        pprint(m.map_metadata(p))