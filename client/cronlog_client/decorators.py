from functools import wraps

from cronlog_client import CronLogClient
from cronlog_client.states import CronState

def log_cron_status(command_name):
    '''
    :param command_name: name of the cron job that needs to logged
    When a function is wrapped with this decorator, it sends
    two requests to tracelog server which updates status of
    the cron.
    For now it supports to statuses
    1. Started
    2. Finished
    '''
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            CronLogClient.log(command_name, CronState.CRON_STARTED)
            val = f(*args, **kwargs)
            CronLogClient.log(command_name, CronState.CRON_FINISHED)
            return val
        return wrapper
    return decorator


def log_cls_cron_status(command_name):
    '''
    :param command_name: name of the cron job that needs to logged
    When a class method is wrapped with this decorator, it sends
    two requests to tracelog server which updates status of
    the cron.
    For now it supports to statuses
    1. Started
    2. Finished
    '''
    def decorator(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            CronLogClient.log(command_name, CronState.CRON_STARTED)
            val = f(self, *args, **kwargs)
            CronLogClient.log(command_name, CronState.CRON_FINISHED)
            return val
        return wrapper
    return decorator
