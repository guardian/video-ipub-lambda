class NoMappingFound(StandardError):
    pass


class Mapper(object):
    #make sure that this list has the same number of entries as FIELD_MAPPINGS.
    FIELD_MULTIPLIERS = [
        {
            u'abitrate': 1,
            u'vbitrate': 1
        },
        {
            u'abitrate': 0.001,
            u'vbitrate': 0.001
        },
        {
            u'abitrate': 1,
            u'vbitrate': 1
        }
    ]
    
    FIELD_MAPPINGS = [
        {   #old-skool mapping
            u'abitrate'    : u'track:audi:bitrate',
            u'acodec'      : u'track:audi:format',
            u'aspect'      : u'meta:aspect_ratio',
            u'duration'    : u'movie:duration',
            u'fcs_id'      : u'meta:FCS asset ID',
            u'file_size'   : u'movie:size',
            u'format'      : u'movie:format',
            u'frame_height': u'track:vide:height',
            u'frame_width' : u'track:vide:width',
            u'mobile'      : u'meta:for_mobile',
            u'multirate'   : u'meta:is_multirate',
            u'octopus_id'  : u'meta:octopus ID',
            u'url'         : u'meta:cdn_url',
            u'vbitrate'    : u'track:vide:bitrate',
            u'vcodec'      : u'track:vide:format',
            u'filename'    : u'filename'
        },
        {   #Elemental encoder mapping
            u'abitrate'    : u'track:audi:aac_settings_bitrate',
            u'acodec'      : u'track:audi:codec',
            u'aspect'      : u'meta:aspect_ratio',
            u'duration'    : u'meta:durationSeconds',
            u'fcs_id'      : u'meta:itemId',
            u'file_size'   : u'movie:size',
            u'format'      : u'movie:extension',
            u'frame_height': u'track:vide:height',
            u'frame_width' : u'track:vide:width',
            u'mobile'      : u'meta:for_mobile',
            u'multirate'   : u'meta:is_multirate',
            u'octopus_id'  : u'meta:gnm_master_generic_titleid',
            u'url'         : u'meta:cdn_url',
            u'vbitrate'    : u'track:vide:h264_settings_bitrate',
            u'vcodec'      : u'track:vide:codec',
            u'originalFilename': u'originalFilename',
            u'project': u'__collection'
        },
        {   #Elastic Transcoder mapping
            u'abitrate'        : u'track:audi:bitrate',
            u'acodec'          : u'track:audi:format',
            u'aspect'          : u'meta:aspect_ratio',
            u'duration'        : u'meta:durationSeconds',
            u'fcs_id'          : u'meta:itemId',
            u'file_size'       : u'movie:size',
            u'format'          : u'movie:extension',
            u'frame_height'    : u'track:vide:height',
            u'frame_width'     : u'track:vide:width',
            u'mobile'          : u'meta:for_mobile',
            u'multirate'       : u'meta:is_multirate',
            u'octopus_id'      : u'meta:gnm_master_generic_titleid',
            u'url'             : u'meta:cdn_url',
            u'vbitrate'        : u'track:vide:bitrate',
            u'vcodec'          : u'track:vide:format',
            u'originalFilename': u'originalFilename',
            u'project': u'__collection'
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
            parser_instance.get(mappingentry[1],
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