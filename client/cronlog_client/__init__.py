import datetime
import json

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from cronlog_client.cronlog import CronLogService

class CronLogClient(object):
    hostname = 'localhost'
    port = 9002
    timeout = 5 # In seconds

    @classmethod
    def new_transport(cls, host=None, port=None):
        # Use defaults if host, port not provided
        host = host if host else cls.hostname
        port = port if port else cls.port

        # Make socket
        socket = TSocket.TSocket(host, port)

        # Set timeout
        socket.setTimeout(cls.timeout * 1000.0)

        # Buffering is critical. Raw sockets are very slow
        transport = TTransport.TFramedTransport(socket)

        # Wrap in a protocol
        protocol = TBinaryProtocol.TBinaryProtocol(transport)

        # Create a client to use the protocol encoder
        client = CronLogService.Client(protocol)

        # Connect!
        transport.open()
        return transport, client

    @classmethod
    def log(cls, command_name, state, context=None, host=None, port=None):
        try:
            transport, client = cls.new_transport(host=host, port=port)
        except:
            return

        if context and not isinstance(context, dict):
            raise Exception("Context should be of <type 'dict'>")

        if state and not isinstance(state, dict):
            raise Exception("state should be of <type 'dict'> with 'value', 'state_verbose' as keys")

        state, state_verbose = state['state'], state['state_verbose']

        log_timestamp = datetime.datetime.utcnow()

        kwargs = {
            'command_name': command_name,
            'log_timestamp': log_timestamp.isoformat(),
            'state': state,
            'state_verbose': state_verbose,
            'context': context,
            #'hostname': transport.getfqdn(),
        }

        message = json.dumps(kwargs)
        result = client.crlog(message)
        transport.close()
        return result
