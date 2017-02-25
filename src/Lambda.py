#!/usr/bin/env python
import logging
import traceback
import raven
LOGFORMAT = '%(asctime)-15s - %(name)s [%(threadName)s] %(funcName)s - %(levelname)s - %(message)s'
main_log_level = logging.DEBUG

def handler(event, context):
    from Parser import Parser
    from Mapper import Mapper
    from Database import Database
    from pprint import pprint
    import config
    from os import environ

    logging.basicConfig(level=main_log_level, format=LOGFORMAT)
    
    if 'RAVEN_DSN' in environ:
        raven_client = raven.Client(environ['RAVEN_DSN'])
        print "Raven intialised at {0}".format(environ['RAVEN_DSN'])
    else:
        raven_client = None
    
    logging.info("Event handler triggered")
    print "Event was {0}".format(event)
    
    try:
        db = Database({
            'user': environ['DB_USER'],
            'password': environ['DB_PASSWD'],
            'host': environ['DB_HOST'],
            'database': environ['DB_NAME'],
            'use_pure': False
        })
        
    except Exception as e:
        logging.error(traceback.format_exc())
        if raven_client:
            raven_client.user_context(event)
            raven_client.captureException()
        raise
    
    for record in event['Records']:
        document = "(not yet parsed)"
        try:
            document = Parser(record['Sns']['Message'])
            m = Mapper()
            mapped_data = m.map_metadata(document)
            pprint(mapped_data)
            
            content_id = db.get_contentid(mapped_data)
            db.add_encoding(content_id,mapped_data)
            
        except Exception as e:
            logging.error(traceback.format_exc())
            logging.error("Incoming metadata was:")
            logging.error(str(document))
            
            if raven_client:
                print "Logging to Raven"
                try:
                    raven_client.extra_context({'source': record['Sns']['Message']})
                except:
                    raven_client.extra_context({'source': '(not available)'})
                raven_client.captureException()