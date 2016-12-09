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
            u'vcodec'      : u'track:vide:format'
        },
        {
            u'abitrate'    : u'tracks:audi:aac_settings_bitrate',
            u'acodec'      : u'tracks:audi:codec',
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
            u'vcodec'      : u'track:vide:codec'
        }
    ]

    def _do_mapping(self, mappingdict, parser_instance):
        return dict(map(lambda item: (item[0],parser_instance.get(item[1])),mappingdict.items()))
        
    def map_metadata(self, parser_instance):
        failed_mappings = []
        for mappingdict in self.FIELD_MAPPINGS:
            try:
                return self._do_mapping(mappingdict,parser_instance)
            except KeyError as e:
                failed_mappings.append(str(e))
                pass
        #if we got here then all of the mappings failed
        raise NoMappingFound("No mapping matched the provided metadata.  Failed mappings were: {0}".format(failed_mappings))