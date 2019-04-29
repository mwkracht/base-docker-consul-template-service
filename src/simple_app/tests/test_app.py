"""
Module contains test cases for app submodule of simple_app package.

Unit tests in example app are provided as basic examples and are not written for maximum coverage.
"""
import mock
import pytest

import simple_app


def test_load_yaml_file_no_file():
    """Verify method returns empty dictionary if no file is found."""
    yaml_content = simple_app.load_yaml_file('non-existent-file.yaml')
    assert yaml_content == {}


def test_load_yaml_file_valid_yaml_file(tmpdir):
    """Verify method returns dictionary equivalent of yaml file content."""
    yaml_file = tmpdir.join('test.yaml')
    yaml_file.write('---\nsimple_key: simple_value\n')

    yaml_content = simple_app.load_yaml_file(yaml_file)
    assert yaml_content == {
        'simple_key': 'simple_value'
    }


def test_load_yaml_file_empty_yaml_file(tmpdir):
    """Verify method returns empty dictionary if yaml file is empty."""
    yaml_file = tmpdir.join('test.yaml')
    yaml_file.write('---\n')

    yaml_content = simple_app.load_yaml_file(yaml_file)
    assert yaml_content == {}


def test_load_yaml_file_invalid_yaml_file(tmpdir):
    """Verify method raises exception when file contents cannot be parsed."""
    yaml_file = tmpdir.join('test.yaml')
    yaml_file.write('bad brackets: ][')

    with pytest.raises(simple_app.InvalidConfigurationError):
        simple_app.load_yaml_file(yaml_file)


def test_build_configuration_code_defaults():
    """Verify code defaults provide configuration when no CLI env configs are provided."""
    conf = simple_app.build_configuration()
    assert conf == {
        'zmq_rx_addr': 'tcp://0.0.0.0:8888',
        'zmq_tx_addr': 'tcp://0.0.0.0:9999',
        'zmq_message_suffix': '',
    }


def test_build_configuration_env_code_defaults(monkeypatch):
    """Verify env and code defaults are correctly prioritized when building configuration."""
    monkeypatch.setenv('ZMQ_MESSAGE_SUFFIX', 'env config')
    monkeypatch.setenv('EXCLUDE_THIS_VALUE', '4')  # env vars not in defaults must be excluded

    conf = simple_app.build_configuration()
    assert conf == {
        'zmq_rx_addr': 'tcp://0.0.0.0:8888',
        'zmq_tx_addr': 'tcp://0.0.0.0:9999',
        'zmq_message_suffix': 'env config',
    }


@mock.patch('simple_app.app.load_yaml_file')
def test_build_configuration_cli_env_code_defaults(mock_load_yaml, monkeypatch):
    """Verify configuration is correctly ordered based on all provided configuration inputs."""
    monkeypatch.setenv('ZMQ_RX_ADDR', 'tcp://localhost:1234')
    monkeypatch.setenv('ZMQ_TX_ADDR', 'tcp://localhost:9876')

    mock_load_yaml.return_value = {
        'zmq_rx_addr': 'ipc:///var/sockets/test.socket',
        'zmq_message_suffix': 'cli config'
    }

    conf = simple_app.build_configuration('dummy_config.yml')
    assert conf == {
        'zmq_rx_addr': 'ipc:///var/sockets/test.socket',
        'zmq_tx_addr': 'tcp://localhost:9876',
        'zmq_message_suffix': 'cli config',
    }
