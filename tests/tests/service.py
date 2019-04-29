"""Module contains interface class for modifying and interacting with simple_app service during testing."""
import os

import consul
import zmq


def join(*args):
    return '/'.join(args)


class SimpleApp(object):
    """Testing interface to SimpleApp service running within container under test (CUT)"""

    CONSUL_HOST = os.environ.get('CONSUL_HOST', '0.0.0.0')
    CONSUL_PORT = os.environ.get('CONSUL_PORT', 8500)
    CONSUL_SCHEME = os.environ.get('CONSUL_SCHEME', 'http')
    CONSUL_SIMPLE_APP_PREFIX = 'simple_app'

    DEFAULT_ZMQ_INPUT_ADDR = 'tcp://0.0.0.0:8888'
    DEFAULT_ZMQ_OUTPUT_ADDR = 'tcp://0.0.0.0:9999'

    def __init__(self,
                 host=CONSUL_HOST,
                 port=CONSUL_PORT,
                 scheme=CONSUL_SCHEME,
                 prefix=CONSUL_SIMPLE_APP_PREFIX):
        """Initialize required instance variables for interfacing with simple app service."""
        self.consul_prefix = prefix
        self.consul = consul.Consul(host=host, port=port, scheme=scheme)
        self._wait_for_leader_election()

        self.zmq_input_addr = self.DEFAULT_ZMQ_INPUT_ADDR
        self.zmq_output_addr = self.DEFAULT_ZMQ_OUTPUT_ADDR

        self.zmq_context = None
        self.zmq_input_socket = None
        self.zmq_output_socket = None

    def _wait_for_leader_election(self):
        """Wait until leader election has occurred so consul cluster can be used."""
        leader = None
        while not leader:
            try:
                leader = self.consul.status.leader()
            except consul.ConsulException:
                pass

    def __enter__(self):
        """Perform any setup required before entering each test."""
        self.zmq_context = zmq.Context()
        self.zmq_input_socket = self.zmq_context.socket(zmq.PUSH)
        self.zmq_input_socket.bind(self.zmq_input_addr)
        self.zmq_output_socket = self.zmq_context.socket(zmq.PULL)
        self.zmq_output_socket.bind(self.zmq_output_addr)
        return self

    def __exit__(self, *args, **kwargs):
        """Cleanup any changes made during the current test."""
        self.zmq_input_socket.close()
        self.zmq_output_socket.close()
        self.zmq_context.term()

        self.consul.kv.delete(self.consul_prefix, recurse=True)

    def consul_set(self, key, value):
        """Set key-value pair in simple app partition of consul KV store."""
        self.consul.kv.put(join(self.consul_prefix, key), value)

    def consul_get(self, key):
        """Return value associated with key in simple_app partition of consul KV store."""
        _, data = self.consul.kv.get(join(self.consul_prefix, key))
        return data['Value'] if data else None

    def consul_del(self, key):
        """Clear key from simple_app partition of consul KV store."""
        self.consul.kv.delete(join(self.consul_prefix, key))

    def read_service_output(self, timeout=None, poll_interval=50):
        """
        Read output string from service.

        If timeout is not set then the read will block indefinitely until a message is received.

        :param timeout: int - milliseconds to wait to receive output message
        :param poll_interval: int - milliseconds to wait in between socket polls
        :return string:
        """
        elapsed_ms = 0
        poller = zmq.Poller()
        poller.register(self.zmq_output_socket, zmq.POLLIN)

        while not timeout or elapsed_ms < timeout:
            socks = dict(poller.poll(poll_interval))
            if socks and socks.get(self.zmq_output_socket) == zmq.POLLIN:
                return self.zmq_output_socket.recv_string(zmq.NOBLOCK)

            elapsed_ms += poll_interval
        else:
            raise TimeoutError('Unable to read any output message within timeout {0}'.format(timeout))

    def write_service_input(self, message):
        """Write byte string message to simple_app input socket."""
        self.zmq_input_socket.send_string(message)
