from cronlog_client.decorators import log_cls_cron_status

class TestClass(object):

    @log_cls_cron_status('test_method')
    def test_method(self):
        print "inside test method"

if __name__ == '__main__':
    obj = TestClass()
    obj.test_method()
