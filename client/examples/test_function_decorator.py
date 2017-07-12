from cronlog_client.decorators import log_cron_status

@log_cron_status('test_function')
def test_function():
    print "Inside test function"


test_function()
