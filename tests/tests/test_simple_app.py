"""Module contains component tests for simple_app service/container."""


def test_initial_configuration(simple_app):
    """Verify that application does not append any suffix to message with base configuration."""
    assert not simple_app.consul_get('zmq_message_suffix')

    simple_app.write_service_input('simple string')
    assert simple_app.read_service_output() == 'simple string'


def test_basic_consul_templating(simple_app):
    """Verify changes in consul configuration cause simple_app to update and use latest values."""
    simple_app.write_service_input('hello')
    assert simple_app.read_service_output() == 'hello'

    simple_app.consul_set('zmq_message_suffix', ' world!')

    simple_app.wait_for_template_update()

    simple_app.write_service_input('hello')
    assert simple_app.read_service_output() == 'hello world!'
