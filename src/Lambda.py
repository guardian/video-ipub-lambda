#!/usr/bin/env python
import logging
import traceback
import raven
LOGFORMAT = '%(asctime)-15s - %(name)s [%(threadName)s] %(funcName)s - %(levelname)s - %(message)s'
main_log_level = logging.DEBUG

logging.basicConfig(level=main_log_level,format=LOGFORMAT)


def handler(event, context):
    from Parser import Parser
    from Mapper import Mapper
    from pprint import pprint
    import config
    if hasattr(config,'RAVEN_DSN') and config.RAVEN_DSN!="":
        raven_client = raven.Client(config.RAVEN_DSN)
    else:
        raven_client = None
        
    logging.info("Event handler triggered")
    print "Event was {0}".format(event)
        
    for record in event['Records']:
        try:
            document = Parser(record['Sns']['Message'])
            m = Mapper()
            mapped_data = m.map_metadata(document)
            pprint(mapped_data)
        except Exception as e:
            logging.error(traceback.format_exc())
            if raven_client:
                raven_client.user_context(event)
                raven_client.captureException()