"""Module contains a simple python application which forwards a zmq message between two queues."""
import argparse
import collections
import os
import sys

import yaml
import zmq

from simple_app import errors


__all__ = (  # Listing in __all__ is very arbitrary since this is a simple example
    'load_yaml_file',
    'build_configuration'
)


DEFAULT_CONFIG = {
    'zmq_rx_addr': 'tcp://0.0.0.0:8888',
    'zmq_tx_addr': 'tcp://0.0.0.0:9999',
    'zmq_message_suffix': '',
}


def load_yaml_file(yaml_file_path):
    """
    Return yaml file configuration as dictionary.

    If file does not exist, an empty dictionary will be returned.
    """
    try:
        with open(yaml_file_path) as yaml_fd:
            return yaml.load(yaml_fd, Loader=yaml.SafeLoader) or {}
    except FileNotFoundError:
        return {}
    except yaml.YAMLError as yaml_error:
        raise errors.InvalidConfigurationError(yaml_error)


def build_configuration(config_path=None):
    """Construct a map of config keys and values based on provided config_path, env, and default values."""
    return collections.ChainMap(
        load_yaml_file(config_path) if config_path else {},  # CLI provided config is highest priority config
        {key.lower(): os.environ[key] for key in os.environ if key.lower() in DEFAULT_CONFIG},
        DEFAULT_CONFIG,  # code default configuration is lowest priorty config
    )


def zmq_forwarder(zmq_rx_addr, zmq_tx_addr, zmq_message_suffix):
    """Forward messages received on rx socket to tx socket indefinitely."""
    context = zmq.Context()

    rx_socket = context.socket(zmq.PULL)
    rx_socket.connect(zmq_rx_addr)

    tx_socket = context.socket(zmq.PUSH)
    tx_socket.connect(zmq_tx_addr)

    while True:
        message = rx_socket.recv_string()
        tx_socket.send_string(message + zmq_message_suffix)


def main():
    """Parse command line arguments and start simple zmq forwarding application."""
    parser = argparse.ArgumentParser(description='A simple zmq forwarder.')
    parser.add_argument('config', nargs='?', default=None, help='Path to yaml configuration file.')
    args = parser.parse_args()

    conf = build_configuration(args.config)
    return zmq_forwarder(**conf)


if __name__ == '__main__':
    sys.exit(main())
