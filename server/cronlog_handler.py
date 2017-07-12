import dateutil.parser
import json

from constants import DEBUG
from models import setup_connection
from models import CronTraceByCron

try:
    from machine_settings import *
except ImportError:
    pass


class CronLogServiceHandler(object):
    def __init__(self, *args, **kwargs):
        setup_connection()

    def crlog(self, message):
        if DEBUG: print 'Received Message: ', message
        payload = json.loads(message)
        context = payload.get('context')
        ctx = {}
        if context:
            for key, value in context.iteritems():
                ctx[unicode(key)] = unicode(value)
        payload['context'] = ctx
        log_timestamp = dateutil.parser.parse(payload['log_timestamp'])
        payload['log_timestamp'] = log_timestamp
        CronTraceByCron.log(**payload)
        CronTraceByCron.log(**payload)
