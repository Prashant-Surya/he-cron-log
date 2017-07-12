import click

from thrift.protocol import TBinaryProtocol
from thrift.server import TNonblockingServer
from thrift.transport import TSocket
from thrift.transport import TTransport

from cronlog import CronLogService
from cronlog_handler import CronLogServiceHandler


clog = click.Group()

@clog.command()
@click.option('--port', default=9002, help='Thirft server port')
def start_clog_service(port):
    handler = CronLogServiceHandler()
    processor = CronLogService.Processor(handler)
    transport = TSocket.TServerSocket(port=port)
    tfactory = TTransport.TBufferedTransportFactory()
    tfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TNonblockingServer.TNonblockingServer(
        processor, transport, threads=20)
    print "Cassandra Log Server Running on port {port}...".format(port=port)
    server.serve()


if __name__ == '__main__':
    try:
        start_clog_service()
    except KeyboardInterrupt:
        print "Server interrupted."

